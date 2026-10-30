---
id: tlc-tt-currency-conversion-queries-0-whole
node: p4.tt-currency-conversion-queries
type: qa
---
## Q
**货币兑换查询**｜Medium · 近一年被问：美国 3 次、国内 0 次 · 最近 2026-01-05（美国面试记录）

给若干货币对及汇率：`pairs[i] = (a, b)`、`rates[i] = r` 表示 `1` 单位 `a` 可兑换 `r` 单位 `b`（`r > 0`），反方向的汇率是倒数。再给若干查询 `(from, to)`，返回从 `from` 换算到 `to` 的比率，可以经过多个货币相乘；两种货币不连通，或者其中一个从未出现过，返回 `-1.0`；货币到自身（且出现过）返回 `1.0`。`1 <= len(pairs), len(queries) <= 10^5`，货币名是不超过 `5` 个字符的字符串，给定的汇率互相不矛盾，结果允许 `1e-5` 的误差。例：`pairs = [("USD","JPY")]`，`rates = [108.0]`，查询 `[("USD","JPY"), ("JPY","USD"), ("USD","GBP")]` → `[108.0, 0.009259259259259259, -1.0]`（`GBP` 没有任何汇率）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 带权并查集（weighted union-find）：每个货币记一个 `ratio[x]`，表示 `1` 个 `x` 等于多少个它所在集合的根；合并两个集合时按汇率算出根与根之间的比率；查询时同一集合就用 `ratio[from] / ratio[to]`，不同集合返回 `-1.0`。均摊近似 `O(1)`。

**识别。** 「汇率可以经多跳相乘」「反向取倒数」「无法到达返回 `-1`」是 LC 399（除法求值）同型：货币是点，汇率是带权边，路径上的权相乘。查询次数达 `10^5`，每次查询都跑一次 BFS/DFS 是 `O(Q · (V + E))`，太慢；汇率之间不矛盾，说明任意路径得到的比率相同，可以把连通的货币归并到一个集合里，每个货币只记它到根的比率。

**推导。** 暴力：建图，每个查询 BFS/DFS 一次，`O(Q · (V + E))`，`10^10` 量级。浪费：同一连通块里的货币，两两比率早就确定了，却每次重新走路径。洞察：选一个根，每个货币到根的比率只算一次；查 `from -> to` 就是 `ratio[from] / ratio[to]`（都换成根的单位再相除）。合并时 `1 a = r b`，设 `a` 的根为 `ra`、`b` 的根为 `rb`，则 `1 ra = r · ratio[b] / ratio[a]` 个 `rb`，一次赋值接好。`find` 递归走到根，回溯时做路径压缩，并同步把比率乘到根。

```python
def convert(pairs: list[tuple[str, str]], rates: list[float], queries: list[tuple[str, str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}          # ratio[x]：1 个 x 兑换成多少个 parent[x]

    def find(x: str) -> str:
        if parent[x] != x:
            root = find(parent[x])        # 先把父亲压缩到直连根，ratio[父亲] 就是父亲到根的比率
            ratio[x] *= ratio[parent[x]]  # 1 个 x = ratio[x] 个父亲 = ratio[x] * ratio[父亲] 个根
            parent[x] = root
        return parent[x]

    for a, b in pairs:
        parent.setdefault(a, a)
        ratio.setdefault(a, 1.0)
        parent.setdefault(b, b)
        ratio.setdefault(b, 1.0)
    for (a, b), rate in zip(pairs, rates):    # 1 个 a = rate 个 b
        ra, rb = find(a), find(b)
        if ra != rb:
            # 1 a = ratio[a] ra ; 1 b = ratio[b] rb ; 1 a = rate b = rate*ratio[b] rb  =>  1 ra = rate*ratio[b]/ratio[a] rb
            parent[ra] = rb
            ratio[ra] = rate * ratio[b] / ratio[a]
    out: list[float] = []
    for a, b in queries:
        if a not in parent or b not in parent or find(a) != find(b):
            out.append(-1.0)
        else:
            out.append(ratio[a] / ratio[b])   # a、b 都已直连根：1 a = ratio[a] root, 1 b = ratio[b] root
    return out
```

运行：`[("USD","JPY")]`、`[108.0]`，查询 `USD->JPY`、`JPY->USD`、`USD->GBP`、`USD->USD`、`GBP->GBP` → `[108.0, 0.009259259259259259, -1.0, 1.0, -1.0]`；`[("USD","EUR"),("EUR","JPY"),("GBP","CHF")]`、`[0.9, 160.0, 1.1]`，查询 `USD->JPY`、`JPY->USD`、`GBP->USD`、`CHF->GBP` → `[144.0, 0.006944444444444444, -1.0, 0.9090909090909091]`；长度 `900` 的汇率链（每个汇率都是 `1.0`）上查询两端 → `1.0`。

**复杂度。** 时间 `O((P + Q) · α)`，`α` 为反阿克曼函数，实际近似常数；空间 `O(V)`。

**易错点。**
- 反方向忘记取倒数：用邻接表时只存正向边，`JPY -> USD` 会得到 `108.0` 或者找不到；并查集版本中反向比率由 `ratio[a] / ratio[b]` 自然给出倒数。
- 查询里的货币从未出现过，直接取 `parent[x]` 抛 `KeyError`；先判断 `a not in parent`，返回 `-1.0`。
- 路径压缩只改 `parent` 不改 `ratio`：压缩之后 `ratio` 仍是到旧父亲的比率，结果乱掉；压缩时必须把父亲到根的比率乘上。
- 深度：`find` 的递归深度等于该点到根的链长。汇率依次是 `(x0,x1),(x1,x2),…` 这样的长度 `10^5` 的链时，查询 `x0` 要递归 `10^5` 层，超过 CPython 默认递归上限（约 `1000`，`1500` 层的链就会）而抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么把 `find` 写成循环（见追问）。

**追问。**
- 两天各有一套汇率，起始货币的数量最大能换到多少（LC 3387）：第一天从起点遍历图，算出能换到的每种货币的数量；第二天在另一套汇率里同样遍历，把每种货币换回起点货币，取最大值。
- 迭代的 `find`（深链安全）：先循环走到根并把路径存进列表，再从靠近根的一端往下压缩；也可以按大小合并（union by size），让树高保持 `O(log n)`，递归就没有深度风险。
- 不用并查集：建带权图，每个查询 BFS/DFS，`O(Q · (V + E))`；查询很少时更直观。
- 汇率出现矛盾（存在套利）：把 `-log(rate)` 当边权，用 Bellman-Ford 检测负环。

**同模式。** LC 399 除法求值、LC 990 等式方程的可满足性、LC 1202 交换字符串中的元素、LC 3387 两天内转换后的最大货币量。
