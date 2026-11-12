---
slug: tt-course-schedule-output-path
---
## Q
**课程表输出学习顺序，及单词接龙输出最短路径**｜Medium

两问。一：`[a, b]` 表示学 `a` 前先学 `b`，输出一种可行学习顺序，有环返回 `[]`。二：每次改一个字母且结果须在 `words` 里，输出 `begin` 到 `end` 的一条最短转换路径（含首尾），不可达返回 `[]`。

## A
**一句话。** 都是图上的 BFS：第一问用入度的拓扑排序（Kahn），第二问按通配模式分桶找邻居，入队时记前驱再回溯。

```python
def find_order(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for c, p in prerequisites:
        graph[p].append(c)            # 边 p -> c
        indeg[c] += 1
    q = deque(i for i, d in enumerate(indeg) if d == 0)
    order = []
    while q:
        cur = q.popleft()
        order.append(cur)
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return order if len(order) == num_courses else []

def shortest_ladder(begin, end, words):
    if end not in set(words):
        return []
    buckets = defaultdict(list)       # "h*t" -> [hot, hit]
    for w in dict.fromkeys((begin, *words)):
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    parent = {begin: None}            # 既是 visited，又记前驱
    q = deque([begin])
    while q:
        cur = q.popleft()
        if cur == end:
            break
        for i in range(len(cur)):
            for nxt in buckets[cur[:i] + "*" + cur[i + 1:]]:
                if nxt not in parent:
                    parent[nxt] = cur
                    q.append(nxt)
    if end not in parent:
        return []
    path, node = [], end
    while node is not None:           # 沿前驱回溯再反转
        path.append(node)
        node = parent[node]
    return path[::-1]
```

**复杂度。** 课程 时间 `O(V + E)`；接龙 时间 `O(N·L²)`，空间 `O(N·L)`。

**易错点。**
- 边方向反了：`[a, b]` 的边是 `b -> a`，写成 `graph[a].append(b)` 则 `(2, [[1,0]])` 得 `[1, 0]`，应为 `[0, 1]`。
- 不检查出队数量：`(3, [[1,2],[2,1]])` 有环却返回 `[0]`，应为 `[]`。
- 接龙在出队时才标记已访问：同一单词多次入队，前驱被覆盖，队列膨胀。
- 两两比较单词建图：`N = 5000` 超时，必须分桶。

**追问。**
- 字典序最小的课程顺序？：把队列换成最小堆。
- 输出所有最短接龙路径？：BFS 记录每个单词的所有前驱（仅距离恰好小一层），到达后 DFS 展开。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 127 单词接龙、LC 126 单词接龙 II
