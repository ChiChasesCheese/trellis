---
id: tlc-python-bisect-sorted-7-sortedlist
node: python.bisect-sorted
type: qa
step: 7
---
## Q
**Python 工具箱｜`sortedcontainers.SortedList`**

需要边插入、边删除、边查前驱后继（Python 没有内置平衡树）时，`SortedList` 提供什么？复杂度如何？面试里能不能用？

## A
`SortedList` 是第三方库 `sortedcontainers` 的类，内部是「分块的有序列表」，增删查约 `O(log n)`，实际常数很小。

```python
# usage：需要第三方库 sortedcontainers
from sortedcontainers import SortedList
sl = SortedList([5, 1, 3])
sl.add(4)
print(sl, sl[0], sl[-1], sl.bisect_left(4))   # SortedList([1, 3, 4, 5]) 1 5 2
sl.remove(3); print(sl, list(sl.irange(2, 5)))   # SortedList([1, 4, 5]) [4, 5]
sl.discard(99)                                  # 不存在时不报错
print(sl.pop(0), sl)                            # 1 SortedList([4, 5])
```

- `add`、`remove`、`discard`、`bisect_left/right`、`index`、`count`、`sl[i]`、`pop(i)`、`irange(lo, hi)` 都是 `O(log n)` 量级；构造 `SortedList(iterable)` 是 `O(n log n)`。
- 一个对象同时回答「第 `k` 小」「某值的前驱 / 后继」「区间内元素」：LC 220 存在重复元素 III、LC 480 滑动窗口中位数、LC 729 我的日程安排表 I。
- `remove(x)` 在 `x` 不存在时抛 `ValueError`，用 `discard` 更稳妥。
- **能不能用**：LeetCode 的 Python 环境自带这个库；面试用的在线编辑器未必有。先问一句「能不能用 `sortedcontainers`」，否则退回 `bisect` + `list`（`O(n)` 插入）或改用堆加懒删除。

**坑**：键必须可比较且比较不能随元素变化；元素是可变对象并改了排序依据，会破坏有序性。
