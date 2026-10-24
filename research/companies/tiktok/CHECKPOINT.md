# TikTok / ByteDance — checkpoint

## State (2026-10-24)

- LeetCode list: 362 problems in `index.json` (A 161 / B 201; incl. 50 reported originals and 34 TikTok variants from catalog/additions.json; US TikTok + ByteDance lists unioned with China-side CodeTop 字节跳动). Skeletons
  `tiktok-lc` (deck LeetCode Tops::24, whole answers + Python toolkit + patterns) and `tiktok-lc-drill` (::25, split
  cards). Statements in gitignored `sources/local/tiktok-lc/`; four 补充题 have none (restated from knowledge).
- Cards done and committed: pilot LC 3, A1 (23), A2 (23). Split cards are filed into the drill deck by the orchestrator
  (`tools/file_split.py`, or by group as in the A1/A2 commits).
- Running: P (python + patterns), research EN, research CN.

## Queue (≤ 3 agents at a time, sonnet; relaunch on opus if sonnet is limited)

Running 2026-10-24 ~02:00: L1, L10, L11. Research (EN, CN) and the catalog are done and committed.

1. Kit pages: `agents/prompt_K1.md` (company, loop, behavioural), `K2a` + `K2b` (eight system designs), `K3` (八股)
2. LeetCode cards: `agents/prompt_L2.md` … `L9`, `L12` (file split cards per group after review)
3. Obsidian: `vault/interviews/core/leetcode/tiktok/README.md` problem index linking each whole-answer card
4. Build + anki-push `tiktok-lc`, `tiktok-lc-drill`, `pl` (pl push pending: AnkiConnect not responding since ~01:40;
   after it, delete the empty old root deck 编程语言原理：Go · Java · Rust · Python if it remains)
