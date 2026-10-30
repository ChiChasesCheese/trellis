---
id: tlc-tt-currency-conversion-queries-4-followup
node: p4.tt-currency-conversion-queries
type: qa
step: 4
---
## Q
**货币兑换查询**｜追问

货币对加汇率、多次查询比率的问题已经用带权并查集解决。面试官接着问：（1）汇率形成 `10^5` 长的链，递归的 `find` 会怎样，怎么改？（2）第一天和第二天各有一套汇率，从起始货币出发，两天内最多能换回多少起始货币（LC 3387）？（3）汇率互相矛盾（出现套利）怎么检测？精度要求高怎么办？

## A
1. **深链与循环版 `find`**：递归深度等于到根的链长，汇率依次连成 `10^5` 长的链时，查询链头会抛 `RecursionError`。改成循环：先走到根并记录路径，再从靠近根的一端往下压缩（先让父亲直连根，再乘上父亲的比率）：

```python
def find_iter(parent: dict[str, str], ratio: dict[str, float], x: str) -> str:
    path: list[str] = []
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
```

   把主解法里内层的 `find` 换成这个函数即可，其余不变。按大小合并（union by size）让树高保持 `O(log n)`，也能消除递归深度风险。
2. **两天汇率**：每天各做一次遍历。第一天从起点出发，算出能换到的每种货币的数量；第二天在另一套汇率里同样算出“起点到各货币”的比率，把每种货币换回起点，取最大值。

```python
from collections import defaultdict, deque


def max_amount(initial: str, pairs1: list[tuple[str, str]], rates1: list[float],
               pairs2: list[tuple[str, str]], rates2: list[float]) -> float:
    def reach(pairs: list[tuple[str, str]], rates: list[float]) -> dict[str, float]:
        g: defaultdict[str, list[tuple[str, float]]] = defaultdict(list)
        for (a, b), r in zip(pairs, rates):
            g[a].append((b, r))
            g[b].append((a, 1.0 / r))
        amount = {initial: 1.0}
        queue = deque([initial])
        while queue:
            cur = queue.popleft()
            for nxt, r in g[cur]:
                if nxt not in amount:
                    amount[nxt] = amount[cur] * r
                    queue.append(nxt)
        return amount

    day1, day2 = reach(pairs1, rates1), reach(pairs2, rates2)
    return max(amt / day2[c] for c, amt in day1.items() if c in day2)
```

   `EUR` 起步、第一天 `[EUR->USD 2.0, USD->JPY 3.0]`、第二天 `[JPY->USD 4.0, USD->CHF 5.0, CHF->EUR 6.0]` → `720.0`；`NGN` 起步、两天都只有 `NGN->EUR`，分别是 `9.0` 和 `6.0` → `1.5`。
3. **套利与精度**：取 `-log(rate)` 当边权，若图里存在负环，说明沿着环兑换一圈能增值，用 Bellman-Ford 检测；并查集默认汇率一致，遇到矛盾只会保留先到的那条。精度：汇率是整数比时用 `fractions.Fraction`，结果精确；十进制金额用 `decimal.Decimal`。比较时用容差，不要 `==`。

**Python 提醒**：`float` 连乘的误差会累积；`math.isclose(a, b, rel_tol=1e-9)` 比较浮点数；`1.0 / r` 当 `r` 是 `0` 会 `ZeroDivisionError`，汇率输入要先校验为正。
