"""Quick deck planner: one order for the cards not yet seen and the day's number of new ones, both from the answers so far.

    uv run python scripts/quick_plan.py             # what it would do, nothing written to Anki
    uv run python scripts/quick_plan.py --apply     # deal the day's cards, set the day's limit (study_plan.py daily does this)

There are no day batches for the learner: every unseen card has one priority, the list is sorted by it and cut at the
day's number. The priority of a card is

    weight of its point × need × fit × related × hold

* need: how likely the point is to be news. How well a point is known is predicted from the first answers so far:
  the overall level, the topic, and how the point's prerequisites went. Small samples are shrunk towards the overall
  level, so one answer moves a topic a little and ten move it a lot.
* fit: the difficulty dial. The recent first answers are scored (Again 0, Hard 0.5, Good 0.8, Easy 1; a slow right
  answer a little less) and compared with a target just under "all Good". Above it, cards predicted harder come
  forward (weaker topics, recall formats); below it, cards predicted easier do (recognition formats).
* related: a miss brings forward the unseen prerequisites of the missed point and the unseen points of its topic.
* hold: a point that builds on a missed one waits until the missed one is answered right again.
* focus: a multiplier per topic from `quick.focus` in the plan config, for what a real mock interview showed weak.

A miss fades: each later right answer after an hour or more halves it, and so do four days. The points still missed
are written to deepen.json; the main plan deals their full cards first (study_plan.py).

The day's number follows what was actually done: more after a finished day, fewer when cards seen again are being
forgotten or the days stay unfinished, never more than the time budget allows.

The cut is made with decks, because AnkiConnect refuses to write a new card's position: the day's cards and every card
already seen sit in the deck itself, the other unseen cards in the sub-deck WAIT, whose preset deals no new cards.
Inside the day Anki deals by import position, which already has every prerequisite before the point built on it.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import quick_deck as qd  # noqa: E402

SCORE = {1: 0.0, 2: 0.5, 3: 0.8, 4: 1.0}
SLOW, SLOW_FLOOR, SLOW_COST = 2.5, 20.0, 0.15  # a right answer slower than this many medians (and seconds) was not fluent
SPACED_H = 1.0  # an answer this long after the previous one tests memory, not the last minute
HALF_LIFE_DAYS = 4.0
LEVEL, K_LEVEL, K_TOPIC, K_FORMAT = 0.75, 10, 4, 8  # the level assumed before any answer, and how many answers outweigh an assumption
FORMAT_PRIOR = {"mc": 0.05, "match": 0.05, "order": 0.0, "cloze": -0.03, "qa": -0.05, "flaw": -0.05}  # recognising is easier than recalling
PREREQ_CARRY = 0.3  # how much of a prerequisite's result carries to the point built on it
DEFAULTS = {"target": 0.75, "band": 0.15, "tilt": 0.5, "recent": 40, "prereq_boost": 1.5, "topic_boost": 0.6, "hold": 0.5,
            "window": 8, "per_window": 2, "min_new": 30, "max_new": 200, "minutes": 90, "grow": 1.15, "shrink": 0.8,
            "retention_floor": 0.75, "deepen_per_day": 10, "rollover_hour": 4, "focus": {}}


def settings() -> dict:
    cfg = qd.config()
    return {**DEFAULTS, **{k: v for k, v in cfg.items() if k in DEFAULTS}, "per_day": int(cfg["per_day"])}


@dataclass
class Sight:
    at: int  # ms
    ease: int
    secs: float


@dataclass
class Card:
    kp: str
    fmt: str
    topic: str
    weight: float
    cid: int = 0
    new: bool = True
    due: int = 0
    deck: str = ""
    sights: list[Sight] = field(default_factory=list)


# ---------------------------------------------------------------- evidence


def first_scores(cards: list[Card]) -> dict[str, float]:
    """Each seen point's first answer as a score."""
    times = [s.secs for c in cards for s in c.sights]
    slow = max(SLOW_FLOOR, SLOW * median(times)) if times else SLOW_FLOOR
    out = {}
    for c in cards:
        if c.sights:
            s = c.sights[0]
            out[c.kp] = max(0.0, SCORE.get(s.ease, 0.8) - (SLOW_COST if s.ease >= 3 and s.secs > slow else 0.0))
    return out


