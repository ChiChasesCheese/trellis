"""系统设计高频题: one system-design question a day, all its cards in order, plus the reviews of the questions done before.

study_plan.py calls `pick` during the daily run; the cards it returns go into the deck 5 系统设计高频题 and no other.

Order (Chi, 2026-11-12: by exam-point coverage). Every question done before counts as held. The next question is the
one whose cards, once held, add the most exam-point weight to what is held. The deck names, per question, the share of
all exam-point weight held once it is learnt and how much it adds. A question stays until every one of its cards has
been seen; then the next one is chosen. Questions in the plan config's `deep_dive.paused` are skipped for now.

A question brings its foundations (Chi, 2026-11-12: 「以一个题为标的，去学习这个题相关的所有卡片」): for every exam point
the question needs (plan kp questions/<q>.json), the cards that teach the point in its own topic, prerequisites first.
They are dealt before the question's own cards, one sub-deck per topic, and count towards the question's coverage.

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
MOCK_FIX = "-mockfix-"  # card ids written from a real mock of the question: dealt first, as part 0


KP = ROOT / "sources/local/plan/kp"
ROLE = {"必讲": 0, "追问": 1, "加分": 2}
NOT_A_QUESTION = {"q.in-the-wild"}  # 真实系统案例: a collection of real systems, not one problem to design


def is_question(top: str, topic: str) -> bool:
    return (top == "s05" or topic.startswith("tt.sd.")) and topic not in NOT_A_QUESTION


def paused() -> set[str]:
    """Questions set aside for now (plan config `deep_dive.paused`): skipped, and left if one is in progress."""
    f = ROOT / "sources/local/plan/config.json"
    cfg = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    return set(cfg.get("deep_dive", {}).get("paused", []))


def foundations(prereq: dict[str, list[str]]) -> dict[str, list[tuple[str, str]]]:
    """Question -> (card, topic) for the cards that teach its exam points in each point's own topic, in learning
    order: prerequisites before the points that lean on them, then 必讲 before 追问 before 加分."""
    docs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((KP / "topics").glob("*.json"))]
    home = {k["id"]: d["topic"] for d in docs for k in d["kps"]}
    teach: dict[str, list[str]] = defaultdict(list)
    for d in docs:
        for cid, ks in d.get("cards", {}).items():
            for k in ks:
                if home.get(k) == d["topic"]:
                    teach[k].append(cid)
    out = {}
    for f in sorted((KP / "questions").glob("*.json")):
        q = json.loads(f.read_text(encoding="utf-8"))
        pos = {n["kp"]: (ROLE.get(n.get("role"), 3), i) for i, n in enumerate(q.get("needs", []))}
        order: list[str] = []

        def visit(k: str, path: frozenset = frozenset()) -> None:
            if k in order or k in path:
                return
            for pre in sorted((x for x in prereq.get(k, []) if x in pos), key=pos.get):
                visit(pre, path | {k})
            order.append(k)

        for k in sorted(pos, key=pos.get):
            visit(k)
        out[q["topic"]] = [(cid, home[k]) for k in order for cid in teach.get(k, [])]
    return out


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"current": None, "since": None, "done": []}


def pick(cards, model, card_mastery: dict[str, float], top, title, seen: set[str], due: set[str], day: str,
         node: dict | None = None) -> dict | None:
    """Today's question, its cards to study (unseen, or seen and due) in teaching order, the due cards of earlier
    questions, and the coverage once it is learnt. `cards` are the plan's cards; `top(topic)` the top node of a topic;
    `node` the skeleton's nodes by id, whose order under the question is the order the cards are dealt in."""
    state = load()
    by_q: dict[str, list] = defaultdict(list)
    for c in cards:
        if is_question(top(c.topic), c.topic) and c.id in model.cards:
            by_q[c.topic].append(c)
    if not by_q:
        return None
    for v in by_q.values():
        v.sort(key=lambda c: c.rank)
    by_id = {c.id: c for c in cards}
    base_of: dict[str, dict[str, str]] = {}  # question -> its foundation cards, in learning order, with their topic
    for q, found in foundations(model.prereq).items():
        if q in by_q:
            own = {c.id for c in by_q[q]}
            base_of[q] = {}
            for cid, t in found:
                if cid in by_id and cid not in own and cid not in base_of[q] and not is_question(top(by_id[cid].topic), by_id[cid].topic):
                    base_of[q][cid] = t
            by_q[q] = [by_id[i] for i in base_of[q]] + by_q[q]
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
        if cur not in state["done"]:  # a done question comes back when a mock adds cards to it
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
    later = dict(held)  # the questions after this one, so their answers can be written ahead (MOCK_FIX_DAILY, ANSWER_AGENT)
    later.update({c.id: 1.0 for c in by_q[cur]})
    rest = [q for q in by_q if q not in state["done"] and q not in skip and q != cur]
    upcoming = []
    for _ in range(3):
        if not rest:
            break
        b = model.coverage(later)

        def more(q: str) -> float:
            t = dict(later)
            t.update({c.id: 1.0 for c in by_q[q]})
            return model.coverage(t) - b

        nxt = max(rest, key=more)
        upcoming.append(nxt)
        rest.remove(nxt)
        later.update({c.id: 1.0 for c in by_q[nxt]})
    state["upcoming"] = upcoming
    todo = [c for c in by_q[cur] if c.id not in seen or c.id in due]
    return {"state": state, "question": cur, "title": title(cur), "parts": parts(cur, todo, node, title(cur), base_of.get(cur, {}), title),
            "cards": [c.id for c in todo],
            "reviews": [c.id for q in state["done"] for c in by_q.get(q, []) if c.id in due],
            "coverage": covered, "gain": covered - base, "left": len([q for q in by_q if q not in state["done"] and q not in skip]) - 1}


