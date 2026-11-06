"""List Hello Interview nodes that can take merged cards: question / page nodes (parents of leaves), with titles."""
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[3]
hi = yaml.safe_load((ROOT / "skeleton/hello-interview.yaml").read_text())
def walk(ns, depth=0):
    for n in ns:
        kids = n.get("children", [])
        if kids and all(not k.get("children") for k in kids):
            print(n["id"], "|", n.get("title", ""), "|", ",".join(k["id"].rsplit(".", 1)[1] for k in kids))
        walk(kids, depth + 1)
walk(hi["nodes"])
