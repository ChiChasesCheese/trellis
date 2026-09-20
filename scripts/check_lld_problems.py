"""Acceptance gate for the low-level design problem bank (vault/domains/low-level-design/BUILD.md).

    uv run python scripts/check_lld_problems.py problems.games.tic-tac-toe [...]
    uv run python scripts/check_lld_problems.py --all

A problem leaf is done when: its reference solution passes its own tests and the empty starter
fails them; the code is standard-library Python with Chinese docstrings and comments; the solution
article is written here in Chinese with every required section, a class diagram and the tested
code embedded verbatim; there are at least six Chinese cards with steps, a drill with staged
requirements whose grading points link real cards, and at least two source readings — commercial
prep sites linked but marked `no-archive`, mirrors of paid material refused.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from trellis.project import load_project  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lld_embed_code import render  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "vault/domains/low-level-design"
BRANCH = "problems"
MIN_ARTICLE, MIN_CARDS, MIN_TESTS, MIN_DECISIONS = 8000, 6, 10, 3
# Measured on the *code*: blank lines, comments and docstrings are excluded, because this bank
# requires Chinese docstrings and comments and must not then penalise writing them. A third to a
# half of an accepted file is prose. The generous total cap is only a bloat guard.
SOLUTION_CODE_LINES, SOLUTION_TOTAL_MAX = (120, 480), 900
SECTIONS = ["题目与澄清", "需求与分级", "核心对象与职责", "关键设计决策", "代码走读", "测试与自检",
            "扩展与追问", "常见错误", "45 分钟怎么分配", "来源与延伸"]
COMMERCIAL = ("hellointerview.com", "educative.io", "designgurus.io", "algomaster.io", "codemia.io",
              "tryexponent.com", "interviewing.io", "workat.tech", "codezym.com", "interviewready.io",
              "leetcode.com", "bytebytego.com", "refactoring.guru", "amazon.com", "oreilly.com", "udemy.com")
MIRRORS = ("tssovi/grokking-the-object-oriented-design-interview",)
CJK = re.compile(r"[一-鿿]")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def run_tests(folder: Path, impl: str) -> tuple[int, str]:
    env = {**os.environ, "IMPL": impl, "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run(["uv", "run", "--project", str(ROOT), "--with", "pytest", "python", "-m", "pytest",
                          str(folder), "-q", "-p", "no:cacheprovider", "--rootdir", str(folder)],
                         capture_output=True, text=True, env=env, cwd=folder, timeout=300)
    return out.returncode, (out.stdout + out.stderr).strip().splitlines()[-1] if (out.stdout + out.stderr).strip() else ""


def check_code(slug: str) -> list[str]:
    problems: list[str] = []
    folder = BASE / "problems" / slug
    solution, starter = folder / "solution.py", folder / "starter.py"
    tests = sorted(folder.glob("test_*.py"))
    for f in (solution, starter):
        if not f.exists():
            problems.append(f"missing {f.relative_to(ROOT)}")
    if not tests:
        problems.append(f"no test_*.py in {folder.relative_to(ROOT)}")
    if problems:
        return problems
    source = solution.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    doc_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node, clean=False) is not None:
                first = node.body[0]
                doc_lines |= set(range(first.lineno, first.end_lineno + 1))
    code = sum(1 for i, line in enumerate(lines, 1)
               if line.strip() and not line.strip().startswith("#") and i not in doc_lines)
    lo, hi = SOLUTION_CODE_LINES
    if not lo <= code <= hi:
        problems.append(f"solution.py has {code} lines of code (excluding docstrings and comments), "
                        f"want {lo}–{hi}")
    if len(lines) > SOLUTION_TOTAL_MAX:
        problems.append(f"solution.py is {len(lines)} lines in total, over the {SOLUTION_TOTAL_MAX} cap")
    for node in ast.walk(tree):
        names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                [node.module or ""] if isinstance(node, ast.ImportFrom) and node.level == 0 else []
        for name in names:
            if name.split(".")[0] not in sys.stdlib_module_names:
                problems.append(f"solution.py imports {name}: standard library only")
    doc = ast.get_docstring(tree) or ""
    if not CJK.search(doc):
        problems.append("solution.py: the module docstring must be Chinese")
    comments = [l.split("#", 1)[1] for l in source.splitlines() if "#" in l and not l.strip().startswith("#!")]
    docstrings = [ast.get_docstring(n) or "" for n in ast.walk(tree)
                  if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))]
    prose = [t for t in comments + docstrings if t.strip()]
    if prose and sum(1 for t in prose if CJK.search(t)) / len(prose) < 0.8:
        problems.append("solution.py: comments and docstrings must be Chinese (≥ 80%)")
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    if len(classes) < 3:
        problems.append(f"solution.py defines {len(classes)} top-level class(es); an object design needs ≥ 3")
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    untyped = [f.name for f in funcs if f.returns is None and f.name != "__init__"]
    if funcs and len(untyped) / len(funcs) > 0.2:
        problems.append(f"solution.py: {len(untyped)} function(s) without a return annotation, e.g. {untyped[:3]}")
    n_tests = sum(len(re.findall(r"^\s*def test_", t.read_text(encoding="utf-8"), re.M)) for t in tests)
    if n_tests < MIN_TESTS:
        problems.append(f"{n_tests} test(s), need ≥ {MIN_TESTS}")
    code, tail = run_tests(folder, "solution")
    if code != 0:
        problems.append(f"reference solution fails its tests: {tail}")
    code, tail = run_tests(folder, "starter")
    if code == 0:
        problems.append("the empty starter passes the tests — they assert nothing")
    elif "error" in tail.lower() and "failed" not in tail.lower():
        problems.append(f"starter does not even import/collect: {tail}")
    return problems


def check(project, leaf_id: str) -> list[str]:
    slug = leaf_id.rsplit(".", 1)[-1]
    problems = check_code(slug)
    card_ids = {c.id for c in project.cards}
    cards = [c for c in project.cards if c.node == leaf_id and not c.adopted]
    readings = [r for r in project.readings if leaf_id in r.nodes]
    drills = [d for d in project.drills if leaf_id in d.nodes]

    solutions = [r for r in readings if r.authored]
    if len(solutions) != 1:
        problems.append(f"expected exactly one authored solution reading, found {len(solutions)}")
    for s in solutions:
        text = s.path.read_text(encoding="utf-8")
        outside_code = re.sub(r"```.*?```", "", text, flags=re.S)
        if len(outside_code) < MIN_ARTICLE:
            problems.append(f"{s.path.name}: {len(outside_code)} chars of prose outside code, need ≥ {MIN_ARTICLE}")
        if len(CJK.findall(outside_code)) / max(1, len(outside_code)) < 0.35:
            problems.append(f"{s.path.name}: the prose is not predominantly Chinese")
        heads = re.findall(r"^## (.+)$", text, re.M)
        missing = [h for h in SECTIONS if not any(x.strip().startswith(h) for x in heads)]
        if missing:
            problems.append(f"{s.path.name}: missing sections {missing}")
        decisions = text.split("## 关键设计决策", 1)[1].split("\n## ", 1)[0] if "## 关键设计决策" in text else ""
        if len(re.findall(r"^### ", decisions, re.M)) < MIN_DECISIONS:
            problems.append(f"{s.path.name}: fewer than {MIN_DECISIONS} decisions (### under 关键设计决策)")
        if "classDiagram" not in text:
            problems.append(f"{s.path.name}: no mermaid classDiagram")
        if "%% code:begin solution.py" not in text:
            problems.append(f"{s.path.name}: no embedded code block (%% code:begin solution.py %%)")
        elif render(slug, text) != text:
            problems.append(f"{s.path.name}: embedded code is stale — run scripts/lld_embed_code.py {slug}")
        if re.search(r"```java|public class |System\.out", text):
            problems.append(f"{s.path.name}: Java in the article; this bank is Python")
        if any(m.lower() in text.lower() for m in MIRRORS):
            problems.append(f"{s.path.name}: links a mirror of paid material")
        tail = text.split("## 来源与延伸", 1)[1] if "## 来源与延伸" in text else ""
        if len(re.findall(r"https?://", tail)) < 3:
            problems.append(f"{s.path.name}: fewer than 3 source links under 来源与延伸")

    if len(cards) < MIN_CARDS:
        problems.append(f"{len(cards)} card(s), need ≥ {MIN_CARDS}")
    for c in cards:
        if not CJK.search(c.question or c.text):
            problems.append(f"card {c.id}: the question is not Chinese")
        if c.tr:
            problems.append(f"card {c.id}: carries a translation section; this domain is Chinese-native")
        if c.step is None:
            problems.append(f"card {c.id}: no step")
        if re.search(r"```java", (c.answer or "") + (c.text or "")):
            problems.append(f"card {c.id}: Java code")

    if not drills:
        problems.append("no drill attached to this leaf")
    for d in drills:
        text = d.path.read_text(encoding="utf-8")
        if len(re.findall(r"第\s*[1-4一二三四]\s*关", text)) < 3:
            problems.append(f"{d.path.name}: needs staged requirements (第 1 关 … 第 3 关 at least)")
        points = text.split("评分点", 1)[1] if "评分点" in text else ""
        real = [w.strip() for w in WIKILINK.findall(points) if w.strip() in card_ids]
        if len(real) < 4:
            problems.append(f"{d.path.name}: {len(real)} grading-point link(s) to real cards, need ≥ 4")
        if solutions and solutions[0].path.stem not in text:
            problems.append(f"{d.path.name}: does not link its solution [[{solutions[0].path.stem}]]")
        if f"problems/{slug}" not in text:
            problems.append(f"{d.path.name}: does not say where the starter and tests are (problems/{slug}/)")

    pointers = [r for r in readings if r.url]
    if len(pointers) < 2:
        problems.append(f"{len(pointers)} source reading(s) with a url, need ≥ 2")
    for r in pointers:
        if any(m.lower() in r.url.lower() for m in MIRRORS):
            problems.append(f"{r.path.name}: points at a mirror of paid material — cite the original instead")
        host = urlsplit(r.url).netloc.lower()
        if any(host == h or host.endswith("." + h) for h in COMMERCIAL) and "no-archive" not in r.tags:
            problems.append(f"{r.path.name}: {host} is a commercial site — tag it no-archive")
    return problems


def main(argv: list[str]) -> int:
    project = load_project(ROOT, "low-level-design")
    errors = project.card_errors + project.reading_errors + project.drill_errors
    leaves = [l.id for l in project.skeleton.leaves() if l.id.startswith(BRANCH + ".")]
    wanted = leaves if argv == ["--all"] else argv
    failed = 0
    for leaf_id in wanted:
        if leaf_id not in leaves:
            print(f"FAIL {leaf_id}: not a leaf under `{BRANCH}`")
            failed += 1
            continue
        slug = leaf_id.rsplit(".", 1)[-1]
        found = check(project, leaf_id) + [e for e in errors if slug in e]
        print(f"{'FAIL' if found else 'ok  '} {leaf_id}" + "".join(f"\n       - {p}" for p in found))
        failed += bool(found)
    print(f"{len(wanted) - failed}/{len(wanted)} problem(s) pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
