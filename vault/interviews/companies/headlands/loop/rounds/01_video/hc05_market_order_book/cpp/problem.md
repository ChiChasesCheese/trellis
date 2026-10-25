# hc05 · Market Order Book（订单簿 + 限价撮合，C++20 版）

订单簿是交易所存放所有尚未成交的买单和卖单的数据结构：买盘按价格从高到低、卖盘从低到高排列，同价位按先来后到排队。你要实现下单、撤单、改量、查最优价，再加限价撮合：新订单来了，按价格-时间优先与对手盘成交。最后的追问落在性能上：热路径不分配内存。C++ 版的重点是：用节点式容器（`std::map` / `std::list`）存迭代器做到 O(1) 撤单、用 `std::variant` 表示命令和事件、有符号溢出是 UB、`from_chars` 做严格解析，以及 `TickBook` 的预分配和零分配。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `book`）。

## 读题前你需要知道

- **买盘 / 卖盘 / 最优价**：想买的人挂买单（bid），想卖的人挂卖单（ask）。买盘里出价最高的叫 best bid，卖盘里要价最低的叫 best ask。
- **价格-时间优先**：先比价格（买方价高者先成交，卖方价低者先成交），同价按到达顺序。**成交价取被动方（簿上那张）的价**。
- **tick**：最小报价单位。价格用整数 tick 表示，数量也是整数；不用 `double`，因为浮点数存不准十进制小数，相等的价格可能分进两个价位。
- **迭代器失效**（iterator invalidation）：`std::map` 和 `std::list` 在插入或删除**别的**元素时，不会让已有元素的迭代器失效；`std::vector` 一增长，所有迭代器和引用都悬空。
- **未定义行为**（undefined behavior，UB）：有符号整数溢出就是 UB，所以溢出检查要在加之前做，或者用 `__builtin_add_overflow`。

## 公共类型（starter 已给出）

```cpp
enum class Side { Buy, Sell };
struct Level { long long price; long long total_qty; int order_count; };   // 一个价位
struct Order { long long id; Side side; long long price; long long qty; }; // 簿上一张单，qty = 剩余量

struct Limit  { long long id; Side side; long long price; long long qty; };
struct Market { long long id; Side side; long long qty; };
struct Cancel { long long id; };
struct Modify { long long id; long long new_qty; };
using Command = std::variant<Limit, Market, Cancel, Modify>;

struct Trade     { long long taker_id, maker_id; Side taker_side; long long price, qty; };
struct Rested    { long long id; Side side; long long price, qty; };
struct Cancelled { long long id; long long remaining; };
struct Modified  { long long id; long long old_qty, new_qty; };
struct Rejected  { long long id; std::string_view reason; };   // reason 是下面的静态常量之一
using Event = std::variant<Trade, Rested, Cancelled, Modified, Rejected>;

// INVALID_ID "invalid id" · INVALID_PRICE "invalid price" · INVALID_QTY "invalid quantity"
// DUPLICATE_ID "duplicate id" · UNKNOWN_ID "unknown id" · OVERFLOW_REASON "overflow"
```

所有类型都带 `operator==`。`OrderBook` 的拷贝构造和拷贝赋值已经 `= delete`，移动构造和移动赋值是 `noexcept` 的 `= default`。

## Part 1 · 维护（不撮合）

| 签名 | 要求 |
|---|---|
| `void add(long long id, Side, long long price, long long qty)` | 挂到对应价位的**队尾**，**不撮合**（买 105 和卖 100 可以同时躺在簿上）。按顺序检查：`id <= 0`、`price <= 0`、`qty <= 0`、重复 id（不论方向），都抛 `std::invalid_argument`，消息分别是 `INVALID_*` / `DUPLICATE_ID` 的文本。同价位总量溢出抛 `std::overflow_error`，簿保持原样 |
| `bool cancel(long long id)` | 撤掉返回 `true`，不存在返回 `false`；撤掉之后这个 id 可以再用 |
| `bool modify(long long id, long long new_qty)` | 只改数量。`new_qty <= 0` 抛 `invalid_argument`（**即使 id 未知**）；未知 id 返回 `false`；总量溢出抛 `overflow_error` |
| `std::optional<long long> best_bid() const` · `best_ask() const` | 空盘口返回 `std::nullopt` |
| `std::vector<Level> depth(Side, int n) const` | 最优的 n 档：买盘价格降序、卖盘升序；n 大于档数返回全部；`n < 0` 抛 `invalid_argument` |
| `std::optional<Order> find(long long id) const` | 当前剩余量 |
| `std::vector<long long> queue(Side, long long price) const` | 该价位的订单 id，队头在前；没有这个价位返回空 |
| `std::size_t size() const noexcept` | 簿上订单总数 |

