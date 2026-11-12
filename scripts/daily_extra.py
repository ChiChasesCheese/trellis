"""The parts of the daily plan beyond system design: LeetCode practice and the review queue of every deck.

study_plan.py calls this; on its own it prints what it would do:

    uv run python scripts/daily_extra.py            # dry run

LeetCode (its own daily deck 今日算法): `lc_new` problems a day, each by its whole answer, from two lists of the knowledge
tree at a time.
- **The tree** is 0x3F's problem lists as deep as his posts go (scripts/lc_tree.py), in his order.
- **A round** takes `lc.per_section` more problems from every leaf, most asked first. Two lists are in focus,
  `lc.per_topic` problems each a day; when one has nothing left this round, the next list takes its place.
- **Done** means answered since `lc.since`. A problem seen before counts as new: if it is not due, it is made due today
  (Anki's own Set Due Date). One left unanswered comes back the next day, as it is still first in its section.
- The LeetCode review backlog is not dealt.

Low-level design has its own daily deck too (今日低层设计), `lld_new` cards a day plus its reviews.

Reviews (stage `9 到期复习` of each subject): every due card in every deck, ranked by
    deck weight x (0.3 + value) x urgency,   urgency = 1 + min(2, days overdue / interval)
where value is the percentile, inside its deck, of the card's planner value (system design) or its problem's importance
(LeetCode); cards with no value measure sit at 0.5. The
first `review_budget` come into the plan; one card per LeetCode problem. The rest wait in their decks.

Every card moved into a daily deck is recorded with its home deck in sources/local/plan/homes.json and goes back there at the
next run unless it is picked again.
"""
from __future__ import annotations

import functools
import json
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lc_data import call  # noqa: E402

OUT = ROOT / "sources/local/plan"
HOMES = OUT / "homes.json"
DECK = "今日计划"
LC_DECK, LLD_DECK = "今日算法", "今日低层设计"  # LeetCode and low-level design each have a daily deck of their own (Chi 2026-11-11)
DAILY = (DECK, LC_DECK, LLD_DECK)
CARRIED = "0 昨天没学完"  # what was dealt and not learned comes first the next day
LLD_ROOT, SD_ROOT = "低层设计（LLD）", "系统设计"
SUBJECT_DECK = {SD_ROOT: f"{DECK}::1 系统设计", LLD_ROOT: LLD_DECK, "LeetCode Tops": LC_DECK}  # each subject: its deck and budget
REVIEWS = {SD_ROOT: 150, LLD_ROOT: 80, "LeetCode Tops": 0}  # LeetCode: new problems only, its backlog is left alone
LLD_FOUNDATIONS = ("低层设计答题框架", "并发", "低层设计跨题模式")
DAY_MS = 86_400_000
URGENCY_CAP = 2.0  # how far overdue-ness can raise a review: urgency is 1 + min(cap, days overdue / interval)
VALUE_FLOOR = 0.3  # a review of the least valuable card in a deck still counts this much
TREE_ROOT = "算法知识树（灵神题单）"  # the knowledge tree's own deck: a learning card per leaf, then its problems
LC_ROOTS = ("LeetCode Tops", TREE_ROOT)
SOLVED_DECK = "LeetCode Tops::28 Daily"
LC_DEFAULTS = {"since": "2026-11-12T04:00", "per_topic": 5, "per_section": 1}
PREFER = ("lct-{s}", "tlc-tops-{s}-0-whole", "tlc-{s}-0-whole", "tlc-core-{s}", "lca-{s}", "tlc-daily-{s}-0-whole")
DEFAULT_DECKS = {"系统设计": 1.0, "LeetCode Tops": 1.0, "低层设计（LLD）": 0.6, "Kafka": 0.5, "Python": 0.5,
                 "Code Core": 0.5, "Narrative Round": 0.4, "编程语言原理：Go · Java · Rust · Python · C++": 0.3,
                 "Snowflake 原理": 0.3, "HFT 低延迟交易系统": 0.2, "CDN Content": 0.2, "Stripe": 0.2, "篮球（Basketball）": 0.2,
                 "Headlands": 0.1, "Markets & Factors": 0.1, "Quant Infrastructure": 0.1}


