---
id: cc-algorithms-binary-search-continuous
node: algorithms.binary-search
type: qa
---
## Q
The answer is a real number — a rate, a radius, a break-even price. How do you terminate the search?

## A
**Fix the iteration count instead of chasing an epsilon.** A hundred bisections on a `float` range exhaust double precision, so the loop is both exact enough and provably terminating.

```python
for _ in range(100):
    mid = (lo + hi) / 2
    if feasible(mid): hi = mid
    else:             lo = mid
```

- An absolute `while hi - lo > 1e-9` loop can spin forever when the values are large: the gap can never shrink below the spacing between adjacent floats at that magnitude.
- A relative tolerance (`hi - lo > 1e-9 * max(1, abs(hi))`) fixes that, but the fixed count is simpler and needs no reasoning at 3 a.m.
- Better still: **scale the answer to integers** — cents, milli-units, squared distances — and binary search those. Exact, and it matches how the output has to be rounded anyway ([[cc-output-formatting-decimal-shapes]]).
- Print at the precision the spec asks for; never dump the raw `lo`.

## Q zh
答案是一个实数 —— 一个速率、一个半径、一个盈亏平衡价。搜索怎么终止？

## A zh
**固定迭代次数，而不是去追一个 epsilon。** 在 `float` 值域上二分一百次已经把双精度耗尽，所以循环既足够精确又可证明终止。

```python
for _ in range(100):
    mid = (lo + hi) / 2
    if feasible(mid): hi = mid
    else:             lo = mid
```

- 绝对判据 `while hi - lo > 1e-9` 在数值很大时可能永远转下去：在那个量级上，间隔根本无法缩到相邻浮点数的间距以下。
- 相对容差（`hi - lo > 1e-9 * max(1, abs(hi))`）能解决这点，但固定次数更简单，凌晨三点也不需要推理。
- 更好的做法：**把答案缩放成整数** —— 分、毫单位、距离平方 —— 再对它二分。精确，而且反正也符合输出该有的取整方式（[[cc-output-formatting-decimal-shapes]]）。
- 按 spec 要求的精度打印；绝不要直接倒出原始的 `lo`。
