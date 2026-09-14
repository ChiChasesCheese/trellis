"""Grow: the loop's verdicts become new cards.

The Brief says which leaves are weak and which are uncovered; `grow` turns
that into prompts grounded in what slipped and what the vault already
holds for the leaf, and lands the answers where the loop will see them.
"""

import json

import pytest
import yaml

from trellis.cli import main
from trellis.traces import Trace, TraceFile, save_traces, traces_path

SKELETON = {
    "domain": "demo", "title": "Demo", "lang": "en",
    "nodes": [
        {"id": "base", "title": "Base", "order": 1, "children": [
            {"id": "base.one", "title": "One", "summary": "The first thing."},
            {"id": "base.two", "title": "Two", "summary": "The second thing."},
        ]},
        {"id": "mid", "title": "Mid", "order": 2, "children": [
            {"id": "mid.a", "title": "A", "summary": "Stands on One.", "requires": ["base.one"]},
            {"id": "mid.b", "title": "B", "summary": "Stands on A.", "requires": ["mid.a"]},
        ]},
    ],
}

CARD = "---\nid: {id}\nnode: {node}\ntype: qa\n---\n## Q\n{q}\n\n## A\n{a}\n"


def _card(root, cid, node, q, a):
    path = root / "vault" / "demo" / "cards" / node.split(".")[0] / f"{cid}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CARD.format(id=cid, node=node, q=q, a=a), encoding="utf-8")


@pytest.fixture
def root(tmp_path):
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(yaml.safe_dump(SKELETON), encoding="utf-8")
    # base.one: three cards, all lapsing — a Weakness. base.two: held.
    for i in range(3):
        _card(tmp_path, f"one-{i}", "base.one", f"Question one-{i}?", f"Answer one-{i}.")
        _card(tmp_path, f"two-{i}", "base.two", f"Question two-{i}?", f"Answer two-{i}.")
    traces = {f"one-{i}": Trace(f"one-{i}", reps=6, lapses=4 - i, interval=1) for i in range(3)}
    traces |= {f"two-{i}": Trace(f"two-{i}", reps=3, lapses=0, interval=30) for i in range(3)}
    save_traces(traces_path(tmp_path, "demo"),
                TraceFile(domain="demo", pulled_at="2026-09-01T00:00:00+00:00", traces=traces))
    # mid.a is uncovered and has a clipped reading to write from.
    readings = tmp_path / "vault" / "demo" / "readings"
    readings.mkdir(parents=True)
    (readings / "a-primer.md").write_text(
        "---\nnodes: [mid.a]\nurl: https://example.org/a\n---\n# A primer\nWhy read.\n",
        encoding="utf-8")
    clippings = tmp_path / "vault" / "demo" / "clippings"
    clippings.mkdir()
    (clippings / "a-primer-clip.md").write_text(
        "---\ntitle: A primer\nsource: https://example.org/a\nclipped: 2026-09-01\n---\n"
        "# A primer\n\nThe mechanism of A is that the lever moves the fulcrum. " * 80,
        encoding="utf-8")
    return tmp_path


def run(root, *argv):
    return main(["--root", str(root), *argv])


def test_grow_lists_the_weakness_first_with_what_slipped_then_the_uncovered(root, capsys):
    assert run(root, "grow") == 0
    out = capsys.readouterr().out
    lines = [l.strip() for l in out.splitlines() if l.strip().startswith(("weak", "uncovered"))]
    assert lines[0].startswith("weak") and "demo:base.one" in lines[0]
    # the card that lapsed most is named, so the reader sees what to re-teach
    assert "one-0" in out
    assert any(l.startswith("uncovered") and "demo:mid.a" in l for l in lines)
    assert any(l.startswith("uncovered") and "demo:mid.b" in l for l in lines)
    assert not any("base.two" in l for l in lines), "a held leaf is not a target"
    # a leaf with a clipped reading says so: there is text to write from
    assert "1 clipped reading" in [l for l in lines if "mid.a" in l][0]
    assert "ungrounded" in [l for l in lines if "mid.b" in l][0]


def test_a_weakness_prompt_carries_the_slipped_cards_and_asks_for_another_angle(root):
    out = root / "p.md"
    assert run(root, "grow", "--next", "-o", str(out)) == 0
    prompt = out.read_text(encoding="utf-8")
    assert "Base › One" in prompt                       # the scaffold's context
    assert "not holding" in prompt.lower()
    assert "Question one-0?" in prompt and "Answer one-0." in prompt
    assert "different angle" in prompt
    assert "Question two-0?" not in prompt              # a held sibling is not evidence


