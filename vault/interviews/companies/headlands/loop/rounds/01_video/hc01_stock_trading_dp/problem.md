# hc01 · 买卖股票（动态规划）

给你一只股票连续 n 天的价格，每天最多做一个动作（买、卖、休息），手里最多一股，卖了才能再买，问最多能赚多少。面试官从「只能买卖一次」开始，逐步放宽到「次数不限」，再到「最多 k 笔」。前两问各几行代码；k 笔需要把每天的持仓状态记成表，是重点。冷却期和手续费放在口头追问里。

## 面试官会怎么说

> "Given an array of prices, find the maximum profit from one buy and one sell."
> 接着会问："What if you can trade as many times as you like?" "Now at most k transactions." "What if there is a cooldown after selling, or a fee per trade?" "Can you return the actual trades?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：同一天能不能又卖又买？价格会不会为负？不赚钱时返回 0 吗？ |
| 3–15 分钟 | **Part 1**：一次交易、次数不限 |
| 15–30 分钟 | **Part 2**：最多 k 笔，状态 DP |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 一次交易和次数不限（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static long maxProfitOnce(long[] prices)` · `static long maxProfitUnlimited(long[] prices)` |
| C++ | `long long max_profit_once(const std::vector<long long>&)` · `long long max_profit_unlimited(const std::vector<long long>&)` |

- `maxProfitOnce`（LeetCode 121）：只能买一次、卖一次，卖在买之后。一笔都不做就是 0。
- `maxProfitUnlimited`（LeetCode 122）：次数不限，但还是先卖后买。
- 两个都要 O(n) 时间、O(1) 空间；空数组和一天的数组返回 0。
- 例子：`[7,1,5,3,6,4]` 一次得 5（1 买、6 卖），不限次数得 7（1→5 赚 4，3→6 赚 3）；`[7,6,4,3,1]` 都是 0；`[2,10,0,1]` 一次得 8。

## Part 2 · 最多 k 笔（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static long maxProfitAtMost(int k, long[] prices)` |
| C++ | `long long max_profit_at_most(int k, const std::vector<long long>&)` |

- 最多 k 笔交易（LeetCode 188），按买入次数数。`k <= 0` 返回 0。
- `k` 可以是 `Integer.MAX_VALUE`：n 天最多完成 n/2 笔，不能按 `k` 开数组。
- 例子：`k=2, [2,4,1]` 得 2；`k=2, [3,2,6,5,0,3]` 得 7；`k=2, [3,3,5,0,0,3,1,4]` 得 6（LeetCode 123）。
- `k=1` 的答案等于 Part 1 的一次交易；`[1,5,2,6,3,9]` 在 `k=1,2,3` 时依次是 8、11、14。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 卖出后要冷却一天才能再买（LeetCode 309），怎么改？
2. 每笔卖出要付手续费（LeetCode 714），怎么改？
3. 这几个变体是不是同一个东西？
4. 除了利润，还要报出具体哪天买、哪天卖，怎么做？
5. n 非常大（装不进内存）时怎么办？

## 边界

- 空数组、一天、价格一路下跌
- 最低价出现在最高价之后（不能拿最低价配最高价）
- `k = 0`、`k = 1`、`k` 比 n/2 大得多

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc01_stock_trading_dp       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc01_stock_trading_dp --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc01_stock_trading_dp       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc01_stock_trading_dp --tag part1
```
