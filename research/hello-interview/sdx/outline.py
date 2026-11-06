"""Print the System Design skeleton outline and card counts per leaf (for planning the merge into Hello Interview)."""
import collections
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[3]
sd = yaml.safe_load((ROOT / "skeleton/system-design.yaml").read_text())
per = collections.Counter()
for f in (ROOT / "vault/domains/system-design/cards").glob("*/*.md"):
    for line in f.read_text().splitlines()[:6]:
        if line.startswith("node: "):
            per[line[6:].strip()] += 1
def walk(ns, depth=0):
    for n in ns:
        kids = n.get("children", [])
        if depth <= 1 or not kids:
            print("  " * depth + n["id"], "|", n.get("title", ""), f"[{per.get(n['id'], 0)}]" if not kids else "")
        walk(kids, depth + 1)
walk(sd["nodes"])