def in_daily(deck: str) -> bool:
    return any(deck == d or deck.startswith(d + "::") for d in DAILY)


def daily_query() -> str:
    return "(" + " OR ".join(f'"deck:{d}"' for d in DAILY) + ")"


@dataclass
class Extra:
    lc_new: list[dict] = field(default_factory=list)       # {card, slug, title, why}
    lc_similar: list[dict] = field(default_factory=list)   # {card, slug, title, why, due_now}: no longer dealt
    lc_focus: list[str] = field(default_factory=list)      # the topics today's problems come from
    lld_new: list[dict] = field(default_factory=list)      # {card, title, carried}
    work_new: list[dict] = field(default_factory=list)     # {card, part, carried}: a private work deck, configured locally
    reviews: list[dict] = field(default_factory=list)      # {card, home, score}
    backlog: int = 0                                       # due cards left in their decks
    by_deck: dict = field(default_factory=dict)            # root deck -> reviews taken


def _cards(query: str) -> list[dict]:
    cids = call("findCards", query=query)
    out = []
    for i in range(0, len(cids), 500):
        out += [c for c in call("cardsInfo", cards=cids[i:i + 500]) if c.get("note")]  # a card deleted meanwhile comes back empty
    return out


def _idents(cards: list[dict]) -> dict[int, str]:
    nids = sorted({c["note"] for c in cards})
    by_note = {}
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            by_note[n["noteId"]] = next((t[4:] for t in n["tags"] if t.startswith("id::")), "")
    return {c["cardId"]: by_note.get(c["note"], "") for c in cards}


def anki_today() -> int:
    """Today as Anki counts review due dates (days since the collection was created), read off a card due near today."""
    for k in [0] + [d for i in range(1, 60) for d in (-i, i)]:
        found = call("findCards", query=f"prop:due={k} is:review")
        if found:
            return call("cardsInfo", cards=found[:1])[0]["due"] - k
    raise RuntimeError("no review card due within 60 days of today")


def homes() -> dict[str, str]:
    return json.loads(HOMES.read_text(encoding="utf-8")) if HOMES.exists() else {}


def lld_rank(c: dict) -> tuple:
    """Low-level design, foundations first: method and principles, then the concurrency and cross-problem material, then problems."""
    parts = c["deckName"].split("::")
    top = parts[1] if len(parts) > 1 else ""
    n = int(top[:2]) if top[:2].isdigit() else 99
    group = 0 if n <= 8 else 1 if n == 11 and len(parts) > 2 and parts[2] in LLD_FOUNDATIONS else 2
    return (group, n, c["due"])


LLD_PROBLEMS = ("可配置淘汰策略的内存键值存储", "限流器", "可配置缓存", "文件系统", "任务调度器", "日志服务", "多线程日志框架", "停车场", "电梯", "熔断器")  # by reported frequency


def lld_order(cfg: dict, home: dict) -> list[dict]:
    """New low-level-design cards in study order. With `essence`: foundations marked core, a dozen cards each of method and concurrency,
    and the first few cards of the most-reported problems. The rest is reference. Until the deck has exam points this is a rule, not a score."""
    new = _cards(f'("deck:{LLD_ROOT}" OR "deck:{SUBJECT_DECK[LLD_ROOT]}") is:new -is:suspended')
    for c in new:
        c["deckName"] = home.get(str(c["cardId"]), c["deckName"])  # rank by where it lives, also while the plan has borrowed it
    new = sorted((c for c in new if c["deckName"].split("::")[0] == LLD_ROOT), key=lld_rank)
    if not cfg.get("essence"):
        return new
    tags: dict[int, list[str]] = {}
    nids = sorted({c["note"] for c in new})
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            tags[n["noteId"]] = n["tags"]
    out, count = [], defaultdict(int)
    for c in new:
        parts = c["deckName"].split("::")
        top, sub = parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else ""
        if top[:2].isdigit() and int(top[:2]) <= 8:
            keep = "trellis::core" in tags.get(c["note"], [])
        elif top.startswith("11") and sub in LLD_FOUNDATIONS[:2]:
            count[sub] += 1
            keep = count[sub] <= 12
        elif top.startswith(("10", "11")) and sub.startswith(LLD_PROBLEMS):
            name = next(p for p in LLD_PROBLEMS if sub.startswith(p))
            count[name] += 1
            keep = count[name] <= 8
        else:
            keep = False
        if keep:
            out.append(c)
    return out


