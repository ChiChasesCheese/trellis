# Names and layout for new content

Date: 2026-10-23.

Kits and domains were named by whoever wrote them: `00-README.md`, `CONTENTS.md`, `01-company-brief.md`, `q01_fraud_mcc_disputes`,
`04_sd`, `oodNN-*.md`, notes with spaces, hubs in English or Chinese. A tool or an agent could not predict where an entry
point, an ordered chapter or a hub would be. These rules apply to **new content only**. Nothing is bulk-renamed: wikilinks
resolve by note name, but card ids, Anki GUIDs, tests, tool paths and plain-text links all depend on current names, and a
rename buys little (ADR 0010 made the same call for card file names: 800 renames, and a card id is its identity in Anki).

The rules:

1. **Kit entry is `README.md`** in `vault/interviews/companies/<co>/` (and in `research/companies/<co>/`). An index page is a
   separate, optional note.
2. **Ordered directories and files use a two-digit prefix with an underscore**: `00_overview.md`, `01_loop.md`, `02_lp/`.
   Start at `00`; the prefix is the reading order, never an id.
3. **Problem directories are `<prefix><nn>_<snake_slug>`**, where the prefix is the round or kind letter(s) and `nn` is
   two-digit, e.g. `q01_fraud_mcc_disputes`, `ood03_parking_lot`. Slugs are lower-case ASCII snake_case.
4. **Learning note file names are ASCII kebab-case** (`consistent-hashing.md`, `leader-election.md`); the Chinese title is
   the H1 inside the file. No spaces in new file names. Names stay unique across the vault, because wikilinks and card links
   address notes by name (ADR 0001).
5. **Domain hubs are `<Title> MOC.md`**, one per domain, written by `trellis sync`. The title is the skeleton title, so a
   Chinese-native domain (the zh rule in `AGENTS.md`) has a Chinese title. The single space before `MOC` is the only space
   allowed in a new file name.
6. **General topics live under `vault/interviews/core/<topic>/<co>/`** while a company's loop is on, and are flattened into
   `core/<topic>/` afterwards (ADR 0008, `AGENTS.md`). Company-only rounds stay in the kit.
7. **Diagrams follow `proposals/WRITING_RULES.md` rule 12**: tables and lists first, then mermaid within rule 9, narrow
   ASCII (<= 40 columns, no CJK on a drawing line) last; `scripts/phone_diagrams.py` checks it.
8. Process files belong in `research/` (ADR 0011) and are named per `research/AGENTS.md`: `CHECKPOINT.md`, `LEDGER.md`,
   `PROVENANCE.md`, `<NAME>_TASK.md`.

**Existing exceptions, left as they are.** Snowflake and Headlands keep hyphen-prefixed files (`01-company-brief.md`,
`06-questions-to-ask.md`) and Snowflake keeps `CONTENTS.md` beside its `README.md`; the reported write-ups under
`core/system-design/` and `core/low-level-design/amazon/` are `sdNN-*.md` and `oodNN-*.md`, checked under those names by
`check_sd.py` and `check_ood.py`; about thirty vault files contain spaces; Snowflake and Low-Level Design each have two hubs
(English and Chinese titles). A migration (ADR 0011) moves files but does not rename them. If a rename is ever wanted, do it per kit in one commit with
a link audit (`scripts/check_wikilinks.py`), never mixed with content changes.

**Consequences.** Agents can predict entry points and hubs for new kits; checkers can rely on `README.md`. Old and new
conventions coexist, so a tool that globs names must accept both until a kit is deliberately renamed.
