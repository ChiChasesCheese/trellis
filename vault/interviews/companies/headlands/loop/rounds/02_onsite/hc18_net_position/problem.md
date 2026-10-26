# hc18 · 净持仓

交易系统要知道每个标的（symbol）现在持有多少股：多头为正，空头为负。信息来自两种事件：券商接口给的**快照**（snapshot，某个序号时刻的完整持仓）和我们自己的**成交**（fill，买入加、卖出减）。Part 1 按到达顺序直接处理，快照覆盖、成交加减；Part 2 事件可能乱序，要用序号（sequence number，seq）判断哪些成交已经被快照包含、哪些快照已经过期。Java 和 C++ 的签名都在下面。

## 面试官会怎么说

> "Calculate the final signed share quantity for each symbol from API snapshots."
> 接着会问："What if events arrive out of order?" "Why sequence numbers and not timestamps?" "How do you reconcile against your own fills?" "What about overflow, and many symbols?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–4 分钟 | 复述题目，问清：成交的数量是正数、方向另给吗？结果里数量为 0 的标的留不留？序号在标的内比较还是全局比较？ |
| 4–16 分钟 | **Part 1**：按顺序处理，快照覆盖，成交加减 |
| 16–32 分钟 | **Part 2**：用 seq 处理乱序、重复和过期快照 |
| 32–40 分钟 | **Part 3**：口头追问，不写代码 |

## 事件

| 事件 | 含义 | Java | C++ |
|---|---|---|---|
| SNAPSHOT(seq, symbol, qty) | 序号 seq 时刻，券商给出该标的的完整持仓 | `Event.snapshot(seq, symbol, qty)` | `Event::snapshot(seq, symbol, qty)` |
| FILL(seq, symbol, side, qty) | 序号为 seq 的成交，`BUY` 加 qty，`SELL` 减 qty | `Event.fill(seq, symbol, side, qty)` | `Event::fill(seq, symbol, side, qty)` |

序号从 1 开始，在同一个标的内比较；`qty` 是非负的 `long`。`side` 不是 `BUY` 或 `SELL`：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。结果是按标的排序的映射，**数量为 0 的标的保留**。

## Part 1 · 按到达顺序处理（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static Map<String, Long> positionsInOrder(List<Event> events)` |
| C++ | `std::map<std::string, long long> positions_in_order(const std::vector<Event>& events)` |

- 不看 seq。快照把该标的的持仓设成 qty；成交在当前持仓上加减。没出现过的标的，持仓从 0 开始。
- 例子：`SNAPSHOT(1, AAPL, 100)`、`FILL(2, AAPL, BUY, 20)`、`FILL(3, AAPL, SELL, 5)`、`FILL(4, MSFT, BUY, 7)` 得到 `AAPL=115, MSFT=7`。
- 例子：`FILL(1, A, BUY, 10)`、`SNAPSHOT(2, A, 50)`、`FILL(3, A, SELL, 20)` 得到 `A=30`：快照把前面的成交整个覆盖了。
- 例子：只有 `FILL(1, X, SELL, 30)` 得到 `X=-30`；先买 5 再卖 5 得到 `X=0`，保留。

## Part 2 · 乱序到达（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static Map<String, Long> positions(List<Event> events)` |
| C++ | `std::map<std::string, long long> positions(const std::vector<Event>& events)` |

规则（对每个标的分别用）：

- 快照 seq 的含义是：序号 ≤ seq 的所有成交都已经算在它的 qty 里。
- 到达的成交 seq ≤ 已有快照的 seq：已经包含在快照里，忽略。
- 到达的快照 seq ≤ 已经采用的快照的 seq：过期（或重复），忽略。
- 序号大于快照 seq 的成交要加上，同一个 seq 只算一次（去重）。成交可以比它的快照**先到**：先记着，快照到了再看它是不是在快照之后。
- 最终持仓 = 最新快照的 qty + 序号大于该快照的成交之和。没有快照的标的，快照 seq 当作 0、qty 当作 0。
- 例子：`SNAPSHOT(10, A, 100)` 后到 `FILL(9, A, BUY, 5)` 或 `FILL(10, A, BUY, 5)`：结果 100；到 `FILL(11, A, BUY, 5)`：结果 105。
- 例子：`FILL(12, A, BUY, 5)` 先到，`SNAPSHOT(10, A, 100)` 后到：结果 105。`FILL(8, A, BUY, 5)` 先到：结果 100。
- 例子：`SNAPSHOT(10, A, 100)`、`FILL(11, A, BUY, 5)`、`FILL(12, A, BUY, 3)`、`SNAPSHOT(11, A, 104)`：结果 107，快照 11 吸收了 seq 11，seq 12 仍要加。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么用序号而不是时间戳？
2. 怎么和我们自己记录的成交对账，不一致时怎么办？
3. 持仓数量用 `long` 会溢出吗？
4. 很多标的同时进来怎么并行？
5. 要保存的状态会不会越积越多？

## 边界

- 没有快照的标的；只有快照没有成交的标的
- seq 等于快照 seq 的成交和快照
- 成交先于快照到达
- 持仓为负、为 0
- `side` 不是 `BUY` / `SELL`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/02_onsite/hc18_net_position       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/02_onsite/hc18_net_position --tag part1
python3 tools/cpptest.py start loop/rounds/02_onsite/hc18_net_position       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/02_onsite/hc18_net_position --tag part1
```