- **改量规则**：减量保持队列位置；增量丢失时间优先（移到该价位的队尾）；等量什么都不变。例：同价 1、2、3 号各 10，`modify(1, 4)` 后队列仍是 `{1, 2, 3}`，该价位总量 24；`modify(1, 5)` 后队列是 `{2, 3, 1}`，总量 25；此时 `modify(1, 6)` 队列仍是 `{2, 3, 1}`。
- 同价位 FIFO：依次 add 7、3、9 号，`queue` 是 `{7, 3, 9}`。
- 撤中间一张后总量和档数要更新；价位撤空后，`best_bid` 要跳到下一档。
- 深度例：买盘 100 价位两张（5 和 7）、99 价位一张（3），`depth(Buy, 10)` 是 `{100, 12, 2}, {99, 3, 1}`；`depth(Sell, 0)` 为空。
- 溢出：先挂 `price = LLONG_MAX`、`qty = LLONG_MAX − 5`，价格可以是 `LLONG_MAX`；再挂同价位 6 张要抛 `overflow_error`，`size()` 和总量不变；挂 5 张恰好到顶，合法；之后 `modify(2, 6)` 抛 `overflow_error`，订单 2 的量仍是 5。
- 参数检查顺序：`add(0, Buy, 0, 0)` 报的是 `invalid id`。`modify(404, q)` 对 `q` 取 0、−1、`LLONG_MIN` 都抛 `invalid_argument`。
- 性能：20 万次 add（价格 1..5000）加 10 万次 cancel，2 秒内。

## Part 2 · 撮合 + 事件

| 签名 | 要求 |
|---|---|
| `std::vector<Event> execute(const Command&)` | 执行一条命令，返回它产生的事件（按发生顺序） |
| `std::vector<Event> execute_all(const std::vector<Command>&)` | 依次执行，事件拼在一起 |
| `Command parse(std::string_view line)` | 解析一行；格式错抛 `std::invalid_argument` |
| `std::string render(const Event&)` | 渲染一个事件 |
| `std::vector<std::string> replay(const std::vector<std::string>&)` | 在新簿上依次执行脚本，返回渲染后的事件行；跳过空行和 `#` 开头的行 |

| 命令 | 语义 | 事件 |
|---|---|---|
| `Limit` | 买单：只要最低卖价 ≤ `price` 就吃；卖单：只要最高买价 ≥ `price` 就吃。价格优先，同价按到达顺序。成交价 = 被动方的价。吃不完的部分挂簿 | 若干 `Trade`；剩余非 0 再来一个 `Rested{id, side, price, remaining}` |
| `Market` | 不限价，吃到没有对手盘为止；吃不完的部分**作废** | 若干 `Trade`；有剩余则 `Cancelled{id, remaining}` |
| `Cancel` | 撤单 | `Cancelled{id, remaining}` |
| `Modify` | 同 Part 1 的 `modify`；**不触发撮合** | `Modified{id, old, new}` |

任何失败都返回**单个** `Rejected{id, reason}` 且**不改变簿**，检查顺序 `id → price → quantity → 簿状态`：`INVALID_ID`、`INVALID_PRICE`（只有 `Limit` 有价格）、`INVALID_QTY`、`DUPLICATE_ID`（新单的 id 已在簿上）、`UNKNOWN_ID`（撤 / 改一个不在簿上的 id，包括已成交完的）、`OVERFLOW_REASON`。

`OVERFLOW_REASON`：限价单挂簿后会让**自己那一侧同价位**总量溢出 → 整单拒绝，**且不先去吃对手盘**；`Modify` 增量会溢出同理。

**文本格式**（大小写不敏感、空白任意，包括制表符和 `\r`）：

