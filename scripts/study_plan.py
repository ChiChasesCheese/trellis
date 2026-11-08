"""Daily study plan: score every topic and leaf, summarise yesterday, deal the next cards into Anki, draw the dashboard.

    uv run python scripts/study_plan.py report          # compute and write the report + dashboard, change nothing in Anki
    uv run python scripts/study_plan.py daily           # report, then rebuild the 今日计划 deck and its report card
    uv run python scripts/study_plan.py serve --host <tailnet ip> [--minutes 30]   # the dashboard, live, then stop

The model is trellis/plan.py (weight x not-yet-held x readiness). This script is the adapter: it reads the merged
skeleton and its cards, pulls card states and review logs from AnkiConnect, and feeds them in. Topics are the
skeleton's deck groups (one Anki deck each); TikTok questions are one topic each. A question's weight is how often it
is reported (summaries carry 「报告 N 次」), with a bonus for the classic ten; concepts inherit weight through three kinds
of edge: a question's `requires`, the 八股 a question's map card links ([[node]]), and the cross-question patterns
that list it. Personal boosts live in sources/local/plan/config.json.

Outputs stay local (personal study data): sources/local/plan/{state.json, history.jsonl, report.html, index.html}.
In Anki: the deck 今日计划 with 0 今日报告 / 1 弱项补强 / 2 概念与技术 / 3 题目与整轮; studied cards go back to their own
deck tagged 今日计划::已学; the report card is reset to new each day so it is the first thing shown.
"""
from __future__ import annotations

import html
import json
import math
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import daily_extra  # noqa: E402
import plan_kp  # noqa: E402
from trellis.plan import HELD_CARDS, CardInfo, Edge, PointModel, plan  # noqa: E402
from trellis.project import load_project  # noqa: E402
from trellis.sequence import core_leaves  # noqa: E402
from trellis.traces import Trace  # noqa: E402

DOMAIN = "sysdesign"
OUT = ROOT / "sources/local/plan"
DECK = "今日计划"
OLD_DECK = "今日 100（面试轮廓）"
DONE_TAG = "今日计划::已学"
REPORT_TAG = "plan::report"
STAGES = {"s00": "1 弱项补强", "s05": "3 题目与整轮", "s07": "3 题目与整轮", "s08": "3 题目与整轮"}
STAGE_DEFAULT = "2 概念与技术"
TOPIC_DEPTH = {"s08": 3}  # TikTok: one topic per question, not one per section
EXTRA = {f"q.{m}" for m in ("cdn-design", "pastebin", "object-storage", "auth-service", "reddit", "social-graph", "email-service",
                             "video-conferencing", "google-maps", "calendar", "e-commerce", "in-the-wild", "uid")}
cfg_global: dict = {}
CONCEPT_SHARE = 0.3  # direct concept evidence counts this much against the question mass (which sums to about 1)
EVIDENCE = ROOT / "sources/local/plan/evidence/bank.json"


def load_evidence():
    return json.loads(EVIDENCE.read_text(encoding="utf-8")) if EVIDENCE.exists() else None


def concept_words() -> dict:
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from plan_evidence import CONCEPTS
        return CONCEPTS
    except Exception:  # noqa: BLE001 - the planner runs without the evidence module
        return {}


CONCEPT_WORDS = concept_words()
STOP_TERMS = {"design", "system", "what", "when", "with", "this", "that", "from", "into", "your", "have", "does", "data", "time",
              "user", "users", "service", "api", "the", "and", "for", "how", "why", "which"}


def report_corpus() -> dict[str, float]:
    """term -> share of system-design report descriptions that use it (lower-case substring), for terms cards use."""
    bank = ROOT / "sources/local/hello-interview/premium/questions.json"
    if not bank.exists():
        return {}
    descs = [(r.get("description") or "").lower() for q in json.loads(bank.read_text(encoding="utf-8"))
             if q["defaultInterviewType"] in ("SYSTEM_DESIGN", "OBJECT_ORIENTED_DESIGN") for r in q["upvotes"] if r.get("description")]
    descs += [(q["title"] or "").lower() for q in json.loads(bank.read_text(encoding="utf-8"))]

    class Lazy(dict):
        def __missing__(self, term):
            v = sum(1 for d in descs if term in d) / max(1, len(descs))
            self[term] = v
            return v

        def get(self, term, default=0.0):
            return self[term]
    return Lazy()
LLD_FOUNDATIONS = {"t.lld-delivery", "t.lld-concurrency", "t.lld-cross"}
TOP10 = {"q.bitly", "q.dropbox", "q.ticketmaster", "q.news-feed", "q.chat", "q.leetcode", "q.uber", "q.web-crawler",
         "q.ad-click", "q.fb-post-search"}  # Hello Interview's ten most common problems
DAY_MS = 86_400_000


