"""
Compression strategies for different content types.
"""

import re
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class CompressionResult:
    """Result of a compression operation."""

    def __init__(self, original: str, compressed: str, strategy: str):
        self.original = original
        self.compressed = compressed
        self.strategy = strategy
        self.original_tokens = 0
        self.compressed_tokens = 0
        self.reduction_percent = 0.0

    def calculate_stats(self, token_counter):
        """Calculate compression statistics."""
        self.original_tokens = token_counter.count(self.original)
        self.compressed_tokens = token_counter.count(self.compressed)
        if self.original_tokens > 0:
            self.reduction_percent = (
                (self.original_tokens - self.compressed_tokens) / self.original_tokens * 100
            )


class BaseCompressor(ABC):
    """Base class for all compressors."""

    def __init__(self, token_counter):
        self.token_counter = token_counter

    @abstractmethod
    def compress(self, text: str, **kwargs) -> CompressionResult:
        """Compress the given text."""
        pass

    @abstractmethod
    def can_handle(self, text: str) -> bool:
        """Check if this compressor can handle the given text."""
        pass


class SmartTruncateCompressor(BaseCompressor):
    """
    Smart truncation compressor.
    Keeps the beginning and end, removes middle content.
    """

    def __init__(self, token_counter):
        super().__init__(token_counter)
        self.name = "smart_truncate"

    def can_handle(self, text: str) -> bool:
        return True

    def compress(self, text: str, keep_ratio: float = 0.3, **kwargs) -> CompressionResult:
        """
        Compress by keeping beginning and end, truncating middle.

        Args:
            text: Input text
            keep_ratio: Ratio of content to keep (0.0-1.0)
        """
        tokens = self.token_counter.count(text)
        target_tokens = int(tokens * keep_ratio)

        if target_tokens >= tokens:
            return CompressionResult(text, text, self.name)

        # Split into words
        words = text.split()
        total_words = len(words)

        if total_words <= 10:
            # Too short to truncate
            return CompressionResult(text, text, self.name)

        # Keep beginning and end
        keep_words = max(5, int(total_words * keep_ratio / 2))
        beginning = words[:keep_words]
        end = words[-keep_words:] if keep_words < total_words else []

        compressed = " ".join(beginning) + "\n\n... [content truncated] ...\n\n" + " ".join(end)

        result = CompressionResult(text, compressed, self.name)
        result.calculate_stats(self.token_counter)
        return result


class CodeCompressor(BaseCompressor):
    """
    Code-specific compressor.
    Removes comments, extra whitespace, and docstrings.
    """

    def __init__(self, token_counter):
        super().__init__(token_counter)
        self.name = "code"

    def can_handle(self, text: str) -> bool:
        # Check if text looks like code
        code_indicators = [
            'def ', 'class ', 'import ', 'function', 'const ', 'let ',
            'var ', '#include', 'using namespace', 'public class',
            'package ', 'module ', '<?php', '<html', '<!DOCTYPE'
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in code_indicators)

    def compress(self, text: str, preserve_comments: bool = False, **kwargs) -> CompressionResult:
        """Compress code by removing comments and extra whitespace."""
        lines = text.split('\n')
        compressed_lines = []

        in_multiline_comment = False
        multiline_end = None

        for line in lines:
            original_line = line
            stripped = line.strip()

            # Skip empty lines (but keep some for structure)
            if not stripped:
                if compressed_lines and compressed_lines[-1] != '':
                    compressed_lines.append('')
                continue

            # Handle Python docstrings and multiline strings
            if '"""' in line or "'''" in line:
                if not preserve_comments:
                    # Simple heuristic: remove lines with docstrings
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        continue
                    if stripped.endswith('"""') or stripped.endswith("'''"):
                        continue

            # Handle single-line comments
            if not preserve_comments:
                # Python/Ruby/Shell comments
                if '#' in line:
                    line = line[:line.index('#')]
                # C-style comments (simple handling)
                if '//' in line:
                    line = line[:line.index('//')]

            # Clean up trailing whitespace
            line = line.rstrip()

            if line or (compressed_lines and compressed_lines[-1] != ''):
                compressed_lines.append(line)

        # Remove consecutive empty lines
        cleaned_lines = []
        prev_empty = False
        for line in compressed_lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            cleaned_lines.append(line)
            prev_empty = is_empty

        compressed = '\n'.join(cleaned_lines)

        result = CompressionResult(text, compressed, self.name)
        result.calculate_stats(self.token_counter)
        return result


