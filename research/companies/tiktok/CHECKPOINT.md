# TikTok / ByteDance — checkpoint

## State (2026-10-24)

- LeetCode list: 362 problems in `index.json` (A 161 / B 201; incl. 50 reported originals and 34 TikTok variants from catalog/additions.json; US TikTok + ByteDance lists unioned with China-side CodeTop 字节跳动). Skeletons
  `tiktok-lc` (deck LeetCode Tops::24, whole answers + Python toolkit + patterns) and `tiktok-lc-drill` (::25, split
  cards). Statements in gitignored `sources/local/tiktok-lc/`; four 补充题 have none (restated from knowledge).
- Cards done and committed: pilot LC 3, A1 (23), A2 (23). Split cards are filed into the drill deck by the orchestrator
  (`tools/file_split.py`, or by group as in the A1/A2 commits).
- Running: P (python + patterns), research EN, research CN.

## Queue (paused 2026-10-24 ~14:00 to save usage; resume here)

Done and committed: research (EN, CN), catalog + additions, kit pages (README, LOOP_GUIDE, brief, behavioural, 8 system
designs, fundamentals), Python toolkit + patterns, card groups A1, A2, P, L1, L2, L3, L4, L10, L11. Both decks pushed to
Anki after L3. `pl` (five languages, 1312 cards) pushed.

Running when paused: L5, L6, L7 — let them finish, then for each: `tools/file_group.py <G>` → gate → commit; then
`tools/gen_index.py`, sync + anki-push `tiktok-lc` and `tiktok-lc-drill`, commit maps.

Not started: `agents/prompt_L8.md`, `L9`, `L12` (~80 problems). Launch ≤ 3 at a time, sonnet. Card agents write split
cards straight into `tiktok-drill/cards/<branch>/`.

At the very end: if no tiktok card has been reviewed in Anki, delete both decks' notes and re-import so every card sits
in heat order (AnkiConnect cannot reposition new cards).
