# Checks reference

Every checker is a plain script; all exit **0** when clean and **1** when anything is reported unless noted. Run from the
repo root. Use `uv run python` where the script imports `trellis`, plain `python3` otherwise.

| Script | Checks | Run | Notes |
|---|---|---|---|
| `uv run trellis --all validate` | skeletons (order vs `requires`), cards, readings, drills | see left | prints errors; 0 errors is the bar |
| `pytest` (`tests/`) | trellis package | `uv run --with pytest python -m pytest -q` | kit suites run from inside the kit |
| `scripts/check_wikilinks.py` | dead `[[wikilinks]]` (by note name, path suffix, frontmatter `aliases`) and relative `(x.md)` links; ignores code and `*/clippings/*` | `python3 -B scripts/check_wikilinks.py [vault-subpath ...] \| tail -1` | last line `N dead link(s)`; the bar is 0 |
| `scripts/plain_style.py` | machine half of `proposals/WRITING_RULES.md`: provenance and process words, third-person narration, mermaid size limits | `python3 scripts/plain_style.py [--outline] <file.md \| cards.json> ...` | `--outline` for LP pages (bullets only); also imported as a library by the gates below |
| `scripts/phone_diagrams.py` | text diagrams in fenced non-code blocks: <= 40 display columns (CJK = 2), no CJK on a drawing line (rule 12) | `python3 scripts/phone_diagrams.py <file.md \| dir> ...` | exit 1 if any block reported |
| `scripts/check_sd.py` | reported system-design write-ups `vault/interviews/core/system-design/sdNN-*.md`: sections in order, 3+ mermaid diagrams, 9,000+ chars, no provenance, links resolve | `python3 scripts/check_sd.py [sd01 ...]` | prefix filter |
| `scripts/check_ood.py` | Amazon OOD write-ups `core/low-level-design/amazon/oodNN-*.md`: sections, `## 来源` last, 3,000-7,500 chars, runnable <= 170-line Python skeleton, classDiagram | `python3 scripts/check_ood.py [ood03 ...]` | |
| `scripts/check_design_problems.py` | system-design problem leaves: solution article, drill, 6+ cards with translations and steps, 2+ readings | `uv run python scripts/check_design_problems.py <leaf ...> \| --all` | 49/49 is the bar |
| `scripts/check_lld_problems.py` | LLD problem leaves: solution passes its tests, empty starter fails, standard-library Python, Chinese article, class diagram, 6+ cards, drill | `uv run python scripts/check_lld_problems.py <leaf ...> \| --all [--branch amazon]` | |
| `scripts/check_lld_concepts.py` | LLD concept layer outside `problems`: 4-8 Chinese-native cards per leaf, unique `step`, no Java, python blocks parse | `uv run python scripts/check_lld_concepts.py <branch ...> \| --all` | |
| `scripts/lld_embed_code.py` | article code blocks (`%% code:begin file [Symbol] %%`) equal the tested file | `uv run python scripts/lld_embed_code.py [--check] <slug> ...` | without `--check` it rewrites; `--check` exits 1 if stale |
| `scripts/changed_learning_pages.py` | lists the changed vault pages (not `*/clippings/*`, not the generated `Brief.md`, `Codebases/`, `Corpora/`), split into LP-style (`*/lp/**`, `*/behavioral/**`, `core/stories/**`) and the rest; `--check` runs `plain_style.py` (`--outline` on LP pages) and `phone_diagrams.py` on them only | `python3 scripts/changed_learning_pages.py [--base REF] [--check] [--lp \| --rest] [--files F ...]` | `--base REF` diffs `REF...HEAD`; no `--base` = working tree vs HEAD. Old style debt in pages you did not touch never fails |
| `scripts/check_mermaid.py` | every ```` ```mermaid ```` block on the changed `.md` pages renders with `@mermaid-js/mermaid-cli` (pinned in the script, `$MERMAID_CLI_VERSION` overrides) | `python3 scripts/check_mermaid.py [--base REF] [--list] [page.md ...]` | needs Node + network (headless Chrome) |
| `scripts/kit_suites.py` | every interview kit's practice suites in one table; exits 1 on any unexpected result | `python3 scripts/kit_suites.py [--co <co> ...] [--list] [--skip-missing]` | see "Kit suites" below |
| `scripts/check_links.py` | every reading / drill URL answers (network) | `python3 scripts/check_links.py` | manual, not in CI |

## Helpers that are not gates

`review_design_problem.py <slug>` (what to re-derive before accepting a problem), `design_problem_survey.py [--names]
[--domain low-level-design]` (problems x sources), `demo_traces.py [--keep DIR]` (synthetic review history, writes nothing
to `traces/`), `amazon_push_cards.py [--dry-run] [--set recent|patterns]`, `obsidian_setup.sh [vault]`,
`sync_laptop.sh [--no-anki]`.

## Kit suites

A company kit carries its own `pytest.ini`; run it inside the kit: `cd vault/interviews/companies/<co> && python3 -m pytest
problems -q`. Root `pytest` is scoped to `tests/`. `scripts/kit_suites.py` runs them all the way CI does (pytest through
`uv run --project <repo> --with pytest`, `UV_FROZEN=1` so uv.lock stays untouched); `--list` prints the commands.

| Kit | Suites (`--co <co>`) | Expected |
|---|---|---|
| amazon | `core/coding/amazon/run_all.py` (solutions + lecture code blocks) | `ALL PASS` |
| headlands | `tools/jtest.py verify "loop/rounds/*/*"`, `tools/cpptest.py verify "loop/rounds/*/*"`, `mock_maven/java`: `mvn -q test` | reference green, starter red; needs JDK 21, Maven, clang++/g++ (`$CXX` overrides; cpptest otherwise picks clang++, then g++) |
| stripe | `problems`; `loop` without `loop/study` and `04_bug_squash`; `loop/study` + `04_bug_squash` | the first two green; the last is red on purpose, exactly **82 failed** (72 learner exercises + 10 bug-squash starters), no errors |
| snowflake | `pytest problems loop` | green |
| millennium | `pytest` (testpaths `loop/rounds`) | green (1 skipped) |
| airbnb, roblox | `unittest discover` per problem / per game | green |
| abnormal | `trellis kit verify_suites --co abnormal` on `loop/rounds/01_ai_screen/cb*` and `03_code_review/cr*` (acceptance green on the solution, every `core` test red on the starter, own tests green); pytest on `02_incident_sd`, `06_legacy_coding` | `ALL ACCEPTED`, green |

If a count changes on purpose (a new exercise under `stripe/loop/study`), change `expect_failed` in `scripts/kit_suites.py`.
Whole run: about 4 minutes (headlands ~2 of them).

## CI and local hooks

`.github/workflows/ci.yml` (all actions pinned to commit SHAs; `permissions: contents: read`; one run per ref, newer cancels older):

| Job | Runs | When |
|---|---|---|
| `check` | `trellis --all validate`, `pytest -q`, `trellis --all build`, uploads the decks | always |
| `changes` | `dorny/paths-filter`: which kits, vault pages, `.md` files changed | always |
| `wikilinks` | `python3 -B scripts/check_wikilinks.py` | always |
| `learning-pages` | `changed_learning_pages.py --base <PR base or previous tip> --check` (`fetch-depth: 0`) | `vault/**/*.md` changed |
| `kits` | matrix over the kits whose folder changed: `kit_suites.py --co <co>` (headlands installs JDK 21 and sets `CXX`) | a kit folder, `trellis/**`, `pyproject.toml`, `uv.lock`, `kit_suites.py` or `ci.yml` changed |
| `mermaid` | `check_mermaid.py --base ...` | any `.md` changed |

Bump a pinned action: `gh api repos/<owner>/<repo>/releases/latest --jq .tag_name`, then `gh api repos/<owner>/<repo>/git/ref/tags/<tag> --jq .object.sha`
(an annotated tag gives a tag object: resolve it once more with `git/tags/<sha>`), and update the SHA and the `# vX.Y.Z` comment.

Local equivalents: `just test | kits [co] | style [base] | mermaid [base] | all` (`justfile`).

**pre-commit (opt-in, not installed by any script).** `.pre-commit-config.yaml` has ruff (lint only; the rule set is
`[tool.ruff.lint]` in `pyproject.toml`, scope `trellis/ scripts/ tests/`), gitleaks on the staged diff, and two local hooks:
the two style checkers on staged vault pages and `check_wikilinks.py`. To turn it on in your clone:

```bash
uv tool install pre-commit
pre-commit install
pre-commit run --all-files     # optional; stage-only is the normal mode. Legacy pages will report their old debt
```
