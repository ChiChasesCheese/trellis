import pytest

from trellis.skeleton import SkeletonError, load_skeleton

GOOD = """
domain: demo
title: Demo
nodes:
  - id: beta
    title: Beta
  - id: alpha
    title: Alpha
    children:
      - id: alpha.one
        title: One
      - id: alpha.two
        title: Two
        requires: [beta]
"""


def write(tmp_path, text):
    p = tmp_path / "s.yaml"
    p.write_text(text, encoding="utf-8")
    return p


def test_load_good(tmp_path):
    s = load_skeleton(write(tmp_path, GOOD))
    assert [n.id for n in s.walk()] == ["beta", "alpha", "alpha.one", "alpha.two"]
    assert [n.id for n in s.leaves()] == ["beta", "alpha.one", "alpha.two"]
    assert s.by_id["alpha.two"].requires == ["beta"]
    assert s.by_id["alpha.one"].parent is s.by_id["alpha"]


def test_a_domain_is_written_in_chinese_unless_it_says_otherwise(tmp_path):
    """The learner reviews in Chinese, so a skeleton with no `lang` is a Chinese
    domain; an English domain must say `lang: en`."""
    assert load_skeleton(write(tmp_path, GOOD)).lang == "zh"
    english = GOOD.replace("title: Demo\n", "title: Demo\nlang: en\n", 1)
    assert load_skeleton(write(tmp_path, english)).lang == "en"


def test_deck_name_carries_study_order(tmp_path):
    s = load_skeleton(write(tmp_path, GOOD))
    assert s.deck_name(s.by_id["alpha.one"]) == "Demo::02 Alpha::One"
    assert s.deck_name(s.by_id["beta"]) == "Demo::01 Beta"


@pytest.mark.parametrize("mutation, fragment", [
    (GOOD.replace("id: beta", "id: alpha"), "duplicate node id"),
    (GOOD.replace("requires: [beta]", "requires: [ghost]"), "unknown node"),
    (GOOD.replace("id: alpha.one", "id: one"), "prefixed by its parent"),
    (GOOD.replace("title: One\n", "title: One\n        bogus: 1\n"), "unknown keys"),
    (GOOD + "  - id: gamma\n    title: G\n    requires: [gamma]\n", "requires itself"),
])
def test_rejects_bad_skeletons(tmp_path, mutation, fragment):
    with pytest.raises(SkeletonError, match=fragment):
        load_skeleton(write(tmp_path, mutation))


def test_rejects_prerequisite_ordered_after_dependent(tmp_path):
    bad = """
domain: demo
title: Demo
nodes:
  - id: alpha
    title: Alpha
    requires: [beta]
  - id: beta
    title: Beta
"""
    with pytest.raises(SkeletonError, match="ordered before its prerequisite"):
        load_skeleton(write(tmp_path, bad))


def test_rejects_requires_cycle(tmp_path):
    text = GOOD.replace("  - id: beta\n    title: Beta\n",
                        "  - id: beta\n    title: Beta\n    requires: [alpha.two]\n")
    with pytest.raises(SkeletonError, match="cycle"):
        load_skeleton(write(tmp_path, text))


def test_global_options_work_on_either_side_of_the_subcommand(tmp_path, capsys):
    """The multi-domain error tells you to pass --all, so where you type it
    must not decide whether the command runs."""
    from trellis.cli import main

    (tmp_path / "skeleton").mkdir()
    for domain in ("alpha", "beta"):
        (tmp_path / "skeleton" / f"{domain}.yaml").write_text(
            f"domain: {domain}\ntitle: {domain.title()}\nnodes:\n"
            f"  - id: root\n    title: Root\n",
            encoding="utf-8",
        )

    before = main(["--root", str(tmp_path), "--all", "validate"])
    after = main(["validate", "--root", str(tmp_path), "--all"])
    assert before == after == 0
    out = capsys.readouterr().out
    assert out.count("Alpha") == out.count("Beta") == 2  # both runs, both domains


def test_a_domain_named_after_the_subcommand_still_wins(tmp_path):
    """An option given after the subcommand overrides the one before it,
    rather than being silently dropped."""
    from trellis.cli import main

    (tmp_path / "skeleton").mkdir()
    for domain in ("alpha", "beta"):
        (tmp_path / "skeleton" / f"{domain}.yaml").write_text(
            f"domain: {domain}\ntitle: {domain.title()}\nnodes:\n"
            f"  - id: root\n    title: Root\n",
            encoding="utf-8",
        )

    assert main(["--domain", "alpha", "validate", "--domain", "beta",
                 "--root", str(tmp_path)]) == 0
