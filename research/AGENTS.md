# research/ — the research area

Nothing under `research/` is a learning page. Chi never studies from it; it is how the learning pages in `vault/` were
made (ADR 0011). Obsidian does not open this tree, so process talk is allowed here and forbidden in `vault/`
(`proposals/WRITING_RULES.md` rule 1).

## `research/companies/<co>/`

Everything about *how* one company kit was made. Learning pages live in `vault/interviews/companies/<co>/`.

- Sources and evidence: `catalog/` (`raw/` one file per source, `CATALOG.md`, `PARETO.md`), `reports/`, harvest JSON,
  coverage outputs, `archive/`.
- Process: `README.md` (5-10 lines: what is here, where the learning pages are), `CHECKPOINT.md` (state + next action),
  `LEDGER.md` (one row per accepted task), `HANDOFF.md`, `CONVENTIONS.md`, `PROVENANCE.md` (where each fact came from).
- Agent files: `AGENT*.md`, `AGENT_RULES.md`, `<TOPIC>_TASK.md` (one atomic task per file, upper-case snake case ending
  in `_TASK`, e.g. `SD_TASK.md`), nested `CLAUDE.md` / `AGENTS.md` for that company.
- Authoring tools: `tools/` (pareto, coverage, summary, verify_suites, refresh_check ...), card JSON in `cards/`,
  generated `bank.json`.
- Needs a runner the learner uses (`drill.py`, `loop/mock.py`)? That stays in the kit, not here.

## `research/agents/`

Task files that are not tied to one company, e.g. `MIGRATE_KIT_TASK.md` (split an old kit into learning + research area).
Same naming: `<VERB>_<OBJECT>_TASK.md`.
Naming: ADR 0012. Resume from `CHECKPOINT.md`; skip rows already in `LEDGER.md`.