def open_miss(c: Card, now_ms: int) -> float:
    """0..1: how much the point still counts as missed."""
    m, last = 0.0, 0
    for n, s in enumerate(c.sights):
        spaced = n == 0 or (s.at - c.sights[n - 1].at) >= SPACED_H * 3600_000
        if not spaced:
            continue
        if s.ease == 1:
            m, last = 1.0, s.at
        elif s.ease == 2 and n == 0:
            m, last = 0.5, s.at
        elif s.ease >= 3 and n > 0:
            m /= 2
    if not m:
        return 0.0
    return m * 0.5 ** ((now_ms - last) / 86400_000 / HALF_LIFE_DAYS)


def predict(cards: list[Card], prereq: dict[str, list[str]], scores: dict[str, float]) -> tuple[dict[str, float], dict]:
    """The chance of a right first answer for every card, and the parts it was built from."""
    seen = [c for c in cards if c.kp in scores]
    level = (LEVEL * K_LEVEL + sum(scores[c.kp] for c in seen)) / (K_LEVEL + len(seen))
    by_topic, by_fmt = defaultdict(list), defaultdict(list)
    for c in seen:
        by_topic[c.topic].append(scores[c.kp] - level)
        by_fmt[c.fmt].append(scores[c.kp] - level)
    topic = {t: sum(v) / (len(v) + K_TOPIC) for t, v in by_topic.items()}
    fmt = {f: (K_FORMAT * FORMAT_PRIOR.get(f, 0.0) + sum(by_fmt.get(f, []))) / (K_FORMAT + len(by_fmt.get(f, []))) for f in qd.FORMATS}
    p, know = {}, {}
    for c in cards:
        known = [scores[q] - level for q in prereq.get(c.kp, []) if q in scores]
        carry = PREREQ_CARRY * sum(known) / len(known) if known else 0.0
        know[c.kp] = min(0.98, max(0.05, level + topic.get(c.topic, 0.0) + carry))  # the point, whatever the card's format
        p[c.kp] = min(0.98, max(0.05, know[c.kp] + fmt.get(c.fmt, 0.0)))
    return p, {"level": level, "topic": topic, "format": fmt, "n": len(seen), "know": know}


def tilt(cards: list[Card], scores: dict[str, float], cfg: dict) -> tuple[float, float | None]:
    """-1..1: below 0 the recent cards were too hard, above 0 too easy. Needs a real sample first."""
    recent = sorted((c for c in cards if c.kp in scores), key=lambda c: c.sights[0].at)[-int(cfg["recent"]):]
    if len(recent) < 15:
        return 0.0, None
    mean = sum(scores[c.kp] for c in recent) / len(recent)
    return max(-1.0, min(1.0, (mean - cfg["target"]) / cfg["band"])), mean


# ---------------------------------------------------------------- priority and order


def priorities(cards: list[Card], prereq: dict[str, list[str]], now_ms: int, cfg: dict) -> tuple[dict[str, float], dict]:
    scores = first_scores(cards)
    p, parts = predict(cards, prereq, scores)
    t, recent = tilt(cards, scores, cfg)
    unseen = [c for c in cards if c.new and not c.sights]
    mean_p = sum(p[c.kp] for c in unseen) / len(unseen) if unseen else LEVEL
    miss = {c.kp: m for c in cards if (m := open_miss(c, now_ms)) > 0.05}
    topic_miss = defaultdict(float)
    topic_of = {c.kp: c.topic for c in cards}
    for k, m in miss.items():
        topic_miss[topic_of[k]] += m
    wanted_by = defaultdict(float)  # an unseen prerequisite of a missed point -> the strongest such miss
    for k, m in miss.items():
        for q in prereq.get(k, []):
            wanted_by[q] = max(wanted_by[q], m)
    out, why = {}, {}
    for c in unseen:
        need = (1.0 - parts["know"][c.kp]) ** 0.5
        fit = max(0.5, min(1.6, 1.0 + cfg["tilt"] * t * (mean_p - p[c.kp]) / 0.2))
        related = 1.0 + cfg["prereq_boost"] * wanted_by.get(c.kp, 0.0) + cfg["topic_boost"] * min(1.0, topic_miss.get(c.topic, 0.0))
        hold = 1.0 - cfg["hold"] * max((miss.get(q, 0.0) for q in prereq.get(c.kp, [])), default=0.0)
        focus = float(cfg["focus"].get(c.topic, 1.0))  # topics a real mock showed weak (config quick.focus)
        out[c.kp] = c.weight * need * fit * related * hold * focus
        why[c.kp] = {"p": round(p[c.kp], 3), "need": round(need, 3), "fit": round(fit, 3), "related": round(related, 3), "hold": round(hold, 3),
                     "focus": focus}
    return out, {**parts, "tilt": t, "recent": recent, "miss": miss, "why": why, "scores": scores}


