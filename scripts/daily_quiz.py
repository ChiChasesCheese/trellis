"""每日测验: a small daily deck of test cards written from what Chi studied, separate from the learning decks.

    uv run python scripts/daily_quiz.py pick [--hours 30] [--n 20]   # choose topics from real answers → sources/local/quiz/pick-<date>.md
    uv run python scripts/daily_quiz.py import <questions.json>      # lint, then add the questions to the deck 1 每日测验
    uv run python scripts/daily_quiz.py settle                       # answered questions: record the result, move them to their topic's 考察题 deck
    uv run python scripts/daily_quiz.py score [--weak]               # accuracy per topic from the results (guides what to relearn)

    uv run python scripts/daily_quiz.py todo [--n 60] [--chunk 100]  # 模式识别: the next tree problems with no question yet, in plan order
    uv run python scripts/daily_quiz.py import <file> --set recog    # one recognition question per LeetCode problem, in its own deck;
    uv run python scripts/daily_quiz.py full                         # the back carries the problem's own card (re-copied from the tree)
    uv run python scripts/daily_quiz.py score --set recog            # recognised / missed per problem
    uv run python scripts/daily_quiz.py learn                        # leaf learning cards for the coming problems → sub-deck 1 学习卡
    uv run python scripts/daily_quiz.py lint <file> [--set recog]    # the importer's checks alone; `import … --update` rewrites known questions

模式识别 is the algorithm deck (Chi, 2026-11-21: it replaces 今日算法). Front: the problem and "which approach?". Back: the
answer, why, then the problem's whole tree card (statement, solution, pitfalls), so a miss is learnt on the spot and
Anki's own schedule brings it back. Its notes use the models Trellis Recog Choice / Multi: the quick-choice templates
plus a field `Full`. New cards come in plan order (core problems first, one per leaf a round), shuffled within the day.

How it fits (Chi, 2026-11-21): the quiz is independent of the learning flow and may steer it. A scheduled writer
(brief: research/agents/daily-quiz.md) runs settle → pick → writes questions → import each morning. A question is a
test card, not a teaching card: one interview-style probe, three or four short options, one correct, wrong options
taken from real mistakes. Once answered it leaves the quiz deck for `<topic deck>::考察题`, where it comes back on
Anki's schedule as a fast recap of that topic.

Topics are picked from real answers only (revlog types learn / review / relearn / filtered; a manual reschedule is not
studying): answered Again or Hard first, then newly learned, core cards weighted up; a topic is not quizzed twice in a
week. Domains: plan config `quiz.domains` (default sysdesign, leetcode-tree). Everything this writes is under
sources/local/quiz/ (gitignored: system-design sources are private). Notes use the model Trellis Quick Choice, so the
options are tappable on AnkiMobile; the result is the ease of the first answer (Again = wrong).
"""
from __future__ import annotations

