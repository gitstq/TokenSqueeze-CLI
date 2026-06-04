#!/usr/bin/env python3
"""
TokenSqueeze CLI - Main command-line interface
"""

import sys
import argparse
import os
from typing import Optional

from .tokenizer import TokenCounter
from .compressors import CompressorRegistry, CompressionResult


class Colors:
    """Terminal colors."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_stats(result: CompressionResult, use_color: bool = True):
    """Print compression statistics."""
    c = Colors if use_color else type('obj', (object,), {
        'GREEN': '', 'YELLOW': '', 'RED': '', 'BLUE': '',
        'CYAN': '', 'BOLD': '', 'END': ''
    })()

    print(f"\n{c.BOLD}{'='*60}{c.END}")
    print(f"{c.CYAN}📊 Compression Results{c.END}")
    print(f"{c.BOLD}{'='*60}{c.END}")
    print(f"  Strategy:        {c.YELLOW}{result.strategy}{c.END}")
    print(f"  Original tokens: {c.RED}{result.original_tokens:,}{c.END}")
    print(f"  Compressed:      {c.GREEN}{result.compressed_tokens:,}{c.END}")
    print(f"  Reduction:       {c.GREEN}{result.reduction_percent:.1f}%{c.END}")
    print(f"  Tokens saved:    {c.GREEN}{result.original_tokens - result.compressed_tokens:,}{c.END}")
    print(f"{c.BOLD}{'='*60}{c.END}\n")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog='tokensqueeze',
        description='TokenSqueeze - Lightweight LLM Input Intelligent Compression Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tokensqueeze input.txt                    # Auto-detect and compress
  tokensqueeze input.txt -s code            # Use code compression
  tokensqueeze input.txt -r 0.5             # Keep 50% of tokens
  echo "text" | tokensqueeze                # Pipe input
  tokensqueeze input.txt -o output.txt      # Save to file

Strategies:
  auto          Auto-detect best strategy (default)
  smart_truncate Keep beginning and end, truncate middle
  code          Remove comments and whitespace from code
  json          Minify JSON by removing whitespace
  log           Remove timestamps and deduplicate logs
  markdown      Simplify markdown formatting
  semantic      Extractive summarization of text
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Input file (default: stdin)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '-s', '--strategy',
        default='auto',
        choices=['auto', 'smart_truncate', 'code', 'json', 'log', 'markdown', 'semantic'],
        help='Compression strategy (default: auto)'
    )

    parser.add_argument(
        '-r', '--ratio',
        type=float,
        default=0.5,
        help='Target keep ratio 0.0-1.0 (default: 0.5)'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (only output compressed text)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    parser.add_argument(
        '--list-strategies',
        action='store_true',
        help='List available compression strategies'
    )

    return parser


def read_input(input_path: Optional[str]) -> str:
    """Read input from file or stdin."""
    if input_path:
        with open(input_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        if sys.stdin.isatty():
            return ""
        return sys.stdin.read()


def write_output(output_path: Optional[str], content: str):
    """Write output to file or stdout."""
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(content)


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()
    c = Colors if use_color else type('obj', (object,), {
        'GREEN': '', 'YELLOW': '', 'RED': '', 'BLUE': '',
        'CYAN': '', 'BOLD': '', 'END': ''
    })()

    # List strategies
    if args.list_strategies:
        registry = CompressorRegistry(TokenCounter())
        print(f"{c.BOLD}Available Compression Strategies:{c.END}")
        for name, desc in registry.list_compressors().items():
            print(f"  {c.CYAN}{name:15}{c.END} {desc}")
        return 0

    # Validate ratio
    if not 0.0 < args.ratio <= 1.0:
        print(f"{c.RED}Error: Ratio must be between 0.0 and 1.0{c.END}", file=sys.stderr)
        return 1

    # Read input
    text = read_input(args.input)

    if not text:
        if not args.quiet:
            print(f"{c.YELLOW}Warning: No input provided{c.END}", file=sys.stderr)
            parser.print_help()
        return 1

    # Initialize
    token_counter = TokenCounter()
    registry = CompressorRegistry(token_counter)

    # Select strategy
    if args.strategy == 'auto':
        compressor = registry.auto_detect(text)
        if not args.quiet:
            print(f"{c.BLUE}Auto-detected strategy: {compressor.name}{c.END}")
    else:
        compressor = registry.get_compressor(args.strategy)
        if not compressor:
            print(f"{c.RED}Error: Unknown strategy '{args.strategy}'{c.END}", file=sys.stderr)
            return 1

    # Compress
    result = compressor.compress(text, keep_ratio=args.ratio)

    # Output
    if not args.quiet:
        print_stats(result, use_color)

    write_output(args.output, result.compressed)

    return 0


if __name__ == '__main__':
    sys.exit(main())
