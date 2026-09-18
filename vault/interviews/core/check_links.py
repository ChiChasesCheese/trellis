#!/usr/bin/env python3
"""Check every [[wikilink]] under vault/interviews resolves the way Obsidian resolves it.

  python3 vault/interviews/core/check_links.py            # report, exit 1 on any broken/ambiguous link
  python3 vault/interviews/core/check_links.py --all      # also scan generated card/map trees (slow, noisy)

Resolution order (Obsidian): exact vault-relative path (with or without .md) → unique basename →
frontmatter alias → error. A `#Heading` part must match a heading in the target (case-insensitive,
markdown stripped). Embeds (![[...]]) and block refs (#^id) are checked only for the target note.
Skipped: stories/raw/ (gitignored evidence), code fences, inline code.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]  # vault/
SCOPE = VAULT / "interviews"
SKIP_DIRS = {"raw", ".obsidian", ".git", "__pycache__"}
STRAY_TOP = {"code-core"}  # a duplicate of interviews/rounds/code-core sitting at the vault root; delete it
GENERATED = {"cards", "map", "clippings"}  # trellis-generated trees under rounds/*: skip unless --all

LINK = re.compile(r"(?<!\\)\[\[([^\]\|#]*)(?:#([^\]\|]*))?(?:\|[^\]]*)?\]\]")
FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE = re.compile(r"`[^`\n]*`")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)
FM = re.compile(r"\A---\n(.*?)\n---", re.S)


def clean_heading(h: str) -> str:
    h = re.sub(r"\[\[([^\]|]*)(?:\|([^\]]*))?\]\]", lambda m: m.group(2) or m.group(1), h)
    h = re.sub(r"[*_`]", "", h)
    return h.strip().lower()


def aliases_of(text: str) -> list[str]:
    m = FM.match(text)
    if not m:
        return []
    fm = m.group(1)
    out, in_alias = [], False
    for line in fm.splitlines():
        if re.match(r"^aliases:\s*\[(.*)\]\s*$", line):
            out += [a.strip().strip("'\"") for a in re.match(r"^aliases:\s*\[(.*)\]\s*$", line).group(1).split(",") if a.strip()]
            in_alias = False
        elif line.startswith("aliases:"):
            in_alias = True
        elif in_alias and re.match(r"^\s+-\s+", line):
            out.append(re.sub(r"^\s+-\s+", "", line).strip().strip("'\""))
        elif in_alias and not line.startswith(" "):
            in_alias = False
    return out


def main() -> None:
    scan_all = "--all" in sys.argv
    notes: dict[str, Path] = {}  # vault-relative path without .md → file
    by_base: dict[str, list[str]] = defaultdict(list)
    by_alias: dict[str, list[str]] = defaultdict(list)
    headings: dict[str, set[str]] = {}
    for f in VAULT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in f.parts) or f.relative_to(VAULT).parts[0] in STRAY_TOP:
            continue
        rel = f.relative_to(VAULT).with_suffix("").as_posix()
        notes[rel] = f
        by_base[f.stem.lower()].append(rel)
    def load(rel: str) -> None:
        if rel in headings:
            return
        text = notes[rel].read_text(encoding="utf-8", errors="ignore")
        headings[rel] = {clean_heading(h) for h in HEADING.findall(text)}
        for a in aliases_of(text):
            by_alias[a.lower()].append(rel)
    for rel in list(notes):
        load(rel)

    def resolve(target: str) -> tuple[str | None, str]:
        t = target.strip().rstrip("\\")  # `[[note\|text]]` inside a markdown table
        if t.endswith(".md"):
            t = t[:-3]
        if not t:
            return None, "self"
        if t in notes:
            return t, ""
        cands = [r for r in notes if r.endswith("/" + t) or r == t]
        if len(cands) == 1:
            return cands[0], ""
        if len(cands) > 1:
            return None, f"ambiguous path: {cands}"
        b = by_base.get(t.lower(), [])
        if len(b) == 1:
            return b[0], ""
        if len(b) > 1:
            return None, f"ambiguous basename: {b}"
        a = by_alias.get(t.lower(), [])
        if len(a) == 1:
            return a[0], ""
        if len(a) > 1:
            return None, f"ambiguous alias: {a}"
        return None, "not found"

    problems, checked, files = [], 0, 0
    for rel, f in sorted(notes.items()):
        if not f.is_relative_to(SCOPE):
            continue
        if not scan_all and (any(p in GENERATED for p in f.relative_to(SCOPE).parts[:-1]) or f.name.endswith(" MOC.md") or "/deck/" in f.as_posix()):
            continue  # trellis-generated notes: link style is the generator's business
        files += 1
        text = FENCE.sub("", f.read_text(encoding="utf-8", errors="ignore"))
        text = INLINE.sub("", text)
        for m in LINK.finditer(text):
            target, head = m.group(1), m.group(2)
            checked += 1
            if target.strip() == "":
                tgt = rel  # [[#heading]] in the same note
            else:
                tgt, why = resolve(target)
                if tgt is None:
                    problems.append(f"{rel}.md: [[{target}]] — {why}")
                    continue
            if head and not head.startswith("^"):
                if clean_heading(head) not in headings.get(tgt, set()):
                    problems.append(f"{rel}.md: [[{target}#{head}]] — heading not in {tgt}")
    print(f"scanned {files} notes · {checked} wikilinks · {len(problems)} problems")
    for p in problems:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