class JSONCompressor(BaseCompressor):
    """
    JSON-specific compressor.
    Minifies JSON by removing whitespace.
    """

    def __init__(self, token_counter):
        super().__init__(token_counter)
        self.name = "json"

    def can_handle(self, text: str) -> bool:
        text = text.strip()
        return (text.startswith('{') and text.endswith('}')) or \
               (text.startswith('[') and text.endswith(']'))

    def compress(self, text: str, **kwargs) -> CompressionResult:
        """Compress JSON by removing whitespace."""
        try:
            # Parse and re-serialize without whitespace
            data = json.loads(text)
            compressed = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        except json.JSONDecodeError:
            # Not valid JSON, return as-is
            compressed = text

        result = CompressionResult(text, compressed, self.name)
        result.calculate_stats(self.token_counter)
        return result


class LogCompressor(BaseCompressor):
    """
    Log file compressor.
    Removes duplicate patterns and timestamps.
    """

    def __init__(self, token_counter):
        super().__init__(token_counter)
        self.name = "log"
        # Common log timestamp patterns
        self.timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?',
            r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}',
            r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}',
            r'\d{2}:\d{2}:\d{2}\.\d+',
        ]

    def can_handle(self, text: str) -> bool:
        # Check if text looks like logs
        log_indicators = ['ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE', 'FATAL']
        lines = text.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            if any(level in line for level in log_indicators):
                return True
        return False

    def compress(self, text: str, remove_timestamps: bool = True, **kwargs) -> CompressionResult:
        """Compress log files by removing timestamps and deduplicating."""
        lines = text.split('\n')
        compressed_lines = []
        seen_patterns = set()

        for line in lines:
            if not line.strip():
                continue

            # Remove timestamps
            if remove_timestamps:
                for pattern in self.timestamp_patterns:
                    line = re.sub(pattern, '[T]', line)

            # Simple deduplication: check for similar error patterns
            simplified = re.sub(r'\d+', '#', line)

            if simplified not in seen_patterns:
                seen_patterns.add(simplified)
                compressed_lines.append(line)

        compressed = '\n'.join(compressed_lines)

        result = CompressionResult(text, compressed, self.name)
        result.calculate_stats(self.token_counter)
        return result


class MarkdownCompressor(BaseCompressor):
    """
    Markdown-specific compressor.
    Simplifies formatting while preserving structure.
    """

    def __init__(self, token_counter):
        super().__init__(token_counter)
        self.name = "markdown"

    def can_handle(self, text: str) -> bool:
        md_indicators = ['# ', '## ', '### ', '- ', '* ', '> ', '```', '---', '| ']
        return any(indicator in text for indicator in md_indicators)

    def compress(self, text: str, **kwargs) -> CompressionResult:
        """Compress markdown by simplifying formatting."""
        lines = text.split('\n')
        compressed_lines = []

        in_code_block = False

        for line in lines:
            stripped = line.strip()

            # Handle code blocks
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                compressed_lines.append(line)
                continue

            if in_code_block:
                compressed_lines.append(line)
                continue

            # Simplify headings (keep # but remove extra formatting)
            if stripped.startswith('#'):
                compressed_lines.append(stripped)
                continue

            # Simplify lists
            if re.match(r'^\s*[-*+]\s', stripped):
                compressed_lines.append(re.sub(r'^\s*', '- ', stripped.lstrip()))
                continue

            # Remove horizontal rules
            if stripped == '---' or stripped == '***' or stripped == '___':
                continue

            # Simplify links [text](url) -> text
            line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)

            # Simplify images ![alt](url) -> [image: alt]
            line = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'[image: \1]', line)

            # Remove bold/italic markers but keep text
            line = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\1', line)
            line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            line = re.sub(r'\*([^*]+)\*', r'\1', line)
            line = re.sub(r'__([^_]+)__', r'\1', line)
            line = re.sub(r'_([^_]+)_', r'\1', line)

            if stripped:
                compressed_lines.append(line)

        compressed = '\n'.join(compressed_lines)

        result = CompressionResult(text, compressed, self.name)
        result.calculate_stats(self.token_counter)
        return result


