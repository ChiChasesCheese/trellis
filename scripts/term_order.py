"""Check that no card uses a technical term before the deck teaches it (Chi's self-contained rule, 2026-11-21).

    uv run python scripts/term_order.py k8s            # report problems; exit 1 if any
    uv run python scripts/term_order.py k8s --verbose  # also list every term with its teaching leaf

Inputs: skeleton/<d>.yaml (deck order: core leaves first in tree order, then the rest, as `study.order: core-first`
plays them), research/domains/<d>/terms.yaml (term -> id of the leaf that first teaches it), and the cards under
vault/domains/<d>/cards/. A card is flagged when it mentions a term whose teaching leaf comes later in deck order and
the card does not define the term itself — "defined" means the term is followed within a few characters by a
full-width parenthesis or colon (`etcd（…）`, `**etcd：**`). Terms taught by the card's own leaf are fine.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def deck_order(domain: str) -> dict[str, int]:
    sk = yaml.safe_load((ROOT / f"skeleton/{domain}.yaml").read_text(encoding="utf-8"))
    leaves: list[tuple[bool, str]] = []

    def walk(nodes):
        for n in nodes:
            kids = n.get("children") or []
            if kids:
                walk(kids)
            else:
                leaves.append((bool(n.get("core")), n["id"]))
    walk(sk["nodes"])
    core_first = (sk.get("study") or {}).get("order", "core-first") == "core-first"
    ordered = [i for c, i in leaves if c] + [i for c, i in leaves if not c] if core_first else [i for _, i in leaves]
    return {leaf: pos for pos, leaf in enumerate(ordered)}


def pattern(term: str) -> re.Pattern:
    if re.fullmatch(r"[\x00-\x7f]+", term):
        return re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(term) + r"(?![A-Za-z0-9_])")
    return re.compile(re.escape(term))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "--verbose" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    domain = args[0]
    order = deck_order(domain)
    terms_file = ROOT / f"research/domains/{domain}/terms.yaml"
    terms = yaml.safe_load(terms_file.read_text(encoding="utf-8")) or {}
    problems, unknown = [], []
    for term, leaf in terms.items():
        if leaf not in order:
            unknown.append(f"terms.yaml: {term!r} -> {leaf!r} is not a leaf of skeleton/{domain}.yaml")
    cards = sorted((ROOT / f"vault/domains/{domain}/cards").rglob("*.md"))
    for f in cards:
        text = f.read_text(encoding="utf-8")
        node = (re.search(r"^node: (\S+)", text, re.M) or [None, ""])[1]
        if node not in order:
            continue
        body = text.split("\n---\n", 1)[-1]
        for term, leaf in terms.items():
            if leaf not in order or order[leaf] <= order[node]:
                continue
            for m in pattern(str(term)).finditer(body):
                after = body[m.end():m.end() + 4]
                if re.match(r"\**\s*[（(：:]", after):
                    break  # defined in place
            else:
                if pattern(str(term)).search(body):
                    problems.append(f"{f.relative_to(ROOT)}: uses {term!r} (taught later, by {leaf})")
    for line in unknown + problems:
        print(line)
    if verbose:
        for term, leaf in sorted(terms.items(), key=lambda kv: order.get(kv[1], 10**6)):
            print(f"{order.get(leaf, '?'):>4}  {term}  <- {leaf}")
    print(f"{domain}: {len(cards)} cards, {len(terms)} terms, {len(problems)} used before taught, {len(unknown)} bad entries")
    return 1 if problems or unknown else 0


if __name__ == "__main__":
    sys.exit(main())
