"""系统设计高频题: one system-design question a day, all its cards in order, plus the reviews of the questions done before.

study_plan.py calls `pick` during the daily run; the cards it returns go into the deck 5 系统设计高频题 and no other.

Order (Chi, 2026-11-12: by exam-point coverage). Every question done before counts as held. The next question is the
one whose cards, once held, add the most exam-point weight to what is held. The deck names, per question, the share of
all exam-point weight held once it is learnt and how much it adds. A question stays until every one of its cards has
been seen; then the next one is chosen. Questions in the plan config's `deep_dive.paused` are skipped for now.

The questions are the design problems (s05, without the collection of real systems) and TikTok's system-design
questions (tt.sd.*). State lives in
sources/local/plan/deepdive.json: the question in progress, the day it started, and the questions done.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "sources/local/plan/deepdive.json"
DECK = "5 系统设计高频题"
REVIEW = "9 复习"


NOT_A_QUESTION = {"q.in-the-wild"}  # 真实系统案例: a collection of real systems, not one problem to design


def is_question(top: str, topic: str) -> bool:
    return (top == "s05" or topic.startswith("tt.sd.")) and topic not in NOT_A_QUESTION


def paused() -> set[str]:
    """Questions set aside for now (plan config `deep_dive.paused`): skipped, and left if one is in progress."""
    f = ROOT / "sources/local/plan/config.json"
    cfg = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    return set(cfg.get("deep_dive", {}).get("paused", []))


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"current": None, "since": None, "done": []}


def pick(cards, model, card_mastery: dict[str, float], top, title, seen: set[str], due: set[str], day: str) -> dict | None:
    """Today's question, its cards to study (unseen, or seen and due) in teaching order, the due cards of earlier
    questions, and the coverage once it is learnt. `cards` are the plan's cards; `top(topic)` the top node of a topic."""
    state = load()
    by_q: dict[str, list] = defaultdict(list)
    for c in cards:
        if is_question(top(c.topic), c.topic) and c.id in model.cards:
            by_q[c.topic].append(c)
    if not by_q:
        return None
    for v in by_q.values():
        v.sort(key=lambda c: c.rank)
    held = dict(card_mastery)

    def hold(q: str) -> None:
        for c in by_q.get(q, []):
            held[c.id] = 1.0

    for q in state["done"]:
        hold(q)
    skip = paused()
    cur = state.get("current")
    if cur in skip:  # set aside: not done, just not now
        cur = None
    if cur and cur in by_q and all(c.id in seen for c in by_q[cur]):  # learnt: on to the next one
        state["done"].append(cur)
        hold(cur)
        cur = None
    base = model.coverage(held)
    if not cur or cur not in by_q:

        def gain(q: str) -> float:
            trial = dict(held)
            trial.update({c.id: 1.0 for c in by_q[q]})
            return model.coverage(trial) - base

        left = [q for q in by_q if q not in state["done"] and q not in skip]
        if not left:
            return None
        cur = max(left, key=gain)
        state["current"], state["since"] = cur, day
    after = dict(held)
    after.update({c.id: 1.0 for c in by_q[cur]})
    covered = model.coverage(after)
    return {"state": state, "question": cur, "title": title(cur),
            "cards": [c.id for c in by_q[cur] if c.id not in seen or c.id in due],
            "reviews": [c.id for q in state["done"] for c in by_q.get(q, []) if c.id in due],
            "coverage": covered, "gain": covered - base, "left": len([q for q in by_q if q not in state["done"] and q not in skip]) - 1}


def stage(d: dict) -> str:
    """The sub-deck of today's question: its name and the coverage once it is learnt."""
    return f"1 {d['title']} · 学完考点覆盖 {d['coverage']:.1%}（+{d['gain']:.1%}）"


def save(d: dict) -> None:
    STATE.write_text(json.dumps(d["state"], ensure_ascii=False, indent=1), encoding="utf-8")
