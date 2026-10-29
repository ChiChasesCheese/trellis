---
id: tlc-remove-zero-sum-consecutive-nodes-from-linked-list-4-followup
node: a.remove-zero-sum-consecutive-nodes-from-linked-list
type: qa
step: 4
---
## Q
**LC 1171 从链表中删去总和值为零的连续节点**｜追问

面试官接着问：（1）数组版本：求和为 `K` 的连续子数组个数？（2）能不能只扫一遍？（3）答案不唯一，这个解法返回的是哪一个？

## A
1. **数组版（LC 560）。** 一遍扫描，哈希表记「前缀和 → 出现次数」，到每个位置累加 `count[前缀和 - K]`：

```python
from collections import Counter


def subarray_sum(nums: list[int], k: int) -> int:
    seen: Counter[int] = Counter({0: 1})        # 空前缀的和是 0
    s = ans = 0
    for x in nums:
        s += x
        ans += seen[s - k]                      # 之前有多少个前缀和等于 s - k
        seen[s] += 1
    return ans
```

2. **一遍扫描。** 用栈保存节点，并用字典记录「前缀和 → 栈中位置」；遇到重复前缀和就把栈里这一段弹出，同时清掉字典里被弹出节点的记录。写法比两遍扫描复杂，常数更小，复杂度同为 `O(n)`。
3. **返回的是哪一个。** 每个节点都跳到同前缀和的最远处，等价于「从最靠左的起点出发，删掉最长的零和段，再对剩下的链表重复」。`[1,2,-3,3,1]` 因此得到 `[3,1]` 而不是同样合法的 `[1,2,1]`。

**Python 提醒**：`Counter` 读取不存在的键返回 `0` 且不会插入，所以 `seen[s - k]` 可以直接累加；若换成 `dict`，要用 `seen.get(s - k, 0)`。
