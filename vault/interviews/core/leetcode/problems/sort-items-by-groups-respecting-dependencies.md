---
slug: sort-items-by-groups-respecting-dependencies
---
## Q
**LC 1203 项目管理**｜Hard

`n` 个项目，第 `i` 个属于小组 `group[i]`（`-1` 表示不属于任何组），`beforeItems[i]` 是必须排在 `i` 之前的项目。排一个顺序，使同组项目相邻，且满足所有先后约束，不存在返回 `[]`。

## A
**一句话。** 两层拓扑排序：先给项目拓扑排序，再给小组拓扑排序（项目依赖跨组时连组边），最后按组顺序、组内按项目顺序输出。

```python
def sort_items(n, m, group, before_items):
    for i in range(n):
        if group[i] == -1:           # 无组的项目自成一组
            group[i] = m
            m += 1
    item_g = [[] for _ in range(n)]
    grp_g = [[] for _ in range(m)]
    item_deg, grp_deg = [0] * n, [0] * m
    for i in range(n):
        for j in before_items[i]:    # j 必须在 i 之前
            item_g[j].append(i)
            item_deg[i] += 1
            if group[j] != group[i]:
                grp_g[group[j]].append(group[i])
                grp_deg[group[i]] += 1
    def topo(g, deg, size):
        q = deque(x for x in range(size) if deg[x] == 0)
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in g[u]:
                deg[v] -= 1
                if deg[v] == 0:
                    q.append(v)
        return order if len(order) == size else None
    items = topo(item_g, item_deg, n)
    groups = topo(grp_g, grp_deg, m)
    if items is None or groups is None:
        return []
    members = defaultdict(list)
    for i in items:                  # 按项目拓扑序分到各组
        members[group[i]].append(i)
    return [i for g in groups for i in members[g]]
```

**复杂度。** 时间 `O(n + m + e)`，空间 `O(n + m + e)`。

**易错点。**
- 把 `-1` 都当成同一个组：它们互不相关，应各成一个小组，否则会被强行排在一起。
- 同组内的依赖也连组边：同组项目之间只影响项目排序，只有跨组依赖才需要建组边，否则会出现自环。
- 只做一层拓扑排序：同组项目必须相邻，组之间要先排序再展开。

**追问。**
- 为什么要两张图？：项目图保证组内顺序，组图保证组间顺序，两个图任意一个有环都无解。
- 空结果怎么区分？：用 `None` 表示有环，`[]` 是合法的空输入（`n = 0`）下的合法结果。

**同模式。** LC 210 课程表 II、LC 1136 平行课程、LC 269 火星词典