| 命令 | 格式 |
|---|---|
| 限价单 | `LIMIT id BUY\|SELL price qty` |
| 市价单 | `MARKET id BUY\|SELL qty` |
| 撤单 | `CANCEL id` |
| 改量 | `MODIFY id newQty` |

事件渲染：

```
TRADE taker=3 maker=1 side=SELL px=100 qty=3     REST id=1 side=BUY px=7 qty=2     CANCEL id=1 remaining=2
MODIFY id=1 old=5 new=3                           REJECT id=1 reason=duplicate id
```

`replay` 里格式错的行抛 `invalid_argument`，消息以 `line N` 开头（N 从 1 起，跳过的行也算）。

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

手算：4 号买 101 × 6，先吃 101 档队头 1 号（5），再吃 2 号（1）；5 号买 103 × 10，先吃 2 号剩下的 2，再吃 102 的 3 号 4 张，剩 4 张挂在 103；6 号市价卖 5，只有 5 号的 4 张可吃，剩 1 作废；3 号早被吃光，所以 `CANCEL 3` 被拒。

- 更好的价格先成交：卖 102（1 号）先到、卖 101（2 号）后到，买 110 × 5 只和 2 号成交，价格是 101。
- 成交价取 maker 价：1、2 号各买 100 × 3，卖 90 × 4 的成交是 `Trade{3, 1, Sell, 100, 3}` 和 `Trade{3, 2, Sell, 100, 1}`；部分成交的 2 号留在队头，剩 2。
- 没交叉不成交：卖 100 × 4 挂着，买 99 × 4 只是 `Rested`；买 100 × 10 得到 `Trade{.., 100, 4}` 加 `Rested{.., 100, 6}`。
- 市价单：空簿上 `Market{1, Buy, 5}` 得 `Cancelled{1, 5}`；没有买盘时市价卖也是整单作废。
- 拒绝：`lim(0, ..)` → `invalid id`；`price = 0` → `invalid price`；`qty = 0` 或市价单 `qty = -1` → `invalid quantity`；对簿上已有的 id 下限价单或市价单 → `duplicate id`；`Cancel{9}`、`Modify{9, 3}` 对不存在的 id → `unknown id`；`Modify{1, 0}` → `invalid quantity`。被拒绝的命令不改变簿。
- 原子拒绝：买 100 上已有 `LLONG_MAX − 1` 张，同时卖 200 上有 3 张；再下买 100 × 2，得到 `Rejected{.., overflow}`，200 上的卖单必须仍是 3 张（没有先成交）。
- 已成交完的 id 可以复用。
- `parse` 必须拒绝：空串、全空白、`BOGUS 1`、`LIMIT 1 BUY 100`（参数少）、`LIMIT 1 BUY 100 5 7`（参数多）、`LIMIT 1 HOLD 100 5`、`LIMIT x BUY 100 5`、`LIMIT 1 BUY 1.5 5`、`MARKET 1 BUY`、`CANCEL`、`CANCEL 1 2`、`MODIFY 1`、`LIMIT 99999999999999999999 BUY 1 1`。`CANCEL -7` 是合法的（簿负责拒绝这个 id，解析器不管）。
- 不变量：2 万步随机流量里，买卖永不交叉（`best_bid < best_ask`），提交总量 = 2 × 成交量 + 簿上剩余 + 作废量。
- 对拍：每步和一个「线性扫描的暴力模型」逐事件比较（6 个种子，各 5000 步，id 只有 120 个，所以重复 id、未知 id、复用都会大量出现）。
- 性能：30 万条混合命令（约 70% 限价、20% 撤单、10% 改量）用 `execute_all` 跑完，2 秒内。
- C++ 专属测试：
  - 严格解析：`LIMIT 1 BUY +5 1`、`100 5x`、`0x10`、`1e3`、`CANCEL 1_000`、`MODIFY 1 -` 都要拒绝；`LIMIT 007 BUY 0100 5` 合法，等于 `Limit{7, Buy, 100, 5}`；行尾的 `\t\r` 当空白。`std::stoll` 对 `"5x"` 不报错，`strtoll` 接受 `+` 和十六进制，所以用 `std::from_chars` 并检查整个 token 被消费。
  - 非 ASCII 字节：`L\xC3\x89MIT 1 BUY 1 1`、`LIMIT 1 B\xFFY 1 1` 必须抛 `invalid_argument`，不能触发 UB。`char` 可能是有符号的，对负值调 `toupper` / `tolower` 是 UB，要先转成 `unsigned char`。
  - 簿只能移动：`OrderBook` 不能拷贝（`static_assert`），移动构造是 `noexcept`；移动之后，撤单、改量、扫单仍然正常（存着的迭代器跟着节点走）。
  - `Rejected.reason` 是 `string_view`：簿销毁之后，事件里的 reason 仍然可以渲染，因为它指向静态存储。

