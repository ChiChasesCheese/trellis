---
name: building-company-interview-kits
description: Use when preparing for a specific company's interview loop (OA, phone screen, onsite, system design, behavioral), doing company due diligence, collecting leaked or reported interview questions, or claiming coverage of a company's question pool in the trellis vault.
---

# Building Company Interview Kits

## Overview

A company has two homes (CLAUDE.md, "Learning area vs research area"; Amazon and Headlands are the models).

- **Learning area, the kit**: `vault/interviews/companies/<co>/`. Only what Chi reads or practises: `README.md` (the one
  entry point), `LOOP_GUIDE.md`, LP/behavioural pages, company-only rounds, and practice code (problem dirs with
  `problem.md`, starter, solution, tests; the runner the README names, `conftest.py`, `pytest.ini`). No sources, catalogs,
  CHECKPOINT/LEDGER, authoring tools or agent files in here.
- **Research area**: `research/companies/<co>/`. Sources and evidence (`catalog/raw/`, `CATALOG.md`), `CHECKPOINT.md`,
  `LEDGER.md`, `PROVENANCE.md`, `CONVENTIONS.md`, agent task files, and the authoring tools (`pareto`, `coverage`,
  `verify_suites`, `summary`, `contents`, `check_tree`, `harvest`, `mirror`, `refresh_check`). Start it with a `README.md`
  of 5–10 lines saying what is there and where the learning pages are.
- **General topics** (system design, LLD, coding patterns, language courses) are not kit-only: they go to
  `vault/interviews/core/<topic>/<co>/` (for example `core/system-design/amazon/`, `core/cpp/headlands/`) or a domain
  branch (LLD deck 10 is the `amazon` branch). The kit links to them.

General coding-round skills live in the `code-core` domain (`vault/interviews/rounds/code-core/`): give the company a
`transfer.<co>` leaf and a `core: [leaf, …]` list per coding round in the kit's loop tree, so the
kit links to the general leaves instead of rewriting them.

Every page under `vault/` is a learning page and follows `proposals/WRITING_RULES.md`: no provenance or process words,
no reconstruction labels, no agent or gate talk, `（low priority）` on problems not asked in the last month, and diagrams
that survive a phone (rule 12: text diagrams at most 40 display columns, no CJK on drawing lines; prefer a table, a list,
or a small mermaid). Check pages with `python3 scripts/plain_style.py <page.md>` (LP pages with `--outline`) and
`python3 scripts/phone_diagrams.py <page.md | dir>`; dead links with `python3 scripts/check_wikilinks.py`.

**Core principle: distill what others already curated before researching yourself, and never
state a number you did not compute.**

## Procedure

0. **GitHub first.** Search repositories and code (`gh api -X GET search/repositories -f q="<co> interview"`,
   `"<co> oa"`, `company wise leetcode`; `search/code` for `"<co>" "phone screen"`). Fetch every
   company-specific file. Write `research/companies/<co>/catalog/raw/github_repos.md`: source, stars, last push,
   confidence, how used. Run `vault/interviews/core/leetcode/lc_company.py <Co>` (from the repo root) for LeetCode originals.
1. **Web sources** (forums, 1p3a, Blind, aggregators) → `research/companies/<co>/catalog/raw/<topic>.md`, URL + date per fact, one file per source (`emails`, `official`,
   `forums_en`, `forums_cn`, `aggregators`). Confidence: high = first-hand post or official page, medium = aggregator whose
   details match a first-hand one, low = SEO or AI-rewritten site (trust the problem type, not the numbers).
2. **`research/companies/<co>/catalog/CATALOG.md`**: one row per problem family; `#refs` = independent sources; confidence
   high (first-hand) / medium (consistent aggregator) / low (SEO). `tools/pareto.py` ranks and
   writes the cut line (put it in `CATALOG.md`).
