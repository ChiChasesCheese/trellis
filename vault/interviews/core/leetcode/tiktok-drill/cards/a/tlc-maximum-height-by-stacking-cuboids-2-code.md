---
id: tlc-maximum-height-by-stacking-cuboids-2-code
node: a.maximum-height-by-stacking-cuboids
type: qa
step: 2
---
## Q
**LC 1691 堆叠长方体的最大高度**｜写出 Python 实现

`cuboids` 是 `n` 个 `[width, length, height]`（`1 <= n <= 100`，边长 `1..100`），可旋转，`i` 能放在 `j` 上当且仅当三维都 `<=`，选子集堆叠，返回最大高度。

## A
**思路。** 先把每个长方体的三条边升序，使最长边做高；再把所有长方体按三元组排序。`dp[i]` 是以第 `i` 个为底的最大高度，等于它的高度加上排在前面、三维都不大于它的 `dp[j]`（放在它上面）的最大值。

```python
def max_height(cuboids: list[list[int]]) -> int:
    boxes = sorted(sorted(c) for c in cuboids)      # 先让每个长方体 w<=l<=h，再整体按字典序排
    dp = [0] * len(boxes)                            # dp[i]：以 boxes[i] 为底的最大高度
    for i, box in enumerate(boxes):
        dp[i] = box[2] + max(
            (dp[j] for j in range(i) if all(a <= b for a, b in zip(boxes[j], box))),
            default=0,                               # 上面放不了任何箱子：只有它自己
        )
    return max(dp)
```

运行：`[[50,45,20],[95,37,53],[45,23,12]]` → `190`，`[[38,25,45],[76,35,3]]` → `76`，六个同尺寸旋转版 → `102`，`[[1,1,1]]` → `1`。

**复杂度。** 时间 `O(n log n + n^2)`（排序加双层循环），空间 `O(n)`。

**写法要点。** `sorted(sorted(c) for c in cuboids)`：内层 `sorted` 返回新列表，不改入参（`c.sort()` 会改）；外层对 `list[int]` 排序就是字典序。`all(a <= b for a, b in zip(...))` 表达逐维比较；`max(生成器, default=0)` 处理「上面放不了任何箱子」，不用先判空；生成器不建中间列表。
