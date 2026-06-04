"""Tests for the tokenizer module."""

import unittest
from tokensqueeze.tokenizer import SimpleTokenizer, TokenCounter, count_tokens


class TestSimpleTokenizer(unittest.TestCase):
    """Test cases for SimpleTokenizer."""

    def setUp(self):
        self.tokenizer = SimpleTokenizer()

    def test_empty_string(self):
        """Test tokenizing empty string."""
        self.assertEqual(self.tokenizer.encode(""), [])
        self.assertEqual(self.tokenizer.count_tokens(""), 0)

    def test_single_word(self):
        """Test tokenizing a single word."""
        tokens = self.tokenizer.encode("hello")
        self.assertGreater(len(tokens), 0)

    def test_multiple_words(self):
        """Test tokenizing multiple words."""
        text = "hello world test"
        tokens = self.tokenizer.encode(text)
        self.assertGreater(len(tokens), 2)

    def test_with_punctuation(self):
        """Test tokenizing text with punctuation."""
        text = "Hello, world!"
        tokens = self.tokenizer.encode(text)
        self.assertGreater(len(tokens), 2)

    def test_contractions(self):
        """Test tokenizing contractions."""
        text = "don't won't can't"
        tokens = self.tokenizer.encode(text)
        self.assertGreater(len(tokens), 3)

    def test_long_word(self):
        """Test tokenizing long words."""
        text = "supercalifragilisticexpialidocious"
        tokens = self.tokenizer.encode(text)
        self.assertGreater(len(tokens), 1)


class TestTokenCounter(unittest.TestCase):
    """Test cases for TokenCounter."""

    def setUp(self):
        self.counter = TokenCounter()

    def test_count_empty(self):
        """Test counting empty string."""
        self.assertEqual(self.counter.count(""), 0)

    def test_count_text(self):
        """Test counting text tokens."""
        count = self.counter.count("hello world")
        self.assertGreater(count, 0)

    def test_count_messages(self):
        """Test counting message tokens."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        count = self.counter.count_messages(messages)
        self.assertGreater(count, 0)


class TestCountTokensFunction(unittest.TestCase):
    """Test cases for the count_tokens convenience function."""

    def test_basic(self):
        """Test basic token counting."""
        self.assertEqual(count_tokens(""), 0)
        self.assertGreater(count_tokens("hello"), 0)


if __name__ == '__main__':
    unittest.main()
