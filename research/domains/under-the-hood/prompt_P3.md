# Card agent — domain `under-the-hood` (工具里的数据结构与算法), group P3

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents, never
edit files you do not own. Scratch work goes in `/tmp/uth_P3/`. `git checkout uv.lock` whenever uv touches it.

**You own these leaves:** python.exceptions-context, python.numbers-floats, python.typing-dataclasses, python.imports-modules

Cards go to `vault/domains/under-the-hood/cards/<branch>/` (`<branch>` = the part of the leaf id before the dot), one
file per card, file name = card id + `.md`. Your claim ledger goes to `research/domains/under-the-hood/claims-P3.md`.

## 0. Resume rule

`uv run trellis --domain under-the-hood stats` and `ls` your folders; skip leaves that already have their cards.

## 1. Who reads these cards, and why

Chi, a senior backend engineer, grinds LeetCode decks every day. This deck is his **break**: when another LeetCode card
makes him feel sick, he switches here. Each card shows one real tool he uses (Python, Java, C++, Go, Rust, Redis, Kafka,
databases, Linux, git …) and the data structure or algorithm inside it, so LeetCode patterns stop feeling abstract.
So the cards must be **short, concrete and intuitive** — a fun fact with a mechanism, not a textbook. The opposite of
what he dislikes: abstract, dense, niche (an earlier deck explained Zopfli and Viola-Jones; do not write like that).

