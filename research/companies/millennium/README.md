# Millennium kit — research area

How the kit in `vault/interviews/companies/millennium/` was made. Learning pages (entry `README.md`, `CONTENTS.md`, `loop/LOOP_GUIDE.md`, `loop/rounds/`, `study/`, `01-company-brief.md`, `02-process.md`, `fit.md`, `06-questions-to-ask.md`) stay in the vault.

- `catalog/`: `CATALOG.md` (problem table), `RANK.md` / `PARETO.md` (28 rule, cut line), `raw/` (one file per source, GitHub first).
- `reports/COVERAGE.md`: coverage of reported problems.
- `CHECKPOINT.md`, `LEDGER.md`, `CONVENTIONS.md`, `tasks/AGENT_PROBLEMS.md`: build state and agent rules.
- `tools/`: pareto, coverage, summary, contents (writes the vault's `CONTENTS.md`), articles_readme, verify_suites, `tree/` (`check_tree.py` + `interview-loop.yaml`). Their relative paths still assume the old in-kit layout; adjust before running.
- The vault keeps `tools/progress.py` and `tools/pytest_progress.py` because `loop/mock.py` imports them.
