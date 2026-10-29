---
id: tlc-third-maximum-number-4-followup
node: a.third-maximum-number
type: qa
step: 4
---
## Q
**LC 414 第三大的数**｜追问

面试官接着问：（1）改成第 `k` 大的不同值（`k` 可能到几千），不存在时返回最大值？（2）数据是一个流，随时要能回答当前的第三大？（3）写出不用列表、只用三个变量的版本。

## A
1. **第 `k` 大不同值**：大小为 `k` 的最小堆，堆顶是当前第 `k` 名；再配一个集合记录堆里有哪些值，用于去重。新值大于堆顶时用 `heapreplace` 替换堆顶，并同步更新集合。

```python
import heapq


def kth_distinct_max(nums: list[int], k: int) -> int:
    heap: list[int] = []                       # 当前最大的至多 k 个不同值，堆顶是其中最小的
    members: set[int] = set()
    for x in nums:
        if x in members:
            continue
        if len(heap) < k:
            heapq.heappush(heap, x)
            members.add(x)
        elif x > heap[0]:
            members.discard(heapq.heapreplace(heap, x))   # 弹出旧第 k 名、压入 x，一步完成
            members.add(x)
    return heap[0] if len(heap) == k else max(heap)
```

运行：`[2,2,3,1], k = 3` → `1`，`[1,2], k = 3` → `2`，`[5,3,9,3,7], k = 2` → `7`。时间 `O(n log k)`，空间 `O(k)`。
2. **数据流**：同一个堆加集合常驻内存，每来一个数做一次上面的循环体，查询是 `O(1)` 看堆顶（不足 `k` 个时需要最大值，可另存一个变量）。
3. **三变量**：初值都设 `None`；`x` 等于其中之一就跳过；`x > first`（或 `first is None`）时 `first, second, third = x, first, second`；否则同理比 `second`、`third`。元组赋值一次完成「下移」，不会出现先覆盖再读取的顺序错误。

**Python 提醒**：`heapq.heapreplace` 先弹后压，`heapq.heappushpop` 先压后弹；前者在新值比堆顶小时也会把它压进去，所以要先判断 `x > heap[0]`。
