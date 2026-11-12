---
slug: maximum-height-by-stacking-cuboids
---
## Q
**LC 1691 堆叠长方体的最大高度**｜Hard

`n` 个长方体可任意旋转，`i` 能放在 `j` 上当且仅当三维都不大于 `j`。选一个子集堆叠，求最大总高度。

## A
**一句话。** 每个长方体三边升序、最长边当高，整体字典序排序后做带权 LIS：`dp[i] = 高度 + max(dp[j])`。

```python
def max_height(cuboids):
    boxes = sorted(sorted(c) for c in cuboids)  # 先内部再整体
    dp = [0] * len(boxes)        # dp[i]：以 boxes[i] 为底的最大高度
    for i, box in enumerate(boxes):
        dp[i] = box[2] + max(
            (dp[j] for j in range(i)
             if all(a <= b for a, b in zip(boxes[j], box))),
            default=0)
    return max(dp)
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 忘了先给每个长方体内部排序：示例 1 得 `65`，应为 `190`。
- 只内部排序不整体排序：`[[4,5,5],[4,4,2]]` 得 `5`，应为 `9`。
- 把三个朝向都展开成独立项：同一箱子被叠多次，`[[1,2,3]]` 得 `6`，应为 `3`。

**追问。**
- 要输出具体方案？：多存 `prev[i]`，最后沿它回溯。
- `n` 到 `10^5` 怎么办？：三维偏序，用 CDQ 分治加树状数组，`O(n log² n)`。

**同模式。** LC 354 俄罗斯套娃信封、LC 300 最长递增子序列、LC 646 最长数对链、LC 368 最大整除子集
