import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import card_notes as cn  # noqa: E402


def note(nid=1, text="", answer="", tags=()):
    return {"noteId": nid, "tags": list(tags), "fields": {"Note": {"value": text, "order": 3}, "NoteAnswer": {"value": answer, "order": 4}}}


def test_plain_keeps_lines_and_drops_markup():
    assert cn.plain("为什么<br>线程池&nbsp;会满？<script>x()</script>") == "为什么\n线程池 会满？"


def test_a_question_waits_until_answered_and_again_after_an_edit():
    n = note(text="为什么慢比挂更糟？")
    assert cn.waiting(n, {})
    done = {"1": cn.key("为什么慢比挂更糟？")}
    assert not cn.waiting(n, done)
    assert cn.waiting(note(text="那熔断呢？"), done)


def test_a_star_waits_only_without_an_explanation():
    assert cn.waiting(note(tags=["marked"]), {})
    assert not cn.waiting(note(tags=["marked"], answer="<p>讲解</p>"), {})
    assert not cn.waiting(note(), {})
