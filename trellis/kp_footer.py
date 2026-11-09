"""The index on the back of a system-design card: what it teaches, which questions ask that, and which cards sit beside it.

Built from the exam-point annotations (scripts/plan_kp.py, sources/local/plan/kp/) every time the deck is built, so it is
never hand-written and survives regeneration. Without the annotations, or for another domain, there is no index.
"""
from __future__ import annotations

import html
import json
import re
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "sysdesign"
EVIDENCE = ROOT / "sources/local/plan/evidence/bank.json"
MAX_QUESTIONS, MAX_RELATED = 3, 3
ROLE = {"必讲": 1.0, "追问": 0.6, "加分": 0.3}
_PARENS = re.compile(r"[（(][^（）()]*[）)]")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def plain(title: str) -> str:
    return _PARENS.sub("", title).strip()


def card_title(question: str) -> str:
    m = _BOLD.search(question.split("\n", 1)[0])
    return plain(m.group(1) if m else question.split("\n", 1)[0])


def asked_in(points: list[str], needs: dict[str, list[dict]], own: dict[str, list[dict]], freq: dict[str, float],
             known: Callable[[str], bool]) -> list[tuple[str, str]]:
    """The questions using any of these points, most often asked and most central first: [(question, its best role)]."""
    want = set(points)
    best: dict[str, str] = {}
    def see(q: str, role: str) -> None:
        if known(q) and (q not in best or ROLE.get(role, 0.6) > ROLE.get(best[q], 0.6)):
            best[q] = role
    for q, ns in needs.items():
        for n in ns:
            if n["kp"] in want:
                see(q, n["role"])
    for q, os in own.items():
        for o in os:
            if o["id"] in want:
                see(q, o.get("role", "追问"))
    ranked = sorted(best.items(), key=lambda kv: (-ROLE.get(kv[1], 0.6) * freq.get(kv[0], 0.0), kv[0]))
    return ranked[:MAX_QUESTIONS]


def related(cid: str, primary: str, by_primary: dict[str, list[str]], leaf: dict[str, str]) -> list[str]:
    """Other cards on the same point, from other leaves first: the same idea met in another setting."""
    others = [c for c in by_primary.get(primary, []) if c != cid]
    return sorted(others, key=lambda c: leaf[c] == leaf[cid])[:MAX_RELATED]


def _link(text: str, base: str, target: str) -> str:
    """`text` as a link into the map site, or plain when no site is configured."""
    return f'<a href="{html.escape(base)}#{html.escape(target)}">{html.escape(text)}</a>' if base else html.escape(text)


def render(points: Iterable[tuple[str, str]], questions: list[tuple[str, str, str]], cards: Iterable[tuple[str, str]], base: str = "") -> str:
    """Each item is (text, map target); `questions` also carries the role."""
    rows = [("考点", "；".join(_link(t, base, x) for t, x in points)),
            ("常考于", "、".join(f"{_link(q, base, x)}（{html.escape(r)}）" for q, x, r in questions)),
            ("相关卡", "；".join(_link(t, base, x) for t, x in cards))]
    body = "".join(f"<p><b>{k}</b>{v}</p>" for k, v in rows if v)
    return f'<div class="kpidx">{body}</div>' if body else ""


def footers(skeleton, cards: list) -> dict[str, str]:
    """Card id -> its index, for the domain that has exam points."""
    if skeleton.domain != DOMAIN:
        return {}
    sys.path.insert(0, str(ROOT / "scripts"))
    import plan_kp
    pts = plan_kp.load()
    if not pts.ready:
        return {}
    freq = {q: v["freq"] for q, v in json.loads(EVIDENCE.read_text(encoding="utf-8")).get("questions", {}).items()} if EVIDENCE.exists() else {}
    leaf = {c.id: c.node for c in cards}
    titles = {c.id: card_title(c.render("")[0]) for c in cards}
    by_primary: dict[str, list[str]] = {}
    for cid, ks in pts.card.items():
        if ks and cid in leaf:
            by_primary.setdefault(ks[0], []).append(cid)
    known = lambda q: q in skeleton.by_id  # noqa: E731
    config = ROOT / "sources/local/plan/config.json"
    base = json.loads(config.read_text(encoding="utf-8")).get("map_url", "") if config.exists() else ""  # kept out of the repo: a private address
    out = {}
    for c in cards:
        ks = [k for k in pts.card.get(c.id, []) if k in pts.meta and k not in plan_kp.META]
        if not ks:
            continue
        qs = [(plain(skeleton.by_id[q].title), f"t/{q}", role) for q, role in asked_in(ks, pts.needs, pts.own, freq, known)]
        out[c.id] = render([(plain(pts.meta[k]["title"]), f"p/{pts.meta[k]['topic']}/{k}") for k in ks], qs,
                           [(titles[x], f"c/{x}") for x in related(c.id, ks[0], by_primary, leaf)], base)
    return out
