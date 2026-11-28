---
id: mlp-coding-pc12-solve
node: coding.pc12
step: 1
type: qa
---
## Q
**盈亏计算（PnL）：题与解**｜编程轮

给一串按时间顺序的成交 `(symbol, 买卖方向, 数量, 价格)` 和每个 symbol 的最新价，算总的已实现盈亏（realized PnL，已经平掉的仓位赚了多少）和未实现盈亏（unrealized PnL，还没平的仓位按最新价算赚了多少）。买卖配对用先进先出（FIFO，先开的仓先被平）。要处理部分成交、卖空（short，先卖后买，价格跌了才赚）和每笔手续费。

## A
**一句话思路。** 每个 symbol 维护一个未平仓批次（lot，一次开仓留下的数量和成本价）的队列，买为正、卖为负。新成交如果和队首方向相反，就先平最老的批次，每次配对赚 `数量 × (卖价 − 买价)`；平完还有剩余就开新批次，卖空就是这样出现的。最后用最新价给剩下的批次估值。金额用 `Decimal`。

```python
from collections import defaultdict, deque
from decimal import Decimal

def pnl(trades, marks, fee=Decimal(0)):
    """trades: (symbol, 'B'/'S', 数量, 价格)，按时间顺序；marks: {symbol: 最新价}。"""
    lots = defaultdict(deque)                  # symbol -> 未平仓批次 [带符号数量, 成本价]，先开的在左
    realized = Decimal(0)
    for sym, side, qty, px in trades:
        qty, px = Decimal(qty), Decimal(px)
        signed = qty if side == "B" else -qty  # 买为正，卖为负
        q = lots[sym]
        while signed and q and (q[0][0] > 0) != (signed > 0):   # 方向相反：先平最老的批次
            lot = q[0]
            m = min(abs(signed), abs(lot[0]))                   # 这次配对的数量
            sign = 1 if lot[0] > 0 else -1                      # 多头批次赚 卖价-成本；空头批次赚 成本-买价
            realized += sign * m * (px - lot[1])
            lot[0] -= sign * m
            signed += sign * m
            if lot[0] == 0:
                q.popleft()
        if signed:                                              # 平完还有剩：开新批次（空头也在这里）
            q.append([signed, px])
        realized -= fee                                         # 每笔成交一次手续费
    unrealized = sum((lot[0] * (Decimal(marks[s]) - lot[1])
                      for s, q in lots.items() for lot in q), Decimal(0))
    return realized, unrealized

T = [("A", "B", 10, "10"), ("A", "B", 10, "12"), ("A", "S", 15, "13")]
assert pnl(T, {"A": "14"}) == (35, 10)       # 平 10@10 赚 30，再平 5@12 赚 5；剩多头 5@12，标 14 赚 10
assert pnl([("A", "S", 10, "20"), ("A", "B", 4, "18")], {"A": "17"}) == (8, 18)   # 空头平 4 手赚 8；剩空 6@20，标 17 赚 18
assert pnl([("A", "B", 5, "10"), ("A", "S", 8, "11")], {"A": "11"}) == (5, 0)     # 先平 5 手，多卖的 3 手开空头
assert pnl([("A", "B", 1, "10"), ("A", "S", 1, "11")], {}, fee=Decimal("0.5")) == (0, 0)  # 赚 1，两笔手续费共 1
```

**复杂度。** 每笔成交至多新增一个批次，每个批次至多被弹出一次，所以整体 O(n)；空间是未平仓批次数。

**边写边讲。**
- "I match **FIFO**: a closing trade consumes the oldest open lot first, and may span several lots."
- "I keep **signed quantity**, so shorts need no special case: when a sell outruns the longs, the leftover opens a negative lot."
- "I use **Decimal** for prices, and fees are subtracted from realized PnL."