def call(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    for _ in range(90):
        with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8765", body), timeout=600) as r:
            out = json.load(r)
        if out["error"] and "lifecycle" in out["error"]:
            time.sleep(3)
            continue
        if out["error"]:
            raise RuntimeError(f"{action}: {out['error']}")
        return out["result"]
    raise RuntimeError("Anki stayed busy")


def config() -> dict:
    p = OUT / "config.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


# ---------------------------------------------------------------- the tree


class Tree:
    def __init__(self):
        self.project = load_project(ROOT, DOMAIN)
        self.sk = self.project.skeleton
        self.node = self.sk.by_id
        self.core = core_leaves(self.sk)

    def path(self, nid):
        return self.node[nid].path()

    def top(self, nid):
        return self.path(nid)[0].id

    def topic(self, nid):
        p = self.path(nid)
        depth = TOPIC_DEPTH.get(p[0].id, self.sk.deck_depth or 2)
        return p[min(depth, len(p)) - 1].id

    def title(self, nid):
        return self.node[nid].title


def card_level(q: str) -> str:
    first = next((x for x in q.splitlines() if x.strip()), "")
    m = re.search(r"(必会|追问|加分)", first)
    return m.group(1) if m else ""


def card_title(q: str) -> str:
    first = next((x for x in q.splitlines() if x.strip()), "")
    first = re.sub(r"\*\*|\{\{c\d+::|\}\}", "", first)
    return first.split("｜")[0].strip()[:40]


def build_inputs(tree: Tree):
    cards, titles = [], {}
    for c in tree.project.cards:
        if c.node not in tree.node or tree.node[c.node].children:
            continue
        q = c.render(None)[0]
        cards.append(CardInfo(id=c.id, leaf=c.node, topic=tree.topic(c.node), order=c.step or 999,
                              level=card_level(q), core=c.node in tree.core))
        titles[c.id] = card_title(q)
    leaf_pos = {n.id: i for i, n in enumerate(tree.sk.walk())}
    by_topic = defaultdict(list)
    for c in cards:
        by_topic[c.topic].append(c)
    for cs in by_topic.values():  # teaching order inside a topic: tree order of leaves, then each leaf's steps
        for r, c in enumerate(sorted(cs, key=lambda c: (leaf_pos[c.leaf], c.order))):
            c.rank = r
    skip = tuple(cfg_global.get("skip", []))
    cards = [c for c in cards if not c.topic.startswith(skip) and not c.leaf.startswith(skip)]
    topics = {c.topic for c in cards}

    # base weight. With evidence (scripts/plan_evidence.py): a question's company-normalised, target-mixed frequency,
    # and a concept's direct share of what reports name; without it, the bank counts in the skeleton's summaries.
    ev = load_evidence()
    reports = defaultdict(float)
    for n in tree.sk.walk():
        m = re.search(r"报告\s*(\d+)\s*次", n.summary or "")
        if m and not n.children:
            reports[tree.topic(n.id)] += math.log1p(int(m.group(1)))
    med = median(reports.values()) if reports else 1.0
    base = {}
    if ev:
        qf = {t: v["freq"] for t, v in ev["questions"].items() if t in topics}
        cf = ev.get("concepts", {})
        qmed = median(qf.values()) if qf else 0.01
        for t in topics:
            top = tree.top(t)
            if t in qf:
                base[t] = qf[t]
            elif t in EXTRA:
                base[t] = qmed * 0.3
            elif top in ("s05", "s08") or (top == "s07" and t not in LLD_FOUNDATIONS):
                base[t] = qmed * 0.5  # a question no source reports: kept, but below the median reported one
            elif top == "s06":
                base[t] = qmed * 0.6 + CONCEPT_SHARE * cf.get(t, 0.0)
            elif top == "s00":
                base[t] = qmed * 2  # weak spots found in a real mock
            else:
                base[t] = CONCEPT_SHARE * cf.get(t, 0.0)  # what reports name directly; the rest flows in from questions
    else:
        for t in topics:
            top = tree.top(t)
            if t in reports:
                base[t] = reports[t] * (1.4 if t in TOP10 else 1.0)
            elif t in EXTRA:
                base[t] = med * 0.3
            elif top in ("s05", "s08") or (top == "s07" and t not in LLD_FOUNDATIONS):
                base[t] = med * (1.4 if t in TOP10 else 0.7)
            elif top == "s06":
                base[t] = med * 0.6
            elif top == "s00":
                base[t] = med
            else:
                base[t] = 0.0

    # card level: how often its point is asked (the concepts it touches, by what reports name), and how hard it is
    cf = (ev or {}).get("concepts", {})
    texts = {c.id: c.render(None) for c in tree.project.cards}
    lengths = sorted(len(re.sub(r"```.*?```", "", texts[c.id][1], flags=re.S)) for c in cards)
    by_topic = defaultdict(list)
    reports_text = report_corpus()
    for c in cards:
        q, a = texts[c.id]
        body = re.sub(r"```svg.*?```", "", (q + a), flags=re.S).lower()
        # concepts beyond the card's own topic that it ties in, weighted by how often reports name them
        c._rel = sum(v for k, v in cf.items() if k != c.topic and any(w in body for w in CONCEPT_WORDS.get(k, [])))
        # the card's own technical terms (the English in its title and question), by how many report descriptions use them
        terms = {t for t in re.findall(r"[a-z][a-z0-9+\-/ ]{2,30}[a-z0-9]", q.lower().split("\n", 1)[0] + " " + q.lower()[:300])
                 if len(t) >= 4 and t not in STOP_TERMS}
        c._hits = max((reports_text.get(t, 0.0) for t in terms), default=0.0)
        plain = len(re.sub(r"```.*?```", "", a, flags=re.S))
        pct = sum(1 for x in lengths if x <= plain) / max(1, len(lengths))
        c.difficulty = min(1.0, 0.5 * pct + {"加分": 0.3, "追问": 0.15}.get(c.level, 0.0) + (0.2 if "```" in a and "```svg" not in a else 0.0))
        by_topic[c.topic].append(c)
    for cs in by_topic.values():
        mean_rel = sum(c._rel for c in cs) / len(cs)
        mean_hit = sum(c._hits for c in cs) / len(cs)
        for c in cs:
            rel = 0.85 + 0.3 * min(2.0, c._rel / mean_rel) / 2 if mean_rel > 0 else 1.0  # 0.85 .. 1.15: ties to other asked concepts
            hit = 0.8 + 0.6 * min(2.0, c._hits / mean_hit) / 2 if mean_hit > 0 else 1.0  # 0.8 .. 1.4: its own terms in reports
            c.freq = rel * hit

    # edges: question -> what it needs
    agg = defaultdict(float)
    kinds = {}

    def is_question(t):
        return question_topic(tree, t)

    def add(src_leaf, dst_leaf, s, kind):
        if src_leaf not in tree.node or dst_leaf not in tree.node:
            return
        a, b = tree.topic(src_leaf), tree.topic(dst_leaf)
        if a == b or a not in topics or b not in topics:
            return
        if kind != "requires" and not (is_question(a) and not is_question(b)):
            return  # a mention only says a question leans on a concept; concept -> question or question <-> question would leak weight
        agg[(a, b)] += s
        kinds[(a, b)] = "requires" if kind == "requires" or kinds.get((a, b)) == "requires" else kind
    for n in tree.sk.walk():
        for r in n.requires:
            add(n.id, r, 1.0, "requires")
    for c in tree.project.cards:  # [[node]] links: a 八股 map names what its question asks; any card naming a node leans on it
        text = (c.question or "") + (c.answer or "") + (getattr(c, "text", "") or "")
        for target in set(re.findall(r"\[\[([a-z][a-z0-9.\-]+)(?:\|[^\]]*)?\]\]", text)):
            add(c.node, target, 0.5 if c.node.startswith("links.") else 0.25, "asks")
    pat_file = ROOT / "research/hello-interview/patterns.json"
    if pat_file.exists():
        slug_topic = {}
        for n in tree.sk.walk():
            m = re.match(r"^(?:qb\.sd|tt\.sd|sd\.problem-breakdowns)\.([a-z0-9-]+)", n.id)
            if m and n.id in tree.node:
                slug_topic.setdefault(m.group(1), n.id)
        for p in json.loads(pat_file.read_text(encoding="utf-8"))["patterns"]:
            leaf = f"sd.cross.{p['id']}"
            for q in p["questions"]:
                if q["slug"] in slug_topic:
                    add(slug_topic[q["slug"]], leaf, 0.6, "pattern")
    for t in topics:  # every design question is answered through the delivery framework and an estimate
        if tree.top(t) in ("s05", "s08"):
            for f, w in (("t.sd-delivery", 0.15), ("t.numbers", 0.12)):
                if f in topics:
                    agg[(t, f)] += w
                    kinds.setdefault((t, f), "asks")
        elif is_question(t) and "t.lld-delivery" in topics:
            agg[(t, "t.lld-delivery")] += 0.15
            kinds.setdefault((t, "t.lld-delivery"), "asks")
    apply_exam_points(tree, cards, base, topics, agg, kinds, is_question, by_topic)
    edges = [Edge(a, b, min(s, 6.0), kinds[(a, b)]) for (a, b), s in agg.items()]
    return cards, titles, base, edges


kp_state: dict = {}  # exam points of this run, for the dashboard and the report


def coverage_metrics(tree, p, gen, cfg) -> dict | None:
    """The numbers the dashboard leads with, all measured on exam points."""
    if not kp_state:
        return None
    pts, model, q_freq = kp_state["points"], kp_state["model"], kp_state["q_freq"]
    m = p.card_mastery
    held = model.mastery(m)
    total = sum(model.weight.get(k, 0.0) for k in held) or 1.0
    touched = {k for cid, ks in pts.card.items() if m.get(cid, 0.0) > 0 for k in ks}
    after = dict(m)
    for cid in kp_state.get("today", p.picked):
        after[cid] = max(after.get(cid, 0.0), LEARNED)
    n = model.teaching_cached()
    # the cheapest way to 80%: points by what they would add per card still to learn
    rest = []
    for k, v in held.items():
        w = model.weight.get(k, 0.0)
        cost = max(1, round((1 - v) * min(HELD_CARDS, n[k])))
        rest.append((w * (1 - v) / cost, w * (1 - v), cost))
    rest.sort(key=lambda r: -r[0])
    cov, need = p.held, 0
    for _, gain, cost in rest:
        if cov >= 0.8:
            break
        cov += gain / total
        need += cost
    rows = []
    for q, f in q_freq.items():
        needs, own = pts.needs.get(q, []), pts.own.get(q, [])
        items = [(n_["kp"], plan_kp.ROLE.get(n_["role"], 0.6), n_["role"]) for n_ in needs] + \
                [(o["id"], plan_kp.ROLE.get(o.get("role"), 0.6), o.get("role")) for o in own]
        z = sum(r for _, r, _ in items)
        if not z or not f or q in NOT_A_QUESTION:
            continue
        ready = sum(r * held.get(k, 0.0) for k, r, _ in items) / z
        missing = sorted((k for k, _, role in items if role == "必讲" and held.get(k, 0.0) < 0.5 and k in pts.meta and k not in plan_kp.META),
                         key=lambda k: -model.weight.get(k, 0.0))
        rows.append({"id": q, "title": tree.title(q), "f": f, "ready": ready, "miss": [pts.meta[k]["title"] for k in missing[:3]],
                     "n_miss": len(missing), "n_must": sum(1 for _, _, role in items if role == "必讲")})
    rows.sort(key=lambda r: -r["f"])
    fz = sum(r["f"] for r in rows) or 1.0
    daily = int(cfg.get("daily_new", 35))
    return {"covered": p.held, "touched": sum(model.weight.get(k, 0.0) for k in touched) / total,
            "after_today": model.coverage(after), "to80_cards": need, "to80_days": math.ceil(need / max(1, daily)), "daily_new": daily,
            "ready": sum(r["f"] * r["ready"] for r in rows) / fz, "ready_n": sum(1 for r in rows if r["ready"] >= 0.6), "ready_total": len(rows),
            "representatives": (gen["representatives"][-1] if gen and gen.get("representatives") else None), "questions": rows[:30]}


LEARNED = 0.58  # mastery of a card just learned and past its first few-day interval


def exam_point_rows(tree, p) -> dict | None:
    """Per point: its weight, the learner's mastery, which questions need it and in what role."""
    if not kp_state:
        return None
    pts, w, teach = kp_state["points"], kp_state["weight"], kp_state["teach"]
    held = plan_kp.mastery(pts, p.card_mastery)
    req = plan_kp.required_by(pts)
    total = sum(w.values()) or 1.0
    q_weight = lambda q: p.topics[q].weight if q in p.topics else 0.0
    rows = {}
    for k, meta in pts.meta.items():
        if k not in held or k not in teach:
            continue
        qs = sorted(req.get(k, []), key=lambda r: -q_weight(r[0]))
        n = Counter(r[1] for r in qs)
        share = w[k] / total
        rows[k] = {"id": k, "title": meta["title"], "kind": meta.get("kind", ""), "core": bool(meta.get("core")), "own": meta["topic"] in pts.needs,
                   "w": share, "m": held[k], "p": share * (1 - held[k]), "n": [n["必讲"], n["追问"], n["加分"]],
                   "q": [[q, tree.title(q) if q in tree.node else q, role, why] for q, role, why in qs[:6]],
                   "cards": round(sum(teach[k].values()))}
    by_topic = defaultdict(list)
    for k in rows:
        for t in teach[k]:
            by_topic[t].append(k)
    for ks in by_topic.values():
        ks.sort(key=lambda k: -rows[k]["w"])
    order = sorted((k for k in rows if not rows[k]["own"]), key=lambda k: -rows[k]["w"])  # points that several questions share
    acc, n80 = 0.0, len(order)
    z = sum(rows[k]["w"] for k in order) or 1.0
    for i, k in enumerate(order):
        acc += rows[k]["w"] / z
        if acc >= 0.8:
            n80 = i + 1
            break
    top = sorted((k for k in rows if not rows[k]["own"] and k not in plan_kp.META), key=lambda k: -rows[k]["p"])[:40]
    return {"rows": rows, "byTopic": dict(by_topic), "top": top, "n80": n80, "n": len(order),
            "questions": len(pts.needs), "cards": sum(1 for ks in pts.card.values() if ks)}


def apply_exam_points(tree, cards, base, topics, agg, kinds, is_question, by_topic) -> None:
    """Where exam points exist, they replace the coarse signals: a question's edges come from the points its answer
    needs, and a card's freq from what the points it teaches are worth."""
    pts = plan_kp.load()
    if not pts.ready:
        return
    topic_of = {c.id: c.topic for c in cards}
    teach: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for cid, ks in pts.card.items():
        if cid in topic_of:
            for i, k in enumerate(ks):
                teach[k][topic_of[cid]] += 1.0 if i == 0 else plan_kp.SECONDARY
    for q, needs in pts.needs.items():
        if q not in topics:
            continue
        for key in [k for k in agg if k[0] == q and kinds.get(k) != "requires" and k[1] not in UNIVERSAL]:
            del agg[key]
            kinds.pop(key, None)
        for n in needs:
            where = {t: v for t, v in teach[n["kp"]].items() if not is_question(t)}
            z = sum(where.values())
            for t, v in where.items():
                agg[(q, t)] += plan_kp.ROLE.get(n["role"], 0.6) * v / z
                kinds.setdefault((q, t), "asks")
    spread = float(cfg_global.get("spread", 0.5))
    q_freq = {t: base.get(t, 0.0) for t in topics if is_question(t)}
    direct = {t: base.get(t, 0.0) for t in topics if not is_question(t)}
    kp_w = plan_kp.weights(pts, q_freq, direct, spread)
    vals = plan_kp.card_values(pts, kp_w)
    for cs in by_topic.values():
        graded = [c for c in cs if pts.card.get(c.id)]
        if not graded:
            continue
        mean = sum(vals[c.id] for c in graded) / len(graded) or 1.0
        for c in cs:
            if pts.card.get(c.id):
                c.freq, c.graded, c.point = max(0.3, min(3.0, vals[c.id] / mean)), True, pts.card[c.id][0]
            elif c.id in pts.card:  # an intro or navigation card teaches no point
                c.freq, c.graded = 0.3, True
    # interview-process points stay visible on the map but count for nothing
    model = PointModel({k: v for k, v in kp_w.items() if k not in plan_kp.META}, pts.card)
    kp_state.update(points=pts, weight=kp_w, teach=teach, model=model, q_freq=q_freq)


def question_topic(tree: Tree, t: str) -> bool:
    top = tree.top(t)
    return top in ("s05", "s08") or (top == "s07" and t not in LLD_FOUNDATIONS)


UNIVERSAL = {"t.sd-delivery", "t.numbers", "t.lld-delivery"}  # every question uses these; they say nothing about which to practise


NOT_A_QUESTION = {"q.in-the-wild"}  # a collection of real-system case studies, not one question


def representatives(tree: Tree, qs: dict[str, float], pool: list[str], k: int) -> tuple[list[dict], dict]:
    """The few questions whose answers between them use the most exam-point weight, and what they really cover.

    Measured on points shared by several questions (a question's own tricks transfer to nothing else). `covered` is the
    share of all shared-point weight that the chosen questions' answers use in any role; `must` counts only points they
    must cover. Picked greedily from the `pool` most-asked questions by the weight each adds times how often it is asked:
    weight alone favours whichever answer was annotated with the most points. Using a point in one answer does not teach
    the topic around it."""
    pts, w = kp_state["points"], kp_state["weight"]
    shared = {p: v for p, v in w.items() if pts.meta[p]["topic"] not in pts.needs and p not in plan_kp.META}
    total = sum(shared.values()) or 1.0

    def needs(q, roles=("必讲", "追问", "加分")):
        return {n["kp"] for n in pts.needs.get(q, []) if n["role"] in roles and n["kp"] in shared}

    def share(points):
        return sum(shared[p] for p in points) / total

    reps, seen, must = [], set(), set()
    for _ in range(min(k, len(pool))):
        best = max((q for q in pool if q not in {r["id"] for r in reps}), key=lambda q: share(needs(q) - seen) * qs[q])
        seen |= needs(best)
        must |= needs(best, ("必讲",))
        top = sorted(needs(best), key=lambda p: -shared[p])[:5]
        reps.append({"id": best, "title": tree.title(best), "freq": qs[best] / (sum(qs.values()) or 1.0), "covered": share(seen), "must": share(must),
                     "points": len(seen), "concepts": [pts.meta[p]["title"] for p in top]})
    every = [q for q in qs if q in pts.needs and q not in NOT_A_QUESTION]
    curve, cur = [], set()
    remaining = list(pool)
    for n in range(1, len(pool) + 1):
        best = max(remaining, key=lambda q: share(needs(q) - cur) * qs[q])
        remaining.remove(best)
        cur |= needs(best)
        if n in (5, 8, 10, 15, 20, 25):
            curve.append({"k": n, "covered": share(cur)})
    return reps, {"curve": curve, "all": share(set().union(*(needs(q) for q in every))), "shared": len(shared), "questions": len(every)}


def generality(tree: Tree, base: dict[str, float], edges: list[Edge], k: int = 8, pool: int = 25) -> dict:
    """How much of the answers' knowledge sits in shared concepts, and which few questions practise most of it.

    A question's answer leans on its concepts in proportion to edge strength; a concept's share is that, summed over
    questions weighted by how often each is asked. A question is ready once the learned concepts carry 80% of its edges.
    Representatives are chosen by the exam points their answers use: see representatives()."""
    qs = {t: w for t, w in base.items() if question_topic(tree, t) and w > 0}
    total = sum(qs.values()) or 1.0
    out: dict[str, dict[str, float]] = defaultdict(dict)
    for e in edges:
        if e.src in qs and not question_topic(tree, e.dst):
            out[e.src][e.dst] = out[e.src].get(e.dst, 0.0) + e.strength
    share = defaultdict(float)
    for q, w in qs.items():
        s = sum(out[q].values())
        for c, v in out[q].items():
            share[c] += w / total * v / s
    order = sorted(share, key=lambda c: -share[c])
    acc, n80 = 0.0, len(order)
    for i, c in enumerate(order):
        acc += share[c]
        if acc >= 0.8:
            n80 = i + 1
            break
    curve = []
    for n in (5, 10, 15, 20, 25, 30, 40):
        learned = set(order[:n])
        ready = sum(w for q, w in qs.items() if out[q] and sum(v for c, v in out[q].items() if c in learned) >= 0.8 * sum(out[q].values()))
        curve.append({"k": n, "ready": ready / total, "share": sum(share[c] for c in order[:n])})
    pool_qs = [q for q in sorted(qs, key=lambda q: -qs[q]) if tree.top(q) in ("s05", "s08") and q not in NOT_A_QUESTION][:pool]
    reps, coverage = representatives(tree, qs, pool_qs, k)
    return {"concepts": [{"id": c, "title": tree.title(c), "share": share[c]} for c in order], "n80": n80,
            "curve": curve, "representatives": reps, "coverage": coverage, "questions": len(qs)}


def topic_boost(tree: Tree, topics: set[str], boost: dict[str, float]) -> dict[str, float]:
    """A boost may name a topic or a whole group (a top-level id such as s06); a topic gets the product of both."""
    return {t: boost.get(t, 1.0) * (boost.get(tree.top(t), 1.0) if tree.top(t) != t else 1.0) for t in topics}


# ---------------------------------------------------------------- Anki state


def anki_state(ids: set[str]):
    q = f'"deck:系统设计" OR "deck:{DECK}" OR "deck:{OLD_DECK}"'
    cids = call("findCards", query=q)
    info = []
    for i in range(0, len(cids), 500):
        info += call("cardsInfo", cards=cids[i:i + 500])
    nids = sorted({c["note"] for c in info})
    tag_of = {}
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            tag_of[n["noteId"]] = n["tags"]
    reviewed = [c["cardId"] for c in info if c["reps"]]
    revs = call("getReviewsOfCards", cards=reviewed) if reviewed else {}
    traces, anki, logs = {}, {}, {}
    for c in info:
        tags = tag_of.get(c["note"], [])
        ident = next((t[4:] for t in tags if t.startswith("id::")), None)
        if REPORT_TAG in tags or ident not in ids:
            continue
        log = revs.get(str(c["cardId"]), [])
        logs[ident] = log
        traces[ident] = Trace(card_id=ident, reps=c["reps"], lapses=c["lapses"], interval=max(c["interval"], 0),
                              ease=c.get("factor", 0) / 1000, type=c["type"], due=c["due"],
                              last_review=max((r["id"] for r in log), default=0))
        anki[ident] = c
    return traces, anki, logs


# ---------------------------------------------------------------- report


def activity(logs: dict, now_ms: int, days: int) -> dict:
    since = now_ms - days * DAY_MS
    rows = [(cid, r) for cid, log in logs.items() for r in log if r["id"] >= since]
    first = {cid: min(r["id"] for r in log) for cid, log in logs.items() if log}
    return {"reviews": len(rows), "again": sum(1 for _, r in rows if r["ease"] == 1),
            "new": sum(1 for cid, t in first.items() if t >= since), "minutes": round(sum(r.get("time", 0) for _, r in rows) / 60000),
            "again_cards": sorted({cid for cid, r in rows if r["ease"] == 1})}


def streak(logs: dict, now: datetime) -> int:
    days = {datetime.fromtimestamp((r["id"] - 4 * 3_600_000) / 1000).date() for log in logs.values() for r in log}
    d, n = (now - timedelta(hours=4)).date(), 0
    if d not in days:
        d -= timedelta(days=1)
    while d in days:
        n += 1
        d -= timedelta(days=1)
    return n


def svg_bars(rows: list[tuple[str, float, float]], width=340) -> str:
    """One bar per group: dark = held (weight-averaged mastery), light = seen."""
    h = 22 * len(rows) + 8
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" style="width:100%">']
    for i, (label, held, seen) in enumerate(rows):
        y = 4 + i * 22
        out.append(f'<text x="0" y="{y + 13}" font-size="11" fill="currentColor">{html.escape(label[:9])}</text>')
        x0, w = 118, width - 160
        out.append(f'<rect x="{x0}" y="{y + 3}" width="{w}" height="12" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>')
        out.append(f'<rect x="{x0}" y="{y + 3}" width="{w * seen:.1f}" height="12" rx="3" style="fill:var(--accent,#3b6fd4);opacity:.35"/>')
        out.append(f'<rect x="{x0}" y="{y + 3}" width="{w * held:.1f}" height="12" rx="3" style="fill:var(--accent,#3b6fd4)"/>')
        out.append(f'<text x="{width - 2}" y="{y + 13}" font-size="11" text-anchor="end" fill="currentColor">{held * 100:.0f}%</text>')
    out.append("</svg>")
    return "".join(out)


def svg_pareto(curve, held, width=340, height=150) -> str:
    pad = 26
    pts = [(0, 0)] + curve
    path = " ".join(f"{pad + x * (width - pad - 6):.1f},{height - pad - y * (height - pad - 6):.1f}" for x, y in pts)
    x80 = next((x for x, y in curve if y >= 0.8), 1.0)
    gx = pad + x80 * (width - pad - 6)
    gy = height - pad - 0.8 * (height - pad - 6)
    hy = height - pad - held * (height - pad - 6)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" style="width:100%">'
            f'<polyline points="{path}" fill="none" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>'
            f'<line x1="{pad}" y1="{gy:.1f}" x2="{gx:.1f}" y2="{gy:.1f}" stroke-dasharray="3 3" stroke="currentColor" opacity=".5"/>'
            f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="{gx:.1f}" y2="{height - pad}" stroke-dasharray="3 3" stroke="currentColor" opacity=".5"/>'
            f'<line x1="{pad}" y1="{hy:.1f}" x2="{width - 6}" y2="{hy:.1f}" stroke-width="1.5" style="stroke:#e0a030"/>'
            f'<text x="{gx + 4:.1f}" y="{gy - 4:.1f}" font-size="10" fill="currentColor">{x80 * 100:.0f}% 的卡覆盖 80% 权重</text>'
            f'<text x="{width - 8}" y="{hy - 4:.1f}" font-size="10" text-anchor="end" style="fill:#e0a030">已掌握 {held * 100:.0f}%</text>'
            f'<text x="{pad}" y="{height - 8}" font-size="10" fill="currentColor">卡片（按重要度排序）→</text></svg>')


