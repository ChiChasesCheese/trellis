"""Pulling review history back out of Anki.

The fake below is the contract: it answers exactly the three actions
`pull` is allowed to use and raises on anything else, so widening the
conversation with Anki has to be a deliberate edit here first.
"""

from __future__ import annotations

import pytest

from trellis.anki import pull
from trellis.skeleton import load_skeleton
from trellis.traces import TYPE_RELEARNING

SKELETON = """
domain: demo
title: Demo
nodes:
  - id: alpha
    title: Alpha
    children:
      - id: alpha.one
        title: One
"""


class FakeCollection:
    """Two trellis notes and one hand-made note carrying no id:: tag —
    the state every existing collection is in until the next push."""

    NOTES = [
        {"noteId": 1, "tags": ["demo::alpha::one", "id::cap-theorem"],
         "cards": [11]},
        {"noteId": 2, "tags": ["demo::alpha::one", "id::quorum-formula"],
         "cards": [21, 22]},                      # a cloze with two cards
        {"noteId": 3, "tags": ["demo::alpha::one"], "cards": [31]},
    ]
    CARDS = {
        11: {"cardId": 11, "reps": 9, "lapses": 1, "interval": 40,
             "factor": 2500, "type": 2, "due": 900, "mod": 1000},
        21: {"cardId": 21, "reps": 4, "lapses": 0, "interval": 30,
             "factor": 2300, "type": 2, "due": 910, "mod": 1010},
        22: {"cardId": 22, "reps": 3, "lapses": 2, "interval": 2,
             "factor": 2100, "type": 3, "due": 911, "mod": 1020},
        31: {"cardId": 31, "reps": 1, "lapses": 0, "interval": 1,
             "factor": 2500, "type": 2, "due": 912, "mod": 1030},
    }

    def __call__(self, action, url, **params):
        if action == "findNotes":
            assert params["query"] == "tag:demo::*"
            return [n["noteId"] for n in self.NOTES]
        if action == "notesInfo":
            return list(self.NOTES)
        if action == "cardsInfo":
            return [self.CARDS[c] for c in params["cards"]]
        raise AssertionError(f"pull must not call {action}")


@pytest.fixture
def skeleton(tmp_path):
    path = tmp_path / "s.yaml"
    path.write_text(SKELETON, encoding="utf-8")
    return load_skeleton(path)


def test_pull_reads_review_history_back_onto_card_ids(skeleton):
    file = pull(skeleton, call=FakeCollection())
    assert set(file.traces) == {"cap-theorem", "quorum-formula"}
    assert file.traces["cap-theorem"].reps == 9
    assert file.traces["cap-theorem"].ease == 2.5
    assert file.traces["cap-theorem"].interval == 40


def test_a_note_is_held_only_as_well_as_its_weakest_card(skeleton):
    """A cloze note owns one card per deletion; forgetting any one of
    them means the note is not held."""
    trace = pull(skeleton, call=FakeCollection()).traces["quorum-formula"]
    assert trace.interval == 2, "the shortest interval, not the longest"
    assert trace.reps == 7 and trace.lapses == 2, "summed across the note"
    assert trace.type == TYPE_RELEARNING


def test_notes_without_an_id_tag_are_counted_not_guessed(skeleton):
    assert pull(skeleton, call=FakeCollection()).unmapped == 1


def test_pull_on_an_empty_collection_is_not_an_error(skeleton):
    def empty(action, url, **params):
        return []
    assert pull(skeleton, call=empty).traces == {}


def test_pull_writes_nothing_to_anki(skeleton):
    """The only command that asks Anki a question must not also answer
    one — a read path that mutates is a read path you stop trusting."""
    seen: list[str] = []

    fake = FakeCollection()

    def recording(action, url, **params):
        seen.append(action)
        return fake(action, url, **params)

    pull(skeleton, call=recording)
    assert set(seen) <= {"findNotes", "notesInfo", "cardsInfo"}
