---
id: tlc-best-time-to-buy-and-sell-stock-iv-5-alt
node: b.best-time-to-buy-and-sell-stock-iv
type: qa
step: 5
---
## Q
**LC 188 买卖股票的最佳时机 IV**｜另一种解法

不用 `O(n·k)` 的状态机 DP，有没有只和价格曲线的“谷与峰”有关的做法？它的复杂度是多少，什么时候选它？

## A
**谷到峰分段，栈合并，取前 `k` 大。** 把价格曲线拆成一段段「谷（局部最低）到峰（局部最高）」，每段是一笔候选交易。用栈保存已经处理的段（谷值递增、峰值递减）：新来的段如果谷更低，旧段就单独成为一笔交易；如果峰更高，就和栈顶的段合并（旧谷到新峰），被合并掉的部分也作为一笔候选。最后栈里剩下的段也加入候选，取利润最大的 `k` 笔求和。

```python
from heapq import nlargest


def max_profit_peaks(k: int, prices: list[int]) -> int:
    profits: list[int] = []
    stack: list[tuple[int, int]] = []            # (谷下标, 峰下标 + 1)，峰值递减、谷值递增
    n, v, p = len(prices), 0, 0
    while p < n:
        v = p
        while v < n - 1 and prices[v] >= prices[v + 1]:
            v += 1
        p = v + 1
        while p < n and prices[p] >= prices[p - 1]:
            p += 1
        while stack and prices[v] < prices[stack[-1][0]]:     # 新谷更低：旧的一段单独成交易
            lv, lp = stack.pop()
            profits.append(prices[lp - 1] - prices[lv])
        while stack and prices[p - 1] >= prices[stack[-1][1] - 1]:   # 新峰更高：与旧段合并
            lv, lp = stack.pop()
            profits.append(prices[lp - 1] - prices[v])
            v = lv
        stack.append((v, p))
    profits.extend(prices[lp - 1] - prices[lv] for lv, lp in stack)
    return sum(nlargest(k, profits))
```

`(2, [3,2,6,5,0,3])` → `7`，`(2, [2,4,1])` → `2`，`(2, [1,2,4,2,5,7,2,4,9,0])` → `13`，与状态机版本的结果一致。时间 `O(n + p log k)`（`p` 是候选交易数，`p <= n`），空间 `O(n)`，与 `k` 的大小几乎无关。

**怎么选。**
- `k` 小（几十以内）、`n` 不大：状态机 DP，十行，不容易写错，面试首选。
- `k` 很大、`n` 很大（`O(n·k)` 不可行）：这个做法 `O(n log n)`；代价是边界条件多，栈里的合并规则不好当场推出，写之前先把规则讲清楚。
- 面试里的顺序：先写状态机 DP；被追问 `k` 很大时，再讲“谷到峰加栈合并”或 aliens trick 的思路。
