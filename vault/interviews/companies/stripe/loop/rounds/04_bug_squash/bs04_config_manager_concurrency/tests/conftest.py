"""Puts src/ on sys.path so `import confmgr` works whether this repo is run in place or copied
elsewhere wholesale (loop/mock.py copies the whole problem dir, minus solution/ and REPORT.md,
into loop/work/<id>/ and runs pytest there -- this file must keep working after that copy)."""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
