# hc05 · Market Order Book（FastPrep「Market Order Book」+ 并入 hc14「Limit Order Matching」）

> 阶段：电面（FastPrep 标 Phone Screen，lastSeen 2026-06-25）· 置信度：**中**（FastPrep 1 + Glassdoor Amsterdam 2026-02 1，共 2 个独立来源）
> 证据只有两句话：FastPrep 题面第一句 "Implement a finite in-memory order book for one instrument. Process the operations in o…"（被截断），
> Glassdoor 的 "making market order book in c++"；hc14 只有 "Process the finite orders batch in arrival order. Every row is [side,price,quantity]…"。
> **所以本题的操作集合、事件格式、校验规则、Part 的划分全部是 (reconstructed)**——按「一小时电面里面试官会怎么一路追问」推出来的。真题的细节以你实际看到的为准。

## 读题前你需要知道

* **订单簿（order book）**是什么、**买盘 / 卖盘 / 最优价 / 价位 / 价格-时间优先**各是什么意思；
* **红黑树（TreeMap）**为什么能在 O(log n) 里取到「最小的价格」，**LinkedHashMap** 为什么能同时做到 O(1) 按 id 删除又保持先后顺序；
* 为什么性能题里「装箱（boxing）」和「每次操作 new 一个对象」会成为问题。

这些都在讲义里从零讲：`study/30-articles/hc05_market_order_book.md`（先读第 1–2 节再动手）。

## 背景

交易所对每个品种维护一本**订单簿**：想买的人挂**买单**（BUY / bid），想卖的人挂**卖单**（SELL / ask），每张单有 `id`、价格、数量。
价格以整数 **tick**（最小报价单位）表示，数量是整数。买盘里出价最高的叫 **best bid**，卖盘里要价最低的叫 **best ask**。
新来一张单如果「买价 ≥ 当前最低卖价」（或「卖价 ≤ 当前最高买价」），就会和簿上的单**成交**；剩下没成交的挂在簿上等人来吃。

你要实现一个单品种、内存里、容量有限的订单簿，分四步走。

## Part 一览

| Part | 入口 | 内容 |
|---|---|---|
| 1 | `OrderBook.add / cancel / modify / bestBid / bestAsk / depth / find / queue / size` | 只维护，**不撮合**：挂单、撤单、改量、查最优价、查 N 档深度、同价位 FIFO |
| 2 | `OrderBook.execute(Command)` → `List<Event>`，`parse` / `render` / `replay` | 价格-时间优先撮合：限价单、市价单、撤单、改量，产出 sealed 事件流 |
| 3 | `BatchMatcher.run(long[][] rows)` → `Summary` | hc14：一批 `[side, price, qty]` 按到达顺序撮合，汇总成交、成交量、名义金额、剩余盘口 |
| 4 | `TickBook`（`limit` / `cancel` / `bestBid` / `bestAsk` / `qtyAt`） | 性能追问：价格用 `long` tick、不装箱、O(1) 按 id 撤单、稳态零分配 |

`Side`、`Level`、`Order`、`Command`（`Limit` / `Market` / `Cancel` / `Modify`）、`Event`（`Trade` / `Rested` / `Cancelled` / `Modified` / `Rejected`）、
`Summary` 在 starter 里已给出。签名以 starter 为准，这里只写语义。

## Part 1 · 维护（不撮合）

* `add(id, side, price, qty)`：挂单到对应方向、对应价位的**队尾**。`id > 0`、`price > 0`、`qty > 0`，否则 `IllegalArgumentException`
  （信息分别是 `invalid id` / `invalid price` / `invalid quantity`，按这个顺序检查）；`id` 已在簿上（不论方向）→ `IAE("duplicate id")`；
  `side == null` → NPE。`add` **不撮合**：买 105 的单可以和卖 100 的单同时躺在簿上（簿可以是「交叉」的）。
* `cancel(id)` → 撤掉返回 `true`，不存在返回 `false`。撤掉之后这个 `id` 可以再用。
* `modify(id, newQty)`：只改数量。`newQty ≤ 0` → `IAE`（**即使 id 未知**，先报参数错）；未知 id → `false`。
  **减量保持队列位置；增量丢失时间优先（移到该价位的队尾）；等量什么都不变。** (reconstructed：真实交易所通用规则，真题未必这么说)
