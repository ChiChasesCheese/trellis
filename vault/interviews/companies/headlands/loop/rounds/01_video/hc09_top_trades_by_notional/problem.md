# hc09 · 按名义金额取 top-k 成交

一天里交易所产生很多成交事件，每个事件的名义金额（notional）等于价格乘以数量。面试官要你取名义金额最大的 k 个事件，然后换一个口径：按 ticker 汇总后取最大的 k 个。两问用的是同一个工具，大小为 k 的最小堆（min-heap）；分数在细节上：并列怎么排、乘法会不会溢出。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "You get parallel arrays `tickers`, `prices`, `volumes` describing trade events. Return the top k events by notional, where notional is price times volume."
> 接着会问："Now return the top k tickers by total notional." "What if price × volume overflows?" "What if the trades arrive as a stream?" "How would you parallelize it?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：并列怎么排？返回下标还是事件？k 比事件数大怎么办？价格和数量是整数吗？ |
| 3–15 分钟 | **Part 1**：top-k 事件，大小为 k 的最小堆 |
| 15–30 分钟 | **Part 2**：按 ticker 汇总，再取 top-k |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · top-k 事件（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<Integer> topEvents(String[] tickers, long[] prices, long[] volumes, int k)` |
| C++ | `std::vector<int> top_events(const std::vector<std::string>& tickers, const std::vector<long long>& prices, const std::vector<long long>& volumes, int k)` |

- 第 `i` 个事件是 `(tickers[i], prices[i], volumes[i])`，`notional = prices[i] * volumes[i]`，价格和数量是非负整数。
- 返回 notional 最大的 `k` 个事件的**下标**，最大的在前。并列规则：notional 相同，下标小的在前。有了这条规则，结果唯一。
- `k` 比事件数大：返回全部事件；`k == 0` 或没有事件：返回空列表。
- `k < 0` 或三个数组长度不等：Java 抛 `IllegalArgumentException`，C++ 抛 `std::invalid_argument`。
- 乘法溢出：Java 抛 `ArithmeticException`，C++ 抛 `std::overflow_error`。每个事件都要算，包括进不了 top-k 的。
- 例子：三个数组如下，notional 依次为 180000、120000、90500、126000、120000、200000。

| i | ticker | price | volume | notional |
|---|---|---|---|---|
| 0 | AAPL | 18000 | 10 | 180000 |
| 1 | MSFT | 40000 | 3 | 120000 |
| 2 | AAPL | 18100 | 5 | 90500 |
| 3 | GOOG | 14000 | 9 | 126000 |
| 4 | MSFT | 40000 | 3 | 120000 |
| 5 | TSLA | 25000 | 8 | 200000 |

  `k = 3` 返回 `[5, 0, 3]`；`k = 4` 返回 `[5, 0, 3, 1]`：第 4 名是下标 1 而不是 4，因为二者 notional 相同，下标小的在前。

## Part 2 · top-k ticker（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<String> topTickers(String[] tickers, long[] prices, long[] volumes, int k)` |
| C++ | `std::vector<std::string> top_tickers(const std::vector<std::string>& tickers, const std::vector<long long>& prices, const std::vector<long long>& volumes, int k)` |

- 同一个 ticker 的所有事件的 notional 相加，返回总额最大的 `k` 个 ticker，总额大的在前；总额相同，ticker 字典序小的在前。
- 先用哈希表（HashMap）汇总，再用 Part 1 同样的堆在汇总结果里选。
- 单个事件不溢出，加起来也可能溢出：累加也要检查，溢出时抛 Part 1 里同样的异常。
- `k`、长度、空输入的规则同 Part 1。
- 例子：同一组数据，总额为 AAPL 270500、MSFT 240000、TSLA 200000、GOOG 126000。`k = 2` 返回 `["AAPL", "MSFT"]`。最大的单个事件是 TSLA，最大的 ticker 是 AAPL，两个问题的答案不同。
- 例子：总额都是 50 的两个 ticker `ZZ` 和 `AA`，`k = 1` 返回 `["AA"]`。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么取最大的 k 个要用最小堆，而不是最大堆？
2. 排序、堆、quickselect 三种做法的复杂度怎么比？什么时候选哪个？
3. `price × volume` 溢出怎么处理？价格是 `double` 时呢？
4. 事件是实时流，随时要报出 top-k，怎么做？只关心最近一段时间呢？
5. 数据有两千万条，怎么用多核？
6. 并列规则不写清楚会出什么问题？

## 边界

- `k = 0`、`k` 大于事件数、空输入、`k < 0`
- notional 并列（下标决定）、总额并列（ticker 决定）
- 乘法溢出：`3037000499²` 放得下，`3037000500²` 放不下
- 单个事件放得下、同一 ticker 累加后放不下：两个 `Long.MAX_VALUE / 2 + 1`

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc09_top_trades_by_notional       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc09_top_trades_by_notional --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc09_top_trades_by_notional       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc09_top_trades_by_notional --tag part1
```