WORK_PART = f"{DECK}::4 公司实践"
MAP_PART = "0 全生命周期总览"
STAGES = {"overview": "1 全景", "core": "2 核心", "deep": "3 深入"}
LEVEL = {"必会": 1.0, "追问": 0.6, "加分": 0.3}


def work_root(cfg: dict) -> str | None:
    """The private work deck, named only in the local config (its name is private), joins the plan as its own subject."""
    root = (cfg.get("work") or {}).get("deck")
    if root:
        SUBJECT_DECK[root] = WORK_PART
        REVIEWS.setdefault(root, int(cfg["work"].get("reviews", 60)))
    return root


def work_order(cfg: dict, home: dict, points) -> list[dict]:
    """New cards of the work deck in study order, the system-design way: stage first (the system map and the payment life
    cycle, then the core mechanisms, then depth); inside a stage the more required level on the heavier exam point first
    (the point's interview weight from the system-design plan), then moved behind the cards here that teach its
    prerequisites. A `seq::<n>` tag puts authored map cards first in their stage. Each card gets the sub-deck it is dealt into: its stage, and 先学 or 后学 by prerequisite layer.
    Merged and dropped cards are suspended and never dealt."""
    from trellis.plan import PointModel, order_by_prereq, prereq_layers
    root = work_root(cfg)
    if not root:
        return []
    new = _cards(f'("deck:{root}" OR "deck:{WORK_PART}") is:new -is:suspended')
    for c in new:
        c["deckName"] = home.get(str(c["cardId"]), c["deckName"])
    new = [c for c in new if c["deckName"].split("::")[0] == root]
    tags = {}
    nids = sorted({c["note"] for c in new})
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            tags[n["noteId"]] = n["tags"]

    def tag(c, key):
        return [t[len(key) + 2:] for t in tags.get(c["note"], []) if t.startswith(key + "::")]
    weight = dict(points.weight) if points else {}
    floor = min(weight.values()) if weight else 1.0
    kps = {str(c["cardId"]): tag(c, "kp") for c in new}

    def key(c):
        stage = (tag(c, "stage") or ["core"])[0]
        ks = kps[str(c["cardId"])]
        w = weight.get(ks[0], floor) if ks else floor
        seq = tag(c, "seq")  # an authored reading order (the map cards of a stage) comes before the weight order
        return (list(STAGES).index(stage) if stage in STAGES else 1, int(seq[0]) if seq and seq[0].isdigit() else 999,
                -LEVEL.get((tag(c, "level") or ["追问"])[0], 0.6) * w, c["deckName"], c["due"])
    new.sort(key=key)
    model = PointModel(weight, kps, dict(points.prereq) if points else {})
    by_id = {str(c["cardId"]): c for c in new}
    out = []
    for stage, part in STAGES.items():
        ids = [i for i in (str(c["cardId"]) for c in new) if (tag(by_id[i], "stage") or ["core"])[0] == stage]
        ids = order_by_prereq(ids, model)
        layer = prereq_layers(ids, model)
        for i in ids:
            # Anki shows a sub-deck's new cards in the order they were added, so authored map cards get a sub-deck of their own, first
            by_id[i]["part"] = MAP_PART if tag(by_id[i], "seq") else f"{part} · {'先学' if layer.get(i, 0) == 0 else '后学'}"
            out.append(by_id[i])
    return out


