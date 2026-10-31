---
id: tlc-number-of-submatrices-that-sum-to-target-4-followup
node: b.number-of-submatrices-that-sum-to-target
type: qa
step: 4
---
## Q
**LC 1074 元素和为目标值的子矩阵数量**｜追问

面试官接着问：（1）矩阵是 `5000 × 20` 的细长形，怎么调整？（2）要输出每个符合条件的子矩阵坐标？（3）改成「和**不超过** `target`」的个数？

## A
1. **细长矩阵**：复杂度由「行对数 × 列数」决定。行数远多于列数时，先转置（`matrix = [list(r) for r in zip(*matrix)]`），把较短的一边作为被枚举的边界，变成 `O(min^2 · max)`；`5000 × 20` 转置后是 `20 × 5000`，行对只有约 `200` 个，每对扫 `5000` 列。
2. **输出坐标**：哈希表的值从计数改成「起点下标列表」，命中 `s - target` 时展开列表，对每个起点输出 `(top, start, bottom, j)`。输出规模可能达到 `O(R^2 C^2)`，所以复杂度由答案大小决定。
3. **和不超过 `target` 的个数**：哈希表不再适用，要找前缀和 `p >= s - target` 的个数。边扫边把前缀和插入有序列表，用 `bisect_left` 求个数：

```python
from bisect import bisect_left, insort


def count_not_over(arr: list[int], target: int) -> int:
    """一维：arr 中和不超过 target 的子数组个数。"""
    prefix = [0]                           # 已出现的前缀和，保持有序
    s = ans = 0
    for v in arr:
        s += v
        ans += len(prefix) - bisect_left(prefix, s - target)   # 前缀和 >= s - target 的起点
        insort(prefix, s)
    return ans
```
   运行：`[1, -1]`、`target = 0` → `2`（`[-1]` 和 `[1,-1]`）；`[2, -1, 3]`、`target = 2` → `4`。

**Python 提醒**：`Counter` 读取缺失键返回 `0` 且不插入；`defaultdict(int)` 读取缺失键会把键插进去，在大量查询 `s - target` 时让字典越来越大，也会改变遍历结果。
