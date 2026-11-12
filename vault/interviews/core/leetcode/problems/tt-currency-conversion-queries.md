---
slug: tt-currency-conversion-queries
---
## Q
**货币兑换查询**｜Medium

`pairs[i] = (a, b)`、`rates[i] = r` 表示 `1` 个 `a` 换 `r` 个 `b`（反向是倒数）。对每个查询 `(from, to)` 返回换算比率（可经多个货币相乘），不连通或没出现过返回 `-1.0`。

## A
**一句话。** 带权并查集：`ratio[x]` 记「1 个 `x` 等于几个根」，合并时算出根与根的比率，查询用 `ratio[a] / ratio[b]`。

```python
def convert(pairs, rates, queries):
    parent, ratio = {}, {}   # ratio[x]：1 个 x = 几个父

    def find(x):
        if parent[x] != x:
            root = find(parent[x])
            ratio[x] *= ratio[parent[x]]   # 路径压缩，比率连乘
            parent[x] = root
        return parent[x]

    for a, b in pairs:
        for x in a, b:
            parent.setdefault(x, x)
            ratio.setdefault(x, 1.0)
    for (a, b), rate in zip(pairs, rates):  # 1 a = rate b
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            ratio[ra] = rate * ratio[b] / ratio[a]
    out = []
    for a, b in queries:
        if a not in parent or b not in parent:
            out.append(-1.0)
        elif find(a) != find(b):
            out.append(-1.0)
        else:
            out.append(ratio[a] / ratio[b])
    return out
```

**复杂度。** 时间 `O((P + Q) α)`，空间 `O(V)`。

**易错点。**
- 查询里的货币从没出现过：直接取 `parent[x]` 抛 `KeyError`，先判 `a not in parent`。
- 路径压缩只改 `parent` 不改 `ratio`：`ratio` 仍是到旧父亲的比率，结果乱掉。
- 邻接表只存正向边：`JPY -> USD` 找不到，要补倒数边。

**追问。**
- 长度 `10^5` 的链会爆递归吗？：会，`find` 递归深度等于链长；改成循环，或按大小合并让树高 `O(log n)`。
- 汇率可能矛盾（套利）？：边权取 `-log(rate)`，用 Bellman-Ford 检测负环。

**同模式。** LC 399 除法求值、LC 990 等式方程的可满足性、LC 1202 交换字符串中的元素、LC 3387 两天内转换后的最大货币量
