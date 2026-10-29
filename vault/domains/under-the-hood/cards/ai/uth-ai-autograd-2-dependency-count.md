---
id: uth-ai-autograd-2-dependency-count
node: ai.autograd
type: qa
step: 2
---
## Q
**用了两次的张量，什么时候才能往前传**｜PyTorch · 2.14

上图里 `a` 被乘法和加法各用了一次，反向时会收到两份梯度；引擎怎么知道「两份都到齐了」？

## A
**背景。** 一个节点可能被多条路通向。第一份梯度一到就往前传，只传了半截，等第二份到了还得再传一遍；所以节点必须等所有用过它的节点都算完，才能执行。这就是拓扑排序（topological sort）：每个节点排在它的所有依赖之后。

**结构。** 先数依赖，再执行（Kahn 算法）：`backward()` 开始时，从损失出发遍历一遍图，数出每个节点有几条边指向它；执行时，一个节点算完，就把下游的计数减 1，减到 0 才放进就绪队列。

**细节。**

- 梯度先放进该节点的输入缓冲（`InputBuffer`），同一个输入收到几份就加起来：a 收到 1 和 3，等计数为 0，才以 4 执行
- 就绪队列是优先队列：同时就绪的节点里，`sequence_nr` 大的（前向里后创建的）先执行

**为什么。** 每个节点只执行一次，总代价与节点数加边数成正比；不用等所有路径各自递归地算完。

**例题：** LC 210 课程表 II（同样是先数入度，入度为 0 才出队）

`numCourses` 门课，`prerequisites[i] = [a, b]` 表示学 `a` 之前要先学 `b`。返回一个能学完所有课的顺序，学不完返回 `[]`。例：`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0,1,2,3]`。

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
