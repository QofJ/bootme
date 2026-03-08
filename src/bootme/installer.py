"""Installer functions for copying AHK files."""

import shutil
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

from .utils import get_autohotkeys_dir


@dataclass
class InstallResult:
    """Result of installation operation."""
    installed: List[str]
    failed: List[str]
    skipped: List[str]


def ensure_dir(dir_path: str) -> None:
    """Ensure a directory exists, create if not.

    Args:
        dir_path: Directory path
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def install_ahk_file(file_name: str, target_dir: str) -> bool:
    """Install a single AHK file to the target directory.

    Args:
        file_name: Name of the file to install
        target_dir: Target installation directory

    Returns:
        bool: Success status
    """
    source_dir = get_autohotkeys_dir()
    source_path = source_dir.joinpath(file_name)
    target_path = Path(target_dir) / file_name

    try:
        ensure_dir(target_dir)
        # Read from package resource and write to target
        content = source_path.read_bytes()
        target_path.write_bytes(content)
        return True
    except Exception as e:
        print(f"Failed to install {file_name}: {e}")
        return False


def install_ahk_files(
    files: List[str],
    target_dir: str,
    skip_files: List[str] = None
) -> InstallResult:
    """Install multiple AHK files to the target directory.

    Args:
        files: Array of file names to install
        target_dir: Target installation directory
        skip_files: Array of file names to skip

    Returns:
        InstallResult: Object with installed, failed, and skipped lists
    """
    if skip_files is None:
        skip_files = []

    result = InstallResult(installed=[], failed=[], skipped=[])
    skip_set = set(skip_files)

    for file in files:
        if file in skip_set:
            result.skipped.append(file)
            continue

        success = install_ahk_file(file, target_dir)
        if success:
            result.installed.append(file)
        else:
            result.failed.append(file)

    return result
