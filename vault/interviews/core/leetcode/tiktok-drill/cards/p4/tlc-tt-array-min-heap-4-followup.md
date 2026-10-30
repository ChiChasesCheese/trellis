---
id: tlc-tt-array-min-heap-4-followup
node: p4.tt-array-min-heap
type: qa
step: 4
---
## Q
**手写最小堆**｜追问

`MinHeap` 写完后，面试官接着问：（1）用它实现课程表：有多门课可选时总是先上编号最小的课，输出字典序最小的上课顺序，有环返回空列表（`n <= 10^5`，先修关系至多 `10^5` 条）？（2）要最大堆、或者元素带优先级怎么办？（3）从 `n` 个数里取最小的 `k` 个，怎么用堆？

## A
1. **字典序最小的拓扑排序。** 思路：普通 Kahn 算法用队列装“入度为 0 的课”，顺序是先来先上；换成最小堆，每次弹出的就是当前可上的课里编号最小的。贪心成立，因为每一步选最小的可选课，后面可选的课集合只增不减，不会让更小的课被推迟。有环时某些课的入度永远降不到 0，输出长度不足 `n`。复杂度 `O((n + m) log n)`。

```python
# MinHeap 是上面手写的最小堆：构造时线性建堆，用到 pop、push、len
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """prerequisites[k] = [a, b]：先上 b 才能上 a。返回字典序最小的上课顺序，有环返回 []。"""
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    ready = MinHeap(c for c in range(num_courses) if indeg[c] == 0)
    order: list[int] = []
    while ready:
        c = ready.pop()
        order.append(c)
        for nxt in graph[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                ready.push(nxt)
    return order if len(order) == num_courses else []
```

   运行：`find_order(4, [[0, 2], [1, 3]])` → `[2, 0, 3, 1]`（普通队列得到 `[2, 3, 0, 1]`，字典序更大）；`find_order(2, [[1, 0], [0, 1]])` → `[]`；`find_order(3, [[1, 0], [1, 0]])`（重复的边）→ `[0, 1, 2]`。
2. **最大堆 / 带优先级。** 数值取负，或者存 `(-优先级, 序号, 值)`；序号保证优先级相同时不去比较值本身。
3. **最小的 `k` 个。** 全部建堆再弹 `k` 次是 `O(n + k log n)`；想省空间就用大小为 `k` 的**最大**堆，新元素比堆顶小就替换堆顶，`O(n log k)`。

**Python 提醒**：`heapq` 只提供最小堆，最大堆靠取负；标准库里 `heapq.heapify` 是原地改列表，手写的 `heapify` 会先复制一份，两者行为不同。