3. **Build** above the cut line first, in the kit: coding = `problem.md` + `starter_template.py` +
   `solution.py` + `test_*.py` (the per-set `REPORT.md` is process, so it goes to `research/companies/<co>/reports/`);
   non-coding = bank + rubric + stories; system design = prompt/rubric/model_answer/followups in
   `vault/interviews/core/system-design/<co>/`. LeetCode originals get a list row, not a kit.
4. **Accept** each set only after `tools/verify_suites.py` (solution green, empty starter red)
   and `loop/tree/check_tree.py --strict`, both run from the research area, then run the style gates on every learning page
   (`plain_style.py`, `phone_diagrams.py`).
5. **Study layer** in Chinese: essentials, per-round guide, one article per problem, written as rehearsable action items.
6. **Report** `tools/coverage.py` numbers, naming the universe they are measured against. The report lives in
   `research/companies/<co>/`, never in the kit.

## Quick Reference

Paths: the LeetCode tool and the style gates run from the repo root; authoring commands (`tools/`, `check_tree`) run from the research area (`cd research/companies/<co>`) and take the kit path (`../../../vault/interviews/companies/<co>`) where they read or test it; only the practice runners the kit README names (`drill.py`, `loop/mock.py`, a language test runner) run from inside the kit. A new company starts by copying the authoring `tools/` from `research/companies/amazon/` (or `headlands/`) into `research/companies/<co>/tools/`, and `conftest.py` + `pytest.ini` into the kit.

| Artifact | Command |
|---|---|
| LeetCode company-tag list | `python3 vault/interviews/core/leetcode/lc_company.py <Co>` (repo root) |
| Rank + cut line | `python3 tools/pareto.py catalog/RANK.md --table 总表` (research area) |
| Acceptance gate | `uv run --project <repo> --with pytest python tools/verify_suites.py <kit path> "<glob>"` (research area) |
| Coverage | `python3 tools/coverage.py` (research area) |
| Test summary | `python3 tools/summary.py --run` (research area) |
| Book contents (rounds → skills → problems, ranked) | `python3 tools/contents.py` after every tree or RANK change (research area) |
| Page style | `python3 scripts/plain_style.py <page.md>` · `python3 scripts/phone_diagrams.py <dir>` (repo root) |

A LeetCode problem that the company changed (new constraints, extra Parts, a design twist) is not an original: it gets a kit.

## Red Flags — stop

- Opening WebSearch before any `gh api search` call.
- Writing a full solution kit for a LeetCode original.
- "Coverage is ~90%" without a `coverage.py` run, or with a universe that excludes GitHub lists.
- Marking a subagent task accepted from its own report.
- A cut line, count, or percentage typed from memory.
- Filling paywalled or missing parts without recording it in `research/companies/<co>/PROVENANCE.md` (never as a label on a learning page).
- A `raw/`, `catalog/`, `tools/`, CHECKPOINT or LEDGER file created inside `vault/interviews/companies/<co>/`.
- Provenance, confidence, "reconstructed" or agent talk on a learning page, or a wrapped ASCII diagram.

| Rationalization | Reality |
|---|---|
| "Nobody curates this company on GitHub" | The last sweep found a 104-problem LeetCode tag list and an 87-question aggregator mirror. Search takes two minutes. |
| "Web aggregators already cover it" | They missed 26 company-specific problems that one GitHub file listed. |
| "The subagent said tests pass" | Two accepted sets had wrong tests or links. Re-run the gate. |
| "I counted the rows" | Hand counts were wrong twice. Use the script. |

## Common Mistakes

- Denominator drift: adding sources after computing coverage. Recompute after every source.
- Relative links from `loop/rounds/<round>/<id>/` to the kit root need `../../../`.
- Subagents spawning subagents, or more than 3 in parallel: the limit is the orchestrator's job.
- Losing progress on usage limits: append `research/companies/<co>/LEDGER.md`, update `research/companies/<co>/CHECKPOINT.md`, commit + push per task; relaunch the rest on `opus` with a resume rule when sonnet is limited.
