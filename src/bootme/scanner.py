"""Scanner functions for discovering AHK files."""

from pathlib import Path
from typing import List

from .utils import get_autohotkeys_dir


def scan_ahk_files() -> List[str]:
    """Scan all .ahk files in the autohotkeys directory.

    Returns:
        List[str]: Array of .ahk file names
    """
    autohotkeys_dir = get_autohotkeys_dir()

    try:
        # Handle both Traversable (from files()) and Path objects
        if hasattr(autohotkeys_dir, 'iterdir'):
            files_list = list(autohotkeys_dir.iterdir())
            return [f.name for f in files_list if f.name.endswith('.ahk')]
    except (OSError, NotImplementedError):
        pass

    return []


def detect_existing_files(target_dir: str, files_to_install: List[str]) -> List[str]:
    """Detect which files already exist in the target directory.

    Args:
        target_dir: Target installation directory
        files_to_install: Array of file names to check

    Returns:
        List[str]: Array of file names that already exist
    """
    target_path = Path(target_dir)

    if not target_path.exists():
        return []

    return [f for f in files_to_install if (target_path / f).exists()]
