"""
Token estimation without external dependencies.
Provides approximate token counting similar to tiktoken.
"""

import re
from typing import List


class SimpleTokenizer:
    """
    A simple tokenizer that approximates GPT tokenization.
    This is a lightweight implementation that provides reasonable estimates
    without requiring tiktoken or other heavy dependencies.
    """

    # Common contractions and patterns
    CONTRACTIONS = {
        "n't": 1, "'re": 1, "'ve": 1, "'ll": 1, "'d": 1, "'m": 1,
        "'s": 1, "'t": 1
    }

    # Common punctuation that often gets its own token
    PUNCTUATION = set('.,!?;:"()[]{}<>-–—/\\|@#$%^&*+=~`')

    def __init__(self):
        self._cache = {}

    def encode(self, text: str) -> List[int]:
        """
        Encode text into a list of token IDs (simulated).
        Returns a list where length equals estimated token count.
        """
        if not text:
            return []

        # Check cache
        if text in self._cache:
            return self._cache[text]

        tokens = []

        # Split on whitespace first
        words = text.split()

        for word in words:
            tokens.extend(self._tokenize_word(word))

        # Cache result
        self._cache[text] = tokens
        return tokens

    def _tokenize_word(self, word: str) -> List[int]:
        """Tokenize a single word into estimated tokens."""
        tokens = []

        # Handle contractions
        for contraction, _ in self.CONTRACTIONS.items():
            if word.endswith(contraction):
                base = word[:-len(contraction)]
                if base:
                    tokens.extend(self._split_into_subwords(base))
                tokens.append(1)  # contraction token
                return tokens

        # Handle punctuation at end
        while word and word[-1] in self.PUNCTUATION:
            tokens.append(1)
            word = word[:-1]

        # Handle punctuation at start
        while word and word[0] in self.PUNCTUATION:
            tokens.append(1)
            word = word[1:]

        if word:
            tokens.extend(self._split_into_subwords(word))

        return tokens

    def _split_into_subwords(self, word: str) -> List[int]:
        """
        Split word into subword tokens (simulating BPE-like behavior).
        """
        if not word:
            return []

        tokens = []

        # Very short words are usually single tokens
        if len(word) <= 3:
            return [1]

        # Long words get split
        if len(word) <= 6:
            return [1, 1]

        # Very long words get more splits
        # Approximate: every 4 characters is roughly a token
        num_tokens = max(2, len(word) // 4 + 1)
        return [1] * num_tokens

    def count_tokens(self, text: str) -> int:
        """Count the estimated number of tokens in text."""
        return len(self.encode(text))

    def decode(self, tokens: List[int]) -> str:
        """
        Decode tokens back to text (approximate).
        Note: This is a placeholder as we don't actually store the mapping.
        """
        return "<decoded text not available in estimation mode>"


class TokenCounter:
    """
    Unified token counting interface.
    Uses simple estimation by default.
    """

    def __init__(self):
        self.tokenizer = SimpleTokenizer()

    def count(self, text: str) -> int:
        """Count tokens in text."""
        if not text:
            return 0
        return self.tokenizer.count_tokens(text)

    def count_messages(self, messages: List[dict]) -> int:
        """Count tokens in a list of chat messages."""
        total = 0
        for msg in messages:
            # Add tokens for role
            total += self.count(msg.get('role', ''))
            # Add tokens for content
            total += self.count(msg.get('content', ''))
            # Add overhead per message
            total += 4
        # Add initial overhead
        total += 3
        return total


# Global instance for convenience
def count_tokens(text: str) -> int:
    """Quick function to count tokens."""
    counter = TokenCounter()
    return counter.count(text)
