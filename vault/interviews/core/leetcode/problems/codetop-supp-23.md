---
slug: codetop-supp-23
---
## Q
**补充题23 检测循环依赖**｜Medium

`n` 个模块，`deps[k] = [a, b]` 表示 `a` 依赖 `b`。判断依赖里是否存在环（自依赖也算）。

## A
**一句话。** 依赖 `a -> b` 建边 `b -> a`，做拓扑排序（Kahn），取走的模块数小于 `n` 就有环。

```python
def has_cycle(n, deps):
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in deps:              # 先有 b 才能有 a
        graph[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return done < n    # 剩下的在环上或依赖环上的模块
```

**复杂度。** 时间 `O(n + m)`，空间 `O(n + m)`。

**易错点。**
- 当无向边用并查集判环：`[[0,1],[0,2],[1,2]]` 无环却报 `True`。
- 只从模块 `0` 做 DFS：不连通时漏环，`n=4, [[2,3],[3,2]]` 得 `False`。
- 递归 DFS 在 `10^5` 层依赖链上 `RecursionError`。

**追问。**
- 要输出一个具体的环？：迭代 DFS 三色标记，撞上当前路径上的点时截取路径。
- 要输出构建顺序（LC 210）？：Kahn 出队顺序就是合法顺序。

**同模式。** LC 207 课程表、LC 210 课程表 II、LC 802 找到最终的安全状态、LC 269 火星词典
