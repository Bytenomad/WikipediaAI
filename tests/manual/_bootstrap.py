"""Make the repository and src-layout package importable from manual checks."""

from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
for path in (REPOSITORY_ROOT, REPOSITORY_ROOT / "src"):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)
