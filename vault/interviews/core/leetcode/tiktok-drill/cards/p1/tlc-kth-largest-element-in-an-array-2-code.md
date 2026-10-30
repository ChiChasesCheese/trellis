---
id: tlc-kth-largest-element-in-an-array-2-code
node: p1.kth-largest-element-in-an-array
type: qa
step: 2
---
## Q
**LC 215 数组中的第 K 个最大元素**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `10^5`，元素在 `[-10^4, 10^4]`）和 `1 <= k <= nums.length`，返回排序后的第 `k` 个最大元素（重复值各算一个），要求期望 `O(n)`。

## A
**思路。** 随机选 pivot，把数组分成「大于 pivot」「等于 pivot」「小于 pivot」三段。答案在哪一段由 `k` 和各段大小决定：在大于段就丢掉其余、继续；落在等于段就直接返回 pivot；在小于段就先从 `k` 里减去前两段的个数，再继续。

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 答案在比 pivot 大的那一堆里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在 pivot 自己这一段
            return pivot
        else:                                      # 答案在比 pivot 小的那一堆里
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

运行：`([3,2,1,5,6,4], 2)` → `5`，`([3,2,3,1,2,4,5,5,6], 4)` → `4`，`([7], 1)` → `7`，`([2,2,2], 3)` → `2`。

**复杂度。** 期望时间 `O(n)`：每轮扫三次（两次推导加一次 `count`）常数倍 `n`，每轮期望把规模减半；空间 `O(n)`：每轮的子列表。

**写法要点。** `random.choice` 随机 pivot，避免有序输入退化；`nums.count(pivot)` 用 C 循环统计相等段，不必建列表；`nums = bigger` 只是重新绑定局部变量，不会修改调用方的列表；`while True` 加三个出口分支，比递归少一层调用栈。求第 `k` 大时「大于」堆放前面，所以 `k <= len(bigger)` 就在大堆里找。
