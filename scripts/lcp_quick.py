"""LeetCode Project ten-second cards: one tap-or-glance card per fine-grained exam point of a project.

    uv run python scripts/lcp_quick.py gate [<slug> ...]              # check written cards (shape, length, one per point)
    uv run python scripts/lcp_quick.py push [--dry-run] [--unverified] [<slug> ...]   # update Anki, import what never was
    uv run python scripts/lcp_quick.py weak [days]                    # points answered Again/Hard lately, and their leaves

Chi (2026-11-16): no typing; cards read like vocabulary, so he knows at a glance whether he knows the point and grades
1-4; points as fine as possible; an extension line under the answer that does not count toward the point; most cards
under ten seconds, a few longer synthesis cards (those stay in the vault, tag 作答). The formats, length limits and
note types are the quick deck's (scripts/quick_deck.py), plus `multi` (pick every right option) and `bug` (tap the
wrong line of a short code excerpt).

Everything here is local: the cards restate LeetCode Premium workspaces. Per project, in sources/local/lc-project/quick/:
points/<slug>.json   [{"kp": "<slug>.<point>", "title": "...", "kind": "...", "leaves": ["<lld leaf id>", ...]}]
cards/<slug>.jsonl   one card per point, quick-deck schema, `based_on` from SOURCES
verify/<slug>.jsonl  the verifier's verdicts (ok / fix / drop, as in the quick deck)
Agents write them following proposals/lld/LCP_QUICK_AGENT.md. In Anki a card's home is its project's sub-deck of
低层设计（LLD）::28 LeetCode Project（实战项目）; the view deck `8 LC Project` borrows them (scripts/lcp_plan.py).
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import quick_deck as qd  # noqa: E402

HOME = ROOT / "sources/local/lc-project/quick"
TAG = "lcpq"
ROOT_DECK = "低层设计（LLD）::28 LeetCode Project（实战项目）"
SOURCES = ("readme", "overview", "template", "tests", "solution", "article", "reflection", "bank")
KINDS = ("rule", "mechanism", "pitfall", "decision", "number", "agent", "test", "file", "recall")
# file: a reading card for one workspace file (题目); recall: a question on the problem itself, asked after the files (题目理解)


def slugs(args: list[str]) -> list[str]:
    return args or sorted(f.stem for f in (HOME / "points").glob("*.json") if "." not in f.stem)  # skip <slug>.read side files


def titles() -> dict[str, str]:
    """Project slug -> its leaf title, the Anki sub-deck the leaf's cards live in."""
    from trellis.project import load_project
    sk = load_project(ROOT, "low-level-design").skeleton
    return {l.id.split(".", 1)[1].removeprefix("lcp-"): l.title for l in sk.leaves() if l.id.startswith("lcproject.lcp-")}


def points(slug: str) -> list[dict]:
    f = HOME / "points" / f"{slug}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else []


def rows(folder: str, slug: str) -> tuple[list[dict], list[str]]:
    f = HOME / folder / f"{slug}.jsonl"
    return qd.read_rows(f) if f.exists() else ([], [])


