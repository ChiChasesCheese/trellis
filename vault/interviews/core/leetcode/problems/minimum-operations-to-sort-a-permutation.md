---
slug: minimum-operations-to-sort-a-permutation
---
## Q
**LC 3942 排序排列的最少操作数**｜Medium

`[0..n-1]` 的排列只能「反转整个数组」或「左旋一位」，求排成递增的最少操作数，不可能则返回 `-1`。

## A
**一句话。** 只有循环升序或循环降序可排好，按 `0` 的位置 `p` 分别算两种代价取小。

```python
def min_operations(nums):
    n = len(nums)
    p = nums.index(0)             # 0 的位置决定一切
    best = inf
    # 循环升序：左旋 p 次，或 反转、左旋 n-p 次、反转
    if all(nums[i] == (i - p) % n for i in range(n)):
        best = min(best, p, n - p + 2)
    # 循环降序：左旋 b 次再反转，或 反转再左旋 n-b 次
    if all(nums[i] == (p - i) % n for i in range(n)):
        b = (p + 1) % n
        best = min(best, 1 + min(b, n - b))
    return -1 if best == inf else best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 升序只用左旋：`[1,2,3,4,5,0]` 要 `5` 次，其实 `3` 次。
- 忘了循环降序也能排好：`[0,2,1]` 得 `-1`，应为 `2`。
- 降序只算「先反转再左旋」：`[1,0,4,3,2]` 得 `4`，应为 `3`。

**追问。**
- 为什么两种形态可能同时成立？：`n <= 2` 时升降序重合，所以取 `min`。
- 只允许左旋呢？：只检查循环升序，答案为 `p`，否则 `-1`。

**同模式。** LC 189 轮转数组、LC 796 旋转字符串、LC 1752 检查数组是否经排序和轮转得到
