"""Study order and pace, end to end: what the vault says is what Anki deals.

The claim under test is about a person opening a deck: the first new cards
are the Core's, in the steps their author gave them; changing the vault and
pushing again changes that, even though Anki's importer never moves a card it
already has; and the day's mix of new cards and reviews is the domain's own,
without touching the preset the rest of the collection shares.
"""

from __future__ import annotations

import pytest
import yaml

from fake_anki import DEFAULT_PRESET, FakeAnki
from trellis import cli
from trellis.cli import main

SKELETON = {
    "domain": "demo", "title": "Demo", "lang": "en",
    "nodes": [
        {"id": "intro", "title": "Intro", "order": 1, "children": [
            {"id": "intro.history", "title": "History"},
            {"id": "intro.model", "title": "Model"},
        ]},
        {"id": "storage", "title": "Storage", "order": 2, "children": [
            # stood on by nothing, so only its declaration makes it core;
            # intro.model is core because this leaf stands on it
            {"id": "storage.log", "title": "Log", "requires": ["intro.model"], "core": True},
            {"id": "storage.trivia", "title": "Trivia"},
        ]},
    ],
}
CARD = "---\nid: {id}\nnode: {node}\ntype: qa\n{extra}---\n## Q\nQuestion {id}?\n\n## A\nAnswer {id}.\n"


@pytest.fixture
def anki(monkeypatch):
    fake = FakeAnki()
    monkeypatch.setattr(cli, "_anki_call", lambda url: fake)
    return fake


def write_skeleton(root, **top):
    (root / "skeleton").mkdir(exist_ok=True)
    (root / "skeleton" / "demo.yaml").write_text(yaml.safe_dump({**SKELETON, **top}), encoding="utf-8")


def write_card(root, card_id, node, step=None):
    path = root / "vault" / "demo" / "cards" / f"{card_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CARD.format(id=card_id, node=node, extra=f"step: {step}\n" if step else ""),
                    encoding="utf-8")


@pytest.fixture
def root(tmp_path):
    write_skeleton(tmp_path)
    write_card(tmp_path, "history-a", "intro.history")
    write_card(tmp_path, "model-what", "intro.model", step=1)
    write_card(tmp_path, "model-why", "intro.model", step=2)
    write_card(tmp_path, "log-what", "storage.log")
    write_card(tmp_path, "trivia-a", "storage.trivia")
    return tmp_path


def run(root, *argv):
    return main(["--root", str(root), *argv])


CORE_THEN_REST = ["model-what", "model-why", "log-what", "history-a", "trivia-a"]


def test_a_first_push_deals_the_core_first_in_the_steps_given(root, anki, capsys):
    assert run(root, "anki-push") == 0
    assert anki.today("Demo") == CORE_THEN_REST
    assert anki.tagged("trellis::core") == ["log-what", "model-what", "model-why"]
    # nothing to move: a collection that has never seen a card takes the
    # position the package gave it
    out = capsys.readouterr().out
    assert "sequenced 0 new card(s)" in out and "new cards dealt by position" in out


def test_reordering_in_the_vault_reorders_a_collection_that_already_has_the_cards(root, anki, capsys):
    assert run(root, "anki-push") == 0
    anki.review("model-what", reps=3, interval=9)
    held_at = anki.card_of("model-what")["due"]

    write_card(root, "model-why", "intro.model", step=1)        # swap the two steps
    write_card(root, "model-what", "intro.model", step=2)
    write_card(root, "model-between", "intro.model", step=3)    # and add a card
    assert run(root, "anki-push") == 0

    new_today = [c for c in anki.today("Demo") if c != "model-what"]
    assert new_today == ["model-why", "model-between", "log-what", "history-a", "trivia-a"]
    # a card with a review history is scheduled by Anki, and is never touched
    assert anki.card_of("model-what")["due"] == held_at


def test_a_push_that_changes_nothing_moves_nothing(root, anki, capsys):
    assert run(root, "anki-push") == 0
    before = len([c for c in anki.calls if c == "setSpecificValueOfCard"])
    capsys.readouterr()
    assert run(root, "anki-push") == 0
    assert len([c for c in anki.calls if c == "setSpecificValueOfCard"]) == before
    assert "sequenced 0 new card(s)" in capsys.readouterr().out


def test_a_domain_that_sets_no_pace_changes_only_how_new_cards_are_gathered(root, anki):
    # Anki's default gathers new cards deck by deck, and sibling decks sort by
    # title — so without this even the skeleton's order is not what is dealt.
    assert run(root, "anki-push") == 0
    ours = anki.presets[anki.deck_preset["Demo"]]
    changed = {k for k in ours if ours[k] != DEFAULT_PRESET[k]}
    assert changed == {"id", "name", "newGatherPriority", "newSortOrder"}
    assert anki.presets[1] == DEFAULT_PRESET


def test_new_first_shows_todays_new_cards_before_the_reviews(root, anki, capsys):
    write_skeleton(root, study={"mix": "new-first", "new_per_day": 2, "reviews_per_day": 10})
    assert run(root, "anki-push") == 0
    anki.review("history-a", reps=4, interval=12)
    anki.review("trivia-a", reps=4, interval=12)
    assert anki.today("Demo") == ["model-what", "model-why", "history-a", "trivia-a"]

    # its own preset, on every deck of the domain; the shared Default untouched
    assert anki.presets[1] == DEFAULT_PRESET
    ours = anki.presets[anki.deck_preset["Demo"]]
    assert ours["name"] == "Trellis · Demo"
    assert set(anki.deck_preset) == set(anki._deckNames())
    assert len(set(anki.deck_preset.values())) == 1
    assert "pace: new-first, 2 new + 10 review(s) a day" in capsys.readouterr().out


def test_half_and_half_is_equal_limits_mixed_together(root, anki):
    write_skeleton(root, study={"mix": "mixed", "new_per_day": 2, "reviews_per_day": 2})
    assert run(root, "anki-push") == 0
    for card_id in ("history-a", "trivia-a", "log-what"):
        anki.review(card_id, reps=4, interval=12)
    shown = anki.today("Demo")
    assert len(shown) == 4 and shown[0::2] == ["model-what", "model-why"]   # alternating


def test_changing_the_pace_edits_the_domains_preset_instead_of_making_another(root, anki):
    write_skeleton(root, study={"mix": "new-first", "new_per_day": 2})
    assert run(root, "anki-push") == 0
    write_skeleton(root, study={"mix": "reviews-first", "new_per_day": 7})
    assert run(root, "anki-push") == 0
    assert sorted(anki.presets) == [1, 2]
    assert (anki.presets[2]["newMix"], anki.presets[2]["new"]["perDay"]) == (1, 7)
    assert anki.presets[2]["rev"]["perDay"] == 50          # never set, so never changed


def test_the_study_order_can_be_the_plain_skeleton(root, anki):
    write_skeleton(root, study={"order": "skeleton"})
    assert run(root, "anki-push") == 0
    assert anki.today("Demo") == ["history-a", "model-what", "model-why", "log-what", "trivia-a"]


def test_align_alone_converges_order_and_options_without_importing(root, anki, capsys):
    assert run(root, "anki-push") == 0
    write_card(root, "model-why", "intro.model", step=1)
    write_card(root, "model-what", "intro.model", step=2)
    imports = anki.calls.count("importPackage")
    capsys.readouterr()
    assert run(root, "anki-align") == 0
    assert anki.calls.count("importPackage") == imports
    assert anki.today("Demo")[:2] == ["model-why", "model-what"]
    assert "sequenced 2 new card(s)" in capsys.readouterr().out
