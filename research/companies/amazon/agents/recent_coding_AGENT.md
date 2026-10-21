# Agent instructions — Amazon「近一月面经」coding 题（2026-09-16..10-16）

Read `../AGENT_RULES.md` first (role, senior bar, textbook mode, Python, public repo). This file adds the rules for the
`recent/` layer: **coding** problems reported on 1point3acres and Hello Interview in the last 30 days, **not OA**.
OOD problems live in the low-level-design `amazon` branch and system design in `vault/interviews/core/system-design/` — not here.
The cards you write become the Anki deck `LeetCode Tops::22 Amazon 近一月原题（2026-10）`.

> **`proposals/WRITING_RULES.md` overrides everything below** (Chi, 2026-10-16): provenance only in the last section, textbook voice to the reader, cause → effect, self-contained, diagrams `flowchart TB` that fit the page. `scripts/plain_style.py` enforces it inside the gate.

## Inputs (read-only)

- 1p3a digest of all 39 Amazon threads 2026-09-16..10-16 (visible text only; most thread bodies are hidden behind
  "积分 > 188"): `/Users/chizhang/.claude/jobs/5ce355d9/tmp/digest.txt`. Thread URL = `https://www.1point3acres.com/bbs/thread-<tid>-1-1.html`.
- 1p3a question bank rows (slug, stage, dates, #sources; bodies locked): `/Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/qbank.json`.
- Hello Interview Amazon reports with `approxAskedOn`: `/Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_amazon_all.json`
  (question URL = `https://www.hellointerview.com/community/questions/<slug>`... cite the company page
  `https://www.hellointerview.com/community/questions?company=Amazon` plus the slug).
- Hello Interview LLD breakdowns (Chi has a membership; **paid content — read for comparison, never copy sentences,
  diagrams or code into the repo; link the page and paraphrase what differs**): `/Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_lld/*.txt`
  (amazon-locker, parking-lot, file-system, inventory-management, delivery). URLs:
  `https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/<name>`.
- What the kit already has: `../lld/route.md`, `../lld/*.md`, `../coding/solutions/`, `../coding/top_list.md`,
  the LLD domain `vault/domains/low-level-design/problems/<name>/` and its drills. Link to them; do not rewrite them.

## What you write (only in the paths your task names)

1. **One Chinese study note per item** — textbook mode: the problem in plain words → 开场先问的澄清问题 → 最笨解 → 逐步改进（每步：问题 / 想法 /
   为什么有效）→ 最终代码 → 复杂度 → senior 追问（并发、规模、扩展需求 5–6 条，每条说「改哪里」）→ 自测题（答案放
   `<details>`）. File names start with `amz_` (Obsidian resolves notes by name; names must be unique in the vault).
   First line `# <中文名>（<English>）`. The last section `## 来源` holds every URL, date, and which parts are
   reconstructed — nowhere else.
2. **Runnable code** for every coding / OOD item: one `.py` per item, `python3 -I <file>` must print `OK <name>` and
   exit 0. Coding items cross-check against a brute force on ≥ 300 random small inputs (seeded `Random`) plus the
   reported examples. OOD items: asserts that exercise every requirement and every extension you claim is "one class".
   LeetCode originals go to `../coding/solutions/<number>_<snake_name>.py` with the `# --- solution ---` /
   `# --- end ---` markers (copy the layout of `../coding/solutions/399_evaluate_division.py`).
3. **Cards** in one JSON file your task names: a list of objects

   ```json
   {"id": "arm-<slug>[-n]", "slug": "<slug>", "kind": "coding|ood|sd",
    "title": "中文名（English）", "meta": "Medium · 1p3a 2026-10-07 L5 店面 · 重建",
    "question_md": "题面（markdown），含数据范围或明确写出「面经未给范围」",
    "answer_md": "思路｜…\n\n```python\n…\n```\n\n复杂度｜…\n\n追问｜…",
    "note": "<vault-relative path of your study note>",
    "sources": [{"label": "1p3a 1192241", "url": "https://…"}],
    "reconstructed": true, "confidence": "high|medium|low"}
   ```

   1–2 cards per item. A card is a whole-problem recall card: front = the problem, back = idea + code + complexity +
   one follow-up. In `answer_md`, a paragraph that starts with `<label>｜` becomes a chip (`思路｜`, `复杂度｜`,
   `追问｜`, `失败模式｜`, `澄清｜`). Card code ≤ 45 lines and **must appear verbatim in your `.py` file**.
   Confidence: high = first-hand with the question text visible; medium = summary/aggregator naming the problem;
   low = inferred from fragments.

## Rules (each one is a defect found in an earlier batch)

- Never write「本题」「这道题」on a card — name the problem; cards are read out of context.
- No process talk on cards or notes (「我验证过」「对拍 300 组通过」). Show a concrete input and its output instead.
- Every number (complexity bounds, sizes, example outputs) is computed by running code, not typed from memory.
- A reconstructed constraint is labelled **(reconstructed)** in the note and `"reconstructed": true` on the card.
- Chinese body, English terms in parentheses; more Han characters than Latin letters in prose.
- Recursion that can exceed 1000 frames at the stated bounds must be iterative.
- No content from lodely / vervecopilot. 1p3a and Hello Interview text: quote at most one sentence per source, with URL.
- Do not commit, do not spawn agents, do not touch files outside your task. Resume rule: if a file exists, read it and
  only add what is missing.
- Final reply ≤ 12 lines: files written (counts from `ls`/`wc`), `OK` lines from running every `.py`, the weakest claim
  in your work.

## Your task list (write notes in `recent/coding/`, LC solutions in `../coding/solutions/`, cards in `recent/cards/coding.json`)

Card order in the JSON = study order: put them in the order below. Every source line here is from
`../catalog/raw/1p3a_2026-10-16.md` / `../catalog/raw/hellointerview_2026-10-16.md` — cite the URL from there.

1. LC 305 Number of Islands II（数岛屿 II）+ 逐行流式输入的变体 — 1p3a 1191823 (NG onsite, follow-up「如果矩阵是流式一行一行进来的怎么办 union find嘛？」); qbank `number-of-islands-max-area-streaming` (3 src, last 2026-10-03). An existing Anki card `streaming-island-count` covers the row-streaming idea: write the 305 card and one card on the bridge between them.
2. LC 490 The Maze + 方向约束变体 — 1p3a 1190455 (SDE II phone 2026-09-16: BFS with movement constraints, 3-D visited (r, c, dir); reply 「好像490.差不多，但是有方向的变形」). Existing Anki card `forbidden-turn-grid` is the reconstructed variant: write 490 and a card that states the reported variant precisely, labelled (reconstructed).
3. LC 815 Bus Routes（公交路线）— Hello Interview `bus-routes-815`, 2026-09-20 mid APAC.
4. LC 3286 Find a Safe Walk Through a Grid（安全路径）— Hello Interview `safe-walk-grid`, 2026-10-01 mid APAC. 0-1 BFS.
5. LC 2365 Task Scheduler II（任务调度器 II）— Hello Interview `task-scheduler-ii`, 2026-09-10 staff.
6. LC 332 Reconstruct Itinerary（重新安排行程）— Hello Interview `reconstruct-itinerary`, 2026-09-20 mid. Hierholzer; iterative.
7. LC 45 Jump Game II, return the jumps（跳跃游戏 II，返回路径）— Hello Interview `leetcode-jump-game`, 2026-09-10 senior EMEA: "Jump game II but to return array of choices".
8. 棋子最少步数吃掉国王（Chess piece to king, min moves）(reconstructed) — 1p3a 1192241 (L5 phone 2026-10-07): 「下棋游戏：棋子从起始点出发到打倒对面的king，求最短几步」; reply guesses BFS with state compression. Reconstruct: board with obstacles (own pieces), a given move set (knight / king / sliding piece as follow-ups), BFS; follow-up: several of your pieces, opponent's king moves.
9. 组织架构最低共同上级（Lowest Common Manager）— 1p3a qbank `lowest-common-manager-org-chart` (phone/onsite, 3 sources, 2026-07-31..10-01); 1p3a 1191548 (L6 phone 2026-10-01) classic LCA. n-ary tree; follow-ups: parent map, many queries (binary lifting), an employee not in the tree, k employees.
10. LC 399 + 缓存追问（Evaluate Division with caching）— 1p3a 1191084 (L6 phone 2026-09-28: BFS coding + caching follow-up); qbank `evaluate-division-lc-399` (phone 2026-09-28). The kit has `399_evaluate_division.py`; write only the follow-up card(s): memoising query results vs weighted union-find, invalidation when a new equation arrives.
11. LC 472 Concatenated Words 的 Trie + DFS 写法 — 1p3a 1192241 (L5 phone, site summary "a LeetCode 472 variant using Trie and DFS"). The kit has `472_concatenated_words.py`; add the Trie + DFS version and one card contrasting it with the word-set DP.
12. 多粒度滑动窗口限流（Sliding-window rate limiter, per IP / user / experience）— Hello Interview `sliding-window-rate-limiter`, phone screen 2026-10-01 mid USA. Coding round, not OOD: sliding-window log vs sliding-window counter, a key function for granularity, memory bound.

For each LC original: solution file with a brute-force cross-check; a whole-problem card in the style of the existing
`leetcode-tops::amazon-a` cards (front: title line + statement with the official constraints — take constraints from
`https://leetcode.com/problems/<slug>/` via WebFetch, or leetcode.cn GraphQL; never from memory; back: 思路 / code /
复杂度 / 追问). Card `meta` must say where and when it was reported, e.g. `Hard · 1p3a 2026-09-16 SDE II 店面`.
