---
id: tlc-tt-course-schedule-output-path-2-code
node: p1.tt-course-schedule-output-path
type: qa
step: 2
---
## Q
**课程表输出学习顺序，及单词接龙输出最短路径**｜写出 Python 实现

写 `find_order(num_courses, prerequisites)`：课程 `0` 到 `num_courses - 1`（`1 <= num_courses <= 2000`），`[a, b]` 表示先学 `b` 再学 `a`，`len(prerequisites) <= 5000`；返回一种学习顺序，有环返回 `[]`。再写 `shortest_ladder(begin, end, words)`：单词等长、全小写（`1 <= len(words) <= 5000`），每次改一个字母且结果在 `words` 里，返回一条最短路径（含首尾），不可达返回 `[]`。

## A
**思路。** 课程用 Kahn 算法：入度为 `0` 的入队，出队时给后继的入度减 `1`；出队总数不足说明有环。接龙用通配模式分桶建邻接关系，BFS 入队时同时记前驱，到达 `end` 后回溯反转。

```python
from collections import defaultdict, deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """prerequisites[i] = [a, b]：学 a 之前必须先学 b。返回一种可行学习顺序；有环返回 []。"""
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)                 # 边 pre -> course
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    order: list[int] = []
    while queue:
        cur = queue.popleft()
        order.append(cur)
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []     # 有环时总有节点入度永远不为 0


def shortest_ladder(begin: str, end: str, words: list[str]) -> list[str]:
    """每次改一个字母，且结果必须在 words 里。返回一条最短转换路径（含首尾），不可达返回 []。"""
    if end not in set(words):
        return []
    buckets: defaultdict[str, list[str]] = defaultdict(list)    # 通配模式 -> 单词，如 "h*t" -> [hot, hit]
    for w in dict.fromkeys((begin, *words)):
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    parent: dict[str, str | None] = {begin: None}               # 既是 visited，又记前驱
    queue = deque([begin])
    while queue:
        cur = queue.popleft()
        if cur == end:
            break
        for i in range(len(cur)):
            for nxt in buckets[cur[:i] + "*" + cur[i + 1:]]:
                if nxt not in parent:
                    parent[nxt] = cur
                    queue.append(nxt)
    if end not in parent:
        return []
    path: list[str] = []
    node: str | None = end
    while node is not None:                                     # 顺着前驱回溯，再反转
        path.append(node)
        node = parent[node]
    return path[::-1]
```

运行：`find_order(4, [[1,0],[2,0],[3,1],[3,2]])` → `[0, 1, 2, 3]`，`find_order(2, [[1,0],[0,1]])` → `[]`，`find_order(1, [])` → `[0]`；`shortest_ladder("hit", "cog", ["hot","dot","dog","lot","log","cog"])` → `['hit', 'hot', 'dot', 'dog', 'cog']`，去掉 `"cog"` 后 → `[]`；`n = 2000` 的一条先修链正常返回。

**复杂度。** 课程：时间与空间 `O(V + E)`。接龙：建桶与 BFS 都是 `O(N · L^2)`，空间 `O(N · L)`。

**写法要点。**
- `deque(i for i, d in enumerate(indegree) if d == 0)`：用生成器直接初始化队列，一行找出所有起点。
- `parent` 字典同时当 `visited` 和前驱表：`nxt not in parent` 判断是否访问过，赋值即标记，入队时就标记。
- `dict.fromkeys((begin, *words))` 去重且保持顺序，保证同一输入每次输出同一条路径；换成 `set` 遍历顺序会随哈希种子变化。
- `buckets[...]` 用 `defaultdict(list)`；`node: str | None` 沿 `parent` 回溯到 `None` 结束。
