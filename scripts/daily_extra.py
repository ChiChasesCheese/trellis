"""The parts of the daily plan beyond system design: LeetCode practice and the review queue of every deck.

study_plan.py calls this; on its own it prints what it would do:

    uv run python scripts/daily_extra.py            # dry run

LeetCode (deck stage `4 算法`):
- **Similar problems.** A problem pressed 「忘记」 in the last `similar_days` days brings up to `similar_per_fail` problems
  not held yet, ranked by similarity plus asked-frequency. Similarity = 4 if the failed problem's solution lists it under
  同模式 + 3 x same main technique + 1.5 x shared techniques + shared patterns + 0.5 x shared pitfalls; at least 4 to count. A similar problem never
  seen is dealt as new; one seen but not held is made due today (Anki's own Set Due Date).
- **New problems.** `lc_new` unseen problems a day, by what each adds: importance x the slip boost of its main technique
  (at most 1.5) x how much of that technique is not held, less for each pick on the same technique that day.
- **Just solved.** New cards in the daily deck (one per problem solved on LeetCode) are dealt first, up to `solved_max`.
- The card dealt for a problem is fixed by the deck layout: its whole answer in the module deck, as in lc_lists.py.

Reviews (deck stage `5 到期复习`): every due card in every deck, ranked by
    deck weight x (0.3 + value) x urgency,   urgency = 1 + min(2, days overdue / interval)
where value is the percentile, inside its deck, of the card's planner value (system design) or its problem's importance
(LeetCode); cards with no value measure sit at 0.5. The
first `review_budget` come into the plan; one card per LeetCode problem. The rest wait in their decks.

Every card moved into 今日计划 is recorded with its home deck in sources/local/plan/homes.json and goes back there at the
next run unless it is picked again.
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lc_data import call  # noqa: E402

OUT = ROOT / "sources/local/plan"
HOMES = OUT / "homes.json"
DECK = "今日计划"
CARRIED = "0 昨天没学完"  # what was dealt and not learned comes first the next day
LLD_ROOT, SD_ROOT = "低层设计（LLD）", "系统设计"
SUBJECT_DECK = {SD_ROOT: "1 系统设计", LLD_ROOT: "2 低层设计", "LeetCode Tops": "3 算法"}  # each subject has its own part and budget
REVIEWS = {SD_ROOT: 150, LLD_ROOT: 80, "LeetCode Tops": 60}
LLD_FOUNDATIONS = ("低层设计答题框架", "并发", "低层设计跨题模式")
DAY_MS = 86_400_000
URGENCY_CAP = 2.0  # how far overdue-ness can raise a review: urgency is 1 + min(cap, days overdue / interval)
VALUE_FLOOR = 0.3  # a review of the least valuable card in a deck still counts this much
LC_ROOTS = ("LeetCode Tops",)
SOLVED_DECK = "LeetCode Tops::28 Daily"
PREFER = ("tlc-tops-{s}-0-whole", "tlc-{s}-0-whole", "tlc-core-{s}", "lca-{s}", "tlc-daily-{s}-0-whole")
DEFAULT_DECKS = {"系统设计": 1.0, "LeetCode Tops": 1.0, "低层设计（LLD）": 0.6, "Kafka": 0.5, "Python": 0.5,
                 "Code Core": 0.5, "Narrative Round": 0.4, "编程语言原理：Go · Java · Rust · Python · C++": 0.3,
                 "Snowflake 原理": 0.3, "HFT 低延迟交易系统": 0.2, "CDN Content": 0.2, "Stripe": 0.2, "篮球（Basketball）": 0.2,
                 "Headlands": 0.1, "Markets & Factors": 0.1, "Quant Infrastructure": 0.1}


@dataclass
class Extra:
    lc_new: list[dict] = field(default_factory=list)       # {card, slug, title, why}
    lc_similar: list[dict] = field(default_factory=list)   # {card, slug, title, why, due_now}
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
    new = _cards(f'("deck:{LLD_ROOT}" OR "deck:{DECK}::{SUBJECT_DECK[LLD_ROOT]}") is:new -is:suspended')
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


WORK_PART = "4 公司实践"
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
    prerequisites. Each card gets the sub-deck it is dealt into: its stage, and 先学 or 后学 by prerequisite layer.
    Merged and dropped cards are suspended and never dealt."""
    from trellis.plan import PointModel, order_by_prereq, prereq_layers
    root = work_root(cfg)
    if not root:
        return []
    new = _cards(f'("deck:{root}" OR "deck:{DECK}::{WORK_PART}") is:new -is:suspended')
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
        return (list(STAGES).index(stage) if stage in STAGES else 1, -LEVEL.get((tag(c, "level") or ["追问"])[0], 0.6) * w, c["deckName"], c["due"])
    new.sort(key=key)
    model = PointModel(weight, kps, dict(points.prereq) if points else {})
    by_id = {str(c["cardId"]): c for c in new}
    out = []
    for stage, part in STAGES.items():
        ids = [i for i in (str(c["cardId"]) for c in new) if (tag(by_id[i], "stage") or ["core"])[0] == stage]
        ids = order_by_prereq(ids, model)
        layer = prereq_layers(ids, model)
        for i in ids:
            by_id[i]["part"] = f"{part} · {'先学' if layer.get(i, 0) == 0 else '后学'}"
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

    # ---- LeetCode
    analysis = json.loads((ROOT / "sources/local/lc/analysis.json").read_text(encoding="utf-8"))
    probs = analysis["problems"]
    boost = {t["id"]: min(1.5, max(1.0, 1 + 0.5 * (t["slip_ratio"] - 1))) for t in analysis["dims"]["techniques"]}
    lc_cards = _cards(" OR ".join(f'"deck:{d}"' for d in LC_ROOTS) + ' OR "deck:今日计划"')
    ident = _idents(lc_cards)
    slugs_of, known = lca.card_slugs(), set(probs)
    by_ident = {ident[c["cardId"]]: c for c in lc_cards if ident.get(c["cardId"])}
    seen_cards = [c["cardId"] for c in lc_cards if c["reps"]]
    revs = call("getReviewsOfCards", cards=seen_cards) if seen_cards else {}
    failed = {}
    for c in lc_cards:
        slug, _ = lca.resolve(ident.get(c["cardId"], ""), slugs_of, known)
        if slug and any(r["ease"] == 1 and r["id"] > now_ms - int(cfg.get("similar_days", 7)) * DAY_MS
                        for r in revs.get(str(c["cardId"]), [])):
            failed[slug] = probs[slug]

    def card_for(slug: str) -> dict | None:
        return next((by_ident[p.format(s=slug)] for p in PREFER if p.format(s=slug) in by_ident), None)

    today = anki_today()
    taken = set(failed)
    same_file = ROOT / "sources/local/lc/same.json"  # the problems each solution itself lists under 同模式
    same = json.loads(same_file.read_text(encoding="utf-8")) if same_file.exists() else {}
    per_fail, cap = int(cfg.get("similar_per_fail", 2)), int(cfg.get("similar_max", 10))
    for slug, f in sorted(failed.items(), key=lambda kv: -kv[1]["importance"]):
        if not f["techniques"]:
            continue
        def sim(p, f=f):
            return (4.0 * (p["num"] in same.get(f["slug"], ())) + 3.0 * (p["techniques"][:1] == f["techniques"][:1])
                    + 1.5 * len(set(p["techniques"]) & set(f["techniques"])) + len(set(p["patterns"]) & set(f["patterns"]))
                    + 0.5 * len(set(p["pitfalls"]) & set(f["pitfalls"])))
        imp_top = max(p["importance"] for p in probs.values()) or 1.0
        cands = [p for s, p in probs.items() if s not in taken and p["mastery"] < 0.5 and p["techniques"] and sim(p) >= 4.0]
        cands.sort(key=lambda p: -(sim(p) + 2 * p["importance"] / imp_top))
        for p in cands[:per_fail]:
            card = card_for(p["slug"])
            if card is None or len(ex.lc_similar) >= cap:
                continue
            taken.add(p["slug"])
            ex.lc_similar.append({"card": card["cardId"], "slug": p["slug"], "title": p["title"],
                                  "why": f"和你刚忘的「{f['title']}」同一个思路", "due_now": card["queue"] == 2 and card["due"] > today})
    # the day's new LeetCode cards all count against one budget: what was left yesterday, then similar problems, then the rest
    limit = int(cfg.get("lc_new", 20))
    inside = _cards(f'"deck:{DECK}" is:new') if carry else []
    inside_ident = _idents(inside)
    for c in inside:
        if home.get(str(c["cardId"]), "").split("::")[0] in LC_ROOTS and len(ex.lc_new) < limit:
            slug, _ = lca.resolve(inside_ident.get(c["cardId"], ""), slugs_of, known)
            ex.lc_new.append({"card": c["cardId"], "slug": slug or "", "title": probs[slug]["title"] if slug else inside_ident.get(c["cardId"], ""),
                              "why": "昨天没学完", "carried": True})
            taken.add(slug)
    ex.lc_similar = [x for x in ex.lc_similar if x["slug"] not in {n["slug"] for n in ex.lc_new}]
    room = limit - len(ex.lc_new) - sum(1 for x in ex.lc_similar if not x["due_now"])
    # problems just solved on LeetCode (the daily deck writes one card each): deal them while the solve is fresh
    solved = 0
    for c in lc_cards:
        if c["queue"] == 0 and c["deckName"].startswith(SOLVED_DECK) and solved < min(int(cfg.get("solved_max", 10)), room):
            solved += 1
            slug, _ = lca.resolve(ident.get(c["cardId"], ""), slugs_of, known)
            ex.lc_new.append({"card": c["cardId"], "slug": slug or "", "title": probs[slug]["title"] if slug else ident.get(c["cardId"], ""),
                              "why": "你刚在 LeetCode 上做过"})
            taken.add(slug)
    fresh = [p for s, p in probs.items() if s not in taken and not p["seen"] and p["techniques"]]
    # what a new problem adds: its frequency, on a technique not held yet, less again for each pick on that technique today
    held = {t["id"]: t["mastery"] for t in analysis["dims"]["techniques"]}
    picks_on: dict[str, int] = defaultdict(int)
    while len(ex.lc_new) + sum(1 for x in ex.lc_similar if not x["due_now"]) < limit and fresh:
        def worth(p):
            t = p["techniques"][0]
            return p["importance"] * boost.get(t, 1.0) * (1 - held.get(t, 0.0)) * 0.6 ** picks_on[t]
        p = max(fresh, key=worth)
        fresh.remove(p)
        card = card_for(p["slug"])
        if card and card["queue"] == 0:
            ex.lc_new.append({"card": card["cardId"], "slug": p["slug"], "title": p["title"], "why": "考频高，这个思路还没掌握"})
            taken.add(p["slug"])
            picks_on[p["techniques"][0]] += 1

    # ---- low-level design: its own budget
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
        if h.startswith(DECK):  # dealt by the system-design plan today; it is already in the deck
            continue
        root = h.split("::")[0]
        idn = due_ident.get(c["cardId"], "")
        slug = None
        if root in LC_ROOTS:
            slug, _ = lca.resolve(idn, slugs_of, known)
            value = probs[slug]["importance"] if slug else 0.0
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
    inside = {c["cardId"]: c for c in _cards(f'"deck:{DECK}"')}
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
    plan = [(f"{lc}::{CARRIED}", [x for x in ex.lc_new if x.get("carried")]),
            (f"{lc}::2 新题与相似题", [x for x in ex.lc_new if not x.get("carried")] + ex.lc_similar),
            (f"{lld}::{CARRIED}", [x for x in ex.lld_new if x["carried"]]), (f"{lld}::2 新卡", [x for x in ex.lld_new if not x["carried"]])]
    plan += [(f"{WORK_PART}::{part}", [x for x in ex.work_new if x["part"] == part]) for part in dict.fromkeys(x["part"] for x in ex.work_new)]
    plan += [(f"{d}::9 到期复习", [x for x in ex.reviews if x["root"] == r]) for r, d in SUBJECT_DECK.items()]
    for stage, items in plan:
        ids = [x["card"] for x in items if x["card"] in info]
        for i in ids:
            if not info[i]["deckName"].startswith(DECK):
                home[str(i)] = info[i]["deckName"]
        if ids:
            call("changeDeck", cards=ids, deck=f"{DECK}::{stage}")
    now_due = [x["card"] for x in ex.lc_similar if x["due_now"]]
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
