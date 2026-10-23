# Snowflake kit — research area

How the kit in `vault/interviews/companies/snowflake/` was made. Learning pages (entry `README.md`, `loop/LOOP_GUIDE.md`, `study/`, `problems/`, `loop/rounds/`, `debrief/`) stay in the vault.

- `catalog/`: `CATALOG.md` (problem table), `RANK.md` / `PARETO.md` (28 rule, cut line), `raw/` (one file per source, GitHub first), `discovery/` (forum mirror + harvest logs).
- `raw/`: earlier company/process/Chakra/email research notes (separate from `catalog/raw/`).
- `reports/`: `COVERAGE.md`, `TEST_SUMMARY.md`. `skills_matrix.md`: skill / JD / problem map.
- `CHECKPOINT.md`, `LEDGER.md`, `CONVENTIONS.md`, `tasks/plan.md`: build state and rules.
- `tree/interview-loop.yaml`: the round/skill/problem tree. `tools/`: `build_ai_screen_bank.py` and `lint.sh` (Snowflake-only). The other authoring tools are the shared `trellis kit` commands, run from the repo root: `trellis kit pareto|coverage|summary|contents|harvest|mirror|refresh_check|verify_suites|check_tree --co snowflake`.
- `drill.py` and `loop/mock.py` import the practice runtime from `trellis.kit`; run them with `uv run --project <repo root> python drill.py …`.
