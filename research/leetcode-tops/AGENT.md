# Card agent — LeetCode Tops topic decks (01–17), one whole card per problem

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, edit only your cards.
Scratch in `/tmp/tops_<group>/`. `git checkout uv.lock` whenever uv touches it.

Chi (2026-10-31): the topic decks keep the ~370 most valuable problems (company-tag frequency + classic lists), and
the old 3–6 fragment cards per problem are replaced by one whole card in the TikTok style: intuitive code first, extensions after. **Resume rule:** skip a leaf whose card already exists.

## The card

File `vault/interviews/core/leetcode/tops/cards/<branch>/tlc-tops-<slug>-0-whole.md` (branch = leaf id before the dot), frontmatter exactly:

```
---
id: tlc-tops-<slug>-0-whole
node: <leaf id from skeleton/leetcode-tops.yaml>
type: qa
---
```

Statement: `sources/local/leetcode-tops/<slug>.txt` (copy constraints from it; translate faithfully if English). Lists and
difficulty: `research/leetcode-tops/selection.json` (by slug: `lists`, `rank` = rank by company-tag frequency). If the problem already has a whole card in
`vault/interviews/core/leetcode/tiktok/cards/*/tlc-<slug>-0-whole.md` or `vault/interviews/core/leetcode/classic/cards/tlc-classic-<slug>-0-whole.md`, read it for verified facts, then **rewrite**
to the rules below (do not copy its prose).

Rules: `research/companies/tiktok/CARDS.md`, all of it — recursion first; 2-D DP as a full table (compression only as
one line); main problem first; comments carry the explanation; "What 简单解法 is". Shape:

- Front: `**LC n 中文名**｜<Easy|Medium|Hard> · 全公司热度第 <rank> 名 · <lists joined by 、>` (omit the lists part when empty), the full statement in Chinese with all
  constraints and 1–2 examples, then 「给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。」
- Back, in order: **考点** (one line naming the core concept, searchable) · **一句话** · **识别** (statement signals →
  technique, incl. what `n` allows) · **推导** (short: obvious approach → why it fails → key insight) · optional
  **简单解法** (only per CARDS.md) · the solution in one ```python block, type hints on every parameter and return,
  Chinese comments carrying the reasoning · **运行** (real outputs on the examples and 1–2 edge cases) · **复杂度** ·
  optional **拓展优化** (1–2 bullets an interviewer pushes toward, code when more than a one-line change) · **易错点**
  (2–3, with a concrete wrong output where possible) · **同模式** (2–4 LC problems, preferring ones on the three lists).
- Prose is short; anything code + comments already say is not repeated. Chinese prose, English terms in parentheses.

Every solution runs in your scratch folder on the examples and edge cases, and against a brute force on ≥ 300 random
small inputs whenever one is writable. Never write the testing process on the card.

## Gate (before replying)

`uv run python research/companies/tiktok/tools/gate_cards.py <your files>` (0 problems),
`uv run python scripts/plain_style.py <your files>` (ok), `uv run trellis --domain leetcode-tops validate` (0 errors).
Reply in ≤ 6 lines: cards written, anything unverified.

## Premium problems without a statement file

`logger-rate-limiter`, `design-hit-counter`, `optimal-account-balancing` (and any other empty statement file): restate
the problem precisely from your knowledge of LeetCode (signature, constraints, one example) and say so in your reply.
