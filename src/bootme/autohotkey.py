"""AutoHotkey installation command."""

import sys
import inquirer
from rich.console import Console

from .utils import get_default_install_path, get_autohotkeys_dir
from .scanner import scan_ahk_files, detect_existing_files
from .installer import install_ahk_files

console = Console()


def main() -> None:
    """Run the AutoHotkey TUI installer."""
    console.print("\n:rocket: AutoHotkey TUI Installer\n")

    # Step 1: Select installation path
    default_path = get_default_install_path()
    questions = [
        inquirer.Text(
            'install_path',
            message="Select installation path",
            default=default_path,
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        sys.exit(0)

    install_path = answers['install_path']

    # Step 2: Scan and select files to install
    available_files = scan_ahk_files()

    if not available_files:
        console.print("\n:warning: No .ahk files found in autohotkeys directory.")
        console.print(f"   Expected location: {get_autohotkeys_dir()}\n")
        sys.exit(0)

    questions = [
        inquirer.Checkbox(
            'selected_files',
            message="Select files to install",
            choices=available_files,
            default=available_files,
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        sys.exit(0)

    selected_files = answers['selected_files']

    if not selected_files:
        console.print("\n:warning: No files selected. Exiting.\n")
        sys.exit(0)

    # Step 3: Handle existing files
    existing_files = detect_existing_files(install_path, selected_files)
    skip_files = []

    if existing_files:
        console.print(f"\n:file_folder: Found {len(existing_files)} existing file(s) in target directory.\n")

        for file in existing_files:
            questions = [
                inquirer.Confirm(
                    'overwrite',
                    message=f'"{file}" already exists. Overwrite?',
                    default=False,
                ),
            ]
            answers = inquirer.prompt(questions)
            if answers is None:
                sys.exit(0)

            if not answers['overwrite']:
                skip_files.append(file)

    # Step 4: Confirm and install
    files_to_install = [f for f in selected_files if f not in skip_files]

    if not files_to_install:
        console.print("\n:warning: No files to install (all skipped). Exiting.\n")
        sys.exit(0)

    console.print("\n:package: Installation Summary:")
    console.print(f"   Target: {install_path}")
    console.print(f"   Files to install: {len(files_to_install)}")
    if skip_files:
        console.print(f"   Files to skip: {len(skip_files)}")

    questions = [
        inquirer.Confirm(
            'proceed',
            message="Proceed with installation?",
            default=True,
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        sys.exit(0)

    if not answers['proceed']:
        console.print("\n:x: Installation cancelled.\n")
        sys.exit(0)

    # Execute installation
    console.print("\n:hourglass_flowing_sand: Installing...\n")
    result = install_ahk_files(selected_files, install_path, skip_files)

    # Display results
    if result.installed:
        console.print(":white_check_mark: Successfully installed:")
        for f in result.installed:
            console.print(f"   - {f}")

    if result.skipped:
        console.print(":fast_forward: Skipped:")
        for f in result.skipped:
            console.print(f"   - {f}")

    if result.failed:
        console.print(":x: Failed:")
        for f in result.failed:
            console.print(f"   - {f}")

    console.print("\n:sparkles: Done!\n")


if __name__ == "__main__":
    main()
