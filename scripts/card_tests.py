"""A test deck written from a learning deck: one choice question per learning card, the card itself on the back.

    uv run python scripts/card_tests.py status <set>                  # how many source cards, how many have a question
    uv run python scripts/card_tests.py todo <set> [--chunk 60] [--start N]   # source cards with no question yet → sources/local/quiz/<set>-todo-NN.md
    uv run python scripts/card_tests.py lint <set> <file.json>        # the importer's checks alone
    uv run python scripts/card_tests.py review <set> NN [--show]      # a chunk's part files against its todo file; merges them when clean
    uv run python scripts/card_tests.py import-ready <set>            # import the verified chunks' questions, in study order, as far as they reach
    uv run python scripts/card_tests.py import <set> <file.json> [--update]   # one file as it is (use --update to rewrite questions already in Anki)
    uv run python scripts/card_tests.py full <set>                    # copy the source cards onto the backs again
    uv run python scripts/card_tests.py chunks <set> [NN <stage>]     # each chunk's stage (written / verifying / verified / imported); set one

Sets (Chi, 2026-11-22: 「lld 也全量更新，ai 相关卡组也是」): `lld` → deck 3 低层设计测验 from 低层设计（LLD）; `ai` → deck AI 测验 from
AI 通识, LLM 推理, AI 应用工程 and ML 与 LLM 系统设计. They follow the algorithm deck 算法模式识别 (scripts/daily_quiz.py) and
share its note types: the front is answered by tapping; the back shows the answer, why, the card's place among its
neighbours (图谱) and the source card in full (原卡), so a miss is learnt on the spot. The source decks keep their cards
for the backs and for reviews and deal no new ones (plan config `caps.zero_under`).

A question is tied to its source card by the card's id; there is one question per card. New cards come in the source
deck's own order. Writers and verifiers: research/agents/card-test-questions.md, research/agents/card-test-verify.md.
Everything written is under sources/local/quiz/ (some source decks are private).
"""
from __future__ import annotations

import datetime
import hashlib
import html
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import daily_quiz as dq  # noqa: E402
from test_cards import anki, graph_block, some  # noqa: E402

HOME = dq.HOME
MODELS = dq.SETS["recog"]["models"]
SOURCE_MODELS = ("Trellis QA", "Trellis Cloze")
EXCERPT = {"front": 1200, "back": 1800}   # what a writer sees of each side: whole cards (writers did not open cut-off ones)
# set -> its deck, and where its source cards come from: (sub-deck of the test deck, Anki query), in study order
AI = '("tag:ai-literacy::*" OR "tag:llm-inference::*" OR "tag:ml-system-design::*")'
SETS = {
    "lld": {"deck": "3 低层设计测验", "tag": "tlld", "preset": "低层设计测验", "crumb": "低层设计", "per_day": 20,
            "sources": [("", '"deck:低层设计（LLD）"')]},
    # AI: the reading order of 「AI 从零开始」 in the Cerebras deck comes first (basics before everything), then the rest
    "ai": {"deck": "AI 测验", "tag": "tai", "preset": "AI 测验", "crumb": "AI", "per_day": 20,
           "sources": [("1 AI 从零开始", f'"deck:6 Cerebras::04 AI 从零开始" {AI}'), ("2 机器学习基础", f'"deck:6 Cerebras::05 机器学习基础" {AI}'),
                       ("3 LLM 推理", f'"deck:6 Cerebras::08 LLM 推理" {AI}'), ("4 加速器与编译器", f'"deck:6 Cerebras::09 加速器与编译器" {AI}'),
                       ("5 AI 应用工程", '"deck:AI 应用工程"'), ("6 ML 与 LLM 系统设计", f'"deck:6 Cerebras::10 ML 与 LLM 系统设计" {AI}'),
                       ("7 生成式 AI 与经典 ML 设计题", f'"deck:6 Cerebras::16 生成式 AI 与经典 ML 设计题" {AI}'),
                       ("8 AI 通识 · 扩展", f'"deck:6 Cerebras::18 AI 通识 · 扩展" {AI}'), ("9 其他", AI)]},
}
for _name, _cfg in SETS.items():   # settle and score in daily_quiz.py work on these sets too
    dq.SETS[_name] = {**_cfg, "questions": f"{_name}.jsonl", "results": f"{_name}-results.jsonl", "models": MODELS}