* `bestBid()` / `bestAsk()` → `OptionalLong`；空盘口为 `empty`。
* `depth(side, n)` → 最优的 `n` 档 `List<Level>`，`Level(price, totalQty, orderCount)`。买盘价格降序、卖盘升序；`n` 大于档数则返回全部；`n < 0` → `IAE`。
* `find(id)` → `Optional<Order>`（当前剩余量）；`queue(side, price)` → 该价位的订单 id，队头在前；`size()` → 簿上订单总数。
* **溢出**：同一价位的总量超过 `Long.MAX_VALUE` 时 `add` / `modify` 抛 `ArithmeticException`，**簿保持原样**。价格可以是 `Long.MAX_VALUE`。

## Part 2 · 撮合 + 事件

`execute(cmd)` 执行一条命令，返回它产生的事件（按发生顺序）：

| 命令 | 语义 | 事件 |
|---|---|---|
| `Limit(id, side, price, qty)` | 买单：只要最低卖价 ≤ `price` 就吃；卖单：只要最高买价 ≥ `price` 就吃。**价格优先，同价按到达顺序（时间优先）**。成交价 = **被动方（簿上那张）的价**。吃不完的部分挂簿 | 若干 `Trade(takerId, makerId, takerSide, price, qty)`，剩余非 0 再来一个 `Rested(id, side, price, remaining)` |
| `Market(id, side, qty)` | 不限价，吃到没有对手盘为止；吃不完的部分**作废**（IOC） | 若干 `Trade`；有剩余则 `Cancelled(id, remaining)` |
| `Cancel(id)` | 撤单 | `Cancelled(id, remaining)` |
| `Modify(id, newQty)` | 同 Part 1 的 `modify`；**不触发撮合** | `Modified(id, oldQty, newQty)` |

任何失败都返回**单个** `Rejected(id, reason)` 且**不改变簿**，检查顺序 `id → price → quantity → 簿状态`：

`invalid id` · `invalid price` · `invalid quantity` · `duplicate id`（新单的 id 已在簿上）· `unknown id`（撤 / 改一个不在簿上的 id，包括已成交完的）· `overflow`（见下）。

`overflow`：限价单挂簿后会让**自己那一侧同价位**总量溢出 → 整单拒绝，**且不先去吃对手盘**（保守检查，保证原子）；`Modify` 增量溢出同理。

**文本接口**（`parse` / `render` / `replay`，方便写样例）：

```
LIMIT id BUY|SELL price qty     MARKET id BUY|SELL qty     CANCEL id     MODIFY id newQty
```

大小写不敏感、空白任意；`replay` 跳过空行和 `#` 开头的行，格式错抛 `IAE`，信息以 `line N` 开头（N 从 1 起）。事件渲染：

```
TRADE taker=%d maker=%d side=%s px=%d qty=%d      REST id=%d side=%s px=%d qty=%d      CANCEL id=%d remaining=%d
MODIFY id=%d old=%d new=%d                          REJECT id=%d reason=%s
```

### 样例

输入：

```
# 样例
LIMIT 1 SELL 101 5
LIMIT 2 SELL 101 3
LIMIT 3 SELL 102 4

LIMIT 4 BUY 101 6
limit 5 buy 103 10
MARKET 6 SELL 5
CANCEL 3
MODIFY 9 1
```

输出：

```
REST id=1 side=SELL px=101 qty=5
REST id=2 side=SELL px=101 qty=3
REST id=3 side=SELL px=102 qty=4
TRADE taker=4 maker=1 side=BUY px=101 qty=5
TRADE taker=4 maker=2 side=BUY px=101 qty=1
TRADE taker=5 maker=2 side=BUY px=101 qty=2
TRADE taker=5 maker=3 side=BUY px=102 qty=4
REST id=5 side=BUY px=103 qty=4
TRADE taker=6 maker=5 side=SELL px=103 qty=4
CANCEL id=6 remaining=1
REJECT id=3 reason=unknown id
REJECT id=9 reason=unknown id
```

手算：订单 4 买 101 × 6，吃掉最低价 101 档的队头：先 1 号（5），再 2 号（1）；5 号买 103 × 10，先吃 2 号剩下的 2，再吃 102 的 3 号 4 张，剩 4 张挂在 103；
6 号市价卖 5，只有 5 号的 4 张可吃，剩 1 作废；3 号早被吃光，所以 `CANCEL 3` 被拒。

## Part 3 · 批量限价撮合（hc14）

