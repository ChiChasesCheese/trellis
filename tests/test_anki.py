from trellis.anki import align
from trellis.skeleton import load_skeleton

SKELETON = """
domain: demo
title: Demo
nodes:
  - id: alpha
    order: 7
    title: Alpha
    children:
      - id: alpha.one
        title: One
"""


class FakeAnki:
    """Collection with one mis-decked card and one stale empty deck."""

    def __init__(self):
        self.decks = {
            "Demo::01 Alpha::One": [],          # stale ordinal, now empty
            "Demo::07 Alpha": [101],            # card sitting on the branch deck
            "Demo::07 Alpha::One": [],
        }
        self.tags = {101: "demo::alpha::one"}
        self.calls = []

    def __call__(self, action, url, **params):
        self.calls.append(action)
        if action == "findCards":
            q = params["query"]
            if q.startswith("tag:"):
                tag = q.split()[0][len("tag:"):]
                exclude_deck = q.split('-deck:"')[1].rstrip('"')
                return [cid for cid, t in self.tags.items()
                        if t == tag and cid not in self.decks.get(exclude_deck, [])]
            deck = q.split('deck:"')[1].rstrip('"')
            return [cid for name, cards in self.decks.items()
                    if name == deck or name.startswith(deck + "::")
                    for cid in cards]
        if action == "createDeck":
            self.decks.setdefault(params["deck"], [])
            return None
        if action == "changeDeck":
            for cards in self.decks.values():
                for cid in params["cards"]:
                    if cid in cards:
                        cards.remove(cid)
            self.decks[params["deck"]].extend(params["cards"])
            return None
        if action == "deckNames":
            return list(self.decks)
        if action in ("sync", "importPackage"):
            return None
        if action == "deleteDecks":
            for name in params["decks"]:
                del self.decks[name]
            return None
        raise AssertionError(f"unexpected action {action}")


def test_align_moves_cards_and_deletes_stale_decks(tmp_path):
    path = tmp_path / "s.yaml"
    path.write_text(SKELETON, encoding="utf-8")
    skeleton = load_skeleton(path)
    fake = FakeAnki()

    result = align(skeleton, call=fake)

    assert result["moved"] == 1
    assert fake.decks["Demo::07 Alpha::One"] == [101]
    # stale ordinal deck gone; current decks (with cards beneath) kept
    assert "Demo::01 Alpha::One" not in fake.decks
    assert "Demo::07 Alpha" in fake.decks


def test_align_noop_on_clean_collection(tmp_path):
    path = tmp_path / "s.yaml"
    path.write_text(SKELETON, encoding="utf-8")
    skeleton = load_skeleton(path)
    fake = FakeAnki()
    align(skeleton, call=fake)
    calls_before = len(fake.calls)
    result = align(skeleton, call=fake)
    assert result["moved"] == 0 and result["deleted"] == []
    assert len(fake.calls) > calls_before  # it did re-check, found nothing


def test_push_syncs_before_importing_and_after_aligning(tmp_path):
    """The order is the reason this is one command: pulling first means
    the import lands on the phone's current scheduling, and pushing last
    is what actually gets the new cards onto the phone."""
    from trellis.anki import push

    path = tmp_path / "s.yaml"
    path.write_text(SKELETON, encoding="utf-8")
    skeleton = load_skeleton(path)
    fake = FakeAnki()
    apkg = tmp_path / "demo.apkg"
    apkg.write_bytes(b"not really a package")

    result = push(skeleton, apkg, call=fake)

    ordered = [c for c in fake.calls if c in ("sync", "importPackage", "changeDeck")]
    assert ordered[0] == "sync"
    assert ordered.index("importPackage") < ordered.index("changeDeck")
    assert ordered[-1] == "sync"
    assert result["moved"] == 1
    assert any("imported demo.apkg" in s for s in result["steps"])