def _title(front: str) -> str:
    m = re.search(r'<p class="title">(.*?)</p>', front, flags=re.S)
    text = dq.plain(re.sub(r'<span class="meta">.*?</span>', "", m.group(1) if m else front, flags=re.S), 200)
    return text[:40]


def sources(kind: str) -> list[dict]:
    """The set's source cards in study order: {id, group, deck, crumb, title, front, back}. A note counts once, under
    the first group that has it; a note whose cards are all suspended is left out."""
    out, seen = [], set()
    for g, (group, query) in enumerate(SETS[kind]["sources"]):
        cids = anki("findCards", query=query)
        cards = [c for i in range(0, len(cids), 500) for c in anki("cardsInfo", cards=cids[i:i + 500])]
        by_note: dict[int, list[dict]] = {}
        for c in cards:
            if c["modelName"] in SOURCE_MODELS:
                by_note.setdefault(c["note"], []).append(c)
        alive = {n: cs for n, cs in by_note.items() if n not in seen and any(c["queue"] != -1 for c in cs)}
        nids = sorted(alive)
        notes = [n for i in range(0, len(nids), 300) for n in anki("notesInfo", notes=nids[i:i + 300])]
        rows = []
        for n in notes:
            ident = next((t[4:] for t in n["tags"] if t.startswith("id::")), None)
            if not ident:
                continue
            f = n["fields"]
            if "Text" in f:   # a cloze note: the text with its blanks filled is the whole card
                front = re.sub(r"\{\{c\d+::(.*?)(::.*?)?\}\}", r"<b>\1</b>", f["Text"]["value"], flags=re.S)
                back = ""
            else:
                front = f["Question"]["value"]
                back = re.sub(r'<details class="sec related-notes">.*\Z', "", f["Answer"]["value"], flags=re.S)
            first = min(alive[n["noteId"]], key=lambda c: (c["deckName"], c["due"]))
            rows.append({"id": ident, "group": group, "deck": first["deckName"], "due": first["due"], "front": front, "back": back,
                         "crumb": dq.plain(f.get("Crumb", {}).get("value", ""), 120), "title": _title(front), "_g": g})
            seen.add(n["noteId"])
        out += sorted(rows, key=lambda r: (r["deck"], r["due"], r["id"]))
    return out


def done(kind: str) -> dict[str, dict]:
    return {q["source"]: q for q in dq.jsonl(dq.SETS[kind]["questions"])}


def status(kind: str) -> int:
    src, have = sources(kind), done(kind)
    left = [s for s in src if s["id"] not in have]
    print(f"{kind}: {len(src)} source cards, {len(src) - len(left)} with a question, {len(left)} to write")
    for group in dict.fromkeys(s["group"] for s in src):
        g = [s for s in src if s["group"] == group]
        print(f"  {group or SETS[kind]['deck']}: {sum(1 for s in g if s['id'] in have)}/{len(g)}")
    return 0


def written(kind: str) -> set[str]:
    """Sources that already have a question in a part file (written, perhaps not imported yet)."""
    out = set()
    for f in HOME.glob(f"{kind}-bulk-*.part*.json"):
        try:
            out |= {q.get("source") for q in json.loads(f.read_text(encoding="utf-8"))}
        except json.JSONDecodeError:
            pass
    return out


def todo(kind: str, chunk: int, start: int = 1) -> int:
    """Chunk files for the source cards that have no question yet (neither imported nor written), numbered from `start`;
    chunk files below `start` are left as they are."""
    have = set(done(kind)) | written(kind)
    rows = [s for s in sources(kind) if s["id"] not in have]
    for old in HOME.glob(f"{kind}-todo-[0-9][0-9].md"):
        if int(old.stem[-2:]) >= start:
            old.unlink()
    parts = [rows[i:i + chunk] for i in range(0, len(rows), chunk)]
    for k, part in enumerate(parts, start):
        lines = [f"# {SETS[kind]['deck']}：{len(part)} 张原卡，每张写一道测试题\n",
                 f"规则见 research/agents/card-test-questions.md。**保持下面的顺序**，写进 sources/local/quiz/{kind}-bulk-{k:02d}.part1.json "
                 f"和 part2.json（各一半）。\n"]
        for s in part:
            front = EXCERPT["front"] if s["back"] else EXCERPT["front"] + EXCERPT["back"]   # a cloze card is all front
            lines.append(f"- source: {s['id']}\n  - 位置：{s['crumb'] or s['deck']}\n  - 正面：{dq.plain(s['front'], front)}\n"
                         f"  - 背面：{dq.plain(s['back'], EXCERPT['back']) or '（填空卡：正面已含全部内容）'}")
        (HOME / f"{kind}-todo-{k:02d}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} source cards -> {len(parts)} file(s) sources/local/quiz/{kind}-todo-NN.md, from {start:02d}")
    return 0