def load(slug: str, verified_only: bool) -> tuple[list[dict], list[str]]:
    """The project's usable cards in point order, after the verifier's verdicts."""
    pts = points(slug)
    known = {p["kp"]: {**p, "cards": [{"id": s} for s in SOURCES]} for p in pts}
    problems = [f"{slug}: point {p.get('kp')} needs kp, title, kind in {KINDS}, leaves"
                for p in pts if not (p.get("kp", "").startswith(slug + ".") and p.get("title") and p.get("kind") in KINDS and p.get("leaves"))]
    cards_in, bad = rows("cards", slug)
    verdicts_in, vbad = rows("verify", slug)
    problems += bad + vbad
    verdicts = {v.get("kp"): v for v in verdicts_in}
    if cards_in and verified_only and not verdicts:
        return [], problems + [f"{slug}: not verified yet"]
    by_kp, out = {}, []
    for c in cards_in:
        kp, v = c.get("kp"), verdicts.get(c.get("kp"), {})
        if c.get("skip") or v.get("verdict") == "drop":
            continue
        if v.get("verdict") == "fix" and v.get("card"):
            c = {**v["card"], "kp": kp, "based_on": v["card"].get("based_on") or c.get("based_on")}
        elif v.get("more"):
            c = {**c, "more": v["more"]}
        if verified_only and v.get("verdict") not in ("ok", "fix"):
            problems.append(f"{slug} {kp}: no verdict")
            continue
        errs = qd.check(c, known) + (qd.check_more(c["more"], c) if "more" in c else [] if c.get("fmt") == "read" else ["more is missing"])
        if kp in by_kp:
            errs.append("a second card for the point")
        if errs:
            problems.append(f"{slug} {kp} [{c.get('fmt')}]: " + "; ".join(errs))
            continue
        by_kp[kp] = c
    rank = {p["kp"]: i for i, p in enumerate(pts)}
    for kp, c in sorted(by_kp.items(), key=lambda kv: rank.get(kv[0], 1e9)):
        out.append({**c, "_point": known[kp]})
    return out, problems


def gate(args: list[str]) -> int:
    failed = 0
    for slug in slugs(args):
        cards, problems = load(slug, verified_only=False)
        pts = points(slug)
        missing = [p["kp"] for p in pts if p["kp"] not in {c["kp"] for c in cards}]
        mix = Counter(c["fmt"] for c in cards)
        tapped = sum(mix[f] for f in qd.TAPPED)
        print(f"{slug}: {len(pts)} points, {len(cards)} ok, {len(problems)} failing, {len(missing)} without a card; "
              + " ".join(f"{f} {mix[f]}" for f in qd.FORMATS if mix[f]) + f"; tapped {tapped}/{len(cards) or 1}")
        for p in problems:
            print("   ", p)
        failed += len(problems)
    return 1 if failed else 0


def package(cards: list[dict], deck_of: dict[str, str], path: Path) -> dict[str, dict]:
    import genanki
    from trellis.build import _stable_id, note_fields

    sides = qd.templates()
    models = {k: genanki.Model(_stable_id(f"trellis:model:{name}"), name, fields=[{"name": f} for f in (*names, *note_fields())],
                               templates=[{"name": name.split()[-1], "qfmt": sides[k][0], "afmt": sides[k][1]}], css=qd.css(),
                               **({"model_type": genanki.Model.CLOZE} if cloze else {}))
              for k, (name, names, _front, _back, cloze) in qd.MODELS.items()}
    decks: dict[str, object] = {}
    built = {}
    for n, c in enumerate(cards):
        slug = c["kp"].split(".", 1)[0]
        name = deck_of[slug]
        deck = decks.setdefault(name, genanki.Deck(_stable_id(f"trellis:deck:{name}"), name))
        key, vals = qd.fields(c, {"topic_title": name.rsplit("::", 1)[-1], "title": c["_point"]["title"]})
        ident = f"{TAG}.{c['kp']}"
        tags = [TAG, f"{TAG}::{slug}", "lcproject", f"kp::{c['kp']}", f"fmt::{c['fmt']}", f"id::{ident}"]
        deck.add_note(genanki.Note(model=models[key], fields=vals + [""] * len(note_fields()), guid=genanki.guid_for(f"trellis:{ident}"),
                                   tags=tags, due=n + 1))
        built[ident] = {"fields": dict(zip(qd.MODELS[key][1], vals)), "model": qd.MODELS[key][0], "tags": tags}
    genanki.Package(list(decks.values())).write_to_file(path)
    return built


