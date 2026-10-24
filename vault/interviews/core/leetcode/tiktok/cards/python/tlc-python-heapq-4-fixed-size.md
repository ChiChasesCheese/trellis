---
id: tlc-python-heapq-4-fixed-size
node: python.heapq
type: qa
step: 4
---
## Q
**Python 工具箱｜定长堆与 `heappushpop` / `heapreplace`**

数据流或超大输入里求第 `k` 大，为什么用「大小为 `k` 的最小堆」？`heappushpop` 和 `heapreplace` 区别是什么？

## A
求第 `k` 大，堆里只保留当前最大的 `k` 个，用**最小堆**，堆顶就是这 `k` 个里最小的，也就是第 `k` 大。新元素只要比堆顶大，就替掉堆顶。

```python
import heapq
def kth_largest(nums: list[int], k: int) -> int:
    h: list[int] = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        else:
            heapq.heappushpop(h, x)   # 先 push 再 pop，只做一次 O(log k)
    return h[0]
print(kth_largest([3, 2, 1, 5, 6, 4], 2))   # 5
```

- `heappushpop(h, x)`：先放入 `x` 再弹出最小值，返回弹出值。`x` 比堆顶还小时，直接返回 `x`，堆不动。
- `heapreplace(h, x)`：先弹出最小值再放入 `x`，返回**旧**堆顶；堆空时报 `IndexError`，且 `x` 可能比旧堆顶还小。
- 对比：`heappush` 之后再 `heappop` 是两次 `O(log k)`，`heappushpop` 一次；写法也更短。
- 时间 `O(n log k)`，空间 `O(k)`：`n` 很大或输入是流时，这是唯一不用把全部数据存下来的做法。
- 反方向（第 `k` 小）：存负数做最大堆，规则相同。

**坑**：想要「前 `k` 大」按从大到小输出，堆里不是有序的，最后要 `sorted(h, reverse=True)`。