def prepare(cfg: dict, sd_value: dict[str, float], now_ms: int | None = None, carry: bool = True, points=None) -> Extra:
    """Pick today's LeetCode problems, low-level design cards and reviews. Reads Anki, writes nothing. With `carry`, new cards
    dealt on an earlier day and not learned stay first, counted in the day's budget."""
    import lc_analysis as lca
    now_ms = now_ms or int(time.time() * 1000)
    ex = Extra()
    weights = {**DEFAULT_DECKS, **cfg.get("decks", {})}
    home = homes()

    # ---- LeetCode: `lc_new` problems a day from two lists of the knowledge tree at a time (Chi 2026-11-11), each problem by
    # its whole answer. The tree is 0x3F's problem lists as deep as his posts go (lc_tree.py). A round takes `per_section`
    # more problems from every leaf, most asked first, in 0x3F's order; two lists are in focus, `per_topic` each a day,
    # and when one has nothing left this round the next list takes its place. A problem is done once answered since the
    # round began; one seen before counts as new and is made due today. The review backlog is not dealt (REVIEWS: 0).
    import lc_tree
    lcfg = {**LC_DEFAULTS, **cfg.get("lc", {})}
    probs = json.loads((ROOT / "sources/local/lc/analysis.json").read_text(encoding="utf-8"))["problems"]
    lc_cards = _cards("(" + " OR ".join(f'"deck:{d}"' for d in LC_ROOTS) + f") OR {daily_query()}")
    ident = _idents(lc_cards)
    built = lc_tree.build()
    tree, core = built["lists"], set(built["core"])
    named = {c["slug"]: f"LC {c['num']} {c['title']}" for lst in tree for _, x in lc_tree.leaves(lst) for c in x["candidates"]}
    slugs_of, known = lca.card_slugs(), set(probs) | set(named)  # a problem added to a thin leaf has no analysis row yet
    by_ident = {ident[c["cardId"]]: c for c in lc_cards if ident.get(c["cardId"])}
    since = int(datetime.fromisoformat(lcfg["since"]).timestamp() * 1000)
    seen_cards = [c["cardId"] for c in lc_cards if c["reps"]]
    revs = call("getReviewsOfCards", cards=seen_cards) if seen_cards else {}
    done = set()
    for c in lc_cards:
        if any(r["id"] >= since for r in revs.get(str(c["cardId"]), [])):
            slug, _ = lca.resolve(ident.get(c["cardId"], ""), slugs_of, known)
            done.add(slug)

    def card_for(slug: str) -> dict | None:
        card = next((by_ident[p.format(s=slug)] for p in PREFER if p.format(s=slug) in by_ident), None)
        return card if card and card["queue"] != -1 else None  # suspended by hand: left out

    per = int(lcfg["per_section"])

    def left(lst: dict, r: int, only: set | None) -> list[tuple[str, str, str]]:
        """(slug, leaf label, leaf id) still to do this round, in the list's order; with `only`, just those problems."""
        return [(s, f"{n:02d} " + " › ".join(path[1:]), leaf["id"]) for n, (path, leaf) in enumerate(lc_tree.leaves(lst), 1)
                for s in [x for x in leaf["problems"] if only is None or x in only][:per * r] if s not in done and card_for(s)]

    rounds = range(1, max((len(x["problems"]) for lst in tree for _, x in lc_tree.leaves(lst)), default=0) // per + 2)
    # 80/20: the core problems first, through every round; the rest only once the core is done
    r, only = next(((r, o) for o in (core, None) for r in rounds if any(left(lst, r, o) for lst in tree)), (None, None))
    if r:
        left = functools.partial(left, only=only)
        limit, active = int(cfg.get("lc_new", 10)), [lst for lst in tree if left(lst, r)]
        picks = [(lst["title"], *x) for lst in active[:2] for x in left(lst, r)[:int(lcfg["per_topic"])]]
        for lst in active:  # a list in focus with less than its share left: the next list fills the day
            picks += [(lst["title"], *x) for x in left(lst, r) if x[0] not in {p[1] for p in picks}][:max(0, limit - len(picks))]
        today = anki_today()
        learned = set()
        for name, slug, section, leaf in picks[:limit]:
            learn = by_ident.get(lc_tree.card_id(leaf))
            if learn and learn["queue"] == 0 and leaf not in learned:  # the leaf's learning card comes before its first problem
                learned.add(leaf)
                ex.lc_new.append({"card": learn["cardId"], "slug": "", "title": "学习卡", "topic": name, "section": section,
                                  "why": "先学套路", "due_now": False, "learn": True})
            card = card_for(slug)
            ex.lc_new.append({"card": card["cardId"], "slug": slug, "title": probs[slug]["title"] if slug in probs else named.get(slug, slug), "topic": name, "section": section,
                              "why": f"{'核心题' if only else '其余题'} · 第 {r} 轮", "due_now": card["queue"] in (2, 3) and card["due"] > today})
        ex.lc_focus = list(dict.fromkeys(x["topic"] for x in ex.lc_new))

    # ---- low-level design: its own budget
    today = anki_today()
    inside = _cards(f'{daily_query()} is:new') if carry else []
    lld_limit = int(cfg.get("lld_new", 100))
    for c in inside:
        if home.get(str(c["cardId"]), "").split("::")[0] == LLD_ROOT and len(ex.lld_new) < lld_limit:
            ex.lld_new.append({"card": c["cardId"], "carried": True})
    have = {x["card"] for x in ex.lld_new}
    for c in lld_order(cfg, home):
        if len(ex.lld_new) >= lld_limit:
            break
        if c["cardId"] not in have:
            ex.lld_new.append({"card": c["cardId"], "carried": False})

    # ---- the private work deck: its own budget, in the order of work_order
    root = work_root(cfg)
    if root:
        work_limit = int(cfg["work"].get("new", 30))
        for c in inside:
            if home.get(str(c["cardId"]), "").split("::")[0] == root and len(ex.work_new) < work_limit:
                ex.work_new.append({"card": c["cardId"], "part": CARRIED, "carried": True})
        have = {x["card"] for x in ex.work_new}
        for c in work_order(cfg, home, points):
            if len(ex.work_new) >= work_limit:
                break
            if c["cardId"] not in have:
                ex.work_new.append({"card": c["cardId"], "part": c["part"], "carried": False})

    # ---- reviews: each subject's most valuable due cards, within its own budget
    due = _cards("is:due -is:suspended")
    due_ident = _idents(due)
    raw = []
    for c in due:
        h = home.get(str(c["cardId"]), c["deckName"])
        if in_daily(h):  # dealt by the system-design plan today; it is already in the deck
            continue
        root = h.split("::")[0]
        idn = due_ident.get(c["cardId"], "")
        slug = None
        if root in LC_ROOTS:
            slug, _ = lca.resolve(idn, slugs_of, known)
            value = probs.get(slug, {}).get("importance", 0.0) if slug else 0.0
        else:
            value = sd_value.get(idn, 0.0)
        raw.append((c, h, root, slug, value))
    # value as a percentile inside its deck: decks measure value on different scales
    ranks: dict[str, list[float]] = defaultdict(list)
    for _, _, root, _, v in raw:
        ranks[root].append(v)
    for v in ranks.values():
        v.sort()

    def pct(root, v):
        vals = ranks[root]
        if len(vals) < 2 or vals[0] == vals[-1]:
            return 0.5
        import bisect
        return bisect.bisect_left(vals, v) / (len(vals) - 1)

    scored, one_per_problem = [], {}
    for c, h, root, slug, v in raw:
        value = pct(root, v)
        if c["queue"] == 2:
            overdue = max(0, today - c["due"])
            urgency = 1 + min(URGENCY_CAP, overdue / max(1, c["interval"]))
        else:
            urgency = 1 + URGENCY_CAP  # in its learning steps: finish it today
        score = weights.get(root, 0.2) * (VALUE_FLOOR + value) * urgency
        if slug:  # copies of one problem: review the strongest-scored copy only
            prev = one_per_problem.get(slug)
            if prev and prev["score"] >= score:
                continue
            one_per_problem[slug] = {"card": c["cardId"], "home": h, "score": score, "root": root}
            continue
        scored.append({"card": c["cardId"], "home": h, "score": score, "root": root})
    scored += list(one_per_problem.values())
    scored = [s for s in scored if s["card"] not in {x["card"] for x in ex.lc_similar + ex.lc_new}]
    budgets = {**REVIEWS, **cfg.get("reviews", {})}
    scored.sort(key=lambda s: -s["score"])
    taken_of: dict[str, int] = defaultdict(int)
    for s in scored:
        if s["root"] in budgets:
            if taken_of[s["root"]] < budgets[s["root"]]:
                taken_of[s["root"]] += 1
                ex.reviews.append(s)
            else:
                ex.backlog += 1
    counts = defaultdict(int)
    for s in ex.reviews:
        counts[s["root"]] += 1
    ex.by_deck = dict(sorted(counts.items(), key=lambda kv: -kv[1]))
    return ex


def release(keep: set[int]) -> int:
    """Cards this module moved into 今日计划 go home unless picked again. Returns how many moved."""
    home = homes()
    if not home:
        return 0
    inside = {c["cardId"]: c for c in _cards(daily_query())}
    back = defaultdict(list)
    for cid, deck in list(home.items()):
        cid_i = int(cid)
        if cid_i in keep:
            continue
        if cid_i in inside:
            back[deck].append(cid_i)
        del home[cid]
    for deck, ids in back.items():
        call("changeDeck", cards=ids, deck=deck)
    HOMES.write_text(json.dumps(home, ensure_ascii=False, indent=0), encoding="utf-8")
    return sum(len(v) for v in back.values())


def deal(ex: Extra) -> None:
    home = homes()
    info = {c["cardId"]: c for c in call("cardsInfo", cards=[x["card"] for x in ex.lc_new + ex.lc_similar + ex.lld_new + ex.work_new + ex.reviews])}
    lc, lld = SUBJECT_DECK["LeetCode Tops"], SUBJECT_DECK[LLD_ROOT]
    plan = [(f"{lc}::{n} {topic}::{sec}", [x for x in ex.lc_new if (x["topic"], x["section"]) == (topic, sec)])
            for n, topic in enumerate(ex.lc_focus, 1) for sec in dict.fromkeys(x["section"] for x in ex.lc_new if x["topic"] == topic)]
    plan += [(f"{lld}::{CARRIED}", [x for x in ex.lld_new if x["carried"]]), (f"{lld}::2 新卡", [x for x in ex.lld_new if not x["carried"]])]
    plan += [(f"{WORK_PART}::{part}", [x for x in ex.work_new if x["part"] == part]) for part in dict.fromkeys(x["part"] for x in ex.work_new)]
    plan += [(f"{d}::9 到期复习", [x for x in ex.reviews if x["root"] == r]) for r, d in SUBJECT_DECK.items()]
    for stage, items in plan:
        ids = [x["card"] for x in items if x["card"] in info]
        for i in ids:
            if not in_daily(info[i]["deckName"]):
                home[str(i)] = info[i]["deckName"]
        if ids:
            call("changeDeck", cards=ids, deck=stage)
    now_due = [x["card"] for x in ex.lc_new + ex.lc_similar if x.get("due_now")]  # a problem seen before is due today again
    if now_due:
        call("setDueDate", cards=now_due, days="0")
    HOMES.write_text(json.dumps(home, ensure_ascii=False, indent=0), encoding="utf-8")


def keep_ids(ex: Extra) -> set[int]:
    return {x["card"] for x in ex.lc_new + ex.lc_similar + ex.lld_new + ex.work_new + ex.reviews}


def main() -> int:
    cfg = json.loads((OUT / "config.json").read_text(encoding="utf-8"))
    ex = prepare(cfg, {})
    print(f"LeetCode: {len(ex.lc_new)} new, {len(ex.lc_similar)} similar · low-level design: {len(ex.lld_new)} new · work: {len(ex.work_new)} new")
    for part in dict.fromkeys(x["part"] for x in ex.work_new):
        print(f"  work {part}: {sum(x['part'] == part for x in ex.work_new)}")
    for x in ex.lc_similar:
        print(f"  similar {x['title']}  ({x['why']}){'  [due now]' if x['due_now'] else ''}")
    for x in ex.lc_new:
        print(f"  new {x['title']}")
    print(f"reviews: {len(ex.reviews)} taken, {ex.backlog} left in their decks · {ex.by_deck}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
