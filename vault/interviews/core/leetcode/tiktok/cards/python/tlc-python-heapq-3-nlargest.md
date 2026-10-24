---
id: tlc-python-heapq-3-nlargest
node: python.heapq
type: qa
step: 3
---
## Q
**Python 工具箱｜`nlargest` / `nsmallest`**

求前 `k` 大怎样一行写出？它的 `key` 参数怎么用？什么时候不该用它，而该用 `sorted` 或快速选择（quickselect）？

## A
`heapq.nlargest(k, iterable, key=None)` 返回从大到小的前 `k` 个；`nsmallest` 同理，返回从小到大。

```python
import heapq
from collections import Counter
c = Counter(["a", "bb", "a", "ccc", "bb", "a"])
print(heapq.nlargest(2, c, key=c.get))                      # ['a', 'bb']：按次数取前 2 个键
print(heapq.nsmallest(2, [(3, "x"), (1, "y"), (2, "z")]))   # [(1, 'y'), (2, 'z')]
```

复杂度（`n` 个元素）：

| 情况 | 做法 | 时间 |
|---|---|---|
| `k` 很小 | 大小为 `k` 的堆 | `O(n log k)`，空间 `O(k)` |
| `k` 接近 `n` | `sorted(...)[:k]` | `O(n log n)` |
| 只要第 `k` 个，不要顺序 | quickselect | 平均 `O(n)`，最坏 `O(n^2)` |

- 实现里 `k == 1` 直接走 `min` / `max`；`k` 接近 `n` 时库内部会自己改用排序，所以不用手动判断。
- LC 347 前 K 个高频元素：`heapq.nlargest(k, count, key=count.get)`；LC 215 第 K 大：`heapq.nlargest(k, nums)[-1]`。
- **坑**：每次调用都重新扫描整个输入；数据在不断追加、要随时回答时，自己维护一个定长大小为 `k` 的堆，每来一个数 `heappushpop`。
