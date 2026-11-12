---
slug: shortest-path-with-alternating-colors
---
## Q
**LC 1129 颜色交替的最短路径**｜Medium

有向图的边分红、蓝两色。求从 `0` 到每个结点、红蓝边交替出现的最短路径长度，不存在为 `-1`。

## A
**一句话。** 在状态（结点，下一条边须是什么颜色）上做 BFS，起点两种颜色同时入队，每个状态只入队一次。

```python
def shortest_alternating_paths(n, red_edges, blue_edges):
    g = [[[] for _ in range(n)] for _ in range(2)]
    for u, v in red_edges:
        g[0][u].append(v)
    for u, v in blue_edges:
        g[1][u].append(v)
    ans = [-1] * n
    seen = {(0, 0), (0, 1)}        # (结点, 下一条边颜色)
    q = deque([(0, 0, 0), (0, 1, 0)])
    while q:
        u, c, d = q.popleft()
        if ans[u] == -1:           # 首次到达即最短
            ans[u] = d
        for v in g[c][u]:
            if (v, 1 - c) not in seen:
                seen.add((v, 1 - c))
                q.append((v, 1 - c, d + 1))
    return ans
```

**复杂度。** 时间 `O(n + e)`，空间 `O(n + e)`。

**易错点。**
- 只用结点标记已访问：先走红边到 `1` 就封死了「以蓝边到 `1`」这条路，会漏答案。
- 起点只放一种颜色：第一条边可红可蓝，`red=[]`、`blue=[[0,1]]` 会得 `-1`。

**追问。**
- 要返回路径本身？：每个状态记父状态，到达后沿父指针回溯。
- 推广到 `k` 种颜色轮转？：下一色改成 `(c + 1) % k`。

**同模式。** LC 847 访问所有节点的最短路径、LC 1293 网格中的最短路径、LC 752 打开转盘锁
