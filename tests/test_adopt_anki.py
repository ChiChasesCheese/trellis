"""A deck that lives only in Anki becomes a domain: its notes are mirrored
onto leaves as adopted cards, read for Traces, grown around — and never
rebuilt, pushed or moved by Trellis."""

import json

import pytest
import yaml

from trellis.adopt import ADOPTED_TAG, adopt_deck, deck_inventory
from trellis.anki import align
from trellis.build import build_package
from trellis.cards import load_cards
from trellis.cli import main
from trellis.skeleton import load_skeleton

NOTES = [
    {"noteId": 101, "modelName": "LeetCode Recall", "cards": [1001],
     "tags": ["leetcode", "recall", "recognition", "lc::3", "concept::endlesscheng-0vinmk-shrink-window-for-longest"],
     "fields": {"CardID": {"value": "question:longest-substring:recognition"},
                "QuestionID": {"value": "3"}, "Slug": {"value": "longest-substring"},
                "CardType": {"value": "recognition"}, "Topics": {"value": "Hash Table · Sliding Window"},
                "Front": {"value": "<p>看到「最长无重复子串」，第一反应？</p>"},
                "Back": {"value": "<p>变长滑动窗口：右扩、<b>不合法就左缩</b>。</p>"},
                "Evidence": {"value": "<pre><code>while s[r] in seen: l += 1</code></pre>"},
                "Source": {"value": "obsidian://open?vault=lc&file=questions%2F3"}}},
    {"noteId": 102, "modelName": "LeetCode Recall", "cards": [1002],
     "tags": ["leetcode", "recall", "pattern", "lc::3"],
     "fields": {"CardID": {"value": "question:longest-substring:pattern"},
                "QuestionID": {"value": "3"}, "Slug": {"value": "longest-substring"},
                "CardType": {"value": "pattern"}, "Topics": {"value": "Hash Table · Sliding Window"},
                "Front": {"value": "<p>这题的套路名？</p>"}, "Back": {"value": "<p>滑窗。</p>"},
                "Evidence": {"value": ""}, "Source": {"value": ""}}},
    {"noteId": 103, "modelName": "LeetCode Recall", "cards": [1003],
     "tags": ["leetcode", "recall", "pattern", "lc::311"],
     "fields": {"CardID": {"value": "question:sparse-matrix:pattern"},
                "QuestionID": {"value": "311"}, "Slug": {"value": "sparse-matrix"},
                "CardType": {"value": "pattern"}, "Topics": {"value": "Array · Matrix"},
                "Front": {"value": "<p>稀疏矩阵乘法？</p>"}, "Back": {"value": "<p>跳过零。</p>"},
                "Evidence": {"value": ""}, "Source": {"value": ""}}},
    {"noteId": 104, "modelName": "LeetCode Concept Cloze", "cards": [1004, 1005],
     "tags": ["leetcode", "recall", "concept-cloze", "concept::dfs-path-collection"],
     "fields": {"CardID": {"value": "concept:dfs-path-collection:concept-cloze"},
                "ConceptID": {"value": "dfs-path-collection"}, "Title": {"value": "DFS 路径收集"},
                "CardType": {"value": "concept-cloze"},
                "Text": {"value": "<p>用可变 list 传路径，返回后必须{{c1::pop}}。</p>"},
                "Extra": {"value": "<p>字符串不可变，天然隔离。</p>"}, "Evidence": {"value": ""},
                "Source": {"value": ""}}},
]

SKELETON = {
    "domain": "leetcode", "title": "LeetCode", "lang": "zh",
    "nodes": [
        {"id": "window", "title": "滑动窗口", "order": 1, "children": [
            {"id": "window.shrink-window-for-longest", "title": "最长：不合法就缩"}]},
        {"id": "matrix", "title": "矩阵", "order": 2, "children": [
            {"id": "matrix.matrix", "title": "矩阵基本操作"}]},
        {"id": "search", "title": "搜索", "order": 3, "children": [
            {"id": "search.dfs-path-collection", "title": "DFS 路径收集"}]},
    ],
}


class FakeAnki:
    def __init__(self):
        self.tagged: list[tuple[list[int], str]] = []
        self.queries: list[str] = []

    def __call__(self, action, url=None, **params):
        if action == "findNotes":
            self.queries.append(params["query"])
            return [n["noteId"] for n in NOTES] if "LeetCode" in params["query"] else []
        if action == "notesInfo":
            return [n for n in NOTES if n["noteId"] in params["notes"]]
        if action == "addTags":
            self.tagged.append((params["notes"], params["tags"]))
            return None
        if action == "findCards":
            self.queries.append(params["query"])
            return []
        if action == "deckNames":
            return ["LeetCode", "LeetCode::Recall"]
        if action == "deleteDecks":
            return None
        raise AssertionError(f"unexpected {action}")


@pytest.fixture
def root(tmp_path):
    (tmp_path / "skeleton").mkdir()
    (tmp_path / "vault").mkdir()
    return tmp_path


