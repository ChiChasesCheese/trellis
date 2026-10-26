# hc14 · 成交日志 VWAP

交易系统写出一份成交日志，一行一笔：时间戳、代码、价格、数量。面试官先让你按代码算成交量加权平均价（VWAP，volume-weighted average price），坏行要跳过并计数；然后把同样的计算改成流式，只看最近 W 毫秒。代码都不长，分数在边界上：除法怎么取整、窗口的边界算过期还是算活着、用运行和还是每次重算。价格用整数最小价位（tick）存，不用浮点数。

## 面试官会怎么说

> "Each line of the trade log is `ts_ms,symbol,price,qty`. Compute the VWAP per symbol. Skip malformed lines and count them."
> 接着会问："Now trades arrive as a stream — give me the VWAP of a symbol over the last W milliseconds." "How would you get the top k symbols by notional?" "What about a million lines?" "Can price × qty overflow?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–4 分钟 | 复述题目，问清：价格是整数 tick 还是小数？除法怎么取整？坏行包括哪些？ |
| 4–17 分钟 | **Part 1**：解析、跳过坏行、按代码算 VWAP |
| 17–32 分钟 | **Part 2**：滑动窗口 VWAP，每个代码一个队列加两个运行和 |
| 32–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 解析与按代码 VWAP（约 13 分钟）

| 语言 | 签名 |
|---|---|
| Java | `class TradeLog` · `void add(String line)` · `int malformed()` · `Map<String, Long> vwap()` |
| C++ | `class TradeLog` · `void add(const std::string&)` · `int malformed() const` · `std::map<std::string, long long> vwap() const` |

- 一行是 `ts_ms,symbol,price,qty`，恰好 4 个字段；`ts_ms`、`price`、`qty` 都是整数（`long`）。价格已经是 tick 数，不含小数点。
- 坏行：字段数不对、`symbol` 为空、任何一个数字解析失败、`price <= 0` 或 `qty <= 0`、空行。坏行不影响结果，只让 `malformed()` 加一。
- `vwap()` = Σ(price × qty) / Σqty，用 `long` 做整数除法，**向下取整**（rounding down）。结果里只有至少有一笔合法成交的代码。
- 例子：`1000,AAPL,100,10` 和 `1001,AAPL,110,30` → (1000 + 3300) / 40 = 4300 / 40 = 107.5 → `107`。
- 例子：`1,AAPL,1.5,10`（价格不是整数）、`1,,100,10`（symbol 为空）、`1,AAPL,0,10` 都是坏行。

## Part 2 · 滑动窗口 VWAP（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `RollingVwap(long windowMs)` · `void onTrade(long ts, String symbol, long price, long qty)` · `OptionalLong vwap(String symbol, long nowMs)` |
| C++ | `RollingVwap(long long windowMs)` · `void on_trade(long long ts, const std::string&, long long price, long long qty)` · `std::optional<long long> vwap(const std::string&, long long now_ms)` |

- 成交的时间戳不降序到达。一笔成交在时刻 `now` 还活着，当且仅当 `now - ts < windowMs`；`now - ts == windowMs` 时刚好过期。
- `vwap(symbol, nowMs)` 返回该代码在窗口里的 VWAP（同样向下取整）；窗口里没有它的成交（或从没出现过）返回空。
- 每个代码一个队列，里面存窗口内的成交，旁边是两个运行和（running sum）：名义金额 Σ(price × qty) 和数量 Σqty。查询时先从队头弹掉过期的成交并从两个和里减掉，再做除法。每笔成交最多入队一次、出队一次，所以均摊 O(1)（amortised）。
- `windowMs < 1` 抛 `IllegalArgumentException`（C++：`std::invalid_argument`）。
- 例子（`W = 1000`）：`(0, AAPL, 100, 10)`、`(400, AAPL, 120, 20)` → `vwap(AAPL, 999) = 113`（3400 / 30）；`vwap(AAPL, 1000) = 120`，因为 `ts = 0` 那笔此刻刚好过期。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 价格里的小数怎么处理？为什么不用 `double`？
2. 除法怎么做四舍五入而不是向下取整？
3. `price × qty` 和累加会溢出吗？怎么检测？
4. 窗口内名义金额最大的前 k 个代码怎么取？
5. 一百万行日志怎么读得又快又省？
6. 为什么不是每次查询都重扫窗口？

## 边界

- 空日志、全是坏行
- 末尾为空字段的行（`1,AAPL,100,`）
- 同一时间戳的多笔成交
- `now - ts == windowMs`：刚好过期
- 查询一个从没出现过的代码

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc14_vwap_trade_log       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc14_vwap_trade_log --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc14_vwap_trade_log       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc14_vwap_trade_log --tag part1
```
