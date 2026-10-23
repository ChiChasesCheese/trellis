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
| `scripts/check_links.py` | every reading / drill URL answers (network) | `python3 scripts/check_links.py` | manual, not in CI |

## Helpers that are not gates

`review_design_problem.py <slug>` (what to re-derive before accepting a problem), `design_problem_survey.py [--names]
[--domain low-level-design]` (problems x sources), `demo_traces.py [--keep DIR]` (synthetic review history, writes nothing
to `traces/`), `amazon_push_cards.py [--dry-run] [--set recent|patterns]`, `obsidian_setup.sh [vault]`,
`sync_laptop.sh [--no-anki]`.

## Kit suites

A company kit carries its own `pytest.ini`; run it inside the kit: `cd vault/interviews/companies/<co> && python3 -m pytest
problems -q`. Root `pytest` is scoped to `tests/`.
