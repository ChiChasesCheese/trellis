---
id: craft-lock-hierarchy-and-reentrancy-2-one-direction
node: craft.architecture.lock-hierarchy-and-reentrancy
type: qa
step: 2
---
## Q
**调用方向与可重入 · 「司机池从不回调调度服务」是怎样的一条纪律**｜架构

叫车系统里调度服务（有自己的锁）调用司机池（有自己的锁）来占用司机。如果司机池在某些时候又反过来回调调度服务（比如通知「司机下线了」），会出现什么死锁时间线？怎样在 code review 或测试里检查这条纪律？

## A
**要点。** 把锁关系画成一张有向图：持有 A 时去拿 B，就画 A → B。图无环就不会有锁序死锁；一旦司机池回调服务，就出现「池锁 → 服务锁」，与原来的「服务锁 → 池锁」合成环：一个线程持服务锁等池锁，另一个持池锁等服务锁。纪律是规定调用只能单向（服务调池，池不回头），并让它可以被检查：运行时记录实际发生的嵌套，检查有没有环。

```python
edges: dict[str, set[str]] = defaultdict(set)         # 锁序图：持有 A 时去拿 B，记 A -> B
held = threading.local()

class TrackedLock:
    def __init__(self, name: str) -> None:
        self.name, self._lock = name, threading.Lock()
    def __enter__(self) -> None:
        stack = getattr(held, "stack", [])
        for h in stack:
            edges[h].add(self.name)                # 记录实际发生的嵌套
        self._lock.acquire()
        held.stack = stack + [self.name]
    def __exit__(self, *exc) -> None:
        held.stack = held.stack[:-1]
        self._lock.release()

def find_cycle() -> list[str] | None:
    def dfs(node: str, path: list[str]) -> list[str] | None:
        if node in path:
            return path[path.index(node):] + [node]
        for nxt in edges.get(node, ()):
            if (c := dfs(nxt, path + [node])):
                return c
        return None
    for n in list(edges):
        if (c := dfs(n, [])):
            return c
    return None

service, pool = TrackedLock("服务锁"), TrackedLock("池锁")

def dispatch() -> None:                                # 服务 -> 池
    with service:
        with pool: pass
dispatch()                    # with service: with pool: ...
print("只有服务锁 -> 池锁:", dict(edges), "| 环:", find_cycle())

def pool_callback_into_service() -> None:              # 池回调服务：反向
    with pool:
        with service: pass
pool_callback_into_service()  # with pool: with service: ...
print("加上池 -> 服务回调:", {k: sorted(v) for k, v in edges.items()}, "| 环:", find_cycle())
```

`find_cycle` 对 `edges` 做深度优先搜索，实际输出：

```
只有服务锁 -> 池锁: {'服务锁': {'池锁'}} | 环: None
加上池 -> 服务回调: {'服务锁': ['池锁'], '池锁': ['服务锁']} | 环: ['服务锁', '池锁', '服务锁']
```

**为什么。** 死锁需要环，所以消灭环比逐个分析时序简单。池的接口因此尽量不暴露回调，状态变化通过返回值告诉调用者。

**代价。** 单向纪律意味着有些事不能在池里直接做，要返回给上层去做（比如池只返回「这位司机被释放了」，由服务决定后续通知）。