def test_an_uncovered_prompt_is_grounded_in_the_clipped_reading(root):
    out = root / "p.md"
    assert run(root, "grow", "--leaf", "demo:mid.a", "-o", str(out)) == 0
    prompt = out.read_text(encoding="utf-8")
    assert "Mid › A" in prompt
    assert "the lever moves the fulcrum" in prompt
    assert "A primer" in prompt and "https://example.org/a" in prompt


def test_grown_cards_land_on_the_leaf_tagged_and_the_leaf_leaves_the_uncovered_list(root, capsys):
    answer = [{"id": "a-lever", "type": "qa", "q": "What moves the fulcrum of A?", "a": "The lever."}]
    (root / "a.json").write_text(json.dumps(answer), encoding="utf-8")
    assert run(root, "grow", "--import", str(root / "a.json"), "--leaf", "demo:mid.a") == 0
    assert "demo:mid.a: 1 card(s) grown" in capsys.readouterr().out
    card = (root / "vault" / "demo" / "cards" / "mid" / "a-lever.md").read_text(encoding="utf-8")
    assert "node: mid.a" in card and "tags: [grown]" in card
    run(root, "grow")
    out = capsys.readouterr().out
    assert "demo:mid.a" not in out
    assert "demo:mid.b" in out

    # the loop's own rule holds here too: a card must not lean on its source
    leaning = [{"id": "b-leans", "type": "qa", "q": "As discussed above, what is B?", "a": "B."}]
    (root / "b.json").write_text(json.dumps(leaning), encoding="utf-8")
    with pytest.raises(SystemExit):
        run(root, "grow", "--import", str(root / "b.json"), "--leaf", "demo:mid.b")
    assert not (root / "vault" / "demo" / "cards" / "mid" / "b-leans.md").exists()


def test_brief_and_feed_run_on_the_same_traces_and_point_at_grow(root, capsys):
    assert run(root, "brief", "--print") == 0
    out = capsys.readouterr().out
    assert "[[base.one|One]]" in out and "trellis grow" in out
    assert run(root, "feed") == 0
    assert "search:" in capsys.readouterr().out


def test_a_translated_domain_asks_for_and_keeps_a_translation(root):
    # every existing card carries a zh translation, so a grown card must too
    for path in (root / "vault" / "demo" / "cards").rglob("*.md"):
        path.write_text(path.read_text(encoding="utf-8") + "\n## Q zh\n问？\n\n## A zh\n答。\n",
                        encoding="utf-8")
    assert run(root, "grow", "--leaf", "demo:mid.a", "-o", str(root / "p.md")) == 0
    assert "q_zh" in (root / "p.md").read_text(encoding="utf-8")
    answer = [{"id": "a-both", "type": "qa", "q": "What moves A?", "a": "The lever.",
               "q_zh": "什么推动 A？", "a_zh": "杠杆。"},
              {"id": "a-cloze", "type": "cloze", "text": "A moves by {{c1::the lever}}.",
               "text_zh": "A 靠 {{c1::the lever}} 移动。"}]
    (root / "a.json").write_text(json.dumps(answer, ensure_ascii=False), encoding="utf-8")
    assert run(root, "grow", "--import", str(root / "a.json"), "--leaf", "demo:mid.a") == 0
    card = (root / "vault" / "demo" / "cards" / "mid" / "a-both.md").read_text(encoding="utf-8")
    assert "## Q zh\n什么推动 A？" in card and "## A zh\n杠杆。" in card
    cloze = (root / "vault" / "demo" / "cards" / "mid" / "a-cloze.md").read_text(encoding="utf-8")
    assert "## zh\nA 靠 {{c1::the lever}} 移动。" in cloze
    assert run(root, "--domain", "demo", "build", "--lang", "zh") == 0


def test_grow_can_be_held_to_one_domain(root, capsys):
    (root / "skeleton" / "other.yaml").write_text(yaml.safe_dump({
        "domain": "other", "title": "Other",
        "nodes": [{"id": "x", "title": "X", "children": [{"id": "x.y", "title": "Y"}]}]}),
        encoding="utf-8")
    assert run(root, "grow") == 0
    assert "other:x.y" in capsys.readouterr().out
    assert run(root, "--domain", "demo", "grow") == 0
    out = capsys.readouterr().out
    assert "other:x.y" not in out and "demo:mid.a" in out


def test_a_leaf_that_is_neither_weak_nor_uncovered_is_refused(root):
    with pytest.raises(SystemExit):
        run(root, "grow", "--leaf", "demo:base.two")
