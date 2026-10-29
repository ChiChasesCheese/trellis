---
id: tlc-house-robber-ii-4-followup
node: b.house-robber-ii
type: qa
step: 4
---
## Q
**LC 213 打家劫舍 II**｜追问

面试官接着问：（1）要返回具体偷了哪几间房，而不只是金额？（2）房屋改成二叉树（LC 337），思路怎么变？（3）切片会拷贝数组，能做到额外空间 `O(1)` 吗？

## A
1. **返回方案。** 直线版保留整张 `dp` 表，`best[k]` 表示前 `k` 间的最优，再从后往前回溯；两条直线各回溯一次，取总额更大的那条。

```python
def rob_with_houses(nums: list[int]) -> tuple[int, list[int]]:
    def line(lo: int, hi: int) -> tuple[int, list[int]]:       # 只考虑下标区间 [lo, hi)
        m = hi - lo
        best = [0] * (m + 1)                                   # best[k]：前 k 间的最优金额
        for k in range(1, m + 1):
            best[k] = max(best[k - 1], (best[k - 2] if k > 1 else 0) + nums[lo + k - 1])
        picked: list[int] = []
        k = m
        while k > 0:                                           # 回溯：相等说明第 k 间没偷
            if best[k] == best[k - 1]:
                k -= 1
            else:
                picked.append(lo + k - 1)
                k -= 2
        return best[m], picked[::-1]

    if len(nums) == 1:
        return nums[0], [0]
    return max(line(0, len(nums) - 1), line(1, len(nums)))     # 元组比较：先比金额
```

2. **树形。** 状态仍是「偷 / 不偷」，但约束沿树边传递：`take[v] = v.val + skip[左] + skip[右]`，`skip[v] = max(take, skip)[左] + max(take, skip)[右]`，自底向上一遍。
3. **`O(1)` 空间。** 把直线版写成 `rob_range(nums, lo, hi)`，在下标区间上滚动两个变量，调用 `rob_range(nums, 0, n - 1)` 和 `rob_range(nums, 1, n)`，不再切片。

**Python 提醒**：`nums[:-1]` 与 `nums[1:]` 都是新列表（浅拷贝，`O(n)`）；`max` 比较两个 `(金额, 方案)` 元组时先比金额，金额相同才会去比较列表，不会出错但要知道发生了什么。
