#!/usr/bin/env python3
"""LLD study plan runner. Run it from this folder with plain python3 (pytest comes through uv).

  python3 drill.py today                  # the next undone task of the plan, with what to open and run
  python3 drill.py list                   # every problem in plan order, with its state
  python3 drill.py start parking-lot      # print the staged statement, copy the starter into work/, start the timer
  python3 drill.py test parking-lot       # run the tests on YOUR work/parking-lot/starter.py (-k to narrow)
  python3 drill.py time parking-lot       # minutes left
  python3 drill.py solution parking-lot   # where the write-up is; read it only after an attempt
  python3 drill.py ref parking-lot        # sanity: the reference solution passes
  python3 drill.py done s1-read           # tick a reading or mock task
  python3 drill.py status                 # rewrite PROGRESS.md (Obsidian board) and print the summary
  python3 drill.py render                 # rewrite 00-roadmap.md from plan.json

The plan is plan.json; 00-roadmap.md explains it. A drill task ticks itself when its tests go green. work/, progress.jsonl and
PROGRESS.md are personal state and stay out of git.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BANKS = [HERE / "problems", REPO / "vault/domains/low-level-design/problems"]
DRILLS = REPO / "vault/domains/low-level-design/drills/problems"
WORK = HERE / "work"
LOG = HERE / "progress.jsonl"
PLAN = json.loads((HERE / "plan.json").read_text(encoding="utf-8"))


def source(slug: str) -> Path:
    for bank in BANKS:
        if (bank / slug / "solution.py").exists():
            return bank / slug
    sys.exit(f"no problem {slug!r}; try `python3 drill.py list`")


def statement(slug: str) -> Path:
    local = source(slug) / "problem.md"
    return local if local.exists() else DRILLS / f"design-{slug}.md"


def records() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(x) for x in LOG.read_text(encoding="utf-8").splitlines() if x.strip()]


def log(**rec) -> None:
    rec["ts"] = dt.datetime.now().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def state() -> tuple[set[str], dict[str, float]]:
    """Ticked task ids, and the best full-suite green time per drill."""
    done, best = set(), {}
    for r in records():
        if r["kind"] == "done":
            done.add(r["task"])
        elif r["kind"] == "test" and r["rc"] == 0 and not r.get("k"):
            done.add(r["slug"])
            if r.get("minutes") is not None:
                best[r["slug"]] = min(best.get(r["slug"], 1e9), r["minutes"])
    return done, best


def tasks():
    for stage in PLAN["stages"]:
        for t in stage["tasks"]:
            yield stage, t


def key(t: dict) -> str:
    return t.get("drill") or t["id"]


def cmd_today(_) -> None:
    done, _best = state()
    for stage, t in tasks():
        if key(t) in done:
            continue
        print(f"{stage['title']}\n\n下一步：{t['title']}")
        if t.get("open"):
            print("打开：" + "；".join(t["open"]))
        if t.get("anki"):
            print("Anki：" + "；".join(t["anki"]))
        if t.get("drill"):
            print(f"开始：python3 drill.py start {t['drill']} -m {t.get('minutes', 60)}")
            print(f"测试：python3 drill.py test {t['drill']}")
        else:
            print(f"完成后：python3 drill.py done {t['id']}")
        print(f"\n这一阶段的验收：{stage['exit']}")
        return
    print("计划全部完成。")


def cmd_list(_) -> None:
    done, best = state()
    for stage, t in tasks():
        if t.get("drill"):
            mark = "x" if t["drill"] in done else " "
            took = f" {best[t['drill']]:.0f} 分" if t["drill"] in best else ""
            print(f"[{mark}] {stage['id']} {t['drill']:30} {t.get('minutes', 60):3} 分  {t['title']}{took}")


def cmd_start(a) -> None:
    src, dst = source(a.slug), WORK / a.slug
    fresh = not (dst / "starter.py").exists() or a.reset
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.py"):
        if f.name == "starter.py" and not fresh:
            continue
        if f.name != "solution.py":
            shutil.copy(f, dst / f.name)
    (dst / ".timer.json").write_text(json.dumps({"t0": time.time(), "minutes": a.minutes}), encoding="utf-8")
    print(statement(a.slug).read_text(encoding="utf-8"))
    print(f"\n{'=' * 60}\n计时 {a.minutes} 分钟。写 {dst / 'starter.py'}，然后 python3 drill.py test {a.slug}")


def elapsed(slug: str) -> tuple[float, int] | None:
    f = WORK / slug / ".timer.json"
    if not f.exists():
        return None
    st = json.loads(f.read_text(encoding="utf-8"))
    return (time.time() - st["t0"]) / 60, st["minutes"]


def cmd_time(a) -> None:
    e = elapsed(a.slug)
    if e is None:
        sys.exit("还没开始：先 start")
    print(f"还剩 {e[1] - e[0]:.0f} 分钟" if e[0] < e[1] else f"超时 {e[0] - e[1]:.0f} 分钟")


def pytest(folder: Path, impl: str, k: str | None) -> int:
    cmd = ["uv", "run", "--project", str(REPO), "--with", "pytest", "python", "-m", "pytest", str(folder), "-q",
           "-p", "no:cacheprovider", "--no-header", "--rootdir", str(folder), "-c", "/dev/null"]
    return subprocess.call([*cmd, *(["-k", k] if k else [])], cwd=folder, env={**os.environ, "IMPL": impl})


def cmd_test(a) -> None:
    d = WORK / a.slug
    if not (d / "starter.py").exists():
        sys.exit("还没开始：先 start")
    rc = pytest(d, "starter", a.k)
    e = elapsed(a.slug)
    log(kind="test", slug=a.slug, rc=rc, k=a.k, minutes=round(e[0], 1) if e else None)
    if e:
        cmd_time(a)
    sys.exit(rc)


def cmd_ref(a) -> None:
    sys.exit(pytest(source(a.slug), "solution", a.k))


def cmd_solution(a) -> None:
    src = source(a.slug)
    print(src / "solution.md" if (src / "solution.md").exists() else f"[[solution-{a.slug}]]（Obsidian）")
    print(src / "solution.py")


def cmd_done(a) -> None:
    known = {key(t) for _, t in tasks()}
    if a.task not in known:
        sys.exit(f"计划里没有 {a.task!r}")
    log(kind="done", task=a.task)
    cmd_status(a)


def cmd_status(_) -> None:
    done, best = state()
    lines = ["# LLD 学习进度", "", f"更新于 {dt.date.today()}。由 `drill.py status` 生成，不要手改。", ""]
    total = hit = 0
    for stage in PLAN["stages"]:
        ids = [key(t) for t in stage["tasks"]]
        got = sum(i in done for i in ids)
        total, hit = total + len(ids), hit + got
        lines += [f"## {stage['title']}（{got}/{len(ids)}）", ""]
        for t in stage["tasks"]:
            took = f"（最快 {best[key(t)]:.0f} 分钟）" if key(t) in best else ""
            lines.append(f"- [{'x' if key(t) in done else ' '}] {t['title']}{took}")
        lines.append("")
    (HERE / "PROGRESS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"完成 {hit}/{total}。看板：{HERE / 'PROGRESS.md'}")


def cmd_render(_) -> None:
    """Write 00-roadmap.md from plan.json."""
    out = ["# LLD 学习路线", "", "每天的流程：Anki 20 分钟，一道限时题，写完复盘 10 分钟。流程细节见 [[02-how-to-practise|怎么练]]。下一步做什么，运行 `python3 drill.py today`。", "",
           "| 阶段 | 用时 | 练什么 |", "|---|---|---|"]
    out += [f"| {s['title']} | {s['days']} | {'、'.join(s['skills'])} |" for s in PLAN["stages"]]
    for s in PLAN["stages"]:
        out += ["", f"## {s['title']}（{s['days']}）", "", f"**目标。** {s['goal']}", "", f"**验收。** {s['exit']}", ""]
        for t in s["tasks"]:
            if t.get("drill"):
                out.append(f"- [ ] {t['title']}（{t.get('minutes', 60)} 分钟）：`python3 drill.py start {t['drill']} -m {t.get('minutes', 60)}`")
            else:
                out.append(f"- [ ] {t['title']}：`python3 drill.py done {t['id']}`")
                out += [f"  - 打开：{x}" for x in t.get("open", [])]
                out += [f"  - Anki：`{x}`" for x in t.get("anki", [])]
    (HERE / "00-roadmap.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("today", cmd_today), ("list", cmd_list), ("status", cmd_status), ("render", cmd_render)):
        sub.add_parser(name).set_defaults(fn=fn)
    s = sub.add_parser("start")
    s.add_argument("slug"), s.add_argument("-m", "--minutes", type=int, default=60), s.add_argument("--reset", action="store_true")
    s.set_defaults(fn=cmd_start)
    for name, fn in (("test", cmd_test), ("ref", cmd_ref)):
        s = sub.add_parser(name)
        s.add_argument("slug"), s.add_argument("-k", default=None)
        s.set_defaults(fn=fn)
    for name, fn in (("time", cmd_time), ("solution", cmd_solution)):
        s = sub.add_parser(name)
        s.add_argument("slug")
        s.set_defaults(fn=fn)
    s = sub.add_parser("done")
    s.add_argument("task")
    s.set_defaults(fn=cmd_done)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
