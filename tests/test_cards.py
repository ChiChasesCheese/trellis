import pytest

from trellis.cards import CardError, load_cards, parse_card

QA = """---
id: my-card
node: alpha.one
type: qa
tags: [core]
---
## Q
What is X?

## A
X is **Y**.
"""

CLOZE = """---
id: my-cloze
node: alpha.one
type: cloze
---
The formula is {{c1::W + R > N}}.
"""


def write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_parse_qa(tmp_path):
    card = parse_card(write(tmp_path, "my-card.md", QA))
    assert card.id == "my-card"
    assert card.question == "What is X?"
    assert card.answer == "X is **Y**."
    assert card.tags == ["core"]


def test_parse_cloze(tmp_path):
    card = parse_card(write(tmp_path, "my-cloze.md", CLOZE))
    assert card.type == "cloze"
    assert "{{c1::" in card.text


@pytest.mark.parametrize("mutation, fragment", [
    (QA.replace("## A\n", ""), "'## Q' section then '## A'"),
    (QA.replace("id: my-card", "id: My Card"), "invalid id"),
    (QA.replace("node: alpha.one\n", ""), "missing node"),
    (QA.replace("type: qa", "type: basic"), "type must be one of"),
    (QA.replace("tags: [core]", "extra: 1"), "unknown frontmatter"),
    (CLOZE.replace("{{c1::", "(("), "no {{c1::"),
    ("no frontmatter at all", "missing YAML frontmatter"),
])
def test_rejects_bad_cards(tmp_path, mutation, fragment):
    with pytest.raises(CardError, match=fragment):
        parse_card(write(tmp_path, "bad.md", mutation))


def test_load_cards_collects_errors_without_hiding_good_files(tmp_path):
    write(tmp_path, "my-card.md", QA)
    write(tmp_path, "bad.md", "broken")
    cards, errors = load_cards(tmp_path)
    assert [c.id for c in cards] == ["my-card"]
    assert len(errors) == 1


TRANSLATED = """---
id: my-card
node: alpha.one
type: qa
---
## Q
What is X?

## A
X is **Y**.

## Q zh
X 是什么？

## A zh
X 是 **Y**。
"""

CLOZE_TRANSLATED = """---
id: my-cloze
node: alpha.one
type: cloze
---
The formula is {{c1::W + R > N}}.

## zh
公式是 {{c1::W + R > N}}。
"""


def test_translation_sits_beside_the_english_never_replacing_it(tmp_path):
    card = parse_card(write(tmp_path, "my-card.md", TRANSLATED))
    assert card.question == "What is X?"          # English is untouched
    assert card.render() == ("What is X?", "X is **Y**.")
    assert card.render("zh") == ("X 是什么？", "X 是 **Y**。")


def test_a_card_without_the_language_falls_back_to_english(tmp_path):
    card = parse_card(write(tmp_path, "my-card.md", QA))
    assert card.render("zh") == ("What is X?", "X is **Y**.")


def test_cloze_translation_keeps_its_deletion(tmp_path):
    card = parse_card(write(tmp_path, "my-cloze.md", CLOZE_TRANSLATED))
    assert card.render("zh")[0] == "公式是 {{c1::W + R > N}}。"


@pytest.mark.parametrize("mutation, fragment", [
    (TRANSLATED.replace("## A zh\nX 是 **Y**。\n", ""), "missing \\['answer'\\]"),
    (CLOZE_TRANSLATED.replace("{{c1::W + R > N}}。", "W + R > N。"), "no \\{\\{c1"),
    (TRANSLATED.replace("## Q zh", "## Notes"), "unknown section"),
])
def test_half_a_translation_is_rejected(tmp_path, mutation, fragment):
    with pytest.raises(CardError, match=fragment):
        parse_card(write(tmp_path, "bad.md", mutation))


def test_language_does_not_change_a_cards_identity(tmp_path):
    """The same card in two languages is one card: same id, so re-importing
    a translated build replaces the text in place and review history lives."""
    import genanki
    en = parse_card(write(tmp_path, "my-card.md", QA))
    zh = parse_card(write(tmp_path, "my-card.md", TRANSLATED))
    assert genanki.guid_for(f"trellis:{en.id}") == genanki.guid_for(f"trellis:{zh.id}")


