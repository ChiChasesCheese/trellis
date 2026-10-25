# hc01 · 买卖股票家族（动态规划 / 状态机）（C++20 版）

给你一只股票连续 n 天的收盘价，问最多能赚多少。它从只允许一次交易开始，面试官逐步放宽到不限次数、最多 k 笔，再加冷却期、手续费，最后要求还原具体的买卖日，并写一个检查器回放方案。这些变体共用同一台状态机：把每天结束时的持仓情况画成几个状态，用动态规划（dynamic programming，DP）记下每个状态下的最优现金。C++ 版的额外考点集中在整数边界上：无符号的 `size() - 1`、`k + 1`、哨兵值上的加减、格子数的乘法，每一处都可能是未定义行为（undefined behavior，UB）。签名都在 `starter.hpp`（命名空间 `stock`）。

## 读题前你需要知道

- **规则**：价格是非负整数（单位 tick）。每次只能持有**一股**；买之前必须先卖掉手里的；同一天只能做一个动作（买、卖、休息三选一）。
- **一笔交易**（transaction）= 一次买入 + 之后的一次卖出。「最多 k 笔」按**买入次数**数。
- **状态机**（finite state machine）：`FREE` 没有持股、可以买；`HOLD` 持有一股；`COOL` 今天刚卖出、明天只能休息。每个动作是一条箭头，DP 的转移就是把箭头逐条翻译成 `max`。
- **滚动数组**（rolling array）：今天的值只依赖昨天，所以只留一层；更新顺序决定读到的是昨天还是今天的值。
- **回溯**（backtracking）：正向 DP 时记下每格的决定，倒着走一遍才能还原出具体的买卖日。
- **输入上界**：天数不超过 `MAX_DAYS`（2^22），价格在 `[0, MAX_PRICE]`（2^40）。利润最多 2^21 · 2^40 = 2^61，`long long` 里不会溢出，内层循环不需要检查溢出。

## 公共类型（starter 已给出）

```cpp
inline constexpr long long MAX_PRICE = 1LL << 40;
inline constexpr int MAX_DAYS = 1 << 22;
inline constexpr long long MAX_PLAN_CELLS = 1LL << 28;

using Prices = std::span<const long long>;   // vector、std::array、C 数组都能转换；span 不会是 null

struct Trade { int buy_day; int sell_day; };  // 构造时要求 0 <= buy_day < sell_day，否则抛 std::invalid_argument
struct Plan  { long long profit; std::vector<Trade> trades; };

struct Rules {                                // max_transactions：最多买几次；fee：每笔卖出扣；cooldown：卖出后的下一天不能买
    static constexpr int UNLIMITED = INT_MAX;
    int max_transactions; long long fee; bool cooldown;
    Rules(int k, long long fee, bool cooldown);        // k < 0 或 fee 不在 [0, MAX_PRICE] 抛 std::invalid_argument
    static Rules at_most(int k);
    static Rules unlimited();
    Rules with_fee(long long) const;
    Rules with_cooldown(bool) const;
};

struct IllegalState : std::logic_error { ... };         // 非法的状态转移；不是 invalid_argument
enum class State { FREE, HOLD, COOL };
struct Buy  { int day; };
struct Sell { int day; };
using Move = std::variant<Buy, Sell>;
```

`Trade`、`Plan`、`Rules`、`IllegalState`、`State`、`Move` 已经写好，你要写的是下面各 Part 的函数和 `State` 的三个转移函数。

## Part 1 · 一次交易

| 签名 | 要求 |
|---|---|
| `long long max_profit_brute(Prices)` | 试遍所有 (买入日 i, 卖出日 j > i)，取 `p[j] - p[i]` 的最大值，至少是 0。O(n²)，给后面的解法当标准答案 |
| `long long max_profit_once(Prices)` | O(n) 时间、O(1) 空间：一次扫描，记住此前的最低价 |

- **输入校验（所有 Part 共用）**：天数超过 `MAX_DAYS` 或任何价格不在 `[0, MAX_PRICE]`，抛 `std::invalid_argument`。坏价格在数组末尾也要被发现。
- `[7,1,5,3,6,4]` 得 5；`[7,6,4,3,1]` 得 0。
- 空数组、1 天、`[3,3,3]` 都得 0；`[1,2]` 得 1；`[2,1]` 得 0。
- 最低点在最高点之后：`[10,9,8,1]` 得 0，`[5,1,5,0,4]` 得 4。不能算成全局最大减全局最小。
- 极端价格：`[0, MAX_PRICE]` 得 `MAX_PRICE`，`[MAX_PRICE, 0]` 得 0。
- 随机小输入上，暴力和线性版结果相同。100 万天的线性版要在 2 秒内。
- C++ 专属测试：空输入不能读越界。`for (i = 0; i < p.size() - 1; ++i)` 在空 span 上，`size() - 1` 是 `SIZE_MAX`，循环会一路读下去。

