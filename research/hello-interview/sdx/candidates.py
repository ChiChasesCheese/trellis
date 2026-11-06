"""For every System Design card, the existing cards it might duplicate, so the merge agents judge against evidence.

    uv run --with scikit-learn python research/hello-interview/sdx/candidates.py

Writes sources/local/hello-interview/sdx/candidates.json (gitignored: it points into premium cards):
{sd_card_id: {"path", "sd_node", "home", "page_cards": [...], "hi_top": [...], "bagu_top": [...], "pay_top": [...]}}.
Similarity is TF-IDF over Chinese character bigrams and English words of question + answer (Chinese where a card has it).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

ROOT = Path(__file__).resolve().parents[3]
SD = ROOT / "vault/domains/system-design/cards"
HI = ROOT / "vault/domains/hello-interview/cards"
BAGU = ROOT / "vault/domains/bagu/cards"
PAY = ROOT / "vault/domains/payments/cards"
BODIES = [ROOT / "vault/interviews/core/design-questions", ROOT / "vault/domains/hello-interview/premium/bodies"]
OUT = ROOT / "sources/local/hello-interview/sdx/candidates.json"


def front(text: str, key: str) -> str | None:
    m = re.search(rf"^{key}: (.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else None


def sd_text(text: str) -> str:
    """The Chinese question and answer where the card has them, else the English ones."""
    parts = re.split(r"^## ", text, flags=re.M)
    sec = {p.split("\n", 1)[0].strip(): p.split("\n", 1)[1] if "\n" in p else "" for p in parts[1:]}
    return (sec.get("Q zh") or sec.get("Q", "")) + "\n" + (sec.get("A zh") or sec.get("A", ""))


def tokens(text: str) -> list[str]:
    text = re.sub(r"<svg.*?</svg>", " ", text, flags=re.S)
    out = re.findall(r"[a-zA-Z][a-zA-Z0-9_\-]{1,}", text.lower())
    for run in re.findall(r"[一-鿿]+", text):
        out += [run[i:i + 2] for i in range(len(run) - 1)]
    return out


def main() -> None:
    home = json.loads((ROOT / "research/hello-interview/sdx/map.json").read_text(encoding="utf-8"))["leaves"]
    sd = []
    for f in sorted(SD.glob("*/*.md")):
        t = f.read_text(encoding="utf-8")
        sd.append({"id": front(t, "id"), "node": front(t, "node"), "path": str(f.relative_to(ROOT)), "text": sd_text(t)})
    docs = []  # (kind, path, node, text)
    for f in sorted(HI.rglob("*.md")):
        t = f.read_text(encoding="utf-8")
        docs.append(("hi", str(f.relative_to(ROOT)), front(t, "node") or "", t))
    for folder in BODIES:
        for f in sorted(folder.glob("*.md")):
            docs.append(("hi", str(f.relative_to(ROOT)), "", f.read_text(encoding="utf-8")))
    for kind, folder in (("bagu", BAGU), ("pay", PAY)):
        for f in sorted(folder.rglob("*.md")):
            t = f.read_text(encoding="utf-8")
            docs.append((kind, str(f.relative_to(ROOT)), front(t, "node") or "", t))
    vec = TfidfVectorizer(analyzer=tokens, sublinear_tf=True, min_df=1)
    m = vec.fit_transform([d[3] for d in docs] + [s["text"] for s in sd])
    dm, sm = m[: len(docs)], m[len(docs):]
    sims = linear_kernel(sm, dm)
    out = {}
    for i, s in enumerate(sd):
        target = home[s["node"]]
        page = target[: -len(".more")] if target.endswith(".more") else None
        order = sims[i].argsort()[::-1]
        hi_top = [docs[j][1] for j in order if docs[j][0] == "hi"][:8]
        bagu_top = [docs[j][1] for j in order if docs[j][0] == "bagu"][:4]
        pay_top = [docs[j][1] for j in order if docs[j][0] == "pay"][:3]
        page_cards = sorted(d[1] for d in docs if page and d[0] == "hi" and d[2].startswith(page + "."))
        out[s["id"]] = {"path": s["path"], "sd_node": s["node"], "home": target,
                        "page_cards": page_cards, "hi_top": hi_top, "bagu_top": bagu_top, "pay_top": pay_top}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} SD cards, {len(docs)} existing cards indexed -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
