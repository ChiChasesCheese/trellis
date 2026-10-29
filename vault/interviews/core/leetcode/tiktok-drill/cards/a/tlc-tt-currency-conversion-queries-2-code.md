---
id: tlc-tt-currency-conversion-queries-2-code
node: a.tt-currency-conversion-queries
type: qa
step: 2
---
## Q
**货币兑换查询**｜写出 Python 实现

写 `convert(pairs, rates, queries)`：`pairs[i] = (a, b)`、`rates[i] = r` 表示 `1` 个 `a` 等于 `r` 个 `b`（`r > 0`，反向取倒数，汇率互不矛盾）；每个查询 `(from, to)` 返回换算比率，不连通或有货币从未出现过返回 `-1.0`，出现过的货币到自身返回 `1.0`。`1 <= len(pairs), len(queries) <= 10^5`。

## A
**思路。** 带权并查集：`ratio[x]` 是 `1` 个 `x` 兑换成多少个 `parent[x]`。合并时根据汇率算出两个根之间的比率；`find` 用循环收集路径、从靠近根的一端开始压缩并同步乘比率；查询时同一集合返回 `ratio[a] / ratio[b]`。

```python
def convert(pairs: list[tuple[str, str]], rates: list[float], queries: list[tuple[str, str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}          # ratio[x]：1 个 x 兑换成多少个 parent[x]

    def find(x: str) -> str:
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        for node in reversed(path):       # 从靠近根的一端往下压缩：先让父亲直连根，再乘上父亲的比率
            up = parent[node]
            if up != root:
                ratio[node] *= ratio[up]
            parent[node] = root
        return root

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

运行：`[("USD","JPY")]`、`[108.0]`，查询 `USD->JPY`、`JPY->USD`、`USD->GBP`、`USD->USD`、`GBP->GBP` → `[108.0, 0.009259259259259259, -1.0, 1.0, -1.0]`；`[("USD","EUR"),("EUR","JPY"),("GBP","CHF")]`、`[0.9, 160.0, 1.1]`，查询 `USD->JPY`、`JPY->USD`、`GBP->USD`、`CHF->GBP` → `[144.0, 0.006944444444444444, -1.0, 0.9090909090909091]`；长度 `10^5` 的汇率链上查询两端 → `1.0`。

**复杂度。** 时间 `O((P + Q) · α)`，空间 `O(V)`。

**写法要点。**
- `dict.setdefault(k, v)`：登记货币只有第一次生效，两次调用比 `if k not in d` 短。
- `find` 先循环走到根并记录路径，再 `reversed(path)` 压缩：离根最近的节点先直连根，它的比率已经是到根的比率，后面的节点才能乘上它；顺序反过来结果会错。
- `zip(pairs, rates)` 配合元组解包 `for (a, b), rate in ...`，一次拿到货币对和汇率。
- 迭代的 `find` 避免递归：汇率链长到 `10^5` 时递归写法会 `RecursionError`。