@pytest.mark.parametrize("zh, fragment", [
    # what a cheap model actually did to these cards, in miniature
    # dropped two probes
    ("公式是 {{c1::W + R > N}}。", "deletions \\['1'\\] but the English card has"),
    # invented a fourth probe
    ("{{c1::W + R > N}}，容忍 {{c2::一个}}，{{c3::3}} 副本，{{c4::多余的}}。",
     "may not add or drop"),
    # re-worded a quantity into prose
    ("需要 {{c1::W + R > N}}，容忍 {{c2::一个}} 节点，在 {{c3::三}} 副本下。",
     "lost the number"),
])
def test_a_translation_may_not_change_what_a_cloze_tests(tmp_path, zh, fragment):
    body = ("---\nid: c\nnode: alpha.one\ntype: cloze\n---\n"
            "Needs {{c1::W + R > N}}, tolerating {{c2::one}} node down "
            "at {{c3::3}} replicas.\n\n## zh\n" + zh + "\n")
    with pytest.raises(CardError, match=fragment):
        parse_card(write(tmp_path, "c.md", body))


def test_a_faithful_cloze_translation_passes(tmp_path):
    body = ("---\nid: c\nnode: alpha.one\ntype: cloze\n---\n"
            "Needs {{c1::W + R > N}}, tolerating {{c2::one}} node down "
            "at {{c3::3}} replicas.\n\n## zh\n"
            "需要 {{c1::W + R > N}}，在 {{c3::3}} 副本下容忍 {{c2::一个}} 节点故障。\n")
    card = parse_card(write(tmp_path, "c.md", body))
    assert "{{c2::一个}}" in card.render("zh")[0]


def test_a_rewritten_translation_is_flagged_without_breaking_the_english_card(tmp_path):
    """A model that answers the question from its own knowledge tends to
    bring a code block the English card never had. That must not take the
    English card down with it — it is still correct — so it is reported,
    and shipping that language is what gets blocked."""
    from trellis.cards import suspect_translations

    body = QA + "\n## Q zh\nX 是什么？\n\n## A zh\n看这段代码：\n\n```java\nclass X {}\n```\n"
    card = parse_card(write(tmp_path, "my-card.md", body))
    assert card.render()[0] == "What is X?"      # English unharmed
    assert suspect_translations(card) == ["zh"]


def test_a_faithful_translation_is_not_flagged(tmp_path):
    from trellis.cards import suspect_translations
    assert suspect_translations(parse_card(write(tmp_path, "c.md", TRANSLATED))) == []


def test_a_duplicate_pasted_underneath_is_flagged(tmp_path):
    """Two writers appending to the same card leave a second copy with no
    heading of its own, so the repeated-heading check cannot see it — but
    the translation ends up far longer than its source."""
    from trellis.cards import suspect_translations

    dup = QA + "\n## Q zh\nX 是什么？\n\n## A zh\nX 是 **Y**。\n\nX 是什么？\nX 是 **Y**。\n" \
                "X 是什么？\nX 是 **Y**。\nX 是什么？\nX 是 **Y**。\n"
    assert suspect_translations(parse_card(write(tmp_path, "my-card.md", dup))) == ["zh"]


def test_a_card_can_share_its_body_with_other_decks(tmp_path):
    from trellis.cards import parse_card
    vault = tmp_path / "vault"
    (vault / "problems").mkdir(parents=True)
    (vault / "deck").mkdir()
    (vault / "problems" / "two-sum.md").write_text(
        "---\ntitle: two-sum\n---\n## Q\n**LC 1 两数之和**｜Easy\n\n题意。\n\n## A\n哈希表。\n", encoding="utf-8")
    stub = vault / "deck" / "c.md"
    stub.write_text("---\nid: tlc-tops-two-sum-0-whole\nnode: a.two-sum\ntype: qa\nbody: problems/two-sum\n"
                    "meta: Easy · 全公司热度第 1 名\n---\n", encoding="utf-8")
    card = parse_card(stub)
    assert "**LC 1 两数之和**｜Easy · 全公司热度第 1 名" in card.question and card.answer.strip() == "哈希表。"
