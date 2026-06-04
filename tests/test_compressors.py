"""Tests for the compressors module."""

import unittest
from tokensqueeze.tokenizer import TokenCounter
from tokensqueeze.compressors import (
    SmartTruncateCompressor,
    CodeCompressor,
    JSONCompressor,
    LogCompressor,
    MarkdownCompressor,
    SemanticCompressor,
    CompressorRegistry,
)


class TestSmartTruncateCompressor(unittest.TestCase):
    """Test cases for SmartTruncateCompressor."""

    def setUp(self):
        self.compressor = SmartTruncateCompressor(TokenCounter())

    def test_can_handle_any(self):
        """Test that it can handle any text."""
        self.assertTrue(self.compressor.can_handle("any text"))

    def test_compress_short_text(self):
        """Test compressing short text."""
        text = "hello world"
        result = self.compressor.compress(text)
        self.assertEqual(result.original, text)
        self.assertEqual(result.strategy, "smart_truncate")

    def test_compress_long_text(self):
        """Test compressing long text."""
        text = " ".join([f"word{i}" for i in range(100)])
        result = self.compressor.compress(text, keep_ratio=0.3)
        self.assertIn("truncated", result.compressed)


class TestCodeCompressor(unittest.TestCase):
    """Test cases for CodeCompressor."""

    def setUp(self):
        self.compressor = CodeCompressor(TokenCounter())

    def test_can_handle_code(self):
        """Test detecting code."""
        self.assertTrue(self.compressor.can_handle("def hello():\n    pass"))
        self.assertTrue(self.compressor.can_handle("import os"))

    def test_can_handle_non_code(self):
        """Test rejecting non-code."""
        self.assertFalse(self.compressor.can_handle("hello world"))

    def test_compress_code(self):
        """Test compressing code."""
        code = """def hello():
    # This is a comment
    print("hello")
    return 42
"""
        result = self.compressor.compress(code)
        self.assertNotIn("# This is a comment", result.compressed)


class TestJSONCompressor(unittest.TestCase):
    """Test cases for JSONCompressor."""

    def setUp(self):
        self.compressor = JSONCompressor(TokenCounter())

    def test_can_handle_json(self):
        """Test detecting JSON."""
        self.assertTrue(self.compressor.can_handle('{"key": "value"}'))
        self.assertTrue(self.compressor.can_handle('[1, 2, 3]'))

    def test_can_handle_non_json(self):
        """Test rejecting non-JSON."""
        self.assertFalse(self.compressor.can_handle("hello world"))

    def test_compress_json(self):
        """Test compressing JSON."""
        json_text = '{\n  "key": "value",\n  "num": 123\n}'
        result = self.compressor.compress(json_text)
        self.assertNotIn("\n", result.compressed)

    def test_invalid_json(self):
        """Test handling invalid JSON."""
        text = "{invalid json"
        result = self.compressor.compress(text)
        self.assertEqual(result.compressed, text)


class TestLogCompressor(unittest.TestCase):
    """Test cases for LogCompressor."""

    def setUp(self):
        self.compressor = LogCompressor(TokenCounter())

    def test_can_handle_logs(self):
        """Test detecting logs."""
        self.assertTrue(self.compressor.can_handle("2024-01-01 ERROR something"))
        self.assertTrue(self.compressor.can_handle("INFO: starting service"))

    def test_compress_logs(self):
        """Test compressing logs."""
        logs = """2024-01-01 10:00:00 ERROR something failed
2024-01-01 10:00:01 INFO retrying
2024-01-01 10:00:02 ERROR something failed
"""
        result = self.compressor.compress(logs)
        self.assertIn("[T]", result.compressed)


class TestMarkdownCompressor(unittest.TestCase):
    """Test cases for MarkdownCompressor."""

    def setUp(self):
        self.compressor = MarkdownCompressor(TokenCounter())

    def test_can_handle_markdown(self):
        """Test detecting markdown."""
        self.assertTrue(self.compressor.can_handle("# Heading\n\nText"))
        self.assertTrue(self.compressor.can_handle("- list item"))

    def test_compress_markdown(self):
        """Test compressing markdown."""
        md = """# Title

Some **bold** text.

---

[link](http://example.com)
"""
        result = self.compressor.compress(md)
        self.assertNotIn("---", result.compressed)
        self.assertNotIn("[link](http://example.com)", result.compressed)


class TestSemanticCompressor(unittest.TestCase):
    """Test cases for SemanticCompressor."""

    def setUp(self):
        self.compressor = SemanticCompressor(TokenCounter())

    def test_can_handle_long_text(self):
        """Test handling long text."""
        text = " ".join([f"sentence{i}" for i in range(50)])
        self.assertTrue(self.compressor.can_handle(text))

    def test_can_handle_short_text(self):
        """Test rejecting short text."""
        self.assertFalse(self.compressor.can_handle("short"))

    def test_compress_text(self):
        """Test compressing text."""
        text = "First sentence. Second sentence. Third sentence. " * 10
        result = self.compressor.compress(text, keep_ratio=0.5)
        self.assertLess(len(result.compressed), len(result.original))


class TestCompressorRegistry(unittest.TestCase):
    """Test cases for CompressorRegistry."""

    def setUp(self):
        self.registry = CompressorRegistry(TokenCounter())

    def test_get_compressor(self):
        """Test getting compressors."""
        self.assertIsNotNone(self.registry.get_compressor("code"))
        self.assertIsNone(self.registry.get_compressor("nonexistent"))

    def test_auto_detect_code(self):
        """Test auto-detecting code."""
        compressor = self.registry.auto_detect("def hello(): pass")
        self.assertEqual(compressor.name, "code")

    def test_auto_detect_json(self):
        """Test auto-detecting JSON."""
        compressor = self.registry.auto_detect('{"key": "value"}')
        self.assertEqual(compressor.name, "json")

    def test_list_compressors(self):
        """Test listing compressors."""
        compressors = self.registry.list_compressors()
        self.assertIn("code", compressors)
        self.assertIn("json", compressors)


if __name__ == '__main__':
    unittest.main()
