# Task — TikTok / ByteDance catalog: rank what was reported, find what the decks are missing

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only
`research/companies/tiktok/catalog/CATALOG.md`, `catalog/additions.json` and scratch in `/tmp/tiktok_catalog/`.

Inputs: every file in `research/companies/tiktok/catalog/` and `catalog/raw/` (English and Chinese research, 1point3acres
question bank, Nowcoder mirror, the TikTok 面经 PDF compilation, Hello Interview), and `research/companies/tiktok/index.json`
(the 278 LeetCode problems already in the decks, keyed by slug).

1. **CATALOG.md** — one row per problem family (coding, system design, scenario/八股, behavioural kept in separate tables):
   name, aliases, LeetCode number(s) if any, how TikTok changed it (variant), stages (OA / phone / onsite / HM), `#refs`
   = independent reports (de-duplicate the same event seen on several sites — `raw/aggregators_cn.md` §5 maps them),
   last seen (date), region (US / CN / SG), confidence, source pointers. Rank coding rows by refs × recency; write the
   **cut line** where the top rows cover ~80% of coding sightings, computed with a script (state the numbers).
2. **additions.json** — what the decks still need:
   - `leetcode`: LeetCode originals reported at least once in the window (2025-10..2026-10) that are **not** in
     `index.json` — `{slug, id, refs, last_seen, why}` (resolve the slug by checking `https://leetcode.com/problems/<slug>/`
     or the leetcode.cn GraphQL `question(titleSlug:)`).
   - `variants`: TikTok-specific problems that are not plain LeetCode originals (changed constraints, extra parts, or
     custom backend problems such as LRU with TTL, KV store with snapshot/restore, seller task scheduler, percentile
     finder, chat-message window merge, currency conversion, IP range to CIDR) — `{key, title_zh, title_en, refs,
     last_seen, statement}` where `statement` is a precise, self-contained problem statement in Chinese reconstructed
     from the reports (inputs, outputs, constraints, examples, the follow-ups interviewers asked). Mark in a `note`
     field which parts were inferred.
   - `system_design`: ranked prompts with what interviewers pushed on.
Reply ≤ 10 lines: row counts, the cut line numbers, how many LeetCode originals and variants to add.