def reasons(tree: Tree, s, edges_in, edges_out, rank) -> str:
    out = [f"权重第 {rank}"]
    if edges_in:
        out.append(f"{len(edges_in)} 道题依赖它")
    if s.readiness < 0.8 and edges_out:
        out.append("先修未稳")
    out.append(f"掌握 {s.mastery * 100:.0f}%")
    return " · ".join(out)


def render_report(tree, p, cards, titles, base, edges, traces, logs, picks_by_stage, now) -> tuple[str, str, dict]:
    now_ms = int(now.timestamp() * 1000)
    a1, a7 = activity(logs, now_ms, 1), activity(logs, now_ms, 7)
    st = streak(logs, now)
    by_top = defaultdict(list)
    for t, s in p.topics.items():
        by_top[tree.top(t)].append(s)
    bars = []
    for top in tree.sk.roots:
        ss = by_top.get(top.id, [])
        w = sum(s.weight for s in ss) or 1e-9
        held = sum(s.weight * s.mastery for s in ss) / w
        seen = sum(s.seen for s in ss) / max(1, sum(s.cards for s in ss))
        bars.append((re.sub(r"[（(].*", "", top.title), held, seen))
    ranked = sorted(p.topics.values(), key=lambda s: -s.weight)
    rank = {s.topic: i + 1 for i, s in enumerate(ranked)}
    ins, outs = defaultdict(list), defaultdict(list)
    for e in edges:
        ins[e.dst].append(e.src)
        outs[e.src].append(e.dst)
    nxt = sorted(p.topics.values(), key=lambda s: -s.value)[:6]
    weak_cards = [c for c in a7["again_cards"]][:8]
    # weak = what the reviews say, not what is still unseen: a topic's forget rate over the last 14 days
    since = now_ms - 14 * DAY_MS
    rev_by_topic = defaultdict(lambda: [0, 0])
    topic_of = {c.id: c.topic for c in cards}
    for cid, log in logs.items():
        for r in log:
            if r["id"] >= since and cid in topic_of:
                rev_by_topic[topic_of[cid]][0] += 1
                rev_by_topic[topic_of[cid]][1] += r["ease"] == 1
    weak_topics = sorted(((t, n, a) for t, (n, a) in rev_by_topic.items() if n >= 3 and a / n >= 0.15),
                         key=lambda x: -x[2] / x[1])[:5]
    seen_all = sum(1 for t in traces.values() if t.reps)
    stage_counts = {k: len(v) for k, v in picks_by_stage.items()}
    due = len(call("findCards", query=f'("deck:系统设计" OR "deck:{DECK}") is:due')) if picks_by_stage is not None else 0

    head = (f"<b>今日计划 · {now:%m-%d}</b><br>考点覆盖 <b>{p.held * 100:.1f}%</b> · 已见 {seen_all}/{len(cards)} 张"
            f" · 连续 {st} 天")
    body = [f"<p><b>昨天：</b>复习 {a1['reviews']} 次，新学 {a1['new']} 张，按「忘记」{a1['again']} 次，约 {a1['minutes']} 分钟。"
            f"近 7 天复习 {a7['reviews']} 次，忘记率 {a7['again'] / max(1, a7['reviews']) * 100:.0f}%。</p>",
            f"<p><b>今天：</b>到期复习约 {due} 张；新卡每天 {cfg_global.get('daily_new', 35)} 张，计划里备了两天的量："
            + "、".join(f"{k[2:]} {v}" for k, v in sorted(stage_counts.items())) + "，按这个顺序发。</p>",
            "<p><b>各部分掌握度</b>（深色已掌握，浅色已见过）</p>", svg_bars(bars),
            "<p><b>二八曲线</b>：按重要度排卡片，前多少张卡覆盖多少面试权重</p>", svg_pareto(p.pareto, p.held),
            "<p><b>现在最值得学的主题</b></p><ul>"]
    for s in nxt:
        body.append(f"<li><b>{html.escape(tree.title(s.topic))}</b>：{reasons(tree, s, ins[s.topic], outs[s.topic], rank[s.topic])}</li>")
    body.append("</ul>")
    body.append("<p><b>薄弱</b></p><ul>")
    for cid in weak_cards:
        body.append(f"<li>最近忘过：{html.escape(titles.get(cid, cid))}</li>")
    for t, n, a in weak_topics:
        body.append(f"<li>忘记率偏高：{html.escape(tree.title(t))}（近 14 天 {a}/{n}）</li>")
    if not weak_cards and not weak_topics:
        body.append("<li>近 7 天没有按过「忘记」。</li>")
    if a7["reviews"] >= 100 and a7["again"] / a7["reviews"] < 0.03:
        body.append("<li>复习了很多次却几乎不忘，更可能是在认答案而不是在回忆：先出声说出答案再翻面，说不完整就按「忘记」。</li>")
    body.append("</ul>")
    summary = {"date": now.strftime("%Y-%m-%d"), "held": round(p.held, 4), "seen": seen_all, "cards": len(cards),
               "reviews_1d": a1["reviews"], "again_1d": a1["again"], "new_1d": a1["new"], "minutes_1d": a1["minutes"],
               "streak": st, "picked": sum(stage_counts.values())}
    # the same facts, structured, for the dashboard
    first = [i for k in sorted(picks_by_stage) for i in picks_by_stage[k]][:1]
    lead_topic = next((c.topic for c in cards if first and c.id == first[0]), nxt[0].topic if nxt else None)
    lead = p.topics.get(lead_topic)
    brief.clear()
    brief.update({
        "lead": {"id": lead.topic, "title": tree.title(lead.topic), "rank": rank[lead.topic], "users": len(set(ins[lead.topic])),
                 "mastery": lead.mastery, "boosted": tree.top(lead.topic) == "s00"} if lead else None,
        "next": [{"id": s.topic, "title": tree.title(s.topic), "group": re.sub(r"[（(].*", "", tree.title(tree.top(s.topic))),
                  "rank": rank[s.topic], "users": len(set(ins[s.topic])), "mastery": s.mastery, "readiness": s.readiness,
                  "boosted": tree.top(s.topic) == "s00"} for s in nxt],
        "stages": {k[2:]: v for k, v in sorted(stage_counts.items())},
        "weak": [{"kind": "forgot", "title": titles.get(cid, cid)} for cid in weak_cards]
                + [{"kind": "rate", "title": tree.title(t), "n": n, "a": a} for t, n, a in weak_topics],
        "recognising": a7["reviews"] >= 100 and a7["again"] / max(1, a7["reviews"]) < 0.03,
        "yesterday": a1, "week": {k: a7[k] for k in ("reviews", "again", "new", "minutes")}, "streak": st, "due": due,
        "daily_new": cfg_global.get("daily_new", 35),
    })
    return head, "".join(body), summary


