"""Dead-link check for the Obsidian vault: [[wikilinks]] by note name and relative [text](path.md) links.

    python3 scripts/check_wikilinks.py [vault-subpath ...]     # default: the whole vault

Obsidian resolves a wikilink by note name (or a path suffix), so a moved note keeps its wikilinks working; a relative
markdown link breaks when either end moves. Code fences and inline code are ignored.

A note's frontmatter `aliases:` count as names (Obsidian resolves `[[S1]]` to the note whose aliases include S1).
Web clippings (`*/clippings/*`) are archived pages: their own links point into the original site and are not checked.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

VAULT = Path(__file__).resolve().parents[1] / "vault"
WIKI = re.compile(r"(?<!!)\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
FRONT = re.compile(r"\A---\n(.*?)\n---", re.S)


def aliases(text: str) -> set[str]:
    """Names from a frontmatter `aliases:` field, in either list form."""
    m = FRONT.match(text)
    if not m:
        return set()
    out, block = set(), False
    for line in m.group(1).splitlines():
        if line.startswith("aliases:"):
            rest = line[len("aliases:"):].strip()
            if rest.startswith("["):
                out |= {a.strip().strip("'\"") for a in rest.strip("[]").split(",") if a.strip()}
            elif rest:
                out.add(rest.strip("'\""))
            block = not rest
        elif block and line.lstrip().startswith("- "):
            out.add(line.lstrip()[2:].strip().strip("'\""))
        elif block and line and not line.startswith(" "):
            block = False
    return out


def clipped(p: Path) -> bool:
    return "clippings" in p.parts


def main(argv: list[str]) -> int:
    notes = [p for p in VAULT.rglob("*.md") if ".obsidian" not in p.parts]
    names = {p.stem for p in notes} | {p.name for p in VAULT.rglob("*") if p.is_file()}
    for p in notes:
        names |= aliases(p.read_text(encoding="utf-8"))
    rels = {str(p.relative_to(VAULT).with_suffix("")) for p in notes}
    scope = [VAULT / a for a in argv] if argv else [VAULT]
    bad = 0
    for base in scope:
        for p in sorted(base.rglob("*.md") if base.is_dir() else [base]):
            if ".obsidian" in p.parts or clipped(p):
                continue
            text = CODE.sub("", p.read_text(encoding="utf-8"))
            for target in WIKI.findall(text):
                t = target.strip().rstrip("\\")
                if t in names or t in rels or any(r.endswith("/" + t) for r in rels):
                    continue
                bad += 1
                print(f"{p.relative_to(VAULT)}: [[{t}]]")
            for target in MDLINK.findall(text):
                if target.startswith(("http://", "https://")):
                    continue
                if not (p.parent / unquote(target)).resolve().exists():
                    bad += 1
                    print(f"{p.relative_to(VAULT)}: ({target})")
    print(f"{bad} dead link(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
