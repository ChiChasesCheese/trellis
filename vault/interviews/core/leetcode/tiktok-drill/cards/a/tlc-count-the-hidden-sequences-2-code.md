---
id: tlc-count-the-hidden-sequences-2-code
node: a.count-the-hidden-sequences
type: qa
step: 2
---
## Q
**LC 2145 统计隐藏数组数目**｜写出 Python 实现

整数列表 `differences`（长 `n`，`1 <= n <= 10^5`，每项在 `[-10^5, 10^5]`）是长为 `n + 1` 的隐藏数组的相邻差，`lower`、`upper`（`-10^5 <= lower <= upper <= 10^5`）是隐藏数组所有元素的取值闭区间。返回可能的隐藏数组个数。

## A
**思路。** 前缀和 `prefix`（开头补 `0`）给出数组相对起点的偏移；跨度 `max(prefix) - min(prefix)` 固定；起点的取值个数是区间长度减去跨度再加一，最小为 `0`。

```python
from itertools import accumulate


def number_of_arrays(differences: list[int], lower: int, upper: int) -> int:
    prefix = [0, *accumulate(differences)]     # hidden[i] = hidden[0] + prefix[i]，别漏掉开头的 0
    spread = max(prefix) - min(prefix)         # 数组内最大值与最小值之差，由 differences 唯一确定
    return max(0, (upper - lower) - spread + 1)   # 起点 hidden[0] 在区间内能平移多少个位置
```

运行：`([1,-3,4], 1, 6)` → `2`，`([3,-4,5,1,-2], -4, 5)` → `4`，`([4,-7,2], 3, 6)` → `0`，`([1,2], 1, 3)` → `0`，`([0], 5, 5)` → `1`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（前缀和列表）。

**写法要点。** `itertools.accumulate` 生成前缀和迭代器，默认做加法；`[0, *accumulate(...)]` 用星号解包在开头补 `0`，一行搞定“偏移从 `0` 开始”。`max` 和 `min` 各扫一遍 `prefix`，没有必要手写循环。`max(0, ...)` 收口“区间太窄放不下”的情况。整个函数没有循环语句，却是 `O(n)`。
