---
id: cc-algorithms-binary-search-loop-shape
node: algorithms.binary-search
type: qa
---
## Q
Give one binary-search loop shape you can write from memory without an off-by-one, and say exactly what it returns.

## A
**First index where a monotone predicate is true, on a half-open range.**

```python
lo, hi = 0, n                      # hi is EXCLUSIVE and is always "true, or past the end"
while lo < hi:
    mid = (lo + hi) // 2
    if pred(mid): hi = mid         # keep mid as a candidate
    else:         lo = mid + 1
return lo                          # == n when nothing satisfies pred
```

- Invariant: everything below `lo` is false, everything from `hi` up is true. It holds on entry and after every step, so the exit value is provably the boundary.
- `mid` can never equal `hi`, so the range strictly shrinks — no infinite loop, whichever rounding you use.
- "Last true", "first ≥ x", "insertion point" are all this shape with a different `pred`. Do not keep a second, `<=`-flavoured variant around; one shape you trust beats two you half-remember.
- Returning `n` for "no such index" is a legitimate answer, not an error ([[cc-algorithms-binary-search-bounds]]).

## Q zh
给出一个你能凭记忆写出、不会 off-by-one 的二分循环形态，并说清它到底返回什么。

## A zh
**在半开区间上，返回单调谓词首次为真的下标。**

```python
lo, hi = 0, n                      # hi 是开区间端点，且始终「为真或越过末尾」
while lo < hi:
    mid = (lo + hi) // 2
    if pred(mid): hi = mid         # 把 mid 保留为候选
    else:         lo = mid + 1
return lo                          # 没有元素满足 pred 时等于 n
```

- 不变式：`lo` 以下全为假，`hi` 及以上全为真。它在进入时成立、每一步之后也成立，所以退出值可证明就是那个边界。
- `mid` 永远不可能等于 `hi`，所以区间严格收缩 —— 无论怎么取整都不会死循环。
- 「最后一个为真」「第一个 ≥ x」「插入位置」都是同一形态换个 `pred`。不要再留一个 `<=` 风味的第二版本；一个你信得过的形态胜过两个记得半吊子的。
- 「不存在这样的下标」时返回 `n` 是合法答案，不是错误（[[cc-algorithms-binary-search-bounds]]）。