brief: dict = {}


# ---------------------------------------------------------------- dashboard


def per_day(logs: dict, days: int = 30) -> list[dict]:
    """Reviews, forgets and new cards per study day (a day starts at 4 am, as in Anki), straight from the review log."""
    rows = defaultdict(lambda: {"reviews": 0, "again": 0, "new": 0})
    for log in logs.values():
        for i, r in enumerate(sorted(log, key=lambda r: r["id"])):
            d = datetime.fromtimestamp((r["id"] - 4 * 3_600_000) / 1000).strftime("%Y-%m-%d")
            rows[d]["reviews"] += 1
            rows[d]["again"] += r["ease"] == 1
            rows[d]["new"] += i == 0
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return [{"date": d, **v} for d, v in sorted(rows.items()) if d >= start]


daily_activity: list[dict] = []


def dashboard(tree, p, cards, titles, edges, history, gen=None) -> str:
    ev = load_evidence() or {}
    ev_q = {k: {"freq": v["freq"], "reports": v["reports"], "bytedance": v["bytedance"], "last": v["last"]}
            for k, v in ev.get("questions", {}).items()}
    for k, v in ev.get("concepts", {}).items():
        ev_q.setdefault(k, {})["named"] = v
    leaves = defaultdict(list)
    for c in cards:
        leaves[c.topic].append(c)
    topics = []
    for t, s in p.topics.items():
        ls = defaultdict(list)
        for c in leaves[t]:
            ls[c.leaf].append(c)
        topics.append({
            "id": t, "title": tree.title(t), "top": tree.top(t), "topTitle": tree.title(tree.top(t)),
            "weight": s.weight, "mastery": s.mastery, "progress": s.progress, "readiness": s.readiness, "value": s.value,
            "cards": s.cards, "seen": s.seen,
            "leaves": [{"id": l, "title": tree.title(l), "cards": len(cs),
                        "mastery": sum(p.card_mastery[c.id] for c in cs) / len(cs),
                        "value": sum(p.card_value[c.id] for c in cs),
                        "freq": sum(c.freq for c in cs) / len(cs), "difficulty": sum(c.difficulty for c in cs) / len(cs)}
                       for l, cs in ls.items()],
            "evidence": (ev_q.get(t) or {}),
        })
    data = {"topics": topics, "edges": [{"src": e.src, "dst": e.dst, "s": e.strength, "kind": e.kind} for e in edges],
            "pareto": p.pareto, "held": p.held, "generality": gen, "points": exam_point_rows(tree, p), "metrics": coverage_metrics(tree, p, gen, cfg_global), "history": history, "activity": daily_activity, "brief": brief,
            "picked": [{"id": cid, "title": titles.get(cid, cid)} for cid in p.picked],
            "pickedTopics": sorted({c.topic for c in cards if c.id in set(p.picked)}),
            "method": {"coverage": ev.get("coverage"), "bank_reports": ev.get("method", {}).get("bank_reports"),
                       "external_reports": ev.get("method", {}).get("external_reports"), "agreement": ev.get("method", {}).get("agreement")}}
    tpl = (ROOT / "scripts/study_plan.html").read_text(encoding="utf-8")
    return tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))


