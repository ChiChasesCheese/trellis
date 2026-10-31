---
id: tlc-course-schedule-ii-4-followup
node: b.course-schedule-ii
type: qa
step: 4
---
## Q
**LC 210 课程表 II**｜追问

面试官接着问：（1）要字典序最小的学习顺序？（2）怎么判断学习顺序是不是唯一的？（3）改用 DFS 求拓扑序怎么做？

## A
1. **字典序最小**：把队列换成小根堆，每次取编号最小的入度为 0 的课程。因为一门课一旦入度为 0 就随时可选，贪心地先选最小的不会使后面无解。

```python
import heapq


def smallest_order(n: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    heap = [i for i, d in enumerate(indegree) if d == 0]
    heapq.heapify(heap)
    order: list[int] = []
    while heap:
        cur = heapq.heappop(heap)
        order.append(cur)
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(heap, nxt)
    return order if len(order) == n else []
```

`smallest_order(4, [[1,0],[2,0],[3,1],[3,2]])` → `[0, 1, 2, 3]`；`smallest_order(3, [[0,2],[1,2]])` → `[2, 0, 1]`。复杂度升到 `O(V log V + E)`。
2. **顺序是否唯一**：Kahn 过程中，只要某一时刻队列里同时有两个及以上的课程，就存在不同的取法，顺序不唯一；每一步队列都恰好一个元素时才唯一。LC 444 序列重建就是这个判断。
3. **DFS 求拓扑序**：对每个未访问的点做 DFS，所有后继处理完后再把自己追加进结果，最后把结果反转；同时用三色标记判环。递归深度可达 `V`，2000 层的链会超过 Python 默认的 1000 层上限，需要迭代实现。

**Python 提醒**：`heapq` 只有小根堆，要最大字典序就把键取负数入堆；堆里放元组 `(优先级, 编号)` 时，优先级相同会继续比较编号，编号必须可比较。