def lint_file(kind: str, questions: list[dict], known: set[str] | None = None) -> list[tuple[int, str]]:
    for q in questions:
        q.setdefault("topic", f"{kind}::{q.get('source', '')}")
    bad = dq.lint_file(questions)
    for i, q in enumerate(questions):
        if not q.get("source"):
            bad.append((i, "missing source (the id of the card the question is written from)"))
        elif known is not None and q["source"] not in known:
            bad.append((i, f"source {q['source']!r} is not a card of this set"))
        if not q.get("title"):
            bad.append((i, "missing title"))
    if len({q.get("source") for q in questions}) != len(questions):
        bad.append((-1, "two questions for one source card"))
    return bad


def _name(s: dict, titles: dict[str, str]) -> str:
    """A neighbour's name in the 图谱 block: the title of its test question once it has one, else its own first sentence."""
    if s["id"] in titles:
        return titles[s["id"]]
    text = dq.plain(re.sub(r'<span class="meta">.*?</span>', "", s["front"], flags=re.S), 400)
    m = re.match(r".{6,60}?[？?。；]", text)
    return m.group(0) if m else text[:60]


def _full(s: dict, group: list[dict], titles: dict[str, str]) -> str:
    others = [html.escape(_name(x, titles)) for x in group if x["id"] != s["id"]]
    return graph_block([("位置", [html.escape(s["crumb"] or s["deck"])]), ("同组", some(others, 4, "张"))]) + \
        f'{s["front"]}<hr>{s["back"]}'


def _siblings(src: list[dict]) -> dict[str, list[dict]]:
    by: dict[str, list[dict]] = {}
    for s in src:
        by.setdefault(s["deck"], []).append(s)
    return by


def ensure_deck(kind: str, src: list[dict]) -> None:
    cfg = SETS[kind]
    dq.ensure_models()
    names = set(anki("deckNames"))
    wanted = [cfg["deck"]] + [f"{cfg['deck']}::{g}" for g, _ in cfg["sources"] if g]
    if cfg["deck"] not in names:
        anki("createDeck", deck=cfg["deck"])
        cid = anki("cloneDeckConfigId", name=cfg["preset"], cloneFrom=anki("getDeckConfig", deck=dq.SETS["recog"]["deck"])["id"])
        if cid:
            anki("setDeckConfigId", decks=[cfg["deck"]], configId=cid)
            conf = anki("getDeckConfig", deck=cfg["deck"])
            conf["new"]["perDay"], conf["rev"]["perDay"] = int(cfg["per_day"]), 9999
            conf["newGatherPriority"], conf["newSortOrder"], conf["newMix"] = 0, 1, 1   # sub-decks in order, then position; reviews first
            conf["new"]["order"] = 1
            anki("saveDeckConfig", config=conf)
    cid = anki("getDeckConfig", deck=cfg["deck"])["id"]
    for d in wanted[1:]:
        if d not in names:
            anki("createDeck", deck=d)
        anki("setDeckConfigId", decks=[d], configId=cid)


def import_ready(kind: str) -> int:
    """Import what is ready, in study order: the questions of the verified chunks, group by group, up to the first
    source card that has no verified question yet. New cards take their position from the order they are added in, so
    a later card is never added before an earlier one of its group."""
    state_file = HOME / f"{kind}-state.json"
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
    pool = {}
    for nn, stage in state.items():
        f = HOME / f"{kind}-bulk-{nn}.json"
        if stage == "verified" and f.exists():
            pool.update({q["source"]: q for q in json.loads(f.read_text(encoding="utf-8"))})
    src, have = sources(kind), done(kind)
    ready, waiting = [], {}
    for group in dict.fromkeys(s["group"] for s in src):
        for s in (x for x in src if x["group"] == group):
            if s["id"] in have:
                continue
            if s["id"] not in pool:
                waiting[group or SETS[kind]["deck"]] = s["id"]
                break
            ready.append(pool[s["id"]])
    for g, sid in waiting.items():
        print(f"  {g}: waits for {sid}")
    if not ready:
        print(f"{kind}: nothing ready to import")
        return 0
    return import_questions(kind, ready, update=False, src=src)