# ---------------------------------------------------------------- Anki deck


def built_decks() -> dict[str, str]:
    folder = Path(tempfile.mkdtemp(prefix="plan-build-"))
    apkg = folder / "s.apkg"
    r = subprocess.run(["uv", "run", "trellis", "--domain", DOMAIN, "build", "-o", str(apkg)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-400:])
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", folder)
    db = sqlite3.connect(folder / "collection.anki2")
    decks = {int(k): v["name"] for k, v in json.loads(db.execute("select decks from col").fetchone()[0]).items()}
    deck_of = dict(db.execute("select nid, did from cards"))
    out = {}
    for nid, tags in db.execute("select id, tags from notes"):
        ident = next((t[4:] for t in tags.split() if t.startswith("id::")), None)
        out[ident] = decks[deck_of[nid]]
    db.close()
    shutil.rmtree(folder, ignore_errors=True)
    return out


def release(p, anki) -> None:
    """Studied cards go back to their own deck, tagged; unstudied ones the plan no longer wants go back too."""
    home = built_decks()
    want = set(p.picked)
    back, done_notes = defaultdict(list), []
    for i, c in anki.items():
        if not c["deckName"].startswith((DECK, OLD_DECK)):
            continue
        if c["reps"]:
            back[home[i]].append(c["cardId"])
            done_notes.append(c["note"])
        elif i not in want:
            back[home[i]].append(c["cardId"])
    if done_notes:
        call("addTags", notes=done_notes, tags=DONE_TAG)
    for deck, ids in back.items():
        call("changeDeck", cards=ids, deck=deck)


