---
slug: last-stone-weight
---
## Q
**LC 1046 最后一块石头的重量**｜Easy

每回合取最重的两块 `y >= x` 对撞：相等则都消失，否则剩下 `y - x`。求最后剩下那块的重量，没有则为 `0`。

## A
**一句话。** 用大根堆反复取出最重的两块，差值非零就放回去。

```python
def last_stone_weight(stones):
    heap = [-s for s in stones]   # heapq 是小根堆，取负当大根堆
    heapify(heap)
    while len(heap) > 1:
        y = -heappop(heap)        # 最重
        x = -heappop(heap)        # 次重
        if y != x:
            heappush(heap, -(y - x))
    return -heap[0] if heap else 0
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 忘记取负：取到最轻的两块，`[2,7,4,1,8,1]` 得 `3`，应为 `1`。
- 直接返回 `-heap[0]`：`[3,3]` 全粉碎后堆空，抛 `IndexError`。

**追问。**
- 为什么不每轮排序？：每轮排序 `O(n log n)`，共 `n` 轮是 `O(n² log n)`；堆每轮 `O(log n)`。
- 石头重量范围小（`<=1000`）怎么优化？：用桶计数从大到小扫，免去堆。

**同模式。** LC 703 数据流中的第 K 大元素、LC 215 数组中的第 K 个最大元素、LC 295 数据流的中位数、LC 1962 移除石子使总数最小
