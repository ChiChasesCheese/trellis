---
id: tlc-python-bisect-sorted-4-insort
node: python.bisect-sorted
type: qa
step: 4
---
## Q
**Python 工具箱｜`insort` 与有序列表的真实代价**

`bisect.insort` 能让列表始终有序，它的复杂度是多少？什么时候够用，什么时候该换别的结构？

## A
`insort(a, x)` = 二分找位置 `O(log n)` + `list.insert` 搬移元素 `O(n)`，合计 `O(n)`。

```python
from bisect import insort, insort_left, insort_right
l = [1, 4, 9]
insort(l, 4); print(l)         # [1, 4, 4, 9]
insort_left(l, 4); print(l)    # [1, 4, 4, 4, 9]：插在相等元素左边
insort_right(l, 4); print(l)   # [1, 4, 4, 4, 4, 9]：插在相等元素右边，insort 即此
```

- 搬移是 C 层的内存拷贝，`n <= 10^5` 时一次插入只要几十微秒，`10^5` 次插入总计通常能过；`n` 到 `10^6` 以上就会明显超时。
- 删除同理：`i = bisect_left(a, x); del a[i]` 是 `O(n)`。
- 需要大量增删加查「第 k 个」「前驱 / 后继」时，选 `sortedcontainers.SortedList`，或自己写平衡树 / 树状数组 / 分块。
- 典型用法：LC 295 数据流中位数的简版（保持有序，取中间项）、在线统计「已插入元素里有多少个比我小」。

**坑**：`insort` 只管插入，不检查列表是否本来有序；`key` 参数从 3.10 起可用，但 `insort` 的 `key` 只用于比较，插入的仍是原对象。
