---
id: hl-hc05-testing
node: problems.hc05-market-order-book
type: qa
step: 17
---
## Q
怎么证明撮合引擎正确？有哪些不变量和边界清单？

## A
三层测试：
1. 手算样例；
2. **不变量**：簿永不交叉（best bid < best ask，撮合后）；数量守恒（提交量 = 2 × 成交量 + 剩余挂单 + 被撤量）；
3. **对拍**：快版本与慢但明显正确的版本喂同一串随机命令逐步比较。

**边界清单**：空盘口；同价 FIFO；部分成交的 maker 留在队头；成交价取 maker 价；`add` 不撮合；增量 modify 丢优先级、减量不丢；已成交 / 已撤的 id 可复用；`qty = 0` / 负数 / `price = 0`；同价位总量到 `Long.MAX_VALUE` 的边界；市价单遇空盘；撤单后最优价要跳到下一档（跨很多空档）；池满。

变体：可能只有 `add / cancel / best` 而没有 modify；或要求按操作序列输入、输出每步之后的 best bid/ask。

**隐藏测试的坑**：
- `add` 去撮合了；
- 成交价取了 taker 的限价；部分成交的 maker 被丢到队尾；
- 增量 modify 不丢优先级 / 减量却丢了；`modify(未知 id, 0)` 该先报参数错；
- 价位空了没从 `TreeMap` 删；
- 总量溢出：`total += qty` 回绕成负数；先改后查导致簿被改了一半；
- 限价单溢出检查放在撮合之后；
- 批量：`price × qty` 溢出（`4e9 × 3e9`）、`rows[i]` 长度不是 3、`side` 不是 0/1。
