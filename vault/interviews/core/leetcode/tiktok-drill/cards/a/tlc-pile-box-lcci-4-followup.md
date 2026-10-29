---
id: tlc-pile-box-lcci-4-followup
node: a.pile-box-lcci
type: qa
step: 4
---
## Q
**面试题 08.13 堆箱子**｜追问

面试官接着问：（1）返回箱堆本身（从底到顶）？（2）如果箱子**可以旋转**，且叠放条件放宽成「不大于」（LC 1691），怎么改？（3）如果只有两个维度（LC 354 俄罗斯套娃信封），能比 `O(n^2)` 更快吗？

## A
1. **返回箱堆**：多开 `prev[i]` 记录取到最大值的 `j`，从 `dp` 最大的位置沿 `prev` 回溯。

```python
def pile_box_path(box: list[list[int]]) -> list[list[int]]:
    boxes = sorted(box)
    dp = [0] * len(boxes)
    prev = [-1] * len(boxes)                     # prev[i]：箱堆里紧挨在 boxes[i] 上面的那个
    for i, (w, d, h) in enumerate(boxes):
        best = 0
        for j in range(i):
            wj, dj, hj = boxes[j]
            if wj < w and dj < d and hj < h and dp[j] > best:
                best, prev[i] = dp[j], j
        dp[i] = best + h
    i = max(range(len(boxes)), key=dp.__getitem__)   # 最高箱堆的底
    tower: list[list[int]] = []
    while i != -1:
        tower.append(boxes[i])
        i = prev[i]
    return tower                                 # 从底到顶
```

运行：`[[1,1,1],[2,3,4],[2,6,7],[3,4,5]]` → `[[3, 4, 5], [2, 3, 4], [1, 1, 1]]`。
2. **可旋转 + 不大于（LC 1691）**：可以证明每个长方体都把最长边当高、三边升序排列时最优，所以先 `sorted(c)` 把每个长方体三边排好，再整体排序，DP 条件改成两维 `<=`（排序后第一维已不减）：`[[50,45,20],[95,37,53],[45,23,12]]` → `190`。
3. **二维**：按宽度升序、宽度相同时高度**降序**排序，然后只对高度求严格 LIS，用 `bisect_left` 维护「每个长度的最小结尾」，`O(n log n)`。降序是为了让同宽度的信封在高度上无法形成递增，从而不会被误叠。三维偏序没有这样的简单写法（要用 CDQ 分治加树状数组），面试里给出 `O(n^2)` 即可。

**Python 提醒**：`max(range(n), key=dp.__getitem__)` 返回最大值的下标，并列时取第一个；`dp.index(max(dp))` 要扫两遍。
