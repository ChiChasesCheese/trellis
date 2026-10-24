# TikTok / ByteDance — checkpoint

## State (2026-10-24)

- LeetCode list: 362 problems in `index.json` (A 161 / B 201; incl. 50 reported originals and 34 TikTok variants from catalog/additions.json; US TikTok + ByteDance lists unioned with China-side CodeTop 字节跳动). Skeletons
  `tiktok-lc` (deck LeetCode Tops::24, whole answers + Python toolkit + patterns) and `tiktok-lc-drill` (::25, split
  cards). Statements in gitignored `sources/local/tiktok-lc/`; four 补充题 have none (restated from knowledge).
- Cards done and committed: pilot LC 3, A1 (23), A2 (23). Split cards are filed into the drill deck by the orchestrator
  (`tools/file_split.py`, or by group as in the A1/A2 commits).
- Running: P (python + patterns), research EN, research CN.

## Queue (paused 2026-10-24 ~15:00 at the usage limit; resume here)

Done and committed: research (EN, CN), catalog + additions, kit pages (README, LOOP_GUIDE, brief, behavioural, 8 system
designs, fundamentals), Obsidian problem index, Python toolkit + patterns, card groups A1, A2, P, L1–L4, L6, L10, L11,
and the completed problems of L5 and L7 (36). 269 of 362 problems have cards. Both decks pushed to Anki at that state
(deck 24: 518 cards, deck 25: 1131). `pl` (five languages, 1312 cards) pushed.

Remaining (~93 problems):
- L5 and L7: their unfinished leaves (agents died at the usage limit). Relaunch `agents/prompt_L5.md` and `prompt_L7.md`
  — the resume rule skips leaves that already have cards. Two half-written problems (`codetop-supp-2`,
  `longest-common-prefix`) were set aside in `~/.local/state/trellis-backup/tiktok-partial-1792876631/`; just rewrite them.
- Not started: `agents/prompt_L8.md`, `L9`, `L12`.
- Per finished group: `tools/file_group.py <G>` → gate → commit; then `tools/gen_index.py`, sync + anki-push both decks.
- At the very end: if no tiktok card has been reviewed, delete both decks' notes and re-import for heat order.
