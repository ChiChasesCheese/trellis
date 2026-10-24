# TikTok / ByteDance — checkpoint

## State (2026-10-24)

- LeetCode list: 278 problems in `index.json` (A 72 / B 122 US lists; C 84 China-side CodeTop). Skeletons
  `tiktok-lc` (deck LeetCode Tops::24, whole answers + Python toolkit + patterns) and `tiktok-lc-drill` (::25, split
  cards). Statements in gitignored `sources/local/tiktok-lc/`; four 补充题 have none (restated from knowledge).
- Cards done and committed: pilot LC 3, A1 (23), A2 (23). Split cards are filed into the drill deck by the orchestrator
  (`tools/file_split.py`, or by group as in the A1/A2 commits).
- Running: P (python + patterns), research EN, research CN.

## Queue (≤ 3 agents at a time, sonnet; relaunch on opus if sonnet is limited)

1. pl C++: `research/domains/pl/prompt_CPP.md`, `prompt_T1.md`, `prompt_T2.md`
2. LeetCode cards: `agents/prompt_A3.md`, `B1`–`B5`, `C1`–`C4`
3. After research: `catalog/CATALOG.md` (one row per problem family, refs, recency) → new problems / TikTok variants
   into the decks; kit pages in `vault/interviews/companies/tiktok/` (README, LOOP_GUIDE, company brief, behavioural)
   and system design in `vault/interviews/core/system-design/tiktok/`
4. Obsidian: `vault/interviews/core/leetcode/tiktok/README.md` problem index linking each whole-answer card;
   pattern and Python handbooks
5. Build + anki-push `tiktok-lc`, `tiktok-lc-drill`, `pl`
