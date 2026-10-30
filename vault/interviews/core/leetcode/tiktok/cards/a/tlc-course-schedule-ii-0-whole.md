---
id: tlc-course-schedule-ii-0-whole
node: a.course-schedule-ii
type: qa
---
## Q
**LC 210 课程表 II**｜Medium · LC TikTok 热度 88/100 · CodeTop 国内累计 13 次 · 最近 2026-09-15（CodeTop）

共有 `numCourses` 门课，编号 `0` 到 `numCourses - 1`。先修关系 `prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。返回一个能学完所有课程的学习顺序，有多个答案返回任意一个；学不完就返回空数组。`1 <= numCourses <= 2000`，`0 <= prerequisites.length <= numCourses * (numCourses - 1)`，`prerequisites[i].length == 2`，`0 <= a, b < numCourses`，`a != b`，所有先修对互不相同。例：`2, [[1,0]]` → `[0,1]`；`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0,1,2,3]` 或 `[0,2,1,3]`；`1, []` → `[0]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 拓扑排序（Kahn 算法）：入度为 0 的课程先入队，出队顺序就是一个合法的学习顺序；出队总数不足 `numCourses` 说明有环，返回 `[]`。`O(V + E)`。

**识别。** 「给出一个满足先后依赖的顺序」是拓扑排序的直接信号，「学不完返回空」是判环。边数最多 `numCourses * (numCourses - 1)`，约 `4 * 10^6`，所以建图要用邻接表而不是重复扫描先修对。

**推导。** 暴力：枚举 `n!` 种排列检查，不可行；每次找一个所有先修课都已学完的课程，每轮扫全部课程，`O(V^2 + VE)`。浪费在于每次重新找"可以学的课"。洞察：维护每门课还差几门先修（入度）；学完一门课只需要把它的后继入度减一，减到 0 的立即入队，找下一门课摊到 `O(1)`。出队顺序天然满足"先修课在前"；有环时环上的课永远入不了队，长度不足。

```python
from collections import deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    order: list[int] = []
    while queue:
        cur = queue.popleft()
        order.append(cur)                          # 出队顺序就是一个合法的拓扑序
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

运行：`2, [[1,0]]` → `[0, 1]`；`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0, 1, 2, 3]`（题面另一个合法答案 `[0,2,1,3]` 同样正确）；`1, []` → `[0]`；`2, [[1,0],[0,1]]` → `[]`；`3, []` → `[0, 1, 2]`；`2000` 门课连成链 → 长度 `2000` 的顺序。

**复杂度。** 时间 `O(V + E)`；空间 `O(V + E)`。

**易错点。**
- 边的方向。`[a, b]` 是 `b` 在前：边要建成 `b → a`。建反了会输出反序，`2, [[1,0]]` 得到 `[1, 0]`，正确是 `[0, 1]`。
- 有环时必须返回 `[]`，不能返回已经出队的那一部分。
- 结果不唯一，自己测试时要检查"每门课的先修课都在它前面"，不能和某个固定答案直接比较。

**追问。**
- 要字典序最小的顺序：把 `deque` 换成小根堆（`heapq`），每次取编号最小的入度为 0 的课程；`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0,1,2,3]`。
- 判断顺序是否唯一：任一时刻队列里恰好一个元素，顺序才唯一。
- 用 DFS 做：后序遍历的逆序就是拓扑序，同样要三色标记判环。

**同模式。** LC 207 课程表、LC 269 火星词典、LC 1203 项目管理、LC 444 序列重建、LC 2115 从给定原材料中找到所有可以做出的菜。
