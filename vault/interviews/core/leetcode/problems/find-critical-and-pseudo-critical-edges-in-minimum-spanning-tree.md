---
slug: find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree
---
## Q
**LC 1489 找到最小生成树里的关键边和伪关键边**｜Hard

`n <= 100` 个点的带权无向连通图，边数 `<= 200`。删掉后 MST 权值变大的边是关键边；出现在某些 MST 但不在全部 MST 里的边是伪关键边。分别返回两类边的下标。

## A
**一句话。** 先用 Kruskal 求 MST 权值 `base`；逐条边试：不用它时权值变大（或不连通）就是关键边，否则强制先选它时权值仍为 `base` 就是伪关键边。

```python
def find_critical_and_pseudo_critical_edges(n, edges):
    order = sorted(range(len(edges)),
                   key=lambda i: edges[i][2])

    def mst(skip=-1, force=-1):   # Kruskal，返回权值和
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        total = cnt = 0
        if force >= 0:            # 先把这条边放进树里
            u, v, w = edges[force]
            parent[u] = v
            total, cnt = w, 1
        for i in order:
            if i == skip:
                continue
            u, v, w = edges[i]
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                total += w
                cnt += 1
        return total if cnt == n - 1 else inf

    base = mst()
    crit, pseudo = [], []
    for i in range(len(edges)):
        if mst(skip=i) > base:
            crit.append(i)        # 少了它就变贵或不连通
        elif mst(force=i) == base:
            pseudo.append(i)      # 有一棵 MST 用到它
    return [crit, pseudo]
```

**复杂度。** 时间 `O(m² α(n))`（排序只做一次），空间 `O(n + m)`。

**易错点。**
- 删边后图不连通时返回了较小的和：要返回 `inf`，否则关键边漏判。
- 关键边又判一次伪关键：关键边强制选入也等于 `base`，必须用 `elif` 排除。

**追问。**
- 更快的做法？：按权值分组，每组内在缩点后的图上找桥：桥是关键边，非桥且连接不同块的是伪关键边，`O(m log m)`。
- 只问某条边是否在某棵 MST 里？：去掉所有权值 `>=` 它的边后，它的两端若仍不连通就在。

**同模式。** LC 1584 连接所有点的最小费用、LC 1135 最低成本连通所有城市、LC 1168 水资源分配优化
