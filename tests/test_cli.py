"""Tests for the CLI module."""

import unittest
import sys
from io import StringIO
from unittest.mock import patch, mock_open

from tokensqueeze.cli import create_parser, main


class TestCLIParser(unittest.TestCase):
    """Test cases for CLI argument parser."""

    def test_parser_creation(self):
        """Test parser creation."""
        parser = create_parser()
        self.assertIsNotNone(parser)

    def test_default_values(self):
        """Test default argument values."""
        parser = create_parser()
        args = parser.parse_args([])
        self.assertIsNone(args.input)
        self.assertIsNone(args.output)
        self.assertEqual(args.strategy, 'auto')
        self.assertEqual(args.ratio, 0.5)
        self.assertFalse(args.no_color)
        self.assertFalse(args.quiet)

    def test_strategy_choices(self):
        """Test strategy argument choices."""
        parser = create_parser()
        for strategy in ['auto', 'code', 'json', 'log', 'markdown', 'semantic', 'smart_truncate']:
            args = parser.parse_args(['-s', strategy])
            self.assertEqual(args.strategy, strategy)


class TestCLIMain(unittest.TestCase):
    """Test cases for CLI main function."""

    @patch('tokensqueeze.cli.read_input')
    @patch('tokensqueeze.cli.write_output')
    def test_main_with_input(self, mock_write, mock_read):
        """Test main with input."""
        mock_read.return_value = "hello world test text"

        with patch.object(sys, 'argv', ['tokensqueeze', '-q']):
            result = main()

        self.assertEqual(result, 0)
        mock_write.assert_called_once()

    @patch('tokensqueeze.cli.read_input')
    def test_main_no_input(self, mock_read):
        """Test main with no input."""
        mock_read.return_value = ""

        with patch.object(sys, 'argv', ['tokensqueeze']):
            result = main()

        self.assertEqual(result, 1)

    def test_main_list_strategies(self):
        """Test listing strategies."""
        with patch.object(sys, 'argv', ['tokensqueeze', '--list-strategies']):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                result = main()
                output = fake_stdout.getvalue()

        self.assertEqual(result, 0)
        self.assertIn("code", output)
        self.assertIn("json", output)

    @patch('tokensqueeze.cli.read_input')
    @patch('tokensqueeze.cli.write_output')
    def test_main_quiet_mode(self, mock_write, mock_read):
        """Test quiet mode."""
        mock_read.return_value = "hello world"

        with patch.object(sys, 'argv', ['tokensqueeze', '-q']):
            result = main()

        self.assertEqual(result, 0)


class TestCLIIO(unittest.TestCase):
    """Test cases for CLI I/O functions."""

    def test_read_input_from_file(self):
        """Test reading from file."""
        from tokensqueeze.cli import read_input
        test_content = "test content"

        with patch('builtins.open', mock_open(read_data=test_content)):
            result = read_input("test.txt")

        self.assertEqual(result, test_content)

    def test_read_input_from_stdin(self):
        """Test reading from stdin."""
        from tokensqueeze.cli import read_input
        test_content = "stdin content"

        with patch('sys.stdin', StringIO(test_content)):
            result = read_input(None)

        self.assertEqual(result, test_content)

    def test_write_output_to_file(self):
        """Test writing to file."""
        from tokensqueeze.cli import write_output
        test_content = "output content"
        mock_file = mock_open()

        with patch('builtins.open', mock_file):
            write_output("output.txt", test_content)

        mock_file.assert_called_once_with("output.txt", 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(test_content)

    def test_write_output_to_stdout(self):
        """Test writing to stdout."""
        from tokensqueeze.cli import write_output
        test_content = "stdout content"

        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            write_output(None, test_content)
            self.assertIn(test_content, fake_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
