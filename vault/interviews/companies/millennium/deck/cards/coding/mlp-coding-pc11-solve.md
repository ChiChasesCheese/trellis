---
id: mlp-coding-pc11-solve
node: coding.pc11
step: 1
type: qa
---
## Q
**订单簿撮合引擎：题与解**｜编程轮

实现一个订单簿（order book，按价格排队的买卖委托表）的撮合引擎（matching engine，把买单和卖单配成成交的程序）：`placeOrder` 下限价单（limit order，指定价格，价格不满足就挂着等）或市价单（market order，不限价，有什么吃什么）；`cancelOrder` 撤单；`getExecutedTrades` 返回成交记录；`getOrderQuantity` 返回某单剩余数量；`getBestBid` / `getBestAsk` 返回买一价（最高买价）和卖一价（最低卖价）。规则是价格优先、时间优先（price-time priority）：价格好的先成交，同价先来的先成交；成交价取挂单方的价格。操作最多 10^4 次。

## A
**一句话思路。** 每一侧（买、卖）用一个价格堆找最优价，每个价位一个 `deque` 按先后排队；新单先和对手盘交叉的价位逐个成交，限价单剩下的才挂进簿。撤单不去队伍中间删，只把剩余数量置 0，之后在队首碰到再丢掉（惰性删除，lazy deletion）。

```python
import heapq
from collections import deque

class OrderBook:
    def __init__(self):
        self.orders = {}                       # id -> [side, price, 剩余数量]
        self.level = {"B": {}, "S": {}}        # side -> {价格: 排队的订单 id（先来的在左）}
        self.heap = {"B": [], "S": []}         # 价格堆：买盘存负价，两边堆顶都是最优价
        self.trades = []                       # (taker id, maker id, 成交价, 成交量)

    def _best(self, side):
        """返回最优价；堆顶价位上已无有效订单就弹掉（惰性清理）。"""
        h, lv = self.heap[side], self.level[side]
        while h:
            p = h[0] if side == "S" else -h[0]
            q = lv.get(p)
            while q and self.orders[q[0]][2] == 0:   # 队首是已撤/已成交的，丢掉
                q.popleft()
            if q:
                return p
            lv.pop(p, None)
            heapq.heappop(h)
        return None

    def placeOrder(self, oid, side, price, qty):
        """price=None 是市价单。先吃对手盘，限价单剩余的挂进簿。"""
        other = "S" if side == "B" else "B"
        order = self.orders[oid] = [side, price, qty]
        while order[2] > 0:
            best = self._best(other)
            if best is None:
                break
            if price is not None and (best > price if side == "B" else best < price):
                break                                   # 价格不交叉，停
            q = self.level[other][best]
            maker = self.orders[q[0]]
            fill = min(order[2], maker[2])
            self.trades.append((oid, q[0], best, fill))   # 成交价是挂单方的价格
            order[2] -= fill
            maker[2] -= fill
            if maker[2] == 0:
                q.popleft()
        if order[2] > 0 and price is not None:
            lv = self.level[side]
            if price not in lv:
                lv[price] = deque()
                heapq.heappush(self.heap[side], price if side == "S" else -price)
            lv[price].append(oid)                       # 排在同价位队尾：时间优先
        else:
            order[2] = 0                                # 市价单没吃完的部分作废

    def cancelOrder(self, oid):
        o = self.orders.get(oid)
        if o is None or o[2] == 0:
            return False
        o[2] = 0                                        # 惰性删除：只置零，留给 _best 清理
        return True

    def getOrderQuantity(self, oid):
        o = self.orders.get(oid)
        return o[2] if o else 0

    def getBestBid(self):
        return self._best("B")

    def getBestAsk(self):
        return self._best("S")

    def getExecutedTrades(self):
        return list(self.trades)

b = OrderBook()
b.placeOrder(1, "S", 101, 5)
b.placeOrder(2, "S", 100, 3)
b.placeOrder(3, "B", 99, 4)
assert (b.getBestBid(), b.getBestAsk()) == (99, 100)
b.placeOrder(4, "B", 101, 6)               # 先吃 100 的 3 手，再吃 101 的 3 手
assert b.getExecutedTrades() == [(4, 2, 100, 3), (4, 1, 101, 3)]
assert b.getOrderQuantity(1) == 2 and b.getOrderQuantity(4) == 0
assert b.cancelOrder(1) and b.getBestAsk() is None
b.placeOrder(5, "S", 99, 2)                # 与买一 99 交叉
assert b.getExecutedTrades()[-1] == (5, 3, 99, 2)
```

**复杂度。** 挂单 O(log P)（P 是不同价位数，堆操作）；每次成交 O(1)，一笔新单的成交数不超过它吃掉的挂单数；撤单 O(1)；买一卖一均摊 O(1)，惰性清理的每个废单只丢一次。

**边写边讲。**
- "Each side is a **heap of prices**, and each price level is a **FIFO queue**, so I get price priority and then time priority."
- "A trade happens at the **resting order's price**, not the incoming one's."
- "Cancel just **zeroes the remaining quantity**; stale entries are dropped lazily when they reach the front."
- "A market order never rests: whatever it can't fill is discarded."
