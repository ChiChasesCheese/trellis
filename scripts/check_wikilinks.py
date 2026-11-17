"""Dead-link check for the Obsidian vault: [[wikilinks]] by note name and relative [text](path.md) links.

    python3 scripts/check_wikilinks.py [vault-subpath ...]     # default: the whole vault

Obsidian resolves a wikilink by note name (or a path suffix), so a moved note keeps its wikilinks working; a relative
markdown link breaks when either end moves. Code fences and inline code are ignored.

A note's frontmatter `aliases:` count as names (Obsidian resolves `[[S1]]` to the note whose aliases include S1).
Web clippings (`*/clippings/*`) are archived pages: their own links point into the original site and are not checked.
Text inside `<svg>` diagrams is drawing text, not links.

Private notes (Headlands, story bank) are gitignored, so links to them resolve on Chi's machine and nowhere else.
`--update-local-only` (run on that machine) writes the link names that resolve only through untracked files to
`scripts/wikilinks_local_only.txt`; the check accepts those names everywhere. The list holds link names that already
appear in public pages, nothing more.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

VAULT = Path(__file__).resolve().parents[1] / "vault"
WIKI = re.compile(r"(?<!!)\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
CODE = re.compile(r"```.*?```|`[^`\n]*`|<svg.*?</svg>", re.S)
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


LOCAL_ONLY = Path(__file__).with_name("wikilinks_local_only.txt")


def tracked() -> set[Path]:
    import subprocess
    out = subprocess.run(["git", "ls-files", "-z", "vault"], cwd=VAULT.parent, capture_output=True, text=True).stdout
    return {VAULT.parent / f for f in out.split("\0") if f}


def main(argv: list[str]) -> int:
    update = "--update-local-only" in argv
    argv = [a for a in argv if a != "--update-local-only"]
    if update:
        keep = tracked()
        local = run(argv, only=lambda p: p in keep, quiet=True)
        LOCAL_ONLY.write_text("".join(f"{t}\n" for t in sorted(local)), encoding="utf-8")
        print(f"{len(local)} local-only link name(s) -> {LOCAL_ONLY.name}")
        return 0
    allowed = set(LOCAL_ONLY.read_text(encoding="utf-8").split("\n")) - {""} if LOCAL_ONLY.exists() else set()
    return 1 if run(argv, allowed=allowed) else 0


def run(argv: list[str], only=lambda p: True, allowed: set[str] = frozenset(), quiet: bool = False) -> set[str]:
    """Dead wikilink targets; `only` limits which notes count as existing (tracked ones for --update-local-only)."""
    notes = [p for p in VAULT.rglob("*.md") if ".obsidian" not in p.parts and only(p)]
    names = {p.stem for p in notes} | {p.name for p in VAULT.rglob("*") if p.is_file() and only(p)}
    for p in notes:
        names |= aliases(p.read_text(encoding="utf-8"))
    rels = {str(p.relative_to(VAULT).with_suffix("")) for p in notes}
    scope = [VAULT / a for a in argv] if argv else [VAULT]
    bad, dead = 0, set()
    for base in scope:
        for p in sorted(base.rglob("*.md") if base.is_dir() else [base]):
            if ".obsidian" in p.parts or clipped(p) or not only(p):
                continue
            text = CODE.sub("", p.read_text(encoding="utf-8"))
            for target in WIKI.findall(text):
                t = target.strip().rstrip("\\")
                if t in names or t in rels or t in allowed or any(r.endswith("/" + t) for r in rels):
                    continue
                bad += 1
                dead.add(t)
                if not quiet:
                    print(f"{p.relative_to(VAULT)}: [[{t}]]")
            for target in MDLINK.findall(text):
                if target.startswith(("http://", "https://")):
                    continue
                if not (p.parent / unquote(target)).resolve().exists():
                    bad += 1
                    dead.add(f"({target})")
                    if not quiet:
                        print(f"{p.relative_to(VAULT)}: ({target})")
    if not quiet:
        print(f"{bad} dead link(s)")
    return dead


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