## Part 2 · 次数不限

| 签名 | 要求 |
|---|---|
| `long long max_profit_unlimited(Prices)` | 可以买卖任意多次，仍然是先卖后买、同一天一个动作。O(n) |

- `[7,1,5,3,6,4]` 得 7（1→5 赚 4，3→6 赚 3）；`[1,2,3,4,5]` 得 4；`[7,6,4,3,1]` 得 0。
- 空数组、1 天、`[4,4,4,4]` 都得 0。
- `0, MAX_PRICE, 0, MAX_PRICE, …` 共 2000 天：1000 笔，每笔 2^40，结果是 `1000 * MAX_PRICE`。
- 随机小输入与枚举所有（买 < 卖 < 买 < 卖……）序列的朴素解一致。100 万天要在 2 秒内。

## Part 3 · 最多 k 笔（状态机 DP + 滚动数组）

| 签名 | 要求 |
|---|---|
| `long long max_profit_at_most(int k, Prices)` | 最多买入 k 次。`k < 0` 抛 `std::invalid_argument`；`k == 0` 或 n < 2 得 0 |

- **k 可以是 `INT_MAX`**：n 天最多完成 n/2 笔，`k >= n/2` 时必须退化成 Part 2，绝不能按 k 分配空间。starter 注释已提示这一点。
- 时间 O(n · min(k, n/2))，空间 O(min(k, n/2))。
- `k=2, [2,4,1]` 得 2；`k=2, [3,2,6,5,0,3]` 得 7；`k=2, [3,3,5,0,0,3,1,4]` 得 6；`k=1` 同一组价格得 4。
- `k=1` 的结果等于 `max_profit_once`。
- `[7,1,5,3,6,4]`：`k = INT_MAX`、`k = 1'000'000'000`、`k = 3`（恰好 n/2）都得 7。
- 随机小输入上与朴素枚举一致，并且 k 增大时利润不会下降。
- 性能：20 万天、k = 50，以及 100 万天、k = 2，都要在 2 秒内。
- C++ 专属测试：`INT_MAX` 那一条，`k + 1` 是有符号溢出，而且会尝试分配几十 GB。

## Part 4 · 冷却 / 手续费 / 还原交易 / 回放

| 签名 | 要求 |
|---|---|
| `State after_rest(State)` | `COOL` 变 `FREE`，其余不变 |
| `State after_buy(State)` | 只有 `FREE` 能买，得 `HOLD`；否则抛 `IllegalState` |
| `State after_sell(State, const Rules&)` | 只有 `HOLD` 能卖，有冷却得 `COOL`，没有得 `FREE`；否则抛 `IllegalState` |
| `long long max_profit(const Rules&, Prices)` | 只要利润数字 |
| `std::optional<Plan> try_plan(const Rules&, Prices)` | 利润 + 具体交易。格子数 `(n+1) × (min(k, n/2)+1)` 超过 `MAX_PLAN_CELLS` 返回 `std::nullopt`；输入非法仍然抛异常 |
| `Plan plan(const Rules&, Prices)` | 同 `try_plan`，但表太大时抛 `std::invalid_argument` |
| `long long replay(const Rules&, Prices, const std::vector<Trade>&)` | 用 `State` 状态机逐天回放一个方案，返回利润（每笔卖出扣 `fee`） |

`plan` 返回的 `trades` 按时间排序，每笔净利润（卖价 − 买价 − fee）大于 0，零利润的交易不出现。最优方案可能不唯一，测试只检查「合法 + 利润等于最优」，以及少数方案唯一的样例。

`replay` 遇到非法方案抛 `std::invalid_argument`：笔数超过 `max_transactions`、日期 >= n、同一天两个动作（包括同一天卖出又买入）、重叠、冷却期内买入、卖出时没有持股。

利润样例：

| rules | prices | 利润 |
|---|---|---|
| 不限，冷却 | `[1,2,3,0,2]` | 3 |
| 不限，fee = 2 | `[1,3,2,8,4,9]` | 8 |
| 不限，fee = 3 | `[1,3,7,5,10,3]` | 6 |
| 不限，冷却 | `[1]` | 0 |
| 不限，冷却 | `[1,2,1,2]` | 1（不能第 1 天卖、第 2 天买） |
| 不限，无冷却 | `[1,2,1,2]` | 2 |
| 不限，fee = 4 | `[1,5]` | 0（净利润 0 不交易） |
| 不限，fee = 3 | `[1,5]` | 1 |
| 不限，fee = 100 | `[1,5,2,9]` | 0 |
| 至多 0 笔 | `[1,9]` | 0 |

`plan` 样例：