anki_leaf: dict[str, str] = {}


def deal(picked_stage: dict[str, list[str]], anki):
    for stage, ids in picked_stage.items():
        cids = [anki[i]["cardId"] for i in ids if i in anki]
        if cids:
            call("changeDeck", cards=cids, deck=f"{DECK}::{stage}")


def report_card(head: str, body: str):
    found = call("findNotes", query=f'"tag:{REPORT_TAG}"')
    deck = f"{DECK}::0 今日报告"
    fields = {"Question": head, "Answer": body, "Crumb": "今日计划"}
    if found:
        nid = found[0]
        call("updateNoteFields", note={"id": nid, "fields": fields})
        cards = call("findCards", query=f'"tag:{REPORT_TAG}"')
        call("changeDeck", cards=cards, deck=deck)
        call("forgetCards", cards=cards)
    else:
        call("createDeck", deck=deck)
        call("addNote", note={"deckName": deck, "modelName": "Trellis QA", "fields": fields, "tags": [REPORT_TAG],
                              "options": {"allowDuplicate": True}})


def preset(cfg):
    names = [d for d in call("deckNames") if d == DECK or d.startswith(DECK + "::")]
    current = call("getDeckConfig", deck=DECK)
    if current["name"] != DECK:
        cid = call("cloneDeckConfigId", name=DECK, cloneFrom=call("getDeckConfig", deck="系统设计")["id"])
        call("setDeckConfigId", decks=names, configId=cid)
        current = call("getDeckConfig", deck=DECK)
    else:
        call("setDeckConfigId", decks=names, configId=current["id"])
    # system design + LeetCode new + similar + just solved + the report card
    current["new"]["perDay"] = int(cfg.get("daily_new", 35)) + int(cfg.get("lc_new", 8)) + int(cfg.get("similar_max", 10)) + int(cfg.get("solved_max", 10)) + 1
    current["rev"]["perDay"] = 9999
    current["newGatherPriority"] = 0  # deck order: report, weak spots, concepts, questions
    current["newSortOrder"] = 0
    call("saveDeckConfig", config=current)


