"""What the test decks share: 碎片速刷 (system design), 算法模式识别 (LeetCode) and 每日测验.

A test card is written from one or two source cards (the learning cards of an exam point, or a problem's card on the
algorithm tree). Its front is answered by tapping, so the grade is not self-reported; its back is, in this order: the
answer, why, an optional 延伸 line, the card's place in the knowledge graph (图谱), then the source cards under 原卡, so a miss is learnt on the spot and
Anki's schedule brings it back. This module holds the pieces every such deck needs:

    source_notes(idents)        the source cards as they stand in Anki (front and back HTML), by their `id::` tag
    source_block(cards)         the 原卡 block for a back (one card open, a second one folded)
    graph_block(rows, link)     the 图谱 block above it: what to learn first, what builds on it, where it is used
    length_tell(options)        the checks that keep "pick the longest option" from passing a file of questions
    first_answers(card ids)     each card's first real answer (the honest result of a test card)

Deck builders: scripts/quick_deck.py (push), scripts/daily_quiz.py (import, full). Writers' rules:
research/agents/recog-questions.md, research/sysdesign/QUICK_AGENT.md; the second reader: research/agents/recog-verify.md.
"""
from __future__ import annotations

import html
import json
import re
import time
import urllib.request

SOURCE_CSS = """
/* ---- test decks: the source cards under the answer (原卡) ---- */
.src { margin-top: 22px; padding-top: 14px; border-top: 1px solid var(--rule); color: var(--ink); font-size: 18px; font-weight: 400; }
.src-h { font-size: 12px; letter-spacing: 0.04em; color: var(--dim); margin-bottom: 10px; }
.src hr { border: 0; border-top: 1px solid var(--rule); margin: 14px 0; }
.srcd { margin-top: 12px; }
.srcd > summary { color: var(--accent); font-size: 0.9em; margin: 6px 0 10px; }
"""


GRAPH_CSS = """
/* ---- test decks: where the card sits in the knowledge graph (图谱) ---- */
.kg { margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--rule); color: var(--ink); font-size: 14.5px; font-weight: 400; line-height: 1.55; }
.kg-h { font-size: 12px; letter-spacing: 0.04em; color: var(--dim); margin-bottom: 6px; }
.kg-r { display: flex; gap: 10px; margin: 4px 0; }
.kg-r > b { flex: 0 0 3.2em; font-size: 12px; font-weight: 600; color: var(--accent); padding-top: 2px; }
.kg-r > div { flex: 1 1 auto; min-width: 0; }
.kg-r span { display: block; }
.kg-r em { font-style: normal; color: var(--dim); font-size: 12px; margin-left: 6px; }
.kg a { color: var(--accent); text-decoration: none; font-size: 12.5px; }
.full .kg { margin: 0 0 18px; padding: 0 0 12px; border-top: 0; border-bottom: 1px solid var(--rule); }  /* inside 原题与解法: above the card */
"""


def graph_block(rows: list[tuple[str, list[str]]], link: tuple[str, str] | None = None) -> str:
    """The 图谱 block: one row per relation (label, items already escaped), then an optional link (text, url)."""
    rows = [(label, items) for label, items in rows if items]
    if not rows and not link:
        return ""
    body = "".join(f'<div class="kg-r"><b>{label}</b><div>{"".join(f"<span>{x}</span>" for x in items)}</div></div>' for label, items in rows)
    if link:
        body += f'<div class="kg-r"><b></b><div><a href="{html.escape(link[1])}">{html.escape(link[0])}</a></div></div>'
    return f'<div class="kg"><div class="kg-h">图谱</div>{body}</div>'


def some(items: list[str], limit: int, unit: str) -> list[str]:
    """The first `limit` items, and how many more there are: a list is never cut without saying so."""
    return items[:limit] + ([f"<em>等共 {len(items)} {unit}</em>"] if len(items) > limit else [])


def anki(action: str, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", json.dumps({"action": action, "version": 6, "params": params}).encode())
    for _ in range(60):
        out = json.load(urllib.request.urlopen(req, timeout=300))
        if out["error"] and "lifecycle" in str(out["error"]):   # Anki is syncing: wait and ask again
            time.sleep(2)
            continue
        if out["error"]:
            raise RuntimeError(out["error"])
        return out["result"]
    raise RuntimeError("Anki stayed busy for two minutes")


def source_notes(idents: list[str]) -> dict[str, dict]:
    """Card id -> {front, back}: the Question and Answer fields of the note tagged `id::<card id>`."""
    out: dict[str, dict] = {}
    wanted = sorted(set(idents))
    for i in range(0, len(wanted), 40):
        part = wanted[i:i + 40]
        nids = anki("findNotes", query=" OR ".join(f'"tag:id::{x}"' for x in part))
        for n in anki("notesInfo", notes=nids) if nids else []:
            ident = next((t[4:] for t in n["tags"] if t.startswith("id::") and t[4:] in part), None)
            if ident and "Question" in n["fields"] and "Answer" in n["fields"]:
                back = re.sub(r'<details class="sec related-notes">.*\Z', "", n["fields"]["Answer"]["value"], flags=re.S)   # embedded neighbours: too long here
                out[ident] = {"front": n["fields"]["Question"]["value"], "back": back}
    return out


def _label(front: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r'<span class="meta">.*?</span>', "", front, flags=re.S)))
    return html.escape(re.sub(r"\s+", " ", text).strip()[:36])


def source_block(cards: list[dict]) -> str:
    """The 原卡 block: the first source card open, any further one folded under its own question."""
    if not cards:
        return ""
    body = f'{cards[0]["front"]}<hr>{cards[0]["back"]}'
    for c in cards[1:]:
        body += f'<details class="srcd"><summary>另一张原卡：{_label(c["front"])}</summary>{c["front"]}<hr>{c["back"]}</details>'
    return f'<div class="src"><div class="src-h">原卡</div>{body}</div>'


def length_tell(options: list[tuple[list[float], int]], ratio: float = 1.25) -> tuple[list[int], int, int]:
    """`options`: per single-answer question, (the length of each option, the index of the right one).
    -> (questions whose right option is more than `ratio` times the longest wrong one,
        how many have the right option strictly longest, how many have it strictly shortest).
    A file passes when the first list is empty and neither count is above 40% of the questions: evening out the
    lengths must not turn "pick the longest" into "pick the shortest"."""
    far, longest, shortest = [], 0, 0
    for i, (lens, right) in enumerate(options):
        wrong = [n for k, n in enumerate(lens) if k != right]
        if lens[right] > ratio * max(wrong):
            far.append(i)
        longest += lens[right] > max(wrong)
        shortest += lens[right] < min(wrong)
    return far, longest, shortest


def first_answers(card_ids: list[int]) -> dict[int, dict]:
    """Card id -> its first real answer {ease, seconds, at}. A manual reschedule (type 4, ease 0) is not an answer."""
    out = {}
    for i in range(0, len(card_ids), 400):
        revs = anki("getReviewsOfCards", cards=[str(c) for c in card_ids[i:i + 400]])
        for cid, log in revs.items():
            real = sorted((r for r in log if r["type"] in (0, 1, 2, 3) and r["ease"] > 0), key=lambda r: r["id"])
            if real:
                out[int(cid)] = {"ease": real[0]["ease"], "seconds": real[0]["time"] / 1000, "at": real[0]["id"]}
    return out
