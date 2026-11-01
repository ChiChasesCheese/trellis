"""Put the advanced moves (advanced.json) into skeleton/basketball.yaml as the first sub-deck; fundamentals move last.

    uv run python research/domains/basketball/gen_moves.py
"""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
TOO_BASIC = {"baseline-spin", "spin-move-finish", "teardrop-floater", "turnaround-fadeaway"}
GROUPS = [("spin", "Spin 系列"), ("stepback", "Step-back 系列"), ("combo", "Dribble combos"), ("post", "Post moves"),
          ("midrange", "Mid-range"), ("finish", "Finishes")]
moves = [m for m in json.loads((ROOT / "research/domains/basketball/advanced.json").read_text(encoding="utf-8"))["moves"]
         if m["id"] not in TOO_BASIC]
path = ROOT / "skeleton/basketball.yaml"
text = path.read_text(encoding="utf-8")
head = "".join(l for l in text.splitlines(True) if l.startswith("#"))
sk = yaml.safe_load(text)
nodes = {n["id"]: n for n in sk["nodes"]}
kids = []
for gid, gtitle in GROUPS:
    leaves = [{"id": f"moves.{gid}.{m['id']}", "title": f"{m['en']}（{re.split('（', m['zh'])[0]}）",
               "summary": " · ".join(m["players"][:3]) or m["sequence"]} for m in moves if m["group"] == gid]
    if leaves:
        kids.append({"id": f"moves.{gid}", "title": gtitle, "summary": f"{gtitle}：高阶招式和球星招牌动作。", "children": leaves})
nodes["moves"] = {"id": "moves", "order": 1, "core": True, "title": "技能包（Signature moves）",
                  "summary": "高阶连招和球星招牌动作，不是基本功。", "children": kids}
nodes["tactics"]["order"] = 2
nodes["skills"].update({"order": 3, "title": "基本功（Fundamentals）"})
nodes["skills"].pop("core", None)
sk["nodes"] = [nodes["moves"], nodes["tactics"], nodes["skills"]]
path.write_text(head + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
print(sum(len(k["children"]) for k in kids), "moves")
for i in range(3):
    ids = [f"moves.{m['group']}.{m['id']}" for m in moves][i::3]
    (ROOT / f"research/domains/basketball/moves_group_M{i+1}.txt").write_text(", ".join(ids), encoding="utf-8")
