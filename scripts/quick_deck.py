"""Quick deck (碎片速刷): one ten-second card per exam point, in tap-and-check formats, for spare minutes without focus.

    uv run python scripts/quick_deck.py select             # rank the points, write the day batches the cards are written from
    uv run python scripts/quick_deck.py gate [d01 ...]     # check written cards: shape, length, one card per point
    uv run python scripts/quick_deck.py show <chunk> ...   # the cards of a chunk as they stand after the verdicts
    uv run python scripts/quick_deck.py pages <dir>        # static pages of each format, for a phone-size render check
    uv run python scripts/quick_deck.py push [--dry-run] [--unverified]   # update what is in Anki, import what never was
    uv run python scripts/quick_deck.py report [days]      # pace, pass rates against the main deck, the points missed
    uv run python scripts/quick_deck.py tap-export         # the self-graded cards (快问, 找错) in chunks, to be rewritten as choice cards
    uv run python scripts/quick_deck.py tap-gate [t01 ...] # check the rewrites (sources/local/quick/tap/t01.jsonl ...)
    uv run python scripts/quick_deck.py tap-accept t01 ... # accept verified chunks; push then applies them

The deck is the breadth pass of the system-design exam points: the heaviest `cards` points, one card each. The day
batches (d01 ...) only divide the writing; what is dealt, in which order and how many a day, is quick_plan.py's. A card tests exactly one point, so a miss names the point to
study in the main deck. Formats are the ones tried in the low-level-design pilot that fit ten seconds: fill-in (cloze),
choice, spot the flaw, question and answer, ordering, matching. Choice and matching only recognise; the main deck holds
the recall cards of the same point.

Since 2026-11-22 the deck is Chi's main way into system design, next to the algorithm deck 算法模式识别, and follows the
same rules (scripts/test_cards.py): the back carries the point's source cards under 原卡 (config `quick.full_back`), and
the cards he graded himself (快问, 找错) are rewritten as choice cards, which are machine-checked. A rewrite stays on
its old note, so the history is kept: the QA note type shows options when its Question field holds them.

Everything written is local (sources/local/quick/): the cards are derived from the system-design deck, part of which
is not public. Agents write cards following research/sysdesign/QUICK_AGENT.md.
"""
from __future__ import annotations

import html
import json
import os
import random
import re
import shutil
import sys
import tempfile
import zlib
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from trellis.build import NOTE_BLOCK, NOTE_FIELDS, note_fields  # noqa: E402

HOME = Path(os.environ.get("QUICK_HOME") or ROOT / "sources/local/quick")
DECK = "4 碎片速刷"  # the number sorts it with the daily decks
PRESET = "碎片速刷"  # its preset kept the old name
TAG = "quick"
FORMATS = ("cloze", "mc", "flaw", "qa", "order", "match", "multi", "bug", "judge", "read")
KIND = {"cloze": "填空", "mc": "选择", "flaw": "找错", "qa": "快问", "order": "排序", "match": "配对", "multi": "多选", "bug": "找错行", "judge": "判断组", "read": "阅读"}
FRONT, TAP_FRONT, BACK, TOTAL, OPT, LINE, SIDE, BLANK = 55, 62, 42, 90, 16, 14, 10, 14  # reading units: a Chinese character 1, an ASCII letter or digit 1/2
MORE = 45  # the extension line under the answer: read only with a few seconds to spare, so outside the ten-second budget
TAPPED = ("mc", "order", "match", "multi", "bug", "judge")
# multi: 4-6 options, every right one must be picked; bug: a short code excerpt, tap the one wrong line (LeetCode Project, 2026-11-16)
MULTI_FRONT, CODE_LINE, CODE_LINES = 80, 44, (4, 10)
SNIP_LINES = 8
JUDGE_ROW = 22  # a judge statement: read and judged in about two seconds
# read: a reading card for the material a project rests on (one workspace file, or one part of it). Not a ten-second
# card: read once to understand, graded "understood or not" (Chi, 2026-11-16: "我对这些题没有概念，不知道前因后果")
READ_BODY, READ_CODE_LINES = 900, 40  # code_q (with the question) and snippet (on the back): scanned, not read, so outside the units  # options are scanned, not read through: a little more room before the answer
CHUNK = 20
DEFAULTS = {"cards": 1000, "per_day": 100, "topic_cap": 6, "source_cards": 2}


def config() -> dict:
    f = ROOT / "sources/local/plan/config.json"
    cfg = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    return {**DEFAULTS, **cfg.get("quick", {}), "family_caps": cfg.get("family_caps", {})}


def day_name(i: int) -> str:
    return f"d{i + 1:02d}"


# ---------------------------------------------------------------- select: which points, in which order