def order(cards: list[Card], priority: dict[str, float], prereq: dict[str, list[str]], cfg: dict) -> list[Card]:
    """Highest priority first, a prerequisite before what builds on it, and no run of one topic."""
    unseen = {c.kp: c for c in cards if c.kp in priority}
    pr = dict(priority)
    for k in sorted(unseen, key=lambda k: -priority[k]):  # a prerequisite is at least as urgent as what waits for it
        stack, done = [k], {k}
        while stack:
            cur = stack.pop()
            for q in prereq.get(cur, []):
                if q in unseen and q not in done:
                    done.add(q)
                    pr[q] = max(pr[q], pr[k] * 1.0001)
                    stack.append(q)
    left = sorted(unseen.values(), key=lambda c: -pr[c.kp])
    waiting = set(unseen)
    out, recent = [], deque(maxlen=int(cfg["window"]))
    while left:
        ready = [c for c in left if not any(q in waiting and q != c.kp for q in prereq.get(c.kp, []))] or left  # `or left`: a cycle
        pick = next((c for c in ready if recent.count(c.topic) < int(cfg["per_window"])), ready[0])
        out.append(pick)
        recent.append(pick.topic)
        waiting.discard(pick.kp)
        left.remove(pick)
    return out


# ---------------------------------------------------------------- the day's number


def study_day(at_ms: int, rollover: int) -> str:
    return (datetime.fromtimestamp(at_ms / 1000) - timedelta(hours=rollover)).strftime("%Y-%m-%d")


def history(cards: list[Card], rollover: int) -> dict[str, dict]:
    """Per study day: new cards started, their mean first score, and how the cards seen again after an hour went."""
    scores = first_scores(cards)
    days = defaultdict(lambda: {"new": 0, "score": 0.0, "later": 0, "later_ok": 0, "answers": 0, "secs": 0.0})
    for c in cards:
        for n, s in enumerate(c.sights):
            d = days[study_day(s.at, rollover)]
            d["answers"] += 1
            d["secs"] += s.secs
            if n == 0:
                d["new"] += 1
                d["score"] += scores[c.kp]
            elif s.at - c.sights[n - 1].at >= SPACED_H * 3600_000:
                d["later"] += 1
                d["later_ok"] += s.ease > 1
    for d in days.values():
        d["score"] = d["score"] / d["new"] if d["new"] else None
    return dict(sorted(days.items()))


def quota(days: dict[str, dict], limits: dict[str, int], current: int, due_soon: int, unseen: int, cfg: dict) -> tuple[int, str]:
    """Tomorrow's number of new cards and the reason. `days` holds finished study days only; `limits` what each was allowed."""
    done = [(d, v) for d, v in days.items() if v["new"]]
    n, reason = current, "没有新的作答，数量不变"
    if done:
        last_day, last = done[-1]
        limit = limits.get(last_day, current)
        later = sum(v["later"] for _, v in done[-3:])
        later_ok = sum(v["later_ok"] for _, v in done[-3:])
        short = [v["new"] for d, v in done[-2:] if v["new"] < 0.6 * limits.get(d, current)]
        if later >= 15 and later_ok / later < cfg["retention_floor"]:
            n, reason = round(current * cfg["shrink"]), f"隔 1 小时以上再见只答对 {later_ok / later:.0%}，先减量巩固"
        elif last["new"] >= 0.95 * limit and (last["score"] or 0) >= 0.6:
            n, reason = round(current * cfg["grow"]), f"上一天 {last['new']}/{limit} 做完且初见得分 {last['score']:.2f}，加量"
        elif len(short) == 2:
            n, reason = round((current + max(short)) / 2), f"连续两天没做完（{short[0]}、{short[1]}），向实际完成量靠拢"
        else:
            n, reason = current, f"上一天 {last['new']}/{limit}，数量不变"
    # the time budget: a new card costs its first-day answers, a card due costs one
    answers = sum(v["answers"] for _, v in done)
    per_answer = sum(v["secs"] for _, v in done) / answers if answers else 12.0
    per_new = per_answer * (answers / max(1, sum(v["new"] for _, v in done)) if answers else 3.0)
    room = int((cfg["minutes"] * 60 - due_soon * per_answer) / per_new) if per_new else n
    if n > room:
        n, reason = room, reason + f"；时间预算 {cfg['minutes']} 分钟只容得下 {max(room, 0)} 张"
    n = max(int(cfg["min_new"]), min(int(cfg["max_new"]), n))
    return min(n, unseen) if unseen else n, reason