def import_file(kind: str, path: Path, update: bool) -> int:
    return import_questions(kind, json.loads(path.read_text(encoding="utf-8")), update)


def import_questions(kind: str, questions: list[dict], update: bool, src: list[dict] | None = None) -> int:
    cfg = dq.SETS[kind]
    src = src or sources(kind)
    by_id = {s["id"]: s for s in src}
    bad = lint_file(kind, questions, set(by_id))
    for i, e in bad:
        print(f"  question {i + 1}: {e}" if i >= 0 else f"  whole file: {e}")
    if bad:
        print("nothing imported")
        return 1
    ensure_deck(kind, src)
    groups = _siblings(src)
    have = done(kind)
    titles = {**{k: v["title"] for k, v in have.items()}, **{q["source"]: q["title"] for q in questions}}
    today = str(datetime.date.today())
    notes, records, updated = [], [], 0
    for q in questions:
        s = by_id[q["source"]]
        qid = f"{cfg['tag']}-" + hashlib.sha1(q["source"].encode()).hexdigest()[:10]
        if q["source"] in have and not update:
            continue
        order = list(range(len(q["options"])))
        random.Random(qid).shuffle(order)
        letters = "ABCDE"
        opts = "".join(f'<div class="opt tappable" data-k="{letters[pos]}" onclick="qkTap(this)"><span class="k">{letters[pos]}</span>'
                       f'<div class="body">{html.escape(q["options"][i])}</div></div>' for pos, i in enumerate(order))
        multi = isinstance(q["correct"], list)
        right = sorted(letters[order.index(i)] for i in (q["correct"] if multi else [q["correct"]]))
        answer = "；".join(f'{k}. {html.escape(q["options"][order[letters.index(k)]])}' for k in right)
        fields = {"Question": dq.question_html(q), "Opts": opts, "Correct": "".join(right), "Answer": answer, "Why": html.escape(q["why"]),
                  "Crumb": html.escape(SETS[kind]["crumb"]), "Point": html.escape(q["point"]), "Full": _full(s, groups[s["deck"]], titles)}
        if q["source"] in have:
            anki("updateNoteFields", note={"id": have[q["source"]]["note"], "fields": fields})
            updated += 1
            continue
        deck = f"{cfg['deck']}::{s['group']}" if s["group"] else cfg["deck"]
        notes.append({"deckName": deck, "modelName": MODELS[1] if multi else MODELS[0], "fields": fields,
                      "tags": [cfg["tag"], f"{cfg['tag']}::{today}", f"{cfg['tag']}::id::{qid}"], "options": {"allowDuplicate": True}})
        records.append({"id": qid, "date": today, "source": q["source"], "topic": q["topic"], "point": q["point"], "title": q["title"], "home": ""})
    if notes:
        ids = anki("addNotes", notes=notes)
        with (HOME / cfg["questions"]).open("a", encoding="utf-8") as fh:
            for rec, nid in zip(records, ids):
                fh.write(json.dumps({**rec, "note": nid}, ensure_ascii=False) + "\n")
    if notes or updated:
        anki("sync")
    print(f"{len(notes)} question(s) added to {cfg['deck']}" + (f", {updated} updated" if updated else ""))
    return 0


def refresh_full(kind: str) -> int:
    src = sources(kind)
    by_id, groups, have = {s["id"]: s for s in src}, _siblings(src), done(kind)
    titles = {k: v["title"] for k, v in have.items()}
    changed, gone = 0, 0
    notes = {n["noteId"]: n for i in range(0, len(have), 200) for n in anki("notesInfo", notes=[q["note"] for q in list(have.values())[i:i + 200]])}
    for source, q in have.items():
        n, s = notes.get(q["note"]), by_id.get(source)
        if not n:
            continue
        if not s:
            gone += 1
            continue
        want = _full(s, groups[s["deck"]], titles)
        if n["fields"]["Full"]["value"] != want:
            anki("updateNoteFields", note={"id": n["noteId"], "fields": {"Full": want}})
            changed += 1
    print(f"{kind}: {len(have)} questions; {changed} backs updated; {gone} whose source card is gone or suspended")
    if changed:
        anki("sync")
    return 0


