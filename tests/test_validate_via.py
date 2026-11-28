"""A domain that reaches Anki through a merged view may hang cards on that view's nodes (local or projected)."""
from pathlib import Path

from trellis.project import load_project

DOMAIN = """domain: part
title: Part
vault: domains/part
anki_via: view
nodes:
- id: a
  title: A
  summary: a
"""
VIEW = """domain: view
title: View
vault: domains/part
nodes:
- id: a
  title: A
  summary: a
- id: ov.extra
  title: Extra
  summary: extra
"""
CARD = "---\nid: c1\nnode: ov.extra\ntype: qa\n---\n## Q\nq?\n\n## A\na.\n"


def _root(tmp: Path) -> Path:
    (tmp / "skeleton").mkdir()
    (tmp / "skeleton" / "part.yaml").write_text(DOMAIN, encoding="utf-8")
    cards = tmp / "vault" / "domains" / "part" / "cards"
    cards.mkdir(parents=True)
    (cards / "c1.md").write_text(CARD, encoding="utf-8")
    return tmp


def test_card_on_a_node_only_the_view_has_is_an_error_without_the_view(tmp_path):
    root = _root(tmp_path)
    assert not load_project(root, "part").report().ok


def test_the_local_view_lets_it_through(tmp_path):
    root = _root(tmp_path)
    (root / "skeleton" / "view.yaml").write_text(VIEW, encoding="utf-8")
    assert load_project(root, "part").report().ok


def test_the_public_projection_stands_in_for_a_missing_local_view(tmp_path):
    root = _root(tmp_path)
    (root / "atlas" / "skeletons").mkdir(parents=True)
    (root / "atlas" / "skeletons" / "view.yaml").write_text(VIEW, encoding="utf-8")
    assert load_project(root, "part").report().ok
