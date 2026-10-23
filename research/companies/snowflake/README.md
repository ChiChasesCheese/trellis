# Snowflake kit — research area

How the kit in `vault/interviews/companies/snowflake/` was made. Learning pages (entry `README.md`, `loop/LOOP_GUIDE.md`, `study/`, `problems/`, `loop/rounds/`, `debrief/`) stay in the vault.

- `catalog/`: `CATALOG.md` (problem table), `RANK.md` / `PARETO.md` (28 rule, cut line), `raw/` (one file per source, GitHub first), `discovery/` (forum mirror + harvest logs).
- `raw/`: earlier company/process/Chakra/email research notes (separate from `catalog/raw/`).
- `reports/`: `COVERAGE.md`, `TEST_SUMMARY.md`. `skills_matrix.md`: skill / JD / problem map.
- `CHECKPOINT.md`, `LEDGER.md`, `CONVENTIONS.md`, `tasks/plan.md`: build state and rules.
- `tools/`: pareto, coverage, summary, contents (writes the vault's `CONTENTS.md`), harvest, mirror, refresh_check, verify_suites, build_report_html, `tree/` (`check_tree.py` + `interview-loop.yaml`), `build_ai_screen_bank.py`, `lint.sh`. Their relative paths still assume the old in-kit layout; adjust before running.
- The vault keeps `tools/progress.py` and `tools/pytest_progress.py` because `drill.py` and `loop/mock.py` import them.