def moves(cards: list[Card], today: set[str], home: str, wait: str, title: dict[str, str] | None = None) -> dict[str, list[int]]:
    """Deck -> the cards to move there: unseen cards outside today's cut wait, everything else is in the deck itself, in
    the sub-deck of its topic when `title` names it (Chi, 2026-11-12: show what is being drilled, as 今日算法 does)."""
    out: dict[str, list[int]] = {home: [], wait: []}
    for c in cards:
        mine = f"{home}::{title[c.topic]}" if title and c.topic in title else home
        want = wait if c.new and not c.sights and c.kp not in today else mine
        if c.deck != want:
            out.setdefault(want, []).append(c.cid)
    return {deck: ids for deck, ids in out.items() if ids}


# ---------------------------------------------------------------- Anki

WAIT = f"{qd.DECK}::后备"  # unseen cards outside today's cut


def waiting_deck(call) -> None:
    """The sub-deck for the cards not dealt yet, on a preset of its own that gives no new cards."""
    if WAIT not in call("deckNames"):
        call("createDeck", deck=WAIT)
    conf = call("getDeckConfig", deck=WAIT)
    if conf["name"] != f"{qd.PRESET}::后备":  # the preset kept the deck's old name
        cid = call("cloneDeckConfigId", name=f"{qd.PRESET}::后备", cloneFrom=call("getDeckConfig", deck=qd.DECK)["id"])
        if not cid:
            raise RuntimeError(f"could not create preset {WAIT}")
        call("setDeckConfigId", decks=[WAIT], configId=cid)
        conf = call("getDeckConfig", deck=WAIT)
    if conf["new"]["perDay"] != 0:
        conf["new"]["perDay"] = 0
        call("saveDeckConfig", config=conf)


def deal(call, cards: list[Card], today: set[str]) -> int:
    waiting_deck(call)
    title = {p["topic"]: p["topic_title"] for p in json.loads((qd.HOME / "points.json").read_text(encoding="utf-8"))}
    todo = moves(cards, today, qd.DECK, WAIT, title)
    for deck, ids in todo.items():
        call("changeDeck", cards=ids, deck=deck)
    # the topic sub-decks share the deck's preset, which takes new cards by position across them: the planned order holds
    conf = call("getDeckConfig", deck=qd.DECK)
    subs = [d for d in call("deckNames") if d.startswith(qd.DECK + "::") and not d.startswith(WAIT)]
    if subs:
        call("setDeckConfigId", decks=subs, configId=conf["id"])
    if conf.get("newGatherPriority") != 1:  # 1: lowest position first, across sub-decks
        conf["newGatherPriority"] = 1
        call("saveDeckConfig", config=conf)
    empty = sorted((d for d in subs if not call("findCards", query=f'"deck:{d}"')), key=len, reverse=True)
    if empty:
        call("deleteDecks", decks=empty, cardsToo=True)
    return sum(len(ids) for ids in todo.values())


def park(call) -> int:
    """After an import in the middle of a day: the fresh cards wait, the day's cut stays as it was dealt."""
    state_file = qd.HOME / "plan_state.json"
    if not state_file.exists():
        return plan(call, apply=True)["moved"]
    return deal(call, load(call), set(json.loads(state_file.read_text(encoding="utf-8")).get("first", [])))



