"""One readable page per LeetCode Project for Obsidian: uv run python scripts/lcp_pages.py

Obsidian shows Markdown only, so a project's reference solution (`solution.py`), its tests and its knowledge points
were invisible there. This writes, next to them, `vault/domains/low-level-design/problems/lcp-<slug>/<title> 题解.md`:
what the project asks (the skeleton's summary, in our words: no workspace text), the design notes (the solution's
module docstring), the knowledge points with links to their cards, the full solution, what the tests check and how to
run them. Plus one index page, `LeetCode Project 题解.md`, in the skeleton's order. Regenerate after a solution changes.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis.skeleton import load_skeleton  # noqa: E402

LLD = ROOT / "vault/domains/low-level-design"
PROBLEMS = LLD / "problems"


def page_name(title: str) -> str:
    """The Chinese part of the leaf title, safe as a file name: 「短链服务（URL Shortener）」 -> 「短链服务」."""
    name = re.sub(r"[（(].*?[)）]", "", title).strip()
    return re.sub(r'[\\/:*?"<>|#^\[\]]', " ", name).strip() + " 题解"


def tests_of(path: Path) -> list[tuple[str, str]]:
    """(test name, its first docstring line or the name in words)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            doc = (ast.get_docstring(node) or "").strip().splitlines()
            out.append((node.name, doc[0] if doc else ""))
    return sorted(out, key=lambda t: _line(path, t[0]))


def _line(path: Path, name: str) -> int:
    m = re.search(rf"^def {re.escape(name)}\b", path.read_text(encoding="utf-8"), re.M)
    return m.start() if m else 0


def page(leaf, folder: Path) -> str:
    sol = (folder / "solution.py").read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(sol)) or ""
    code = re.sub(r'\A\s*(""".*?"""|\'\'\'.*?\'\'\')\s*', "", sol, count=1, flags=re.S).strip("\n")
    points = json.loads((folder / "points.json").read_text(encoding="utf-8")) if (folder / "points.json").exists() else []
    test_file = next(iter(sorted(folder.glob("test_*.py"))), None)
    tests = tests_of(test_file) if test_file else []
    lines = ["---", "tags:", "  - lld/lcproject", "---", "", f"# {leaf.title}", "", f"**这个项目要做什么。** {leaf.summary}", ""]
    if doc:
        lines += ["## 设计要点", ""] + [ln.rstrip() for ln in doc.splitlines()] + [""]
    if points:
        lines += ["## 考点与卡片", ""]
        for p in points:
            links = "、".join(f"[[{c}]]" for c in p.get("cards", []))
            lines.append(f"- **{p['point']}**" + (f"：{links}" if links else ""))
        lines.append("")
    lines += ["## 参考解", "", "```python", code, "```", ""]
    if tests:
        lines += [f"## 测试覆盖（{len(tests)} 个）", ""] + [f"- `{name}`" + (f"：{text}" if text else "") for name, text in tests] + [""]
    rel = folder.relative_to(ROOT)
    lines += ["## 自己做一遍", "", "从 `starter.py` 开始写，写完跑测试；参考解在 `solution.py`。", "", "```bash",
              f"cd {rel}", "python3 -m pytest -q", "```", ""]
    return "\n".join(lines)


def main() -> int:
    sk = load_skeleton(ROOT / "skeleton/low-level-design.yaml")
    branch = next(n for n in sk.walk() if n.id == "lcproject")
    index = ["---", "tags:", "  - lld/lcproject", "  - moc", "---", "", "# LeetCode Project 题解", "",
             branch.summary, ""]
    written = 0
    for leaf in branch.children:
        slug = leaf.id.split(".", 1)[1]
        folder = PROBLEMS / slug
        if not (folder / "solution.py").exists():
            continue
        name = page_name(leaf.title)
        for old in folder.glob("* 题解.md"):   # a renamed leaf leaves no stale page behind
            if old.stem != name:
                old.unlink()
        (folder / f"{name}.md").write_text(page(leaf, folder), encoding="utf-8")
        index.append(f"- [[{name}]]：{leaf.summary}")
        written += 1
    (LLD / "LeetCode Project 题解.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"{written} project pages + index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
