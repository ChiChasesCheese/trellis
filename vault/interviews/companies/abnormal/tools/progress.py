"""Cross-problem progress log shared by `drill.py` and `loop/mock.py`.

One JSON object per line in `progress.jsonl` at the repo root — one line per
`test` run, appended by the two runners.  `status` renders the whole board:
which of the ~70 problems you have attempted, which are green, how long each
took and whether your times are coming down.

Standalone use:  python3 tools/progress.py status [--all] [--kind drill|loop]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "progress.jsonl"
PROBLEMS = ROOT / "problems"
ROUNDS = ROOT / "loop" / "rounds"

_PART_RE = re.compile(r"\bpart([1-5])\b")


# ---------------------------------------------------------------- writing


def append(record: dict) -> None:
    """Append one run record; never raise into the caller's test run."""
    record.setdefault("ts", dt.datetime.now().isoformat(timespec="seconds"))
    try:
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:  # pragma: no cover - disk full / read-only checkout
        print(f"(progress log not written: {exc})", file=sys.stderr)


def read_summary(path: str | os.PathLike) -> dict:
    """Read the JSON the pytest plugin dropped; {} when the run never got that far."""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def records() -> list[dict]:
    if not LOG.exists():
        return []
    out = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


# ---------------------------------------------------------------- inventory


def _title(d: Path) -> str:
    for name in ("problem.md", "README.md", "prompt.md"):
        f = d / name
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                t = line.lstrip("# ").strip()
                return t.split("—")[0].split("·", 1)[-1].strip() if "·" in t else t
    return d.name


def _declared_parts(d: Path) -> int:
    """How many distinct partN markers the problem's test file declares."""
    found = set()
    for f in d.glob("test_*.py"):
        found |= {int(m) for m in _PART_RE.findall(f.read_text(encoding="utf-8"))}
    return len(found)


def inventory() -> list[dict]:
    """Every drillable item: problems/qNN + loop/rounds/<round>/<id>."""
    items = []
    if PROBLEMS.exists():
        for d in sorted(PROBLEMS.iterdir()):
            if d.is_dir() and (d / "problem.md").exists():
                items.append(
                    {
                        "id": d.name.split("_", 1)[0],
                        "kind": "drill",
                        "group": "algo" if d.name.startswith("qA") else "bespoke",
                        "dir": d,
                        "title": _title(d),
                        "parts": _declared_parts(d),
                    }
                )
    if ROUNDS.exists():
        for round_dir in sorted(ROUNDS.iterdir()):
            if not round_dir.is_dir():
                continue
            for d in sorted(round_dir.iterdir()):
                if not d.is_dir():
                    continue
                items.append(
                    {
                        "id": d.name.split("_", 1)[0],
                        "kind": "loop",
                        "group": round_dir.name,
                        "dir": d,
                        "title": _title(d),
                        "parts": _declared_parts(d),
                    }
                )
    return items


# ---------------------------------------------------------------- aggregate


def aggregate(recs: list[dict]) -> dict[str, dict]:
    """Per-id rollup of the candidate's own (`impl=starter`) runs."""
    agg: dict[str, dict] = {}
    for r in recs:
        if r.get("impl") != "starter":
            continue  # `ref` runs prove the reference solution, not the candidate
        a = agg.setdefault(
            r["id"],
            {"runs": 0, "green": False, "best_parts": 0, "first_green": None, "last": None, "best_min": None},
        )
        a["runs"] += 1
        a["last"] = r
        passed, failed = r.get("passed", 0), r.get("failed", 0) + r.get("error", 0)
        green_parts = sum(
            1
            for p in (r.get("parts") or {}).values()
            if p.get("passed", 0) and not (p.get("failed", 0) + p.get("error", 0))
        )
        a["best_parts"] = max(a["best_parts"], green_parts)
        if passed and not failed and not r.get("k"):
            if not a["green"]:
                a["green"] = True
                a["first_green"] = r
            mins = r.get("elapsed_min")
            if mins is not None and (a["best_min"] is None or mins < a["best_min"]):
                a["best_min"] = mins
    return agg


# ---------------------------------------------------------------- rendering


def _cell(a: dict | None, parts: int) -> tuple[str, str]:
    if not a:
        return "—", ""
    if a["green"]:
        return "✅", f"{a['runs']} 次"
    return "🟡", f"{a['runs']} 次 · part {a['best_parts']}/{parts or '?'}"


def _fmt_min(v) -> str:
    return "" if v is None else f"{v:.0f}m"


def render(show_all: bool = False, kind: str | None = None) -> str:
    items = inventory()
    if kind:
        items = [i for i in items if i["kind"] == kind]
    agg = aggregate(records())
    lines: list[str] = []
    groups: dict[str, list[dict]] = {}
    for it in items:
        groups.setdefault(it["group"], []).append(it)

    done = sum(1 for it in items if agg.get(it["id"], {}).get("green"))
    started = sum(1 for it in items if it["id"] in agg)
    lines.append(f"进度：{done}/{len(items)} 全绿 · {started} 道已开工 · {len(items) - started} 道未开始")
    lines.append("")

    for group, gitems in groups.items():
        gdone = sum(1 for it in gitems if agg.get(it["id"], {}).get("green"))
        lines.append(f"== {group}  ({gdone}/{len(gitems)}) ==")
        for it in gitems:
            a = agg.get(it["id"])
            if not show_all and not a:
                continue
            mark, note = _cell(a, it["parts"])
            when = a["last"]["ts"][:10] if a else ""
            best = _fmt_min(a["best_min"]) if a else ""
            lines.append(f"  {mark} {it['id']:6s} {it['title'][:44]:46s} {note:20s} {best:>5s} {when}")
        if not show_all and not any(it["id"] in agg for it in gitems):
            lines.append("  (未开工)")
        lines.append("")

    recent = [r for r in records() if r.get("impl") == "starter"][-10:]
    if recent:
        lines.append("== 最近 10 次 ==")
        for r in recent:
            parts = r.get("parts") or {}
            gp = sum(
                1
                for p in parts.values()
                if p.get("passed", 0) and not (p.get("failed", 0) + p.get("error", 0))
            )
            lines.append(
                f"  {r['ts'][:16]}  {r['id']:6s} "
                f"{r.get('passed', 0):3d}绿/{r.get('failed', 0) + r.get('error', 0):2d}红  "
                f"part {gp}/{len(parts) or '?'}  {_fmt_min(r.get('elapsed_min')):>5s}"
            )
        lines.append("")
        lines.append("看这一栏的用时和绿灯数是不是在往好的方向走 —— 那是手感恢复的唯一客观证据。")
    else:
        lines.append("还没有任何记录。跑一次 `drill.py test <id>` 或 `loop/mock.py test <id>` 就会开始记账。")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("status", help="print the progress board")
    s.add_argument("--all", action="store_true", help="include problems never attempted")
    s.add_argument("--kind", choices=["drill", "loop"], default=None)
    a = p.parse_args(argv)
    print(render(show_all=getattr(a, "all", False), kind=getattr(a, "kind", None)))


if __name__ == "__main__":
    main()
