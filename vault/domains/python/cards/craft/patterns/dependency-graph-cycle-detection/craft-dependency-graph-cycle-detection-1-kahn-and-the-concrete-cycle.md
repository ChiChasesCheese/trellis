---
id: craft-dependency-graph-cycle-detection-1-kahn-and-the-concrete-cycle
node: craft.patterns.dependency-graph-cycle-detection
type: qa
step: 1
---
## Q
**依赖图与环检测 · 拓扑排序，以及怎样报出「具体哪个环」**｜写法

一批任务（或包）互相依赖：app 依赖 lib 和 log，它们都依赖 core。要给出一个安全的执行顺序，依赖写错成环时还要告诉用户是哪几个任务成了环。「按输入顺序挨个执行、缺依赖就报错」会在哪里出问题？拓扑排序（topological sort，一个节点永远排在它依赖的节点之后）怎么做，又怎么从失败里还原出环？

## A
**要点。** Kahn 算法：给每个节点记「还差几个依赖没完成」（入度，in-degree）；入度为 0 的先出队，出队时给依赖它的节点各减一，减到 0 就入队。排完后若出队数少于节点数，剩下的节点互相等待，必有环。再沿「剩下的节点里的某个依赖」一路走，必然会撞上走过的点，那一段就是具体的环。

```python
import heapq

def order(deps):
    """deps[x] = x 依赖的节点。Kahn：入度为 0 的先出队，出队时给依赖它的节点减一。"""
    idx = {n: i for i, n in enumerate(deps)}                  # 首次出现序号：同时可选时的确定顺序
    waiting = {n: len(set(p)) for n, p in deps.items()}
    users = {n: set() for n in deps}
    for n, ps in deps.items():
        for p in ps:
            users[p].add(n)
    ready = [idx[n] for n, c in waiting.items() if c == 0]
    heapq.heapify(ready)
    names, out = list(deps), []
    while ready:
        n = names[heapq.heappop(ready)]
        out.append(n)
        for u in users[n]:
            waiting[u] -= 1
            if waiting[u] == 0:
                heapq.heappush(ready, idx[u])
    if len(out) != len(names):                                # 没排完 = 剩下的里一定有环
        stuck = {n for n, c in waiting.items() if c > 0}
        raise ValueError(find_cycle(deps, idx, stuck))
    return out

def find_cycle(deps, idx, stuck):
    """stuck 里每个节点至少还有一个 stuck 前置：沿它一直走，必撞上走过的点。"""
    node = min(stuck, key=idx.get)
    path, pos = [], {}
    while node not in pos:
        pos[node] = len(path); path.append(node)
        node = next(d for d in sorted(deps[node], key=idx.get) if d in stuck)
    return path[pos[node]:] + [node]   # 只截取环本身，丢掉走进环之前的那一段

print(order({"app": ["lib", "log"], "lib": ["core"], "log": ["core"], "core": []}))
try: order({"app": ["x"], "x": ["y"], "y": ["z", "x"], "z": [], "w": ["app"]})
except ValueError as e: print("环：", " -> ".join(e.args[0]))
```

实际输出（后一例里 app、w 也卡住了，但它们只是依赖环，不在环上）：

```
['core', 'lib', 'log', 'app']
环： x -> y -> x
```

**为什么。** 「按输入顺序执行」要么依赖未就绪，要么得到一句只说「有环」的报错，用户得自己去找。同时可选的节点用「首次出现序号」入小顶堆，输出顺序才确定，测试才能断言整条序列。

**易错。** `stuck` 是「环 + 环下游」，不要把它整个当作环报告；入度要按去重后的边数算（`len(set(p))`），否则重复写的依赖会让节点永远入不了队。
