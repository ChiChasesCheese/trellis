---
id: hl-hc05-sample-trace
node: problems.hc05-market-order-book
type: qa
step: 10
---
## Q
手跑订单簿样例：卖单 #1 卖 101×5、#2 卖 101×3、#3 卖 102×4，然后 `LIMIT 4 BUY 101 6`、`LIMIT 5 BUY 103 10`、`MARKET 6 SELL 5`、`CANCEL 3`、`MODIFY 9 1`，事件是什么？

## A
前三条各产生 `REST`（#1 101×5，#2 101×3，#3 102×4）。

- `LIMIT 4 BUY 101 6`：吃最低价 101 档队头：先 #1 的 5 个 `TRADE taker=4 maker=1 side=BUY px=101 qty=5`，再 #2 的 1 个 `qty=1`；#4 全部成交不挂簿。
- `LIMIT 5 BUY 103 10`：先吃 #2 剩下的 2（px=101），再吃 102 档 #3 的 4 个（px=102，**成交价取 maker 价**）；剩 4 张 `REST id=5 side=BUY px=103 qty=4`。
- `MARKET 6 SELL 5`：只有 #5 的 4 张可吃（`TRADE taker=6 maker=5 side=SELL px=103 qty=4`），剩 1 作废：`CANCEL id=6 remaining=1`。
- `CANCEL 3`：#3 早被吃光 → `REJECT id=3 reason=unknown id`。
- `MODIFY 9 1`：不存在 → `REJECT id=9 reason=unknown id`。

渲染格式：`TRADE taker=%d maker=%d side=%s px=%d qty=%d`、`REST id=%d side=%s px=%d qty=%d`、`CANCEL id=%d remaining=%d`、`MODIFY id=%d old=%d new=%d`、`REJECT id=%d reason=%s`。

另一个练习：卖盘 100:[#1×2,#2×3]，101:[#3×4]，来 `LIMIT 9 BUY 101 8`：Trade(9,1,BUY,100,2)、Trade(9,2,BUY,100,3)、Trade(9,3,BUY,101,3)；#9 吃光不挂簿；剩卖盘 101:[#3×1]，买盘空。
