# TikTok / ByteDance — checkpoint

## State (2026-10-24)

- LeetCode list: 362 problems in `index.json` (A 161 / B 201; incl. 50 reported originals and 34 TikTok variants from catalog/additions.json; US TikTok + ByteDance lists unioned with China-side CodeTop 字节跳动). Skeletons
  `tiktok-lc` (deck LeetCode Tops::24, whole answers + Python toolkit + patterns) and `tiktok-lc-drill` (::25, split
  cards). Statements in gitignored `sources/local/tiktok-lc/`; four 补充题 have none (restated from knowledge).
- Cards done and committed: pilot LC 3, A1 (23), A2 (23). Split cards are filed into the drill deck by the orchestrator
  (`tools/file_split.py`, or by group as in the A1/A2 commits).
- Running: P (python + patterns), research EN, research CN.

## Done (2026-10-24 ~19:00)

All 362 problems have a whole-answer card (deck 24, plus Python toolkit and patterns: 611 cards) and split cards (deck 25:
1522 cards). Deck 25 was re-imported fresh (no reviews) so it sits in heat order; deck 24 had reviews, so the last ~108
new cards sit after the earlier ones. Kit pages, system design, fundamentals and the Obsidian index are complete.

Possible next steps (not requested): `/catalog refresh` when new reports appear (re-run `tools/build_list.py`,
`gen_skeleton.py`, new card group for new leaves); readings for the decks are deliberately absent (cards-first).

## Re-tier and refresh (2026-10-28)

- Refresh 2026-10-17..28: `catalog/refresh-2026-10-28-{en,cn}.json` (26 sightings; 5 ML / JavaScript-knowledge rows
  marked out of scope). CodeTop snapshot `catalog/codetop.json`. US lists unchanged (repo last commit 2026-10-21).
- Tier A is now chosen by `tools/select_tiers.py` (called by `build_list.py`): 200 problems = everything seen in the
  last 30 days (84), the top 3 of every pattern (15), then the highest scores (reports 0.5 / CodeTop 0.3 / US 0.2,
  recency-weighted). Coverage by tier A: 86.4% of the 485 report sightings (91.6% recency-weighted; 96.1% is the most
  the deck can reach), 84.9% of CodeTop mass, 54.2% of the US crowd-tag mass, 78% of US + SG sightings.
- Problems never leave the deck: `build_list.py` keeps every earlier index entry. `tools/retier_cards.py` moves card
  files and `node:` lines when a tier changes (Anki keeps reviews; anki-push moves the cards between sub-decks).
- 13 new problems with cards (7 LeetCode, 6 TikTok variants). Total 375 problems.
- Card rule: 2-D DP uses the full table; compression only in leaf `python.dp-space-compression` (CARDS.md). 19 problems
  and the DP pattern cards were rewritten.