def points_report(p, cards) -> str:
    """The exam points today's new cards teach, heaviest first, with how interviews use them."""
    if not kp_state:
        return ""
    pts, w = kp_state["points"], kp_state["weight"]
    req = plan_kp.required_by(pts)
    picked = set(p.picked)
    points = sorted({c.point for c in cards if c.id in picked and c.point and c.point in w and c.point not in plan_kp.META}, key=lambda k: -w[k])
    if not points:
        return ""
    out = ["<p><b>今天学的考点</b></p><ul>"]
    for k in points[:8]:
        n = Counter(r[1] for r in req.get(k, []))
        how = "，".join(f"{v} 题{role}" for role, v in n.most_common(2))
        out.append(f"<li>{html.escape(pts.meta[k]['title'])}{'（' + how + '）' if how else ''}</li>")
    out.append("</ul>")
    return "".join(out)


def extra_report(ex) -> str:
    out = ["<p><b>算法</b></p><ul>"]
    for x in ex.lc_similar:
        out.append(f"<li>相似题：{html.escape(x['title'])}（{html.escape(x['why'])}）</li>")
    if ex.lc_new:
        out.append(f"<li>新题 {len(ex.lc_new)} 道：" + "、".join(html.escape(x["title"]) for x in ex.lc_new[:4])
                   + ("等" if len(ex.lc_new) > 4 else "") + "</li>")
    out.append("</ul><p><b>到期复习</b></p><ul>")
    out.append(f"<li>今天拿进来 {len(ex.reviews)} 张：" + "，".join(f"{k} {v}" for k, v in ex.by_deck.items()) + "。</li>")
    if ex.backlog:
        out.append(f"<li>还有 {ex.backlog} 张价值较低的到期卡留在原牌组排队，不用管，计划会按价值一批批拿进来。</li>")
    out.append("</ul>")
    return "".join(out)


OWNED = ("系统设计", "LeetCode Tops")  # new cards in these decks come only through the plan


def exclusive_presets(cfg) -> None:
    """The plan deals every new card of the decks it owns, so their own presets deal none. Originals are kept once in
    sources/local/plan/preset_backup.json; restore by copying perDay back."""
    backup_file = OUT / "preset_backup.json"
    backup = json.loads(backup_file.read_text(encoding="utf-8")) if backup_file.exists() else {}
    for deck in cfg.get("owned_decks", OWNED):
        conf = call("getDeckConfig", deck=deck)
        if conf["name"] == DECK:
            continue
        backup.setdefault(conf["name"], {"deck": deck, "new_per_day": conf["new"]["perDay"]})
        if conf["new"]["perDay"]:
            conf["new"]["perDay"] = 0
            call("saveDeckConfig", config=conf)
    backup_file.write_text(json.dumps(backup, ensure_ascii=False, indent=1), encoding="utf-8")


