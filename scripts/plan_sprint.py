"""A fixed study sprint: a day-by-day curriculum computed from the exam points, and what today deals from it.

The curriculum is stored in sources/local/plan/sprint.json. It is rebuilt on every run before the first day, so it follows the
deck, and frozen from the first day on, so the projection stays comparable with what actually happens.

- Concept cards are picked purely by the exam-point coverage they add (`trellis.plan.coverage_order`), then laid out over the
  days by topic, prerequisites first, so a day has a theme instead of 40 scattered topics.
- Each practice day adds the cards of one representative question, in the order the questions add coverage. The last day is a
  full mock of the next representative question, which is deliberately left unstudied.
- Today's deal is the first `new_per_day` unseen cards of the whole sequence, so whatever was not finished comes first.
- The projection assumes every dealt card is learned that day and every review after it passes on schedule.
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis.hold import MATURE_DAYS  # noqa: E402
from trellis.plan import PointModel, coverage_order  # noqa: E402

FILE = ROOT / "sources/local/plan/sprint.json"
ROLE = {"必讲": 1.0, "追问": 0.6, "加分": 0.3}
QUESTION_CARDS = 16  # of each practice day's new cards, how many come from the day's representative question
GRADUATING, EASE = 1, 2.5  # the deck's first interval and Anki's starting ease


def day_of(sprint_cfg: dict | None, today: date) -> int:
    """1 to `days` during the sprint, 0 before it, -1 after it or when there is none."""
    if not sprint_cfg:
        return -1
    n = (today - date.fromisoformat(sprint_cfg["start"])).days + 1
    if n > int(sprint_cfg["days"]):
        return -1
    return max(n, 0)


def apply(cfg: dict, today: date) -> int:
    """Put the sprint's budgets into `cfg` while it runs. The normal settings return by themselves after the last day."""
    s = cfg.get("sprint")
    n = day_of(s, today)
    if n >= 1:
        cfg.update(daily_new=int(s["new_per_day"]), buffer_days=1, lc_new=int(s.get("lc_new", 0)),
                   review_budget=int(s["review_budget"]), review_only=s.get("review_only", ["系统设计", "LeetCode Tops"]))
    return n


def age_hold(age: int) -> float:
    """Hold of a card `age` days after it was learned, every review on schedule and passed."""
    interval, due = GRADUATING, GRADUATING
    while due <= age:
        interval = math.ceil(interval * EASE)
        due += interval
    return min(1.0, math.log1p(interval) / math.log1p(MATURE_DAYS))


def readiness(pts, q_freq: dict[str, float], held: dict[str, float], skip: set[str]) -> float:
    """How much of an average question's answer is held, drawing a question by how often it is asked."""
    num = den = 0.0
    for q, f in q_freq.items():
        items = [(n["kp"], ROLE.get(n["role"], 0.6)) for n in pts.needs.get(q, [])]
        items += [(o["id"], ROLE.get(o.get("role"), 0.6)) for o in pts.own.get(q, [])]
        z = sum(r for _, r in items)
        if z and f and q not in skip:
            num += f * sum(r * held.get(k, 0.0) for k, r in items) / z
            den += f
    return num / den if den else 0.0


def layout(picked: list[str], cards_by_id: dict, prereqs: dict[str, list[str]], gain: dict[str, float],
           capacity: list[int]) -> list[list[str]]:
    """Lay picked concept cards over the days: prerequisite topics first, then the topics worth most; a leaf stays in order."""
    depth: dict[str, int] = {}

    def level(t, seen=()):
        if t in depth:
            return depth[t]
        if t in seen:
            return 0
        depth[t] = 1 + max((level(p, seen + (t,)) for p in prereqs.get(t, [])), default=-1)
        return depth[t]

    worth: dict[str, float] = defaultdict(float)
    for i in picked:
        worth[cards_by_id[i].topic] += gain[i]
    index = {i: n for n, i in enumerate(picked)}
    ordered = sorted(picked, key=lambda i: (level(cards_by_id[i].topic), -worth[cards_by_id[i].topic], cards_by_id[i].topic,
                                            cards_by_id[i].leaf, cards_by_id[i].order, index[i]))
    days, at = [], 0
    for c in capacity:
        days.append(ordered[at:at + c])
        at += c
    return days


def plain_title(title: str) -> str:
    return re.sub(r"[（(].*", "", title).strip()


