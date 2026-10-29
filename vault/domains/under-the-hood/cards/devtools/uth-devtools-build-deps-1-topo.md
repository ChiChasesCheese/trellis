---
id: uth-devtools-build-deps-1-topo
node: devtools.build-deps
type: qa
step: 1
---
## Q
**构建系统怎么决定先编译谁**｜Ninja · 1.13

你改了一个 `.h`，Ninja 怎么知道哪些文件要重编，还不会陷入死循环？

## A
**背景。** 改了一个头文件，要重新编译哪些文件？全部重编太慢，所以构建系统把依赖画成一张图：每个文件是一个点，“B 由 A 生成”画成 A 指向 B 的箭头。顺序上必须先做被依赖的，这就是拓扑序（topological order）。如果 A 要等 B、B 又要等 A，就成了环，没法排序，只能报错。

**结构。** 构建图是 DAG（有向无环图）：节点是文件，边是构建命令。Ninja 的 `RecomputeNodeDirty` 从目标出发做深度优先遍历（DFS），沿途用一个栈检测环。例：改了 `util.h`，沿箭头的两个 `.o` 和最终的 `app` 都变“脏”（需要重做），`main.c`、`util.c` 不用动。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<rect x="22" y="27" width="68" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">main.c</text>
<rect x="22" y="87" width="68" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">util.h</text>
<rect x="22" y="147" width="68" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">util.c</text>
<rect x="136" y="57" width="68" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">main.o</text>
<rect x="136" y="117" width="68" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">util.o</text>
<rect x="250" y="87" width="68" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="284" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">app</text>
<line x1="90" y1="40" x2="131.567" y2="61.6872" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M136.0,64.0 L128.5,63.8 L131.5,58.0 Z" fill="currentColor" stroke="none"/>
<line x1="90" y1="96" x2="131.528" y2="75.2361" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M136.0,73.0 L131.4,78.9 L128.5,73.1 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="90" y1="104" x2="131.528" y2="124.764" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M136.0,127.0 L128.5,126.9 L131.4,121.1 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="90" y1="160" x2="131.567" y2="138.313" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M136.0,136.0 L131.5,142.0 L128.5,136.2 Z" fill="currentColor" stroke="none"/>
<line x1="204" y1="73" x2="245.528" y2="93.7639" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M250.0,96.0 L242.5,95.9 L245.4,90.1 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="204" y1="127" x2="245.528" y2="106.236" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M250.0,104.0 L245.4,109.9 L242.5,104.1 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">改了 util.h 沿箭头的三个文件都要重做</text>
</svg>
```

**细节。**

- 后序遍历（先处理完输入再处理自己）就是拓扑序；输出缺失，或最新的输入比输出新（比较修改时间 mtime），就标记为脏
- 递归时遇到栈里已有的节点，报错 `dependency cycle: a -> b -> a`
- 互不依赖的任务并行执行，默认并行度是核数 + 2（核数大于 2 时）
- GNU make 遇到环只警告：`Circular x <- y dependency dropped`

**为什么。** 只靠修改时间和图遍历，不需要比较文件内容，增量构建就是一次图的遍历。

**例题：** LC 207 课程表（同类：LC 210 课程表 II）

共 `numCourses` 门课，`prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。判断能否学完所有课程。例：`numCourses=2`，`[[1,0]]` → `true`；`[[1,0],[0,1]]` → `false`（成环）。

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
