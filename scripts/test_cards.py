"""What the test decks share: 碎片速刷 (system design), 算法模式识别 (LeetCode) and 每日测验.

A test card is written from one or two source cards (the learning cards of an exam point, or a problem's card on the
algorithm tree). Its front is answered by tapping, so the grade is not self-reported; its back is, in this order: the
answer, why, an optional 延伸 line, then the source cards themselves under 原卡, so a miss is learnt on the spot and
Anki's schedule brings it back. This module holds the pieces every such deck needs:

    source_notes(idents)        the source cards as they stand in Anki (front and back HTML), by their `id::` tag
    source_block(cards)         the 原卡 block for a back (one card open, a second one folded)
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


def length_tell(options: list[tuple[list[float], int]], share: float = 0.4, ratio: float = 1.25) -> tuple[list[int], int]:
    """`options`: per single-answer question, (the length of each option, the index of the right one).
    -> (questions whose right option is more than `ratio` times the longest wrong one, how many have it strictly longest).
    A file passes when the first list is empty and the count is at most `share` of the questions."""
    far, longest = [], 0
    for i, (lens, right) in enumerate(options):
        wrong = max(n for k, n in enumerate(lens) if k != right)
        if lens[right] > ratio * wrong:
            far.append(i)
        if lens[right] > wrong:
            longest += 1
    return far, longest


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
