"""Lines of a LeetCode Project leaf copied from the private workspace, signatures excepted.

    uv run python scripts/lcp_overlap.py [<slug> ...]        # every lcp leaf by default; exit 1 if any leaf is over
    uv run python scripts/lcp_overlap.py --show <slug>       # print the copied lines

The workspace (README, template, provided modules, tests, REFLECTION) is LeetCode Premium content and stays in
sources/local/; the vault is public. A leaf must keep the workspace's public API so the solution drops in unchanged, so
lines that only declare API (imports, `class`/`def` headers, decorators, dataclass fields, `...`) may match. Everything
else that matches a 12-token run of the workspace — docstrings, comments, provided helper bodies, README examples, test
data — is copied and must be rewritten in our own words and structure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LLD = ROOT / "vault/domains/low-level-design"
WS = ROOT / "sources/local/lc-project/workspaces"
N = 12
LIMIT = 5  # copied non-API lines a leaf may keep (a shared error string, a constant)
SUFFIXES = (".py", ".md", ".essay", ".js", ".ts", ".sql", ".json", ".txt")
TOKEN = re.compile(r"[A-Za-z0-9_]+")
API = re.compile(r"""^\s*(
    (from\s+\S+\s+)?import\s.* |
    @\w[\w.]*(\(.*\))? |
    (async\s+)?def\s+\w+\s*\(.* | class\s+\w+.*: |
    \w+\s*:\s*(?P<type>[\w.\[\]|, "']+?)\s*(=\s*[^=].*)?,? |
    \)\s*(->.*)?:? | \.\.\.|pass | \"\"\"|''' | self,? | raise\s+NotImplementedError(\(\))? |
    self\.(?P<attr>\w+)\s*=\s*(?P=attr) | [A-Z]\w*\s*=\s*[\w.\[\], |]+ )\s*(\#.*)?$""", re.X)


def is_api(line: str) -> bool:
    """A pure declaration: its type part, if any, never has two words in a row (prose does)."""
    m = API.match(line)
    return bool(m) and not re.search(r"\w \w", m.group("type") or "")


def leaf_files(slug: str) -> list[Path]:
    files = sorted((LLD / f"problems/lcp-{slug}").glob("*.py"))
    files += [p for p in (LLD / f"readings/problems/solution-lcp-{slug}.md", LLD / f"drills/problems/design-lcp-{slug}.md") if p.exists()]
    return files + sorted((LLD / "cards/lcproject").glob(f"lcp-{slug}-*.md"))


def grams(slug: str) -> set[tuple[str, ...]]:
    toks: list[str] = []
    for f in sorted((WS / slug / "files").rglob("*")):
        if f.is_file() and f.suffix in SUFFIXES:
            toks += TOKEN.findall(f.read_text(errors="ignore"))
    return {tuple(toks[i:i + N]) for i in range(len(toks) - N + 1)}


def copied(path: Path, g: set) -> list[tuple[int, str]]:
    lines = path.read_text().splitlines()
    toks = [(m.group(), n) for n, line in enumerate(lines) for m in TOKEN.finditer(line)]
    hit = {toks[j][1] for i in range(len(toks) - N + 1) if tuple(t for t, _ in toks[i:i + N]) in g for j in range(i, i + N)}
    return [(n + 1, lines[n]) for n in sorted(hit) if not is_api(lines[n])]


def main() -> int:
    args = sys.argv[1:]
    show = "--show" in args
    args = [a for a in args if a != "--show"]
    slugs = args or sorted(p.name[4:] for p in (LLD / "problems").glob("lcp-*") if (WS / p.name[4:]).exists())
    over = 0
    for slug in slugs:
        g = grams(slug)
        counts, distinct = [], set()
        for f in leaf_files(slug):
            c = copied(f, g)
            distinct |= {line.strip() for _, line in c}
            if c:
                counts.append(f"{f.name}:{len(c)}")
            if show:
                for n, line in c:
                    print(f"  {f.name}:{n}: {line[:110]}")
        total = len(distinct)
        bad = total > LIMIT
        over += bad
        print(f"{'OVER' if bad else 'ok  '} {slug}: {total} distinct copied line(s) {' '.join(counts)}")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())
