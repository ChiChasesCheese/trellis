# Abnormal kit — research area

How the kit in `vault/interviews/companies/abnormal/` was made. Learning pages (entry `README.md`, `CONTENTS.md`, `loop/LOOP_GUIDE.md`, `loop/PRACTICE_INDEX.md`, `loop/rounds/` incl. the `cb*` practice codebases, `study/`, `01-company-brief.md`, `02-process.md`, `fit.md`, `06-questions-to-ask.md`) stay in the vault.

- `catalog/`: `CATALOG.md` (problem table), `RANK.md` / `PARETO.md` (28 rule, cut line), `raw/` (one file per source, GitHub first).
- `reports/COVERAGE.md`: coverage of reported problems.
- `CHECKPOINT.md`, `LEDGER.md`, `CONVENTIONS.md`: build state and the codebase-exercise shape rules.
- `tasks/`: agent briefs `AGENT_CODEBASES.md`, `AGENT_ONSITE.md`, `AGENT_RESEARCH.md` and `acceptance_conftest.py` (template copied into each `acceptance/conftest.py`).
- `tools/`: pareto, coverage, summary, contents (writes the vault's `CONTENTS.md`), articles_readme, make_banks (builds the `bank.json` files), verify_suites (kit acceptance gate), `tree/` (`check_tree.py` + `interview-loop.yaml`). Their relative paths still assume the old in-kit layout; adjust before running.
- The vault keeps `tools/progress.py` and `tools/pytest_progress.py` because `loop/mock.py` imports them.
