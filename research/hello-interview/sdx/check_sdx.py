"""Acceptance gate for one merge group: every System Design card has a verdict, and every new card has the deck's shape.

    python3 research/hello-interview/sdx/check_sdx.py G1        # one group
    python3 research/hello-interview/sdx/check_sdx.py --all     # every group that has a ledger

Inputs (gitignored, under sources/local/hello-interview/sdx/): groups/<G>.txt (SD card ids), ledger/<G>.jsonl, candidates.json.
A ledger line is {"sd": id, "verdict": "dup" | "new" | "drop", ...}:
  dup  -> "covered_by": [existing card paths that already say it, at least as well]
  new  -> "card": the new card id under cards/premium/sdx/<home>/ (several SD cards may share one), "fixed": what was wrong, if anything
  drop -> "reason": why it is not worth a card (trivia, outdated, below the bar)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / "sources/local/hello-interview/sdx"
CARDS = ROOT / "vault/domains/hello-interview/cards/premium/sdx"
MAX_DROP = 0.2
TITLE = re.compile(r"^\*\*[^*\n]{2,40}\*\*｜补充 · [^\n]+ · (必会|追问|加分)$")
NEEDED = ("**结论。**", "**要点。**", "**面试里这样说。**")
BANNED = ("原卡", "原文", "来源", "本章", "本节", "上一张", "下一张", "System Design deck", "这道题", "本题", "面经", "抓取")


def check_card(path: Path, home: str) -> list[str]:
    errs = []
    t = path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not fm:
        return [f"{path.name}: no frontmatter"]
    meta = dict(line.split(": ", 1) for line in fm.group(1).splitlines() if ": " in line)
    if meta.get("id") != path.stem:
        errs.append(f"{path.name}: id {meta.get('id')} does not match the file name")
    if meta.get("node") != home:
        errs.append(f"{path.name}: node {meta.get('node')} should be {home}")
    if meta.get("type") != "qa" or not meta.get("step", "").isdigit():
        errs.append(f"{path.name}: needs type: qa and a numeric step")
    q = re.search(r"^## Q\n(.*?)^## A\n", t, re.S | re.M)
    a = t.split("\n## A\n", 1)[1] if "\n## A\n" in t else ""
    if not q:
        return errs + [f"{path.name}: needs ## Q and ## A"]
    first = q.group(1).strip().splitlines()[0]
    if not TITLE.match(first):
        errs.append(f"{path.name}: Q first line should be **标题**｜补充 · <页面> · 必会|追问|加分, got {first[:60]!r}")
    if len(q.group(1).strip().splitlines()) < 3:
        errs.append(f"{path.name}: Q needs the question itself under the title line")
    for s in NEEDED:
        if s not in a:
            errs.append(f"{path.name}: A lacks {s}")
    m = re.search(r"\*\*要点。\*\*\n(.*?)(?=\n\*\*[^*\n]+。\*\*|\Z)", a, re.S)
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("- ") and not re.match(r"- \*\*[^*]{1,16}[：:]\*\*", line):
                errs.append(f"{path.name}: 要点 bullet without a bold phrase head: {line[:40]!r}")
    for w in BANNED:
        if w in t:
            errs.append(f"{path.name}: banned word {w!r}")
    prose = re.sub(r"```.*?```", "", a, flags=re.S)
    cjk = len(re.findall(r"[一-鿿]", prose))
    if cjk < 0.25 * len(re.sub(r"\s", "", prose)):
        errs.append(f"{path.name}: the answer is not mainly Chinese")
    return errs


def check_group(g: str) -> tuple[int, list[str]]:
    cand = json.loads((LOCAL / "candidates.json").read_text(encoding="utf-8"))
    ids = [x for x in (LOCAL / "groups" / f"{g}.txt").read_text().split() if x]
    ledger_path = LOCAL / "ledger" / f"{g}.jsonl"
    if not ledger_path.exists():
        return 0, [f"{g}: no ledger yet"]
    errs, seen, verdicts, cards = [], {}, {"dup": 0, "new": 0, "drop": 0}, {}
    for n, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            errs.append(f"ledger line {n}: not JSON")
            continue
        sd, v = row.get("sd"), row.get("verdict")
        if sd not in ids:
            errs.append(f"ledger line {n}: {sd} is not in group {g}")
            continue
        if sd in seen:
            errs.append(f"ledger: {sd} has two verdicts")
        seen[sd] = v
        if v not in verdicts:
            errs.append(f"ledger: {sd} verdict {v!r}")
            continue
        verdicts[v] += 1
        home = cand[sd]["home"]
        if v == "dup":
            cov = row.get("covered_by") or []
            if not cov:
                errs.append(f"ledger: {sd} is dup but names no covering card")
            for c in cov:
                if not (ROOT / c).exists():
                    errs.append(f"ledger: {sd} covered_by {c} does not exist")
        elif v == "drop":
            if len(row.get("reason", "")) < 6:
                errs.append(f"ledger: {sd} dropped without a reason")
        else:
            card = row.get("card", "")
            path = CARDS / home / f"{card}.md"
            if not path.exists():
                errs.append(f"ledger: {sd} -> {card} not found in {path.parent.relative_to(ROOT)}")
            else:
                cards[path] = home
    missing = [i for i in ids if i not in seen]
    if missing:
        errs.append(f"{len(missing)} SD card(s) without a verdict, e.g. {missing[:3]}")
    if verdicts["drop"] > MAX_DROP * len(ids):
        errs.append(f"{verdicts['drop']} drops of {len(ids)}: more than {MAX_DROP:.0%}")
    for path, home in cards.items():
        errs += check_card(path, home)
    figs = sum(p.read_text(encoding="utf-8").count("```svg") for p in cards)
    print(f"{g}: {len(ids)} SD cards · dup {verdicts['dup']} · new {verdicts['new']} → {len(cards)} cards · "
          f"drop {verdicts['drop']} · {figs} figures · {len(errs)} problem(s)")
    return len(errs), errs


def main() -> int:
    groups = sorted(p.stem for p in (LOCAL / "ledger").glob("*.jsonl")) if sys.argv[1:] == ["--all"] else sys.argv[1:]
    bad = 0
    for g in groups:
        n, errs = check_group(g)
        bad += n
        for e in errs[:40]:
            print("  " + e)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
