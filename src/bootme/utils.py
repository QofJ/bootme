"""Utility functions for bootme."""

import os
from pathlib import Path
from importlib.resources import files


def get_default_install_path() -> str:
    """Get the default AutoHotkey installation path.

    Returns:
        str: Default path (~/Documents/AutoHotkey)
    """
    return str(Path.home() / "Documents" / "AutoHotkey")


def get_autohotkeys_dir() -> Path:
    """Get the autohotkeys source directory path.

    Returns:
        Path: Path to autohotkeys directory
    """
    # Use importlib.resources to access package data
    return files("bootme").joinpath("autohotkeys")
