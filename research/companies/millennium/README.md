# Millennium kit — research area

How the kit in `vault/interviews/companies/millennium/` was made. Learning pages (entry `README.md`, `CONTENTS.md`, `loop/LOOP_GUIDE.md`, `loop/rounds/`, `study/`, `01-company-brief.md`, `02-process.md`, `fit.md`, `06-questions-to-ask.md`) stay in the vault.

- `catalog/`: `CATALOG.md` (problem table), `RANK.md` / `PARETO.md` (28 rule, cut line), `raw/` (one file per source, GitHub first).
- `reports/COVERAGE.md`: coverage of reported problems.
- `CHECKPOINT.md`, `LEDGER.md`, `CONVENTIONS.md`, `tasks/AGENT_PROBLEMS.md`: build state and agent rules.
- `tree/interview-loop.yaml`: the round/skill/problem tree. The authoring tools are the shared `trellis kit` commands (`trellis/kit/`), run from the repo root: `trellis kit pareto|coverage|summary|contents|articles_readme|verify_suites|check_tree --co millennium` (`--kit` / `--research` override the two directories; `trellis kit <tool> --help`).
- `loop/mock.py` imports the practice runtime from `trellis.kit` (`progress`, `pytest_progress`); run it with `uv run --project <repo root> python loop/mock.py …`.
