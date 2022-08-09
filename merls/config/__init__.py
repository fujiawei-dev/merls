"""Config package for merls."""

from pathlib import Path

DEFAULT_CONFIG_FILE = Path.home() / ".config" / "merls" / "config.yaml"

DEFAULT_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_ROLLBACK_DIR = Path.home() / ".config" / "merls" / "rollback"

DEFAULT_ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
