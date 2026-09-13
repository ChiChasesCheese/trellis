"""Adopting content that arrived from somewhere the repo was not."""

from __future__ import annotations

from trellis.adopt import derive_skeleton, find_adoptable
from trellis.skeleton import load_skeleton

CARD = """---
id: {id}
node: {node}
type: qa
---
## Q
Question?
## A
Answer.
"""


def _drop(root, domain, entries, with_map=None):
    """Write a pile of cards the way another machine would leave them."""
    (root / "skeleton").mkdir(parents=True, exist_ok=True)
    cards = root / "vault" / domain / "cards"
    for i, (card_id, node) in enumerate(entries):
        folder = cards / node.split(".")[0]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{card_id}.md").write_text(
            CARD.format(id=card_id, node=node), encoding="utf-8")
    for node_id, title in (with_map or {}).items():
        map_dir = root / "vault" / domain / "map"
        map_dir.mkdir(parents=True, exist_ok=True)
        (map_dir / f"{node_id}.md").write_text(
            f"%% trellis:begin %%\n# {title}\n%% trellis:end %%\n",
            encoding="utf-8")
    return root


def test_a_folder_with_no_skeleton_is_reported_not_ignored(tmp_path):
    _drop(tmp_path, "stripe", [("a1", "stripe.algorithms"),
                               ("s1", "stripe.money")])
    found = find_adoptable(tmp_path)
    assert [f.name for f in found] == ["stripe"]
    assert found[0].cards == 2
    assert found[0].node_ids == {"stripe.algorithms", "stripe.money"}


def test_a_folder_that_already_has_a_skeleton_is_not_offered(tmp_path):
    _drop(tmp_path, "stripe", [("a1", "stripe.algorithms")])
    (tmp_path / "skeleton" / "stripe.yaml").write_text("domain: stripe\n")
    assert find_adoptable(tmp_path) == []


def test_a_folder_with_no_node_ids_is_not_adoptable(tmp_path):
    root = tmp_path
    (root / "skeleton").mkdir(parents=True)
    loose = root / "vault" / "scratch" / "cards"
    loose.mkdir(parents=True)
    (loose / "note.md").write_text("just some prose, no frontmatter\n")
    assert find_adoptable(root) == []


def test_the_derived_skeleton_is_a_valid_skeleton(tmp_path):
    _drop(tmp_path, "stripe", [("a1", "stripe.algorithms"),
                               ("a2", "stripe.algorithms"),
                               ("m1", "stripe.money.rounding")])
    found = find_adoptable(tmp_path)[0]
    text = derive_skeleton(found.node_ids, "stripe", found.path)
    path = tmp_path / "skeleton" / "stripe.yaml"
    path.write_text(text, encoding="utf-8")

    skeleton = load_skeleton(path)          # raises if invalid
    ids = {n.id for n in skeleton.walk()}
    assert ids == {"stripe", "stripe.algorithms", "stripe.money",
                   "stripe.money.rounding"}, "every ancestor becomes a node"


def test_titles_come_from_the_map_notes_when_they_exist(tmp_path):
    _drop(tmp_path, "stripe", [("a1", "stripe.algorithms")],
          with_map={"stripe.algorithms": "算法套路"})
    found = find_adoptable(tmp_path)[0]
    text = derive_skeleton(found.node_ids, "stripe", found.path)
    assert "算法套路" in text


def test_a_node_id_with_no_map_note_gets_a_readable_title(tmp_path):
    _drop(tmp_path, "stripe", [("a1", "stripe.money-rounding")])
    found = find_adoptable(tmp_path)[0]
    assert "title: Money Rounding" in derive_skeleton(
        found.node_ids, "stripe", found.path)


def test_readings_contribute_their_nodes_too(tmp_path):
    _drop(tmp_path, "stripe", [("a1", "stripe.algorithms")])
    readings = tmp_path / "vault" / "stripe" / "readings"
    readings.mkdir(parents=True)
    (readings / "r.md").write_text(
        "---\nnodes: [stripe.parsing, stripe.output]\nurl: http://x\n---\n# R\n",
        encoding="utf-8")
    found = find_adoptable(tmp_path)[0]
    assert found.node_ids == {"stripe.algorithms", "stripe.parsing",
                              "stripe.output"}


def test_the_header_admits_what_it_could_not_recover(tmp_path):
    """Study order is not in a pile of cards, and the file must say so
    rather than let sorted order pass for a curriculum."""
    _drop(tmp_path, "stripe", [("a1", "stripe.algorithms")])
    found = find_adoptable(tmp_path)[0]
    text = derive_skeleton(found.node_ids, "stripe", found.path)
    assert "STUDY ORDER IS NOT RECOVERABLE" in text
