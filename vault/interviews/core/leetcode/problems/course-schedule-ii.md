---
slug: course-schedule-ii
---
## Q
**LC 210 课程表 II**｜Medium

`prerequisites[i] = [a, b]` 表示学 `a` 前必须先学 `b`。返回一个能学完所有课的顺序，学不完返回空数组。

## A
**一句话。** 拓扑排序（Kahn）：入度为 0 的先入队，出队顺序即学习顺序，出队数不足则有环。

```python
def find_order(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(i for i in range(num_courses)
                  if indegree[i] == 0)
    order = []
    while queue:
        cur = queue.popleft()
        order.append(cur)        # 出队顺序即拓扑序
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

**复杂度。** 时间 `O(V+E)`，空间 `O(V+E)`。

**易错点。**
- 边方向建反：`2, [[1,0]]` 会输出 `[1, 0]`，应为 `[0, 1]`，边要建成 `b → a`。
- 有环时返回已出队的部分：必须返回 `[]`。

**追问。**
- 要字典序最小的顺序？：队列换成小根堆，每次取编号最小的入度为 0 的课。
- 如何判断顺序唯一？：任一时刻队列里恰好一个元素。

**同模式。** LC 207 课程表、LC 269 火星词典、LC 1203 项目管理、LC 444 序列重建