- 不限，`[7,1,5,3,6,4]`：利润 7，`trades == {Trade(1,2), Trade(3,4)}`。
- 不限 + 冷却，`[1,2,3,0,2]`：利润 3，`{Trade(0,1), Trade(3,4)}`。
- 至多 1 笔，`[7,1,5,3,6,4]`：利润 5，`{Trade(1,4)}`。
- 空数组、1 天、全递减、`at_most(0)`、fee 大于所有价差：`Plan{0, {}}`。

`replay` 样例（价格 `[1,2,3,0,2]`，方案 `{Trade(0,1), Trade(3,4)}`）：

- 不限 + 冷却：3。
- 不限 + fee = 1：3 − 2 = 1。
- 空方案：0。

非法方案（价格 `[1,2,3,0,2,5]`）：`{Trade(0,3), Trade(1,4)}` 重叠；`{Trade(0,1), Trade(2,5)}` 在冷却下抛异常、无冷却下合法得 3；`at_most(1)` 下两笔抛异常；`{Trade(0,2), Trade(2,4)}` 同一天卖又买；`{Trade(4,6)}` 日期越界。

约束与性能：

- 随机小输入、所有规则组合下，`max_profit` 和 `plan(...).profit` 都等于朴素枚举的结果。
- `Rules::at_most(1)`、`unlimited()`、`at_most(4)` 的结果分别等于 Part 1、2、3 的函数。
- `plan` 的结果对随机输入都是合法方案，并且 `replay(rules, p, pl.trades) == pl.profit`。
- 100 万天、不限次数 + 冷却 + fee 500：2 秒内。10 万天的 `plan`（冷却 + fee 300；至多 20 笔 + fee 100）：2 秒内。2000 天、至多 500 笔 + 冷却的 `plan`：2 秒内。
- `plan(Rules::at_most(50'000 - 1), V(100'000, 0))` 抛 `std::invalid_argument`。
- C++ 专属测试：
  - 不可达状态用很小的负数做哨兵，对它加价格、减 fee 不能溢出。测试用 `fee == MAX_PRICE` 和极端价格，在有无冷却、`k` 为 1、3、`UNLIMITED` 的组合下检查。
  - 格子数 `(n+1) × (k+1)` 要用 64 位算：n = 100 000、k = 49 999 约 5·10⁹，`int` 装不下。`try_plan(at_most(49'999), 10 万天)` 得 `nullopt`；`at_most(100)` 约 1·10⁷ 格，有结果；`unlimited()` 有结果。
  - `try_plan(at_most(60'000), 13 万个 5)` 得 `nullopt`，`plan` 同一输入抛 `std::invalid_argument`；`try_plan(unlimited(), [1,-2])` 仍然抛 `std::invalid_argument`。
  - `static_cast<State>(7)`：`after_buy` 和 `after_sell` 抛 `IllegalState`，`after_rest` 原样返回。
  - `IllegalState` 不能被 `catch (const std::invalid_argument&)` 接住。
  - `replay(unlimited().with_fee(MAX_PRICE), [0,0], {Trade(0,1)})` 得 `-MAX_PRICE`：回放不要求方案有利可图。

## 其他 C++ 专属测试

- 所有函数都不修改输入。
- `std::array`、C 数组、`std::vector`、`Prices(vec).subspan(1, 4)`（视图 `[1,5,3,6]` 得 7）、`Prices(raw).first(0)`（得 0）都能传进来。
- `MAX_DAYS` 天的全 0 输入合法；`MAX_DAYS + 1` 天抛 `std::invalid_argument`。
- `Trade(-1,2)`、`Trade(2,2)`、`Trade(3,2)` 抛 `std::invalid_argument`；`Trade(0,1)` 合法。`Rules(-1,0,false)` 也抛。

## 边界清单

- 空数组、1 天、全递减、全相等、价格 0 与 `MAX_PRICE`
- 最低点在最高点之后
- `k = 0`、`k = INT_MAX`、`k = n/2`
- fee 大于所有价差、fee 等于价差
- 冷却下 `[1,2,1,2]`
- `plan` 里买入日 < 卖出日、交易不重叠、冷却间隔
- 表太大返回 `nullopt` 而不是抛异常
- `replay` 的各种非法方案
- `enum class` 里的非法值

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc01_stock_trading_dp          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc01_stock_trading_dp --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc01_stock_trading_dp --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc01_stock_trading_dp                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 正好 k=2（LeetCode 123）、任意 k（188）、冷却（309）、手续费（714），以及把它们拼在一起的 `Rules`。
- 「只给利润不够，把买卖日也给出来」：回溯。
- 「价格是流式输入」：只要利润，滚动数组本来就是一遍扫描；要还原，需要记录候选买入点。
- 「买卖价差（bid-ask spread）」：买用 ask、卖用 bid，把价格拆成两个数组，状态机不变。