def drop_old_deck():
    names = sorted((d for d in call("deckNames") if d == OLD_DECK or d.startswith(OLD_DECK + "::")), key=len, reverse=True)
    empty = [d for d in names if not call("findCards", query=f'"deck:{d}"')]
    if empty and len(empty) == len(names):
        call("deleteDecks", decks=empty, cardsToo=True)


# ---------------------------------------------------------------- main


def run(apply_to_anki: bool) -> None:
    cfg = config()
    cfg_global.update(cfg)
    now = datetime.now()
    now_ms = int(now.timestamp() * 1000)
    tree = Tree()
    cards, titles, base, edges = build_inputs(tree)
    for c in cards:
        anki_leaf[c.id] = c.leaf
    if apply_to_anki:
        call("sync")
    traces, anki, logs = anki_state({c.id for c in cards})
    for c in cards:  # once studied, the learner's own record says how hard a card is
        t, log = traces.get(c.id), logs.get(c.id, [])
        if t and t.reps >= 2:
            hard = sum(1 for r in log if r["ease"] == 2)
            personal = min(1.0, (t.lapses + sum(1 for r in log if r["ease"] == 1) * 0.5 + hard * 0.3) / t.reps * 2)
            personal = min(1.0, personal + (0.2 if t.ease and t.ease < 2.3 else 0.0))
            c.difficulty = 0.5 * c.difficulty + 0.5 * personal
    budget = int(cfg.get("daily_new", 35)) * int(cfg.get("buffer_days", 2))
    boosts = topic_boost(tree, {c.topic for c in cards}, cfg.get("boost", {}))
    share = float(cfg.get("question_share", 0.2))
    spread = float(cfg.get("spread", 0.5))
    gen = generality(tree, base, edges, int(cfg.get("representatives", 8)))
    reps = {r["id"] for r in gen["representatives"]}
    model = kp_state.get("model")
    # shared knowledge takes the main budget; whole questions only get their own reserved share, from the representatives
    only_questions = {c.id for c in cards if question_topic(tree, c.topic)}
    p = plan(cards, traces, base, edges, boosts, now_ms, budget - int(budget * share), exclude=only_questions, spread=spread, points=model)
    question_cards = [c for c in cards if STAGES.get(tree.top(c.leaf)) == "3 题目与整轮"]
    # whole questions are practised on a few representatives that between them exercise most shared concepts
    question_cards = [c for c in question_cards if c.topic in reps] or question_cards
    already = {i for i in p.picked if STAGES.get(tree.top(anki_leaf[i])) == "3 题目与整轮"}
    q_plan = plan(question_cards, traces, {t: base.get(t, 0) for t in {c.topic for c in question_cards}}, edges, boosts, now_ms,
                  int(budget * share), exclude=set(p.picked), spread=spread, points=model)
    p.picked += [i for i in q_plan.picked if i not in already][: budget - len(p.picked)]
    stages = defaultdict(list)
    for i in p.picked:
        stages[STAGES.get(tree.top(anki_leaf[i]), STAGE_DEFAULT)].append(i)
    if kp_state:  # what Anki deals today: the stages in deck order, up to the daily limit
        kp_state["today"] = [i for _, ids in sorted(stages.items()) for i in ids][:int(cfg.get("daily_new", 35))]
    daily_activity[:] = per_day(logs)
    head, body, summary = render_report(tree, p, cards, titles, base, edges, traces, logs, stages, now)
    # beyond system design: LeetCode practice and the review queue of every deck
    if model:
        sd_value = {c.id: model.card_value(c.id) for c in cards}
    else:
        tw = {t: s.weight for t, s in p.topics.items()}
        topic_sum = defaultdict(float)
        for c in cards:
            topic_sum[c.topic] += c.weight
        sd_value = {c.id: tw.get(c.topic, 0.0) * c.weight / (topic_sum[c.topic] or 1.0) for c in cards}
    if apply_to_anki:  # today's LeetCode analysis: mastery, slips and similar problems read from fresh numbers
        import lc_analysis
        lc_analysis.main()
    extra = daily_extra.prepare(cfg, sd_value)
    body += points_report(p, cards) + extra_report(extra)
    summary["extra"] = {"lc_new": len(extra.lc_new), "lc_similar": len(extra.lc_similar), "reviews": len(extra.reviews),
                        "backlog": extra.backlog}
    OUT.mkdir(parents=True, exist_ok=True)
    hist_file = OUT / "history.jsonl"
    history = [json.loads(x) for x in hist_file.read_text().splitlines()] if hist_file.exists() else []
    history = [h for h in history if h["date"] != summary["date"]] + [summary]
    hist_file.write_text("".join(json.dumps(h, ensure_ascii=False) + "\n" for h in history), encoding="utf-8")
    state = {"date": summary["date"], "held": p.held, "picked": p.picked,
             "topics": {t: vars(s) for t, s in p.topics.items()}}
    (OUT / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    style = '<style>body{font-family:-apple-system,sans-serif;background:#111;color:#ddd;max-width:420px;margin:auto;padding:12px}</style>'
    (OUT / "report.html").write_text(f"<meta charset='utf-8'>{style}<p>{head}</p><hr>{body}", encoding="utf-8")
    (OUT / "index.html").write_text(dashboard(tree, p, cards, titles, edges, history, gen), encoding="utf-8")
    print(f"held {p.held * 100:.1f}% · seen {summary['seen']}/{len(cards)} · picked {len(p.picked)} "
          f"({', '.join(f'{k} {len(v)}' for k, v in sorted(stages.items()))}) · topics {len(p.topics)} · edges {len(edges)}")
    print(f"LeetCode {len(extra.lc_new)} new + {len(extra.lc_similar)} similar · reviews {len(extra.reviews)} taken, "
          f"{extra.backlog} waiting · {extra.by_deck}")
    if apply_to_anki:
        release(p, anki)
        deal(stages, anki)
        daily_extra.release(daily_extra.keep_ids(extra))
        daily_extra.deal(extra)
        exclusive_presets(cfg)
        report_card(head, body)
        preset(cfg)
        drop_old_deck()
        call("sync")
        print("Anki: 今日计划 rebuilt")


def serve(host: str, minutes: int) -> None:
    import functools
    import http.server
    import threading
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    srv = http.server.ThreadingHTTPServer((host, 8798), handler)
    threading.Timer(minutes * 60, srv.shutdown).start()
    print(f"http://{host}:8798/index.html for {minutes} minutes")
    srv.serve_forever()


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "serve":
        args = sys.argv[2:]
        host = args[args.index("--host") + 1]
        minutes = int(args[args.index("--minutes") + 1]) if "--minutes" in args else 30
        serve(host, minutes)
        return 0
    run(apply_to_anki=cmd == "daily")
    return 0


if __name__ == "__main__":
    sys.exit(main())
