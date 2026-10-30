---
id: tlc-core-evaluate-division
node: p4.evaluate-division
type: qa
---
## Q
**LC 399 除法求值**｜Medium · LC TikTok 热度 53/100 · 近一年被问：美国 3 次、国内 0 次 · CodeTop 国内累计 3 次 · 最近 2026-01-05（面试记录） · 也在：Amazon、Top Interview 150

给变量对数组 `equations` 和实数数组 `values` 作为已知条件：`equations[i] = [Ai, Bi]` 与 `values[i]` 表示 `Ai / Bi = values[i]`，每个变量是一个字符串。再给查询数组 `queries`，`queries[j] = [Cj, Dj]` 表示求 `Cj / Dj`。返回所有查询的答案；无法确定的、或出现了条件里没有的变量，答案用 `-1.0`。输入总是有效的，不会除以零，也没有矛盾。`1 <= equations.length, queries.length <= 20`，`0.0 < values[i] <= 20.0`，变量名长度 `1..5`，由小写字母与数字组成。例：`equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]` → `[6.0, 0.5, -1.0, 1.0, -1.0]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 带权并查集（weighted union-find）：每个变量记 `ratio[x] = x / parent[x]`；`find` 做路径压缩时把沿途的比值累乘到根；合并 `a / b = v` 时把 `a` 的根挂到 `b` 的根下，并算出两个根之比；查询 `c / d` 时，同一棵树就用 `ratio[c] / ratio[d]`，否则 `-1.0`。每次操作近似 `O(α)`。

**识别。** 等式链 `a / b`、`b / c` 能推出 `a / c`：把变量当结点、除法关系当带权边，乘法有传递性，同一连通块内任意两点的比值都由它们各自相对于代表元的比值唯一确定。查询就变成「是否连通」加「两个比值相除」。「未出现的变量 / 不连通返回 `-1.0`」恰好对应并查集里的"不在同一集合"。

**推导。** 暴力：建图（`a → b` 权 `v`，`b → a` 权 `1 / v`），每个查询做一次 DFS / BFS 累乘路径权值，`O(查询数 · (V + E))`。数据很小时足够。洞察：同一连通块内每个变量相对于一个代表元的比值是确定的，只需要预处理一次；查询时两个比值相除，代表元抵消。并查集在合并时就维护这个比值。

```python
def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}                 # ratio[x] = x / parent[x]

    def find(x: str) -> str:
        p = parent.setdefault(x, x)              # 第一次见到的变量自成一组
        ratio.setdefault(x, 1.0)
        if p != x:
            root = find(p)                       # 路径压缩：find(p) 之后 ratio[p] = p / root
            ratio[x] *= ratio[p]                 # x/root = (x/p) * (p/root)
            parent[x] = root
        return parent[x]

    for (a, b), v in zip(equations, values):     # a / b = v
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb                      # ra / rb = (a / b) * (b / rb) / (a / ra)
            ratio[ra] = v * ratio[b] / ratio[a]

    ans: list[float] = []
    for c, d in queries:
        if c in parent and d in parent and find(c) == find(d):
            ans.append(ratio[c] / ratio[d])      # (c/root) / (d/root)
        else:
            ans.append(-1.0)                     # 变量没出现过，或不在同一个连通块
    return ans
```

**运行。** 例 1 → `[6.0, 0.5, -1.0, 1.0, -1.0]`；例 2（`[["a","b"],["b","c"],["bc","cd"]], [1.5,2.5,5.0]`，查询 `a/c, c/b, bc/cd, cd/bc`）→ `[3.75, 0.4, 5.0, 0.2]`；例 3（`[["a","b"]], [0.5]`，查询 `a/b, b/a, a/c, x/y`）→ `[0.5, 2.0, -1.0, -1.0]`。

**复杂度。** 时间：建立并查集 `O(E α(V))`，每个查询 `O(α(V))`；空间 `O(V)`。

**易错点。**
- 路径压缩时先把 `parent[x]` 改成根，再用 `ratio[parent[x]]` 去乘：此时取到的是根自己的比值 `1`，比值没有累乘。`a/b=2, b/c=3, c/d=4`，查询 `a/d` 得 `2.0`，正确是 `24.0`。
- 合并公式写反（`v * ratio[a] / ratio[b]`）：`[["a","b"],["c","d"],["a","c"]]`、`[2,3,5]`，查询 `b/d` 得 `3.33…`，正确是 `7.5`。
- 变量没有出现过时，`x / x` 也要返回 `-1.0`，不是 `1.0`；必须先判断 `x in parent`。

**追问。**
- 数据量大或在线加方程、检测矛盾：并查集更合适；合并时若两个变量已同根，就检查 `ratio[a] / ratio[b]` 与 `v` 是否在浮点误差内相等（`math.isclose`）。
- 变量很少、查询很多：Floyd–Warshall 预处理所有点对，`O(V^3)`，之后每次查询 `O(1)`。
- 图上 BFS / DFS 的写法：每次查询从 `c` 出发累乘到 `d`，代码直观，适合 `V` 和查询都很小。

**同模式。** LC 990 等式方程的可满足性、LC 547 省份数量、LC 721 账户合并、LC 684 冗余连接。
