---
id: tlc-python-collections-1-counter
node: python.collections
type: qa
step: 1
---
## Q
**Python 工具箱｜`collections.Counter`**

刷题里统计字符或数字出现次数、取出现最多的前几个，`Counter` 比手写字典好在哪？它的构造、`most_common`、读取缺失键各自的行为和复杂度是什么？

## A
`Counter` 是 `dict` 的子类，键是元素，值是次数；构造时遍历一次可迭代对象，`O(n)`。

```python
from collections import Counter
c = Counter("abracadabra")
print(c.most_common(2))          # [('a', 5), ('b', 2)]
print(c["z"], "z" in c, len(c))  # 0 False 5：读缺失键返回 0，且不会插入
```

- `most_common(k)` 内部用堆，`O(m log k)`（`m` 是不同元素个数）；不传 `k` 则完整排序，`O(m log m)`。
- 读缺失键得 `0`，不抛 `KeyError`，也**不插入**这个键，所以 `c[x] += 1` 可以直接写，不用先判断。
- `Counter.total()`（3.10+）返回所有次数之和，等于 `sum(c.values())`。
- 适用题型：找出现最多的元素（LC 347 前 K 个高频元素）、判断异位词（LC 242、438）、窗口里的字符计数（LC 76）。

**坑**：`len(c)` 是不同元素个数，不是总次数；次数减到 `0` 的键仍留在里面，用 `len(c)` 表示「窗口里有几种字符」时要 `del c[k]`。
