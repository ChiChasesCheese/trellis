---
id: tlc-tops-contains-duplicate-0-whole
node: arrays-hashing.contains-duplicate
type: qa
---
## Q
**LC 217 存在重复元素（Contains Duplicate）**｜Easy · 全公司热度第 120 名 · Blind 75、NeetCode 150

给你一个整数数组 `nums`。如果任一值在数组中出现至少两次，返回 `true`；如果数组中每个元素互不相同，返回 `false`。`1 <= nums.length <= 10^5`，`-10^9 <= nums[i] <= 10^9`。例：`nums = [1,2,3,1]` → `true`；`nums = [1,2,3,4]` → `false`；`nums = [1,1,1,3,3,4,3,2,4,2]` → `true`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 哈希集合（hash set）判重。

**一句话。** 边扫边把元素放进集合，遇到已经在集合里的就是重复。

**识别。** 「是否出现过」是成员判断，哈希集合 `O(1)`。`n = 10^5` 要求 `O(n)` 或 `O(n log n)`，`O(n^2)` 两两比较不行。

**推导。** 两两比较 `O(n^2)`，`10^5` 时约 `5 * 10^9` 次比较，超时。排序后重复值必然相邻，`O(n log n)`；哈希集合把每次判断降到 `O(1)`，总共 `O(n)`，代价是 `O(n)` 额外空间。

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()
    for x in nums:
        if x in seen:              # 见过：已经有重复，不必扫完
            return True
        seen.add(x)
    return False
```

运行：`[1,2,3,1]` → `True`，`[1,2,3,4]` → `False`，`[1,1,1,3,3,4,3,2,4,2]` → `True`，`[7]` → `False`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 空间要求 `O(1)`：原地排序后检查相邻元素，时间 `O(n log n)`。

```python
from itertools import pairwise


def contains_duplicate_sorted(nums: list[int]) -> bool:
    nums.sort()                                          # 原地排序，额外空间 O(1)
    return any(a == b for a, b in pairwise(nums))        # 重复值排序后必然相邻
```

- 两次出现的下标差不超过 `k`（LC 219）：用字典记最近下标，或维护大小为 `k` 的滑动窗口集合；差值不超过 `t`（LC 220）要用有序结构或桶。

**易错点。**
- 先 `seen.add(x)` 再判断 `x in seen`：第一个元素就会被判成重复，`[1,2,3,4]` 错成 `True`。
- 排序后只比较首尾或隔一个比较：`[1,2,2,3]` 的重复在中间相邻处，必须比较每一对相邻元素。

**同模式。** LC 1 两数之和、LC 242 有效的字母异位词、LC 219 存在重复元素 II、LC 220 存在重复元素 III。
