"""Dead-link check for the Obsidian vault: [[wikilinks]] by note name and relative [text](path.md) links.

    python3 scripts/check_wikilinks.py [vault-subpath ...]     # default: the whole vault

Obsidian resolves a wikilink by note name (or a path suffix), so a moved note keeps its wikilinks working; a relative
markdown link breaks when either end moves. Code fences and inline code are ignored.
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


def main(argv: list[str]) -> int:
    notes = [p for p in VAULT.rglob("*.md") if ".obsidian" not in p.parts]
    names = {p.stem for p in notes} | {p.name for p in VAULT.rglob("*") if p.is_file()}
    rels = {str(p.relative_to(VAULT).with_suffix("")) for p in notes}
    scope = [VAULT / a for a in argv] if argv else [VAULT]
    bad = 0
    for base in scope:
        for p in sorted(base.rglob("*.md") if base.is_dir() else [base]):
            if ".obsidian" in p.parts:
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
