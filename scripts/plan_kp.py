"""Exam points (考点): the layer below a topic, and what each one is worth.

Data (gitignored, written by agents following research/sysdesign/KP_AGENT.md):
- sources/local/plan/kp/topics/<topic>.json      a concept topic's points and which card teaches which point
- sources/local/plan/kp/questions/<topic>.json   a design question's needs (catalog points, with role) and own points
- sources/local/plan/kp/merge.json               {"<point id>": "<canonical id>"}: the same idea under several topics

Weight of a point. Each question q, asked with frequency w_q, splits its weight:
- `spread` of it goes to the catalog points it needs, in proportion to role: 必讲 1.0, 追问 0.6, 加分 0.3;
- the rest stays with its own points (its core trick, its data model), split the same way.
A concept topic's directly reported frequency (reports that name the topic) is shared among its points, core points
counting double. Every point keeps a small floor so an unasked point is ranked, not erased.

Value of a card: the sum, over the points it teaches, of the point's weight divided by how many cards teach it (a
card's primary point counts fully, the others half). Mastery of a point: the mean of its three best-held cards.
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KP = ROOT / "sources/local/plan/kp"
ROLE = {"必讲": 1.0, "追问": 0.6, "加分": 0.3}
SECONDARY = 0.5
HELD_CARDS = 3  # a point is held once about this many of its cards are; a point taught by ten cards does not need all ten
META = {"dlv.level-expectations", "dlv.prep-plan", "dlv.prep-practice", "dlv.problem-catalog", "dlv.variant-recognition",
        "dlv.oral-playbook", "dlv.rubric", "ld.scoring-dimensions"}  # about the interview itself, not something an answer states


@dataclass
class Points:
    meta: dict[str, dict] = field(default_factory=dict)               # point -> {title, kind, core, topic, summary}
    card: dict[str, list[str]] = field(default_factory=dict)          # card id -> points, primary first
    needs: dict[str, list[dict]] = field(default_factory=dict)        # question -> [{kp, role, why}]
    own: dict[str, list[dict]] = field(default_factory=dict)          # question -> own points [{id, title, role}]
    alias: dict[str, str] = field(default_factory=dict)

    def canon(self, k: str) -> str:
        return self.alias.get(k, k)

    @property
    def ready(self) -> bool:
        return bool(self.meta)


def load() -> Points:
    pts = Points()
    merge = KP / "merge.json"
    if merge.exists():
        pts.alias = {k: v for k, v in json.loads(merge.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    for f in sorted((KP / "topics").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for k in d["kps"]:
            c = pts.canon(k["id"])
            m = pts.meta.setdefault(c, {"members": [], "core": False})
            m["members"].append(k["id"])
            core = m["core"] or k.get("core", False)
            if k["id"] == c or "id" not in m:  # the canonical point's own title and topic win over a merged member's
                m.update({**k, "id": c, "topic": d["topic"]})
            m["core"] = core
        for cid, ks in d["cards"].items():
            pts.card[cid] = list(dict.fromkeys(pts.canon(k) for k in ks))
    for f in sorted((KP / "questions").glob("*.json")) if (KP / "questions").exists() else []:
        d = json.loads(f.read_text(encoding="utf-8"))
        q = d["topic"]
        pts.needs[q] = [{**n, "kp": pts.canon(n["kp"])} for n in d.get("needs", [])
                        if pts.canon(n["kp"]) in pts.meta and pts.canon(n["kp"]) not in META]
        pts.own[q] = d.get("own", [])
        for o in pts.own[q]:
            pts.meta.setdefault(o["id"], {**o, "topic": q, "kind": "design", "core": o.get("role") == "必讲", "members": [o["id"]]})
        for cid, ks in d.get("cards", {}).items():
            pts.card[cid] = list(dict.fromkeys(pts.canon(k) for k in ks if pts.canon(k) in pts.meta))
    return pts


def weights(pts: Points, question_freq: dict[str, float], concept_direct: dict[str, float], spread: float) -> dict[str, float]:
    """Point -> weight; sums to about the total question frequency plus the direct concept mass."""
    w = defaultdict(float)
    for q, f in question_freq.items():
        needs, own = pts.needs.get(q, []), pts.own.get(q, [])
        rn = sum(ROLE.get(n["role"], 0.6) for n in needs)
        ro = sum(ROLE.get(o.get("role"), 0.6) for o in own)
        share_needs = spread if rn else 0.0
        share_own = (1 - share_needs) if ro else 0.0
        for n in needs:
            w[n["kp"]] += f * share_needs * ROLE.get(n["role"], 0.6) / rn
        for o in own:
            w[o["id"]] += f * share_own * ROLE.get(o.get("role"), 0.6) / ro
    by_topic = defaultdict(list)
    for k, m in pts.meta.items():
        by_topic[m["topic"]].append(k)
    for t, f in concept_direct.items():
        ks = by_topic.get(t, [])
        z = sum(2.0 if pts.meta[k].get("core") else 1.0 for k in ks)
        for k in ks:
            w[k] += f * (2.0 if pts.meta[k].get("core") else 1.0) / z
    total = sum(w.values()) or 1.0
    floor = 0.05 * total / max(len(pts.meta), 1)
    return {k: w.get(k, 0.0) + floor for k in pts.meta}


def card_values(pts: Points, kp_w: dict[str, float]) -> dict[str, float]:
    teach = defaultdict(float)
    for ks in pts.card.values():
        for i, k in enumerate(ks):
            teach[k] += 1.0 if i == 0 else SECONDARY
    out = {}
    for cid, ks in pts.card.items():
        out[cid] = sum(kp_w.get(k, 0.0) * (1.0 if i == 0 else SECONDARY) / teach[k] for i, k in enumerate(ks))
    return out


def mastery(pts: Points, card_mastery: dict[str, float]) -> dict[str, float]:
    """Point -> mastery: the mean of its best `HELD_CARDS` cards, so an unseen extra card does not count against it."""
    held = defaultdict(list)
    for cid, ks in pts.card.items():
        for k in ks:
            held[k].append(card_mastery.get(cid, 0.0))
    return {k: sum(sorted(v, reverse=True)[:HELD_CARDS]) / min(HELD_CARDS, len(v)) for k, v in held.items()}


def required_by(pts: Points) -> dict[str, list[tuple[str, str, str]]]:
    """Point -> [(question, role, why)]."""
    out = defaultdict(list)
    for q, ns in pts.needs.items():
        for n in ns:
            out[n["kp"]].append((q, n["role"], n.get("why", "")))
    return out
