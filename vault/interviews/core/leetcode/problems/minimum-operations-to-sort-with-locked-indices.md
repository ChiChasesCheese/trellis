---
slug: minimum-operations-to-sort-with-locked-indices
---
## Q
**LC 4099 将锁定数组排序的最少操作次数**｜Medium

排列 `nums` 与 `locked`：仅当 `i`、`i+1` 都解锁才能交换，也可花一次操作永久解锁一个下标（至多 `k` 次）。求排成递增的最少总操作数，不可能返回 `-1`。

## A
**一句话。** 答案是「必须解锁的锁数 + 逆序对数」，锁住的下标只有 `nums[i]==i+1` 且前缀最大也是 `i+1` 时可不解锁。

```python
def min_ops_locked(nums, locked, k):
    unlock = inv = mx = 0
    seen = []                      # 前缀有序列表，数逆序对
    for i, v in enumerate(nums):
        mx = max(mx, v)
        # 固定分隔点：值已就位且左边恰是 1..i
        if locked[i] and not (v == i + 1 and mx == i + 1):
            unlock += 1
        inv += len(seen) - bisect_right(seen, v)
        insort(seen, v)
    return -1 if unlock > k else unlock + inv
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 只查 `nums[i]==i+1`：`[3,2,1]`, `locked=[0,1,0]`, `k=0` 得 `3`，应为 `-1`，`3` 和 `1` 要穿过下标 1。
- 漏算解锁次数：示例 1 只算交换得 `1`，应为 `2`。
- 把所有锁都解开：示例 1 下标 3 是分隔点不用解，`k=1` 会误判 `-1`。

**追问。**
- 怎么降到 `O(n log n)`？：逆序对改用树状数组。

**同模式。** LC 769 最多能完成排序的块、LC 775 全局倒置与局部倒置、LC 315 计算右侧小于当前元素的个数
