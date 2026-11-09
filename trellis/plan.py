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
DIMINISH_POINT = 0.6  # and from the same exam point, much less: a second card on a point adds little the same day
HELD_CARDS = 3  # a point is held once about this many of its cards are; a point taught by ten cards does not need all ten
READ_UNIT = 400  # characters: a card this long costs twice the attention of a very short one
FIRST_PASS_MAX = 2000  # characters: a card longer than this waits until it has been split or the basics are held
LOOKAHEAD = 3  # a leaf is taken in order, but its next cards count: a valuable card must not wait behind a cheap intro
SECONDARY_POINT = 0.5  # a card's points after its primary one count this much


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
    graded: bool = False  # freq was computed from the exam points the card teaches
    point: str = ""  # the card's primary exam point, when graded
    length: int = 0  # characters of answer text; 0 when unknown

    @property
    def weight(self) -> float:
        """Its share of the topic: by level, by how often its point is asked, and front-loaded. A topic's first
        cards (the summary, the main chain) carry most of what an interviewer probes; the tail is detail."""
        # graded cards already carry their importance in freq, so position only nudges toward the teaching order
        position = (1 + self.rank / 20) ** -0.4 if self.graded else (1 + self.rank / 8) ** -0.8
        return LEVEL_WEIGHT.get(self.level, DEFAULT_LEVEL) * (1.3 if self.core else 1.0) * position * self.freq

    @property
    def cost(self) -> float:
        """Relative time to learn: a hard card is worth as much but takes longer, so it pays less per minute."""
        return 1.0 + 0.6 * self.difficulty


