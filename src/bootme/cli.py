"""CLI entry point for bootme."""

import sys
import subprocess
from pathlib import Path


def show_help() -> None:
    """Display help message."""
    print("""
Usage: bootme <command>

Commands:
  autohotkey    Install AutoHotkey scripts

Options:
  -h, --help    Show this help message
""")


def main() -> None:
    """Main CLI entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help'):
        show_help()
        sys.exit(0)

    subcommand = args[0]

    if subcommand == 'autohotkey':
        # Import and run the autohotkey module
        from . import autohotkey
        autohotkey.main()
    else:
        print(f"Unknown command: {subcommand}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
