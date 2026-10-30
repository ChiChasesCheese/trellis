---
id: tlc-evaluate-division-4-followup
node: p4.evaluate-division
type: qa
step: 4
---
## Q
**LC 399 除法求值**｜追问

面试官接着问：（1）不用并查集，用图搜索怎么写？（2）如果方程是在线陆续到来，还要检测矛盾？（3）变量只有几十个、查询很多呢？

## A
1. **图 + BFS。** 建双向带权图，每个查询从 `c` 出发广度优先，累乘到 `d`：

```python
from collections import defaultdict, deque


def calc_equation_bfs(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    graph: defaultdict[str, dict[str, float]] = defaultdict(dict)
    for (a, b), v in zip(equations, values):
        graph[a][b] = v
        graph[b][a] = 1 / v

    def query(c: str, d: str) -> float:
        if c not in graph or d not in graph:
            return -1.0
        seen = {c: 1.0}                          # seen[x] = c / x，从 c 出发沿边累乘
        dq = deque([c])
        while dq:
            x = dq.popleft()
            for y, w in graph[x].items():
                if y not in seen:
                    seen[y] = seen[x] * w
                    dq.append(y)
        return seen.get(d, -1.0)

    return [query(c, d) for c, d in queries]
```

每个查询 `O(V + E)`；数据小时最直观。
2. **在线加方程、查矛盾。** 并查集合并时若两个变量已同根，就检查 `ratio[a] / ratio[b]` 与 `v` 是否在浮点误差内相等（`math.isclose`），不等就是矛盾。
3. **查询多、变量少。** Floyd–Warshall 预处理所有点对，`O(V^3)`，之后每个查询 `O(1)`；或者直接用并查集，每次查询 `O(α)`，不依赖 `V^3`。

**Python 提醒**：浮点数不要用 `==` 判断相等，用 `math.isclose(x, y, rel_tol=1e-9)`；`defaultdict(dict)` 读取不存在的键会**创建**空字典，所以 `c not in graph` 要在访问 `graph[c]` 之前判断，否则未出现的变量会被悄悄加入图里。
