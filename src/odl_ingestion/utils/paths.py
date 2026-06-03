from pathlib import Path

def get_project_root() -> Path:
    """Returns the project root directory."""
    return Path(__file__).parent.parent.parent.parent

def ensure_dir(path: Path) -> Path:
    """Ensures a directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path
