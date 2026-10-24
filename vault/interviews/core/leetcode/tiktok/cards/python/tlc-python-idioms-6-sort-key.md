---
id: tlc-python-idioms-6-sort-key
node: python.idioms
type: qa
step: 6
---
## Q
**Python 工具箱｜`sorted` 的 `key` 与稳定性**

按「次数降序、字典序升序」排序怎样写？排序为什么是稳定的，这有什么用？按字符串排序和按数值排序有什么区别？

## A
`sorted(iterable, key=f, reverse=False)` 返回新列表；`list.sort()` 原地排序。时间 `O(n log n)`，用的是 Timsort，**稳定**：键相同的元素保持原来的相对顺序。

```python
words = [("b", 2), ("a", 2), ("c", 5)]
print(sorted(words, key=lambda w: (-w[1], w[0])))   # [('c',5),('a',2),('b',2)]：次数降序、名字升序
from operator import itemgetter
print(sorted(words, key=itemgetter(1), reverse=True))   # [('c',5),('b',2),('a',2)]：次数相同保持原顺序
print(sorted(["Bb", "a", "C"], key=str.lower))      # ['a', 'Bb', 'C']
print(sorted(["10", "9", "1"]), sorted(["10", "9", "1"], key=int))
# ['1', '10', '9'] ['1', '9', '10']：字符串按字典序，数值要转 int
```

- 键是**元组**时逐项比较；数值项取负可实现混合升降序（字符串项取不了负）。
- 稳定性的用途：先按次要键排序，再按主要键排序，得到多级排序；`reverse=True` 也保持相等元素的原顺序。
- `reverse=True` 比「排序后 `[::-1]`」更好，因为后者会把相等元素的顺序也反过来。
- 常见题型：区间按左端点排序（LC 56、252）、按右端点排序（贪心）、按 `key=lambda x: x[0]` 取元组第一项；LC 179 要用 `cmp_to_key`。
- **坑**：`key` 函数对每个元素只调用一次；`sort` 不返回值，`nums = nums.sort()` 会得到 `None`。
