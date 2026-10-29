---
id: tlc-house-robber-ii-2-code
node: a.house-robber-ii
type: qa
step: 2
---
## Q
**LC 213 打家劫舍 II**｜写出 Python 实现

整数数组 `nums`（长度 `1..100`，元素 `0..1000`）表示围成一圈的房屋里的现金，相邻（含首尾）的两间不能同时偷，返回最高金额。

## A
**思路。** 先写直线版 `rob_line`：遍历金额，维护「到上一间为止的最优 `take`」和「到上上间为止的最优 `skip`」，每间取 `max(take, skip + money)`。环则拆成不含最后一间、不含第一间两段，取较大值；单间房特判。

```python
def rob(nums: list[int]) -> int:
    def rob_line(houses: list[int]) -> int:     # 直线版：dp[i] = max(dp[i-1], dp[i-2] + houses[i])
        skip, take = 0, 0                       # skip：前一间不偷的最优；take：偷到前一间为止的最优
        for money in houses:
            skip, take = take, max(take, skip + money)
        return take

    if len(nums) == 1:                          # 只有一间：首尾是同一间，不能切成两段
        return nums[0]
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))   # 不偷最后一间 / 不偷第一间
```

**运行。** `[2,3,2]` → `3`；`[1,2,3,1]` → `4`；`[1,2,3]` → `3`；`[5]` → `5`；`[1,2]` → `2`；`[2,1,1,2]` → `3`。

**复杂度。** 时间 `O(n)`，两次线性扫描；空间 `O(n)`，来自两次切片（扫描本身 `O(1)`）。

**写法要点。** 嵌套函数 `rob_line` 共用一份逻辑，调用两次；`skip, take = take, max(take, skip + money)` 用元组赋值同时更新两个状态，右侧先整体求值，不会用到被覆盖的旧值；`nums[:-1]` 和 `nums[1:]` 是切片拷贝，`n <= 100` 时无所谓，要省空间就传下标区间。