def review(kind: str, nn: str, show: bool) -> int:
    todo_file = HOME / f"{kind}-todo-{nn}.md"
    want = re.findall(r"^- source: (\S+)", todo_file.read_text(encoding="utf-8"), flags=re.M)
    parts = sorted(HOME.glob(f"{kind}-bulk-{nn}.part*.json"))
    qs = [q for p in parts for q in json.loads(p.read_text(encoding="utf-8"))]
    got = [q.get("source") for q in qs]
    problems = []
    if got != want:
        problems.append(f"sources differ from the todo file: {len(got)} written, {len(want)} wanted; missing "
                        f"{[x for x in want if x not in got][:5]}, extra {[x for x in got if x not in want][:5]}"
                        + ("" if set(got) != set(want) else " (same set, different order)"))
    problems += [f"{i + 1 if i >= 0 else 'file'}: {e}" for i, e in lint_file(kind, qs)]
    single = [q for q in qs if isinstance(q.get("correct"), int)]
    longest = sum(1 for q in single if len(q["options"][q["correct"]]) > max(len(o) for k, o in enumerate(q["options"]) if k != q["correct"]))
    print(f"{kind} chunk {nn}: {len(qs)} questions in {len(parts)} part(s); {len(qs) - len(single)} multi-select; "
          f"right option longest in {longest}/{len(single)}; {len(problems)} problem(s)")
    for p in problems:
        print("  ", p)
    if show:
        for i, q in enumerate(qs, 1):
            right = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
            print(f"{i}. {q['title']} ｜ {q.get('statement', '')} ｜ {q['question']}")
            print("   ✓ " + " + ".join(q["options"][k] for k in right) + " ✗ " + " / ".join(o for k, o in enumerate(q["options"]) if k not in right))
            print(f"   why: {q['why']} 〔{q['point']}〕")
    if not problems:
        (HOME / f"{kind}-bulk-{nn}.json").write_text(json.dumps(qs, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"merged -> sources/local/quiz/{kind}-bulk-{nn}.json")
    return 1 if problems else 0


def chunks(kind: str, mark: tuple[str, str] | None = None) -> int:
    """Where each chunk stands: written (part files exist) → verified (marked by the orchestrator once the verifier's
    report is read) → imported (every source of the chunk has a question in Anki). `mark` sets a chunk's stage."""
    state_file = HOME / f"{kind}-state.json"
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
    if mark:
        state[mark[0]] = mark[1]
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    have = done(kind)
    line = []
    for f in sorted(HOME.glob(f"{kind}-todo-[0-9][0-9].md")):
        nn = f.stem[-2:]
        want = re.findall(r"^- source: (\S+)", f.read_text(encoding="utf-8"), flags=re.M)
        if want and all(x in have for x in want):
            stage = "imported"
        elif state.get(nn):
            stage = state[nn]
        elif list(HOME.glob(f"{kind}-bulk-{nn}.part*.json")):
            stage = "written"
        else:
            stage = "-"
        line.append(f"{nn}:{stage}")
    print(f"{kind}: " + "  ".join(line))
    return 0


def main() -> int:
    args = sys.argv[1:]
    if len(args) < 2 or args[1] not in SETS:
        print(__doc__)
        return 2
    cmd, kind = args[0], args[1]
    if cmd == "status":
        return status(kind)
    if cmd == "chunks":
        return chunks(kind, (args[2], args[3]) if len(args) > 3 else None)
    if cmd == "todo":
        return todo(kind, int(args[args.index("--chunk") + 1]) if "--chunk" in args else 60,
                    int(args[args.index("--start") + 1]) if "--start" in args else 1)
    if cmd == "import-ready":
        return import_ready(kind)
    if cmd == "lint":
        qs = json.loads(Path(args[2]).read_text(encoding="utf-8"))
        bad = lint_file(kind, qs)
        for i, e in bad:
            print(f"  question {i + 1}: {e}" if i >= 0 else f"  whole file: {e}")
        print(f"{len(qs)} questions pass the lint" if not bad else f"{len({i for i, _ in bad})} of {len(qs)} questions fail the lint")
        return 1 if bad else 0
    if cmd == "review":
        return review(kind, args[2], "--show" in args)
    if cmd == "import":
        return import_file(kind, Path(args[2]), "--update" in args)
    if cmd == "full":
        return refresh_full(kind)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