class SemanticCompressor(BaseCompressor):
    """
    Semantic compression using extractive summarization.
    Keeps only the most important sentences.
    """

    def __init__(self, token_counter):
        super().__init__(token_counter)
        self.name = "semantic"

    def can_handle(self, text: str) -> bool:
        return len(text) > 200  # Only for longer texts

    def compress(self, text: str, keep_ratio: float = 0.3, **kwargs) -> CompressionResult:
        """
        Compress by keeping important sentences.
        Uses simple heuristics: sentence position and keyword density.
        """
        # Split into sentences (simple heuristic)
        sentences = re.split(r'(?<=[.!?])\s+', text)

        if len(sentences) <= 3:
            return CompressionResult(text, text, self.name)

        # Score sentences
        scored_sentences = []
        for i, sent in enumerate(sentences):
            score = self._score_sentence(sent, i, len(sentences))
            scored_sentences.append((score, sent))

        # Sort by score and keep top ones
        scored_sentences.sort(reverse=True)
        keep_count = max(1, int(len(sentences) * keep_ratio))
        top_sentences = scored_sentences[:keep_count]

        # Restore original order
        top_sentences.sort(key=lambda x: sentences.index(x[1]))

        compressed = ' '.join([s[1] for s in top_sentences])

        result = CompressionResult(text, compressed, self.name)
        result.calculate_stats(self.token_counter)
        return result

    def _score_sentence(self, sentence: str, position: int, total: int) -> float:
        """Score a sentence based on various heuristics."""
        score = 0.0

        # Position scoring (first and last sentences are often important)
        if position == 0:
            score += 3.0
        elif position == total - 1:
            score += 2.0
        elif position < total * 0.2:  # Early sentences
            score += 1.0

        # Length scoring (avoid very short or very long sentences)
        words = len(sentence.split())
        if 5 <= words <= 25:
            score += 1.0

        # Keyword scoring (sentences with important words)
        important_words = ['important', 'key', 'main', 'critical', 'essential',
                          'significant', 'crucial', 'primary', 'major', 'vital']
        sentence_lower = sentence.lower()
        for word in important_words:
            if word in sentence_lower:
                score += 0.5

        return score


class CompressorRegistry:
    """Registry of available compressors."""

    def __init__(self, token_counter):
        self.token_counter = token_counter
        self.compressors = {
            'smart_truncate': SmartTruncateCompressor(token_counter),
            'code': CodeCompressor(token_counter),
            'json': JSONCompressor(token_counter),
            'log': LogCompressor(token_counter),
            'markdown': MarkdownCompressor(token_counter),
            'semantic': SemanticCompressor(token_counter),
        }

    def get_compressor(self, name: str) -> Optional[BaseCompressor]:
        """Get a compressor by name."""
        return self.compressors.get(name)

    def auto_detect(self, text: str) -> Optional[BaseCompressor]:
        """Auto-detect the best compressor for the text."""
        for name, compressor in self.compressors.items():
            if name != 'smart_truncate' and compressor.can_handle(text):
                return compressor
        return self.compressors['smart_truncate']

    def list_compressors(self) -> Dict[str, str]:
        """List available compressors with descriptions."""
        return {
            'smart_truncate': 'Keep beginning and end, truncate middle',
            'code': 'Remove comments and whitespace from code',
            'json': 'Minify JSON by removing whitespace',
            'log': 'Remove timestamps and deduplicate logs',
            'markdown': 'Simplify markdown formatting',
            'semantic': 'Extractive summarization of text',
            'auto': 'Auto-detect best strategy',
        }
