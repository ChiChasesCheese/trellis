---
id: tlc-patterns-dp-linear-2-template
node: patterns.dp-linear
type: qa
step: 2
---
## Q
**动态规划：线性与状态机｜模板：爬楼梯、打家劫舍、最大子数组和**

写出这三道最基础的线性 DP，说明各自的状态定义和滚动变量。

## A
```python
def climb_stairs(n: int) -> int:
    a, b = 1, 1                            # f(0) = f(1) = 1
    for _ in range(n - 1):
        a, b = b, a + b                    # f(i) = f(i-1) + f(i-2)
    return b

def rob(nums: list[int]) -> int:
    take = skip = 0                        # take：偷到当前；skip：不偷当前
    for x in nums:
        take, skip = skip + x, max(take, skip)   # 偷当前，则前一个必须没偷
    return max(take, skip)

def max_sub_array(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)              # 以 x 结尾的最大和：接在前面，或自己重新开始
        best = max(best, cur)
    return best
```

运行：`[climb_stairs(n) for n in 1..8]` → `[1,2,3,5,8,13,21,34]`，`climb_stairs(45)` → `1836311903`；`rob([1,2,3,1])` → `4`，`rob([2,7,9,3,1])` → `12`；`max_sub_array([-2,1,-3,4,-1,2,1,-5,4])` → `6`，`max_sub_array([-3,-1,-2])` → `-1`。

| 题 | 状态 | 转移 |
|---|---|---|
| 爬楼梯 | `f(i)`：爬到第 `i` 阶的方法数 | `f(i-1) + f(i-2)` |
| 打家劫舍 | `take / skip` | `take' = skip + x`，`skip' = max(take, skip)` |
| 最大子数组和（Kadane） | `cur`：以当前元素结尾的最大和 | `max(x, cur + x)` |

三者时间 `O(n)`、空间 `O(1)`。`take, skip = skip + x, max(take, skip)` 一行同时更新，右边都用旧值。
