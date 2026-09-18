#!/usr/bin/env python3
"""Grade an interview transcript the way we grade a mock: turns → speech → grammar → topics → rubric.

  uv run --extra debrief python vault/interviews/core/debrief/analyze.py <debrief-dir>
      [--bank <kit>/loop/rounds/<round>/bank.json] [--speakers speakers.json] [--no-grammar]
      [--candidate-only [--gap 6]]

<debrief-dir> must hold transcript.json from transcribe.py. Writes there:
  turns.md      the conversation split into AI / me turns (check this first; fix mistakes via --speakers)
  metrics.json  every number the report cites
  report.md     speech metrics · grammar (LanguageTool) · question ↔ bank match + keyword coverage ·
                JD-line hits · per-answer rubric heuristic (3/2/1) · action list

--candidate-only: the recording captured only the candidate's microphone (a screen/mic recorder
during an AI screen does exactly this). Every segment is "me"; answers are split where the audio
goes quiet for more than --gap seconds (the interviewer was speaking), and each answer is matched
back to the bank question whose text + keys it overlaps most.

Speaker attribution is a heuristic (an AI interviewer asks questions; the candidate answers).
It is shown, not hidden: read turns.md, and if a segment is mislabelled write
  {"12": "ai", "40": "me"}   (segment id → speaker)
to speakers.json and pass --speakers. Rule-based scoring is a first pass — the human review
(REVIEW.md next to the report) is where judgement lives.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------- lexicons (edit freely)

INTERVIEWER_OPENERS = re.compile(
    r"^(thank you|thanks|great|got it|okay|ok|alright|perfect|understood|sounds good|interesting|"
    r"let's|now|next|moving on|before we|to wrap up|that's all|we have|we're|we'll|i'd like|i would like|"
    r"can you|could you|would you|tell me|walk me|describe|explain|share|imagine|suppose|say you|"
    r"how |what |why |when |where |which |who |do you|did you|have you|are you|is there|were there)",
    re.I,
)
FILLERS = ["um", "uh", "er", "hmm", "like", "you know", "actually", "basically", "kind of", "sort of", "i mean", "so yeah", "right?"]
OWNERSHIP = re.compile(r"\b(I|I've|I'd|I'm)\s+(designed|built|build|owned|own|decided|decide|wrote|write|led|lead|proposed|propose|implemented|implement|created|create|migrated|migrate|drove|drive|chose|choose|made the call|took ownership|was the owner|am the owner)\b", re.I)
STRUCTURE = re.compile(r"\b(first(ly)?|second(ly)?|third(ly)?|then|finally|next|lastly|step one|step two|option a|option b|on the other hand)\b", re.I)
LEARNING = re.compile(r"\b(trade-?off|learned|lesson|takeaway|would do differently|the cost (is|was)|instead of|in hindsight|looking back|the downside|the risk|the price|what i'd change)\b", re.I)
NUMBERS = re.compile(r"\b(\d[\d,.]*\s*(%|percent|million|billion|thousand|k|m|b|rows?|merchants?|transactions?|dollars?|seconds?|minutes?|hours?|days?|weeks?|months?|years?|lines?|prs?|times?)?|one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|million|billion|dozen|half|double|twice)\b", re.I)
MECHANISM = [
    # Snowflake / database internals
    "stream", "task", "stored procedure", "procedure", "udtf", "table function", "merge", "copy into", "snowpipe",
    "micro-partition", "partition", "pruning", "clustering", "cluster key", "zero-copy", "clone", "time travel",
    "warehouse", "dynamic table", "iceberg", "flyway", "migration", "dag", "idempoten", "upsert", "primary key",
    "composite key", "unique key", "full outer join", "join", "cte", "window", "materialized", "variant", "secure view",
    "result_scan", "execute immediate", "stream_has_data", "trigger status", "handshake", "quality check", "health check",
    # distributed systems / backend
    "kafka", "cdc", "at-least-once", "exactly-once", "offset", "replay", "retry", "backfill", "feature flag", "toggle",
    "shadow", "reconcil", "ledger", "grpc", "rest", "s3", "airflow", "spark", "kubernetes", "terraform", "datadog",
    "pagerduty", "streamlit", "postmortem", "rca", "root cause", "sla", "canary", "rollback", "throughput", "latency", "p99",
    # languages / tooling
    "java", "kotlin", "python", "sql", "gradle", "spring", "protobuf", "claude code", "adr", "design doc",
]
JD_LINES = {
    "SQL": ["sql", "stored procedure", "merge", "join", "cte", "query", "udtf", "table function"],
    "distributed systems": ["distributed", "idempoten", "exactly-once", "at-least-once", "kafka", "cdc", "consistency", "replay", "retry", "reconcil", "handshake", "offset", "partition"],
    "Java": ["java", "kotlin", "gradle", "spring", "jvm"],
    "database internals": ["micro-partition", "pruning", "clustering", "zero-copy", "clone", "time travel", "warehouse", "stream", "task", "dynamic table", "iceberg", "metadata", "columnar"],
    "large-scale production": ["million", "billion", "production", "prod", "on-call", "oncall", "incident", "page", "sla", "scale", "per day", "a day"],
}
GRAMMAR_SKIP_CATEGORIES = {"TYPOGRAPHY", "PUNCTUATION", "CASING", "REDUNDANCY"}  # transcript punctuation is Whisper's, not yours
GRAMMAR_SKIP_RULES = {"UPPERCASE_SENTENCE_START", "WHITESPACE_RULE", "COMMA_COMPOUND_SENTENCE", "SENTENCE_WHITESPACE", "EN_QUOTES", "DASH_RULE", "MORFOLOGIK_RULE_EN_US"}
STOP = set("the a an and or of to in on for with is are was were be been being it its this that these those i we you he she they my our your his her their me us them at by from as if so but not no yes do does did have has had can could would should will shall may might about into over under than then there here what which who whom when where why how all any some more most very just also really".split())


def fmt(sec: float) -> str:
    sec = max(0, int(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


# ---------------------------------------------------------------- junk filter

HALLUCINATIONS = {"thank you", "thanks", "it's", "the", "this is the", "we'll see you next time", "bye", "you", "so", "..."}


def drop_junk(segments: list[dict]) -> list[dict]:
    """Whisper invents 'Thank you.' / 'It's It's' in silence. Drop segments whose words the model itself
    doubts (mean word probability < 0.35), or that are a bare hallucination phrase."""
    keep = []
    for s in segments:
        text = s["text"].strip()
        if not text:
            continue
        words = s.get("words") or []
        probs = [w.get("probability") for w in words if w.get("probability") is not None]
        mean_p = sum(probs) / len(probs) if probs else 1.0
        norm = re.sub(r"[^a-z' ]", "", text.lower()).strip()
        if norm in HALLUCINATIONS or (mean_p < 0.35 and len(words) <= 4) or s.get("no_speech_prob", 0) > 0.8:
            continue
        keep.append(s)
    return keep


# ---------------------------------------------------------------- turns

def label_segments(segments: list[dict], override: dict[str, str]) -> list[str]:
    labels = []
    for s in segments:
        sid = str(s["id"])
        text = s["text"].strip()
        dur = s["end"] - s["start"]
        if sid in override:
            labels.append(override[sid])
            continue
        is_q = text.endswith("?") or (bool(INTERVIEWER_OPENERS.match(text)) and dur < 25 and len(text.split()) < 60)
        labels.append("ai" if is_q else "me")
    # an "ai" segment sandwiched inside a long candidate run whose text is a statement is usually the candidate
    # ("So yeah…" / "Then…"): keep it simple — a lone "ai" not ending in "?" between two "me" runs → "me"
    for i in range(1, len(labels) - 1):
        if labels[i] == "ai" and labels[i - 1] == "me" and labels[i + 1] == "me" and not segments[i]["text"].strip().endswith("?"):
            labels[i] = "me"
    return labels


def build_turns(segments: list[dict], labels: list[str], gap: float = 0.0) -> list[dict]:
    turns: list[dict] = []
    for s, lab in zip(segments, labels):
        text = s["text"].strip()
        if not text:
            continue
        if turns and turns[-1]["speaker"] == lab and not (gap and s["start"] - turns[-1]["end"] > gap):
            t = turns[-1]
            t["end"] = s["end"]
            t["text"] += " " + text
            t["segments"].append(s["id"])
            t["words"].extend(s.get("words") or [])
        else:
            turns.append({"speaker": lab, "start": s["start"], "end": s["end"], "text": text, "segments": [s["id"]], "words": list(s.get("words") or [])})
    for i, t in enumerate(turns):
        t["i"] = i
        t["dur"] = round(t["end"] - t["start"], 1)
        t["n_words"] = len(re.findall(r"[A-Za-z0-9']+", t["text"]))
    return turns


# ---------------------------------------------------------------- speech metrics

MIN_ANSWER_WORDS = 8  # greetings / "yeah, sure" are not answers


def speech_metrics(turns: list[dict]) -> dict:
    me = [t for t in turns if t["speaker"] == "me" and t["n_words"] >= MIN_ANSWER_WORDS]
    ai = [t for t in turns if t["speaker"] == "ai"]
    total_me = sum(t["dur"] for t in me)
    total_ai = sum(t["dur"] for t in ai)
    substantive = [t for t in turns if t["n_words"] >= MIN_ANSWER_WORDS]
    span = (substantive[-1]["end"] - substantive[0]["start"]) if substantive else 0
    if not ai:  # candidate-only recording: the interviewer's time is the silence between my answers
        total_ai = max(0.0, span - total_me)
    words_me = sum(t["n_words"] for t in me)
    text_me = " ".join(t["text"] for t in me).lower()
    fillers = {f: len(re.findall(rf"(?<![a-z]){re.escape(f)}(?![a-z])", text_me)) for f in FILLERS}
    fillers = {k: v for k, v in fillers.items() if v}
    stutters = len(re.findall(r"\b(\w+)\s+\1\b", text_me))
    pauses, long_pauses = [], []
    for t in me:
        ws = t["words"]
        for a, b in zip(ws, ws[1:]):
            gap = (b.get("start") or 0) - (a.get("end") or 0)
            if gap > 1.0:
                pauses.append(gap)
            if gap > 2.5:
                long_pauses.append((fmt(a.get("end") or 0), round(gap, 1)))
    per_answer = [{"i": t["i"], "start": fmt(t["start"]), "dur": t["dur"], "words": t["n_words"], "wpm": round(t["n_words"] / t["dur"] * 60) if t["dur"] > 0 else 0} for t in me]
    return {
        "talk_time_me_s": round(total_me), "talk_time_ai_s": round(total_ai), "conversation_span_s": round(span),
        "share_me": round(total_me / (total_me + total_ai), 2) if total_me + total_ai else 0,
        "words_me": words_me, "wpm_me": round(words_me / total_me * 60) if total_me else 0,
        "answers": len(me), "answers_over_90s": sum(1 for t in me if t["dur"] > 90), "longest_answer_s": max((t["dur"] for t in me), default=0),
        "fillers": fillers, "fillers_total": sum(fillers.values()), "fillers_per_100_words": round(sum(fillers.values()) / words_me * 100, 1) if words_me else 0,
        "stutters": stutters, "pauses_over_1s": len(pauses), "long_pauses": long_pauses[:15], "per_answer": per_answer,
    }


# ---------------------------------------------------------------- grammar

def grammar(turns: list[dict]) -> dict:
    try:
        import language_tool_python  # noqa: WPS433
    except ImportError:
        return {"skipped": "language_tool_python not installed"}
    try:
        tool = language_tool_python.LanguageTool("en-US")
    except Exception as e:  # Java missing, download failed…
        return {"skipped": f"LanguageTool unavailable: {e}"}
    by_rule: Counter = Counter()
    by_cat: Counter = Counter()
    examples: dict[str, list] = defaultdict(list)
    per_turn = {}
    total_words = 0
    for t in turns:
        if t["speaker"] != "me" or t["n_words"] < MIN_ANSWER_WORDS:
            continue
        total_words += t["n_words"]
        n = 0
        for m in tool.check(t["text"]):
            rule = getattr(m, "rule_id", None) or getattr(m, "ruleId", "") or ""  # attribute name differs across versions
            cat = getattr(m, "category", "") or ""
            if cat in GRAMMAR_SKIP_CATEGORIES or rule in GRAMMAR_SKIP_RULES:
                continue
            n += 1
            by_rule[rule] += 1
            by_cat[cat] += 1
            if len(examples[rule]) < 3:
                examples[rule].append({"turn": t["i"], "at": fmt(t["start"]), "context": getattr(m, "context", ""), "message": getattr(m, "message", ""), "fix": (getattr(m, "replacements", None) or [""])[0]})
        per_turn[t["i"]] = n
    tool.close()
    total = sum(by_rule.values())
    return {
        "issues": total, "per_100_words": round(total / total_words * 100, 1) if total_words else 0,
        "by_category": dict(by_cat.most_common()), "by_rule": dict(by_rule.most_common(15)), "examples": dict(examples), "per_turn": per_turn,
    }


# ---------------------------------------------------------------- topics: question ↔ bank, keys coverage, JD lines

def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z'\-]+", text.lower()) if w not in STOP and len(w) > 2}


def match_bank(question: str, bank: list[dict]) -> tuple[dict | None, float]:
    q = content_words(question)
    best, score = None, 0.0
    for item in bank:
        b = content_words(item["q"])
        if not q or not b:
            continue
        j = len(q & b) / len(q | b)
        if j > score:
            best, score = item, j
    return best, round(score, 2)


def match_bank_by_answer(answer: str, bank: list[dict]) -> tuple[dict | None, float]:
    """candidate-only mode: which bank question does this answer look like an answer to?"""
    a = content_words(answer)
    best, score = None, 0.0
    for item in bank:
        hits, misses = key_hits(item.get("keys", ""), answer)
        ratio = len(hits) / (len(hits) + len(misses)) if hits or misses else 0.0
        b = content_words(item["q"])
        j = len(a & b) / len(b) if b else 0.0
        sc = 0.7 * ratio + 0.3 * j
        if sc > score:
            best, score = item, sc
    return best, round(score, 2)


def key_hits(keys: str, answer: str) -> tuple[list[str], list[str]]:
    a = answer.lower()
    hit, miss = [], []
    for k in [k.strip() for k in keys.split("·") if k.strip()]:
        words = [w for w in content_words(k) if len(w) > 3]
        if not words:
            continue
        found = sum(1 for w in words if w.rstrip("s") in a or w in a)
        (hit if found >= max(1, len(words) // 2) else miss).append(k)
    return hit, miss


def rubric(answer: dict) -> dict:
    text = answer["text"]
    low = text.lower()
    signals = {
        "ownership": bool(OWNERSHIP.search(text)),
        "mechanism": sum(1 for m in MECHANISM if m in low) >= 2,
        "number": bool(NUMBERS.search(text)),
        "structure": bool(STRUCTURE.search(text)),
        "learning": bool(LEARNING.search(text)),
        "length_ok": answer["dur"] <= 100,
    }
    core = sum(signals[k] for k in ("ownership", "mechanism", "number", "learning"))
    score = 3 if core >= 3 and signals["length_ok"] else 2 if core >= 2 else 1
    mech = sorted({m for m in MECHANISM if m in low})
    return {"score": score, "signals": signals, "mechanisms": mech[:12]}


def jd_hits(text: str) -> dict:
    low = text.lower()
    return {line: sum(low.count(t) for t in terms) for line, terms in JD_LINES.items()}


# ---------------------------------------------------------------- report

def write_turns(turns: list[dict], path: Path) -> None:
    lines = ["# turns · AI vs me（启发式标注，错了写 speakers.json 再跑）", ""]
    for t in turns:
        who = "**AI**" if t["speaker"] == "ai" else "me"
        lines.append(f"### {t['i']:02d} · {who} · {fmt(t['start'])}–{fmt(t['end'])} · {t['dur']} s · {t['n_words']} words · segs {t['segments'][0]}–{t['segments'][-1]}")
        lines.append("")
        lines.append(t["text"])
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_report(m: dict, path: Path, bank_path: Path | None) -> None:
    sp, gr, qa = m["speech"], m["grammar"], m["qa"]
    L = [f"# report · {m['meta'].get('audio', '').split('/')[-1]}", "", f"> 生成：`analyze.py`（启发式打分，判断在 REVIEW.md）· 转写：{m['meta'].get('backend')} {m['meta'].get('model')} · 题库：`{bank_path or '—'}`", ""]

    L += ["## 1. 说话与节奏", "", "| 指标 | 值 | 参考 |", "|---|---|---|",
          f"| 对话窗口 / 我说话时长 / 占比 | {fmt(sp['conversation_span_s'])} / {fmt(sp['talk_time_me_s'])} / {int(sp['share_me']*100)}% | Chakra 20 min 里候选人 70–80% 正常；candidate-only 时 AI 时长 = 窗口内的静音 |",
          f"| 语速（WPM） | {sp['wpm_me']} | 英语面试舒适区 130–160；< 110 显得犹豫 |",
          f"| 回答数 / 超过 90 s 的 | {sp['answers']} / {sp['answers_over_90s']} | 首答 ≤ 90 s，最长 {int(sp['longest_answer_s'])} s |",
          f"| 填充词 | {sp['fillers_total']}（每百词 {sp['fillers_per_100_words']}） | > 3/百词 明显；top：{', '.join(f'{k}×{v}' for k, v in sorted(sp['fillers'].items(), key=lambda x: -x[1])[:6])} |",
          f"| 重复词（the the）| {sp['stutters']} | |",
          f"| > 1 s 停顿 / > 2.5 s 长停顿 | {sp['pauses_over_1s']} / {len(sp['long_pauses'])} | 长停顿位置：{', '.join(f'{a}({b}s)' for a, b in sp['long_pauses'][:8])} |", ""]
    L += ["每个回答：", "", "| # | 开始 | 时长 | 词数 | WPM | rubric | 信号 |", "|---|---|---|---|---|---|---|"]
    for a in qa["answers"]:
        sig = "".join("✓" if v else "·" for k, v in a["rubric"]["signals"].items())
        L.append(f"| {a['i']:02d} | {a['start']} | {a['dur']} s | {a['words']} | {a['wpm']} | **{a['rubric']['score']}** | {sig} (own·mech·num·struct·learn·len) |")
    L.append("")

    L += ["## 2. 语法（LanguageTool en-US，已剔除标点/大小写类）", ""]
    if "skipped" in gr:
        L.append(f"跳过：{gr['skipped']}")
    else:
        L += [f"共 {gr['issues']} 处，每百词 {gr['per_100_words']}。按类别：{', '.join(f'{k} {v}' for k, v in gr['by_category'].items())}", "", "| 规则 | 次数 | 例子（上下文 → 建议） |", "|---|---|---|"]
        for rule, n in gr["by_rule"].items():
            ex = gr["examples"].get(rule, [])
            exs = "<br>".join(f"{e['at']} `{e['context'].strip()}` → **{e['fix']}**（{e['message']}）" for e in ex[:2])
            L.append(f"| `{rule}` | {n} | {exs} |")
    L.append("")

    L += ["## 3. 题 ↔ 题库 · 关键词覆盖", "", "AI 每一问匹配到题库里最接近的题（Jaccard），再看紧接着的回答说出了几个 keys。candidate-only 模式下题目由回答反推（keys 命中率 + 题面重合）。", "", "| 问 / 回答（时间） | 匹配题 | 相似度 | keys 命中 | 缺的 keys |", "|---|---|---|---|---|"]
    for q in qa["questions"]:
        mq = q["match"]
        L.append(f"| {q['at']} {q['q'][:90]}… | {mq['id'] + ' ' + mq['q'][:50] if mq else '—'} | {q['sim']} | {q['hits']}/{q['hits']+q['misses']} | {'; '.join(q['miss_keys'][:4])} |")
    L.append("")
    L += ["## 4. JD 线命中（整场我的发言里出现次数）", "", "| JD 线 | 次数 |", "|---|---|"]
    for k, v in qa["jd"].items():
        L.append(f"| {k} | {v} |")
    L += ["", f"说出口的原语/工具名（去重）：{', '.join(qa['mechanisms_all'][:40])}", ""]

    L += ["## 5. 自动结论（给 REVIEW.md 起草用）", ""]
    tips = []
    if sp["wpm_me"] < 115:
        tips.append(f"语速 {sp['wpm_me']} WPM 偏慢——不是词汇问题，是每句话前的思考停顿；练法：每个故事先背 headline 一句，开口就说它。")
    if sp["fillers_per_100_words"] > 3:
        top = sorted(sp["fillers"].items(), key=lambda x: -x[1])[:3]
        tips.append(f"填充词每百词 {sp['fillers_per_100_words']}，主要是 {', '.join(k for k, _ in top)}——用停顿代替，transcript 打分对停顿免疫，对 'like' 不免疫。")
    if sp["answers_over_90s"]:
        tips.append(f"{sp['answers_over_90s']} 个回答超过 90 s——AI 会切段；首答只讲 headline → mechanism → 数字 → learning，细节留给追问。")
    low_rubric = [a for a in qa["answers"] if a["rubric"]["score"] <= 1 and a["words"] > 40]
    if low_rubric:
        tips.append("rubric=1 的长回答：" + ", ".join(f"#{a['i']:02d}({a['start']})" for a in low_rubric) + "——缺 ownership/mechanism/number/learning 中至少三项。")
    weak_lines = [k for k, v in qa["jd"].items() if v < 3]
    if weak_lines:
        tips.append("JD 线几乎没提到：" + ", ".join(weak_lines) + "——Chakra 对 must-have 加权，没说 = 0。")
    if isinstance(gr, dict) and "by_rule" in gr and gr["by_rule"]:
        tips.append("语法 top 规则：" + ", ".join(list(gr["by_rule"])[:3]) + "——见 §2 的例子，每条练 5 句替换。")
    L += [f"- {t}" for t in tips] or ["- 无自动提示。"]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("debrief_dir", type=Path)
    ap.add_argument("--bank", type=Path, default=None, help="kit bank.json to match questions and keys against")
    ap.add_argument("--speakers", type=Path, default=None, help="segment id → 'ai'|'me' overrides")
    ap.add_argument("--no-grammar", action="store_true")
    ap.add_argument("--candidate-only", action="store_true", help="recording has only my microphone: no AI turns")
    ap.add_argument("--gap", type=float, default=6.0, help="candidate-only: silence (s) that separates two answers")
    a = ap.parse_args()

    tj = a.debrief_dir / "transcript.json"
    if not tj.exists():
        sys.exit(f"missing {tj} — run transcribe.py first")
    data = json.loads(tj.read_text(encoding="utf-8"))
    segments = drop_junk(data["segments"])
    override = json.loads(a.speakers.read_text()) if a.speakers and a.speakers.exists() else {}
    labels = ["me"] * len(segments) if a.candidate_only else label_segments(segments, override)
    turns = build_turns(segments, labels, gap=a.gap if a.candidate_only else 0.0)
    write_turns(turns, a.debrief_dir / "turns.md")

    speech = speech_metrics(turns)
    gr = {"skipped": "--no-grammar"} if a.no_grammar else grammar(turns)

    bank = json.loads(a.bank.read_text(encoding="utf-8")) if a.bank else []
    questions, answers = [], []
    for i, t in enumerate(turns):
        if t["speaker"] == "me":
            if t["n_words"] < MIN_ANSWER_WORDS:
                continue
            r = rubric(t)
            answers.append({"i": t["i"], "start": fmt(t["start"]), "dur": t["dur"], "words": t["n_words"], "wpm": round(t["n_words"] / t["dur"] * 60) if t["dur"] else 0, "rubric": r})
            if a.candidate_only and bank and t["n_words"] >= 25:
                match, sim = match_bank_by_answer(t["text"], bank)
                if sim < 0.3:
                    match = None
                hits, misses = key_hits(match["keys"], t["text"]) if match else ([], [])
                questions.append({"i": t["i"], "at": fmt(t["start"]), "q": f"(inferred from answer #{t['i']:02d}) " + t["text"][:70], "match": ({"id": match["id"], "q": match["q"], "story": match.get("story", "")} if match else None), "sim": sim, "hits": len(hits), "misses": len(misses), "hit_keys": hits, "miss_keys": misses, "answer_turn": t["i"]})
            continue
        nxt = turns[i + 1] if i + 1 < len(turns) and turns[i + 1]["speaker"] == "me" else None
        match, sim = match_bank(t["text"], bank) if bank else (None, 0.0)
        hits, misses = key_hits(match["keys"], nxt["text"]) if (match and nxt) else ([], [])
        questions.append({"i": t["i"], "at": fmt(t["start"]), "q": t["text"], "match": ({"id": match["id"], "q": match["q"], "story": match.get("story", "")} if match else None), "sim": sim, "hits": len(hits), "misses": len(misses), "hit_keys": hits, "miss_keys": misses, "answer_turn": nxt["i"] if nxt else None})
    text_me = " ".join(t["text"] for t in turns if t["speaker"] == "me")
    mech_all = sorted({m for m in MECHANISM if m in text_me.lower()})
    metrics = {"meta": data.get("_meta", {}), "speech": speech, "grammar": gr, "qa": {"questions": questions, "answers": answers, "jd": jd_hits(text_me), "mechanisms_all": mech_all}}
    (a.debrief_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=1), encoding="utf-8")
    write_report(metrics, a.debrief_dir / "report.md", a.bank)
    print(f"turns {len(turns)} (ai {sum(1 for t in turns if t['speaker']=='ai')} / me {sum(1 for t in turns if t['speaker']=='me')}) · WPM {speech['wpm_me']} · fillers/100w {speech['fillers_per_100_words']} · grammar {gr.get('issues', gr.get('skipped'))} → {a.debrief_dir / 'report.md'}")


if __name__ == "__main__":
    main()
