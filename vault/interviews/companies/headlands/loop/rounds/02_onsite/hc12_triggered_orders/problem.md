# hc12 · 触发的订单

订单按到达顺序一张张进来，每张是 `[价格, 方向]`，方向是 `BUY`（买）或 `SELL`（卖）。一张订单如果能和先前的某张反方向订单成交，就说它被**触发**（triggered）：买单的价格大于等于先前最低的卖价时触发，卖单的价格小于等于先前最高的买价时触发。你要返回所有被触发订单的下标，按到达顺序。Part 1 先写最简单的版本，Part 2 加上「触发的订单会把对手方最优的挂单吃掉」，这时需要堆（heap）。Java 和 C++ 的签名都在下面。

## 面试官会怎么说

> "You receive orders in arrival order. Each row is `[price, side]`, where side is BUY or SELL. Return the indices of the orders that get triggered."
> 接着会问："What if a trigger consumes the resting order it matched?" "What about quantities?" "Ties at the same price?" "Many symbols?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–4 分钟 | 复述题目，问清：相等的价格算不算触发？订单触发后还留在簿子里吗？方向写错了怎么办？ |
| 4–16 分钟 | **Part 1**：只记最低卖价和最高买价，一遍扫描 |
| 16–32 分钟 | **Part 2**：两个堆，触发时弹出对手方最优的一张 |
| 32–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 早先的订单从不被消耗（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<Integer> triggeredSimple(int[] prices, String[] sides)` |
| C++ | `std::vector<int> triggered_simple(const std::vector<int>& prices, const std::vector<std::string>& sides)` |

- 买单触发：`price >= 先前出现过的最低卖价`。卖单触发：`price <= 先前出现过的最高买价`。相等算触发。
- 所有先前的订单都算数，不管它自己有没有被触发；订单只和**先前**的订单比较，第一张订单永远不会触发。
- 方向不是 `BUY` 或 `SELL`：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 空输入返回空列表。
- 例子：价格 `[10, 9, 11, 8, 12]`、方向 `[B, S, B, B, S]` 返回 `[1, 2]`：9 卖 ≤ 最高买价 10；11 买 ≥ 最低卖价 9；8 买 < 9；12 卖 > 11。
- 例子：`[5, 4]` 方向 `[S, B]` 返回 `[]`，`[5, 5]` 方向 `[B, S]` 返回 `[1]`。

## Part 2 · 触发就吃掉最优挂单（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<Integer> triggeredConsuming(int[] prices, String[] sides)` |
| C++ | `std::vector<int> triggered_consuming(const std::vector<int>& prices, const std::vector<std::string>& sides)` |

- 簿子里只放**没有触发**的订单（挂单，resting order）。买单触发时，吃掉价格最低的挂单卖；卖单触发时，吃掉价格最高的挂单买。触发的订单和被吃掉的那张都消失。
- 没触发的订单挂进簿子里等后来的订单。
- 例子：同样的 `[10, 9, 11, 8, 12]`，这次只返回 `[1]`：9 卖吃掉 10 买之后，11 买面前没有卖单，11 买、8 买、12 卖都留在簿子里，没人再来触发。
- 例子：价格 `[10, 12, 11, 11]`、方向 `[B, B, S, S]` 返回 `[2]`：11 卖吃掉的是最高买价 12，剩下的 10 买低于 11，所以第二张 11 卖不触发。
- 例子：价格 `[10, 11, 10, 10, 10]`、方向 `[B, B, S, S, S]` 返回 `[2, 3]`：两张买单只够吃两张卖单。Part 1 的答案是 `[2, 3, 4]`。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. Part 2 为什么要堆，Part 1 为什么不用？各自的复杂度是多少？
2. 订单带数量，一张订单只吃掉一部分怎么办？
3. 同一个价格上有好几张挂单，先吃哪张？
4. 很多个标的（symbol）同时进来怎么办？
5. 真正的止损单（stop order）是按最新成交价触发的，怎么实现？

## 边界

- 空输入，只有一个方向的输入
- 价格相等（买价 = 卖价）
- 先卖后买、先买后卖两种顺序
- 方向字符串不是 `BUY` / `SELL`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/02_onsite/hc12_triggered_orders       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/02_onsite/hc12_triggered_orders --tag part1
python3 tools/cpptest.py start loop/rounds/02_onsite/hc12_triggered_orders       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/02_onsite/hc12_triggered_orders --tag part1
```
