from trellis.kp_footer import asked_in, card_title, plain, related, render


def test_plain_drops_english_glosses():
    assert plain("幂等键（Idempotency Key）的去重") == "幂等键的去重"


def test_card_title_takes_the_bold_title_of_the_first_line():
    assert card_title("**幂等键（Key）**｜必会\n\n题干") == "幂等键"


def test_asked_in_ranks_by_role_times_frequency_and_keeps_the_best_role():
    needs = {"q.a": [{"kp": "k", "role": "加分"}, {"kp": "m", "role": "必讲"}], "q.b": [{"kp": "k", "role": "追问"}], "q.c": [{"kp": "x", "role": "必讲"}]}
    own = {"q.d": [{"id": "k", "role": "必讲"}]}
    got = asked_in(["k", "m"], needs, own, {"q.a": 1.0, "q.b": 1.0, "q.d": 0.1}, lambda q: True)
    assert got == [("q.a", "必讲"), ("q.b", "追问"), ("q.d", "必讲")]


def test_asked_in_skips_questions_outside_the_tree():
    needs = {"gone": [{"kp": "k", "role": "必讲"}]}
    assert asked_in(["k"], needs, {}, {"gone": 1.0}, lambda q: False) == []


def test_related_prefers_other_leaves_and_excludes_the_card():
    leaf = {"a": "l1", "b": "l1", "c": "l2"}
    assert related("a", "k", {"k": ["a", "b", "c"]}, leaf) == ["c", "b"]


def test_render_omits_empty_rows_and_escapes():
    html = kp_footer.render([("a<b", "p/t/k")], [], [("c", "c/x")])
    assert "a&lt;b" in html and "常考于" not in html and "<a " not in html  # no site configured: plain text
    linked = kp_footer.render([("a", "p/t/k")], [("q", "t/q", "必讲")], [], "http://h/m")
    assert '<a href="http://h/m#p/t/k">a</a>' in linked and '<a href="http://h/m#t/q">q</a>（必讲）' in linked
