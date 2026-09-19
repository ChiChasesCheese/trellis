"""`trellis steps`: giving the cards of a leaf their order.

A step is a judgement about teaching — what has to be understood before what
— so it is made by a person or a Runner reading the cards, and Trellis only
asks for it and checks what comes back: every leaf answered with exactly its
own cards, each once. The answer is then written into the card files as one
frontmatter line and nothing else.
"""

from __future__ import annotations

import json

import pytest
import yaml

from trellis.cards import load_cards
from trellis.cli import main

SKELETON = {
    "domain": "demo", "title": "Demo", "lang": "en",
    "nodes": [{"id": "base", "title": "Base", "children": [
        {"id": "base.one", "title": "One", "summary": "The first thing."},
        {"id": "base.two", "title": "Two", "summary": "The second thing."},
    ]}],
}
CARD = "---\nid: {id}\nnode: {node}\ntype: qa\ntags: [kept]   # a comment that must survive\n---\n## Q\n{q}\n\n## A\nAnswer.\n"


@pytest.fixture
def root(tmp_path):
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(yaml.safe_dump(SKELETON), encoding="utf-8")
    for cid, node, q in [("one-tradeoff", "base.one", "When is One the wrong choice?"),
                         ("one-what", "base.one", "What is One?"),
                         ("one-how", "base.one", "How does One work?"),
                         ("two-what", "base.two", "What is Two?")]:
        path = tmp_path / "vault" / "demo" / "cards" / f"{cid}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(CARD.format(id=cid, node=node, q=q), encoding="utf-8")
    return tmp_path


def run(root, *argv):
    return main(["--root", str(root), "--domain", "demo", *argv])


def steps_of(root) -> dict[str, int | None]:
    cards, errors = load_cards(root / "vault" / "demo" / "cards")
    assert not errors
    return {c.id: c.step for c in cards}


def test_status_says_which_leaves_still_have_no_order(root, capsys):
    assert run(root, "steps") == 0
    out = capsys.readouterr().out
    assert "0/2 leaves ordered" in out and "base.one" in out and "3 card(s)" in out


def test_the_prompt_shows_each_leafs_cards_and_asks_for_a_teaching_order(root, capsys):
    prompt = root / "p.md"
    assert run(root, "steps", "-o", str(prompt)) == 0
    text = prompt.read_text(encoding="utf-8")
    assert "base.one" in text and "one-what" in text and "What is One?" in text
    assert "defines" in text and '"base.one": [' in text      # the rule, and the shape to answer in


def test_importing_an_order_writes_one_line_into_each_card_and_nothing_else(root, capsys):
    answer = root / "a.json"
    answer.write_text(json.dumps({"base.one": ["one-what", "one-how", "one-tradeoff"],
                                  "base.two": ["two-what"]}), encoding="utf-8")
    assert run(root, "steps", "--import", str(answer)) == 0
    assert steps_of(root) == {"one-what": 1, "one-how": 2, "one-tradeoff": 3, "two-what": 1}
    text = (root / "vault" / "demo" / "cards" / "one-how.md").read_text(encoding="utf-8")
    assert text == CARD.format(id="one-how", node="base.one", q="How does One work?").replace(
        "type: qa\n", "type: qa\nstep: 2\n")
    assert "2/2 leaves ordered" in capsys.readouterr().out

    # a second answer replaces the first rather than adding a second line
    answer.write_text(json.dumps({"base.one": ["one-how", "one-what", "one-tradeoff"]}), encoding="utf-8")
    assert run(root, "steps", "--import", str(answer)) == 0
    assert steps_of(root)["one-how"] == 1
    assert (root / "vault" / "demo" / "cards" / "one-how.md").read_text().count("step:") == 1


@pytest.mark.parametrize("answer, complaint", [
    ({"base.one": ["one-what", "one-how"]}, "leaves out one-tradeoff"),
    ({"base.one": ["one-what", "one-how", "one-tradeoff", "two-what"]}, "two-what is not a card of base.one"),
    ({"base.one": ["one-what", "one-what", "one-how", "one-tradeoff"]}, "one-what appears twice"),
    ({"base.nine": []}, "base.nine is not a leaf"),
    (["one-what"], "expected a JSON object"),
])
def test_an_answer_that_is_not_exactly_the_leafs_cards_changes_nothing(root, capsys, answer, complaint):
    path = root / "a.json"
    path.write_text(json.dumps(answer), encoding="utf-8")
    with pytest.raises(SystemExit):
        run(root, "steps", "--import", str(path))
    assert complaint in capsys.readouterr().err
    assert set(steps_of(root).values()) == {None}


def test_check_validates_an_answer_without_writing_it(root, capsys):
    good = root / "good.json"
    good.write_text(json.dumps({"base.two": ["two-what"]}), encoding="utf-8")
    assert run(root, "steps", "--import", str(good), "--check") == 0
    assert "ok: 1 leaf, 1 card(s)" in capsys.readouterr().out
    assert set(steps_of(root).values()) == {None}
    bad = root / "bad.json"
    bad.write_text(json.dumps({"base.one": ["one-what"]}), encoding="utf-8")
    with pytest.raises(SystemExit):
        run(root, "steps", "--import", str(bad), "--check")
