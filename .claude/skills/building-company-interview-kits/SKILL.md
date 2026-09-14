---
name: building-company-interview-kits
description: Use when preparing for a specific company's interview loop (OA, phone screen, onsite, system design, behavioral), doing company due diligence, collecting leaked or reported interview questions, or claiming coverage of a company's question pool in the trellis vault.
---

# Building Company Interview Kits

## Overview

A kit is a self-contained, testable, 80/20-ranked book for one company under
`vault/interviews/companies/<co>/`, same shape as `companies/stripe/`.
**Core principle: distill what others already curated before researching yourself, and never
state a number you did not compute.**

## Procedure

0. **GitHub first.** Search repositories and code (`gh api -X GET search/repositories -f q="<co> interview"`,
   `"<co> oa"`, `company wise leetcode`; `search/code` for `"<co>" "phone screen"`). Fetch every
   company-specific file. Write `catalog/raw/github_repos.md`: source, stars, last push,
   confidence, how used. Run `core/leetcode/lc_company.py <Co>` for LeetCode originals.
1. **Web sources** (forums, 1p3a, Blind, aggregators) → `catalog/raw/<topic>.md`, URL + date per fact.
2. **CATALOG.md**: one row per problem family; `#refs` = independent sources; confidence
   high (first-hand) / medium (consistent aggregator) / low (SEO). `tools/pareto.py` ranks and
   writes the cut line.
3. **Build** above the cut line first: coding = `problem.md` + `starter_template.py` +
   `solution.py` + `test_*.py` + `REPORT.md`; SD = prompt/rubric/model_answer/followups;
   non-coding = bank + rubric + stories. LeetCode originals get a list row, not a kit.
4. **Accept** each set only after `tools/verify_suites.py` (solution green, empty starter red)
   and `loop/tree/check_tree.py --strict`.
5. **Study layer** in Chinese: essentials, per-round guide, one article per problem.
6. **Report** `tools/coverage.py` numbers, naming the universe they are measured against.

## Quick Reference

| Artifact | Tool |
|---|---|
| LeetCode company-tag list | `python3 core/leetcode/lc_company.py <Co>` |
| Rank + cut line | `tools/pareto.py` |
| Acceptance gate | `tools/verify_suites.py . "<glob>"` |
| Coverage | `tools/coverage.py` |
| Test summary | `tools/summary.py --run` |

## Red Flags — stop

- Opening WebSearch before any `gh api search` call.
- Writing a full solution kit for a LeetCode original.
- "Coverage is ~90%" without a `coverage.py` run, or with a universe that excludes GitHub lists.
- Marking a subagent task accepted from its own report.
- A cut line, count, or percentage typed from memory.
- Filling paywalled or missing parts without the **(reconstructed)** label.

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
- Losing progress on usage limits: append `LEDGER.md`, update `CHECKPOINT.md`, commit + push per task.
