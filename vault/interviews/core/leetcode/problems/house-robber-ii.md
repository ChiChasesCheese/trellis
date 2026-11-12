---
slug: house-robber-ii
---
## Q
**LC 213 打家劫舍 II**｜Medium

房屋围成一圈，相邻两间不能都偷，求能偷到的最高金额。

## A
**一句话。** 首尾相邻所以不会同时偷，拆成「去掉最后一间」和「去掉第一间」两条直线，各做一遍打家劫舍取大。

```python
def rob(nums):
    def line(houses):
        skip = take = 0        # 前一间不偷 / 偷到前一间的最优
        for money in houses:
            skip, take = take, max(take, skip + money)
        return take

    if len(nums) == 1:         # 首尾是同一间
        return nums[0]
    return max(line(nums[:-1]), line(nums[1:]))
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 当直线做：`[2,3,2]` 得 `4`（偷了两端），应为 `3`。
- 漏掉 `n == 1`：`[5]` 两条直线都是空，得 `0`，应为 `5`。
- `skip, take` 拆成两条赋值：会用到已被覆盖的 `take`。

**追问。**
- 返回具体偷了哪几间？：保留整张 `dp` 表从后往前回溯，两条直线各一次，取总额大的。
- 房屋排成一棵树？：每个节点记偷 / 不偷两个状态，自底向上合并（LC 337）。

**同模式。** LC 198 打家劫舍、LC 337 打家劫舍 III、LC 740 删除并获得点数、LC 2560 打家劫舍 IV
