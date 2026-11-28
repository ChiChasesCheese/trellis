"""The Atlas data contract: scope from atlas.yaml, tracked files only, Reach, the Snapshot, the export."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from trellis.atlas import (AtlasConfig, Scope, check_report, company_words, has_company_word, load_config,
                           load_published)
from trellis.export import SCHEMA_KINDS, export, plain_markdown, schema_text
from trellis.snapshot import (TEST_SETS, build_snapshot, dumps, level, load_snapshots, question_id,
                              write_snapshot)

# -- a tiny repo ---------------------------------------------------------------------------------

SKELETON_A = {
    "domain": "alpha", "title": "Alpha", "vault": "domains/alpha",
    "nodes": [
        {"id": "basics", "title": "Basics", "children": [
            {"id": "basics.one", "title": "One"},
            {"id": "basics.two", "title": "Two", "requires": ["basics.one"]},
        ]},
        {"id": "tt", "title": "TikTok prep", "children": [{"id": "tt.round", "title": "Round"}]},
        {"id": "mine", "title": "Mine", "children": [{"id": "mine.private", "title": "Private"}]},
        {"id": "gear", "title": "Gear", "children": [
            {"id": "gear.amazon-locker", "title": "Locker", "children": [{"id": "gear.amazon-locker.api", "title": "API"}]},
            {"id": "gear.button", "title": "Button"},
        ]},
    ],
}
SKELETON_B = {"domain": "beta", "title": "Beta", "vault": "domains/beta",
              "nodes": [{"id": "snowflake-core", "title": "Core", "children": [{"id": "snowflake-core.x", "title": "X"}]}]}
ATLAS = {
    "companies_from": "vault/interviews/companies",
    "aliases": {"tt": "tiktok"},
    "domains": ["alpha", "beta"],
    "exclude": {"alpha": ["mine"]},
    "allow": ["beta", "alpha:gear.amazon-locker"],
    "strip_tags": ["公司::"],
}


def card_md(card_id: str, node: str, tags=(), q="Q?", a="A.") -> str:
    tag_line = f"tags: {json.dumps(list(tags), ensure_ascii=False)}\n" if tags else ""
    return f"---\nid: {card_id}\nnode: {node}\n{tag_line}---\n## Q\n{q}\n## A\n{a}\n"


CARDS_A = {
    "a-one-1": ("basics.one", ["公司::amazon", "keep"]),
    "a-one-2": ("basics.one", []),
    "a-two-1": ("basics.two", []),
    "a-tt-1": ("tt.round", []),
    "a-mine-1": ("mine.private", []),
    "a-button-1": ("gear.button", []),
    "a-amazon-card": ("basics.two", []),                 # company word in the card id
    "a-hi-tt-lc-x": ("basics.two", []),                  # the alias `tt` as a word of the id
    "a-locker-1": ("gear.amazon-locker.api", []),        # under an allowed node
}


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "skeleton").mkdir()
    for sk in (SKELETON_A, SKELETON_B):
        (tmp_path / "skeleton" / f"{sk['domain']}.yaml").write_text(yaml.safe_dump(sk, allow_unicode=True), encoding="utf-8")
    (tmp_path / "atlas.yaml").write_text(yaml.safe_dump(ATLAS, allow_unicode=True), encoding="utf-8")
    for cid, (node, tags) in CARDS_A.items():
        p = tmp_path / "vault/domains/alpha/cards" / f"{cid}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(card_md(cid, node, tags, q=f"See [[x|{cid}]] and [[y]] obsidian://open?vault=v ![[pic.png]]"), encoding="utf-8")
    for cid, node in (("b-1", "snowflake-core.x"), ("beta-snowflake-card", "snowflake-core.x")):
        p = tmp_path / "vault/domains/beta/cards" / f"{cid}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(card_md(cid, node), encoding="utf-8")
    # an untracked premium card inside a published domain folder
    secret = tmp_path / "vault/domains/alpha/cards/premium/secret.md"
    secret.parent.mkdir(parents=True, exist_ok=True)
    secret.write_text(card_md("a-premium-secret", "basics.one"), encoding="utf-8")
    # a company folder
    for co in ("tiktok", "amazon", "snowflake"):
        f = tmp_path / "vault/interviews/companies" / co / "README.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("x", encoding="utf-8")
    return tmp_path


def tracked_of(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and "premium" not in p.parts}


def published_of(root: Path):
    config = load_config(root)
    tracked = tracked_of(root)
    scope = Scope(config, company_words(config, tracked))
    return scope, *load_published(root, scope, tracked, count_untracked=True)


# -- scope ---------------------------------------------------------------------------------------

def test_company_words_are_folders_plus_aliases(repo):
    config = load_config(repo)
    words = company_words(config, tracked_of(repo))
    assert words == {("tiktok",), ("amazon",), ("snowflake",), ("tt",)}


def test_a_word_matches_whole_tokens_only():
    words = {("tt",), ("jane", "street")}
    assert has_company_word("tt", words)
    assert has_company_word("hi-tt-lc-x", words)
    assert has_company_word("a.tt.b", words)
    assert has_company_word("x_jane-street_y", words)
    assert not has_company_word("button", words)
    assert not has_company_word("jane.other", words)


def test_company_node_and_its_subtree_are_left_out(repo):
    scope, published, notes = published_of(repo)
    alpha = published["alpha"]
    assert "tt" not in alpha.nodes and "tt.round" not in alpha.nodes
    assert {"basics", "basics.one", "basics.two", "gear", "gear.button"} <= alpha.nodes
    assert ("tt", "company", 1) in alpha.left_out


def test_exclude_leaves_out_by_node_id_prefix(repo):
    _, published, _ = published_of(repo)
    assert "mine" not in published["alpha"].nodes and "mine.private" not in published["alpha"].nodes
    assert ("mine", "exclude", 1) in published["alpha"].left_out


def test_allow_keeps_one_node_and_a_whole_domain(repo):
    _, published, _ = published_of(repo)
    assert {"gear.amazon-locker", "gear.amazon-locker.api"} <= published["alpha"].nodes
    assert {"snowflake-core", "snowflake-core.x"} <= published["beta"].nodes      # the domain is allowed as a whole
    ids = {c.id for c in published["alpha"].cards}
    assert "a-locker-1" in ids
    assert "beta-snowflake-card" in {c.id for c in published["beta"].cards}


def test_card_with_a_company_word_in_its_id_is_left_out(repo):
    _, published, _ = published_of(repo)
    ids = {c.id for c in published["alpha"].cards}
    assert "a-amazon-card" not in ids and "a-hi-tt-lc-x" not in ids
    assert {"a-one-1", "a-one-2", "a-two-1", "a-button-1"} <= ids
    assert "a-tt-1" not in ids and "a-mine-1" not in ids                           # their nodes are out
    assert published["alpha"].cards_left_out == 2


def test_company_tags_are_stripped(repo):
    _, published, _ = published_of(repo)
    card = next(c for c in published["alpha"].cards if c.id == "a-one-1")
    assert card.tags == ["keep"]


def test_untracked_cards_are_ignored(repo):
    _, published, _ = published_of(repo)
    assert "a-premium-secret" not in {c.id for c in published["alpha"].cards}
    assert published["alpha"].untracked_cards == 1


def test_check_report_lists_every_left_out_subtree(repo):
    _, published, notes = published_of(repo)
    text = "\n".join(check_report(published, notes))
    assert "tt  [company]  1 card(s)" in text and "mine  [exclude]" in text
    assert "card a-amazon-card" in text and "1 untracked card file(s) ignored" in text


def test_unlisted_and_untracked_skeletons_are_skipped(repo):
    config = load_config(repo)
    config.domains.append("gamma")
    tracked = tracked_of(repo) - {"skeleton/beta.yaml"}
    scope = Scope(config, company_words(config, tracked))
    published, notes = load_published(repo, scope, tracked)
    assert set(published) == {"alpha"}
    assert any("beta" in n for n in notes) and any("gamma" in n for n in notes)


# -- Reach levels --------------------------------------------------------------------------------

@pytest.mark.parametrize("studied,cards,want", [
    (0, 0, -1), (0, 100, 0), (1, 100, 1), (24, 100, 1), (25, 100, 2), (49, 100, 2), (50, 100, 3),
    (74, 100, 3), (75, 100, 4), (99, 100, 4), (100, 100, 5), (1, 1, 5), (None, 10, None), (None, 0, -1),
])
def test_level_boundaries(studied, cards, want):
    assert level(studied, cards) == want


# -- the Snapshot --------------------------------------------------------------------------------

def row(card_id, **kw):
    return {"cardId": card_id, "reps": 0, "lapses": 0, "interval": 0, "factor": 2500, "type": 0, "due": 0,
            "mod": 1_700_000_000, **kw}


class AnkiStub:
    """A hand-made collection that answers what the Snapshot asks, and nothing else."""

    def __init__(self, own=None, tests=None, daily=None):
        self.notes = {}     # note id -> (tags, [card ids])
        self.cards = {}
        self.daily = daily if daily is not None else [["2026-11-27", 29], ["2026-11-26", 4]]
        self.calls = []
        n = 0
        for card_id, reps in (own or {}).items():
            n += 1
            self.notes[n] = ([f"id::{card_id}", "alpha::basics::one"], [n * 10], reps)
        for tag, qid, reps in (tests or []):
            n += 1
            self.notes[n] = ([tag, f"{tag}::2026-11-01", f"{tag}::id::{qid}"], [n * 10], reps)

    def __call__(self, action, url=None, **params):
        self.calls.append(action)
        if action == "findNotes":
            q = params["query"]
            prefix = q[len("tag:"):].rstrip("*")
            return [i for i, (tags, _, _) in self.notes.items() if any(t.startswith(prefix) for t in tags)]
        if action == "notesInfo":
            return [{"noteId": i, "tags": self.notes[i][0], "cards": self.notes[i][1]} for i in params["notes"]]
        if action == "cardsInfo":
            by_card = {c: reps for _, (_, cs, reps) in self.notes.items() for c in cs}
            return [row(c, reps=by_card[c], interval=30 if by_card[c] else 0, type=2 if by_card[c] else 0)
                    for c in params["cards"]]
        if action == "getNumCardsReviewedByDay":
            return self.daily
        raise AssertionError(f"the Snapshot must not call {action}")


def test_reach_counts_a_test_question_by_the_sha1_rule(repo):
    _, published, _ = published_of(repo)
    qid = question_id("tlld", "a-two-1")
    assert qid == "tlld-" + __import__("hashlib").sha1(b"a-two-1").hexdigest()[:10]
    anki = AnkiStub(own={"a-one-1": 3, "a-one-2": 0}, tests=[("tlld", qid, 2), ("tai", question_id("tai", "a-button-1"), 0)])
    snap = build_snapshot({"alpha": published["alpha"]}, anki, date="2026-11-28")
    alpha = snap["domains"]["alpha"]
    # published cards: a-one-1, a-one-2, a-two-1, a-button-1, a-locker-1 -> studied: a-one-1 (own), a-two-1 (its question)
    assert alpha["cards"] == 5 and alpha["studied"] == 2
    assert (alpha["nodes"]["basics"]["cards"], alpha["nodes"]["basics"]["studied"]) == (3, 2)
    assert alpha["nodes"]["basics.two"]["studied"] == 1
    assert "studied" not in alpha["nodes"]["gear.button"]       # a question with no reviews is not a reading
    assert alpha["nodes"]["gear.button"]["cards"] == 1
    assert set(TEST_SETS) == {"lld", "ai"}


def test_snapshot_holds_only_aggregates_and_days(repo):
    _, published, _ = published_of(repo)
    anki = AnkiStub(own={"a-one-1": 3}, daily=[["2026-11-27", 29]])
    snap = build_snapshot({"alpha": published["alpha"]}, anki, date="2026-11-28")
    text = dumps(snap)
    assert json.loads(text) == snap
    assert "a-one-1" not in text and "a-two-1" not in text                       # no card ids at all
    assert re.findall(r"\d{4}-\d{2}-\d{2}[T ]\d", text) == []                    # nothing finer than a day
    assert not re.search(r"\b1[5-9]\d{8}\b", text)                               # no epoch seconds
    assert snap["daily"] == {"2026-11-27": 29}
    # zero and empty keys are omitted
    assert all(e for e in snap["domains"]["alpha"]["nodes"].values())


def test_uncovered_leaf_is_flagged_and_snapshot_is_written(repo):
    _, published, _ = published_of(repo)
    # a leaf with no cards: published node `basics.two` keeps cards; make a card-less leaf by dropping the cards
    pub = published["alpha"]
    pub.cards = [c for c in pub.cards if c.node != "gear.button"]
    snap = build_snapshot({"alpha": pub}, AnkiStub(), date="2026-11-28")
    assert snap["domains"]["alpha"]["nodes"]["gear.button"] == {"flags": ["uncovered"]}
    path = write_snapshot(repo, snap)
    assert path == repo / "snapshots" / "2026-11-28.json"
    assert load_snapshots(repo) == [snap]


# -- the export ----------------------------------------------------------------------------------

def check(value, schema, where="$"):
    """The small part of JSON Schema the shipped schemas use: type, const, enum, required, properties, items,
    additionalProperties, minimum, maximum (no jsonschema dependency)."""
    if "const" in schema:
        assert value == schema["const"], f"{where}: {value!r} != {schema['const']!r}"
    if "enum" in schema:
        assert value in schema["enum"], f"{where}: {value!r} not in {schema['enum']}"
    if "type" in schema:
        names = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        ok = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None),
              "integer": int, "number": (int, float)}
        assert any(isinstance(value, ok[n]) and not (n in ("integer", "number") and isinstance(value, bool))
                   for n in names), f"{where}: {value!r} is not {names}"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema:
            assert value >= schema["minimum"], where
        if "maximum" in schema:
            assert value <= schema["maximum"], where
    if isinstance(value, dict):
        for key in schema.get("required", []):
            assert key in value, f"{where}: missing key {key!r}"
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                check(value[key], sub, f"{where}.{key}")
        extra = schema.get("additionalProperties")
        if isinstance(extra, dict):
            for key, v in value.items():
                if key not in schema.get("properties", {}):
                    check(v, extra, f"{where}.{key}")
    if isinstance(value, list) and "items" in schema:
        for i, v in enumerate(value):
            check(v, schema["items"], f"{where}[{i}]")


def schema(kind):
    return json.loads(schema_text(kind))


@pytest.fixture
def exported(repo, tmp_path_factory):
    _, published, _ = published_of(repo)
    qid = question_id("tlld", "a-two-1")
    snap = build_snapshot(published, AnkiStub(own={"a-one-1": 3, "a-one-2": 1}, tests=[("tlld", qid, 2)]), date="2026-11-28")
    write_snapshot(repo, snap)
    out = tmp_path_factory.mktemp("atlas-data")
    export(published, load_snapshots(repo), out, generated_at="2026-11-28T00:00:00+00:00")
    return out, snap


def test_every_file_carries_its_schema_and_its_required_keys(exported):
    out, snap = exported
    check(json.loads((out / "index.json").read_text()), schema("index"))
    for kind, path in (("history", "history.json"), ("daily", "daily.json")):
        data = json.loads((out / path).read_text())
        assert data["schema"] == f"trellis.{kind}/1"
        check(data, schema(kind))
    for domain in ("alpha", "beta"):
        data = json.loads((out / "d" / f"{domain}.json").read_text())
        assert data["schema"] == "trellis.domain/1"
        check(data, schema("domain"))
        for line in (out / "d" / domain / "cards.jsonl").read_text().splitlines():
            card = json.loads(line)
            assert card["schema"] == "trellis.card/1"
            check(card, schema("card"))
    check(snap, schema("snapshot"))
    for kind in SCHEMA_KINDS:
        assert json.loads((out / "schema" / f"{kind}.schema.json").read_text())["$schema"].endswith("2020-12/schema")


def test_export_content_follows_scope_and_snapshot(exported):
    out, _ = exported
    index = json.loads((out / "index.json").read_text())
    assert index["snapshot_date"] == "2026-11-28" and index["generated_at"] == "2026-11-28T00:00:00+00:00"
    alpha = next(d for d in index["domains"] if d["id"] == "alpha")
    assert (alpha["cards"], alpha["studied"]) == (5, 3) and alpha["reach"] == 0.6 and alpha["level"] == 3
    assert alpha["uncovered"] == [] and alpha["weak"] == []
    tree = json.loads((out / "d" / "alpha.json").read_text())
    by_id = {n["id"]: n for n in tree["nodes"]}
    assert "tt" not in by_id and "mine" not in by_id
    assert by_id["basics.two"]["requires"] == ["basics.one"] and by_id["basics"]["parent"] is None
    assert by_id["basics"]["studied"] == 3 and by_id["basics"]["level"] == 5
    cards = [json.loads(l) for l in (out / "d/alpha/cards.jsonl").read_text().splitlines()]
    one = next(c for c in cards if c["id"] == "a-one-1")
    assert one["tags"] == ["keep"]
    assert "[[" not in one["q"] and "obsidian://" not in one["q"] and "![[" not in one["q"]
    assert "a-one-1 and y" in one["q"]
    md = (out / "d/alpha.md").read_text()
    assert "  - One `basics.one` 2/2" in md and "`tt`" not in md and "`mine`" not in md
    llms = (out / "llms.txt").read_text()
    assert llms.startswith("# ") and "d/alpha.md" in llms and "d/alpha/cards.jsonl" in llms and "index.json" in llms
    hist = json.loads((out / "history.json").read_text())["domains"]["alpha"]
    assert [(h["date"], h["cards"], h["studied"]) for h in hist] == [("2026-11-28", 5, 3)]
    assert json.loads((out / "daily.json").read_text())["daily"] == {"2026-11-26": 4, "2026-11-27": 29}


def test_export_without_a_snapshot_leaves_reach_empty(repo, tmp_path):
    _, published, _ = published_of(repo)
    export(published, [], tmp_path / "o")
    index = json.loads((tmp_path / "o/index.json").read_text())
    alpha = next(d for d in index["domains"] if d["id"] == "alpha")
    assert alpha["studied"] is None and alpha["reach"] is None and alpha["level"] is None and alpha["cards"] == 5
    check(index, schema("index"))


def test_export_is_deterministic(repo, tmp_path):
    _, published, _ = published_of(repo)
    export(published, [], tmp_path / "a", generated_at="x")
    export(published, [], tmp_path / "b", generated_at="x")
    names = sorted(p.relative_to(tmp_path / "a").as_posix() for p in (tmp_path / "a").rglob("*") if p.is_file())
    assert names == sorted(p.relative_to(tmp_path / "b").as_posix() for p in (tmp_path / "b").rglob("*") if p.is_file())
    for n in names:
        assert (tmp_path / "a" / n).read_bytes() == (tmp_path / "b" / n).read_bytes()


def test_plain_markdown():
    assert plain_markdown("a [[x|y]] b [[z]] c [t](obsidian://open?vault=v&file=f) ![[i.png]] end") == "a y b z c t  end"
    fence = "```mermaid\ngraph TD\nA-->B\n```\n<b>x</b>"
    assert plain_markdown(fence) == fence


def test_atlas_yaml_of_this_repo_parses():
    root = Path(__file__).resolve().parent.parent
    if not (root / "atlas.yaml").exists():
        pytest.skip("atlas.yaml is not in this checkout")
    config = load_config(root)
    assert isinstance(config, AtlasConfig) and config.domains


# -- the projection of a local skeleton ----------------------------------------------------------

from trellis.atlas import project_skeleton, projection_path   # noqa: E402

PROJ_SRC = {
    "domain": "merged", "title": "Merged", "lang": "zh", "vault": "domains/open",
    "include": ["domains/closed", "domains/also-open"], "deck": "Merged", "own_decks": {"a": "X"}, "deck_moves": {"a": "Y"},
    "study": {"x": 1},
    "nodes": [
        {"id": "a", "title": "A", "core": True, "children": [
            {"id": "a.one", "title": "One", "requires": ["b.gone", "a.two"]},
            {"id": "a.two", "title": "Two"},
        ]},
        {"id": "b", "title": "B", "children": [{"id": "b.gone", "title": "Gone"}]},
        {"id": "c", "title": "Leaks acme-secret", "children": [{"id": "c.x", "title": "X"}]},
    ],
}
PROJ_CARDS = {"a.one": {"domains/open"}, "a.two": {"!domains/closed"}, "b.gone": {"!domains/closed"}, "c.x": {"domains/open"}}
PROJ_TRACKED = {"vault/domains/open/cards/x.md", "vault/domains/also-open/cards/y.md"}


def test_projection_keeps_tracked_nodes_and_drops_untracked_ones():
    proj = project_skeleton(PROJ_SRC, PROJ_CARDS, PROJ_TRACKED, None)
    ids = [n["id"] for n in proj.data["nodes"]]
    assert ids == ["a", "c"] and proj.top_level == 2
    kids = [c["id"] for c in proj.data["nodes"][0]["children"]]
    assert kids == ["a.one"]                                        # a.two holds only an untracked card
    assert proj.dropped_by == {"untracked cards in domains/closed": 2, "no cards": 1}     # a.two, b.gone; b
    assert proj.kept == 4 and proj.dropped == 3


def test_projection_removes_dangling_requires_and_anki_keys():
    proj = project_skeleton(PROJ_SRC, PROJ_CARDS, PROJ_TRACKED, None)
    one = proj.data["nodes"][0]["children"][0]
    assert "requires" not in one                                    # b.gone and a.two are both dropped
    assert proj.data["nodes"][0]["core"] is True
    assert set(proj.data) == {"domain", "title", "lang", "vault", "include", "nodes"}
    assert proj.data["include"] == ["domains/also-open"]            # only folders with tracked files


def test_projection_keeps_a_requires_to_a_kept_node():
    src = {**PROJ_SRC, "nodes": [{"id": "a", "title": "A", "children": [
        {"id": "a.one", "title": "One", "requires": ["a.two"]}, {"id": "a.two", "title": "Two"}]}]}
    cards = {"a.one": {"domains/open"}, "a.two": {"domains/open"}}
    proj = project_skeleton(src, cards, PROJ_TRACKED, None)
    assert proj.data["nodes"][0]["children"][0]["requires"] == ["a.two"]


def test_projection_drops_a_node_whose_title_hits_a_private_term():
    pat = re.compile(r"(?<![A-Za-z0-9_])(acme-secret)(?![A-Za-z0-9_])")
    proj = project_skeleton(PROJ_SRC, PROJ_CARDS, PROJ_TRACKED, pat)
    assert [n["id"] for n in proj.data["nodes"]] == ["a"]
    assert proj.dropped_by["private term"] == 2                     # the node and its subtree
    assert "acme-secret" not in "".join(f"{k}{v}" for k, v in proj.dropped_by.items())


def test_export_prefers_the_projection_over_the_local_skeleton(repo):
    proj = {"domain": "alpha", "title": "Alpha (projection)", "vault": "domains/alpha",
            "nodes": [{"id": "basics", "title": "Basics", "children": [{"id": "basics.one", "title": "One"}]}]}
    p = repo / projection_path("alpha")
    p.parent.mkdir(parents=True)
    p.write_text(yaml.safe_dump(proj, allow_unicode=True), encoding="utf-8")
    config = load_config(repo)
    tracked = tracked_of(repo)
    scope = Scope(config, company_words(config, tracked))
    published, _ = load_published(repo, scope, tracked)
    assert published["alpha"].skeleton.title == "Alpha (projection)"
    assert "basics.two" not in published["alpha"].nodes
    assert {c.node for c in published["alpha"].cards} == {"basics.one"}   # cards of dropped nodes are not published
    # an untracked projection is ignored
    tracked -= {projection_path("alpha")}
    published, notes = load_published(repo, scope, tracked)
    assert published["alpha"].skeleton.title == "Alpha" and any("not tracked" in n for n in notes)
