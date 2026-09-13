#!/usr/bin/env python3
"""Interview-loop mock runner (post-OA rounds). Mirrors ../drill.py's shape.

  python3 loop/mock.py list                    # list all rounds: ids + titles + minutes
  python3 loop/mock.py show <id>                # print the problem statement
  python3 loop/mock.py start <id> [-m MIN]      # reset starter / copy work dir, start timer
  python3 loop/mock.py test <id> [-k EXPR]      # run tests against YOUR starter (or work copy)
  python3 loop/mock.py ref <id> [-k EXPR]       # run tests against the reference solution
  python3 loop/mock.py time <id>                # how much of the round's minutes are left
  python3 loop/mock.py status [--all]           # progress board across every round (see tools/progress.py)
  python3 loop/mock.py serve <id> [--port N]    # start the mockserver an integration round needs
  python3 loop/mock.py bq [round] [-n N] [-m MIN] [--seed S]
                                                 # draw N random non-coding questions and time them

Rounds:
  ps  03_phone_screen    45 min   problem.md   (has starter_template.py/starter.py/solution.py)
  cd  06_coding_onsite   60 min   problem.md   (same shape as ps)
  int 05_integration     60 min   problem.md   (same shape; `serve` starts its mockserver)
  bs  04_bug_squash      60 min   README.md    (whole dir minus solution/ copied to loop/work/<id>/)
  sd  07_system_design   45 min   prompt.md    (no automated test; rubric.md printed as a hint)
  01_recruiter / 02_hm / 08_behavioral: bank.json question banks, drawn via `bq`, no ids.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools import progress  # noqa: E402  (needs ROOT on sys.path first)

LOOP = ROOT / "loop"
ROUNDS = LOOP / "rounds"
WORK = LOOP / "work"
MOCKSERVER = LOOP / "mockserver"

DEFAULT_MINUTES = {"ps": 45, "cd": 60, "int": 60, "bs": 60, "sd": 45}
SHOW_FILE = {"bs": "README.md", "sd": "prompt.md"}  # everything else: problem.md

NONCODING_ALIASES = {"recruiter": "01_recruiter", "hm": "02_hm", "behavioral": "08_behavioral"}
NONCODING_ROUNDS = list(NONCODING_ALIASES.values())


def _prefix(id_: str) -> str:
    m = re.match(r"^[A-Za-z]+", id_)
    return m.group(0) if m else id_


def _show_file(d: Path, id_: str) -> Path:
    return d / SHOW_FILE.get(_prefix(id_), "problem.md")


def _dir(id_: str) -> Path:
    matches = sorted(ROUNDS.glob(f"*/{id_}_*"))
    if not matches:
        sys.exit(f"no round item matching {id_!r}; try `python3 loop/mock.py list`")
    if len(matches) > 1:
        sys.exit(f"ambiguous {id_!r}: {[str(m.relative_to(ROUNDS)) for m in matches]}")
    return matches[0]


def _timer_file(id_: str) -> Path:
    return WORK / ".timers" / f"{id_}.json"


def _print_time_left(f: Path):
    st = json.loads(f.read_text())
    left = st["minutes"] * 60 - (time.time() - st["t0"])
    print(f"{int(left // 60):02d}:{int(left % 60):02d} left" if left > 0 else "TIME IS UP")


def _first_title_line(f: Path) -> str:
    if not f.exists():
        return f"(no {f.name})"
    for line in f.read_text().splitlines():
        if line.strip():
            return line.lstrip("# ").strip()
    return f"(empty {f.name})"


def cmd_list(_a):
    if not ROUNDS.exists():
        sys.exit(f"no such directory: {ROUNDS}")
    for round_dir in sorted(ROUNDS.iterdir()):
        if not round_dir.is_dir():
            continue
        print(f"== {round_dir.name} ==")
        bank = round_dir / "bank.json"
        if bank.exists():
            try:
                n = len(json.loads(bank.read_text()))
            except json.JSONDecodeError:
                n = "?"
            print(f"  bank.json: {n} 题")
            continue
        items = [d for d in sorted(round_dir.iterdir()) if d.is_dir()]
        if not items:
            print("  (empty)")
            continue
        for d in items:
            id_ = d.name.split("_", 1)[0]
            prefix = _prefix(id_)
            title = _first_title_line(_show_file(d, id_))
            minutes = DEFAULT_MINUTES.get(prefix, 60)
            print(f"  {id_:8s} {title:48s} {minutes}min")


def cmd_show(a):
    d = _dir(a.id)
    f = _show_file(d, a.id)
    if not f.exists():
        sys.exit(f"no {f.name} in {d}")
    print(f.read_text())


_BS_SKIP = {"solution", "REPORT.md", "__pycache__", ".pytest_cache"}


def _copy_bs(d: Path, dest: Path) -> list[str]:
    """Copy a bug-squash problem dir into a work dir, hiding the answer (solution/, REPORT.md)."""
    copied = []
    for child in sorted(d.iterdir()):
        if child.name in _BS_SKIP:
            continue
        target = dest / child.name
        if child.is_dir():
            shutil.copytree(child, target, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        else:
            shutil.copy2(child, target)
        copied.append(child.name)
    return copied


def cmd_start(a):
    d = _dir(a.id)
    prefix = _prefix(a.id)
    minutes = a.minutes if a.minutes is not None else DEFAULT_MINUTES.get(prefix, 60)
    note = ""

    if prefix in ("ps", "cd", "int"):
        tpl = d / "starter_template.py"
        if tpl.exists():
            shutil.copy(tpl, d / "starter.py")
        print((d / "problem.md").read_text())
        note = f"编辑 {d / 'starter.py'}，然后 `python3 loop/mock.py test {a.id}`"

    elif prefix == "bs":
        work = WORK / a.id
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        copied = _copy_bs(d, work)
        readme = d / "README.md"
        print(readme.read_text() if readme.exists() else f"(no README.md in {d})")
        print("\n" + "=" * 70)
        print(f"已拷贝 {copied} 到 {work}；当前失败用例：\n")
        subprocess.call(
            [sys.executable, "-m", "pytest", str(work), "-p", "no:cacheprovider", "--no-header", "-rN"],
            cwd=str(ROOT),
        )
        note = f"在 {work} 中修复；`python3 loop/mock.py test {a.id}` 会在同一目录重跑"

    elif prefix == "sd":
        prompt = d / "prompt.md"
        print(prompt.read_text() if prompt.exists() else f"(no prompt.md in {d})")
        rubric = d / "rubric.md"
        if rubric.exists():
            print("\n" + "-" * 70)
            print("评分维度提示（rubric.md）：\n")
            print(rubric.read_text())
        note = "口头/白板作答，无自动测试；`show` 复看题面，`time` 查看剩余时间"

    else:
        sys.exit(f"unknown round prefix {prefix!r} for id {a.id!r}")

    timers = WORK / ".timers"
    timers.mkdir(parents=True, exist_ok=True)
    _timer_file(a.id).write_text(json.dumps({"t0": time.time(), "minutes": minutes}))
    print("\n" + "=" * 70)
    print(f"计时开始：{minutes} 分钟。{note}")


def _pytest(d: Path, which: str, extra: list[str], record_id: str | None = None, k: str | None = None) -> int:
    env = dict(os.environ, IMPL=which)
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(d),
        "-p",
        "no:cacheprovider",
        "--no-header",
        "-rN",
    ]
    out = None
    if record_id:
        env["PYTHONPATH"] = os.pathsep.join(x for x in (str(ROOT), env.get("PYTHONPATH", "")) if x)
        out = Path(tempfile.mkdtemp(prefix="mock_progress_")) / "summary.json"
        env["DRILL_PROGRESS_OUT"] = str(out)
        cmd += ["-p", "tools.pytest_progress"]
    rc = subprocess.call([*cmd, *extra], cwd=str(ROOT), env=env)
    if record_id:
        _log(record_id, which, rc, out, k)
    return rc


def _log(id_: str, which: str, rc: int, out: Path | None, k: str | None) -> None:
    """Append one line to progress.jsonl. Never let bookkeeping break the round."""
    try:
        summary = progress.read_summary(out) if out else {}
        rec = {
            "id": id_,
            "kind": "loop",
            "impl": which,
            "rc": rc,
            "k": k,
            "parts": summary.get("parts", {}),
            "duration": summary.get("duration"),
        }
        for key in ("passed", "failed", "skipped", "error"):
            rec[key] = summary.get(key, 0)
        if not any(rec[key] for key in ("passed", "failed", "skipped", "error")) and rec["rc"] != 0:
            return  # pytest never ran (import error, missing dep) — do not pollute the log
        timer = _timer_file(id_)
        if timer.exists():
            st = json.loads(timer.read_text())
            rec["elapsed_min"] = round((time.time() - st["t0"]) / 60, 1)
            rec["budget_min"] = st["minutes"]
        progress.append(rec)
    except Exception as exc:  # noqa: BLE001 - bookkeeping must never mask a test result
        print(f"(进度未记录：{exc})", file=sys.stderr)


def cmd_test(a):
    d = _dir(a.id)
    prefix = _prefix(a.id)
    extra = ["-k", a.k] if a.k else []

    if prefix in ("ps", "cd", "int"):
        rc = _pytest(d, "starter", extra, record_id=a.id, k=a.k)
    elif prefix == "bs":
        work = WORK / a.id
        if not work.exists():
            sys.exit(f"no work dir for {a.id!r}; run `python3 loop/mock.py start {a.id}` first")
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(x for x in (str(ROOT), env.get("PYTHONPATH", "")) if x)
        out = Path(tempfile.mkdtemp(prefix="mock_progress_")) / "summary.json"
        env["DRILL_PROGRESS_OUT"] = str(out)
        rc = subprocess.call(
            [
                sys.executable,
                "-m",
                "pytest",
                str(work),
                "-p",
                "no:cacheprovider",
                "-p",
                "tools.pytest_progress",
                "--no-header",
                "-rN",
                *extra,
            ],
            cwd=str(ROOT),
            env=env,
        )
        _log(a.id, "starter", rc, out, a.k)
    else:
        print(f"{prefix} 轮次无自动测试（口头/评分表作答）")
        return

    f = _timer_file(a.id)
    if f.exists():
        _print_time_left(f)
    sys.exit(rc)


def cmd_ref(a):
    d = _dir(a.id)
    prefix = _prefix(a.id)
    extra = ["-k", a.k] if a.k else []

    if prefix in ("ps", "cd", "int"):
        sys.exit(_pytest(d, "solution", extra))

    if prefix == "bs":
        patch = d / "solution" / "FIX.patch"
        if not patch.exists():
            sys.exit(f"no solution/FIX.patch in {d}")
        with tempfile.TemporaryDirectory(prefix=f"mock_ref_{a.id}_") as tmp:
            tmp_path = Path(tmp)
            _copy_bs(d, tmp_path)
            rc_apply = subprocess.call(["git", "apply", str(patch.resolve())], cwd=str(tmp_path))
            if rc_apply != 0:
                sys.exit(f"`git apply {patch}` failed (rc={rc_apply})")
            rc = subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(tmp_path),
                    "-p",
                    "no:cacheprovider",
                    "--no-header",
                    "-rN",
                    *extra,
                ],
                cwd=str(ROOT),
            )
        sys.exit(rc)

    sys.exit(f"{prefix} 轮次无参考实现自动测试")


def cmd_time(a):
    _dir(a.id)  # validate id resolves, for a clean error message
    f = _timer_file(a.id)
    if not f.exists():
        sys.exit(f"no timer for {a.id!r}; run `python3 loop/mock.py start {a.id}` first")
    _print_time_left(f)


def cmd_serve(a):
    d = _dir(a.id)
    prefix = _prefix(a.id)
    if prefix != "int":
        sys.exit("serve 仅适用于 integration 题目（int*）")
    problem = d / "problem.md"
    if not problem.exists():
        sys.exit(f"no problem.md in {d}")
    m = re.search(r"<!--\s*mockserver:\s*(\w+)\s*-->", problem.read_text())
    if not m:
        sys.exit(f"{problem} 未找到 `<!-- mockserver: NAME -->` 元数据")
    name = m.group(1)
    if name == "none":
        print(f"{a.id} 不需要 mockserver（本地文件/子进程题），直接 `start {a.id}`")
        return
    mod_file = MOCKSERVER / f"{name}.py"
    if not mod_file.exists():
        sys.exit(f"未找到 mockserver（{mod_file} 不存在，可能尚未实现）")
    print(f"启动 mockserver: {name}（Ctrl-C 停止）")
    subprocess.call([sys.executable, "-m", f"loop.mockserver.{name}", "--port", str(a.port)], cwd=str(ROOT))


def _bq_round_dirs(round_arg: str | None) -> list[str]:
    if round_arg is None:
        return NONCODING_ROUNDS
    if round_arg in NONCODING_ALIASES:
        return [NONCODING_ALIASES[round_arg]]
    if round_arg in NONCODING_ROUNDS:
        return [round_arg]
    sys.exit(f"unknown round {round_arg!r}; choose from {sorted(NONCODING_ALIASES)} or {NONCODING_ROUNDS}")


def cmd_bq(a):
    round_dirs = _bq_round_dirs(a.round)
    items = []
    for rd in round_dirs:
        bank = ROUNDS / rd / "bank.json"
        if bank.exists():
            items.extend(json.loads(bank.read_text()))
    if not items:
        sys.exit(f"no bank.json found under {', '.join(round_dirs)}")
    rng = random.Random(a.seed)
    n = min(a.n, len(items))
    picked = rng.sample(items, n)
    for i, q in enumerate(picked, 1):
        print(f"[{i}/{n}] ({q.get('round', '?')}) {q.get('q', '')}")
        if q.get("principle"):
            print(f"    principle: {q['principle']}")
        if q.get("source"):
            print(f"    source: {q['source']}")
        print(f"    限时 {a.minutes} 分钟\n")


def cmd_status(a):
    print(progress.render(show_all=a.all, kind=None if a.all_kinds else "loop"))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list").set_defaults(fn=cmd_list)
    s = sub.add_parser("status")
    s.add_argument("--all", action="store_true", help="连没做过的题一起列出来")
    s.add_argument("--all-kinds", action="store_true", help="连 problems/ 的 OA 题一起列出来")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("show")
    s.add_argument("id")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("start")
    s.add_argument("id")
    s.add_argument("-m", "--minutes", type=int, default=None)
    s.set_defaults(fn=cmd_start)

    s = sub.add_parser("test")
    s.add_argument("id")
    s.add_argument("-k", default=None)
    s.set_defaults(fn=cmd_test)

    s = sub.add_parser("ref")
    s.add_argument("id")
    s.add_argument("-k", default=None)
    s.set_defaults(fn=cmd_ref)

    s = sub.add_parser("time")
    s.add_argument("id")
    s.set_defaults(fn=cmd_time)

    s = sub.add_parser("serve")
    s.add_argument("id")
    s.add_argument("--port", type=int, default=0)
    s.set_defaults(fn=cmd_serve)

    s = sub.add_parser("bq")
    s.add_argument("round", nargs="?", default=None)
    s.add_argument("-n", type=int, default=3)
    s.add_argument("-m", "--minutes", type=int, default=3)
    s.add_argument("--seed", type=int, default=None)
    s.set_defaults(fn=cmd_bq)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
