---
id: uth-compose-spring-bean-registry-3-invariant-code
node: compose.spring-bean-registry
type: qa
step: 3
---
## Q
**不变量与核心代码：表和列表同进同出**｜Spring Framework · 7.0

这几个结构要保持哪些一致？用不到 30 行的 Python 写出注册、登记依赖、按依赖反序销毁。

## A
**不变量。**

- 名字列表和定义表一一对应：注册、删除都两处一起改
- 两张依赖表互为转置：`b` 在 `dependents[a]` 里，当且仅当 `a` 在 `dependencies[b]` 里
- 销毁一个 Bean 之前，依赖它的 Bean 已经销毁；销毁后把它从别人的依赖记录里清掉

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="82" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dependencies 我依赖谁</text>
<text x="256" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dependents 谁依赖我</text>
<rect x="12" y="28" width="140" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="82.0" y="46.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A : { B }</text>
<rect x="12" y="68" width="140" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="82.0" y="86.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C : { B }</text>
<rect x="188" y="48" width="140" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="258.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B : { A, C }</text>
<line x1="152" y1="42" x2="188" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="188.0,58.0 182.4,58.3 184.4,53.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="152.0,42.0 157.6,41.7 155.6,46.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="152" y1="82" x2="188" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="188.0,66.0 184.4,70.3 182.4,65.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="152.0,82.0 155.6,77.7 157.6,82.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两张表互为转置 一边改另一边也要改</text>
<text x="170" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">关闭: A 和 C 先销毁 B 最后</text>
<text x="170" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">销毁后把自己从别人的记录里清掉</text>
</svg>
```

**核心代码。** 关闭时按注册顺序反着走；每个 Bean 先带走自己的依赖者，所以注册顺序和依赖顺序不一致也不会出错。

```python
class BeanRegistry:
    def __init__(self) -> None:
        self.defs: dict[str, object] = {}                      # 名字 -> 定义：按名字 O(1) 查
        self.names: list[str] = []                             # 注册顺序：遍历、反序销毁都靠它
        self.dependents: dict[str, set[str]] = {}              # 我 -> 依赖我的
        self.dependencies: dict[str, set[str]] = {}            # 我 -> 我依赖的
        self.closed: dict[str, None] = {}                      # 已销毁的名字，按销毁顺序

    def register(self, name: str, definition: object) -> None:
        if name in self.defs:
            raise ValueError(f"重复注册 {name}")
        self.defs[name] = definition                           # 表和列表一起改
        self.names.append(name)

    def depend(self, bean: str, on: str) -> None:              # bean 依赖 on：两张表同时记
        self.dependents.setdefault(on, set()).add(bean)
        self.dependencies.setdefault(bean, set()).add(on)

    def destroy(self, name: str) -> None:
        for user in self.dependents.pop(name, set()):          # 先销毁依赖我的；pop 掉，防止重复和死循环
            self.destroy(user)
        self.closed.setdefault(name)                           # 再销毁自己；已销毁的不会重复记
        for dep in self.dependencies.pop(name, set()):         # 把我从被依赖者的“依赖我的”里摘掉
            self.dependents.get(dep, set()).discard(name)

    def close(self) -> None:
        for name in reversed(self.names):                      # 注册顺序的反序；每个先带走自己的依赖者
            self.destroy(name)
```

**例题：** LC 210 课程表 II

共有 `numCourses` 门课，先修关系 `prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。返回一个能学完所有课程的顺序，学不完返回空数组。例：`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0,1,2,3]`。同一份依赖图：邻接表加入度表求出先后顺序，Spring 的销毁顺序就是它的反向。

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
