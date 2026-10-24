---
id: tlc-tt-course-schedule-output-path-4-followup
node: a.tt-course-schedule-output-path
type: qa
step: 4
---
## Q
**课程表输出学习顺序，及单词接龙输出最短路径**｜追问

课程表已经能输出一种拓扑序，单词接龙能输出一条最短路径。面试官接着问：（1）输出字典序最小的课程顺序？（2）每门课有学习时长，可以并行学，最少多久学完（Parallel Courses III）？（3）输出所有最短接龙路径？（4）有环时输出环本身？

## A
1. **字典序最小**：把 `deque` 换成 `heapq` 最小堆，初始放入所有入度为 `0` 的课，每次弹出编号最小的，后继入度归零时 `heappush`；`(3, [[0,2],[1,2]])` → `[2, 0, 1]`。时间 `O((V + E) log V)`。
2. **并行加时长**：沿拓扑序做 DP，`done[v]` 是课程 `v` 最早完成的时刻，初值是自己的时长，处理边 `u -> v` 时 `done[v] = max(done[v], done[u] + time[v])`，答案是 `max(done)`。

```python
def min_total_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for a, b in relations:                         # 课程编号从 1 起：先学 a 再学 b
        graph[a - 1].append(b - 1)
        indegree[b - 1] += 1
    done = time[:]
    queue = [i for i, d in enumerate(indegree) if d == 0]
    while queue:
        cur = queue.pop()
        for nxt in graph[cur]:
            done[nxt] = max(done[nxt], done[cur] + time[nxt])
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return max(done)
```

   `n = 3`，`[[1,3],[2,3]]`，`time = [3,2,5]` → `8`。
3. **所有最短路径**：BFS 时为每个单词记录一个**前驱列表**，只在 `dist[nxt] == dist[cur] + 1` 时追加；到达后从 `end` 用 DFS 沿前驱展开。路径数可能指数多，注意输出规模。
4. **输出环**：用 DFS 三色标记，遇到灰色节点说明有环，沿递归栈回溯到该节点即为一个环。

**Python 提醒**：`heapq` 默认小顶堆，元素是元组时按字典序比较；`deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`，队列别用列表头部弹出。
