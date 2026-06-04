#!/usr/bin/env python3
"""
TokenSqueeze TUI - Terminal User Interface for interactive compression.
"""

import sys
import os

from .tokenizer import TokenCounter
from .compressors import CompressorRegistry


class TUI:
    """Simple Terminal User Interface."""

    def __init__(self):
        self.token_counter = TokenCounter()
        self.registry = CompressorRegistry(self.token_counter)
        self.use_color = sys.stdout.isatty()

    def clear(self):
        """Clear the terminal."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Print the application header."""
        self.clear()
        print("=" * 70)
        print("  🗜️  TokenSqueeze - LLM Input Intelligent Compression Engine")
        print("=" * 70)
        print()

    def print_menu(self):
        """Print the main menu."""
        print("Compression Strategies:")
        print()
        strategies = self.registry.list_compressors()
        for i, (name, desc) in enumerate(strategies.items(), 1):
            print(f"  [{i}] {name:15} - {desc}")
        print()
        print("  [0] Exit")
        print()

    def get_input_text(self) -> str:
        """Get input text from user."""
        print("Enter your text (press Ctrl+D or type 'EOF' on a new line to finish):")
        print("-" * 70)

        lines = []
        try:
            while True:
                line = input()
                if line.strip() == 'EOF':
                    break
                lines.append(line)
        except EOFError:
            pass

        return '\n'.join(lines)

    def get_file_input(self) -> str:
        """Get input from file."""
        filepath = input("Enter file path: ").strip()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""

    def get_ratio(self) -> float:
        """Get compression ratio from user."""
        while True:
            try:
                ratio_input = input("Enter keep ratio (0.1-1.0, default 0.5): ").strip()
                if not ratio_input:
                    return 0.5
                ratio = float(ratio_input)
                if 0.0 < ratio <= 1.0:
                    return ratio
                print("Please enter a value between 0.1 and 1.0")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def display_results(self, result):
        """Display compression results."""
        print()
        print("=" * 70)
        print("  📊 Compression Results")
        print("=" * 70)
        print(f"  Strategy:         {result.strategy}")
        print(f"  Original tokens:  {result.original_tokens:,}")
        print(f"  Compressed:       {result.compressed_tokens:,}")
        print(f"  Reduction:        {result.reduction_percent:.1f}%")
        print(f"  Tokens saved:     {result.original_tokens - result.compressed_tokens:,}")
        print("=" * 70)
        print()

    def display_preview(self, result):
        """Display preview of compressed text."""
        print("Compressed text preview:")
        print("-" * 70)
        preview = result.compressed[:500]
        if len(result.compressed) > 500:
            preview += "\n... (truncated)"
        print(preview)
        print("-" * 70)
        print()

    def save_prompt(self, result):
        """Ask user if they want to save the result."""
        save = input("Save to file? (y/n): ").strip().lower()
        if save == 'y':
            filepath = input("Enter output file path: ").strip()
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(result.compressed)
                print(f"Saved to {filepath}")
            except Exception as e:
                print(f"Error saving file: {e}")

    def run(self):
        """Run the TUI."""
        while True:
            self.print_header()
            self.print_menu()

            choice = input("Select option: ").strip()

            if choice == '0':
                print("Goodbye! 👋")
                break

            strategies = list(self.registry.list_compressors().keys())
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(strategies):
                    print("Invalid option. Press Enter to continue...")
                    input()
                    continue
                strategy_name = strategies[idx]
            except ValueError:
                print("Invalid input. Press Enter to continue...")
                input()
                continue

            # Get input
            self.print_header()
            print("Input source:")
            print("  [1] Type/paste text")
            print("  [2] Read from file")
            print()
            source = input("Select: ").strip()

            if source == '2':
                text = self.get_file_input()
            else:
                text = self.get_input_text()

            if not text:
                print("No input provided. Press Enter to continue...")
                input()
                continue

            # Get ratio
            ratio = self.get_ratio()

            # Compress
            if strategy_name == 'auto':
                compressor = self.registry.auto_detect(text)
            else:
                compressor = self.registry.get_compressor(strategy_name)

            result = compressor.compress(text, keep_ratio=ratio)

            # Display results
            self.print_header()
            self.display_results(result)
            self.display_preview(result)
            self.save_prompt(result)

            print()
            input("Press Enter to continue...")


def main():
    """TUI entry point."""
    try:
        tui = TUI()
        tui.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 👋")
        sys.exit(0)


if __name__ == '__main__':
    main()
