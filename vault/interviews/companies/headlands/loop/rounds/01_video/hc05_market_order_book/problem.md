# hc05 · 限价订单簿与撮合

订单簿（order book）是交易所存放所有尚未成交的买单和卖单的数据结构：买盘价格从高到低，卖盘从低到高，同价位按先来后到排队。面试官先让你实现挂单、撤单和查最优价，再加上限价撮合：新订单来了，按价格-时间优先与对手盘成交，吃不完的部分挂在簿上。最后的追问落在性能上，放在口头部分。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "Implement a limit order book for one symbol: add an order, cancel an order, and get the best bid and best ask."
> 接着会问："Now an incoming order should match against the book — price-time priority, partial fills. Return the trades." "How would you make it faster? No allocation on the hot path?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：价格是整数 tick 还是小数？id 是否唯一？`add` 要不要撮合？ |
| 3–15 分钟 | **Part 1**：订单簿的数据结构 |
| 15–30 分钟 | **Part 2**：限价撮合 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 订单簿（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `void add(long id, Side side, long price, long qty)` · `boolean cancel(long id)` · `OptionalLong bestBid()` · `OptionalLong bestAsk()` · `int size()` |
| C++ | `void add(long long id, Side side, long long price, long long qty)` · `bool cancel(long long id)` · `std::optional<long long> best_bid() const` · `best_ask() const` · `std::size_t size() const` |

- 价格是整数（tick），数量是整数。`Side` 是 `BUY` / `SELL`。
- `add` 把订单放到对应价位的队尾，**不撮合**。`price <= 0`、`qty <= 0`、`id` 已在簿上：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- `cancel` 撤掉返回 true，id 不在簿上返回 false。价位上最后一张单被撤掉时，这个价位要从簿里删掉，否则 `bestBid` 会指向一个空价位。
- `bestBid` 是买盘最高价，`bestAsk` 是卖盘最低价，空盘口返回空（`OptionalLong.empty()` / `std::nullopt`）。
- 例子：买 99、买 100、卖 102、卖 101 之后，`bestBid = 100`，`bestAsk = 101`，`size = 4`。

## Part 2 · 限价撮合（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `List<Trade> match(long id, Side side, long price, long qty)`，`Trade(takerId, makerId, price, qty)` |
| C++ | `std::vector<Trade> match(long long id, Side side, long long price, long long qty)`，`Trade{taker_id, maker_id, price, qty}` |

- 买单：只要对手盘最低卖价 ≤ `price` 就吃；卖单：只要最高买价 ≥ `price` 就吃。
- 价格优先：先吃最好的价位。同价位时间优先：先吃先挂的单。
- 成交价是**被动方**（簿上那张）的价，不是新单的限价。
- 部分成交：被吃的单剩余量留在簿上，继续排在原来的位置。新单吃不完的部分挂簿。
- 参数检查和 `add` 一样，而且要在任何成交之前做：id 重复时不改变簿。
- 例子：簿上卖 102×4（1 号）、卖 101×5（2 号）、卖 101×3（3 号）。买 101×6（4 号）得到 `(4,2,101,5)` 和 `(4,3,101,1)`；再买 103×10（5 号）得到 `(5,3,101,2)` 和 `(5,1,102,4)`，剩下 4 张挂在买 103。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 你的数据结构里每个操作的复杂度是多少？为什么撤单是 O(1) 或 O(log n)？
2. 价格范围很小而且密集，怎么把 `TreeMap` / `std::map` 换成更快的结构？
3. 热路径上怎么做到零分配（不装箱、不 new）？
4. 订单簿的延迟瓶颈在哪里？怎么测？
5. 如果要加市价单、改量、止损单，各自要改哪里？
6. 多线程怎么用这个订单簿？

## 边界

- 空盘口
- 撤掉一个价位的最后一张单
- 一张新单吃穿多个价位
- 恰好吃完一张被动单，和只吃掉它的一部分
- 买单和卖单价格恰好相等（算交叉，要成交）

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc05_market_order_book       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc05_market_order_book --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc05_market_order_book       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc05_market_order_book --tag part1
```
