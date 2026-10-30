---
id: tlc-find-the-duplicate-number-2-code
node: p4.find-the-duplicate-number
type: qa
step: 2
---
## Q
**LC 287 寻找重复数**｜写出 Python 实现

数组 `nums` 有 `n + 1` 个整数，每个都在 `[1, n]`（`1 <= n <= 10^5`），恰有一个值重复出现（可能出现多次）。返回这个重复的数，不修改数组，额外空间 `O(1)`，时间 `O(n)`。

## A
**思路。** 把 `i → nums[i]` 当作链表的"下一个"指针。阶段一：`slow` 每次走一步、`fast` 每次走两步，从下标 `0` 出发，直到在环内相遇。阶段二：`slow` 回到 `0`，两个指针每次都只走一步，再次相遇的位置就是环的入口，也就是重复的数。

```python
def find_duplicate(nums: list[int]) -> int:
    slow = fast = 0                        # 把 i -> nums[i] 看成链表；0 没有入边（值在 1..n），一定在链上而不在环里
    while True:                            # 阶段一：快慢指针在环内相遇
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0                               # 阶段二：一个回到起点，两个都每次走一步，相遇点就是环的入口
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow                            # 环的入口有两条入边，即重复的数
```

运行：`[1,3,4,2,2]` → `2`，`[3,1,3,4,2]` → `3`，`[3,3,3,3,3]` → `3`，`[1,1]` → `1`，`[2,2,2]` → `2`；`n = 10^5` 的数组约 `0.003` 秒；调用之后数组没有变化。

**复杂度。** 时间 `O(n)`；空间 `O(1)`，两个整数指针。

**写法要点。** `while True` 加 `break` 模拟"先走再比"的 do-while（Python 没有 do-while），因为起点 `slow == fast == 0` 时不能一开始就判相等；`slow`、`fast` 是**下标**，`nums[slow]` 是"下一个下标"；起点选 `0` 是因为值域 `[1, n]` 保证没有任何元素指向 `0`，`0` 在环外；返回的 `slow` 既是入口下标，也是被两个位置指向的值，即重复数。
