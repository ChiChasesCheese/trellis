---
id: tlc-pile-box-lcci-2-code
node: b.pile-box-lcci
type: qa
step: 2
---
## Q
**面试题 08.13 堆箱子**｜写出 Python 实现

`box` 是至多 `3000` 个 `[w, d, h]`，不能翻转；上面的箱子三维都必须严格小于下面的。返回最大总高度。要求 `O(n^2)`。

## A
**思路。** 先按宽度排序，使得能放在 `boxes[i]` 上面的箱子都在它前面。`dp[i]` 是以 `boxes[i]` 为底的最高箱堆：在前面三维都严格更小的箱子里取最大的 `dp[j]`，加上 `h_i`。答案是 `max(dp)`。

```python
def pile_box(box: list[list[int]]) -> int:
    boxes = sorted(box)                          # 按宽度升序：能放在 boxes[i] 上面的箱子都排在它前面
    dp = [0] * len(boxes)                        # dp[i]：以 boxes[i] 为最底层的箱堆的最大高度
    for i, (w, d, h) in enumerate(boxes):
        above = 0                                # 能放在 boxes[i] 上面的最高箱堆
        for j in range(i):
            wj, dj, hj = boxes[j]
            if wj < w and dj < d and hj < h:     # 三个维度都严格更小
                above = max(above, dp[j])
        dp[i] = above + h
    return max(dp)
```

运行：`[[1,1,1],[2,2,2],[3,3,3]]` → `6`，`[[1,1,1],[2,3,4],[2,6,7],[3,4,5]]` → `10`，`[[5,5,5]]` → `5`，`[[1,1,1],[1,1,1]]` → `1`，`[[3,1,1],[1,3,1]]` → `1`。

**复杂度。** 时间 `O(n^2)`：约 `n^2/2` 次三维比较，`n = 3000` 约 `4.5 * 10^6` 次；空间 `O(n)`。

**写法要点。** `sorted(box)` 对列表按字典序比较，第一关键字就是宽度，不必写 `key`；`for i, (w, d, h) in enumerate(boxes)` 在循环头里同时解包下标和三个维度，比 `boxes[i][0]` 可读得多；`above = 0` 表示「上面不放箱子」，所以没有可叠的箱子时 `dp[i] = h`。
