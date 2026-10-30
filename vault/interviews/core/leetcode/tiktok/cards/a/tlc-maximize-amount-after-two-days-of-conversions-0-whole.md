---
id: tlc-maximize-amount-after-two-days-of-conversions-0-whole
node: a.maximize-amount-after-two-days-of-conversions
type: qa
---
## Q
**LC 3387 两天自由外汇交易后的最大货币数**｜Medium · 近一年被问：美国 3 次、国内 0 次 · 最近 2026-01-05（面试记录）

给字符串 `initialCurrency`，表示初始货币，你一开始有 `1.0` 单位。另给四个数组：`pairs1[i] = [start, target]` 表示在**第 1 天**可以按汇率 `rates1[i]` 把 `start` 换成 `target`；`pairs2[i]` 与 `rates2[i]` 表示**第 2 天**的兑换。此外每种 `target` 都可以按汇率 `1 / rate` 换回对应的 `start`。你可以在第 1 天用 `rates1` 兑换任意次（包括 `0` 次），然后在第 2 天用 `rates2` 再兑换任意次。返回两天兑换后**最多能拥有的 `initialCurrency` 数量**。保证两天各自的汇率图内部没有矛盾、没有环。`1 <= initialCurrency.length <= 3`（大写字母），`1 <= pairs1.length, pairs2.length <= 10`，货币名 `1` 到 `3` 个大写字母，`1.0 <= rates1[i], rates2[i] <= 10.0`，输出最大为 `5 * 10^10`。例：`initialCurrency = "EUR"`，`pairs1 = [["EUR","USD"],["USD","JPY"]]`，`rates1 = [2.0, 3.0]`，`pairs2 = [["JPY","USD"],["USD","CHF"],["CHF","EUR"]]`，`rates2 = [4.0, 5.0, 6.0]` → `720.0`；`initialCurrency = "NGN"`，`pairs1 = [["NGN","EUR"]]`，`rates1 = [9.0]`，`pairs2 = [["NGN","EUR"]]`，`rates2 = [6.0]` → `1.5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每天的汇率图没有矛盾也没有环，所以任意两种货币之间的换算比是**唯一**的，不需要最短路：先在第 1 天的图上 DFS 算出 `1` 个初始货币能换成每种货币 `c` 的数量 `day1[c]`；再在第 2 天的图上算 `day2[c]`（同样从 `1` 个初始货币出发），第 2 天把 `c` 换回初始货币的比率就是 `1 / day2[c]`；答案是对两天都出现的货币 `c`，取 `day1[c] / day2[c]` 的最大值。`O(n + m)`。

**识别。** 「两阶段换汇 + 求最大」。关键是图性质：保证无矛盾、无环，说明每个连通分量是一棵树，任意两点间只有一种换算，不存在套利，DFS 一次传播汇率就够，不必 Floyd 或 Bellman-Ford。两阶段的衔接：第 1 天结束时手里是某种货币 `c`，第 2 天要把它换回初始货币，这条通路必须在第 2 天的图里存在。

**推导。** 暴力：枚举第 1 天结束时持有的货币 `c`，枚举 `c` 在第 2 天换回初始货币的所有路径，要先求任意两点的换算 → 无环无矛盾，从初始货币出发 DFS 一次，就得到它到每种货币的比率；`c` 换回初始货币的比率就是这个比率的倒数（反向边的汇率 `1 / rate`） → 两天各做一次 DFS，再枚举中转货币 `c` 取最大。

```python
from collections import defaultdict


def max_amount(initialCurrency: str, pairs1: list[list[str]], rates1: list[float],
               pairs2: list[list[str]], rates2: list[float]) -> float:
    def rates_from(src: str, pairs: list[list[str]], rates: list[float]) -> dict[str, float]:
        graph: defaultdict[str, list[tuple[str, float]]] = defaultdict(list)
        for (a, b), r in zip(pairs, rates):
            graph[a].append((b, r))                # 正向：1 个 a 换 r 个 b
            graph[b].append((a, 1 / r))            # 反向：1 个 b 换 1/r 个 a
        amount = {src: 1.0}                        # amount[c]：1 个 src 能换到几个 c
        stack = [src]
        while stack:
            u = stack.pop()
            for v, r in graph[u]:
                if v not in amount:                # 无矛盾无环：任何路径换算结果一样，首次到达即可
                    amount[v] = amount[u] * r
                    stack.append(v)
        return amount

    day1 = rates_from(initialCurrency, pairs1, rates1)
    day2 = rates_from(initialCurrency, pairs2, rates2)
    # 第 1 天把 1 个初始货币换成 c 得 day1[c] 个；第 2 天 c 换回初始货币的比率是 1 / day2[c]
    return max(a / day2[c] for c, a in day1.items() if c in day2)
```

运行：示例 1 → `720.0`；示例 2 → `1.5`；`("USD", [["USD","EUR"]], [1.0], [["EUR","JPY"]], [10.0])` → `1.0`（什么都不换）；`("A", [["B","C"]], [2.0], [["B","C"]], [3.0])`（汇率都与初始货币不相连）→ `1.0`。

**复杂度。** 时间 `O(n + m)`；空间 `O(n + m)`，货币种类至多 `20` 种。

**易错点。**
- 漏掉反向边 `1 / rate`：示例 1 的第 2 天只有 `JPY → USD → CHF → EUR`，从 `EUR` 出发正向走不到任何货币，只剩 `EUR` 自己，结果 `1.0`，正确是 `720.0`。
- 把第 2 天的换回比率写成 `day2[c]`（应该是它的倒数）：示例 2 得到 `9 * 6 = 54.0`，正确是 `9 / 6 = 1.5`。
- 只枚举第 1 天图里的货币 `c`，但没有检查 `c` 在第 2 天图里是否存在：不存在的货币第 2 天换不回来，必须排除（代码里的 `if c in day2`）。

**追问。**
- 不依赖"无矛盾、无环"的保证：改成每天做 Bellman-Ford 式松弛（每条边正反各松弛一次，最多重复"边数 + 1"轮），状态是「手里每种货币的最大数量」。有套利环时数值会无限增长，要用对数加检测正环，或限制轮数。
- 不止两天，`d` 天：把第 1 天的 `day1` 作为第 2 天的初值，逐天做松弛，最后读出初始货币的数量。
- 要求最少兑换次数：在 DFS / BFS 中再记录步数。

**同模式。** LC 399 除法求值、LC 1514 概率最大的路径、LC 787 K 站中转内最便宜的航班、LC 743 网络延迟时间、LC 997 找到小镇的法官。
