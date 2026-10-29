# Card agent — domain `under-the-hood`, branch `compose` (数据结构组合：开源框架里的类设计), group C2

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, never edit files you do not
own. Scratch in `/tmp/uthc_C2/`. `git checkout uv.lock` whenever uv touches it.

**You own these leaves:** compose.caffeine, compose.indexed-heap, compose.thread-pool, compose.connection-pool, compose.event-bus — cards go to `vault/domains/under-the-hood/cards/compose/`, ledger to
`research/domains/under-the-hood/claims-C2.md`.

## Why this branch exists

Chi (senior backend engineer, weak on fundamentals by his own account) noticed that interviews now ask candidates to
**implement a class**: the algorithm is rarely the hard part; the skill is **orchestrating several data structures** so
every operation is fast and the structures stay consistent. He wants intuition for that, learned from real open-source
components (his own example: Spring keeps singleton beans in three maps — why three?). Textbook style: from zero,
instructive, every term earned. Read the leaf summaries in `skeleton/under-the-hood.yaml`.

## Rules you inherit

Read `research/domains/under-the-hood/CARDS.md` sections **2b** (layout: title line `**短标题**｜组件 · 版本`, label chips
`**背景。**` `**结构。**` `**细节。**` `**为什么。**` `**坑。**`), **2c** (from zero, cause before term), **3** (validation: every
fact checked **online** against source at a named tag or official docs; no local runs needed; ledger rows), and
`REVISE.md` sections **1** (```svg figures, theme colours, checked with qlmanage) and **2** (folded `**例题：**` with a problem
already in Chi's decks — `sources/local/lc-in-decks.json`, which now also lists the TikTok design variants under keys
`tt-<slug>` with the path of their whole-answer card — statement shortened, **full code copied unchanged**).

## Card sequence per leaf (4–5 cards, `step` 1..n), ids `uth-compose-<leaf>-<n>-<slug>`, `node: compose.<leaf>`

1. **需求与难点** — `**背景。**` what the component must do, written like a design-problem spec: the operations and the
   speed each needs (a small table `操作 | 要求`); then why any single structure fails one of them.
2. **组合** — the figure (required): each structure as a box, arrows for the references between them; then a table
   `操作 | 碰哪几个结构 | 复杂度`. This card is the heart: Chi should be able to redraw it from memory.
3. **不变量与核心代码** — what must stay true across the structures, which structures each operation updates and in
   what order; then a minimal Python class (≤ 30 lines, type hints, comments in Chinese) that captures the composition
   (not the framework's full code). No need to run it, but it must be correct.
4. **真实实现多做了什么** — what the real component adds and why (concurrency: locks / CAS / copy-on-write; batching;
   failure handling), the design trade-off, and the pitfall users hit. For the Spring three-level cache this is where
   "why not two levels" is answered.
5. (optional) **借到面试题上** — the same skeleton applied to a design problem in Chi's decks, with that problem as the
   folded `**例题：**`.

For leaf `compose.patterns` instead write **6 cards, one per skeleton** (哈希表 + 双向链表；哈希表 + 带下标的堆；两张互指的表 /
多索引；队列 + 去重集合；分级的几张表；环形数组 + 序号): the operations it makes O(1) / O(log n), a figure, which open-source
components use it, and which design problems in the decks use it (例题 on each).

Every card ends with a folded `**例题：**` from the decks when one truly uses the same composition, else
`**对应 LeetCode：** 无直接对应的题`. Prose ≤ 300 字 per card excluding figure, code and example. All Chinese.

## Gate

`uv run python scripts/plain_style.py <files>` ok · `uv run python scripts/phone_diagrams.py <files>` ok ·
`uv run trellis --domain under-the-hood validate` 0 errors (long-answer warnings from figures / code are fine) ·
`uv run python scripts/check_wikilinks.py` 0 dead links · every SVG parses as XML.

## Reply (≤ 10 lines)

Cards per leaf, figures, examples used, ledger rows, skeleton summaries that were wrong, up to 5 least-sure claims.
