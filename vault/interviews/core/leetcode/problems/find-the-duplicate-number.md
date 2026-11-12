---
slug: find-the-duplicate-number
---
## Q
**LC 287 寻找重复数**｜Medium

`n+1` 个数都在 `[1, n]` 内，恰有一个重复数。不修改数组、只用 `O(1)` 空间，找出它。

## A
**一句话。** 把 `i → nums[i]` 当链表，重复数就是环的入口，用快慢指针（Floyd）找入口。

```python
def find_duplicate(nums):
    slow = fast = 0
    while True:                  # 阶段一：在环内相遇
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0                     # 阶段二：同速走，入口处会合
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 把第一阶段的相遇点当答案：`[1,3,4,2,2]` 相遇在 `4`，重复数是 `2`，必须有第二阶段。
- 二分时统计「值 `== mid`」的个数：不单调，要统计「值 `<= mid`」的个数。

**追问。**
- 为什么 `0` 一定不在环上？：值域是 `[1, n]`，没有任何下标指向 `0`。
- 重复数出现多次（`[3,3,3,3,3]`）还成立吗？：成立，环入口只看入边数，不看重复次数。

**同模式。** LC 142 环形链表 II、LC 141 环形链表、LC 202 快乐数、LC 41 缺失的第一个正数
