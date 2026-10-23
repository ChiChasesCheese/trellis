"""Regenerate loop/rounds/<round>/bank.json from the first table in its questions.md.

usage (inside the kit): python3 tools/make_banks.py
"""
import json, pathlib, re

KIT = pathlib.Path(__file__).resolve().parents[1]
ROUNDS = {"04_manager_deep_dive": "hm", "05_team_values": "team"}

for rd, tag in ROUNDS.items():
    md = (KIT / "loop" / "rounds" / rd / "questions.md").read_text(encoding="utf-8")
    lines = md.splitlines()
    rows = [l for l in lines if re.match(r"^\|\s*\d+\s*\|", l)]
    head = [x.strip() for x in lines[lines.index(rows[0]) - 2].strip().strip("|").split("|")]
    bank = []
    for r in rows:
        c = [x.strip().replace("\\|", "|") for x in re.split(r"(?<!\\)\|", r.strip().strip("|"))]
        item = {"round": tag, "q": c[1], "principle": c[2], "story": c[3]}
        item["source" if "来源" in head[4] else "point"] = c[4] if len(c) > 4 else ""
        bank.append(item)
    (KIT / "loop" / "rounds" / rd / "bank.json").write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(rd, len(bank))