## Part 3 · 批量限价撮合

| 签名 | 要求 |
|---|---|
| `Summary run_batch(const std::vector<std::vector<long long>>& rows)` | `rows[i] = {side, price, qty}`，`side`：0 买、1 卖；第 i 行的 id 是 `i + 1`；按行序当作限价单依次撮合 |

```cpp
struct Summary {
    std::vector<Trade> trades;        // 全部成交，顺序同事件流
    long long filled_qty;             // 成交总量
    long long notional;               // Σ price × qty
    std::vector<Level> bids, asks;    // 最终盘口，全部档位，最优在前
};
```

- 先**整体校验**再处理：行长度 ≠ 3、`side ∉ {0, 1}`、`price <= 0`、`qty <= 0` 抛 `invalid_argument`，消息以 `row i` 开头（i 从 0 起）。
- `notional` 或 `filled_qty` 溢出抛 `std::overflow_error`。
- 样例：`{{0,100,5},{1,99,3},{1,100,4},{0,101,10}}` → 成交 `{2,1,Sell,100,3}`、`{3,1,Sell,100,2}`、`{4,3,Buy,100,2}`；`filled_qty = 7`，`notional = 700`；`bids = {101, 8, 1}`，`asks` 为空。
- 空输入得到全 0 的 `Summary`；没有交叉就没有成交，两边盘口都在。
- 扫多档：卖 103 × 2、卖 101 × 2、卖 102 × 2，再买 105 × 5，成交按价格 101、102、103 的顺序，最后 103 剩 1。
- 溢出边界：`{{0, 3e9, 3e9}, {1, 3e9, 3e9}}` 的 `notional` 是 `9'000'000'000'000'000'000`，放得下；一笔 `4e9 × 3e9 = 1.2e19` 放不下，抛 `overflow_error`；两笔各 9e18 也放不下。
- 性能：20 万行随机订单，2 秒内；买入总量 = 成交量 + 剩余买盘，卖出同理，簿不交叉。

## Part 4 · 性能追问：`TickBook`

面试官：「你的 `OrderBook` 每秒要处理几百万条命令，每个挂单都有 `list` 节点和 `unordered_map` 节点的分配。怎么办？」

`TickBook(int max_ticks, int capacity)`：价格是整数 tick，合法范围 `1..max_ticks-1`；同时挂簿订单数不超过 `capacity`。

| 签名 | 要求 |
|---|---|
| `TickBook(int max_ticks, int capacity)` | 构造时一次分配完；`max_ticks < 2` 或 `capacity` 不在 `1..2^22` 抛 `std::invalid_argument` |
| `template<class Sink> long long limit(long long id, Side, long long price, long long qty, Sink&& sink)` | 撮合语义同 Part 2 的 `Limit`；每笔成交调用 `sink(taker_id, maker_id, price, qty)`，不创建事件对象；返回挂簿的剩余量（0 = 全部成交） |
| `bool cancel(long long id)` | O(1) |
| `long long best_bid() const noexcept` · `best_ask()` | 没有则返回 `NONE`（−1） |
| `long long qty_at(Side, long long price) const noexcept` | 价位总量；价格带外返回 0 |
| `int live_orders() const noexcept` | 簿上订单数 |

常量：`NONE = -1`、`REJECTED = -1`、`FULL = -2`、`MAX_QTY = 2^40`（保证 2^22 张 × 2^40 = 2^62 装得进 `long long`，价位总量不会溢出）。

