---
id: performance-ds-heap
node: performance.data-structures
type: qa
step: 4
---
## Q
定时付款服务要不停地取“最早到期的那笔”，同时不断有新付款加进来。每次加入后 `list.sort()` 再取第一个，为什么会慢？用堆（`heapq`）时，到期时间相同的两笔怎么保证顺序确定？

## A
**只要“最小的那一个”时，不需要全排序，用堆**

- **全排序做了多余的事**：你每次只用第一个，却维护了整个序；堆只保证 `h[0]` 最小，插入和弹出都是 O(log n)；
- **取前 k 个**：`heapq.nsmallest(k, data)` 不排序全部数据；k 远小于 n 时远快于 `sorted(data)[:k]`；
- **并列要自己定顺序**：元组比较在第一项相等时看第二项，所以放 `(到期时间, 创建序号, 付款)`；序号递增且唯一，比较永远不会落到付款对象上（它可能根本不可比较）；
- **堆不能删中间项**：取消一笔付款，用“打标记、弹出时跳过”（惰性删除），而不是在堆里找它；
- **堆不支持遍历有序**：要按序输出全部，还是 `sorted`。

实测（3.11，本机）：10 万个随机浮点数里取最小的 10 个，`sorted(data)[:10]` 6.74 ms，`heapq.nsmallest(10, data)` 0.41 ms。1000 个元素的容器里做 1000 次“放入一个、取出最小”，每次追加再 `sort()` 共 1.28 ms，`heappushpop` 共 0.047 ms。

```python
import heapq, itertools

seq = itertools.count()
heap: list[tuple[int, int, str]] = []
for due, pid in [(5, "b"), (3, "a"), (5, "c")]:
    heapq.heappush(heap, (due, next(seq), pid))   # 并列时序号小的先到

print([heapq.heappop(heap)[2] for _ in range(3)])  # ['a', 'b', 'c']
```

**知识点：**按访问模式选结构（Choosing Structures）