def plain(text: str, limit: int) -> str:
    text = re.sub(r"```(?:svg|mermaid).*?```", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()
    return text[:limit]


def select() -> None:
    import plan_kp
    import study_plan as sp

    cfg = config()
    sp.cfg_global.update(sp.config())
    tree = sp.Tree()
    cards, _titles, _base, _edges = sp.build_inputs(tree)
    pts, weight, model = sp.kp_state["points"], sp.kp_state["weight"], sp.kp_state["model"]
    by_id = {c.id: c for c in cards}
    texts = {c.id: c.render(None) for c in tree.project.cards if c.id in by_id}
    teachers: dict[str, list[str]] = defaultdict(list)  # point -> its cards, the ones teaching it first before the ones touching it
    for cid, ks in pts.card.items():
        for i, k in enumerate(ks):
            teachers[k].append((i, {"必会": 0, "": 1, "追问": 2, "加分": 3}.get(by_id[cid].level, 1), by_id[cid].rank, cid))
    ranked = sorted((k for k in pts.meta if k not in plan_kp.META and teachers.get(k) and tree.top(pts.meta[k]["topic"]) != "s07"),
                    key=lambda k: -weight[k])[: int(cfg["cards"])]
    total = sum(weight[k] for k in pts.meta if k not in plan_kp.META and teachers.get(k))
    chosen = set(ranked)
    family = {t: name for name, f in cfg["family_caps"].items() for t in f["topics"]}
    cap = {name: int(f["max"]) for name, f in cfg["family_caps"].items()}

    days: list[list[str]] = []
    placed: set[str] = set()
    left = list(ranked)
    while left:  # a day takes the heaviest points whose prerequisites are already placed, a few per topic so it stays varied
        day, count, extra = [], Counter(), 0
        while len(day) < min(cfg["per_day"], len(left)):
            grew = False
            for k in left:
                if len(day) >= cfg["per_day"]:
                    break
                group = family.get(pts.meta[k]["topic"], pts.meta[k]["topic"])
                if k in placed or count[group] >= cap.get(group, cfg["topic_cap"] + extra):
                    continue
                if any(p in chosen and p not in placed for p in model.prereq.get(k, [])):
                    continue
                day.append(k)
                placed.add(k)
                count[group] += 1
                grew = True
            if not grew:
                extra += 2  # too few topics left to fill the day under the cap: loosen it
                if extra > cfg["per_day"]:  # only a prerequisite cycle is left: take the points as they come
                    rest = [k for k in left if k not in placed][: cfg["per_day"] - len(day)]
                    day += rest
                    placed.update(rest)
        left = [k for k in left if k not in placed]
        days.append(day)

    used = sp.plan_kp.required_by(pts)
    q_freq = sp.kp_state["q_freq"]
    (HOME / "input" / "chunks").mkdir(parents=True, exist_ok=True)
    points, acc = [], 0.0
    for d, day in enumerate(days):
        rows = []
        for k in day:
            m = pts.meta[k]
            acc += weight[k]
            points.append({"kp": k, "day": day_name(d), "title": m["title"], "kind": m.get("kind", ""), "topic": m["topic"],
                           "topic_title": tree.title(m["topic"]), "share": round(weight[k] / total, 5), "covered": round(acc / total, 4)})
            uses = sorted(used.get(k, []), key=lambda u: -q_freq.get(u[0], 0.0))[:2]
            src = [cid for *_, cid in sorted(teachers[k])[: int(cfg["source_cards"])]]
            rows.append({"kp": k, "title": m["title"], "kind": m.get("kind", ""), "summary": m.get("summary", ""),
                         "topic": tree.title(m["topic"]),
                         "used_by": [{"question": tree.title(q), "role": role, "why": why} for q, role, why in uses],
                         "cards": [{"id": cid, "q": plain(texts[cid][0], 180), "a": plain(texts[cid][1], 420)} for cid in src]})
        (HOME / "input" / f"{day_name(d)}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        for n in range(0, len(rows), CHUNK):  # the same rows in pieces an agent can read in one go
            (HOME / "input" / "chunks" / f"{day_name(d)}-{n // CHUNK + 1}.json").write_text(
                json.dumps(rows[n:n + CHUNK], ensure_ascii=False, indent=1), encoding="utf-8")
    (HOME / "points.json").write_text(json.dumps(points, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(points)} points in {len(days)} days; weight covered by day: "
          + " ".join(f"{day_name(d)} {points[sum(len(x) for x in days[:d + 1]) - 1]['covered']:.0%}" for d in range(len(days))))
    print("kinds:", dict(Counter(p["kind"] for p in points)))


# ---------------------------------------------------------------- cards: load, gate


def units(s: str) -> float:
    s = re.sub(r"\{\{c1::(.*?)\}\}", r"\1", s)
    s = re.sub(r"<[^>]+>|\*\*|`", "", s)
    return len(re.findall(r"[㐀-鿿]", s)) + len(re.findall(r"[A-Za-z0-9%$]", s)) / 2


def sides(c: dict) -> tuple[list[str], list[str]]:
    """What is read before the answer shows, and after."""
    f = c.get("fmt")
    if f == "cloze":
        return [c.get("text", "")], [c.get("why", "")]
    if f in ("mc", "multi"):
        return [c.get("q", ""), *c.get("opts", [])], [c.get("why", "")]
    if f == "judge":
        return [c.get("q", ""), *[r[0] for r in c.get("rows", []) if isinstance(r, list) and r]], [c.get("why", "")]
    if f == "read":
        return [c.get("title", "")], [c.get("key", "")]
    if f == "order":
        return [c.get("q", ""), *c.get("lines", []), *c.get("decoys", [])], [c.get("why", "")]
    if f == "bug":
        return [c.get("q", "")], [c.get("fix", ""), c.get("why", "")]  # code is scanned, not read: outside the units
    if f == "order":
        return [c.get("q", ""), *c.get("lines", [])], [c.get("why", "")]
    if f == "match":
        return [c.get("q", ""), *[x for p in c.get("pairs", []) for x in p]], [c.get("why", "")]
    return [c.get("q", "")], [c.get("a", ""), c.get("why", "")]


def check(c: dict, known: dict[str, dict]) -> list[str]:
    bad = []
    f, kp = c.get("fmt"), c.get("kp")
    if kp not in known:
        return [f"unknown point {kp}"]
    if f not in FORMATS:
        return [f"unknown format {f}"]
    ids = {x["id"] for x in known[kp]["cards"]}
    if not c.get("based_on") or not set(c["based_on"]) <= ids:
        bad.append("based_on must name the point's source cards")
    front, back = sides(c)
    if any(not isinstance(x, str) or not x.strip() for x in front) or (f in ("qa", "flaw") and not c.get("a", "").strip()):
        bad.append("an empty field")
        return bad
    if f not in ("qa", "flaw", "read") and not c.get("why", "").strip():
        bad.append("why is empty")
    if f == "read":
        body = c.get("body", "")
        prose = re.sub(r"```.*?```", "", body, flags=re.S)
        code = [l for b in re.findall(r"```[^\n]*\n(.*?)```", body, flags=re.S) for l in b.splitlines()]
        if not c.get("title", "").strip() or not body.strip() or not c.get("key", "").strip():
            bad.append("read needs title, body and key")
        if units(prose) > READ_BODY:
            bad.append(f"read body prose {units(prose):.0f} > {READ_BODY}")
        if len(code) > READ_CODE_LINES:
            bad.append(f"read code {len(code)} lines > {READ_CODE_LINES}")
        if units(c.get("key", "")) > 60:
            bad.append("read key over 60")
        return bad
    uf, ub = sum(units(x) for x in front), sum(units(x) for x in back)
    limit = MULTI_FRONT if f in ("multi", "judge") else TAP_FRONT if f in TAPPED else FRONT
    if uf > limit:
        bad.append(f"front {uf:.0f} > {limit}")
    if ub > BACK:
        bad.append(f"back {ub:.0f} > {BACK}")
    if uf + ub > TOTAL:
        bad.append(f"whole card {uf + ub:.0f} > {TOTAL}")
    if f == "cloze":
        blanks = re.findall(r"\{\{c1::(.*?)\}\}", c["text"])
        if len(blanks) != 1 or "{{c2" in c["text"]:
            bad.append("exactly one {{c1::…}}")
        elif not blanks[0].strip() or units(blanks[0]) > BLANK or "::" in blanks[0]:
            bad.append(f"blank must be 1..{BLANK} units, no hint")
        elif units(c["text"]) - units(blanks[0]) < 8:
            bad.append("too little context around the blank")
    if f == "mc":
        o = c["opts"]
        if not 2 <= len(o) <= 3 or len(set(o)) != len(o):
            bad.append("2 or 3 distinct options, the right one first")
        if any(units(x) > OPT for x in o):
            bad.append(f"an option over {OPT}")
        if any(re.search(r"以上|都对|都不|皆", x) for x in o):
            bad.append("no all-of-the-above option")
        if o and max(units(x) for x in o) > 0 and units(o[0]) > 1.6 * max(units(x) for x in o[1:]) + 2:
            bad.append("the right option is much longer than the others")
    if f == "multi":
        o, ok = c["opts"], c.get("ok", [])
        if not 4 <= len(o) <= 6 or len(set(o)) != len(o):
            bad.append("4 to 6 distinct options")
        if not ok or len(set(ok)) != len(ok) or not all(isinstance(i, int) and 0 <= i < len(o) for i in ok) or len(ok) == len(o):
            bad.append("ok lists the right options' indices: at least one, not all")
        if any(units(x) > OPT for x in o):
            bad.append(f"an option over {OPT}")
        if any(re.search(r"以上|都对|都不|皆", x) for x in o):
            bad.append("no all-of-the-above option")
    if f == "judge":
        r = c.get("rows", [])
        if not 3 <= len(r) <= 5 or any(not (isinstance(x, list) and len(x) in (2, 3) and isinstance(x[0], str) and isinstance(x[1], bool)) for x in r):
            bad.append("3 to 5 rows [statement, true/false, optional reason]")
        elif any(units(x[0]) > JUDGE_ROW for x in r) or len({x[0] for x in r}) != len(r):
            bad.append(f"distinct statements of at most {JUDGE_ROW}")
        elif all(x[1] for x in r) or not any(x[1] for x in r):
            bad.append("mix true and false rows")
        elif any(not x[1] and (len(x) < 3 or not x[2].strip()) for x in r):
            bad.append("every false row carries its one-line reason")
    if f == "order" and c.get("decoys"):
        d = c["decoys"]
        if not isinstance(d, list) or not 1 <= len(d) <= 2 or any(units(x) > LINE for x in d) or set(d) & set(c.get("lines", [])):
            bad.append(f"1 or 2 decoys of at most {LINE}, none equal to a line")
    if f == "bug":
        code, i = c.get("code", []), c.get("bad")
        if not CODE_LINES[0] <= len(code) <= CODE_LINES[1] or any(not isinstance(x, str) or len(x) > CODE_LINE for x in code):
            bad.append(f"{CODE_LINES[0]}..{CODE_LINES[1]} code lines of at most {CODE_LINE} characters")
        elif not isinstance(i, int) or not 0 <= i < len(code) or not code[i].strip():
            bad.append("bad is the index of the one wrong, non-empty line")
        if not c.get("fix", "").strip():
            bad.append("fix (the corrected line) is empty")
    if f == "order":
        n = c["lines"]
        if not 3 <= len(n) <= 4 or len(set(n)) != len(n) or any(units(x) > LINE for x in n):
            bad.append(f"3 or 4 distinct lines of at most {LINE}")
    if f == "match":
        p = c["pairs"]
        if len(p) != 3 or any(len(x) != 2 for x in p) or len({x[0] for x in p}) != 3 or len({x[1] for x in p}) != 3:
            bad.append("3 pairs, all sides distinct")
        elif any(units(x) > SIDE for pair in p for x in pair):
            bad.append(f"a side over {SIDE}")
    for name in ("code_q", "snippet"):
        if name in c:
            code = c[name]
            if not isinstance(code, list) or not 1 <= len(code) <= SNIP_LINES or any(not isinstance(x, str) or len(x) > CODE_LINE for x in code):
                bad.append(f"{name}: 1..{SNIP_LINES} code lines of at most {CODE_LINE} characters")
    if "code_q" in c and f not in ("mc", "multi", "qa", "flaw"):
        bad.append("code_q only on mc, multi, qa or flaw")
    text = " ".join(front + back)
    if re.search(r"见上|如上|本卡|原文|上文|来源卡", text):
        bad.append("leans on something outside the card")
    return bad


def check_more(more, c: dict) -> list[str]:
    if not isinstance(more, str) or not more.strip():
        return ["more is empty"]
    bad = []
    if units(more) > MORE:
        bad.append(f"more {units(more):.0f} > {MORE}")
    if "\n" in more.strip() or re.search(r"见上|如上|本卡|原文|上文|来源卡", more):
        bad.append("more is one self-contained sentence")
    if more.strip() in (c.get("why", "").strip(), c.get("a", "").strip()):
        bad.append("more repeats the answer")
    return bad


def load_more(day: str, verified_only: bool) -> tuple[dict[str, str], list[str]]:
    """Extension lines written after the cards (more/<chunk>.jsonl), after their own verdicts (morev/<chunk>.jsonl)."""
    rows, bad = day_rows("more", day)
    vrows, vbad = day_rows("morev", day)
    verdicts = {v.get("kp"): v for v in vrows}
    out = {}
    for r in rows:
        v = verdicts.get(r.get("kp"), {})
        if v.get("verdict") == "drop" or (verified_only and v.get("verdict") not in ("ok", "fix")):
            continue
        out[r.get("kp")] = v.get("more") if v.get("verdict") == "fix" and v.get("more") else r.get("more")
    return out, bad + vbad


def load_inputs() -> dict[str, dict[str, dict]]:
    return {f.stem: {r["kp"]: r for r in json.loads(f.read_text(encoding="utf-8"))} for f in sorted((HOME / "input").glob("d*.json"))}


def read_rows(path: Path) -> tuple[list[dict], list[str]]:
    rows, bad = [], []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            bad.append(f"{path.name}:{n}: {e}")
    return rows, bad


def day_rows(folder: str, day: str) -> tuple[list[dict], list[str]]:
    """A day's rows: one file for the day, or one per chunk (d01.jsonl, d01-1.jsonl ...)."""
    rows, bad = [], []
    for f in sorted((HOME / folder).glob(f"{day}*.jsonl")):
        r, b = read_rows(f)
        rows += r
        bad += b
    return rows, bad


def load_cards(day: str, known: dict[str, dict], verified_only: bool) -> tuple[list[dict], list[str]]:
    """The day's cards after the verifier's verdicts: a fix replaces the card, a drop removes it."""
    rows, problems = day_rows("cards", day)
    vrows, vbad = day_rows("verify", day)
    problems += vbad
    verdicts = {v.get("kp"): v for v in vrows}
    if rows and verified_only and not verdicts:
        return [], [f"{day}: not verified yet"]
    later, more_bad = load_more(day, verified_only)
    problems += more_bad
    cards, seen = [], set()
    for c in rows:
        kp = c.get("kp")
        if c.get("skip"):
            continue
        v = verdicts.get(kp, {})
        if v.get("verdict") == "drop":
            continue
        if v.get("verdict") == "fix" and v.get("card"):
            c = {**v["card"], "kp": kp, "based_on": v["card"].get("based_on") or c.get("based_on")}
        elif v.get("more"):  # the card stands, only its extension line is replaced
            c = {**c, "more": v["more"]}
        if verified_only and v.get("verdict") not in ("ok", "fix"):
            problems.append(f"{day} {kp}: no verdict")
            continue
        errs = check(c, known)
        if "more" in c:
            errs += check_more(c["more"], c)
        elif kp in later:
            late = check_more(later[kp], c)
            if late:
                problems.append(f"{day} {kp} [more]: " + "; ".join(late))
            else:
                c = {**c, "more": later[kp]}
        if kp in seen:
            errs.append("a second card for the point")
        if errs:
            problems.append(f"{day} {kp} [{c.get('fmt')}]: " + "; ".join(errs))
            continue
        seen.add(kp)
        cards.append(c)
    return cards, problems


def gate(days: list[str]) -> int:
    inputs = load_inputs()
    failed = 0
    mix = Counter()
    seen_cards: list[dict] = []
    for day in days or sorted(inputs):
        rows, _ = day_rows("cards", day)
        if not rows:
            continue
        cards, problems = load_cards(day, inputs[day], verified_only=False)
        skipped = {r["kp"] for r in rows if r.get("skip")}
        dropped = {v["kp"] for v in day_rows("verify", day)[0] if v.get("verdict") == "drop"}
        written = {r.get("kp") for r in rows}
        missing = set(inputs[day]) - written
        day_mix = Counter(c["fmt"] for c in cards)
        mix.update(day_mix)
        seen_cards += cards
        bare = sum(1 for c in cards if not c.get("more"))
        print(f"{day}: {len(cards)} ok, {len(problems)} failing, {len(skipped)} skipped, {len(dropped)} dropped, {len(missing)} not written"
              + (f", {bare} without more" if bare else "") + "  " + " ".join(f"{f} {day_mix[f]}" for f in FORMATS if day_mix[f]))
        for p in problems:
            print("  ", p)
        if 0 < len(missing) <= 20:
            print("   not written:", " ".join(sorted(missing)))
        failed += len(problems)
    if mix:
        n = sum(mix.values())
        print("mix: " + " ".join(f"{f} {mix[f] / n:.0%}" for f in FORMATS))
        print(choice_tell(seen_cards))
    return 1 if failed else 0


def choice_tell(cards: list[dict]) -> str:
    """How often the right option of a choice card is the longest: with three options, chance is a third."""
    import test_cards
    mc = [c for c in cards if c.get("fmt") == "mc" and len(c.get("opts", [])) > 1]
    far, longest = test_cards.length_tell([([units(o) for o in c["opts"]], 0) for c in mc])
    return f"choice cards: the right option is the longest in {longest} of {len(mc)} ({100 * longest // max(1, len(mc))}%; aim for at most 40%)"


def show(chunks: list[str]) -> None:
    """The cards of the given chunks as they stand after the verdicts, one JSON line each: what an extension line is written for."""
    inputs = load_inputs()
    for chunk in chunks:
        day = chunk.split("-")[0]
        kps = [r["kp"] for r in json.loads((HOME / "input" / "chunks" / f"{chunk}.json").read_text(encoding="utf-8"))]
        cards = {c["kp"]: c for c in load_cards(day, inputs[day], verified_only=False)[0]}
        for kp in kps:
            if kp in cards:
                print(json.dumps({k: v for k, v in cards[kp].items() if k != "based_on"}, ensure_ascii=False))


# ---------------------------------------------------------------- note types

QUICK_CSS = """
/* ---- quick deck ---- */
.chip { display:inline-block; margin-left:8px; padding:0 7px; border-radius:4px; background:var(--chip); color:var(--accent); font-size:11px; letter-spacing:.04em; }
.q { font-size:1.08em; font-weight:600; line-height:1.5; margin-bottom:14px; }
.a { font-weight:600; margin-bottom:8px; }
.why { color:var(--dim); font-size:.94em; }
.pt { margin-top:18px; padding-top:8px; border-top:1px solid var(--rule); font-size:12px; color:var(--dim); }
.mine { font-size:14px; font-weight:600; margin-bottom:8px; min-height:1em; }
.q .opts { font-size:0.926em; font-weight:400; line-height:1.6; margin-top:14px; }  /* a choice card hosted by a QA note */
.q + .mine:empty { display:none; }
.mine.good { color:#2e9e5b; } .mine.miss { color:#c0392b; }
.opts, .pool { display:flex; flex-direction:column; gap:8px; margin:6px 0; }
.opt, .pl, .mit { display:flex; gap:10px; align-items:center; min-height:44px; padding:8px 12px; border:1px solid var(--rule); border-radius:8px; cursor:pointer; -webkit-tap-highlight-color:transparent; -webkit-user-select:none; user-select:none; -webkit-touch-callout:none; }
.opt > *, .pl > *, .mit > * { pointer-events:none; }
.opt .k, .pl .n, .mit .badge { flex:0 0 auto; width:22px; height:22px; border-radius:50%; border:1px solid var(--rule); text-align:center; font-size:12px; line-height:21px; color:var(--dim); }
.opt .body, .pl .body, .mit .body { flex:1 1 auto; min-width:0; overflow-wrap:anywhere; }
.opt.sel, .pl.sel, .mit.active { border-color:var(--accent); background:var(--chip); }
.opt.sel .k, .pl.sel .n { background:var(--accent); color:var(--paper); border-color:var(--accent); }
.opt.ok { border-color:#2e9e5b; } .opt.ok .k { background:#2e9e5b; color:#fff; border-color:#2e9e5b; }
.opt.bad { opacity:.55; } .opt.bad.sel { opacity:1; border-color:#c0392b; background:none; } .opt.bad.sel .k { background:#c0392b; color:#fff; border-color:#c0392b; }
.pl.ok, .mit.ok { border-color:#2e9e5b; background:none; } .pl.ok .n { background:#2e9e5b; color:#fff; border-color:#2e9e5b; }
.pl.bad, .mit.bad { border-color:#c0392b; background:none; } .pl.bad .n { background:#c0392b; color:#fff; border-color:#c0392b; }
.more { margin-top:10px; padding-top:8px; border-top:1px dashed var(--rule); font-size:.94em; }
.more:first-child { margin-top:0; padding-top:0; border-top:none; }
.more b { display:inline-block; margin-right:8px; padding:0 6px; border-radius:4px; background:var(--chip); color:var(--accent); font-size:11px; font-weight:600; letter-spacing:.04em; }
.mcols { display:flex; gap:8px; } .mcols > div { flex:1 1 0; min-width:0; display:flex; flex-direction:column; gap:8px; }
.mit { padding:8px 8px; gap:6px; font-size:.94em; }
.mit.paired .badge { color:#fff; }
.c1 .badge { background:#3b6fd4; border-color:#3b6fd4; } .c2 .badge { background:#b76b01; border-color:#b76b01; } .c3 .badge { background:#8e44ad; border-color:#8e44ad; }
ol.steps { margin:0 0 10px; padding-left:1.4em; } ol.steps li { margin-bottom:.3em; }
table.sol { margin:0 0 10px; } table.sol td { border:none; border-bottom:1px solid var(--rule); padding:5px 8px 5px 0; }
.hint { font-weight:400; font-size:.86em; color:var(--dim); margin-left:4px; }
button.go { margin:4px 0 2px; padding:8px 22px; border-radius:8px; border:1px solid var(--accent); background:var(--chip); color:var(--accent); font-size:15px; font-weight:600; }
.code { margin:6px 0; border:1px solid var(--rule); border-radius:8px; overflow-x:auto; padding:4px 0; }
.cl { display:flex; gap:8px; align-items:baseline; padding:3px 10px; white-space:pre; cursor:pointer; -webkit-tap-highlight-color:transparent; -webkit-user-select:none; user-select:none; }
.cl > * { pointer-events:none; } .cl code { background:none; padding:0; white-space:pre; font-size:13px; }
.cl .ln { flex:0 0 auto; width:18px; text-align:right; color:var(--dim); font-size:11px; }
.cl.sel { background:rgba(192,57,43,.14); } .cl.ok { background:rgba(46,158,91,.18); }
button.idk { margin:6px 8px 2px 0; padding:6px 14px; border-radius:8px; border:1px solid var(--rule); background:none; color:var(--dim); font-size:13px; }
.jrows { display:flex; flex-direction:column; gap:8px; margin:6px 0; }
.jr { display:flex; gap:8px; align-items:center; padding:6px 8px 6px 12px; border:1px solid var(--rule); border-radius:8px; }
.jr .body { flex:1 1 auto; min-width:0; overflow-wrap:anywhere; }
.jb { flex:0 0 auto; width:40px; height:40px; line-height:40px; text-align:center; border:1px solid var(--rule); border-radius:8px; font-size:17px; cursor:pointer; -webkit-tap-highlight-color:transparent; -webkit-user-select:none; user-select:none; }
.jb.sel { border-color:var(--accent); background:var(--chip); color:var(--accent); }
.jr.ok { border-color:#2e9e5b; } .jr.bad { border-color:#c0392b; }
ol.jsol { margin:0 0 10px; padding-left:1.4em; } ol.jsol li { margin-bottom:.35em; } ol.jsol li.bad { color:#c0392b; }
.jwhy { display:block; color:var(--dim); font-size:.9em; }
.rbody { line-height:1.6; } .rbody pre { overflow-x:auto; white-space:pre; } .rbody pre code { white-space:pre; }
.rbody h3, .rbody h4 { margin:12px 0 4px; font-size:1em; }
pre.snip { margin:8px 0 4px; padding:6px 10px; border:1px solid var(--rule); border-radius:6px; overflow-x:auto; white-space:pre; font-size:12.5px; line-height:1.45; }
pre.snip code { background:none; padding:0; white-space:pre; }
"""

HEAD = '<div class="crumb">{{Crumb}}<span class="chip">%s</span></div>'
TAIL = ('{{#Why}}<div class="why">{{Why}}</div>{{/Why}}<div class="pt">考点：{{Point}}</div>' + NOTE_BLOCK +
        '<div class="grade" id="grade">答对 Good · 答错或猜的 Again</div>')

# Script shared by the tapped formats. Three things it has to get right on a phone:
# - AnkiMobile shows the answer on any tap unless the element tapped is a link or button, has an onclick handler, or carries
#   the class `tappable` (its manual, "JavaScript"). The options carry both, and their children take no pointer events, so
#   the element tapped is always the option itself. Once the card is answered they give both up: the next tap anywhere flips.
# - The answer is marked on the front at once, then the card turns itself where the client lets a script do that (desktop,
#   AnkiDroid, and AnkiMobile's unofficial tap message). Where it does not, the usual tap does. A turn must never fire on
#   the answer side, where the same tap would grade the card, so it checks that the front it belongs to is still shown.
# - The pick reaches the back through sessionStorage, and through a global for clients that keep one page per card pair.
FLIP_MS = (450, 1100)  # right, wrong: time to see the mark before the card turns
CLEAR = 'try{sessionStorage.removeItem("qk")}catch(e){}window._qk=null;window._qkT=(window._qkT||0)+1;'
TOOLS = ('function keep(v){window._qk=v;try{sessionStorage.setItem("qk",v)}catch(e){}}'
         # released a moment later: a client that reads the class after the tap's own handler ran must still see the tap as taken
         'function free(el){setTimeout(function(){el.classList.remove("tappable");el.onclick=null;el.removeAttribute("onclick")},300)}'
         'function arm(list,fn){for(var i=0;i<list.length;i++){list[i].classList.add("tappable");list[i].onclick=function(){fn(this)}}}'
         'function say(ok,t){var e=document.getElementById("fb");e.textContent=(ok?"✓ 答对":"✗ 答错")+(t||"");e.className="mine "+(ok?"good":"miss")}'
         'function flip(ok){var t=window._qkT;setTimeout(function(){'
         'if(window._qkT!==t||document.getElementById("answer")||!document.body.contains(root)){return}'
         'try{if(typeof pycmd!=="undefined"){pycmd("ans");return}}catch(e){}'
         'try{if(typeof showAnswer==="function"){showAnswer();return}}catch(e){}'
         'try{if(window.anki&&window.sendMessage2){window.sendMessage2("ankitap","midCenter")}}catch(e){}'
         '},ok?%d:%d)}' % FLIP_MS)
NO_FLIP = 'function flip(ok){}'
SAVED = ('window._qkT=(window._qkT||0)+1;var m=null;try{m=sessionStorage.getItem("qk")}catch(e){}'
         'if(m===null&&typeof window._qk==="string"){m=window._qk}'
         'var t=document.querySelectorAll(".tappable");for(var i=0;i<t.length;i++){t[i].classList.remove("tappable");t[i].onclick=null;t[i].removeAttribute("onclick")}')
SHOW = ('if(m==="?"){ok=false;miss="：不会"}'
        'if(m){var e=document.getElementById("mine"),g=document.getElementById("grade");e.textContent=ok?"✓ 答对":"✗ 答错"+miss;'
        'e.className="mine "+(ok?"good":"miss");if(g){g.textContent=ok?"答对 → Good（蒙对的按 Again）":"答错 → Again"}}')
FB = '<div class="mine" id="fb"></div>'
IDK = '<button class="idk" onclick="qkIdk()">不会</button>'
# a tap on 不会 ends the card as a miss; the back reads "?" and says Again
IDK_JS = ('function idk(){if(done){return}done=true;var t=document.querySelectorAll(".tappable");for(var i=0;i<t.length;i++){free(t[i])}'
          'keep("?");say(false," · 不会，看答案");flip(false)}window.qkIdk=idk;')

# A QA note can host a choice card: the options sit inside its Question field as <div class="opts" id="opts" data-c="B">,
# and these scripts wake up only when that element is there. A self-graded card rewritten as a tap card keeps its note,
# and with it its history; changing a note's type would force a one-way full sync (Chi, 2026-11-22: 自评卡全部改成点选).
QA_Q = (HEAD % "{{Kind}}" + '<div class="q">{{Question}}</div><div id="qkx" style="display:none">' + IDK + FB + '</div>'
        '<script>(function(){var root=document.getElementById("opts");if(!root){return}'
        'var c=root.getAttribute("data-c"),o=root.querySelectorAll(".opt"),done=false;document.getElementById("qkx").style.display="";' + TOOLS +
        'function tap(el){if(done){return}done=true;var k=el.getAttribute("data-k");'
        'for(var i=0;i<o.length;i++){var x=o[i].getAttribute("data-k");o[i].classList.add(x===c?"ok":"bad");if(x===k){o[i].classList.add("sel")}free(o[i])}'
        'keep(k);say(k===c,k===c?"":"，正确是 "+c);flip(k===c)}'
        + CLEAR + IDK_JS + 'window.qkTap=tap;arm(o,tap)})();</script>')
QA_A = (HEAD % "{{Kind}}" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><hr id="answer"><div class="a">{{Answer}}</div>' + TAIL +
        '<script>(function(){var root=document.getElementById("opts");if(!root){return}var c=root.getAttribute("data-c");var o=root.querySelectorAll(".opt");' + SAVED +
        'for(var i=0;i<o.length;i++){var k=o[i].getAttribute("data-k");o[i].classList.add(k===c?"ok":"bad");if(k===m){o[i].classList.add("sel")}}'
        'var ok=m===c,miss="：你选了 "+m;' + SHOW + '})();</script>')
CLOZE_Q = HEAD % "填空" + '<div class="q">{{cloze:Text}}</div>'
CLOZE_A = CLOZE_Q + '<hr id="answer">' + TAIL

MC_Q = (HEAD % "选择" + '<div class="q">{{Question}}</div><div class="opts" id="opts">{{Opts}}</div>' + IDK + FB +
        '<script>(function(){var c="{{Correct}}",root=document.getElementById("opts"),o=root.querySelectorAll(".opt"),done=false;' + TOOLS +
        'function tap(el){if(done){return}done=true;var k=el.getAttribute("data-k");'
        'for(var i=0;i<o.length;i++){var x=o[i].getAttribute("data-k");o[i].classList.add(x===c?"ok":"bad");if(x===k){o[i].classList.add("sel")}free(o[i])}'
        'keep(k);say(k===c,k===c?"":"，正确是 "+c);flip(k===c)}'
        + CLEAR + IDK_JS + 'window.qkTap=tap;arm(o,tap)})();</script>')
MC_A = (HEAD % "选择" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><div class="opts" id="opts">{{Opts}}</div>'
        '<hr id="answer"><div class="a">{{Answer}}</div>' + TAIL +
        '<script>(function(){var c="{{Correct}}";var o=document.querySelectorAll("#opts .opt");' + SAVED +
        'for(var i=0;i<o.length;i++){var k=o[i].getAttribute("data-k");o[i].classList.add(k===c?"ok":"bad");if(k===m){o[i].classList.add("sel")}}'
        'var ok=m===c,miss="：你选了 "+m;' + SHOW + '})();</script>')

ORDER_Q = (HEAD % "排序" + '<div class="q">{{Question}}</div><div class="pool" id="pool">{{Lines}}</div>' + IDK + FB +
           '<script>(function(){var root=document.getElementById("pool"),L=root.querySelectorAll(".pl"),seq=[],done=false;'
           # n real steps; rows whose data-i starts with x are decoys that belong in no position
           'var N=+(root.querySelector(".pl[data-n]")||{getAttribute:function(){return L.length}}).getAttribute("data-n")||L.length,decoy=N<L.length;' + TOOLS +
           'function draw(){for(var i=0;i<L.length;i++){var p=seq.indexOf(L[i].getAttribute("data-i"));'
           'L[i].querySelector(".n").textContent=p<0?"":(p+1);L[i].classList.toggle("sel",p>=0)}}'
           'function finish(){done=true;var ok=true,d=0;for(var i=0;i<L.length;i++){var k=L[i].getAttribute("data-i"),p=seq.indexOf(k),x=k.charAt(0)==="x";'
           'var good=x?p<0:p===+k;if(!x){d+=p<0?9:Math.abs(p-(+k))}else if(p>=0){d+=9}'
           'L[i].classList.add(good?"ok":"bad");if(!good){ok=false}free(L[i])}keep(seq.join(","));'
           'say(ok,ok?"":(d===2?"，一处相邻颠倒（Hard）":"，翻面看顺序"));flip(ok)}'
           # the last line has only one place left, so it is filled in: one tap fewer
           'function tap(el){if(done){return}var k=el.getAttribute("data-i"),p=seq.indexOf(k);if(p<0){seq.push(k)}else{seq.splice(p)}'
           'if(!decoy&&seq.length===N-1){for(var i=0;i<L.length;i++){var x=L[i].getAttribute("data-i");if(seq.indexOf(x)<0){seq.push(x);break}}}'
           'draw();if(seq.length===N){finish()}}'
           + CLEAR + IDK_JS + 'window.qkTap=tap;arm(L,tap)})();</script>')
ORDER_A = (HEAD % "排序" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><hr id="answer">{{Solution}}' + TAIL +
           '<script>(function(){var n=document.querySelectorAll("ol.steps li").length;' + SAVED +
           'var want=[];for(var i=0;i<n;i++){want.push(i)}var got=m&&m!=="?"?m.split(","):[],d=0;'
           'for(var i=0;i<n;i++){var p=got.indexOf(String(i));d+=p<0?9:Math.abs(p-i)}for(var j=0;j<got.length;j++){if(got[j].charAt(0)==="x"){d+=9}}'
           'var ok=d===0,miss=m==="?"?"：不会":(d===2?"：一处相邻颠倒":"");' + SHOW +
           'var g=document.getElementById("grade");if(g&&m&&d===2){g.textContent="一处相邻颠倒 → Hard"}})();</script>')

MATCH_Q = (HEAD % "配对" + '<div class="q">{{Question}}</div><div class="mcols" id="mcols"><div id="ml">{{Left}}</div><div id="mr">{{Right}}</div></div>' + FB +
           '<script>(function(){var root=document.getElementById("mcols"),L=root.querySelectorAll("#ml .mit"),R=root.querySelectorAll("#mr .mit");'
           'var pair={},act=null,done=false;' + TOOLS +
           'function at(list,i){for(var j=0;j<list.length;j++){if(list[j].getAttribute("data-i")===i){return list[j]}}}'
           'function count(){var n=0;for(var l in pair){n++}return n}'
           'function next(){act=null;for(var j=0;j<L.length;j++){var i=L[j].getAttribute("data-i");if(!(i in pair)){act=i;return}}}'
           'function mark(el,cls,t){el.className="mit tappable"+cls;el.querySelector(".badge").textContent=t}'
           'function draw(){var j;for(j=0;j<L.length;j++){mark(L[j],"","")}for(j=0;j<R.length;j++){mark(R[j],"","")}'
           'var n=0;for(var l in pair){n++;mark(at(L,l)," paired c"+n,n);mark(at(R,pair[l])," paired c"+n,n)}'
           'if(act!==null){at(L,act).classList.add("active")}}'
           'function finish(){done=true;var good=0,n=0,s=[];for(var l in pair){n++;var ok=pair[l]===l;if(ok){good++}s.push(l+pair[l]);'
           'at(L,l).classList.add(ok?"ok":"bad");at(R,pair[l]).classList.add(ok?"ok":"bad")}'
           'for(var j=0;j<L.length;j++){free(L[j]);free(R[j])}keep(s.join(","));say(good===n,good===n?"":"：对了 "+good+"/"+n);flip(good===n)}'
           'function tap(el){if(done){return}var i=el.getAttribute("data-i");'
           'if(el.parentNode.id==="ml"){delete pair[i];act=i;draw();return}'
           'for(var l in pair){if(pair[l]===i){delete pair[l]}}if(act===null){next()}if(act!==null){pair[act]=i;next()}'
           # the last pair has only one side left each, so it is filled in
           'if(count()===L.length-1&&act!==null){var used={};for(var q in pair){used[pair[q]]=1}'
           'for(var j=0;j<R.length;j++){var r=R[j].getAttribute("data-i");if(!used[r]){pair[act]=r;break}}act=null}'
           'draw();if(count()===L.length){finish()}}'
           + CLEAR + 'window.qkTap=tap;next();draw();arm(L,tap);arm(R,tap)})();</script>')
MATCH_A = (HEAD % "配对" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><hr id="answer">{{Solution}}' + TAIL +
           '<script>(function(){var n=document.querySelectorAll("table.sol tr").length;' + SAVED +
           'var good=0,ps=m?m.split(","):[];for(var i=0;i<ps.length;i++){if(ps[i].charAt(0)===ps[i].charAt(1)){good++}}'
           'var ok=good===n,miss="：对了 "+good+"/"+n;' + SHOW + '})();</script>')


MULTI_Q = (HEAD % "多选" + '<div class="q">{{Question}}<span class="hint">（选出所有对的）</span></div><div class="opts" id="opts">{{Opts}}</div>'
           '<button class="go" id="go" onclick="qkGo()">确定</button>' + IDK + FB +
           '<script>(function(){var c="{{Correct}}",root=document.getElementById("opts"),o=root.querySelectorAll(".opt"),pick={},done=false;' + TOOLS +
           'function tap(el){if(done){return}var k=el.getAttribute("data-k");if(pick[k]){delete pick[k];el.classList.remove("sel")}else{pick[k]=1;el.classList.add("sel")}}'
           'function go(){if(done){return}done=true;var s="";for(var i=0;i<o.length;i++){var x=o[i].getAttribute("data-k");'
           'o[i].classList.add(c.indexOf(x)>=0?"ok":"bad");if(pick[x]){s+=x}free(o[i])}'
           'var b=document.getElementById("go");b.style.display="none";keep(s);say(s===c,s===c?"":"，正确是 "+c);flip(s===c)}'
           + CLEAR + IDK_JS + 'window.qkTap=tap;window.qkGo=go;arm(o,tap)})();</script>')
MULTI_A = (HEAD % "多选" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><div class="opts" id="opts">{{Opts}}</div>'
           '<hr id="answer"><div class="a">{{Answer}}</div>' + TAIL +
           '<script>(function(){var c="{{Correct}}";var o=document.querySelectorAll("#opts .opt");' + SAVED +
           'for(var i=0;i<o.length;i++){var k=o[i].getAttribute("data-k");o[i].classList.add(c.indexOf(k)>=0?"ok":"bad");if(m&&m.indexOf(k)>=0){o[i].classList.add("sel")}}'
           'var ok=m===c,miss="：你选了 "+(m||"（无）");' + SHOW + '})();</script>')

BUG_Q = (HEAD % "找错行" + '<div class="q">{{Question}}</div><div class="code" id="opts">{{Lines}}</div>' + IDK + FB +
         '<script>(function(){var c="{{Correct}}",root=document.getElementById("opts"),o=root.querySelectorAll(".cl"),done=false;' + TOOLS +
         'function tap(el){if(done){return}done=true;var k=el.getAttribute("data-k");'
         'for(var i=0;i<o.length;i++){var x=o[i].getAttribute("data-k");if(x===c){o[i].classList.add("ok")}if(x===k){o[i].classList.add("sel")}free(o[i])}'
         'keep(k);say(k===c,k===c?"":"，错的是第 "+c+" 行");flip(k===c)}'
         + CLEAR + IDK_JS + 'window.qkTap=tap;arm(o,tap)})();</script>')
BUG_A = (HEAD % "找错行" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><div class="code" id="opts">{{Lines}}</div>'
         '<hr id="answer"><div class="a">{{Answer}}</div>' + TAIL +
         '<script>(function(){var c="{{Correct}}";var o=document.querySelectorAll("#opts .cl");' + SAVED +
         'for(var i=0;i<o.length;i++){var k=o[i].getAttribute("data-k");if(k===c){o[i].classList.add("ok")}if(k===m){o[i].classList.add("sel")}}'
         'var ok=m===c,miss="：你点了第 "+m+" 行";' + SHOW + '})();</script>')


JUDGE_Q = (HEAD % "判断组" + '<div class="q">{{Question}}<span class="hint">（每句点 ✓ 或 ✗）</span></div><div class="jrows" id="opts">{{Rows}}</div>' + IDK + FB +
           '<script>(function(){var c="{{Correct}}",root=document.getElementById("opts"),R=root.querySelectorAll(".jr"),B=root.querySelectorAll(".jb"),pick={},done=false;' + TOOLS +
           'function tap(el){if(done){return}var r=el.parentNode,i=r.getAttribute("data-i");pick[i]=el.getAttribute("data-v");'
           'var bs=r.querySelectorAll(".jb");for(var j=0;j<bs.length;j++){bs[j].classList.toggle("sel",bs[j]===el)}'
           'var n=0;for(var k in pick){n++}if(n===R.length){finish()}}'
           'function finish(){done=true;var s="",good=0;for(var i=0;i<R.length;i++){var v=pick[i],ok=v===c.charAt(i);s+=v;if(ok){good++}'
           'R[i].classList.add(ok?"ok":"bad")}for(var j=0;j<B.length;j++){free(B[j])}keep(s);'
           'say(good===R.length,good===R.length?"":"：对了 "+good+"/"+R.length);flip(good===R.length)}'
           + CLEAR + IDK_JS + 'window.qkTap=tap;arm(B,tap)})();</script>')
JUDGE_A = (HEAD % "判断组" + '<div class="q">{{Question}}</div><div class="mine" id="mine"></div><hr id="answer">{{Answer}}' + TAIL +
           '<script>(function(){var c="{{Correct}}";' + SAVED +
           'var R=document.querySelectorAll(".jsol li"),good=0;for(var i=0;i<R.length;i++){var ok=m&&m.charAt(i)===c.charAt(i);if(ok){good++}'
           'R[i].classList.add(ok?"ok":"bad")}var ok=good===R.length,miss="：对了 "+good+"/"+R.length;' + SHOW + '})();</script>')

READ_Q = (HEAD % "阅读" + '<div class="q">{{Title}}</div><div class="rbody">{{Body}}</div>')
READ_A = (READ_Q + '<hr id="answer"><div class="a">{{Key}}</div>' +
          '<div class="pt">考点：{{Point}}</div>' + NOTE_BLOCK + '<div class="grade">读懂了 → Good · 没懂 → Again</div>')

def templates() -> dict[str, tuple[str, str]]:
    """Front and back per model key. `quick.autoflip: false` in the plan config leaves turning the card to the usual tap."""
    out = {k: (front, back) for k, (_n, _f, front, back, _c) in MODELS.items()}
    if not note_fields():  # the collection has no note fields yet
        out = {k: (front, back.replace(NOTE_BLOCK, "")) for k, (front, back) in out.items()}
    if not config().get("autoflip", True):
        cut = TOOLS[TOOLS.index("function flip"):]
        out = {k: (front.replace(cut, NO_FLIP), back) for k, (front, back) in out.items()}
    return out


MODELS = {  # name, fields, front, back, cloze
    "qa": ("Trellis Quick QA", ["Question", "Answer", "Why", "Crumb", "Kind", "Point"], QA_Q, QA_A, False),
    "cloze": ("Trellis Quick Cloze", ["Text", "Why", "Crumb", "Point"], CLOZE_Q, CLOZE_A, True),
    "mc": ("Trellis Quick Choice", ["Question", "Opts", "Correct", "Answer", "Why", "Crumb", "Point"], MC_Q, MC_A, False),
    "order": ("Trellis Quick Order", ["Question", "Lines", "Solution", "Why", "Crumb", "Point"], ORDER_Q, ORDER_A, False),
    "match": ("Trellis Quick Match", ["Question", "Left", "Right", "Solution", "Why", "Crumb", "Point"], MATCH_Q, MATCH_A, False),
    "multi": ("Trellis Quick Multi", ["Question", "Opts", "Correct", "Answer", "Why", "Crumb", "Point"], MULTI_Q, MULTI_A, False),
    "bug": ("Trellis Quick Bug", ["Question", "Lines", "Correct", "Answer", "Why", "Crumb", "Point"], BUG_Q, BUG_A, False),
    "judge": ("Trellis Quick Judge", ["Question", "Rows", "Correct", "Answer", "Why", "Crumb", "Point"], JUDGE_Q, JUDGE_A, False),
    "read": ("Trellis Quick Read", ["Title", "Body", "Key", "Crumb", "Point"], READ_Q, READ_A, False),
}
MODEL_OF = {"flaw": "qa"}


def css() -> str:
    from trellis.build import CSS
    import test_cards
    return CSS + QUICK_CSS + test_cards.GRAPH_CSS + test_cards.SOURCE_CSS


def mark(s: str) -> str:
    s = html.escape(s.strip(), quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def scrambled(n: int, seed: str, identity_ok: bool) -> list[int]:
    """A fixed shuffle per card, so the front shows the same order on every device and never needs script to hide the answer."""
    rng = random.Random(zlib.crc32(seed.encode()))
    order = list(range(n))
    rng.shuffle(order)
    while not identity_ok and order == list(range(n)):
        rng.shuffle(order)
    return order


def snip(code: list[str]) -> str:
    """A short code block: one line per item, never wrapped, scrolls sideways."""
    return '<pre class="snip"><code>' + "\n".join(html.escape(x) for x in code) + "</code></pre>"



def dedent_code(md: str) -> str:
    """Strip the indent a code excerpt kept from its class or function, so a phone shows code, not margin."""
    import re
    import textwrap
    return re.sub(r"(```[^\n]*\n)(.*?)(```)", lambda m: m.group(1) + textwrap.dedent(m.group(2)) + m.group(3), md, flags=re.S)

def fields(c: dict, point: dict) -> tuple[str, list[str]]:
    """Model key and field values of a card."""
    f, why, crumb, title = c["fmt"], mark(c.get("why", "")), point["topic_title"], point["title"]
    if c.get("snippet"):  # a minimal working snippet on the back: code instead of prose (Chi, 2026-11-16)
        why += snip(c["snippet"])
    if c.get("code_q"):  # code shown with the question; scanned, so outside the reading units
        c = {**c, "q": c.get("q", ""), "_code_q": snip(c["code_q"])}
    if c.get("more"):  # kept inside the Why field: a new field forces a one-way full sync of the collection
        why += f'<div class="more"><b>延伸</b>{mark(c["more"])}</div>'
    if c.get("_graph") or c.get("_sources"):  # under the answer: the point's place in the graph (图谱), then its source cards (原卡)
        import test_cards
        why += test_cards.graph_block(c.get("_graph", []), c.get("_map")) + test_cards.source_block(c.get("_sources", []))
    if f in ("qa", "flaw"):
        q = ("这句话错在哪？<br>" if f == "flaw" else "") + mark(c["q"]) + c.get("_code_q", "")
        return "qa", [q, mark(c["a"]), why, crumb, KIND[f], title]
    if f == "cloze":
        return "cloze", [mark(c["text"]), why, crumb, title]
    if f == "mc":
        order = scrambled(len(c["opts"]), c["kp"], identity_ok=True)
        opts = "".join(f'<div class="opt tappable" data-k="{"ABC"[pos]}" onclick="qkTap(this)"><span class="k">{"ABC"[pos]}</span><div class="body">{mark(c["opts"][i])}</div></div>'
                       for pos, i in enumerate(order))
        right = "ABC"[order.index(0)]
        if c.get("_host") == "qa":  # the note is a QA note (the card used to be self-graded): options go inside its Question field
            return "qa", [mark(c["q"]) + c.get("_code_q", "") + f'<div class="opts" id="opts" data-c="{right}">{opts}</div>',
                          f"{right}. {mark(c['opts'][0])}", why, crumb, KIND["mc"], title]
        return "mc", [mark(c["q"]) + c.get("_code_q", ""), opts, right, f"{right}. {mark(c['opts'][0])}", why, crumb, title]
    if f == "multi":
        order = scrambled(len(c["opts"]), c["kp"], identity_ok=True)
        letters = "ABCDEF"
        opts = "".join(f'<div class="opt tappable" data-k="{letters[pos]}" onclick="qkTap(this)"><span class="k">{letters[pos]}</span><div class="body">{mark(c["opts"][i])}</div></div>'
                       for pos, i in enumerate(order))
        right = "".join(letters[pos] for pos, i in enumerate(order) if i in c["ok"])
        answer = "；".join(f"{letters[pos]}. {mark(c['opts'][i])}" for pos, i in enumerate(order) if i in c["ok"])
        return "multi", [mark(c["q"]) + c.get("_code_q", ""), opts, right, answer, why, crumb, title]
    if f == "bug":
        lines = "".join(f'<div class="cl tappable" data-k="{n + 1}" onclick="qkTap(this)"><span class="ln">{n + 1}</span><code>{html.escape(x)}</code></div>'
                        for n, x in enumerate(c["code"]))
        answer = f"第 {c['bad'] + 1} 行 → <code>{html.escape(c['fix'])}</code>"
        return "bug", [mark(c["q"]), lines, str(c["bad"] + 1), answer, why, crumb, title]
    if f == "read":
        from trellis.build import _html
        return "read", [mark(c["title"]), _html(dedent_code(c["body"])), mark(c["key"]), crumb, title]
    if f == "judge":
        rows = "".join(f'<div class="jr" data-i="{i}"><div class="body">{mark(r[0])}</div>'
                       '<span class="jb tappable" data-v="T" onclick="qkTap(this)">✓</span><span class="jb tappable" data-v="F" onclick="qkTap(this)">✗</span></div>'
                       for i, r in enumerate(c["rows"]))
        correct = "".join("T" if r[1] else "F" for r in c["rows"])
        answer = '<ol class="jsol">' + "".join(f'<li>{"✓" if r[1] else "✗"} {mark(r[0])}' + (f'<span class="jwhy">{mark(r[2])}</span>' if len(r) > 2 and r[2] else "") + "</li>"
                                               for r in c["rows"]) + "</ol>"
        return "judge", [mark(c["q"]), rows, correct, answer, why, crumb, title]
    if f == "order":
        items = [(str(i), x) for i, x in enumerate(c["lines"])] + [(f"x{i}", x) for i, x in enumerate(c.get("decoys", []))]
        order = scrambled(len(items), c["kp"], identity_ok=False)
        n = len(c["lines"])
        lines = "".join(f'<div class="pl tappable" data-i="{items[i][0]}"' + (f' data-n="{n}"' if pos == 0 else "") +
                        f' onclick="qkTap(this)"><span class="n"></span><div class="body">{mark(items[i][1])}</div></div>' for pos, i in enumerate(order))
        solution = '<ol class="steps">' + "".join(f"<li>{mark(x)}</li>" for x in c["lines"]) + "</ol>"
        if c.get("decoys"):
            solution += '<div class="why">不该出现：' + "；".join(mark(x) for x in c["decoys"]) + "</div>"
        return "order", [mark(c["q"]), lines, solution, why, crumb, title]
    order = scrambled(3, c["kp"], identity_ok=False)
    item = '<div class="mit tappable" data-i="{i}" onclick="qkTap(this)"><span class="badge"></span><div class="body">{t}</div></div>'
    left = "".join(item.format(i=i, t=mark(c["pairs"][i][0])) for i in range(3))
    right = "".join(item.format(i=i, t=mark(c["pairs"][i][1])) for i in order)
    solution = '<table class="sol">' + "".join(f"<tr><td>{mark(a)}</td><td>→</td><td>{mark(b)}</td></tr>" for a, b in c["pairs"]) + "</table>"
    return "match", [mark(c["q"]), left, right, solution, why, crumb, title]


def with_sources(cards: list[dict]) -> int:
    """Config `quick.full_back`: every card carries its point's source cards, as they stand in Anki, for its back.
    Returns how many cards got at least one."""
    import test_cards
    found = test_cards.source_notes([i for c in cards for i in c.get("based_on", [])])
    n = 0
    for c in cards:
        src = [found[i] for i in c.get("based_on", []) if i in found]
        if src:
            c["_sources"] = src
            n += 1
    return n


def with_graph(cards: list[dict]) -> int:
    """Every card carries its point's neighbours in the exam-point graph: what to learn first (prereq.json), what
    builds on it, and the interview questions that use it; plus a link to the point on the map."""
    import test_cards
    known = {kp: r for day in load_inputs().values() for kp, r in day.items()}
    pre = json.loads((HOME / "prereq.json").read_text(encoding="utf-8")) if (HOME / "prereq.json").exists() else {}
    rank = {c["kp"]: c["_point"]["rank"] for c in cards}
    title = {c["kp"]: mark(c["_point"]["title"]) for c in cards}
    after = defaultdict(list)
    for kp, needs in pre.items():
        for x in needs:
            after[x].append(kp)
    base = (json.loads((ROOT / "sources/local/plan/config.json").read_text(encoding="utf-8")).get("map_url") or "").strip()
    n = 0
    for c in cards:
        kp = c["kp"]
        first = [title[x] for x in sorted(pre.get(kp, []), key=lambda x: rank.get(x, 1e9)) if x in title]
        then = [title[x] for x in sorted(after.get(kp, []), key=lambda x: rank.get(x, 1e9)) if x in title]
        uses = sorted(known.get(kp, {}).get("used_by", []), key=lambda u: u.get("role") != "必讲")
        used = [mark(u["question"]) + (f'<em>{mark(u["role"])}</em>' if u.get("role") else "") for u in uses]
        c["_graph"] = [("先学", test_cards.some(first, 4, "个")), ("接着学", test_cards.some(then, 3, "个")), ("用在", test_cards.some(used, 3, "题"))]
        if base:
            c["_map"] = ("在知识地图里看这个考点", f"{base}#p/{c['_point']['topic']}/{kp}")
        n += any(items for _, items in c["_graph"])
    return n


def all_cards(verified_only: bool) -> tuple[list[dict], list[str]]:
    """Every usable card in deal order, each with its point."""
    inputs = load_inputs()
    points = {p["kp"]: {**p, "rank": i} for i, p in enumerate(json.loads((HOME / "points.json").read_text(encoding="utf-8")))}
    out, problems = [], []
    for day in sorted(inputs):
        cards, bad = load_cards(day, inputs[day], verified_only)
        problems += bad
        out += [{**c, "_point": points[c["kp"]]} for c in cards if c["kp"] in points]
    known = {kp: r for day in inputs.values() for kp, r in day.items()}
    taps = tap_rows()
    for i, c in enumerate(out):
        t = taps.get(c["kp"])
        if not t or c["fmt"] not in SELF_GRADED:
            continue
        new = tap_card(c, t)
        errs = check(new, known)
        if errs:
            problems.append(f"tap {c['kp']}: " + "; ".join(errs))   # the self-graded card stays until its rewrite passes
        else:
            out[i] = new
    return sorted(out, key=lambda c: c["_point"]["rank"]), problems


# ---------------------------------------------------------------- tap: self-graded cards rewritten as choice cards

SELF_GRADED = ("qa", "flaw")   # answered in the head and graded by himself: 97% "right" against 90% on machine-checked choice cards
TAP_CHUNK = 55


def tap_rows() -> dict[str, dict]:
    """kp -> the choice card that replaces the point's self-graded card (sources/local/quick/tap/t*.jsonl). Only the
    chunks named in tap/accepted.json count: a chunk is accepted by `tap-accept` once it is verified and read."""
    out = {}
    ok_file = HOME / "tap/accepted.json"
    accepted = set(json.loads(ok_file.read_text(encoding="utf-8"))) if ok_file.exists() else set()
    for f in sorted((HOME / "tap").glob("t*.jsonl")):
        if f.stem not in accepted:
            continue
        for r in read_rows(f)[0]:
            if r.get("kp") and not r.get("skip"):
                out[r["kp"]] = r
    return out


def tap_card(old: dict, t: dict) -> dict:
    keep = {k: old[k] for k in ("kp", "more", "_point") if k in old}
    return {**keep, "fmt": "mc", "q": t.get("q", ""), "opts": t.get("opts", []), "why": t.get("why", ""),
            "based_on": t.get("based_on") or old.get("based_on")}


def tap_accept(chunks: list[str]) -> int:
    """Mark verified chunks as accepted (after `tap-gate` is clean and the orchestrator has read them): `push` then applies them."""
    if tap_gate(chunks):
        print("not accepted: the gate has problems")
        return 1
    ok_file = HOME / "tap/accepted.json"
    accepted = set(json.loads(ok_file.read_text(encoding="utf-8"))) if ok_file.exists() else set()
    ok_file.write_text(json.dumps(sorted(accepted | set(chunks))), encoding="utf-8")
    print("accepted:", " ".join(sorted(accepted | set(chunks))))
    return 0


def tap_export() -> int:
    """The self-graded cards, 55 to a chunk, with what a writer needs: the point, the card as it stands, its source cards."""
    inputs = load_inputs()
    known = {kp: r for day in inputs.values() for kp, r in day.items()}
    cards, _ = all_cards(verified_only=True)
    todo = [c for c in cards if c["fmt"] in SELF_GRADED]
    out = HOME / "tap/input"
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for n, i in enumerate(range(0, len(todo), TAP_CHUNK), 1):
        rows = [{"kp": c["kp"], "title": known[c["kp"]]["title"], "summary": known[c["kp"]].get("summary", ""), "kind": known[c["kp"]].get("kind", ""),
                 "topic": known[c["kp"]].get("topic", ""), "card": {k: c[k] for k in ("fmt", "q", "a", "why", "more", "based_on") if c.get(k)},
                 "cards": known[c["kp"]]["cards"]} for c in todo[i:i + TAP_CHUNK]]
        (out / f"t{n:02d}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(todo)} self-graded cards -> {n} chunk(s) in {out.relative_to(ROOT)}")
    return 0


def tap_gate(chunks: list[str]) -> int:
    """A chunk of rewrites: one choice card per point of the input, every card passing the ten-second checks, and the
    right option not standing out by length."""
    inputs = load_inputs()
    known = {kp: r for day in inputs.values() for kp, r in day.items()}
    failed = 0
    for f in sorted((HOME / "tap/input").glob("t*.json")):
        if chunks and f.stem not in chunks:
            continue
        want = [r["kp"] for r in json.loads(f.read_text(encoding="utf-8"))]
        out = HOME / "tap" / f"{f.stem}.jsonl"
        rows, bad = read_rows(out) if out.exists() else ([], [])
        got = {r.get("kp"): r for r in rows}
        problems = list(bad) + [f"{kp}: not written" for kp in want if kp not in got] + [f"{kp}: not in this chunk" for kp in got if kp not in want]
        good = []
        for kp in want:
            r = got.get(kp)
            if not r or r.get("skip"):
                continue
            card = tap_card({"kp": kp, "based_on": [c["id"] for c in known[kp]["cards"]]}, r)
            errs = check(card, known)
            if errs:
                problems.append(f"{kp}: " + "; ".join(errs))
            else:
                good.append(card)
        import test_cards
        far, longest = test_cards.length_tell([([units(o) for o in c["opts"]], 0) for c in good if len(c["opts"]) > 1])
        if len(good) >= 10 and longest > 0.4 * len(good):
            problems.append(f"the right option is the longest in {longest} of {len(good)} cards (at most 40%): even them out")
        skipped = sum(1 for r in rows if r.get("skip"))
        print(f"{f.stem}: {len(good)} ok, {skipped} skipped, {len(problems)} problem(s); right option longest in {longest}/{len(good)}")
        for x in problems:
            print("  ", x)
        failed += len(problems)
    return 1 if failed else 0


# ---------------------------------------------------------------- pages: the templates outside Anki, for a render check


def substitute(tmpl: str, vals: dict[str, str], back: bool) -> str:
    section = re.compile(r"\{\{([#^])(\w+)\}\}(.*?)\{\{/\2\}\}", re.S)
    while section.search(tmpl):  # sections of other fields nest: resolve the outer ones until none is left
        tmpl = section.sub(lambda m: m.group(3) if bool(vals.get(m.group(2))) == (m.group(1) == "#") else "", tmpl)

    def rep(m):
        key = m.group(1)
        if key.startswith("cloze:"):
            show = r'<span class="cloze">\1</span>' if back else '<span class="cloze">[...]</span>'
            return re.sub(r"\{\{c1::(.*?)\}\}", show, vals[key[6:]])
        return vals.get(key, "")
    return re.sub(r"\{\{([^#^/}][^}]*)\}\}", rep, tmpl)


SIM = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html{background:#fbfbfb}%s</style></head><body class="card"><div id="qa"></div>
<script>
var SIDES = %s, side = "", flips = 0;
function put(name) {  // what a client does: replace the card's markup, then run its scripts
  side = name; var qa = document.getElementById("qa"); qa.innerHTML = SIDES[name];
  var old = qa.querySelectorAll("script");
  for (var i = 0; i < old.length; i++) { var n = document.createElement("script"); n.text = old[i].text; old[i].parentNode.replaceChild(n, old[i]); }
}
function turn() { if (side === "front") { flips++; put("back"); } }
if (location.hash !== "#mobile") { window.pycmd = function (c) { if (c === "ans") { turn(); } }; }
// AnkiMobile's rule, as its manual states it: a tap shows the answer unless it lands on a link, a button, an element with onclick, or one of class tappable
document.addEventListener("click", function (e) {
  if (location.hash !== "#mobile") { return; }
  var t = e.target;
  if (!(t.tagName === "A" || t.tagName === "BUTTON" || t.onclick || t.classList.contains("tappable"))) { turn(); }
});
put("front");
</script></body></html>"""


def pages(out: Path) -> None:
    """Per format, two cards: each side as a page, and a page that plays both sides the way a client does (add #mobile for AnkiMobile's tap rule)."""
    cards, _ = all_cards(verified_only=False)
    out.mkdir(parents=True, exist_ok=True)
    seen = Counter()
    sides = templates()
    for c in cards:
        if seen[c["fmt"]] >= 2 or (seen[c["fmt"]] == 1 and not c.get("more")):  # the second sample shows an extension line when one exists
            continue
        seen[c["fmt"]] += 1
        key, vals = fields(c, c["_point"])
        v = dict(zip(MODELS[key][1], vals))
        body = {side: substitute(tmpl, v, side == "back") for side, tmpl in zip(("front", "back"), sides[key])}
        for side, text in body.items():
            page = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<style>html{{background:#fbfbfb}}{css()}</style></head><body class="card">{text}</body></html>')
            (out / f"{c['fmt']}{seen[c['fmt']]}-{side}.html").write_text(page, encoding="utf-8")
        (out / f"{c['fmt']}{seen[c['fmt']]}-sim.html").write_text(SIM % (css(), json.dumps(body, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    print(f"{sum(seen.values()) * 3} pages in {out}")


# ---------------------------------------------------------------- push: into Anki


def package(cards: list[dict], path: Path) -> dict[str, dict]:
    import genanki
    from trellis.build import _stable_id

    sides = templates()
    models = {k: genanki.Model(_stable_id(f"trellis:model:{name}"), name, fields=[{"name": f} for f in (*names, *note_fields())],
                               templates=[{"name": name.split()[-1], "qfmt": sides[k][0], "afmt": sides[k][1]}], css=css(),
                               **({"model_type": genanki.Model.CLOZE} if cloze else {}))
              for k, (name, names, _front, _back, cloze) in MODELS.items()}
    deck = genanki.Deck(_stable_id(f"trellis:deck:{DECK}"), DECK)
    built = {}
    for c in cards:
        key, vals = fields(c, c["_point"])
        ident = f"quick.{c['kp']}"
        tags = [TAG, f"{TAG}::{c['_point']['day']}", f"kp::{c['kp']}", f"fmt::{c['fmt']}", f"id::{ident}"]
        deck.add_note(genanki.Note(model=models[key], fields=vals + [""] * len(note_fields()), guid=genanki.guid_for(f"trellis:{ident}"), tags=tags,
                                   due=c["_point"]["rank"] + 1))
        built[ident] = {"fields": dict(zip(MODELS[key][1], vals)), "model": MODELS[key][0], "tags": tags}
    genanki.Package([deck]).write_to_file(path)
    return built


def push(dry: bool, verified_only: bool) -> int:
    from anki_refresh import call

    from anki_refresh import match_note_fields
    match_note_fields()
    cards, problems = all_cards(verified_only)
    for p in problems:
        print("  ", p)
    if config().get("full_back"):
        print(f"source cards on the back of {with_sources(cards)} of {len(cards)} cards")
        print(f"graph neighbours on the back of {with_graph(cards)} of {len(cards)} cards")
    pushed_file = HOME / "pushed.json"
    pushed = set(json.loads(pushed_file.read_text(encoding="utf-8"))) if pushed_file.exists() else set()
    ids = call("findNotes", query=f"tag:{TAG}")
    info = []
    for i in range(0, len(ids), 400):
        info += call("notesInfo", notes=ids[i:i + 400])
    present = {next(t[4:] for t in n["tags"] if t.startswith("id::")): n for n in info}
    for c in cards:  # a self-graded card rewritten as a choice card stays on its QA note (see QA_Q)
        note = present.get(f"quick.{c['kp']}")
        if c["fmt"] == "mc" and note and note["modelName"] == MODELS["qa"][0]:
            c["_host"] = "qa"
    folder = Path(tempfile.mkdtemp(prefix="quick-"))
    built = package(cards, folder / "all.apkg")
    changes, retype = [], []
    for ident, b in built.items():
        note = present.get(ident)
        if not note:
            continue
        if note["modelName"] != b["model"]:
            retype.append(ident)  # a card rewritten in another format: the note type cannot change in place
            continue
        diff = {k: v for k, v in b["fields"].items() if note["fields"][k]["value"] != v}
        if diff:
            changes.append({"id": note["noteId"], "fields": diff})
    # a card Chi deleted in Anki was pushed once and is not present: it stays deleted
    fresh = [c for c in cards if f"quick.{c['kp']}" not in present and f"quick.{c['kp']}" not in pushed]
    print(f"{len(cards)} usable cards, {len(present)} in Anki, {len(changes)} to update, {len(fresh)} to add"
          + (f", {len(retype)} changed format (left as they are): {' '.join(retype[:5])}" if retype else ""))
    if dry:
        shutil.rmtree(folder, ignore_errors=True)
        return 0
    for i in range(0, len(changes), 50):
        call("multi", actions=[{"action": "updateNoteFields", "params": {"note": c}} for c in changes[i:i + 50]])
    if fresh:
        package(fresh, folder / "fresh.apkg")
        call("importPackage", path=str(folder / "fresh.apkg"))
        pushed |= {f"quick.{c['kp']}" for c in fresh}
        pushed_file.write_text(json.dumps(sorted(pushed)), encoding="utf-8")
        preset(call)
        import quick_plan
        quick_plan.park(call)  # the fresh cards wait for the planner; today's cut stays as dealt
    known = set(call("modelNames"))
    for key, (name, *_rest) in MODELS.items():
        if name not in known:
            continue
        call("updateModelStyling", model={"name": name, "css": css()})
        front, back = templates()[key]
        for card, now in call("modelTemplates", modelName=name).items():  # the text of a template syncs normally; only adding or removing one does not
            if (now["Front"], now["Back"]) != (front, back):
                call("updateModelTemplates", model={"name": name, "templates": {card: {"Front": front, "Back": back}}})
                print(f"template updated: {name}")
    call("sync")
    shutil.rmtree(folder, ignore_errors=True)
    return 0


def preset(call) -> None:
    """The deck's own preset: `per_day` new cards a day to start with, the learning steps of the system-design deck so the two can be compared."""
    cfg = config()
    conf = call("getDeckConfig", deck=DECK)
    if conf["name"] != PRESET:
        known_file = HOME / "preset.json"
        cid = json.loads(known_file.read_text())["id"] if known_file.exists() else \
            call("cloneDeckConfigId", name=PRESET, cloneFrom=call("getDeckConfig", deck="系统设计")["id"])
        if not cid:
            raise RuntimeError(f"could not create preset {DECK}")
        known_file.write_text(json.dumps({"id": cid}))
        call("setDeckConfigId", decks=[DECK], configId=cid)
        conf = call("getDeckConfig", deck=DECK)
    if not (HOME / "plan_state.json").exists():  # afterwards the planner sets the day's number (quick_plan.py)
        conf["new"]["perDay"] = int(cfg["per_day"])
    conf["rev"]["perDay"] = 9999
    conf["maxTaken"] = 60
    if cfg.get("steps"):
        conf["new"]["delays"] = cfg["steps"]
    call("saveDeckConfig", config=conf)


# ---------------------------------------------------------------- report: what the reviews say


def review_stats(call, query: str, since_ms: int) -> dict:
    cids = call("findCards", query=query)
    logs = {}
    for i in range(0, len(cids), 300):
        logs.update(call("getReviewsOfCards", cards=cids[i:i + 300]))
    first, later, secs, per_card = [], [], [], defaultdict(list)
    for cid, rows in logs.items():
        rows = sorted(rows, key=lambda r: r["id"])
        for n, r in enumerate(rows):
            if r["id"] < since_ms or r["type"] == 4:  # 4: rescheduled by hand, not an answer
                continue
            secs.append(r["time"] / 1000)
            per_card[cid].append(r)
            if n == 0:
                first.append(r["ease"] > 1)
            elif r["id"] - rows[n - 1]["id"] >= 3600_000:  # seen again after an hour or more: was it still there?
                later.append(r["ease"] > 1)
    studied = [c for c, rows in per_card.items() if rows]
    return {"cards": len(studied), "answers": len(secs), "minutes": sum(secs) / 60,
            "median_s": median(secs) if secs else 0.0,
            "first_ok": sum(first) / len(first) if first else None, "first_n": len(first),
            "later_ok": sum(later) / len(later) if later else None, "later_n": len(later),
            "missed": [int(c) for c, rows in per_card.items() if any(r["ease"] == 1 for r in rows)]}


def report(days: int) -> int:
    import time

    from anki_refresh import call

    call("sync")
    since = int((time.time() - days * 86400) * 1000)
    rows = [("碎片速刷", review_stats(call, f"tag:{TAG}", since)), ("系统设计", review_stats(call, "tag:sysdesign::* -tag:quick", since))]
    pct = lambda v, n: f"{v:.0%} ({n})" if v is not None else "无数据"  # noqa: E731
    print(f"最近 {days} 天")
    for name, s in rows:
        per = s["minutes"] * 60 / s["cards"] if s["cards"] else 0
        print(f"{name}: 学过 {s['cards']} 张，作答 {s['answers']} 次，共 {s['minutes']:.0f} 分钟；每次中位 {s['median_s']:.0f} 秒，每张合计 {per:.0f} 秒；"
              f"初见答对 {pct(s['first_ok'], s['first_n'])}，隔 1 小时以上再见答对 {pct(s['later_ok'], s['later_n'])}")
    missed = rows[0][1]["missed"]
    if missed:
        info = call("cardsInfo", cards=missed)
        points = {p["kp"]: p for p in json.loads((HOME / "points.json").read_text(encoding="utf-8"))}
        by_topic = defaultdict(list)
        tags = {n["noteId"]: n["tags"] for n in call("notesInfo", notes=sorted({c["note"] for c in info}))}
        for c in info:
            kp = next((t[4:] for t in tags[c["note"]] if t.startswith("kp::")), None)
            if kp in points:
                by_topic[points[kp]["topic_title"]].append((points[kp]["share"], points[kp]["title"], kp))
        print(f"答错过的考点 {sum(len(v) for v in by_topic.values())} 个（按专题，重的在前）：")
        for topic, ks in sorted(by_topic.items(), key=lambda kv: -sum(x[0] for x in kv[1])):
            print(f"  {topic}: " + "；".join(t for _, t, _ in sorted(ks, reverse=True)))
        (HOME / "missed.json").write_text(json.dumps(sorted({k for ks in by_topic.values() for _, _, k in ks})), encoding="utf-8")
    return 0


def main() -> int:
    args = sys.argv[1:]
    cmd = args[0] if args else ""
    if cmd == "select":
        select()
    elif cmd == "gate":
        return gate(args[1:])
    elif cmd == "show":
        show(args[1:])
    elif cmd == "pages":
        pages(Path(args[1]))
    elif cmd == "push":
        return push("--dry-run" in args, "--unverified" not in args)
    elif cmd == "report":
        return report(int(args[1]) if len(args) > 1 else 7)
    elif cmd == "tap-export":
        return tap_export()
    elif cmd == "tap-gate":
        return tap_gate(args[1:])
    elif cmd == "tap-accept":
        return tap_accept(args[1:])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
