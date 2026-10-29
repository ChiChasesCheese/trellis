---
id: uth-python-memory-gc-2-cycle
node: python.memory-gc
type: qa
step: 2
---
## Q
**循环引用的垃圾怎么找出来**｜Python · CPython 3.14

`x.me = x` 之后 `del x`，对象为什么没被释放？循环垃圾回收器靠什么判断它是垃圾？

## A
**背景。** 引用计数有个盲点：两个对象互相指着对方，外面再没人用，各自的计数却还是 1，永远不归零。所以另有循环垃圾回收器（cycle GC），只跟踪能互相引用的容器对象（`list`、`dict`、实例，不含 `int`、`str`）。

**结构。** 思路：把每个对象的计数减去「来自被检查对象集合内部的引用」，剩下还大于 0 的，说明被集合外面引用着，是活的；从它们能走到的也是活的，其余就是垃圾。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="90" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只被彼此引用</text>
<circle cx="50" cy="70" r="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<circle cx="130" cy="70" r="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<line x1="72" y1="62" x2="108" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,62.0 102.0,65.0 102.0,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="108" y1="78" x2="72" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="72.0,78.0 78.0,75.0 78.0,81.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="50" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1-1=0</text>
<text x="130" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1-1=0</text>
<text x="90" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">无人引用 垃圾</text>
<line x1="170" y1="20" x2="170" y2="190" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="210" y="16" width="52" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="236" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">变量</text>
<line x1="236" y1="40" x2="236" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,62.0 233.0,56.0 239.0,56.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="236" cy="84" r="20" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="236" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<line x1="236" y1="104" x2="236" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,128.0 233.0,122.0 239.0,122.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="236" cy="150" r="20" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="236" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<text x="266" y="88" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">gc_refs 1</text>
<text x="266" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">gc_refs 0</text>
<text x="270" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">C 走得到</text>
<text x="236" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">都是活的</text>
</svg>
```

**细节。**

- 先把每个对象的 `gc_refs` 设为引用计数，再遍历容器，减去**容器之间**的内部引用。
- 实测 `del x` 后弱引用仍存活；`gc.collect()` 返回 1，之后对象消失。

**为什么。** 不用从根扫描整个堆，只在被检查的对象集合里算内部引用。

**例题：** LC 207 课程表

共 `numCourses` 门课，`prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。判断能否学完所有课程。例：2 门课、先修 `[[1,0],[0,1]]`（互相要求）返回 `false`。

```python
from collections import deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)                  # 边 pre -> course：先修课指向后修课
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses                    # 有环 => 环上的点入度永远降不到 0
```
