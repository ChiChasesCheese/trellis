---
id: tlc-python-itertools-functools-1-accumulate
node: python.itertools-functools
type: qa
step: 1
---
## Q
**Python 工具箱｜`itertools.accumulate`**

前缀和、前缀最大值怎样用 `accumulate` 一行得到？`initial=0` 解决什么问题？

## A
`accumulate(iterable, func=operator.add, *, initial=None)` 返回惰性迭代器，第 `i` 项是前 `i+1` 项按 `func` 折叠的结果，`O(n)`。

```python
from itertools import accumulate
import operator
nums = [3, 1, 4, 1, 5]
print(list(accumulate(nums)))                  # [3, 4, 8, 9, 14]
print(list(accumulate(nums, initial=0)))       # [0, 3, 4, 8, 9, 14]：多一个开头的 0
print(list(accumulate(nums, max)))             # [3, 3, 4, 4, 5]：前缀最大值
print(list(accumulate(nums, operator.mul)))    # [3, 3, 12, 12, 60]：前缀积
pre = list(accumulate(nums, initial=0))
print(pre[4] - pre[1])                         # 6：nums[1:4] 的和 = pre[右端] - pre[左端]
```

- `initial=0`（3.8+）让 `pre` 长度是 `n+1`，且 `pre[0] = 0`，区间 `[l, r)` 的和永远是 `pre[r] - pre[l]`，不用对 `l = 0` 单独判断。
- 前缀最大 / 最小（`accumulate(h, max)`）是接雨水（LC 42）的 DP 版需要的左右最高墙：左边 `left = list(accumulate(h, max))`，右边 `right = list(accumulate(reversed(h), max))[::-1]`。
- 前缀异或：`accumulate(nums, operator.xor)`。
- 返回的是迭代器，要多次使用必须 `list(...)`。

适用：LC 560、974 的前缀和 + 哈希；LC 303 区域和检索；LC 528 带权随机（配 `bisect`）。
