---
id: hl-hc09-what-asked
node: problems.hc09-top-trades-by-notional
type: qa
step: 1
---
## Q
按名义金额取 top-k 成交（Top Trade Events by Notional）题的输入、规则和四个 Part 是什么？

## A
成交事件以三个**平行数组**给出：第 i 个事件是 `(tickers[i], prices[i], volumes[i])`，**notional（名义金额）= price × volume**。价格用整数 tick（如 1 tick = 1 美分），数量用整数股数，价格、数量 ≥ 0；乘法和累加都用 `Math.xxxExact`，溢出抛 `ArithmeticException`，绝不静默回绕。

四个 Part：
1. **top-k 事件** `topEvents(tickers, prices, volumes, k)`：大小为 k 的最小堆 + 完整 tie-break + 溢出检查；`topEventsSorted` 是排序基线；
2. **top-k ticker** `topTickers`：同一 ticker 的 notional 相加，取总额最大的 k 个；`topOf`、`topTickersStream`、`summarize`（`teeing`）；
3. **流式滑动窗口** `SlidingTopK`：成交按时间顺序到达，只看窗口内，旧成交过期；
4. **并行分块聚合** `ParallelNotional`：数组切块并行，最后合并，结果与顺序版完全相同。

样例（6 个事件）：`AAPL 18000×10=180000`、`MSFT 40000×3=120000`、`AAPL 18100×5=90500`、`GOOG 14000×9=126000`、`MSFT 40000×3=120000`、`TSLA 25000×8=200000`。`k=3` → 下标 5, 0, 3；`k=4` 第 4 名是下标 1 不是 4（notional 与 ticker 都相同，下标小的在前）；按 ticker：AAPL 270500、MSFT 240000、TSLA 200000、GOOG 126000，`k=2` → AAPL、MSFT。**最大的事件（TSLA）不属于最大的 ticker（AAPL）**，别混。

输入校验：`k > n` 返回全部；`k == 0` 或空输入 → 空列表；`k < 0` → `IllegalArgumentException`；数组长度不等 → IAE；null 数组 / null ticker → NPE；负价格 / 数量 → IAE；输入数组不得修改，返回列表不可变。
