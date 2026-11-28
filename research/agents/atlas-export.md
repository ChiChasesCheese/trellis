# Task: `trellis export` and `trellis snapshot` — the Atlas data contract (Phase 1)

Read first: `AGENTS.md`, `CONTEXT.md` (section "The Atlas": Atlas, View, Reach, Snapshot), `docs/adr/0014-*.md`,
`atlas.yaml`, `trellis/hold.py`, `trellis/anki.py` (`pull`, `invoke`), `trellis/cards.py` (`load_cards`, `Card`),
`trellis/skeleton.py` (`load_skeleton`, `Skeleton.folder`), `trellis/web.py` (`/api/state` builds a similar per-domain
standing — reuse its logic, do not fork it), `tests/conftest.py` and `tests/fake_anki.py`.

## Goal

The Atlas (a static site, built later) and agents read one contract. You write the engine half: two commands, one
library module per concern, tests. You do not write any site, HTML or JS.

```
trellis export [--out atlas-data] [--check]   # skeletons + cards + atlas.yaml + snapshots/ -> atlas-data/
trellis snapshot [--date YYYY-MM-DD]           # Anki -> snapshots/<date>.json (the only step that needs Anki)
```

## Rules that are not negotiable

1. **Only tracked files.** Export reads a card or skeleton only if `git ls-files` lists it. Chi's machine holds
   gitignored premium and private cards inside published domain folders (e.g. `vault/domains/hello-interview/cards/premium/`,
   3,226 files); they must never reach the output. CI and chi-mini must produce identical output from the same commit.
   Implement this once (a function returning the set of tracked paths, with an injectable override for tests).
2. **Scope comes from `atlas.yaml` only** (format documented in its header). Company words = folder names under
   `companies_from` plus `aliases`; a token match is a whole word inside an id split on `.`, `-`, `_` (so `tt` matches
   `tt` and `hi-tt-lc-x` but not `button`). A node whose id has a company word is left out with its subtree unless
   `allow` lists it (`<domain>:<node id>`) or the whole domain. `exclude` lists subtrees by node id prefix. A card is out
   when its node is out or its id has a company word. Strip tags starting with any `strip_tags` prefix.
   `--check` prints every left-out subtree and card count per domain and exits 0; it is what Chi reads before publishing.
3. **No Trace leaves the machine.** `snapshots/<date>.json` holds per-node aggregates only: no card ids with times, no
   review timestamps, nothing finer than a day.
4. **Tests never touch live Anki** (`tests/conftest.py` makes the real client refuse). `snapshot` takes the Anki call as a
   parameter like `trellis.anki.pull` does; tests pass a fake.
5. Do not run `snapshot` against the real Anki, do not commit, do not push. Chi's orchestrator reviews and commits.

## Reach (CONTEXT.md)

A card is studied when its own Anki card(s) have `reps > 0`, or when its **test question** has. Test questions are
notes tagged `<set>::id::<qid>` with `qid = f"{tag}-" + sha1(source_card_id).hexdigest()[:10]` for the sets in
`scripts/card_tests.py` `SETS` (tags `tlld`, `tai`). Read that file to confirm; list in `atlas.yaml`-independent code
the sets as data (a dict), not as a hard-coded branch. Also look at `scripts/daily_quiz.py` set `recog` (questions on
LeetCode tree problems, tag `recog`) and the quick deck (`scripts/quick_deck.py`, tap cards): if their questions map to a
source card id by a rule you can verify in the code, include them; otherwise list them in your report as not mapped.
A node's Reach = studied cards / cards under it (subtree included). Level for the colour: none (no cards: uncovered),
0, 1–24%, 25–49%, 50–74%, 75–99%, 100% → `level` −1..5.

Hold and flags: build traces for published cards (a card's own trace, else its test question's trace), then
`trellis.hold.assess`. Record per node: `hold` (rounded 3), and per leaf flags `weak`, `uncovered`, `sealed`, `settling`.