def test_inventory_names_every_concept_and_the_topics_left_over():
    inv = deck_inventory(NOTES)
    assert [c.slug for c in inv.concepts] == ["dfs-path-collection", "shrink-window-for-longest"]
    assert inv.concepts[1].family == "endlesscheng-0vinmk" and inv.concepts[1].notes == 1
    # a question-level note borrows the concept its sibling notes carry;
    # only a question with no concept anywhere falls back to a topic
    assert [t.slug for t in inv.topics] == ["matrix"]


def test_without_a_skeleton_adopt_writes_the_seed_prompt(root, capsys):
    anki = FakeAnki()
    prompt = adopt_deck(root, "leetcode", "LeetCode", call=anki)
    assert prompt is not None
    text = prompt.read_text(encoding="utf-8")
    assert "`shrink-window-for-longest`" in text and "`dfs-path-collection`" in text
    assert "`matrix`" in text and "domain slug: `leetcode`" in text
    assert "看到「最长无重复子串」" in text, "a sample front shows what the slug means"
    assert not anki.tagged, "nothing in Anki is touched before there is a skeleton"


def test_with_a_skeleton_adopt_mirrors_notes_onto_leaves_and_tags_them(root):
    (root / "skeleton" / "leetcode.yaml").write_text(yaml.safe_dump(SKELETON, allow_unicode=True),
                                                     encoding="utf-8")
    anki = FakeAnki()
    result = adopt_deck(root, "leetcode", "LeetCode", call=anki)
    cards, errors = load_cards(root / "vault" / "leetcode" / "cards")
    assert not errors and len(cards) == 4
    by_id = {c.id: c for c in cards}
    rec = by_id["leetcode-q-longest-substring-recognition"]
    assert rec.node == "window.shrink-window-for-longest" and rec.anki == 101
    assert "最长无重复子串" in rec.question and "**不合法就左缩**" in rec.answer
    assert "while s[r] in seen" in rec.answer, "evidence rides along in the answer"
    assert "lc::3" in rec.tags and "recognition" in rec.tags
    # the pattern note of the same question borrows its sibling's concept
    assert by_id["leetcode-q-longest-substring-pattern"].node == "window.shrink-window-for-longest"
    assert by_id["leetcode-q-sparse-matrix-pattern"].node == "matrix.matrix"
    cloze = by_id["leetcode-c-dfs-path-collection"]
    assert cloze.type == "cloze" and "{{c1::pop}}" in cloze.text and cloze.node == "search.dfs-path-collection"
    # Anki notes learn who they are to Trellis
    tagged = {n: tags for notes, tags in anki.tagged for n in notes}
    assert tagged[101] == f"id::leetcode-q-longest-substring-recognition leetcode::window::shrink-window-for-longest {ADOPTED_TAG}"
    assert result.unmapped == []


def test_adopted_cards_are_never_built_and_never_moved(root, tmp_path):
    (root / "skeleton" / "leetcode.yaml").write_text(yaml.safe_dump(SKELETON, allow_unicode=True),
                                                     encoding="utf-8")
    adopt_deck(root, "leetcode", "LeetCode", call=FakeAnki())
    # one Trellis-owned card beside the adopted ones
    own = root / "vault" / "leetcode" / "cards" / "window" / "own-card.md"
    own.write_text("---\nid: own-card\nnode: window.shrink-window-for-longest\ntype: qa\n---\n"
                   "## Q\n自己写的？\n\n## A\n是。\n", encoding="utf-8")
    skeleton = load_skeleton(root / "skeleton" / "leetcode.yaml")
    cards, _ = load_cards(root / "vault" / "leetcode" / "cards")
    result = build_package(skeleton, cards, tmp_path / "out.apkg", [])
    assert result["notes"] == 1
    anki = FakeAnki()
    align(skeleton, call=anki)
    assert all(f"-tag:{ADOPTED_TAG}" in q for q in anki.queries if q.startswith("tag:"))


def test_cli_adopt_anki_and_grow_see_the_domain(root, capsys, monkeypatch):
    import trellis.cli as cli
    monkeypatch.setattr(cli, "_anki_call", lambda url: FakeAnki())
    assert main(["--root", str(root), "adopt", "leetcode", "--anki", "LeetCode"]) == 0
    assert "seed" in capsys.readouterr().out
    (root / "skeleton" / "leetcode.yaml").write_text(yaml.safe_dump(SKELETON, allow_unicode=True),
                                                     encoding="utf-8")
    assert main(["--root", str(root), "adopt", "leetcode", "--anki", "LeetCode"]) == 0
    assert "4 note(s) adopted" in capsys.readouterr().out
    assert main(["--root", str(root), "--domain", "leetcode", "validate"]) == 0
    assert main(["--root", str(root), "--domain", "leetcode", "grow"]) == 0
    assert "0 weak" in capsys.readouterr().out
