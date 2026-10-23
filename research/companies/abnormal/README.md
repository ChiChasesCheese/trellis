# Abnormal kit — research area

How the kit in `vault/interviews/companies/abnormal/` was made. Learning pages (entry `README.md`, `CONTENTS.md`, `loop/LOOP_GUIDE.md`, `loop/PRACTICE_INDEX.md`, `loop/rounds/` incl. the `cb*` practice codebases, `study/`, `01-company-brief.md`, `02-process.md`, `fit.md`, `06-questions-to-ask.md`) stay in the vault.

- `catalog/`: `CATALOG.md` (problem table), `RANK.md` / `PARETO.md` (28 rule, cut line), `raw/` (one file per source, GitHub first).
- `reports/COVERAGE.md`: coverage of reported problems.
- `CHECKPOINT.md`, `LEDGER.md`, `CONVENTIONS.md`: build state and the codebase-exercise shape rules.
- `tasks/`: agent briefs `AGENT_CODEBASES.md`, `AGENT_ONSITE.md`, `AGENT_RESEARCH.md` and `acceptance_conftest.py` (template copied into each `acceptance/conftest.py`).
- `tree/interview-loop.yaml`: the round/skill/problem tree. `tools/make_banks.py` builds the `bank.json` files (Abnormal-only; its paths still assume the old in-kit layout). The other authoring tools are the shared `trellis kit` commands, run from the repo root: `trellis kit pareto|coverage|summary|contents|articles_readme|verify_suites|check_tree --co abnormal`. The Abnormal defaults (codebase-style `contents`, `cb`/`cr`/`ic` coverage rows, `verify_suites` on `cbNN_*/acceptance/`) come from its profile in `trellis/kit/paths.py`.
- `loop/mock.py` imports the practice runtime from `trellis.kit`; run it with `uv run --project <repo root> python loop/mock.py …`.
