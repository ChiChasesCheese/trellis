# Architecture

Trellis is a skeleton-constrained knowledge base: a YAML mind map decides what exists, the Obsidian vault holds the content,
Anki is the build target for spaced repetition. Vocabulary: `CONTEXT.md`.

## From skeleton to Anki

| Step | Command | Output |
|---|---|---|
| 1. Declare | author `skeleton/<d>.yaml` | what exists, in what order (ADR 0002, 0005) |
| 2. Fill | cards, readings, drills in the vault | content hung on leaves |
| 3. Check, map | `validate`, `sync` | map notes: topic, reading, card in one graph |
| 4. Build | `build` | `dist/<d>.apkg`, cards numbered in Sequence (ADR 0010) |
| 5. Publish | `anki-push` | Anki and AnkiWeb, then the phone |
| 6. Learn | `pull` | `traces/<d>.json`, the review history |
| 7. Decide | `brief`, `feed`, `grow` | what to do next, new cards for weak leaves (ADR 0009) |

- **Skeleton** is the only source of truth for what topics exist, their order and prerequisites (`requires`). A skeleton's
  `vault:` line says where its content lives (ADR 0008); the slug is the identity in card ids, Anki decks and traces.
- **Cards and readings** are plain markdown attached to leaves; **drills** train producing an answer. Ordinary wikilinks
  connect them. Cards open the reading in Obsidian (ADR 0001).
- **Content comes in three ways**: written from the field (ADR 0002), digested from a corpus (`corpora/` -> `sources/` ->
  `pipeline/`, ADR 0006), or distilled from a codebase as cases (`codebases/`, ADR 0003). LLM steps are prompt out, JSON in:
  `triage` / `digest` / `grow` write prompts, `accept` / `--import` validate the answer before touching the vault.
- **The loop** pulls review history into `traces/` (ADR 0004), seals leaves whose prerequisites do not hold (ADR 0005) and
  waits for a verdict before acting again (ADR 0009).

## Vault vs research

Two areas (ADR 0011):

| Area | Path | Holds | Rule |
|---|---|---|---|
| Learning | `vault/` | what Chi studies or practises with | no sources, confidence, ledgers, agent talk (`proposals/WRITING_RULES.md`) |
| Research | `research/companies/<co>/`, `research/agents/`, `proposals/` | sources, catalogs, provenance, checkpoints, task files, pipeline JSON | never inside `vault/` |

The vault is opened in Obsidian, so everything in it must read as a study page; `scripts/plain_style.py` enforces the
machine-checkable half. Runnable practice (problem tests, `drill.py`) stays in the kit; authoring tools move to research.
Company kits are plain notes, not trellis domains; their general topics are domain branches or `core/<topic>/<co>/`.

## Sync: Obsidian Sync, the server's Git plugin and agents

1. Agents push to GitHub `main`.
2. The Git plugin in chi-mini's Obsidian pulls into `~/Code/trellis/vault` every 5 minutes.
3. Obsidian Sync carries the vault from chi-mini to the phone and laptop.
4. Edits made on the phone or laptop come back through Sync; the Git plugin on chi-mini commits and pushes them every
   10 minutes (vault folder only).

- Agents work in the repo and merge to `main`; they never write into another vault.
- chi-mini is the always-on hub: its Obsidian runs the Git plugin on `vault/` only (pull 5 min, commit + push 10 min,
  rebase), and Obsidian Sync carries the vault to the phone and laptop.
- Only one machine runs the Git plugin's auto commit against a Sync-connected vault; elsewhere set the interval to 0 or use
  Sync alone. Card links name the vault and address notes by name, so they work wherever the vault root is (ADR 0001;
  the current remote vault name is in the sync how-to).
- Anki is separate: `anki-push` runs on a machine with desktop Anki and AnkiConnect.

Setup and state: `docs/how-to/obsidian-sync.md`. Decisions: ADR 0001, 0007, 0008, 0011.
