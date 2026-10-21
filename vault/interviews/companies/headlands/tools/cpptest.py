#!/usr/bin/env python3
"""C++20 题集运行器 + 验收门（jtest.py 的 C++ 对应物；说明见 CPP_CONVENTIONS.md）。

  python3 tools/cpptest.py run   <题目目录> [--impl reference|starter|work] [--tag part1] [--exclude-tag perf] [-q]
  python3 tools/cpptest.py start <题目目录>        # 把 cpp/starter.hpp 复制到 cpp/work.hpp（已存在就不动）
  python3 tools/cpptest.py verify "<glob>"         # 验收：reference 编译(-Werror)且全绿，starter 编译且至少一个测试红
  python3 tools/cpptest.py main  <题目目录> [--impl …] < input.txt   # 跑 cpp/main.cpp（stdin → stdout）

布局：<题目目录>/cpp/{reference.hpp, starter.hpp, [work.hpp], test.cpp, [main.cpp], [cases/*.in|*.out]}。
test.cpp / main.cpp 用 `#include IMPL_HEADER`，由 -DIMPL_HEADER 选择实现头文件。测试框架是 tools/cpp/minitest.hpp。

编译参数（AGENT_RULES）：clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined。另加
-fno-sanitize-recover=undefined（UBSan 默认只打印不退出，那样有符号溢出会让测试"绿着"通过）。
带 `perf` 标签的测试不在 sanitizer 二进制里跑（慢 2–5 倍，限时没意义）：另编一个 -O2 无 sanitizer 的二进制只跑它们。
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
HARNESS_DIR = KIT / "tools" / "cpp"
CXX = os.environ.get("CXX", "clang++")
BASE = ["-std=c++20", "-O2", "-Wall", "-Wextra"]
SAN = ["-fsanitize=address,undefined", "-fno-sanitize-recover=undefined", "-fno-omit-frame-pointer", "-g"]
SUMMARY = re.compile(r"SUMMARY total=(\d+) passed=(\d+) failed=(\d+) checks=(\d+)")


def resolve(arg: str) -> Path:
    p = Path(arg)
    if p.exists():
        return p.resolve()
    if (KIT / arg).exists():
        return (KIT / arg).resolve()
    sys.exit(f"{arg} 不存在")


def impl_header(problem: Path, impl: str) -> Path:
    h = problem / "cpp" / f"{impl}.hpp"
    if not h.is_file():
        sys.exit(f"{h} 不存在" + ("（先跑 `cpptest.py start`）" if impl == "work" else ""))
    return h


def compile_cpp(src: Path, header: Path, out: Path, *, sanitize: bool, werror: bool) -> subprocess.CompletedProcess:
    cmd = [CXX, *BASE, *(SAN if sanitize else []), *(["-Werror"] if werror else []),
           f'-DIMPL_HEADER="{header}"', "-I", str(HARNESS_DIR), "-I", str(src.parent), str(src), "-o", str(out)]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_env() -> dict:
    env = dict(os.environ)
    env.setdefault("UBSAN_OPTIONS", "halt_on_error=1:print_stacktrace=1")
    env.setdefault("ASAN_OPTIONS", "abort_on_error=0")
    return env


def run_bin(binary: Path, args: list[str], *, capture: bool) -> subprocess.CompletedProcess:
    return subprocess.run([str(binary), *args], capture_output=capture, text=True, env=run_env())


def filter_args(tags, excludes, quiet) -> list[str]:
    a: list[str] = []
    for t in tags or []:
        a += ["--tag", t]
    for t in excludes or []:
        a += ["--exclude-tag", t]
    return a + (["-q"] if quiet else [])


class Built:
    """Two binaries for test.cpp: sanitized (everything but perf) and fast (perf only), compiled in parallel."""

    def __init__(self, problem: Path, impl: str, tmp: Path, *, werror: bool, want_fast: bool):
        header = impl_header(problem, impl)
        test = problem / "cpp" / "test.cpp"
        if not test.is_file():
            sys.exit(f"{test} 不存在")
        self.san_bin, self.fast_bin = tmp / "test_san", tmp / "test_fast"
        with ThreadPoolExecutor(max_workers=2) as pool:
            f_san = pool.submit(compile_cpp, test, header, self.san_bin, sanitize=True, werror=werror)
            f_fast = pool.submit(compile_cpp, test, header, self.fast_bin, sanitize=False, werror=werror) if want_fast else None
            self.san = f_san.result()
            self.fast = f_fast.result() if f_fast else None

    def errors(self) -> str:
        return "".join((c.stdout + c.stderr) for c in (self.san, self.fast) if c is not None and c.returncode != 0)

    def ok(self) -> bool:
        return self.san.returncode == 0 and (self.fast is None or self.fast.returncode == 0)

    def warnings(self) -> str:
        return self.san.stderr if self.san.returncode == 0 else ""


def execute(built: Built, tags, excludes, quiet, *, capture=False) -> tuple[int, str]:
    """Run the sanitized binary (perf excluded) and, if wanted, the fast binary (perf only). Returns (exit code, output)."""
    out = ""
    rc = 0
    perf_excluded = "perf" in (excludes or [])
    only_perf = "perf" in (tags or [])
    if not only_perf:
        r = run_bin(built.san_bin, filter_args(tags, (excludes or []) + ["perf"], quiet), capture=capture)
        out += (r.stdout or "") + (r.stderr or "")
        rc = r.returncode
    if built.fast is not None and not perf_excluded:
        args = filter_args(tags, excludes, quiet) + ["--require-tag", "perf", "--allow-empty"]
        if not quiet and not capture:
            print("  -- perf tests, -O2 without sanitizers --", flush=True)
        r = run_bin(built.fast_bin, args, capture=capture)
        out += (r.stdout or "") + (r.stderr or "")
        if r.returncode not in (0, 2) and rc in (0, 2):
            rc = r.returncode
        elif rc == 2 and r.returncode == 0:
            rc = 0  # nothing matched in the sanitized binary, perf tests did
    return rc, out


def cmd_run(a) -> int:
    problem = resolve(a.dir)
    with tempfile.TemporaryDirectory() as t:
        wants_fast = "perf" not in (a.exclude_tag or [])
        built = Built(problem, a.impl, Path(t), werror=(a.impl == "reference"), want_fast=wants_fast)
        if not built.ok():
            print(built.errors(), file=sys.stderr)
            return 2
        if built.warnings() and a.impl == "work":
            print(built.warnings(), file=sys.stderr)
        rc, _ = execute(built, a.tag, a.exclude_tag, a.q)
        return rc


def cmd_start(a) -> int:
    p = resolve(a.dir) / "cpp"
    work = p / "work.hpp"
    if work.exists():
        print(f"{work} 已存在，不覆盖")
        return 0
    shutil.copyfile(p / "starter.hpp", work)
    print(f"已复制 starter.hpp → work.hpp；写完跑：python3 tools/cpptest.py run {a.dir} --impl work")
    return 0


def cmd_main(a) -> int:
    problem = resolve(a.dir)
    src = problem / "cpp" / "main.cpp"
    if not src.is_file():
        sys.exit(f"{src} 不存在（这题没有 stdin→stdout 形态）")
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "main"
        c = compile_cpp(src, impl_header(problem, a.impl), out, sanitize=True, werror=(a.impl == "reference"))
        if c.returncode != 0:
            print(c.stdout + c.stderr, file=sys.stderr)
            return 2
        return subprocess.run([str(out)], env=run_env()).returncode


def parse_summary(text: str) -> tuple[int, int, int] | None:
    m = SUMMARY.findall(text)
    if not m:
        return None
    total = sum(int(x[0]) for x in m)
    passed = sum(int(x[1]) for x in m)
    return total, passed, total - passed


def verify_one(problem: Path) -> tuple[bool, str]:
    notes: list[str] = []
    ok = True
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        ref_dir, st_dir = tmp / "ref", tmp / "st"
        ref_dir.mkdir(), st_dir.mkdir()
        # --- reference: compiles with -Werror, everything green
        ref = Built(problem, "reference", ref_dir, werror=True, want_fast=True)
        if not ref.ok():
            return False, "reference 编译失败:\n" + ref.errors()
        rc, out = execute(ref, None, None, True, capture=True)
        s = parse_summary(out)
        if rc != 0 or s is None:
            ok = False
            notes.append(f"reference=RED(exit {rc})\n{out}")
        else:
            notes.append(f"reference=green ({s[0]} tests)")
        # --- starter: compiles, and at least one test is red (exit code exactly 1 = test failures, not a crash)
        st = Built(problem, "starter", st_dir, werror=False, want_fast=False)
        if not st.ok():
            ok = False
            notes.append("starter=不能编译\n" + st.errors())
        else:
            rc, out = execute(st, None, None, True, capture=True)
            s = parse_summary(out)
            if rc == 1 and s and s[2] >= 1:
                notes.append(f"starter=red ({s[2]}/{s[0]} failing)")
            else:
                ok = False
                notes.append(f"starter={'green（测试太弱）' if rc == 0 else f'异常退出 {rc}'}")
        # --- stdin→stdout form: main.cpp builds for both impls; reference reproduces cases/*.out and exits zero
        main_src = problem / "cpp" / "main.cpp"
        if main_src.is_file():
            for impl in ("reference", "starter"):
                c = compile_cpp(main_src, impl_header(problem, impl), tmp / f"main_{impl}", sanitize=True, werror=(impl == "reference"))
                if c.returncode != 0:
                    ok = False
                    notes.append(f"main.cpp({impl})=不能编译\n{c.stdout}{c.stderr}")
            cases = sorted((problem / "cpp" / "cases").glob("*.in"))
            bad = 0
            if (tmp / "main_reference").exists():
                for case in cases:
                    expected = case.with_suffix(".out")
                    r = subprocess.run([str(tmp / "main_reference")], stdin=case.open("rb"), capture_output=True, env=run_env())
                    if r.returncode != 0 or (expected.exists() and r.stdout != expected.read_bytes()):
                        bad += 1
                        notes.append(f"case {case.name}: exit {r.returncode}\n{r.stdout.decode(errors='replace')}{r.stderr.decode(errors='replace')}")
            ok = ok and bad == 0
            notes.append(f"main={'ok' if bad == 0 else 'FAIL'} ({len(cases)} cases)")
    return ok, "  ".join(n for n in notes if "\n" not in n) + "".join("\n" + n for n in notes if "\n" in n)


def cmd_verify(a) -> int:
    pattern = a.glob if Path(a.glob).is_absolute() or glob.glob(a.glob) else str(KIT / a.glob)
    dirs = sorted(Path(d) for d in glob.glob(pattern) if (Path(d) / "cpp" / "test.cpp").is_file())
    if not dirs:
        sys.exit(f"没有匹配 {a.glob!r} 且带 cpp/test.cpp 的目录")
    bad = 0
    for d in dirs:
        ok, msg = verify_one(d.resolve())
        bad += not ok
        try:
            shown = d.resolve().relative_to(Path.cwd())
        except ValueError:
            shown = d
        print(f"{'OK  ' if ok else 'FAIL'} {shown}  {msg}", flush=True)
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("dir")
    r.add_argument("--impl", default="work", choices=["reference", "starter", "work"])
    r.add_argument("--tag", action="append")
    r.add_argument("--exclude-tag", action="append")
    r.add_argument("-q", action="store_true")
    r.set_defaults(f=cmd_run)
    s = sub.add_parser("start")
    s.add_argument("dir")
    s.set_defaults(f=cmd_start)
    m = sub.add_parser("main")
    m.add_argument("dir")
    m.add_argument("--impl", default="work", choices=["reference", "starter", "work"])
    m.set_defaults(f=cmd_main)
    v = sub.add_parser("verify")
    v.add_argument("glob")
    v.set_defaults(f=cmd_verify)
    a = ap.parse_args()
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