def parts(q: str, todo: list, node: dict | None, name: str, base: dict[str, str] | None = None, title=None) -> list[dict]:
    """Today's cards in teaching order: the mock's fixes, then the foundations one sub-deck per topic (in learning
    order), then one part per child of the question in the skeleton's order (完整答案, 摘要, 考点, 拓展 …). Anki deals
    a deck by import position, which follows import batches, so only sub-decks in this order keep the teaching order."""
    base = base or {}
    kids = [k.id for k in node[q].children] if node and q in node else []

    def child(c) -> str:
        path = [x.id for x in node[c.leaf].path()] if node and c.leaf in node else []
        i = path.index(q) if q in path else -1
        return path[i + 1] if 0 <= i < len(path) - 1 else q

    out: dict[str, list] = {}
    mock = [c.id for c in sorted(todo, key=lambda c: c.rank) if MOCK_FIX in c.id]  # weak spots a mock of this question exposed
    if mock:
        out[MOCK_FIX] = mock
    for c in todo:  # foundations keep their learning order
        if c.id in base:
            out.setdefault("base:" + base[c.id], []).append(c.id)
    own = [c for c in todo if c.id not in base and MOCK_FIX not in c.id]
    for c in sorted(own, key=lambda c: (kids.index(child(c)) if child(c) in kids else len(kids), c.rank)):
        out.setdefault(child(c), []).append(c.id)

    def label(k: str) -> str:
        if k == MOCK_FIX:
            return "模拟面试补强"
        if k.startswith("base:"):
            return "基础 · " + (title(k[5:]) if title else k[5:])
        t = node[k].title.replace(f" · {name}", "") if node and k in node else "其他"
        return "八股关联" if t == name else t  # the links node carries the question's own title

    start = 0 if mock else 1  # the mock's part is 0, before everything else
    return [{"label": f"{n:02d} {label(k)}", "cards": ids} for n, (k, ids) in enumerate(out.items(), start)]


def stage(d: dict) -> str:
    """The sub-deck of today's question: its name and the coverage once it is learnt."""
    return f"1 {d['title']} · 学完考点覆盖 {d['coverage']:.1%}（+{d['gain']:.1%}）"


def save(d: dict) -> None:
    STATE.write_text(json.dumps(d["state"], ensure_ascii=False, indent=1), encoding="utf-8")