def test_push_builds_the_package_instead_of_trusting_dist(tmp_path, monkeypatch):
    """Anki updates a note only when the incoming one is newer, so pushing
    a package built before the collection last changed silently leaves
    those notes stale. Building inside push removes that footgun."""
    from trellis import cli

    (tmp_path / "skeleton").mkdir()
    (tmp_path / "skeleton" / "demo.yaml").write_text(SKELETON, encoding="utf-8")
    cards = tmp_path / "vault" / "demo" / "cards"
    cards.mkdir(parents=True)
    (cards / "alpha-c.md").write_text(
        "---\nid: alpha-c\nnode: alpha.one\ntype: qa\n---\n## Q\nq?\n\n## A\na.\n",
        encoding="utf-8")

    order = []
    monkeypatch.setattr(cli, "build_package", lambda *a, **k: (
        order.append("build"), {"notes": 1, "decks": 1, "path": str(a[2])})[1])
    monkeypatch.setattr(cli, "push", lambda *a, **k: (
        order.append("push"), {"steps": [], "moved": 0, "deleted": []})[1], raising=False)
    import trellis.anki
    monkeypatch.setattr(trellis.anki, "push", lambda *a, **k: (
        order.append("push"), {"steps": [], "moved": 0, "deleted": []})[1])

    assert cli.main(["--root", str(tmp_path), "anki-push"]) == 0
    assert order == ["build", "push"]


def test_deck_names_are_escaped_inside_a_quoted_search():
    from trellis.anki import _quoted
    assert _quoted('keep it "hot"') == 'keep it \\"hot\\"'
    assert _quoted("a_b*c") == "a\\_b\\*c"


def test_invoke_waits_out_a_collection_busy_syncing(monkeypatch):
    import trellis.anki as anki
    answers = [anki.AnkiConnectError(anki.BUSY[0]), anki.AnkiConnectError(anki.BUSY[1]), 42]

    def once(action, url, **params):
        a = answers.pop(0)
        if isinstance(a, Exception):
            raise a
        return a

    monkeypatch.setattr(anki, "_invoke_once", once)
    monkeypatch.setattr(anki.time, "sleep", lambda s: None)
    assert anki.invoke("importPackage", path="x.apkg") == 42


def test_push_carries_on_when_positions_cannot_be_written(tmp_path):
    from trellis.anki import PositionsLocked, push
    from trellis.skeleton import load_skeleton
    import trellis.anki as anki
    sk = tmp_path / "s.yaml"
    sk.write_text("domain: d\ntitle: D\nnodes:\n- id: a\n  title: A\n  summary: s\n")
    skeleton = load_skeleton(sk)
    calls = []

    def call(action, url=None, **params):
        calls.append(action)
        return [] if action in ("findCards", "deckNames") else None

    def locked(*a, **k):
        raise PositionsLocked(3)

    original = anki.sequence_new
    anki.sequence_new = locked
    try:
        result = push(skeleton, tmp_path / "d.apkg", call=call, ordered=["x"])
    finally:
        anki.sequence_new = original
    assert calls[-1] == "sync"
    assert any("import order" in s for s in result["steps"])


def test_align_deletes_only_the_topmost_stale_decks(tmp_path):
    from trellis.anki import align
    from trellis.skeleton import load_skeleton
    sk = tmp_path / "s.yaml"
    sk.write_text("domain: d\ntitle: D\nnodes:\n- id: a\n  title: A\n  summary: s\n")
    deleted = []

    def call(action, url=None, **params):
        if action == "deckNames":
            return ["D", "D::01 A", "D::02 Old", "D::02 Old::Leaf"]
        if action == "deleteDecks":
            deleted.extend(params["decks"])
        if action == "findCards" and params.get("query") in ('deck:"D"', 'deck:"D::01 A"'):
            return [1]
        return []

    result = align(load_skeleton(sk), call=call)
    assert deleted == ["D::02 Old"]
    assert set(result["deleted"]) >= {"D::02 Old", "D::02 Old::Leaf"}
