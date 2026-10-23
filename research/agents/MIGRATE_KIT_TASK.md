# Task — split an old company kit into learning area + research area

Repo `/Users/chiserver/sessions/trellis`, branch `main` (never switch branches, never commit, never spawn agents).
Read `CLAUDE.md` (section "Learning area vs research area"), `proposals/WRITING_RULES.md`, and look at the two kits that
already follow it: `vault/interviews/companies/amazon/` + `research/companies/amazon/`, and
`vault/interviews/companies/headlands/` + `research/companies/headlands/`.

For each kit you own (`vault/interviews/companies/<co>/`), use `git mv` (never plain mv/cp) to move into
`research/companies/<co>/`:
- sources and evidence: `catalog/`, any `raw/`, `discovery/`, harvest JSON, `reports/`, coverage/summary outputs;
- process and agent files: `CHECKPOINT.md`, `LEDGER.md`, `HANDOFF.md`, `CONVENTIONS.md`, nested `CLAUDE.md`/`AGENTS.md`,
  `tasks/`, `AGENT*.md`, `*_TASK.md`, `BUILD.md`, `PROVENANCE.md`;
- authoring tools: `tools/` scripts that build/rank/harvest/report (pareto, progress, summary, harvest, mirror,
  refresh_check, build_report_html, coverage, contents, articles_readme, verify_suites, pytest_progress), generated
  `bank.json` + their builders, `Makefile` targets that only serve authoring, `loop/tree/check_tree.py`.

Keep in the kit everything Chi studies or practises with: README/guides/LP/study pages, problem dirs (problem.md,
starter, solution, tests, cases), and the minimum runtime needed to run the practice tests (`conftest.py`, `pytest.ini`,
`drill.py`, `loop/mock.py`, a runner the README tells Chi to use). If a kept runner imports a moved tool, keep that tool.

Then:
1. **One entry point**: the kit's entry is `README.md` (rename `00-README.md` → `README.md`; keep `CONTENTS.md` as a
   plain index page if it is useful to a learner, otherwise move it to research). Fix every relative link that broke
   (`python3 /tmp/mdlinks.py <kit>` style check: write your own small checker for `](relative/path)` links).
2. **Tests unchanged**: run the kit's practice suites before and after the move with
   `uv run --project /Users/chiserver/sessions/trellis --with pytest python -m pytest -q <kit or problems dir>`
   (`git checkout uv.lock` if uv touches it) — same pass/fail counts before and after. Report both.
3. Write `research/companies/<co>/README.md`: 5–10 lines on what is here and where the learning pages are.
4. Do **not** edit learning-page prose (style debt is a separate task) beyond fixing links.

Final reply ≤ 8 lines per kit: moved (files count), kept, test counts before/after, links fixed, anything unsure.
