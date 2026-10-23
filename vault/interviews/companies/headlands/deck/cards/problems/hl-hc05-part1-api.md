---
id: hl-hc05-part1-api
node: problems.hc05-market-order-book
type: qa
step: 3
---
## Q
订单簿 Part 1（只维护、不撮合）的 `add`、`cancel`、`modify`、`depth` 各有哪些参数检查和语义规则？

## A
- `add(id, side, price, qty)`：挂到对应方向、对应价位的**队尾**。`id > 0`、`price > 0`、`qty > 0`，否则 `IllegalArgumentException`（信息 `invalid id / invalid price / invalid quantity`，**按此顺序检查**）；`id` 已在簿上（不论方向）→ `IAE("duplicate id")`；`side == null` → NPE。`add` **不撮合**：买 105 的单可以和卖 100 的单同时躺在簿上。
- `cancel(id)`：撤掉返回 `true`，不存在返回 `false`；撤掉后 `id` 可复用。
- `modify(id, newQty)`：只改数量。`newQty ≤ 0` → `IAE`（**即使 id 未知**也先报参数错）；未知 id → `false`。**减量保持队列位置；增量丢失时间优先（移到该价位队尾）；等量什么都不变。**
- `bestBid()` / `bestAsk()` → `OptionalLong`，空盘口为 `empty`。
- `depth(side, n)` → 最优 `n` 档 `List<Level>`，买盘价格降序、卖盘升序；`n` 大于档数返回全部；`n < 0` → `IAE`。
- `find(id)` → `Optional<Order>`（当前剩余量）；`queue(side, price)` → 该价位订单 id，队头在前；`size()` → 总订单数。
- **溢出**：同一价位总量超过 `Long.MAX_VALUE` 时 `add / modify` 抛 `ArithmeticException`，**簿保持原样**；价格可以是 `Long.MAX_VALUE`。