`BatchMatcher.run(long[][] rows)`：`rows[i] = {side, price, qty}`，`side`：`0 = BUY`，`1 = SELL`（**(reconstructed)**，真题编码未知）；第 `i` 行订单的 `id = i + 1`。
按行序当作限价单依次撮合（直接复用 Part 2），返回

```
Summary(trades, filledQty, notional, bids, asks)
```

* `trades`：全部成交（顺序同事件流）；`filledQty`：成交总量（每笔只算一次）；`notional`：Σ price × qty；`bids` / `asks`：最终盘口，全部档位，最优在前。
* 先**整体校验**再处理：行长度 ≠ 3、`side ∉ {0,1}`、`price ≤ 0`、`qty ≤ 0` → `IAE`，信息以 `row i`（i 从 0 起）开头；`rows == null` → NPE。
* `notional` 溢出 → `ArithmeticException`（`4e9 × 3e9` 就会溢出）。

样例：`{{0,100,5},{1,99,3},{1,100,4},{0,101,10}}` → 成交 `(2,1,SELL,100,3)`、`(3,1,SELL,100,2)`、`(4,3,BUY,100,2)`；`filledQty = 7`，`notional = 700`；
`bids = [Level(101, 8, 1)]`，`asks = []`。

## Part 4 · 性能追问：不装箱的 `TickBook`

面试官：「你的 `OrderBook` 每秒要处理几百万条命令。profile 显示 GC 很忙。怎么办？」

`TickBook(int maxTicks, int capacity)`：价格是 `long` tick，合法范围 `1..maxTicks-1`；同时挂簿订单数不超过 `capacity`（≤ 2^22）。

* `limit(id, side, price, qty, sink)`：撮合语义同 Part 2 的 `Limit`，但成交通过回调 `TradeSink.onTrade(takerId, makerId, price, qty)` 报告，**不创建事件对象**。
  返回挂簿的剩余量（0 = 全部成交）；非法返回 `REJECTED`（id ≤ 0、id 已在簿上、价格不在带内、`qty ∉ 1..MAX_QTY`）；池满返回 `FULL`（此时**不撮合**）。
* `cancel(id)`：O(1) 按 id 撤单。`bestBid()` / `bestAsk()`：没有返回 `NONE (-1)`。`qtyAt(side, price)`：价位总量，带外返回 0。`liveOrders()`。
* 要求：2,000,000 次随机操作 < 2 s；稳态（预热后）60 万次操作分配 < 512 KB；与 Part 2 的 `OrderBook` 逐步对拍结果一致。
* `MAX_QTY = 2^40`：单笔数量上限，保证「2^22 张 × 2^40」仍装得进 `long`，从源头消灭价位总量溢出。

## 边界清单（隐藏测试多半打这些）

空盘口；同价 FIFO；部分成交的 maker 留在队头；成交价取 maker 价；`add` 不撮合；增量 modify 丢优先级、减量不丢；已成交 / 已撤的 id 可复用；
`qty = 0` / 负数 / `price = 0`；同价位总量到 `Long.MAX_VALUE` 的边界；市价单遇空盘；撤单后最优价要跳到下一档（跨很多空档）；池满。

## 野外变体

* 真题可能只有 `add / cancel / best` 而没有 modify；或者要求按「操作序列」输入、输出每步之后的 best bid/ask。
* 面试官常见追问：撤单怎么做到 O(1)？同价位怎么保证先来先成交？为什么用 `long` 不用 `double`？（见 REPORT 追问）
* C++ 版（Glassdoor）：`std::map<Price, std::list<Order>>` + `unordered_map<Id, list::iterator>`，和这里的 Java 版同构。

## 来源

`catalog/raw/github_repos.md` §3.1.A（Market Order Book · Limit Order Matching）；`catalog/raw/forums.md` G2（Glassdoor Amsterdam 2026-02）。
FastPrep 页面：https://www.fastprep.io/problems/headlands-market-order-book · https://www.fastprep.io/problems/headlands-limit-order-matching

## 考什么

不是算法，是**建模与工程判断**：选对数据结构（有序 Map + 带序的队列 + id 索引）、把规则（价格-时间优先、成交价取谁的、减量保优先级）说清楚并实现一致、
用 sealed 类型把结果变成穷尽的代数类型，最后能回答「怎么让它更快」——long tick、数组代替树、预分配池、零分配。
