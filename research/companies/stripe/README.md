# Stripe — research area

How the Stripe kit was made. Nothing here is studied; the learning pages are in `vault/interviews/companies/stripe/`.

- `catalog/` — `CATALOG.md` (every problem found online, ranked), `SOURCES.md`, `sources.json`, `raw/` (one file per source, with the mirrored forum posts), `discovery/` (dated sweeps and harvest JSON).
- `loop/` — the same for the rounds after the OA: `CATALOG.md`, `raw/`, `LEDGER.md`, `CHECKPOINT.md`, `tasks/`, `tree/` (round/skill tree `interview-loop.yaml` and the map generator `map/`), `lint.sh`, the Anki exporters in `study/`.
- `reports/` — overall report, review findings, test summary, HTML report.
- `HANDOFF.md`, `CHECKPOINT.md`, `CONVENTIONS.md`, `CLAUDE.md` — where the work stopped, the problem-set rules, the agent rules.
- `skills_matrix.md` — test targets against problems and job-description lines.
- Authoring tools are the shared `trellis kit` commands, run from the repo root: `trellis kit pareto|summary|harvest|mirror|refresh_check|build_report_html|check_tree --co stripe` (they read this folder and write the kit's `problems/` and `loop/rounds/`; `--kit` / `--research` override the two directories). `drill.py` and `loop/mock.py` import the practice runtime from `trellis.kit`.

Learning pages: `vault/interviews/companies/stripe/README.md` (OA drills, `drill.py`), `study/README.md` (Chinese walkthroughs), `loop/README.md` (later rounds, `loop/mock.py`), `loop/LOOP_GUIDE.md`. The trellis deck is `vault/interviews/companies/stripe/deck/`.