def load(call) -> list[Card]:
    points = {p["kp"]: p for p in json.loads((qd.HOME / "points.json").read_text(encoding="utf-8"))}
    nids = call("findNotes", query=f"tag:{qd.TAG}")
    notes = []
    for i in range(0, len(nids), 400):
        notes += call("notesInfo", notes=nids[i:i + 400])
    by_card = {}
    for n in notes:
        tag = {t.split("::")[0]: t.split("::", 1)[1] for t in n["tags"] if "::" in t and t.split("::")[0] in ("kp", "fmt")}
        if tag.get("kp") in points:
            for cid in n["cards"]:
                by_card[cid] = (tag["kp"], tag.get("fmt", "qa"))
    cids = list(by_card)
    info, logs = [], {}
    for i in range(0, len(cids), 300):
        info += call("cardsInfo", cards=cids[i:i + 300])
        logs.update(call("getReviewsOfCards", cards=cids[i:i + 300]))
    out = []
    for c in info:
        if c["queue"] == -1:  # suspended by hand: not ours to plan
            continue
        kp, fmt = by_card[c["cardId"]]
        rows = sorted((r for r in logs.get(str(c["cardId"]), []) if r["type"] != 4 and r["ease"]), key=lambda r: r["id"])
        out.append(Card(kp, fmt, points[kp]["topic"], points[kp]["share"], c["cardId"], c["type"] == 0, c["due"], c["deckName"],
                        [Sight(r["id"], r["ease"], r["time"] / 1000) for r in rows]))
    return out


def prerequisites(model=None) -> dict[str, list[str]]:
    """Point -> the points to learn first. Read from the main plan's model when it is at hand, else from the last copy."""
    f = qd.HOME / "prereq.json"
    if model is None and f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    if model is None:
        import study_plan as sp
        sp.cfg_global.update(sp.config())
        sp.build_inputs(sp.Tree())
        model = sp.kp_state["model"]
    deck = {p["kp"] for p in json.loads((qd.HOME / "points.json").read_text(encoding="utf-8"))}
    pre = {k: [q for q in v if q in deck] for k, v in model.prereq.items() if k in deck}
    pre = {k: v for k, v in pre.items() if v}
    f.write_text(json.dumps(pre, ensure_ascii=False), encoding="utf-8")
    return pre


