---
id: tlc-maximize-amount-after-two-days-of-conversions-2-code
node: a.maximize-amount-after-two-days-of-conversions
type: qa
step: 2
---
## Q
**LC 3387 两天自由外汇交易后的最大货币数**｜写出 Python 实现

初始货币 `initialCurrency`，数量 `1.0`。第 1 天的兑换规则 `pairs1`、`rates1`，第 2 天的 `pairs2`、`rates2`，每个 `[a, b]` 的汇率 `rate` 表示 `1` 个 `a` 换 `rate` 个 `b`，反向是 `1 / rate`。每天可兑换任意次，保证每天的图无矛盾、无环。返回两天后最多能有多少 `initialCurrency`。

## A
**思路。** 写一个 `rates_from(src, pairs, rates)`：建无向图，边 `a → b` 权为 `rate`，`b → a` 权为 `1 / rate`；从 `src` 出发 DFS，`amount[v] = amount[u] * 边权`，首次到达即记录。用它分别算出 `day1`、`day2`，再对两张图都含有的货币取 `day1[c] / day2[c]` 的最大值。

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

运行（保留 5 位小数）：示例 1 → `720.0`；示例 2 → `1.5`；示例 3 → `1.0`；`("A", [["B","C"]], [2.0], [["B","C"]], [3.0])`（汇率都与初始货币不相连）→ `1.0`。

**复杂度。** 时间 `O(n + m)`：两天各一次建图加一次 DFS；空间 `O(n + m)`。

**写法要点。** `zip(pairs, rates)` 里 `(a, b), r` 直接解包嵌套的 `[a, b]`；`defaultdict(list)` 建邻接表；`dict` 既记录数值又兼任 `visited`；`max(... for c, a in day1.items() if c in day2)` 一个生成器表达式完成枚举与过滤，初始货币总在两个字典里，所以结果至少是 `1.0`，不会对空序列取 `max`；函数参数名沿用题目的驼峰（`initialCurrency`），内部函数写成蛇形。