Daily counts: AnkiConnect `getNumCardsReviewedByDay` → `{date: n}` for the last 26 weeks plus all history in the
snapshot's `daily` (dates only).

## Snapshot file `snapshots/<date>.json`

```json
{"schema": "trellis.snapshot/1", "date": "2026-11-28", "domains": {"hft": {"cards": 531, "studied": 223, "hold": 0.91,
 "nodes": {"<node id>": {"cards": 4, "studied": 4, "hold": 1.0, "flags": ["weak"]}}}}, "daily": {"2026-11-27": 29}}
```

`snapshots/` is committed (it replaces `traces/` as the dated record, ADR 0014). Keep files small: omit zero/empty keys.

## Contract `atlas-data/` (gitignored, rebuilt by CI)

- `index.json`: `schema`, `generated_at`, `snapshot_date`, `reach_definition` (one Chinese sentence, from CONTEXT.md),
  `domains[]`: id, title, lang, nodes, leaves, cards, studied, reach, level, hold, weak[], uncovered[] (leaf ids).
- `d/<domain>.json`: domain meta + `nodes[]` flat, each: id, parent, title, summary, core, requires[], depth, order,
  cards, studied, reach, level, hold, flags[], readings[] (title + url only).
- `d/<domain>.md`: the tree as a Markdown outline, one line per node with `studied/cards` and flags — for agents.
- `d/<domain>/cards.jsonl`: published cards: id, node, type, step, q, a (Markdown; turn `[[x|y]]` into `y`, `[[x]]` into
  `x`, drop `obsidian://` links, keep mermaid fences and HTML), tags (after stripping).
- `history.json`: per domain per snapshot date: cards, studied, hold (from every file in `snapshots/`).
- `daily.json`: the latest snapshot's daily counts.
- `schema/*.schema.json`: JSON Schema (2020-12) for index, domain, card line, snapshot; ship them inside the package
  (`trellis/atlas_schema/`) and copy them out. Every JSON file carries `"schema": "trellis.<kind>/1"`.
- `llms.txt`: llmstxt.org format: H1, one-paragraph summary (what Trellis is, what Reach means), H2 sections linking
  `index.json`, every `d/<domain>.md` and `cards.jsonl`, with relative URLs.

## Code layout

- `trellis/atlas.py`: load `atlas.yaml`, company words, `published(skeleton) -> set of node ids`, `card_published(card)`,
  tracked-file filter. Pure functions.
- `trellis/snapshot.py`: build a snapshot from (published skeletons, cards, anki call). Pure except the call.
- `trellis/export.py`: write the contract from (published skeletons, cards, snapshots dir).
- `trellis/cli.py`: the two subcommands, following the file's existing style. `docs/reference/cli.md`: two rows.
- `.gitignore`: `atlas-data/`.
- `tests/test_atlas.py`: fixtures in tmp dirs (two tiny skeletons, cards, an `atlas.yaml`, a fake Anki). Cover: a
  company node and its subtree left out; `allow` keeps one; a card with `tt` in its id left out; `公司::` tags stripped;
  an untracked card file ignored; Reach counting a test question by the sha1 rule; level boundaries (0, 24/100, 25/100,
  99/100, 100/100); snapshot has no timestamps finer than a day; every output file carries its `schema` key and the
  required keys of its schema (validate with a small helper; do not add a dependency unless `jsonschema` is already in
  the environment — check `uv run python -c "import jsonschema"`).

## Done when

```bash
uv run --with pytest python -m pytest -q          # all green, yours included
uv run trellis --all validate                     # 0 errors
uv run trellis export --check                     # prints the left-out list (paste it in your report)
uv run trellis export --out /tmp/atlas-try        # runs on the real repo with no snapshot yet (Reach fields empty)
```

Report: files changed, test count, the `--check` output, which test-question sets are mapped and which are not and why,
and the three claims you are least sure about.

Resume rule: if `trellis/atlas.py` etc. already exist from an earlier run, read them and continue; do not start over.
