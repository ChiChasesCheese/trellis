"""File one finished card group: move its split cards into the drill deck and print every card file of the group.

    uv run python research/companies/tiktok/tools/file_group.py L1 > /tmp/files.txt
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "vault/interviews/core/leetcode/tiktok/cards"
DST = ROOT / "vault/interviews/core/leetcode/tiktok-drill/cards"

group = sys.argv[1]
prompt = (ROOT / f"research/companies/tiktok/agents/prompt_{group}.md").read_text(encoding="utf-8")
line = prompt.split("**You own these leaves**")[1].split("\n")[0]
for leaf in re.findall(r"`(a|b|p[1-5])\.([a-z0-9-]+)`", line):
    branch, slug = leaf
    (DST / branch).mkdir(parents=True, exist_ok=True)
    for f in (SRC / branch).glob(f"tlc-{slug}-[1-5]-*.md"):
        shutil.move(f, DST / branch / f.name)
    for f in [*(SRC / branch).glob(f"tlc-{slug}-0-whole.md"), *(DST / branch).glob(f"tlc-{slug}-[1-5]-*.md")]:
        print(f.relative_to(ROOT))