@dataclass
class PointModel:
    """Exam points: what each is worth, and which cards teach it (primary first). With this the plan measures coverage
    on points, not topics: a point is covered when it is held, however many other cards its topic has."""
    weight: dict[str, float]
    cards: dict[str, list[str]]

    def teaching(self) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for ks in self.cards.values():
            for i, k in enumerate(ks):
                out[k] += 1.0 if i == 0 else SECONDARY_POINT
        return out

    def mastery(self, card_mastery: dict[str, float]) -> dict[str, float]:
        """Point -> the mean of its best `HELD_CARDS` cards, so an unseen extra card does not count against it."""
        held: dict[str, list[float]] = defaultdict(list)
        for cid, ks in self.cards.items():
            for k in ks:
                held[k].append(card_mastery.get(cid, 0.0))
        return {k: sum(sorted(v, reverse=True)[:HELD_CARDS]) / min(HELD_CARDS, len(v)) for k, v in held.items()}

    def coverage(self, card_mastery: dict[str, float]) -> float:
        """The share of all point weight that is held."""
        held = self.mastery(card_mastery)
        total = sum(self.weight.get(k, 0.0) for k in held) or 1.0
        return sum(self.weight.get(k, 0.0) * m for k, m in held.items()) / total

    def card_value(self, cid: str) -> float:
        """What learning this card is worth with nothing held: its points' weight, shared among the cards needed."""
        n = self.teaching_cached()
        return sum(self.weight.get(k, 0.0) * (1.0 if i == 0 else SECONDARY_POINT) / max(1.0, min(HELD_CARDS, n[k]))
                   for i, k in enumerate(self.cards.get(cid, [])))

    def teaching_cached(self) -> dict[str, float]:
        if not hasattr(self, "_teaching"):
            self._teaching = self.teaching()
        return self._teaching


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
         boost: dict[str, float], now_ms: int, budget: int, exclude: set[str] = frozenset(), spread: float = 0.5,
         points: PointModel | None = None) -> Plan:
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

    point_held: dict[str, float] = {}
    if points:  # weight and mastery of a topic are what its exam points add up to
        point_held = points.mastery(mastery)
        topic_of = {c.id: c.topic for c in cards}
        where: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        for cid, ks in points.cards.items():
            if cid in topic_of:
                for i, k in enumerate(ks):
                    where[k][topic_of[cid]] += 1.0 if i == 0 else SECONDARY_POINT
        raw, held_w = defaultdict(float), defaultdict(float)
        for k, by in where.items():
            z = sum(by.values())
            for t, v in by.items():
                w = points.weight.get(k, 0.0) * v / z
                raw[t] += w * boost.get(t, 1.0)
                held_w[t] += w * point_held.get(k, 0.0)
        norm = sum(raw.values()) or 1.0
        for t, s in topics.items():
            plain = raw[t] / (boost.get(t, 1.0) or 1.0)
            s.weight = raw[t] / norm
            s.mastery = held_w[t] / plain if plain else 0.0

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
    if points:
        n = points.teaching_cached()
        known = [points.card_value(c.id) for c in cards if points.cards.get(c.id)]
        typical = sorted(known)[len(known) // 2] if known else 0.0
        for c in cards:
            ks = points.cards.get(c.id)
            if ks is None:  # not annotated yet: still learnable, at a typical value
                worth = typical
            else:  # what it adds: each point's weight, shared among the cards needed, on what is not held
                worth = sum(points.weight.get(k, 0.0) * (1.0 if i == 0 else SECONDARY_POINT) / max(1.0, min(HELD_CARDS, n[k]))
                            * (1 - point_held.get(k, 0.0)) for i, k in enumerate(ks))
            card_value[c.id] = worth * boost.get(c.topic, 1.0) * (1 - mastery[c.id]) * topics[c.topic].readiness / c.cost
    else:
        for t, cs in by_topic.items():
            wsum = sum(c.weight for c in cs) or 1.0
            for c in cs:
                card_value[c.id] = topics[t].weight * c.weight / wsum * (1 - mastery[c.id]) * topics[t].readiness / c.cost

    picked = pick(cards, traces, card_value, prereqs, budget, exclude)
    if points:
        held = points.coverage(mastery)
        n = points.teaching_cached()
        ranked_points = sorted(n, key=lambda k: -points.weight.get(k, 0.0) / max(1.0, min(HELD_CARDS, n[k])))
        total_w = sum(points.weight.get(k, 0.0) for k in ranked_points) or 1.0
        n_cards = sum(min(HELD_CARDS, n[k]) for k in ranked_points) or 1
        curve, cc, cw = [], 0.0, 0.0
        for k in ranked_points:  # learning the cards a point needs, most valuable point first
            cc += min(HELD_CARDS, n[k])
            cw += points.weight.get(k, 0.0)
            curve.append((cc / n_cards, cw / total_w))
        return Plan(topics=topics, card_value=card_value, card_mastery=mastery, picked=picked, held=held, pareto=curve)
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


def coverage_order(cards: list[CardInfo], mastery: dict[str, float], points: PointModel, budget: int,
                   learned: float = 0.58) -> tuple[list[str], dict[str, float]]:
    """The `budget` cards that add the most exam-point coverage, chosen one at a time, each leaf in its teaching order.

    A point is held by its best `HELD_CARDS` cards, so the gain of a card shrinks as a point fills up and is zero once the
    point has enough. Cards are compared by gain per unit of reading, so a short sharp card comes before a long one that
    adds the same, and cards longer than `FIRST_PASS_MAX` wait. Returns the ids in the order chosen and each one's gain."""
    top: dict[str, list[float]] = {}
    counts: dict[str, int] = defaultdict(int)
    for cid, ks in points.cards.items():
        for k in ks:
            counts[k] += 1
            top.setdefault(k, []).append(mastery.get(cid, 0.0))
    for k in top:
        top[k] = sorted(top[k], reverse=True)[:HELD_CARDS]

    def gain(c: CardInfo) -> float:
        total = 0.0
        for i, k in enumerate(points.cards.get(c.id, [])):
            value = learned * (1.0 if i == 0 else SECONDARY_POINT)
            have = top.get(k, [])
            if value > mastery.get(c.id, 0.0):
                better = sorted(have + [value], reverse=True)[:HELD_CARDS]
                total += points.weight.get(k, 0.0) * (sum(better) - sum(have)) / min(HELD_CARDS, counts[k])
        return total

    leaves: dict[str, list[CardInfo]] = defaultdict(list)
    for c in cards:
        if c.length <= FIRST_PASS_MAX:
            leaves[c.leaf].append(c)
    for cs in leaves.values():
        cs.sort(key=lambda c: c.order)
    heads = {leaf: 0 for leaf in leaves}

    def per_reading(c: CardInfo) -> float:
        return gain(c) / (1 + c.length / READ_UNIT)

    order: list[str] = []
    gains: dict[str, float] = {}
    while len(order) < budget:
        best, best_v = None, 0.0
        for leaf, i in heads.items():
            v = max((per_reading(x) for x in leaves[leaf][i:i + LOOKAHEAD]), default=0.0)
            if v > best_v:
                best, best_v = leaf, v
        if best is None:
            break
        c = leaves[best][heads[best]]
        order.append(c.id)
        gains[c.id] = gain(c)
        for i, k in enumerate(points.cards.get(c.id, [])):
            value = learned * (1.0 if i == 0 else SECONDARY_POINT)
            top[k] = sorted(top.get(k, []) + [value], reverse=True)[:HELD_CARDS]
        heads[best] += 1
    return order, gains


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
    taken_point: dict[str, int] = defaultdict(int)  # and from each exam point
    out: list[CardInfo] = []
    while len(out) < budget:
        best, best_v = None, -1.0
        for leaf, i in heads.items():
            cs = leaves[leaf]
            if i < len(cs):
                v = max(value[x.id] for x in cs[i:i + LOOKAHEAD]) * DIMINISH ** taken[cs[i].topic]  # one topic eight times a day teaches less than eight topics
                if cs[i].point:
                    v *= DIMINISH_POINT ** taken_point[cs[i].point]
                if v > best_v:
                    best, best_v = leaf, v
        if best is None:
            break
        c = leaves[best][heads[best]]
        out.append(c)
        taken[c.topic] += 1
        if c.point:
            taken_point[c.point] += 1
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
