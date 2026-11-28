# Task: migrate the old DDIA `system-design` domain into 系统设计, then retire it

Chi (2026-11-28): move what the old English domain still adds into today's 系统设计, in today's format and in Chinese;
add any missing leaves; then the old domain goes. No sample round: do it all.

Read first: `AGENTS.md` (deck rules: remove filler, self-contained, English terms in parentheses, Chinese prose;
diagrams), `proposals/WRITING_RULES.md`, `CONTEXT.md`, `sources/local/audit/ddia-map.md` and `ddia-map.json` (the map
you work from: per old card a verdict covered/partial/unique and a target node; 43 proposed new leaves; readings,
drills, cases, solution articles with target nodes), `research/sysdesign/gen.py` (builds the local
`skeleton/sysdesign.yaml`; find how the existing `more.*` and `*.more` 补充 nodes were added — an earlier migration of
the best old cards — and follow that precedent for nodes and for where cards live), five `more.*` cards and five
`vault/domains/hello-interview/cards/premium/sd/` cards (the format to copy: bold title line `**主题 · 子题**｜类别`,
question, structured answer).

## Do

1. **Cards.** For every old card rated `partial` or `unique`: write the mechanism it adds as a new card in today's
   format, in Chinese, on its target node (or a new leaf). Merge near-duplicates; skip what an existing card already
   says (re-check the three verdicts the map's author was least sure about). Never edit an existing card. Never copy
   the English across: write the card for a Chinese reader from the mechanism. Card ids follow the precedent of the
   `more.*` cards. Card by card, not by script.
2. **Leaves.** Add the new leaves through `gen.py`'s mechanism (not by hand-editing the generated skeleton), regenerate
   `skeleton/sysdesign.yaml`, then `uv run python scripts/atlas_project.py sysdesign`.
3. **Readings, drills, cases, solution articles.** Keep the files; point each one's nodes at its sysdesign target from
   the map. Decide where they live so `trellis --domain sysdesign validate` and CI's `trellis --all validate` both
   load them (the merged view loads `include:` folders' cards and readings; check what it does with drills and cases,
   and extend gen.py's include list or move files as needed). Clippings stay local (gitignored).
4. **Retire the old domain.** Remove `skeleton/system-design.yaml` and the old cards (`git rm`; history keeps them).
   Write `research/domains/system-design/MIGRATION.md`: per old card id, `covered by <card id>` or `migrated to <new
   card id>` or `dropped: <reason>`. Fix every link that pointed at old cards or the old skeleton (wikilinks, docs,
   scripts, `scripts/check_design_problems.py` and the design-problem bank tooling if they read the old domain).
5. **Checks.** `uv run trellis --all validate` 0 errors; `uv run trellis --domain sysdesign validate` 0 errors;
   `python3 -B scripts/check_wikilinks.py` no new dead links (7 exist today); `uv run --with pytest python -m pytest -q`
   green; `python3 scripts/plain_style.py` on the new cards; `uv run trellis export --check` runs.

Resume rule: keep `research/domains/system-design/MIGRATION.md` current as you go; on restart read it and continue
with the first old card that has no line. Do not touch Anki, do not commit or push, do not spawn agents. Another agent
is retiring LeetCode sources (vault/interviews/rounds/leetcode etc.); do not touch those.

Report: cards written (count, per branch), leaves added, readings/drills/cases moved, links fixed, checks output, and
the five new cards you are least sure about (ids).
