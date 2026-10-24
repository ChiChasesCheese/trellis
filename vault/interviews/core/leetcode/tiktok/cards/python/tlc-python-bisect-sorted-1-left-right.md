---
id: tlc-python-bisect-sorted-1-left-right
node: python.bisect-sorted
type: qa
step: 1
---
## Q
**Python 工具箱｜`bisect_left` 与 `bisect_right`**

在有序列表 `[1, 2, 2, 2, 5, 8]` 里，`bisect_left(a, 2)` 和 `bisect_right(a, 2)` 各返回什么？这两个函数的语义怎样一句话记住？

## A
两者返回的都是**插入点**（insertion point）：把 `x` 插到这个下标，列表仍有序。区别只在遇到相等元素时插在它们的左边还是右边。

```python
from bisect import bisect_left, bisect_right
a = [1, 2, 2, 2, 5, 8]
print(bisect_left(a, 2), bisect_right(a, 2))    # 1 4
print(bisect_left(a, 3), bisect_right(a, 3))    # 4 4：值不存在时两者相同
print(bisect_left(a, 0), bisect_left(a, 9))     # 0 6：越界时返回 0 或 len(a)
print(bisect_right(a, 2) - bisect_left(a, 2))   # 3：x 出现的次数
```

- `bisect_left(a, x)` = 第一个 `>= x` 的下标（即 `<x` 的元素个数）。
- `bisect_right(a, x)`（别名 `bisect`）= 第一个 `> x` 的下标（即 `<=x` 的元素个数）。
- 复杂度 `O(log n)`；比较只用 `<`，所以 `a` 必须已按升序排好，否则结果没有意义，且不会报错。
- 返回值可能是 `len(a)`，用它取元素前必须先判断 `i < len(a)`。
- 适用：有序数组的边界查询（LC 34）、统计区间内元素个数、LIS 的 `tails` 数组（LC 300）。

**坑**：对降序列表直接用 `bisect` 得到错误结果；降序时取负存，或自己写二分。
