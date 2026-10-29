---
id: tlc-majority-element-ii-2-code
node: a.majority-element-ii
type: qa
step: 2
---
## Q
**LC 229 求众数 II**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `5 * 10^4`，元素在 `[-10^9, 10^9]`），返回所有出现次数超过 `⌊n / 3⌋` 的元素，`O(n)` 时间。

## A
**思路。** 一遍 `Counter` 数出每个值的次数，留下次数严格大于 `len(nums) // 3` 的值。由鸽巢原理，结果至多 2 个。

```python
from collections import Counter


def majority_element(nums: list[int]) -> list[int]:
    limit = len(nums) // 3                  # 出现次数必须严格大于它
    return [x for x, c in Counter(nums).items() if c > limit]
```

运行：`[3,2,3]` → `[3]`，`[1]` → `[1]`，`[1,2]` → `[1, 2]`，`[1,2,3]` → `[]`，`[2,2,1,1,1,2,2]` → `[2, 1]`。

**复杂度。** 时间 `O(n)`：建 `Counter` 一遍，筛选扫一遍不同的值；空间 `O(m)`，`m` 为不同值的个数，最坏 `O(n)`。

**写法要点。** `Counter(nums)` 一行完成计数，`.items()` 同时拿到值和次数；阈值先算好存进 `limit`，不在推导式里反复求 `len`；用整数除法 `//` 和严格大于号，与「超过 `⌊n / 3⌋`」逐字对应；`Counter` 按首次出现顺序迭代，结果顺序稳定。
