---
id: cc-algorithms-prefix-suffix-pair
node: algorithms.prefix
type: qa
---
## Q
"Split the array at some index; the score is best-of-left plus best-of-right." Two passes — write the shape.

## A
**Build a suffix aggregate first, then sweep left maintaining the prefix aggregate.**

```python
suf = [0] * (n + 1)
for i in range(n - 1, -1, -1):
    suf[i] = max(suf[i + 1], a[i])        # or sum, count, min, running gcd ...
run, best = float("-inf"), None
for i in range(n):                         # split after index i
    run = max(run, a[i])
    cand = run + suf[i + 1]
    if best is None or cand > best: best = cand
```

- Two O(n) passes and O(n) memory, versus O(n²) for recomputing each side per split.
- Decide whether the split is *between* elements or *at* one, and whether an empty side is allowed. That single decision fixes both loop bounds and the size of `suf`.
- Any **associative** aggregate works; a non-associative one (median, distinct count) does not and needs a different structure.
- If both sides need the same aggregate, one array and one running value is enough — do not build two full arrays out of symmetry.

## Q zh
「在某个下标处分割数组；得分是左侧最优加右侧最优。」两趟 —— 写出它的形态。

## A zh
**先构造后缀聚合，再从左往右扫描并维护前缀聚合。**

```python
suf = [0] * (n + 1)
for i in range(n - 1, -1, -1):
    suf[i] = max(suf[i + 1], a[i])        # 也可以是 sum、count、min、滚动 gcd……
run, best = float("-inf"), None
for i in range(n):                         # 在下标 i 之后分割
    run = max(run, a[i])
    cand = run + suf[i + 1]
    if best is None or cand > best: best = cand
```

- 两趟 O(n)、O(n) 内存，对比每个分割点各自重算两侧的 O(n²)。
- 先决定分割是在元素*之间*还是*落在*某个元素上，以及是否允许某一侧为空。这一个决定同时确定了两个循环边界和 `suf` 的大小。
- 任何**可结合**的聚合都行；不可结合的（中位数、去重计数）不行，需要另一种结构。
- 如果两侧需要同一种聚合，一个数组加一个滚动值就够了 —— 不要为了对称而建两个完整数组。
