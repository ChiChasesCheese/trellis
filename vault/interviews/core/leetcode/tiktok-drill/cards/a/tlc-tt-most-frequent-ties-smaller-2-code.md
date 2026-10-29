---
id: tlc-tt-most-frequent-ties-smaller-2-code
node: a.tt-most-frequent-ties-smaller
type: qa
step: 2
---
## Q
**出现次数最多的元素（并列取较小的）**｜写出 Python 实现

整数数组 `nums`（长度至多 `10^5`，值在 `±10^9`），返回出现次数最多的元素，并列时返回数值最小的。要求 `O(n)`。

## A
**思路。** `Counter` 一遍计数；对所有不同值用复合键 `(-次数, 数值)` 取最小：次数越多键越小，次数相同时数值小的键小。

```python
from collections import Counter


def most_frequent(nums: list[int]) -> int:
    count = Counter(nums)
    # 复合键：次数大的优先（取负），次数相同取数值小的
    return min(count, key=lambda x: (-count[x], x))
```

运行：`[3,1,3,1,2]` → `1`；`[7]` → `7`；`[-5,-5,2,2]` → `-5`；`[4,4,1]` → `4`。

**复杂度。** 时间 `O(n)`：计数一遍，`min` 遍历 `k` 个不同值；空间 `O(k)`。

**写法要点。** 元组按字典序比较，先比第一项再比第二项，一个 `key` 表达多级规则；对数值类取负把「最大」转成「最小」，避免写两次比较；遍历 `Counter` 本身就是遍历不同的键；`most_common` 并列时按首次出现顺序，不符合「取最小」，不要用它。
