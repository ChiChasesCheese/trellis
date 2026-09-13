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

1. `catalog/raw/` first: one file per source, every fact with URL + date; nothing rewritten.
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

- The main session (Fable 5.1) orchestrates; **subagents are `sonnet`, at most 3 in parallel**.
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

## Commands

```bash
uv run trellis --all validate                  # 0 errors is the bar
uv run --with pytest python -m pytest -q       # trellis tests (tests/ only)
cd vault/interviews/companies/stripe && python3 -m pytest problems -q   # a kit's suite
```