def plan(call, apply: bool, model=None, now: datetime | None = None) -> dict:
    cfg = settings()
    now = now or datetime.now()
    now_ms = int(now.timestamp() * 1000)
    cards = load(call)
    prereq = prerequisites(model)
    pr, parts = priorities(cards, prereq, now_ms, cfg)
    seq = order(cards, pr, prereq, cfg)

    state_file = qd.HOME / "plan_state.json"
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
    limits = state.get("limits", {})
    today = study_day(now_ms, cfg["rollover_hour"])
    closing = now.hour == (cfg["rollover_hour"] - 1) % 24  # the scheduled run, just before the day turns: today is finished
    target_day = (datetime.strptime(today, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d") if closing else today
    days = {d: v for d, v in history(cards, cfg["rollover_hour"]).items() if d < target_day}
    current = int(state.get("per_day", cfg["per_day"]))
    if state.get("day") == target_day:  # decided already for this day: a second run must not compound it
        n, reason = current, state.get("reason", "")
    else:
        n, reason = quota(days, limits, current, _due(call, cards), len(seq), cfg)
    limits[target_day] = n

    deepen = sorted(parts["miss"], key=lambda k: -parts["miss"][k] * next(c.weight for c in cards if c.kp == k))
    result = {"at": now.isoformat(timespec="minutes"), "day": target_day, "per_day": n, "reason": reason, "unseen": len(seq),
              "seen": parts["n"], "level": round(parts["level"], 3), "tilt": round(parts["tilt"], 2),
              "recent": None if parts["recent"] is None else round(parts["recent"], 3),
              "format": {k: round(v, 3) for k, v in parts["format"].items()},
              "topic": {k: round(v, 3) for k, v in sorted(parts["topic"].items(), key=lambda kv: kv[1])},
              "missed": deepen, "first": [c.kp for c in sorted(seq[:n], key=lambda c: c.due)],  # as Anki deals them
              "why": {c.kp: parts["why"][c.kp] for c in seq[:n]}}
    if apply:
        result["moved"] = deal(call, cards, set(result["first"]))
        conf = call("getDeckConfig", deck=qd.DECK)
        if conf["name"] == qd.DECK and conf["new"]["perDay"] != n:
            conf["new"]["perDay"] = n
            call("saveDeckConfig", config=conf)
        state_file.write_text(json.dumps({"day": target_day, "per_day": n, "reason": reason, "first": result["first"],
                                          "limits": dict(sorted(limits.items())[-60:])}, ensure_ascii=False, indent=1), encoding="utf-8")
        (qd.HOME / "deepen.json").write_text(json.dumps(deepen, ensure_ascii=False), encoding="utf-8")
        with (qd.HOME / "plan_log.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({k: v for k, v in result.items() if k != "why"}, ensure_ascii=False) + "\n")
    return result


def _due(call, cards: list[Card]) -> int:
    """Quick cards that come back within a day, new ones aside."""
    ids = set(call("findCards", query=f"tag:{qd.TAG} -is:new -is:suspended prop:due<=1"))
    return len(ids & {c.cid for c in cards})


def deepen() -> list[str]:
    """The points still missed in the quick deck, the heaviest first: the main plan deals their full cards early."""
    f = qd.HOME / "deepen.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else []


def full_cards(missed: list[str], card_points: dict[str, list[str]], unseen_rank: dict[str, int], limit: int) -> list[str]:
    """For each missed point, the unseen card of the main deck that teaches it most directly, at most `limit` cards.
    `card_points`: card id -> its points, the one it teaches first; `unseen_rank`: the cards that may be dealt -> deck rank."""
    best: dict[str, tuple[int, int, str]] = {}
    for cid, ks in card_points.items():
        if cid in unseen_rank:
            for i, k in enumerate(ks):
                best[k] = min(best.get(k, (i, unseen_rank[cid], cid)), (i, unseen_rank[cid], cid))
    out: list[str] = []
    for k in missed:
        if k in best and best[k][2] not in out:
            out.append(best[k][2])
    return out[:limit]


def line(r: dict) -> str:
    """One line for the daily report."""
    dial = "正合适" if abs(r["tilt"]) < 0.25 else ("偏易，调难" if r["tilt"] > 0 else "偏难，调易")
    recent = "样本不足" if r["recent"] is None else f"{r['recent']:.2f}（{dial}）"
    return f"碎片速刷：明日新卡 {r['per_day']} 张（{r['reason']}）· 近期初见得分 {recent} · 未解决的错题考点 {len(r['missed'])} 个 · 剩 {r['unseen']} 张未见"


def show(r: dict) -> None:
    points = {p["kp"]: p for p in json.loads((qd.HOME / "points.json").read_text(encoding="utf-8"))}
    print(line(r))
    print(f"已见 {r['seen']} 张，整体水平 {r['level']:.2f}，难度旋钮 {r['tilt']:+.2f}")
    print("格式偏差（正 = 你答得比平均好）：" + "  ".join(f"{qd.KIND[k]} {v:+.2f}" for k, v in r["format"].items()))
    topics = list(r["topic"].items())
    title = {p["topic"]: p["topic_title"] for p in points.values()}
    if topics:
        print("最弱专题：" + "；".join(f"{title.get(t, t)} {v:+.2f}" for t, v in topics[:5] if v < 0))
        print("最强专题：" + "；".join(f"{title.get(t, t)} {v:+.2f}" for t, v in topics[::-1][:5] if v > 0))
    if r["missed"]:
        print("未解决的错题考点：" + "；".join(points[k]["title"] for k in r["missed"][:10]))
    print("接下来 15 张：")
    for k in r["first"][:15]:
        w = r["why"][k]
        print(f"  {points[k]['title'][:28]}  [{title.get(points[k]['topic'], '')[:10]}] p={w['p']} need={w['need']} fit={w['fit']} related={w['related']} hold={w['hold']}")
    if "moved" in r:
        print(f"Anki：换牌堆 {r['moved']} 张，每日新卡 {r['per_day']}")


def main() -> int:
    from anki_refresh import call

    apply = "--apply" in sys.argv[1:]
    call("sync")
    show(plan(call, apply))
    if apply:
        call("sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
