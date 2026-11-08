"""Plan: which cards are worth learning next, and how much of an interview a learner already holds.

Hold (hold.py) says how well each card is retained. A plan needs three more numbers, all per topic and per leaf:

* **Weight**: how much the topic is worth in an interview. A design question carries its own weight (how often it
  is reported, whether the target companies ask it). A concept carries the weight of the questions that lean on it,
  so a concept every frequent question needs outranks a famous but isolated one. That is the 80/20, made explicit and
  computed rather than guessed.
* **Mastery**: how much of the topic is held now. A card's mastery is its Hold, decayed by the time since it was last
  seen (an interval is the scheduler's estimate of when recall falls to about 90%).
* **Readiness**: whether the topic's prerequisites hold. A question whose concepts are unknown is not the next thing
  to study; its concepts are.

The value of learning a card next is its share of the weight, times what is not yet held, times readiness. Picking
cards by that value, in the order each leaf teaches them and prerequisites first, is the plan.

Pure functions over plain data, like hold.py: nothing here talks to Anki or reads files.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .hold import card_hold
from .traces import Trace

LEVEL_WEIGHT = {"必会": 1.0, "追问": 0.6, "加分": 0.3}
DEFAULT_LEVEL = 0.8
READY_AT = 0.4  # prerequisite mastery at which a dependant counts as fully ready
DIMINISH = 0.8  # each further card from the same topic in one round is worth this much less


@dataclass
class CardInfo:
    id: str
    leaf: str
    topic: str
    order: int  # position within its leaf (the leaf's teaching order)
    level: str = ""  # 必会 / 追问 / 加分, or empty
    core: bool = False
    rank: int = 0  # position in its topic's teaching order (0 = first)
    freq: float = 1.0  # how often interviews probe what this card covers, relative to its topic's other cards
    difficulty: float = 0.3  # 0 easy .. 1 hard: intrinsic before study, blended with the learner's record after

    @property
    def weight(self) -> float:
        """Its share of the topic: by level, by how often its point is asked, and front-loaded. A topic's first
        cards (the summary, the main chain) carry most of what an interviewer probes; the tail is detail."""
        position = (1 + self.rank / 8) ** -0.8
        return LEVEL_WEIGHT.get(self.level, DEFAULT_LEVEL) * (1.3 if self.core else 1.0) * position * self.freq

    @property
    def cost(self) -> float:
        """Relative time to learn: a hard card is worth as much but takes longer, so it pays less per minute."""
        return 1.0 + 0.6 * self.difficulty


@dataclass
class Edge:
    src: str  # the topic that leans on dst (a question, or a concept built on another)
    dst: str
    strength: float  # 1.0 a hard prerequisite, lower for a looser tie
    kind: str = "requires"


@dataclass
class TopicScore:
    topic: str
    weight: float = 0.0  # share of the whole interview, sums to 1 over topics
    mastery: float = 0.0  # weighted by card importance
    progress: float = 0.0  # share of cards ever seen
    readiness: float = 1.0
    cards: int = 0
    seen: int = 0
    value: float = 0.0  # weight x (1 - mastery) x readiness: what studying it now is worth
    reasons: list[str] = field(default_factory=list)


@dataclass
class Plan:
    topics: dict[str, TopicScore]
    card_value: dict[str, float]
    card_mastery: dict[str, float]
    picked: list[str]  # card ids to learn next, in order
    held: float  # weight-averaged mastery over the whole tree: the interview share already held
    pareto: list[tuple[float, float]]  # (cumulative card share, cumulative weight share), topics by weight


def card_mastery(trace: Trace | None, now_ms: int) -> float:
    """Hold, decayed by the time since the last review: 0.9 at one interval, lower after."""
    h = card_hold(trace)
    if h is None:
        return 0.0
    if trace.last_review and trace.interval > 0:
        elapsed = max(0.0, (now_ms - trace.last_review) / 86_400_000)
        h *= 0.9 ** (elapsed / trace.interval) / 0.9 if elapsed > trace.interval else 1.0
    return max(0.0, min(1.0, h))


def topic_weights(base: dict[str, float], edges: list[Edge], boost: dict[str, float], spread: float = 0.5) -> dict[str, float]:
    """Each topic keeps (1 - spread) of its base weight and passes `spread` down its edges, split by strength; the
    flow repeats down chains of prerequisites. A concept many heavy questions need ends up heavy. Personal boosts
    (weak spots from a mock, a target company's focus) multiply the result. Normalised to sum to 1."""
    out_edges = defaultdict(list)
    for e in edges:
        out_edges[e.src].append(e)
    weight = defaultdict(float)
    frontier = dict(base)
    for _ in range(6):  # chains are short; six hops is plenty
        nxt = defaultdict(float)
        for t, w in frontier.items():
            es = out_edges.get(t)
            if not es:
                weight[t] += w
                continue
            weight[t] += w * (1 - spread)
            total = sum(e.strength for e in es)
            for e in es:
                nxt[e.dst] += w * spread * e.strength / total
        frontier = nxt
        if not frontier:
            break
    for t, w in frontier.items():
        weight[t] += w
    for t, b in boost.items():
        if t in weight:
            weight[t] *= b
    z = sum(weight.values()) or 1.0
    return {t: w / z for t, w in weight.items()}


def plan(cards: list[CardInfo], traces: dict[str, Trace], base: dict[str, float], edges: list[Edge],
         boost: dict[str, float], now_ms: int, budget: int, exclude: set[str] = frozenset(), spread: float = 0.5) -> Plan:
    by_topic: dict[str, list[CardInfo]] = defaultdict(list)
    for c in cards:
        by_topic[c.topic].append(c)
    # every topic gets a floor so a topic no question names still counts a little
    floor = {t: 0.1 * (sum(base.values()) / max(len(base), 1)) for t in by_topic}
    weights = topic_weights({t: base.get(t, 0.0) + floor[t] for t in by_topic}, edges, boost, spread)

    mastery = {c.id: card_mastery(traces.get(c.id), now_ms) for c in cards}
    topics: dict[str, TopicScore] = {}
    for t, cs in by_topic.items():
        wsum = sum(c.weight for c in cs)
        topics[t] = TopicScore(topic=t, weight=weights.get(t, 0.0), cards=len(cs),
                               seen=sum(1 for c in cs if traces.get(c.id) and traces[c.id].reps),
                               mastery=sum(c.weight * mastery[c.id] for c in cs) / wsum if wsum else 0.0)
        topics[t].progress = topics[t].seen / len(cs)

    prereqs = defaultdict(list)
    for e in edges:
        if e.kind == "requires" and e.src in topics and e.dst in topics:
            prereqs[e.src].append(e.dst)
    for t, s in topics.items():
        ps = prereqs.get(t, [])
        if ps:
            r = sum(min(1.0, topics[p].mastery / READY_AT) for p in ps) / len(ps)
            s.readiness = 0.35 + 0.65 * r  # never fully blocked: a question can be read before its concepts settle
        s.value = s.weight * (1 - s.mastery) * s.readiness

    # a card's value: its share of its topic's weight, what is not held, the topic's readiness
    card_value = {}
    for t, cs in by_topic.items():
        wsum = sum(c.weight for c in cs) or 1.0
        for c in cs:
            card_value[c.id] = topics[t].weight * c.weight / wsum * (1 - mastery[c.id]) * topics[t].readiness / c.cost

    picked = pick(cards, traces, card_value, prereqs, budget, exclude)
    total_w = sum(s.weight for s in topics.values()) or 1.0
    held = sum(s.weight * s.mastery for s in topics.values()) / total_w
    ranked = sorted(topics.values(), key=lambda s: -s.weight / max(s.cards, 1))
    n_cards = sum(s.cards for s in ranked) or 1
    curve, cc, cw = [], 0, 0.0
    for s in ranked:
        cc += s.cards
        cw += s.weight
        curve.append((cc / n_cards, cw / total_w))
    return Plan(topics=topics, card_value=card_value, card_mastery=mastery, picked=picked, held=held, pareto=curve)


def pick(cards: list[CardInfo], traces: dict[str, Trace], value: dict[str, float], prereqs: dict[str, list[str]],
         budget: int, exclude: set[str]) -> list[str]:
    """The `budget` most valuable unseen cards, taken in each leaf's teaching order (a leaf's third card never comes
    before its first), then ordered so a prerequisite topic's cards come before its dependants'."""
    leaves: dict[str, list[CardInfo]] = defaultdict(list)
    for c in cards:
        if c.id in exclude or (traces.get(c.id) and traces[c.id].reps):
            continue
        leaves[c.leaf].append(c)
    for cs in leaves.values():
        cs.sort(key=lambda c: c.order)
    heads = {leaf: 0 for leaf in leaves}
    taken: dict[str, int] = defaultdict(int)  # cards already taken from each topic this round
    out: list[CardInfo] = []
    while len(out) < budget:
        best, best_v = None, -1.0
        for leaf, i in heads.items():
            cs = leaves[leaf]
            if i < len(cs):
                v = value[cs[i].id] * DIMINISH ** taken[cs[i].topic]  # one topic eight times a day teaches less than eight topics
                if v > best_v:
                    best, best_v = leaf, v
        if best is None:
            break
        c = leaves[best][heads[best]]
        out.append(c)
        taken[c.topic] += 1
        heads[best] += 1
    depth = {}

    def level(t, seen=()):
        if t in depth:
            return depth[t]
        if t in seen:
            return 0
        d = 1 + max((level(p, seen + (t,)) for p in prereqs.get(t, [])), default=-1)
        depth[t] = d
        return d
    order = {id(c): i for i, c in enumerate(out)}
    out.sort(key=lambda c: (level(c.topic), c.topic, c.order, order[id(c)]))
    return [c.id for c in out]
