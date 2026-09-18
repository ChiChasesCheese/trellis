"""Run from this folder: `uv run --extra debrief --with pytest python -m pytest -q` (repo root pytest is scoped to tests/)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import analyze  # noqa: E402


def seg(i, text, start, end, prob=0.9, words=None):
    ws = words if words is not None else [{"word": w, "start": start, "end": end, "probability": prob} for w in text.split()]
    return {"id": i, "text": text, "start": start, "end": end, "no_speech_prob": 0.0, "words": ws}


def test_drop_junk_removes_hallucinations_and_keeps_speech():
    segs = [seg(0, "Thank you.", 1, 2), seg(1, "It's It's It's", 3, 4, prob=0.02), seg(2, "I built the pipeline end to end.", 5, 9)]
    kept = analyze.drop_junk(segs)
    assert [s["id"] for s in kept] == [2]


def test_candidate_only_splits_answers_on_silence():
    segs = [seg(0, "first answer part one", 0, 5), seg(1, "part two", 6, 9), seg(2, "second answer", 30, 34)]
    turns = analyze.build_turns(segs, ["me"] * 3, gap=6.0)
    assert len(turns) == 2 and turns[0]["text"].startswith("first") and turns[1]["text"] == "second answer"


def test_key_hits_matches_half_the_content_words():
    keys = "append-only Streams · MERGE on composite key · Java 17 + Gradle"
    hit, miss = analyze.key_hits(keys, "we use six append-only streams and merge on a composite key")
    assert "append-only Streams" in hit and "MERGE on composite key" in hit and "Java 17 + Gradle" in miss


def test_rubric_signals():
    good = {"text": "I designed the MERGE and stream pipeline; it handles 22 million rows. The trade-off was cost.", "dur": 60}
    weak = {"text": "In general the best practice is to be careful.", "dur": 60}
    assert analyze.rubric(good)["score"] == 3
    assert analyze.rubric(weak)["score"] == 1


def test_bank_row_split_keeps_escaped_pipe():
    sys.path.insert(0, str(Path(__file__).parents[1] / ".." / "companies" / "snowflake" / "loop" / "rounds" / "00_ai_screen"))
    import build_bank  # noqa: E402

    cells = build_bank.split_row("| A03 | q | p | S3 | 'BT_' \\|\\| NULL · x | src |")
    assert cells[4] == "'BT_' || NULL · x" and len(cells) == 6
