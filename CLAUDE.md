# CLAUDE.md — trellis

Skeleton-constrained knowledge base (Obsidian vault + Anki build) **plus** the interview
folder `vault/interviews/`. Vocabulary is in `CONTEXT.md`; the product is in `README.md`.
This file is only what an agent needs to work here without re-deriving it.

## Where things live

| Path | What |
|---|---|
| `trellis/` | the CLI (`uv run trellis --domain <d> validate/build/...`) |
| `skeleton/*.yaml` | one mind map per domain; the only source of truth for what exists |
| `vault/<domain>/` | cards, readings, clippings, map notes per domain |
| `vault/interviews/` | **all** interview material: `core/` (resume, stories, answers, playbooks), `companies/<co>/` (one self-contained kit per company), `_template/company/` |
| `vault/interviews/companies/stripe/` | the full `stripeoa` kit mirrored here (drill.py, loop/mock.py, tools/, problems/, loop/rounds/, catalog/, study/) — this is the reference methodology |
| `vault/interviews/companies/snowflake/` | same shape, built 2026-09 |

Rules that are not derivable from the code:

- **Everything Chi studies lives in this repo's vault and is merged to `main`.** Never write
  interview or study material into `~/Documents/Chi` or any other vault; never copy across vaults.
- `vault/` is an Obsidian vault: `.py` files inside company kits are invisible to Obsidian and
  harmless to `trellis` (it only reads `*.md`). Root `pytest` is scoped to `tests/` via
  `pyproject.toml`; run a kit's suite from inside its folder (`cd vault/interviews/companies/stripe && python3 -m pytest problems -q`).
- `core/resume/resume.tex` is the only resume source. Company folders link to `core/`, never copy it.

## Interview kit methodology (the Stripe way — reuse for every company)

Full procedure, lessons and red flags: `.claude/skills/building-company-interview-kits/SKILL.md`.

0. **GitHub first, always.** Before any web research, search GitHub for what others already
   curated (`gh api -X GET search/repositories -f q="<co> interview"`, `search/code`, company-wise
   LeetCode repos), then distill into `catalog/raw/github_repos.md` with a confidence per source.
   Only then go to forums/aggregators. The coverage denominator must include what GitHub found.
   - LeetCode originals never get a full kit: run `python3 vault/interviews/core/leetcode/lc_company.py <Company>`
     (link + tags + frequency, tiered A/B/C); map to kit ids in `core/leetcode/companies/<co>.kitmap.json`.
1. `catalog/raw/`: one file per source, every fact with URL + date; nothing rewritten.
2. `catalog/CATALOG.md`: one row per problem — aliases, stage, parts, last asked, `#refs`
   (independent sources), confidence (high/medium/low), URLs. Rank by stage × refs × recency;
   the top ~20% of rows must cover ~80% of reported sightings (write the cut line down).
3. `LOOP_GUIDE.md`: per round — format · what is scored · pass line · failure modes · prep actions,
   every claim traceable to raw.
4. Problem sets follow `CONVENTIONS.md` (`problem.md` + `starter_template.py` + `solution.py` +
   `test_*.py` with part/edge/fmt/perf/io markers + `REPORT.md`); non-coding rounds are
   `bank.json` + `questions.md` + `rubric.md` + `stories.md`; system design is
   `prompt.md` + `rubric.md` + `model_answer.md` + `followups.md`.
5. `study/` is Chinese: essentials (transferable), per-round prep, one article per problem.
6. Runners: `drill.py` (OA) and `loop/mock.py` (all other rounds); `tools/summary.py --run`
   regenerates the test summary; `tools/refresh_check.py` re-verifies sources.
7. Reconstructed parts are labelled **(reconstructed)** in `problem.md`; AI content farms
   (lodely, vervecopilot) are never cited; a single fetch failure never condemns a site —
   record which path failed (see `companies/stripe/HANDOFF.md` §2 for the reachability table).

## Orchestration rules for multi-agent work in this repo

- The main session orchestrates; **subagents are `sonnet`, at most 3 in parallel, and never spawn their own agents**.
  There is no settings key for this — it is a rule, apply it by passing `model: "sonnet"`.
- Tasks are atomic: one agent → one directory it owns → one deliverable that is verifiable by
  a command (`pytest`, `check_tree.py`, a row count). No shared files between parallel agents.
- Progress is durable: after every accepted task append a row to the company's `LEDGER.md`,
  update `CHECKPOINT.md` (state + next action), and **commit + push the worktree branch**.
  A new session must be able to resume from `CHECKPOINT.md` alone.
- Usage limits: user settings set `fallbackModel: ["claude-opus-5"]`; if the session dies,
  resume from the ledger, do not redo accepted tasks.
- Git in a worktree: the rtk hook rewrites `git` and the worktree guard then refuses it —
  call `/usr/bin/git ...` in plain, single commands. Merge PRs only when Chi says so.
- Never accept a subagent's "done": re-run `tools/verify_suites.py` (reference green **and** empty
  starter red) and `check_tree.py --strict` yourself. A 429 usage-limit death leaves partial files —
  salvage and finish them, don't respawn from scratch.

## Gotchas

- The worktree guard rejects heredocs, `for` loops and `$var` in commands: write the script to
  `$CLAUDE_JOB_DIR/tmp/*.py` with Write, then run `python3 <script>`.
- Plain `python3` has no pytest: `uv run --project <worktree> --with pytest python -m pytest ...`; `git checkout uv.lock` if uv touches it.
- macOS `sed -i ''`; relative links from `loop/rounds/<round>/<id>/` to the kit root are `../../../`.
- Counts in prose (cut line, coverage, "N problems") come from a script (`tools/pareto.py`,
  `tools/coverage.py`, `summary.py`), never from memory — hand counts were wrong twice.
- Paywalled aggregators (trueinterview) still expose intro + part outline via WebFetch: enough to
  rebuild the problem, labelled **(reconstructed)**.
- `uv run trellis --all anki-push` needs desktop Anki running (AnkiConnect on :8765). Company kits are
  not trellis domains: syncing adds no cards for them.

## Commands

```bash
uv run trellis --all validate                  # 0 errors is the bar
uv run --with pytest python -m pytest -q       # trellis tests (tests/ only)
cd vault/interviews/companies/stripe && python3 -m pytest problems -q   # a kit's suite
python3 tools/verify_suites.py . "problems/q1*"   # kit acceptance gate (run inside the kit)
python3 tools/coverage.py                          # sighting-weighted coverage → reports/COVERAGE.md
python3 vault/interviews/core/leetcode/lc_company.py Snowflake   # LeetCode company-tag list
```
