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
  last 30 days (84), the top 3 of every pattern (14), then the highest scores (reports 0.5 / US lists 0.4 / CodeTop 0.1,
  recency-weighted; Chi set US 0.4, CN 0.1). Coverage by tier A: 85.8% of the 485 report sightings (91.0%
  recency-weighted; 96.1% is the most the deck can reach), 78.8% of US + SG sightings, 58.9% of the US crowd-tag mass,
  81.6% of CodeTop mass.
- Problems never leave the deck: `build_list.py` keeps every earlier index entry. `tools/retier_cards.py` moves card
  files and `node:` lines when a tier changes (Anki keeps reviews; anki-push moves the cards between sub-decks).
- 13 new problems with cards (7 LeetCode, 6 TikTok variants). Total 375 problems.
- Card rule: 2-D DP uses the full table; compression only in leaf `python.dp-space-compression` (CARDS.md). 19 problems
  and the DP pattern cards were rewritten.

## Audit re-sweep 2026-07-17..10-28 (2026-10-28, later)

- `catalog/refresh-2026-10-28-audit-{en,cn}.json`: EN 15 missed sightings (1P3A recall of the first collection about 69%),
  CN 133 rows from 105 Nowcoder reports (first collection had about a third; CN sweep stopped early on Chi's time limit,
  07-17..07-31 thin). 15 CN rows (front-end / JS knowledge, SQL, ML) marked out of scope.
- 9 new LeetCode problems (all tier B): 328, 389, 478, 593, 889, 912, 986, 1740, 2816. Total 384.
- Tier A after the audit: 85 seen in 30 days + 15 pattern + score; covers 84.3% of 618 sightings (88.8% weighted;
  95.1% reachable), 81.9% of CodeTop mass, 58.8% of US crowd-tag mass.

## Past-year tier A, order, pace (2026-10-29)

- Tier A = pinned (`catalog/pinned.json`) ∪ everything seen in the past year (reports, CodeTop, US 30d/3m/6m lists)
  ∪ the top 200 by score ∪ 3 per pattern. 83 China-side past-year problems added with cards (one SQL excluded).
  468 problems: A 401 / B 67. Deck 24: 724 cards, deck 25: 1965.
- Card headers carry data via `tools/stamp_headers.py` (re-run after every rebuild).
- Study order: inside a tier, score percentile + 0.2 for Easy / −0.2 for Hard; tier A is the first sub-deck of
  deck 24. Still-new notes were deleted and re-imported so Anki follows the order (122 studied notes kept).
- Anki presets (LeetCode Tops, 24, 25, 26): learning steps 1 h → 6 h, relearning 1 h. Deck 24: 80 new / 500
  reviews a day; deck 25 paused (0 new); deck 26: 10 new.

## Tier A by evidence (2026-10-29, Chi)

Tier A = pinned ∪ asked in a US interview in the past year (counted sighting, or the US company tag's 30d / 3m / 6m
window) ∪ asked at least twice in the past year anywhere ∪ asked at least once in the last three months (reports or
CodeTop). Score only orders problems inside a tier. A 286 / B 188; US sightings covered about 93%.

## General-core deck (2026-10-30)

`tools/gen_core.py` builds domain `tiktok-core` (deck `LeetCode Tops::27 通用核心`): tier-A problems that are also in
Chi's Amazon decks or on Blind 75 / NeetCode 150 / LeetCode Hot 100 / Top Interview 150 (`catalog/other_lists.json`),
146 copies of the whole-answer cards with their own schedule, sub-decks P1..P5. Re-run after any change to deck 24.

## US first (2026-10-30)

Tier A = pinned ∪ US sighting in the past year ∪ US company tag 30d / 3m / 6m window ∪ China-side reported at least twice in the past year. A 196 / B 278, split P1..P5 by cumulative frequency share.
