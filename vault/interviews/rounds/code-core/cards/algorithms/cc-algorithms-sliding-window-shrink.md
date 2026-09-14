---
id: cc-algorithms-sliding-window-shrink
node: algorithms.sliding-window
type: qa
---
## Q
Longest stretch whose sum is at most S, all values positive. Write the loop and justify the linear cost.

## A
**Expand `r` unconditionally; shrink `l` while the invariant is violated.**

```python
l = cur = best = 0
for r, x in enumerate(a):
    cur += x
    while cur > S:                  # restore the invariant before measuring
        cur -= a[l]; l += 1
    best = max(best, r - l + 1)
```

- Each index enters the window once and leaves once, so the inner `while` runs at most n times **in total** — O(n) despite being nested.
- Measure only *after* restoring the invariant, never inside the shrink loop.
- The technique needs the invariant to be **monotone**: adding an element can only push you further from valid, removing one only closer ([[cc-algorithms-sliding-window-monotone-requirement]]).
- With `l` and `r` both moving forward only, nothing is ever re-examined; if your fix involves moving `l` backwards, the shape is wrong.

## Q zh
所有元素为正，求和不超过 S 的最长连续段。写出循环并论证线性代价。

## A zh
**无条件右移 `r`；在不变式被破坏时右移 `l` 收缩。**

```python
l = cur = best = 0
for r, x in enumerate(a):
    cur += x
    while cur > S:                  # 先恢复不变式，再度量
        cur -= a[l]; l += 1
    best = max(best, r - l + 1)
```

- 每个下标进入窗口一次、离开一次，所以内层 `while` **总共**最多执行 n 次 —— 虽然嵌套但仍是 O(n)。
- 只在恢复不变式*之后*度量，绝不在收缩循环内部度量。
- 这项技术要求不变式是**单调的**：加入元素只会让它更远离合法，移除只会更接近（[[cc-algorithms-sliding-window-monotone-requirement]]）。
- `l` 和 `r` 都只前进，所以任何元素都不会被重新检查；如果你的修法需要把 `l` 往回移，说明形态本身就不对。
