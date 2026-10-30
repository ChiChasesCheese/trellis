---
id: tlc-max-submatrix-lcci-4-followup
node: p5.max-submatrix-lcci
type: qa
step: 4
---
## Q
**面试题 17.24 最大子矩阵**｜追问

面试官接着问：（1）矩阵是 `1000 × 3` 的瘦长形，怎么调整？（2）改成「和不超过 `K` 的最大子矩阵」（LC 363）？（3）只含 `0/1`、求最大全 `1` 矩形（LC 85）？

## A
1. **瘦长矩阵**：复杂度是 `O(R^2 · C)`，枚举的是**行对**。行数远多于列数时，先转置（`matrix = [list(r) for r in zip(*matrix)]`）让行数变少，变成 `O(min^2 · max)`；返回坐标时把 `(r1, c1, r2, c2)` 换回 `(c1, r1, c2, r2)`。
2. **和不超过 `K`**：Kadane 不再适用（最大和可能超过 `K`，需要找「最大但不超过 `K`」的）。对每个 `(top, bottom)`，在 `col` 上边扫边维护前缀和的有序列表 `sorted_prefix`：当前前缀和 `s`，需要最小的前缀和 `p >= s - K`，用 `bisect_left` 找到，`s - p` 就是以当前列结尾、不超过 `K` 的最大和；然后 `insort(sorted_prefix, s)`。总时间 `O(R^2 · C log C)`（`insort` 在列表上是 `O(C)` 的搬移，但常数很小）。
3. **最大全 `1` 矩形**：不枚举行对。逐行维护每列向上连续 `1` 的高度，每一行当作直方图，用单调栈求最大矩形，`O(R · C)`。
4. 只要最大和：去掉 `ans`、`start`，保持核心不变。

```python
from bisect import bisect_left, insort


def best_sum_not_over_k(arr: list[int], k: int) -> int:
    """一维：arr 的子数组和中不超过 k 的最大值（可能不存在则返回负无穷）。"""
    prefix = [0]                           # 已出现的前缀和，保持有序
    s, best = 0, float("-inf")
    for v in arr:
        s += v
        i = bisect_left(prefix, s - k)     # 最小的 p >= s - k，使得 s - p <= k
        if i < len(prefix):
            best = max(best, s - prefix[i])
        insort(prefix, s)
    return best
```

**Python 提醒**：`bisect_left(a, x)` 返回第一个 `>= x` 的位置，`bisect_right` 返回第一个 `> x` 的位置；这里需要「`>= s - k`」所以用 `bisect_left`，用错会漏掉恰好等于 `K` 的情形。
