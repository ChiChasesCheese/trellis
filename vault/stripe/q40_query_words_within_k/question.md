# q40 · Query Words Within k — proximity search, minimal window, normalization, document ranking

## Context
Stripe's support search has to find help articles where all the words of a query occur *close
together* ("dispute evidence" within a few words of each other is a much better hit than the two
words in different paragraphs). The interview reduces this to word positions: given a text and a
query of words, find where the query words appear within `k` words of each other, then the
tightest window, then make it robust to punctuation and rank several documents.

## Input (stdin)
First line `PART n` (n ∈ 1..4). Blank lines ignored.
- Part 1: line 2 is the text; every following line is `query|k`.
- Parts 2–3: line 2 is the text; every following line is a query.
- Part 4: line 2 is the query; every following line is `name|text`.
Words are whitespace-separated tokens. In Parts 1–2 tokens are matched **exactly** (case and
punctuation included); Parts 3–4 normalize (see Part 3). Repeated words in a query count once.

## Output
- Part 1: the start indices, ascending, separated by single spaces (empty line if none).
- Parts 2–3: `start,end` (0-based, inclusive) of the minimal window, or `-1`.
- Part 4: `name,length` per document that contains every query word, sorted by window length
  ascending, ties by input order; nothing for documents missing a word.

## Rules
### Part 1 — `find_starts(text, query, k) -> list[int]`
Return every index `i` at which the **first word of the query** occurs such that every other
query word occurs at some position `p` with `i < p ≤ i + k` ("within at most k words after
it"). Positions are 0-based word indices. A one-word query returns all its positions.

### Part 2 — `min_window(text, query) -> (start, end) | None`
The shortest contiguous span of words containing **all** query words in **any order**; on equal
length the **earliest** start. `None` if some word never occurs. Sliding window over the token
list (LC 76 on words), O(n).

### Part 3 — normalization
`tokenize(text, normalize=True)`: lowercase, then tokens are maximal runs of letters/digits
(`[a-z0-9]+`), so punctuation is dropped and `Quick-fox` yields `quick`, `fox`. The query is
normalized the same way. Parts 1–2 functions accept `normalize=True` as a keyword.

### Part 4 — `rank(docs, query) -> list[(name, length)]`
Normalize; for each `(name, text)` compute the Part 2 window; keep documents that contain all
words; sort by `(length, input order)`; `length = end - start + 1`.

Follow-up the interviewer asked (source): preprocess the text into `word -> sorted list of
positions` so repeated queries do not rescan the text — the `Document` class does this and
Part 1 uses `bisect` on it.

## Worked examples
Text (22 words; reproduces the source's `[1, 20]`):
```
The quick brown fox is quick and the lazy dog sleeps while a quick cat runs far away from the quick fox
```
```
PART 1
quick fox|2       -> 1 20
quick fox|1       -> 20
fox quick|2       -> 3
quick|0           -> 1 5 13 20
zebra fox|5       ->               (empty line)
PART 2
quick fox         -> 20,21         (window [1,3] has length 3, [20,21] length 2)
lazy cat          -> 8,14
quick zebra       -> -1
```
```
PART 3        text: The Quick, brown fox! Quick-fox.
QUICK fox         -> 3,4          ("fox! Quick" — any order)
PART 4        query: quick fox
a|the quick brown fox
b|fox quick
c|quick and slow
d|Quick, fox!     -> b,2
                     d,2
                     a,3
```

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s14-string-normalization|S14 字符串归一化 / 规范化]]
- [[s16-sliding-window-token-bucket|S16 滑动窗口计数器 / 令牌桶]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
