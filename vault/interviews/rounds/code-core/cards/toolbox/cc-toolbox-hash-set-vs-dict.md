---
id: cc-toolbox-hash-set-vs-dict
node: toolbox.hash
type: qa
---
## Q
You need "have I seen this id" and, separately, "dedupe this list keeping first-appearance order". Which structure for each, and what does the wrong one cost?

## A
**Set for membership, dict when you need the payload, `dict.fromkeys` for ordered dedupe.**

- `x in some_set` is O(1); `x in some_list` is O(n). A membership test on a list inside a loop is the most common accidental quadratic there is — 10^5 × 10^5 is 10^10.
- Sets are **unordered**: never iterate one to produce output. `list(dict.fromkeys(xs))` dedupes *and* keeps first-appearance order in one pass.
- `set(a) & set(b)`, `|`, `-` express intersection, union and difference directly, but throw away both order and multiplicity — use `Counter` when counts matter ([[cc-toolbox-hash-counter]]).
- A set of tuples is the cheap way to dedupe composite records; a set of dicts is impossible ([[cc-toolbox-hash-tuple-keys]]).

## Q zh
你需要「这个 id 见过吗」，另外还需要「按首次出现顺序给这个列表去重」。各用什么结构，用错的代价是什么？

## A zh
**成员判断用 set，需要携带值时用 dict，有序去重用 `dict.fromkeys`。**

- `x in some_set` 是 O(1)；`x in some_list` 是 O(n)。在循环里对 list 做成员判断是最常见的无意二次复杂度 —— 10^5 × 10^5 就是 10^10。
- set 是**无序的**：绝不要遍历 set 来产生输出。`list(dict.fromkeys(xs))` 一趟既去重*又*保留首次出现顺序。
- `set(a) & set(b)`、`|`、`-` 直接表达交、并、差，但会丢掉顺序和重数 —— 重数重要时用 `Counter`（[[cc-toolbox-hash-counter]]）。
- 用 tuple 的 set 是给复合记录去重的廉价办法；dict 的 set 则根本不存在（[[cc-toolbox-hash-tuple-keys]]）。
