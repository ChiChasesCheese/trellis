#!/usr/bin/env python3
"""Compile every ```java block of the foundation chapters with javac --release 21 --enable-preview.

A block may be: (1) a complete file (has a top-level class/record/interface/enum), (2) a list of class
members (fields/methods), or (3) a list of statements. Each block is tried in that order; it passes if any
wrapping compiles. Usage:  python3 check_snippets.py ../*.md
"""
import textwrap, re, subprocess, sys, tempfile, pathlib, concurrent.futures as cf

JAVAC = "/opt/homebrew/opt/openjdk@21/bin/javac"
IMPORTS = """import java.util.*;
import java.util.function.*;
import java.util.stream.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.concurrent.locks.*;
import java.io.*;
import java.net.*;
import java.nio.*;
import java.nio.channels.*;
import java.nio.file.*;
import java.lang.foreign.*;
import java.lang.invoke.*;
"""
TOP = re.compile(r"^(?:public\s+|final\s+|abstract\s+|sealed\s+|static\s+)*(?:class|record|interface|enum)\s", re.M)

def split_imports(code):
    imps, rest = [], []
    for line in code.splitlines():
        (imps if line.startswith("import ") else rest).append(line)
    return "\n".join(imps), "\n".join(rest)

def variants(code):
    imps, body = split_imports(code)
    body_nopub = re.sub(r"^public\s+(?=(?:final\s+|abstract\s+|sealed\s+)*(?:class|record|interface|enum)\s)", "", body, flags=re.M)
    out = []
    if TOP.search(body):
        out.append(("top", IMPORTS + imps + "\n" + body_nopub + "\n"))
    out.append(("members", IMPORTS + imps + "\nclass Snip { \n" + body + "\n}\n"))
    out.append(("stmts", IMPORTS + imps + "\nclass Snip { static void run() throws Throwable {\n" + body + "\n} }\n"))
    return out

def try_compile(args):
    idx, src, code = args
    for kind, text in variants(code):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "Snip.java"
            p.write_text(text)
            r = subprocess.run([JAVAC, "--release", "21", "--enable-preview", "-Xlint:none", "-d", d, str(p)],
                               capture_output=True, text=True)
            if r.returncode == 0:
                return idx, src, True, kind, ""
            last = r.stderr
    return idx, src, False, "", last

def main(files):
    jobs = []
    for f in files:
        txt = pathlib.Path(f).read_text()
        for i, m in enumerate(re.finditer(r"^[ \t]*```java\n(.*?)^[ \t]*```", txt, re.S | re.M)):
            line = txt[:m.start()].count("\n") + 2
            jobs.append((i, f"{f}:{line}", textwrap.dedent(m.group(1))))
    bad = 0
    with cf.ThreadPoolExecutor(8) as ex:
        for idx, src, ok, kind, err in ex.map(try_compile, jobs):
            if not ok:
                bad += 1
                print("FAIL", src); print(err[:1200])
    print(f"{len(jobs)} java blocks checked, {bad} failed")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