def push(args: list[str]) -> int:
    from anki_refresh import call, match_note_fields

    dry, verified_only = "--dry-run" in args, "--unverified" not in args
    args = [a for a in args if not a.startswith("--")]
    match_note_fields()
    names = titles()
    cards, problems = [], []
    for slug in slugs(args):
        c, p = load(slug, verified_only)
        cards += c
        problems += p
    for p in problems:
        print("  ", p)
    deck_of = {s: f"{ROOT_DECK}::{names[s]}" for s in {c["kp"].split('.', 1)[0] for c in cards}}
    pushed_file = HOME / "pushed.json"
    pushed = set(json.loads(pushed_file.read_text(encoding="utf-8"))) if pushed_file.exists() else set()
    ids = call("findNotes", query=f"tag:{TAG}")
    info = []
    for i in range(0, len(ids), 400):
        info += call("notesInfo", notes=ids[i:i + 400])
    present = {next(t[4:] for t in n["tags"] if t.startswith("id::")): n for n in info}
    folder = Path(tempfile.mkdtemp(prefix="lcpq-"))
    built = package(cards, deck_of, folder / "all.apkg")
    changes, retype = [], []
    for ident, b in built.items():
        note = present.get(ident)
        if not note:
            continue
        if note["modelName"] != b["model"]:
            retype.append(ident)
            continue
        diff = {k: v for k, v in b["fields"].items() if note["fields"][k]["value"] != v}
        if diff:
            changes.append({"id": note["noteId"], "fields": diff})
    fresh = [c for c in cards if f"{TAG}.{c['kp']}" not in present and f"{TAG}.{c['kp']}" not in pushed]
    print(f"{len(cards)} usable cards, {len(present)} in Anki, {len(changes)} to update, {len(fresh)} to add"
          + (f", {len(retype)} changed format (left as they are): {' '.join(retype[:5])}" if retype else ""))
    if dry:
        shutil.rmtree(folder, ignore_errors=True)
        return 0
    for i in range(0, len(changes), 50):
        call("multi", actions=[{"action": "updateNoteFields", "params": {"note": c}} for c in changes[i:i + 50]])
    if fresh:
        package(fresh, deck_of, folder / "fresh.apkg")
        call("importPackage", path=str(folder / "fresh.apkg"))
        pushed |= {f"{TAG}.{c['kp']}" for c in fresh}
        pushed_file.parent.mkdir(parents=True, exist_ok=True)
        pushed_file.write_text(json.dumps(sorted(pushed)), encoding="utf-8")
    known = set(call("modelNames"))
    for key, (name, *_rest) in qd.MODELS.items():
        if name not in known:
            continue
        call("updateModelStyling", model={"name": name, "css": qd.css()})
        front, back = qd.templates()[key]
        for card, now in call("modelTemplates", modelName=name).items():
            if (now["Front"], now["Back"]) != (front, back):
                call("updateModelTemplates", model={"name": name, "templates": {card: {"Front": front, "Back": back}}})
                print(f"template updated: {name}")
    call("sync")
    shutil.rmtree(folder, ignore_errors=True)
    return 0


def weak(days: int = 14) -> list[str]:
    """Leaves behind the points Chi answered Again or Hard in the last `days` days, the most missed first."""
    from anki_refresh import call

    cids = call("findCards", query=f"tag:{TAG} (rated:{days}:1 OR rated:{days}:2)")
    if not cids:
        return []
    notes = {c["note"] for c in call("cardsInfo", cards=cids)}
    kps = [t[4:] for n in call("notesInfo", notes=sorted(notes)) for t in n["tags"] if t.startswith("kp::")]
    leaf_of = {p["kp"]: p["leaves"] for s in slugs([]) for p in points(s)}
    count = Counter(leaf for kp in kps for leaf in leaf_of.get(kp, []))
    return [leaf for leaf, _ in count.most_common()]


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] not in ("gate", "push", "weak"):
        print(__doc__)
        return 2
    if args[0] == "gate":
        return gate(args[1:])
    if args[0] == "push":
        return push(args[1:])
    print("\n".join(weak(int(args[1]) if len(args) > 1 else 14)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
