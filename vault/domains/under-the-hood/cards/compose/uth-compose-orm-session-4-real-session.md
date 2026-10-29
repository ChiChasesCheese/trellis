---
id: uth-compose-orm-session-4-real-session
node: compose.orm-session
type: qa
step: 4
---
## Q
**真实 ORM 多做了什么**｜SQLAlchemy 2.0.55 · Hibernate 7.4

真实的 Session 比上面的版本多做了什么？为什么这样设计？

## A
**细节。**

- 弱引用：SQLAlchemy 的身份映射是 `WeakInstanceDict`，没人引用的对象会被回收并从表里消失；`new` 和 `deleted` 是强引用，待写的对象不会丢
- 找脏对象：SQLAlchemy 在属性被赋值时就打标记，flush 时再逐属性比较，没有净变化就不发 SQL；Hibernate 保存加载时的快照，flush 时逐属性比较
- 排序：SQLAlchemy 把类之间的外键依赖建成图，做拓扑排序，每轮取出没有未处理父节点的动作；有环时（例如表引用自己）改成逐对象排序
- 事务：flush 在数据库事务里，任何一条 SQL 失败就整体回滚；SQLAlchemy 里还必须调用 `rollback()` 才能继续用这个 Session

**为什么。** 先记账、后批量写：少发 SQL、能排序、一次事务保证原子；代价是内存里的对象和数据库可能不一致。

**坑。** Session 不是缓存：`select` 查询照样发 SQL，只有按主键 `get` 才能跳过。它也不是线程安全的，一个线程（或任务）一个 Session。

**例题：** LC 210 课程表 II

共有 `numCourses` 门课，`prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。返回一个能学完所有课程的顺序，学不完就返回空数组。`1 <= numCourses <= 2000`。例：`2, [[1,0]]` → `[0,1]`。flush 要排的就是这个顺序：被外键引用的父表相当于先修课，学习顺序就是写入顺序，有环则 SQLAlchemy 抛 `CircularDependencyError`。

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