Read the leaf titles and summaries in `skeleton/under-the-hood.yaml` (your leaves' summaries list the points to cover).

## 2. Card shape (2–4 cards per leaf)

```
---
id: uth-<branch>-<leaf-suffix>-<n>-<slug>
node: <leaf id>
type: qa
step: <n>
---
## Q
**<短标题>**｜<工具 · 版本>

<一个具体的问题，一两句话。例如：「Python 的 list.append 为什么是均摊 O(1)？连续 append 时容量怎样增长？」>

## A
<2–5 条短要点或一张小表，总共不超过 150 字（中文字符 + 英文单词）。必须有：底下是什么结构；一个具体的细节或数字
（常数、阈值、版本）；为什么这样设计（和另一种做法比的取舍）。>

**对应 LeetCode：** LC 146 LRU 缓存 · LC 707 设计链表（1–3 道，真正用到同一结构或算法的题）
```

- Chinese prose, English terms in full-width parentheses on first use, identifiers in backticks.
- A tiny code snippet (≤ 6 lines) or phone-width ASCII sketch is welcome when it makes the idea click, e.g. a real
  Python session showing `sys.getsizeof` jumping, or the 3 lines of Java that turn LinkedHashMap into an LRU.
- Each card self-contained: no "如上所述", no reference to other cards or to sources. No URLs, no citations on cards.
- When behaviour depends on version or implementation, say which on the card: 「CPython 3.6 起」「Java 8 起」
  「libstdc++ 与 libc++ 是 2 倍，MSVC 是 1.5 倍」「Go 1.24 起」「Redis 7.0 起 listpack 取代 ziplist」.
- First card of a leaf = the core mechanism; later cards = one surprising detail each, or a pitfall a user actually hits
  (iterator invalidation, hash flooding, catastrophic regex backtracking, `del` not freeing memory …).

## 2b. Card layout — fixed components (Chi, 2026-10-28; overrides the shape in §2)

Chi wants every card beautiful and consistent, all in Chinese, and the **components themselves** carry the meaning: no
sentences that describe what a section is about ("下面说明结构：…", "这一部分讲…"). The Anki template turns these
markdown patterns into styled parts, so use them exactly:

- **Title line** (first line of Q): `**<短标题>**｜<工具 · 版本>` — bold title, full-width bar, plain meta. Example:
  `**append 为什么是均摊 O(1)**｜Python · CPython 3.13`. (Not `**Python｜…**`: the bold part is the title.)
- Q body: one or two sentences, a concrete question.
- A uses **label chips**: a paragraph that starts with a bold short label ending in `。` *inside* the bold, e.g.
  `**结构。** 连续的 `PyObject*` 指针数组。` The fixed labels, in this order, each used only when it has content:
  1. `**结构。**` — one line: what the thing is underneath.
  2. `**细节。**` — then a blank line and 2–4 bullets: numbers, thresholds, versions.
  3. `**为什么。**` — one or two lines: the trade-off against the obvious alternative.
  4. `**坑。**` — optional, one line: the pitfall a user actually hits.
  5. optional fenced code block (≤ 6 lines, real output in comments) or a small table — placed after 细节 or 为什么.
  6. `**对应 LeetCode：**` — last line: `LC 146 LRU 缓存 · LC 460 LFU 缓存`.
- Lists always have a blank line before them. Full-width `；` breaks lines in the template, so prefer bullets over long
  `；` chains. Everything in Chinese; English only for terms (in full-width parentheses on first use) and identifiers.

## 2c. From zero, cause before term (Chi, 2026-10-29; overrides anything shorter)

Chi has never touched most of these internals. A card that lists terms (token, nibble, FSE, entropy coding, RFC
window size …) with no cause and effect is unreadable to him. Rules:

1. **Every leaf opens with a from-zero card** (step 1): the problem the tool has to solve in everyday words, the
   obvious way to do it and where that breaks, then the tool's trick, shown on a **tiny worked example** with a figure
   (e.g. compression: `abcabcabc` → `abc` + 「往回 3 个、复制 6 个」; then why frequent letters get short codes,
   with a Huffman tree for a 4-letter string). Use the label `**背景。**` for the problem and its naive fix, before 结构.
2. **Every term is earned**: the first time a term appears on a card, say what it is in plain words in the same
   sentence, or drop it. A term needs a job in the story; trivia (bit layouts, RFC numbers, default levels) goes
   unless the card is about exactly that.
3. Later cards of a leaf build on the story in order (one new idea per card) and each still restates the 1-line
   context it needs, so it stands alone. Read like a chain: 问题 → 直觉做法 → 卡在哪 → 工具怎么做 → 代价.
4. Shorter is not the goal; understandable is. A from-zero card may be longer (≤ 250 字 excluding figure and example).

## 3. Validation (the most important rule)

Chi asked that **everything is validated**. Every number, threshold, constant, version and mechanism on a card must be
checked against a primary source **in this session**, never written from memory alone:

- Source code at a named tag or branch, fetched with `gh api repos/<owner>/<repo>/contents/<path>?ref=<tag>` or
  `curl https://raw.githubusercontent.com/...` (CPython `Objects/listobject.c`, `Objects/dictobject.c`, `Lib/heapq.py`;
  OpenJDK `jdk21u` `java/util/HashMap.java`; gcc `libstdc++-v3`; llvm `libcxx`; golang/go `src/runtime/slice.go`;
  rust-lang/rust `library/`; rust-lang/hashbrown; redis/redis `src/t_zset.c`, `src/server.h`; apache/kafka; torvalds/linux;
  git/git; google/re2 …), or official documentation / design docs / the paper.
- Online verification is enough (Chi, 2026-10-28): no local runs, builds or benchmarks needed.
- If a claim cannot be verified, drop it. If a skeleton summary is wrong, write the correction in your reply.
- Ledger: `research/domains/under-the-hood/claims-P3.md`, one table row per checked claim:
  `| card id | claim | source (repo@tag:path:function, or doc URL) | how checked (read / ran) |`.

## 4. Gate (before replying)

1. `uv run python scripts/plain_style.py <your files>` — ok.
2. `uv run trellis --domain under-the-hood validate` — 0 errors; no `not_self_contained` / `leans_on_source` on your
   cards; no long-answer warning on your cards (keep answers short).
3. `uv run python scripts/check_wikilinks.py` — 0 dead links.
4. `git checkout uv.lock` if changed.

## 5. Reply (≤ 12 lines)

Cards per leaf, gate results, number of ledger rows, skeleton summaries you found wrong, and up to 5 claims you are least
sure of.

## 6. Also required for this batch

- Follow sections **1 (Pictures)** and **2 (Worked example)** of `research/domains/under-the-hood/REVISE.md` (scratch
  dir `/tmp/uthp_P3/`): a figure per leaf at least, and a folded `**例题：**` with a problem already in Chi's decks
  (`sources/local/lc-in-decks.json`) wherever the Python behaviour actually matters to that problem's solution (for
  example `path[:]` in LC 46 / 78, `nonlocal` in LC 543, `__lt__` or tuple keys in LC 23, an iterator class in LC 173),
  else `**对应 LeetCode：** 无直接对应的题`.
- Goal from Chi: after this branch he should understand Python **from the root**. Teach from zero (§2c), 4–5 cards per
  leaf, one idea per card, in story order. Verify against CPython 3.14 source / docs online. Check that nothing
  contradicts the Python cards of the programming-languages deck (`vault/domains/pl/cards/`, grep for the topic); if
  it does, follow the primary source and say so in your reply.