import collections
import datetime
import hashlib
import html
import json
import os
import random
import re
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "sources/local/quiz"
CONFIG = ROOT / "sources/local/plan/config.json"
COLLECTION = Path(os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.anki2"))
DECK = "1 每日测验"
MODEL = "Trellis Quick Choice"
MULTI = "Trellis Quick Multi"
# a set = its own deck, tag and record files. `recog` is the pattern-recognition pass over the algorithm tree: every card
# shows only "模式识别" as its crumb (the topic would give the answer away) and stays in its deck after it is answered.
SETS = {"quiz": {"deck": DECK, "tag": "quiz", "preset": "每日测验", "questions": "questions.jsonl", "results": "results.jsonl"},
        "recog": {"deck": "2 算法模式识别", "tag": "recog", "preset": "算法模式识别", "questions": "recog.jsonl", "results": "recog-results.jsonl",
                  "models": ("Trellis Recog Choice", "Trellis Recog Multi"), "into": "2 算法模式识别::2 识别题"}}
LEARN_DECK = "2 算法模式识别::1 学习卡"   # a leaf's learning card (from the tree deck) waits here until its first problem is near
FULL_BLOCK = '{{#Full}}<div class="full"><div class="full-h">原卡</div>{{Full}}</div>{{/Full}}'
FULL_CSS = """
/* ---- 模式识别: the problem's own card under the answer ---- */
.full { margin-top: 22px; padding-top: 14px; border-top: 1px solid var(--rule); }
.full-h { font-size: 12px; letter-spacing: 0.04em; color: var(--dim); margin-bottom: 10px; }
.full hr { border: 0; border-top: 1px solid var(--rule); margin: 14px 0; }
"""
STATEMENT = '<div style="font-size:.86em;opacity:.8;margin:.35em 0 .55em">{}</div>'
RECAP = "考察题"
DAILY_DECKS = ("1 每日测验", "2 今日算法", "3 今日低层设计", "4 碎片速刷", "5 系统设计高频题", "6 Millennium", "7 Millennium 力扣", "8 LC Project")
LIMITS = {"question": 90, "option": 34, "why": 90, "title": 44, "statement": 100}   # characters; a test card is read in seconds


sys.path.insert(0, str(ROOT / "scripts"))
from test_cards import GRAPH_CSS, anki, graph_block, length_tell, some  # noqa: E402  (shared with the quick deck: scripts/test_cards.py)


def settings() -> dict:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8")).get("quiz", {}) if CONFIG.exists() else {}
    return {"domains": ["sysdesign", "leetcode-tree"], "per_day": 20, "rest_days": 7, **cfg}


def plain(field: str, limit: int) -> str:
    field = re.sub(r"<svg.*?</svg>", " [图] ", field, flags=re.S)
    field = re.sub(r'<details class="sec related-notes">.*\Z', " ", field, flags=re.S)
    text = html.unescape(re.sub(r"</?[A-Za-z!][^>]*>", " ", field))   # a real tag only: `1 << 20` in code is text
    return re.sub(r"\s+", " ", text).strip()[:limit]


def jsonl(name: str) -> list[dict]:
    f = HOME / name
    return [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()] if f.exists() else []


def topic_of(tags: list[str], domains: list[str]) -> tuple[str, str] | None:
    for t in tags:
        parts = t.split("::")
        if parts[0] in domains and len(parts) > 1:
            return parts[0], "::".join(parts[1:4])   # e.g. sd::patterns::large-blobs, sliding-window::2::1
    return None


# ---------------------------------------------------------------- pick

def pick(hours: int, n: int) -> int:
    cfg = settings()
    db = sqlite3.connect(f"file:{COLLECTION}?mode=ro", uri=True)
    db.create_collation("unicase", lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))
    since = (time.time() - hours * 3600) * 1000
    fields: dict[int, list[str]] = collections.defaultdict(list)
    for ntid, name in db.execute("select ntid, name from fields order by ntid, ord"):
        fields[ntid].append(name)
    rows = db.execute("""select c.id, n.id, n.mid, n.tags, n.flds, min(r.ease), sum(r.type = 0), count(*)
                         from revlog r join cards c on c.id = r.cid join notes n on n.id = c.nid
                         where r.id > ? and r.type in (0, 1, 2, 3) and r.ease > 0 group by c.id""", (since,)).fetchall()
    rested = {q["topic"] for q in jsonl("questions.jsonl")
              if q["date"] >= str(datetime.date.today() - datetime.timedelta(days=cfg["rest_days"]))}
    topics: dict[tuple[str, str], dict] = {}
    for cid, nid, mid, tags, flds, worst, new_answers, answers in rows:
        tag_list = tags.split()
        if "quiz" in tag_list:
            continue
        key = topic_of(tag_list, cfg["domains"])
        if not key or f"{key[0]}::{key[1]}" in rested:
            continue
        vals = dict(zip(fields[mid], flds.split("\x1f")))
        q = vals.get("Question") or vals.get("Front") or vals.get("Text") or ""
        a = vals.get("Answer") or vals.get("Back") or ""
        score = {1: 3.0, 2: 2.0}.get(worst, 1.5 if new_answers else 1.0)
        if "trellis::core" in tag_list or any(t.startswith("level::必会") for t in tag_list):
            score *= 1.5
        t = topics.setdefault(key, {"score": 0.0, "cards": [], "crumb": plain(vals.get("Crumb", ""), 60), "why": set()})
        t["score"] += score
        t["why"].add("答错过" if worst == 1 else "觉得难" if worst == 2 else "新学" if new_answers else "复习")
        t["cards"].append({"card": cid, "score": score, "q": plain(q, 300), "a": plain(a, 700)})
    per_domain = max(1, n // max(1, len(cfg["domains"])))
    chosen: list[tuple[tuple[str, str], dict]] = []
    for dom in cfg["domains"]:
        ranked = sorted((kv for kv in topics.items() if kv[0][0] == dom), key=lambda kv: -kv[1]["score"])
        chosen += ranked[:per_domain]
    HOME.mkdir(parents=True, exist_ok=True)
    today = str(datetime.date.today())
    out = [f"# 每日测验 · {today} · {len(chosen)} 个题目位\n",
           "按 research/agents/daily-quiz.md 的规则，每个题目位写一道选择题，输出 JSON 数组到 "
           f"sources/local/quiz/questions-{today}.json，然后运行 `uv run python scripts/daily_quiz.py import <该文件>`。\n"]
    for (dom, key), t in chosen:
        cards = sorted(t["cards"], key=lambda c: -c["score"])[:3]
        out.append(f"\n## topic `{dom}::{key}` · {t['crumb'] or key} · {'、'.join(sorted(t['why']))}\n"
                   f"source cards: {[c['card'] for c in cards]}\n")
        for c in cards:
            out.append(f"- **Q** {c['q']}\n  **A** {c['a']}\n")
    target = HOME / f"pick-{today}.md"
    target.write_text("".join(out), encoding="utf-8")
    print(f"{target.relative_to(ROOT)}: {len(chosen)} topics from {len(rows)} cards answered in the last {hours} h "
          f"({', '.join(f'{d} {sum(1 for (x, _), _ in chosen if x == d)}' for d in cfg['domains'])})")
    return 0


# ---------------------------------------------------------------- 模式识别: models and the problem's own card

def ensure_models() -> None:
    """Trellis Recog Choice / Multi: the quick-choice note types plus the field `Full`, shown under the answer. A new note
    type syncs normally; adding a field to an existing one would force a full sync, hence the separate types."""
    have = set(anki("modelNames"))
    for base, name in zip((MODEL, MULTI), SETS["recog"]["models"]):
        if name in have:
            continue
        tpl = next(iter(anki("modelTemplates", modelName=base).values()))
        mark = '<div class="pt">考点：{{Point}}</div>'
        if mark not in tpl["Back"]:
            raise RuntimeError(f"the back template of {base} changed: no {mark!r} to put the full card after")
        fields = [f for f in anki("modelFieldNames", modelName=base) if f not in ("Note", "NoteAnswer")] + ["Full", "Note", "NoteAnswer"]
        anki("createModel", modelName=name, inOrderFields=fields, css=anki("modelStyling", modelName=base)["css"] + FULL_CSS + GRAPH_CSS,
             cardTemplates=[{"Name": "Choice", "Front": tpl["Front"], "Back": tpl["Back"].replace(mark, mark + FULL_BLOCK)}])


def tree_cards() -> dict[str, dict]:
    """LC number -> {slug, front, back, card} of the problem's card on the algorithm tree."""
    out = {}
    nids = anki("findNotes", query='"tag:id::lct-*" -"tag:id::lct-learn-*"')
    for i in range(0, len(nids), 400):
        for n in anki("notesInfo", notes=nids[i:i + 400]):
            front = n["fields"]["Question"]["value"]
            m = re.search(r"LC (\d+)", front)
            slug = next((t[len("id::lct-"):] for t in n["tags"] if t.startswith("id::lct-")), "")
            if m and slug:
                out[m.group(1)] = {"slug": slug, "front": front, "back": n["fields"]["Answer"]["value"], "card": n["cards"][0]}
    return out


def full_html(card: dict) -> str:
    """The back's lower half: the problem's place on the algorithm tree (图谱), then its own card."""
    return graph_block(card.get("graph", []), None) + f'{card["front"]}<hr>{card["back"]}'


def with_graph(tree: dict[str, dict]) -> dict[str, dict]:
    """Each tree card gets its pattern (the leaf's path) and the other problems of that leaf, in the leaf's order."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import lc_tree
    by_slug = {c["slug"]: c for c in tree.values()}
    name = {c["slug"]: html.escape(plain(re.sub(r'<span class="meta">.*?</span>', "", c["front"].split("</p>")[0], flags=re.S), 60)) for c in tree.values()}
    for lst in lc_tree.build()["lists"]:
        for path, leaf in lc_tree.leaves(lst):
            here = [s for s in leaf["problems"] if s in by_slug]
            for s in here:
                others = [name[x] for x in here if x != s]
                by_slug[s]["graph"] = [("套路", [html.escape(" › ".join(path))]), ("同套路", some(others, 4, "题"))]
    return tree


def lc_number(title: str) -> str:
    m = re.search(r"LC (\d+)", title)
    return m.group(1) if m else ""


def refresh_full() -> int:
    """Copy each problem's tree card onto the back of its recognition question again (the tree card may have changed)."""
    tree = with_graph(tree_cards())
    for name in SETS["recog"]["models"]:   # the 图谱 block's styling, once
        css = anki("modelStyling", modelName=name)["css"]
        if GRAPH_CSS not in css:
            mark = css.find("/* ---- test decks: where the card sits")
            anki("updateModelStyling", model={"name": name, "css": (css[:mark] if mark >= 0 else css).rstrip() + "\n" + GRAPH_CSS})
    nids = anki("findNotes", query=f'"deck:{SETS["recog"]["deck"]}" tag:recog')
    changed, missing = 0, []
    for i in range(0, len(nids), 200):
        for n in anki("notesInfo", notes=nids[i:i + 200]):
            if "Full" not in n["fields"]:
                continue
            title = plain(n["fields"]["Question"]["value"], 60)
            card = tree.get(lc_number(title))
            if not card:
                missing.append(title[:40])
                continue
            want = full_html(card)
            if n["fields"]["Full"]["value"] != want:
                anki("updateNoteFields", note={"id": n["noteId"], "fields": {"Full": want}})
                changed += 1
    print(f"{len(nids)} recognition questions; {changed} backs updated; {len(missing)} with no tree card yet")
    for t in missing:
        print("  no card:", t)
    if changed:
        anki("sync")
    return 0


def plan_order() -> list[tuple[str, tuple]]:
    """Every tree problem once, in the order the plan studies them: the core problems first, a round taking one more
    problem from every leaf (most asked first), two lists alternating. -> [(slug, leaf path)]"""
    sys.path.insert(0, str(ROOT / "scripts"))
    import lc_tree
    built = lc_tree.build()
    core, out, seen = set(built["core"]), [], set()
    for only in (core, None):
        per_list = []
        for lst in built["lists"]:
            leaves = [(path, [s for s in leaf["problems"] if only is None or s in only]) for path, leaf in lc_tree.leaves(lst)]
            per_list.append(leaves)
        for r in range(max((len(p) for leaves in per_list for _, p in leaves), default=0)):
            rows = [[(p[r], path) for path, p in leaves if r < len(p)] for leaves in per_list]
            rows = [row for row in rows if row]
            for a in range(0, len(rows), 2):   # two lists at a time, one problem each in turn
                pair = rows[a:a + 2]
                for k in range(max(map(len, pair))):
                    for row in pair:
                        if k < len(row) and row[k][0] not in seen:
                            seen.add(row[k][0])
                            out.append(row[k])
    return out


def todo(n: int, chunk: int = 0) -> int:
    """The next `n` tree problems with no recognition question, with what the writer needs: statement and the gist.
    With `chunk`, one file per `chunk` problems (recog-todo-<date>-01.md …), each answered by recog-<date>-01.json."""
    tree = {c["slug"]: (num, c) for num, c in tree_cards().items()}
    have = {lc_number(q.get("title", "")) for q in jsonl(SETS["recog"]["questions"])}
    rows = [(slug, path) for slug, path in plan_order() if slug in tree and tree[slug][0] not in have][:n]
    today = str(datetime.date.today())
    parts = [rows[i:i + chunk] for i in range(0, len(rows), chunk)] if chunk else [rows]
    for k, part in enumerate(parts, 1):
        tail = f"-{k:02d}" if chunk else ""
        lines = [f"# 模式识别：{len(part)} 道题\n",
                 "按 research/agents/daily-quiz.md 的「模式识别」一节，每题写一道识别题，**保持下面的顺序**，写进 "
                 f"sources/local/quiz/recog-{today}{tail}.json。\n"]
        for slug, path in part:
            num, card = tree[slug]
            front = plain(re.sub(r'<span class="meta">.*?</span>', " ｜ ", card["front"], flags=re.S), 260)
            gist = plain(card["back"].split("</p>")[0], 160)
            lines.append(f"- topic: leetcode-tree::{slug}\n  - 题目：{front}\n  - 所在叶子（不要写进题目）：{' › '.join(path)}\n  - 解法要点：{gist}")
        (HOME / f"recog-todo-{today}{tail}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} problems -> {len(parts)} file(s) sources/local/quiz/recog-todo-{today}*.md")
    return 0


def deal_learn() -> int:
    """A leaf's learning card (it teaches the pattern) comes just before the leaf's first problem. Each morning the
    learning cards behind the day's problems move into the sub-deck 1 学习卡, which Anki deals before 2 识别题. The day is
    counted out against the deck's new-card limit: a problem costs one card, two when its leaf's learning card is still
    unseen, so learning cards and problems arrive together and never crowd each other out. A learning card stays in the
    sub-deck once moved (its old deck is kept in learn-homes.json)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import lc_tree
    cfg = SETS["recog"]
    names = anki("deckNames")
    if cfg["deck"] not in names:
        return 0
    if LEARN_DECK not in names:
        anki("createDeck", deck=LEARN_DECK)
        anki("setDeckConfigId", decks=[LEARN_DECK], configId=anki("getDeckConfig", deck=cfg["deck"])["id"])
    budget = anki("getDeckConfig", deck=cfg["deck"])["new"]["perDay"]
    ahead = sorted(anki("cardsInfo", cards=anki("findCards", query=f'"deck:{cfg["deck"]}" tag:recog is:new -is:suspended')),
                   key=lambda c: c["due"])
    slug_of = {num: c["slug"] for num, c in tree_cards().items()}
    leaf_of = {s: leaf["id"] for lst in lc_tree.build()["lists"] for _, leaf in lc_tree.leaves(lst) for s in leaf["problems"]}
    unseen = {}   # learning-card id -> its card, for every learning card still new
    cards = anki("findCards", query='"tag:id::lct-learn-*" is:new -is:suspended')
    notes = {n["noteId"]: n["tags"] for n in anki("notesInfo", notes=anki("findNotes", query='"tag:id::lct-learn-*"'))}
    for c in anki("cardsInfo", cards=cards):
        ident = next((t[4:] for t in notes.get(c["note"], []) if t.startswith("id::lct-learn-")), "")
        unseen[ident] = c
    waiting = {i for i, c in unseen.items() if c["deckName"] == LEARN_DECK}   # dealt earlier, not learnt yet: they come first
    used, problems, move = len(waiting), 0, []
    for c in ahead:
        slug = slug_of.get(lc_number(plain(c["fields"]["Question"]["value"], 60)))
        ident = lc_tree.card_id(leaf_of[slug]) if slug in leaf_of else ""
        extra = 1 if ident in unseen and ident not in waiting else 0
        if used + 1 + extra > budget:
            break
        used, problems = used + 1 + extra, problems + 1
        if extra:
            waiting.add(ident)
            move.append(unseen[ident])
    if move:
        homes_file = HOME / "learn-homes.json"
        homes = json.loads(homes_file.read_text(encoding="utf-8")) if homes_file.exists() else {}
        homes.update({str(c["cardId"]): c["deckName"] for c in move})
        homes_file.write_text(json.dumps(homes, ensure_ascii=False, indent=0), encoding="utf-8")
        anki("changeDeck", cards=[c["cardId"] for c in move], deck=LEARN_DECK)
        anki("sync")
    print(f"today's {budget} new cards: {problems} problems + {len(waiting)} learning cards ({len(move)} moved to {LEARN_DECK} now)")
    return 0


# ---------------------------------------------------------------- import

def lint(q: dict) -> list[str]:
    errs = []
    opts = q.get("options", [])
    right = q.get("correct")
    multi = isinstance(right, list)
    if not 3 <= len(opts) <= (5 if multi else 4):
        errs.append("needs 3 or 4 options (up to 5 when several are correct)")
    if multi:
        if not (2 <= len(right) < len(opts) and all(isinstance(i, int) and 0 <= i < len(opts) for i in right)):
            errs.append("multi-select: correct must list 2 or more option indexes, not all of them")
    elif not isinstance(right, int) or not 0 <= right < len(opts):
        errs.append("correct must be the index of one option (or a list of indexes for multi-select)")
    for key in ("question", "title", "statement"):
        if len(q.get(key, "")) > LIMITS[key]:
            errs.append(f"{key} over {LIMITS[key]} characters")
    if any(len(o) > LIMITS["option"] for o in opts):
        errs.append(f"an option over {LIMITS['option']} characters")
    if len(q.get("why", "")) > LIMITS["why"] or not q.get("why"):
        errs.append(f"why missing or over {LIMITS['why']} characters")
    if opts and max(map(len, opts)) > 2.5 * max(4, min(map(len, opts))):
        errs.append("option lengths differ too much (the longest gives the answer away)")
    if opts and isinstance(right, int) and 0 <= right < len(opts) and len(opts[right]) > 1.25 * max(len(o) for i, o in enumerate(opts) if i != right):
        errs.append("the correct option is much longer than every wrong one: lengthen a wrong option or shorten the right one")
    if any(re.search(r"以上|都对|都不对|全部正确", o) for o in opts):
        errs.append('no "all / none of the above" options')
    if len(set(opts)) != len(opts):
        errs.append("duplicate options")
    for key in ("topic", "point"):
        if not q.get(key):
            errs.append(f"missing {key}")
    if q.get("topic", "").startswith("leetcode") and not q.get("statement"):
        errs.append("an algorithm question needs a statement: what the problem asks, in one or two lines")
    return errs


def lint_file(questions: list[dict]) -> list[tuple[int, str]]:
    bad = [(i, e) for i, q in enumerate(questions) for e in lint(q)]
    single = [q for q in questions if isinstance(q.get("correct"), int) and len(q.get("options", [])) > 1 and 0 <= q["correct"] < len(q["options"])]
    _far, longest, shortest = length_tell([([len(o) for o in q["options"]], q["correct"]) for q in single])
    for n, word in ((longest, "longest"), (shortest, "shortest")):   # neither "pick the longest" nor "pick the shortest" may pass the test
        if len(single) >= 10 and n > 0.4 * len(single):
            bad.append((-1, f"the correct option is the {word} in {n} of {len(single)} questions (at most 40%): even them out"))
    return bad


def home_deck(source: list[int]) -> str:
    """The topic deck of the question's source cards (their home, not a daily deck they were dealt into)."""
    moved: dict[str, str] = {}
    for name in ("homes.json", "company_homes.json"):   # where the planners remember a dealt card's own deck
        f = ROOT / "sources/local/plan" / name
        if f.exists():
            moved.update({k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if isinstance(v, str)})
    for info in anki("cardsInfo", cards=source):
        deck = moved.get(str(info["cardId"])) or info["deckName"]
        if not deck.startswith(DAILY_DECKS):
            return "::".join(deck.split("::")[:3])
    return ""


def question_html(q: dict) -> str:
    """Title, then what the problem asks in small print, then the question itself."""
    head = f'<b>{html.escape(q["title"])}</b>' if q.get("title") else ""
    stmt = STATEMENT.format(html.escape(q["statement"])) if q.get("statement") else ("<br>" if head else "")
    return head + stmt + html.escape(q["question"])


def import_questions(path: Path, kind: str = "quiz", update: bool = False, only_lint: bool = False) -> int:
    cfg = SETS[kind]
    questions = json.loads(path.read_text(encoding="utf-8"))
    bad = lint_file(questions)
    for i, e in bad:
        print(f"  question {i + 1}: {e}" if i >= 0 else f"  whole file: {e}")
    if bad:
        print(f"{len({i for i, _ in bad})} of {len(questions)} questions fail the lint; nothing imported")
        return 1
    if only_lint:
        print(f"{len(questions)} questions pass the lint")
        return 0
    today = str(datetime.date.today())
    known = {q["id"]: q["note"] for q in jsonl(cfg["questions"])}
    if cfg["deck"] not in anki("deckNames"):
        anki("createDeck", deck=cfg["deck"])
        base = anki("getDeckConfig", deck="4 碎片速刷")
        cid = anki("cloneDeckConfigId", name=cfg["preset"], cloneFrom=base["id"])
        if cid:
            anki("setDeckConfigId", decks=[cfg["deck"]], configId=cid)
            conf = anki("getDeckConfig", deck=cfg["deck"])
            conf["new"]["perDay"], conf["rev"]["perDay"] = 9999, 9999   # the deck holds exactly what is meant to be answered
            if kind == "recog":   # the day's cards are the next ones in plan order, shown shuffled: a run of one topic gives the answer away
                conf["newGatherPriority"], conf["newSortOrder"] = 0, 4
                conf["new"]["order"] = 1   # a new note takes the next position; the quick deck's preset inserts at random
            anki("saveDeckConfig", config=conf)
    notes, records, updated = [], [], 0
    tree = {}
    target = cfg.get("into", cfg["deck"])
    if kind == "recog":
        ensure_models()
        tree = with_graph(tree_cards())
        if target not in anki("deckNames"):   # sub-decks share the deck's preset, so its daily limit covers them together
            anki("createDeck", deck=target)
            anki("setDeckConfigId", decks=[target], configId=anki("getDeckConfig", deck=cfg["deck"])["id"])
    for q in questions:
        qid = f"{cfg['tag']}-" + hashlib.sha1((q["topic"] + q.get("title", "") + q["question"]).encode()).hexdigest()[:10]
        if qid in known and not update:
            continue
        order = list(range(len(q["options"])))
        random.Random(qid).shuffle(order)   # the writer tends to put the right answer first
        letters = "ABCDE"
        opts = "".join(f'<div class="opt tappable" data-k="{letters[pos]}" onclick="qkTap(this)"><span class="k">{letters[pos]}</span>'
                       f'<div class="body">{html.escape(q["options"][i])}</div></div>' for pos, i in enumerate(order))
        multi = isinstance(q["correct"], list)
        right = sorted(letters[order.index(i)] for i in (q["correct"] if multi else [q["correct"]]))
        answer = "；".join(f'{k}. {html.escape(q["options"][order[letters.index(k)]])}' for k in right)
        source = [int(c) for c in q.get("source", [])]
        home = home_deck(source) if source and kind == "quiz" else ""
        crumb = "模式识别" if kind == "recog" else q.get("crumb") or q["point"]
        choice, several = cfg.get("models", (MODEL, MULTI))
        fields = {"Question": question_html(q), "Opts": opts, "Correct": "".join(right), "Answer": answer,
                  "Why": html.escape(q["why"]), "Crumb": html.escape(crumb), "Point": html.escape(q["point"])}
        if kind == "recog":   # the problem's own card goes under the answer; a problem not on the tree yet gets it at the next `full`
            own = tree.get(lc_number(q.get("title", "")))
            fields["Full"] = full_html(own) if own else ""
        if qid in known:   # --update: a corrected question replaces the text of its note; scheduling and the back stay
            anki("updateNoteFields", note={"id": known[qid], "fields": fields})
            updated += 1
            continue
        notes.append({"deckName": target, "modelName": several if multi else choice, "fields": fields,
                      "tags": [cfg["tag"], f"{cfg['tag']}::{today}", f"{cfg['tag']}::id::{qid}", f"{cfg['tag']}::leaf::{q['topic']}"],
                      "options": {"allowDuplicate": True}})
        records.append({"id": qid, "date": today, "topic": q["topic"], "point": q["point"], "source": source, "home": home,
                        "title": q.get("title", "")})
    if notes:
        ids = anki("addNotes", notes=notes)
        with (HOME / cfg["questions"]).open("a", encoding="utf-8") as fh:
            for rec, nid in zip(records, ids):
                fh.write(json.dumps({**rec, "note": nid}, ensure_ascii=False) + "\n")
        anki("sync")
    if updated:
        anki("sync")
    print(f"{len(notes)} question(s) added to {target}" + (f", {updated} updated" if updated else ""))
    return 0


# ---------------------------------------------------------------- settle and score

def settle(kind: str = "quiz") -> int:
    """Answered questions: the first answer is the result. Quiz cards then go to their topic's 考察题 deck; recognition
    cards stay where they are and come back on Anki's schedule."""
    cfg = SETS[kind]
    done = {r["id"] for r in jsonl(cfg["results"])}
    cards = anki("cardsInfo", cards=anki("findCards", query=f'"deck:{cfg["deck"]}" tag:{cfg["tag"]} -is:new'))
    by_note = {q["note"]: q for q in jsonl(cfg["questions"])}
    cards = [c for c in cards if c["note"] in by_note and by_note[c["note"]]["id"] not in done]
    if not cards:
        print("nothing answered since the last settle")
        return 0
    reviews = anki("getReviewsOfCards", cards=[str(c["cardId"]) for c in cards])
    moves: dict[str, list[int]] = collections.defaultdict(list)
    with (HOME / cfg["results"]).open("a", encoding="utf-8") as fh:
        for c in cards:
            q = by_note.get(c["note"])
            log = sorted(reviews.get(str(c["cardId"]), []), key=lambda r: r["id"])
            if not q or not log:
                continue
            fh.write(json.dumps({"id": q["id"], "topic": q["topic"], "point": q["point"], "title": q.get("title", ""), "correct": log[0]["ease"] > 1,
                                 "ease": log[0]["ease"], "date": str(datetime.date.fromtimestamp(log[0]["id"] / 1000))},
                                ensure_ascii=False) + "\n")
            if q.get("home"):
                moves[f"{q['home']}::{RECAP}"].append(c["cardId"])
    names = set(anki("deckNames"))
    for deck, ids in moves.items():
        if deck not in names:   # a new 考察题 deck takes its topic deck's preset, so its reviews follow the topic's limits
            anki("createDeck", deck=deck)
            anki("setDeckConfigId", decks=[deck], configId=anki("getDeckConfig", deck=deck.rsplit("::", 1)[0])["id"])
        anki("changeDeck", cards=ids, deck=deck)
    anki("sync")
    print(f"{len(cards)} answered; {sum(map(len, moves.values()))} moved to {len(moves)} 考察题 deck(s)")
    return 0


def score(weak_only: bool, kind: str = "quiz") -> int:
    results = jsonl(SETS[kind]["results"])
    if kind == "recog":   # per problem; a missed one is relearnt from its own back and returns on Anki's schedule
        missed = [r for r in results if not r["correct"]]
        (HOME / "recog-missed.json").write_text(json.dumps([{"title": r["title"], "topic": r["topic"]} for r in missed],
                                                           ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(results)} problems answered, {len(results) - len(missed)} recognised ({100 * (len(results) - len(missed)) // max(1, len(results))}%); "
              f"{len(missed)} missed -> sources/local/quiz/recog-missed.json")
        for r in missed:
            print("  ✗", r["title"])
        return 0
    by_topic: dict[str, list[bool]] = collections.defaultdict(list)
    for r in results:
        by_topic[r["topic"]].append(r["correct"])
    total = sum(len(v) for v in by_topic.values())
    print(f"{total} questions answered, {sum(sum(v) for v in by_topic.values())} correct "
          f"({100 * sum(sum(v) for v in by_topic.values()) // max(1, total)}%)")
    for topic, v in sorted(by_topic.items(), key=lambda kv: (sum(kv[1]) / len(kv[1]), -len(kv[1]))):
        if weak_only and all(v):
            continue
        print(f"  {sum(v)}/{len(v)}  {topic}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "pick":
        hours = int(args[args.index("--hours") + 1]) if "--hours" in args else 30
        n = int(args[args.index("--n") + 1]) if "--n" in args else settings()["per_day"]
        return pick(hours, n)
    kind = args[args.index("--set") + 1] if "--set" in args else "quiz"
    if kind not in SETS:
        print(f"unknown set {kind!r}; one of {sorted(SETS)}")
        return 2
    if args[0] == "todo":
        return todo(int(args[args.index("--n") + 1]) if "--n" in args else 60, int(args[args.index("--chunk") + 1]) if "--chunk" in args else 0)
    if args[0] == "full":
        return refresh_full()
    if args[0] == "learn":
        return deal_learn()
    if args[0] in ("import", "lint"):
        return import_questions(Path(args[1]), kind, update="--update" in args, only_lint=args[0] == "lint")
    if args[0] == "settle":
        return settle(kind)
    if args[0] == "score":
        return score("--weak" in args, kind)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