def build(cfg: dict, cards: list, mastery: dict[str, float], unseen: set[str], model: PointModel, pts, prereqs: dict[str, list[str]],
          reps: list[dict], q_freq: dict[str, float], title, is_question, skip: set[str], generated: str) -> dict:
    s = cfg["sprint"]
    n_days, per_day = int(s["days"]), int(s["new_per_day"])
    practice = reps[:n_days - 1]
    mock = reps[n_days - 1] if len(reps) >= n_days else None
    concept = [c for c in cards if not is_question(c.topic) and c.id in unseen]
    capacity = [per_day - (QUESTION_CARDS if i < len(practice) else 0) for i in range(n_days)]
    picked, gain = coverage_order(concept, mastery, model, sum(capacity))
    by_id = {c.id: c for c in cards}
    days_concept = layout(picked, by_id, prereqs, gain, capacity)
    days = []
    start = date.fromisoformat(s["start"])
    point_weight = lambda k: model.weight.get(k, 0.0)  # noqa: E731
    used: dict[str, int] = {}  # card -> the day it is dealt
    listed: set[str] = set()  # a point is listed on the first day that teaches it
    for n in range(1, n_days + 1):
        q = practice[n - 1] if n <= len(practice) else None
        q_cards = []
        if q:
            pool = [c for c in cards if c.topic == q["id"] and c.id in unseen]
            q_cards, _ = coverage_order(pool, mastery, model, QUESTION_CARDS)
        ids = days_concept[n - 1] + q_cards
        for i in ids:
            used[i] = n
        topics = Counter(by_id[i].topic for i in days_concept[n - 1])
        points = sorted({by_id[i].point for i in ids if by_id[i].point and point_weight(by_id[i].point) > 0} - listed, key=lambda k: -point_weight(k))
        listed |= set(points)
        held = dict(mastery)
        for i, d in used.items():
            held[i] = max(held.get(i, 0.0), age_hold(n - d))
        point_held = model.mastery(held)
        days.append({"n": n, "date": (start + timedelta(days=n - 1)).isoformat(),
                     "theme": [plain_title(title(t)) for t, _ in topics.most_common(3)],
                     "topics": [{"id": t, "title": title(t), "cards": v} for t, v in topics.most_common()],
                     "points": [pts.meta[k]["title"] for k in points[:8]],
                     "question": {"id": q["id"], "title": q["title"], "mock": False} if q else
                                 ({"id": mock["id"], "title": mock["title"], "mock": True} if mock and n == n_days else None),
                     "cards": ids,
                     "proj_covered": model.coverage(held),
                     "proj_ready": readiness(pts, q_freq, point_held, skip)})
    return {"start": s["start"], "days": n_days, "new_per_day": per_day, "generated": generated, "plan": days,
            "baseline": {"covered": model.coverage(mastery), "ready": readiness(pts, q_freq, model.mastery(mastery), skip)}}


def load() -> dict | None:
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else None


def save(sprint: dict) -> None:
    FILE.write_text(json.dumps(sprint, ensure_ascii=False, indent=0), encoding="utf-8")


def deal_today(sprint: dict, seen: set[str], n: int) -> list[str]:
    """The first `n` cards of the whole sequence not seen yet: what is left of earlier days comes first."""
    return [i for d in sprint["plan"] for i in d["cards"] if i not in seen][:n]


def view(sprint: dict, n: int, history: list[dict], seen: set[str], today: date) -> dict:
    """What the dashboard and the report card show. A day's actual is measured the next morning."""
    by_date = {h["date"]: h for h in history}
    rows, behind = [], 0
    for d in sprint["plan"]:
        after = by_date.get((date.fromisoformat(d["date"]) + timedelta(days=1)).isoformat())
        left = sum(1 for i in d["cards"] if i not in seen)
        if d["n"] < n:
            behind += left
        rows.append({"n": d["n"], "date": d["date"], "theme": d["theme"], "question": d["question"], "cards": len(d["cards"]), "left": left,
                     "proj_covered": d["proj_covered"], "proj_ready": d["proj_ready"],
                     "covered": after.get("held") if after and date.fromisoformat(d["date"]) < today else None,
                     "ready": after.get("ready") if after and date.fromisoformat(d["date"]) < today else None})
    current = sprint["plan"][max(n, 1) - 1]
    return {"n": n, "days": sprint["days"], "start": sprint["start"], "new_per_day": sprint["new_per_day"], "behind": behind, "today": current,
            "baseline": sprint["baseline"], "rows": rows}


def report_html(v: dict, esc) -> str:
    """The sprint block at the top of the Anki report card."""
    d = v["today"]
    q = d["question"]
    out = [f"<p><b>第 {v['n']}/{v['days']} 天</b>：{esc('、'.join(d['theme']))}。</p>"]
    if v["behind"]:
        out.append(f"<p>前几天还剩 {v['behind']} 张没学，今天先发这些。</p>")
    out.append("<p><b>今天的考点</b></p><ul>" + "".join(f"<li>{esc(p)}</li>" for p in d["points"][:6]) + "</ul>")
    if q and q["mock"]:
        out.append(f"<p><b>今天整题模拟：</b>{esc(q['title'])}。计时 60 分钟，不看卡，白板写完再对答案。</p>")
    elif q:
        out.append(f"<p><b>今天练这道题：</b>{esc(q['title'])}。学完今天的卡，先计时 35 分钟自己讲一遍，再翻这道题的卡对答案。</p>")
    return "".join(out)
