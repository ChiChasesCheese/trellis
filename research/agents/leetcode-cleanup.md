# Task: one LeetCode source — the 0x3F tree

Chi (2026-11-28): LeetCode lives in one place, the 0x3F knowledge tree (`skeleton/leetcode-tree.yaml`,
`vault/interviews/core/leetcode/tree/`, one card `lct-<slug>` per problem, lists and companies are tags). Every other
LeetCode source goes. A problem that only a company (TikTok, Amazon …) asked and that the tree lacks is written as a
tree-format card and filed into the tree, tagged with its company; the old company-format cards are then deleted.

Read first: `AGENTS.md`, `docs/explanation/study-system.md` (One card per problem), `research/leetcode-unify/`
(rules), `scripts/lc_tree.py`, `scripts/lc_tags.py`, five `lct-*` cards in the tree (the format to copy), and
`sources/local/audit/card-sources.md` finding #3.

## Sources to retire (none of these is in Anki, except tiktok-lc's 256)

`leetcode` (interviews/rounds/leetcode, 1,054 files), `leetcode-tops` (375), `tiktok-lc-drill` (2,000),
`tiktok-core` (110), `tiktok-lc` (841; 256 are in Anki under `Under the Hood::02 解题模式与 Python 技巧（TikTok）`),
`leetcode-mustread` (19, local). Keep `leetcode-daily` (a daily task writes it; check it follows the tree format and say
so). Keep `vault/interviews/core/leetcode/problems/` (problem bodies the tree uses).

## Steps

1. Inventory: for every problem in the retiring sources, its LeetCode number/slug (or "not a LeetCode problem"), and
   whether the tree already has `lct-<slug>`. Write `sources/local/audit/leetcode-retire.md` (+ `.json`): counts per
   source; problems missing from the tree; company tags each problem carries.
2. Problems missing from the tree: write a tree-format card for each (copy the structure of existing `lct-*` cards;
   Chinese; English terms in parentheses), hang it on the right tree leaf the way `lc_tree.py` / `expand.json` does,
   tag the company with `scripts/lc_tags.py` conventions. Company variants that are not LeetCode problems (e.g. "LRU
   with TTL") become tree cards only if they teach a pattern the tree covers; otherwise list them as dropped.
3. Links: find every wikilink or path in tracked files (vault, docs, scripts, company kits, `kitmap.json`) that points
   into a retiring source; repoint it to the tree card, or list it if there is no equivalent.
4. Delete the retiring sources from the vault and their skeletons (`git rm`; history keeps them). Remove them from
   `atlas.yaml` if present, from any script config that names them, and from `docs/`. `trellis --all validate` 0 errors,
   `python3 -B scripts/check_wikilinks.py` no new dead links (7 exist today), pytest green.
5. Anki: list the note ids of the 256 tiktok-lc notes and, for each, the tree card that replaces it (or none) in
   `sources/local/audit/leetcode-retire.json`. Do NOT delete or modify anything in Anki; the orchestrator does that.

Do not commit or push. Do not spawn agents. Report: counts, the new tree cards written (ids), links repointed, links
left dangling, and the three decisions you are least sure about. Resume rule: read the audit file first and continue.
