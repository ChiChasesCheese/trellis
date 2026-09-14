---
id: cc-chrono-intervals-covered-sort
node: chrono.intervals
type: qa
---
## Q
Count the ranges that are *not* contained in another range. Sorting by start ascending gives the wrong count when two ranges share a start. Fix it.

## A
**Sort by `(start ascending, end descending)`.** Scanning left to right, an interval is covered exactly when its end is `<= best_end` seen so far.

```python
best_end, kept = float("-inf"), 0
for s, e in sorted(iv, key=lambda x: (x[0], -x[1])):
    if e > best_end:
        kept, best_end = kept + 1, e
```

- With ties on start sorted end-*ascending*, the shorter interval is seen first and wrongly counted as new — that is the whole bug.
- Exact duplicates: the second has `e == best_end`, so exactly one survives.
- Chains like `[1,10], [2,9], [3,8]` collapse to 1 in a single pass; no pairwise containment test is ever needed.
- One interval covering everything reduces the answer to 1, and an empty list to 0 — both worth a line of test.

## Q zh
统计*不*被其他区间包含的区间数。按起点升序排序，在两个区间起点相同时会数错。怎么修？

## A zh
**按 `(起点升序, 终点降序)` 排序。** 从左向右扫描，一个区间被覆盖当且仅当它的终点 `<=` 已见到的 `best_end`。

```python
best_end, kept = float("-inf"), 0
for s, e in sorted(iv, key=lambda x: (x[0], -x[1])):
    if e > best_end:
        kept, best_end = kept + 1, e
```

- 起点相同却按终点*升序*排时，较短的那个先被看到并被错误计为新区间 —— 这就是全部 bug。
- 完全重复的区间：第二个满足 `e == best_end`，因此恰好留下一个。
- 像 `[1,10], [2,9], [3,8]` 这样的链在一次扫描中塌缩为 1；完全不需要两两包含判断。
- 一个覆盖全部的区间会让答案变成 1，空列表则是 0 —— 两者都值得写一行测试。
