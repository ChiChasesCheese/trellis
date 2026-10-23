# CLI reference

Generated from `uv run trellis --help` and each subcommand's `--help` (2026-10-23). Run `uv run trellis <cmd> --help` for the
current text.

```
trellis [--root ROOT] [--domain DOMAIN] [--all] <command> ...
```

Global options (also accepted after the subcommand): `--root ROOT` project root (default cwd); `--domain DOMAIN` domain slug
(default: the only skeleton); `--all` run over every skeleton in `skeleton/`.

## Vault and cards

| Command | Options | What it does |
|---|---|---|
| `validate` | | check skeleton, cards, readings, drills |
| `sync` | | regenerate Obsidian map notes and corpus notes |
| `build` | `-o OUTPUT`, `--force`, `--lang LANG`, `--corpus CORPUS`, `--vault-name NAME` | compile the vault into an Anki `.apkg` (`dist/<domain>[.<lang>].apkg`); `--lang` renders translations (ids unchanged); `--corpus` only cards written from that corpus; `--force` builds despite rewritten-looking translations |
| `clip` | `--node NODE` | archive readings' pages as markdown in the vault (needs `--extra clip`) |
| `stats` | | card counts and leaf coverage per branch |
| `path` | `--weeks N` | write the linear study path into the vault |
| `steps` | `-o FILE`, `--branch ID`, `--pending`, `--check`, `--import FILE` | per-leaf card order: no option lists leaves without one; `-o` writes a prompt; `--import` lands `{leaf: [card ids]}` as `step:` lines; `--check` validates only |
| `scaffold NODE` | `-n COUNT`, `-o OUTPUT` | emit an LLM prompt for a node (no language rules; prefer `digest` / `grow`) |
| `import FILE` | | import LLM-generated JSON as cards |
| `adopt [NAME]` | `--title`, `--force`, `--anki DECK`, `--prefix`, `--anki-url` | turn a correctly formatted vault folder into a domain (no name lists adoptable folders); `--anki` adopts a deck that lives only in Anki |

## Corpora, codebases, growing content

| Command | Options | What it does |
|---|---|---|
| `ingest CORPUS` | `--retry` | fetch / parse `corpora/<id>.yaml` into `sources/archive/` and `sources/outlines/`; `--retry` re-attempts failed chapters |
| `seed CORPUS` | `-o OUTPUT` | prompt that drafts a skeleton for a subject that has none (ADR 0006) |
| `triage NAME` | `--kinds`, `--lens`, `--prefix`, `-o OUTPUT` | triage prompt for a codebase (`codebases/<name>.yaml`) or an ingested corpus |
| `accept FILE` | | validate a proposal (seed, corpus, codebase) and write what it accepts |
| `digest CORPUS` | `--status` (default), `--next`, `--leaf ID`, `--import FILE`, `-n COUNT`, `--budget CHARS`, `-o OUTPUT` | write cards from a corpus leaf by leaf |
| `grow` | `--next`, `--leaf DOMAIN:ID`, `--import FILE`, `-n COUNT`, `--budget CHARS`, `-o OUTPUT` | cards where the loop says it pays; imported cards are tagged `grown` |

## Anki and the review loop

| Command | Options | What it does |
|---|---|---|
| `anki-push` | `--lang LANG`, `--apkg PATH`, `--anki-url URL` | build, sync AnkiWeb, import, align, sync again (needs desktop Anki + AnkiConnect) |
| `anki-align` | `--anki-url URL` | move cards to the decks and positions the skeleton defines; delete stale empty decks |
| `pull` | `--anki-url URL` | read review history into `traces/<domain>.json` (the only command that asks Anki a question) |
| `brief` | `--print` | write `vault/Brief.md`: what to do next, ranked across domains |
| `feed` | `-n LIMIT`, `--include-sealed` | print the filtered-deck recipe for one interleaved stream; sealed leaves held back unless `--include-sealed` |
| `serve` | `--port PORT`, `--no-open` | open the local Workbench page |

Common recipes: `docs/how-to/build-and-push-anki-decks.md`. Design background: ADRs 0004-0010.
