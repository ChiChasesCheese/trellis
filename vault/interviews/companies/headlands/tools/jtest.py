#!/usr/bin/env python3
"""Java 21 题集运行器 + 验收门（替代 Python kit 的 pytest / verify_suites）。

  python3 tools/jtest.py run   <题目目录> [--impl reference|starter|work] [--tag part1] [--exclude-tag perf]
  python3 tools/jtest.py start <题目目录>        # 把 starter/ 复制到 work/（已存在就不动），之后在 work/ 里写
  python3 tools/jtest.py verify "<glob>"         # 验收：reference 全绿，starter 能编译且至少一个测试红
  python3 tools/jtest.py main  <题目目录> [--impl …] < input.txt   # 跑 Main（stdin → stdout）

题目目录布局见 CONVENTIONS.md：starter/ reference/ [work/] 放同名类，test/ 放 JUnit 5 测试，
三者都在默认包。编译一律 `--release 21 --enable-preview`，所以预览特性（StructuredTaskScope、
ScopedValue、未命名变量 `_`）可以用。
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

JUNIT_VERSION = "1.11.3"
JUNIT_JAR = Path.home() / ".cache" / "trellis-java" / f"junit-platform-console-standalone-{JUNIT_VERSION}.jar"
KIT = Path(__file__).resolve().parent.parent


def java_home() -> Path:
    for cand in (os.environ.get("JAVA_HOME"), "/opt/homebrew/opt/openjdk@21", "/usr/local/opt/openjdk@21"):
        if cand and (Path(cand) / "bin" / "javac").exists():
            return Path(cand)
    out = subprocess.run(["/usr/libexec/java_home", "-v", "21"], capture_output=True, text=True)
    if out.returncode == 0:
        return Path(out.stdout.strip())
    sys.exit("找不到 JDK 21：brew install openjdk@21，或设置 JAVA_HOME")


def junit_jar() -> Path:
    if JUNIT_JAR.exists():
        return JUNIT_JAR
    JUNIT_JAR.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["mvn", "-q", "dependency:copy",
                    f"-Dartifact=org.junit.platform:junit-platform-console-standalone:{JUNIT_VERSION}",
                    f"-DoutputDirectory={JUNIT_JAR.parent}"], check=True)
    return JUNIT_JAR


def sources(d: Path) -> list[str]:
    return sorted(str(p) for p in d.rglob("*.java"))


def compile_dir(problem: Path, impl: str, out: Path, with_tests: bool = True) -> subprocess.CompletedProcess:
    impl_dir = problem / impl
    if not impl_dir.is_dir():
        sys.exit(f"{impl_dir} 不存在（work/ 先跑 `jtest.py start`）")
    files = sources(impl_dir) + (sources(problem / "test") if with_tests else [])
    jh = java_home()
    return subprocess.run([str(jh / "bin" / "javac"), "--release", "21", "--enable-preview", "-Xlint:-preview",
                           "-encoding", "UTF-8", "-cp", str(junit_jar()), "-d", str(out), *files],
                          capture_output=True, text=True)


def run_tests(problem: Path, impl: str, tags: list[str], excludes: list[str], quiet: bool = False) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        c = compile_dir(problem, impl, Path(tmp))
        if c.returncode != 0:
            print(c.stdout + c.stderr, file=sys.stderr)
            return 2
        cmd = [str(java_home() / "bin" / "java"), "--enable-preview", "-XX:+UseZGC", "-XX:+ZGenerational",
               "-jar", str(junit_jar()), "execute", "--disable-banner", "--class-path", tmp, "--scan-class-path",
               "--details", "summary" if quiet else "tree"]
        for t in tags:
            cmd += ["--include-tag", t]
        for t in excludes:
            cmd += ["--exclude-tag", t]
        r = subprocess.run(cmd, capture_output=quiet, text=True)
        return r.returncode


def cmd_run(a) -> int:
    return run_tests(Path(a.dir), a.impl, a.tag or [], a.exclude_tag or [])


def cmd_start(a) -> int:
    p = Path(a.dir)
    if (p / "work").exists():
        print(f"{p / 'work'} 已存在，不覆盖")
        return 0
    shutil.copytree(p / "starter", p / "work")
    print(f"已复制 starter/ → work/；写完跑：python3 tools/jtest.py run {p} --impl work")
    return 0


def cmd_main(a) -> int:
    p = Path(a.dir)
    with tempfile.TemporaryDirectory() as tmp:
        c = compile_dir(p, a.impl, Path(tmp), with_tests=False)
        if c.returncode != 0:
            print(c.stdout + c.stderr, file=sys.stderr)
            return 2
        return subprocess.run([str(java_home() / "bin" / "java"), "--enable-preview", "-cp", tmp, a.cls]).returncode


def cmd_verify(a) -> int:
    dirs = sorted(Path(d) for d in glob.glob(a.glob) if (Path(d) / "test").is_dir())
    if not dirs:
        sys.exit(f"没有匹配 {a.glob!r} 且带 test/ 的目录")
    bad = 0
    for d in dirs:
        ref = run_tests(d, "reference", [], [], quiet=True)
        with tempfile.TemporaryDirectory() as tmp:
            starter_compiles = compile_dir(d, "starter", Path(tmp)).returncode == 0
        st = run_tests(d, "starter", [], [], quiet=True) if starter_compiles else 2
        ok = ref == 0 and starter_compiles and st == 1
        bad += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {d}  reference={'green' if ref == 0 else f'exit {ref}'}  "
              f"starter={'red' if st == 1 else ('不能编译' if not starter_compiles else 'green（测试太弱）')}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("dir"); r.add_argument("--impl", default="work")
    r.add_argument("--tag", action="append"); r.add_argument("--exclude-tag", action="append")
    r.set_defaults(f=cmd_run)
    s = sub.add_parser("start"); s.add_argument("dir"); s.set_defaults(f=cmd_start)
    m = sub.add_parser("main"); m.add_argument("dir"); m.add_argument("--impl", default="work")
    m.add_argument("--cls", default="Main"); m.set_defaults(f=cmd_main)
    v = sub.add_parser("verify"); v.add_argument("glob"); v.set_defaults(f=cmd_verify)
    a = ap.parse_args()
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
