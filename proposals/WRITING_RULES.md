# Writing rules for learner-facing pages (Chi, 2026-10-16)

Chi: 「出处这种东西如果非要放就放在页面末尾；所有产出都说人话，教科书级别，有前因后果，自包含，不需要第三人称视角。」
Applies to every article, drill, study note, write-up and card a learner reads. Machine-checkable parts are enforced by
`scripts/plain_style.py` (called from `check_sd.py` and `check_lld_problems.py --branch amazon`).

1. **Provenance goes last.** Where and when a question was reported, thread ids, URLs, dates, confidence, which parts
   are reconstructed — all of it lives only in the page's final section (`## 来源与延伸` in LLD articles, `## 来源与延伸阅读`
   in SD write-ups, `## 来源` in study notes). The body never mentions 一亩三分地 / 1p3a / Hello Interview / 面经 / 帖子 /
   楼主 / 报告 / 置信度 / 重建 / 推断. Write the problem as the problem, not as "what someone was asked".
2. **Talk to the reader, not about the text.** Textbook voice: plain exposition, or「你」when giving instructions
   （「开场先问三个问题」）. Never 本篇 / 本文 / 本题 / 本题解 / 这道题 / 作者 / 我们认为 / 候选人说 / 据报道.
3. **Cause → effect, every time.** Each design choice says what forces it (the cause: a requirement, a number, a failure)
   and what it buys and costs (the effect). A bare "用 X" without why is a defect.
4. **Plain words.** Short sentences. A term of art gets a one-line plain definition the first time it appears, then its
   English name in full-width parentheses: 「幂等（idempotent）：同一个请求做一次和做十次，结果一样。」
5. **Self-contained.** The page can be understood alone. Links to other notes are further reading, never required to
   follow the argument: state the fact here instead of 「见 XX」.
6. **Open with the system in plain words**: what it is, who uses it, what the hard part is — 3–5 sentences, before any
   list or table.
7. **Diagrams that fit a page.** Obsidian's reading column is ~700 px.
   - `flowchart TB` / `graph TD` only — never `LR`/`RL`.
   - ≤ 12 nodes per flowchart, ≤ 4 nodes side by side; split a big system into two diagrams (e.g. 写路径 / 读路径).
   - Node labels ≤ 16 characters (no long parentheticals: `CDN` not `CloudFront (CDN, edge cache)`); explain in prose.
   - `sequenceDiagram` ≤ 5 participants, `autonumber`, every message ≤ 24 display units, a CJK character counting 2 (the
     longest message sets the width); explain each numbered step in a list under the diagram. Start it with
     `%%{init: {'sequence': {'actorMargin': 16, 'width': 104, 'messageMargin': 28}}}%%` (narrow actors).
   - `classDiagram` ≤ 8 classes, members trimmed to what the text discusses.
8. **Cards.** The front asks something answerable from understanding (「火车票价系统里，为什么用前缀和算两站票价？」),
   not 「Amazon 面试里怎么问的」. Provenance goes only in the card's footer link. A meta chip says at most difficulty
   and 「Amazon 2026-10」.