- `limit` 返回 `REJECTED`：`id <= 0`、id 已在簿上、价格不在 `1..max_ticks-1`、`qty` 不在 `1..MAX_QTY`。`max_ticks = 1000` 时价格 1000 被拒（上界不含），999 合法；`qty = MAX_QTY` 合法，`MAX_QTY + 1` 被拒。
- 池满返回 `FULL`，此时**不撮合**、簿不变。`capacity = 3` 挂满 3 张后，任何新单（哪怕本可以成交）都是 `FULL`；撤掉一张后，卖 5 × 2 能吃掉剩下的两张买单（先 12 再 10），新单又能用空出来的记录。
- 样例：`TickBook(1000, 16)` 上，买 100 × 5、买 100 × 3、买 98 × 2、卖 105 × 4 后，`best_bid = 100`、`best_ask = 105`、`qty_at(Buy, 100) = 8`、`qty_at(Sell, 5000) = 0`（带外不是越界读）、`live_orders = 4`。
- 撮合与 Part 2 的样例一致：卖 101×5、卖 101×3、卖 102×4，再买 101×6 返回 0，买 103×10 返回 4；成交序列是 `{4,1,101,5}, {4,2,101,1}, {5,2,101,2}, {5,3,102,4}`。
- 撤单后最优价要跨过大量空价位：`TickBook(100000, 16)`，买 10 和买 90000，撤掉 90000 后 `best_bid` 变成 10；卖 95000 和卖 99999 同理。
- id 表经受得住折腾：30 万次随机下单和撤单，id 是 4096 的倍数（对弱哈希不友好），`live_orders` 始终等于参照集合的大小。
- 对拍：5 万步随机流量，每步和 Part 2 的 `OrderBook` 比较成交序列、剩余量、两边最优价、订单数，最后逐档比较 `qty_at`。
- 性能：200 万次随机操作（约 60% 限价、40% 撤单，`max_ticks = 100000`，`capacity = 2^21`）2 秒内。
- C++ 专属测试：
  - 64 位价格要先在 64 位上检查再收窄成 `int`：`price = 2^32 + 5` 必须被拒，不能被截成 5；`qty_at(Buy, 2^32 + 5)` 和 `qty_at(Buy, -1)` 都返回 0。
  - 构造函数校验：`TickBook(1, 10)`、`TickBook(1000, 0)`、`TickBook(1000, 2^22 + 1)`、`TickBook(1000, -5)` 都抛 `invalid_argument`。
  - 任何可调用对象都能当 sink：无捕获 lambda、有捕获 lambda、右值函数对象。
  - 预热之后 100 万次操作的 `operator new` 调用次数必须是 0（测试重载了全局 `operator new` 来计数）；对照实验里，`OrderBook` 挂 1000 张单至少分配 1000 次，`TickBook` 是 0 次。
- 提示：starter 里写了结构：订单记录数组用 `int` 下标串成链并带 free list，每个 tick 每侧一条 `{head, tail, qty}` 记录，一个位图标记非空价位，用 `std::countr_zero` / `std::countl_zero` 找下一个最优价，开放寻址表做 id → 记录并用回移删除。

## 边界清单

- 空盘口；同价 FIFO；部分成交的 maker 留在队头；成交价取 maker 价；`add` 不撮合。
- 增量 modify 丢优先级，减量不丢；已成交 / 已撤的 id 可复用；`modify(未知 id, 0)` 先报参数错。
- `qty = 0` / 负数 / `price = 0`；同价位总量到 `LLONG_MAX` 的边界；溢出时簿不变。
- 市价单遇空盘；撤单后最优价跨很多空档；池满。
- 解析：大小写、`+5`、`0x10`、`1.5`、`1e3`、前导 0、字节 ≥ 0x80。
- 价格 `LLONG_MAX`（`OrderBook` 合法，`TickBook` 越带被拒）；`2^32 + 5` 这种截断后合法的值。

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc05_market_order_book          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc05_market_order_book --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc05_market_order_book --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc05_market_order_book                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 只有 `add / cancel / best`，没有 `modify`；或者按「操作序列」输入、输出每步之后的 best bid / ask。
- 追问：撤单怎么做到 O(1)？同价位怎么保证先来先成交？为什么用 `long long` 不用 `double`？
- `std::map<Price, std::list<Order>>` 加 `unordered_map<Id, list::iterator>` 是面试里的标准答案，和这里的 `OrderBook` 同构。
