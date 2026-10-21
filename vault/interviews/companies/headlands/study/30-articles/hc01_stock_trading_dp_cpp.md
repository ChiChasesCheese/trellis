# hc01 · 买卖股票家族（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

给你一只股票连续 n 天的收盘价 `prices[i]`（非负整数，单位是最小报价单位 tick，不超过 2^40）。同一时刻最多持有**一股**；买之前必须先卖掉手里的；同一天只能做一个动作（买、卖、休息三选一）。问最多能赚多少。面试官一路加规则：

| Part | 内容 | 入口 |
|---|---|---|
| 1 | 只能买卖**一次**：先写 O(n²) 暴力，再改成 O(n) | `max_profit_brute` · `max_profit_once` |
| 2 | 次数**不限** | `max_profit_unlimited` |
| 3 | 最多 **k 笔**交易（k 可以是 `INT_MAX`） | `max_profit_at_most` |
| 4 | 加**冷却**（卖出后的下一天不能买）/ **手续费**（每笔卖出扣）；还原具体的买卖日；写一个检查器回放方案 | `max_profit` · `plan` · `try_plan` · `replay` |

一笔**交易**（transaction）= 一次买入 + 之后的一次卖出；「最多 k 笔」按买入次数数。

手算：

| 规则 | prices | 答案 | 说明 |
|---|---|---|---|
| 一次 | `[7,1,5,3,6,4]` | 5 | 第 1 天买、第 4 天卖 |
| 不限 | `[7,1,5,3,6,4]` | 7 | 1→5 赚 4，3→6 赚 3 |
| k=2 | `[3,2,6,5,0,3]` | 7 | 2→6 赚 4，0→3 赚 3 |
| 不限 + 冷却 | `[1,2,3,0,2]` | 3 | 第 0 天买第 1 天卖，第 3 天买第 4 天卖 |
| 不限 + fee=2 | `[1,3,2,8,4,9]` | 8 | 1→8 赚 5，4→9 赚 3 |

## 2. 地基：类型、边界、不会溢出的理由

先看文件开头。

```cpp
// hc01 · Best time to buy and sell stock family — C++20 reference.  Statement: ../problem.md (Java: reference/StockTrading.java).
// Parts: 1 one trade (brute O(n^2), then O(n)), 2 unlimited, 3 at most k (state machine + rolling array),
//        4 cooldown / fee / recovering the trades (plan) / replaying a plan with the State machine.
#pragma once

#include <algorithm>
#include <array>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <ranges>
#include <span>
#include <stdexcept>
#include <string>
#include <utility>
#include <variant>
#include <vector>

namespace stock {

/// Price bound 2^40 ticks: profit <= (days/2) * price <= 2^21 * 2^40 = 2^61 < 2^63, so nothing in the loops can overflow.
inline constexpr long long MAX_PRICE = 1LL << 40;
inline constexpr int MAX_DAYS = 1 << 22;
/// plan() records one byte per (day, transaction count) cell.
inline constexpr long long MAX_PLAN_CELLS = 1LL << 28;

/// Read-only view of the prices.  A span cannot be null and never copies: vector, std::array and C arrays all convert.
using Prices = std::span<const long long>;

namespace detail {
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

/// Signed overflow is undefined behaviour, so the compiler builtin does the check (no "check afterwards").
inline long long checked_add(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("add overflows long long");
    return r;
}
inline long long checked_sub(long long a, long long b) {
    long long r;
    if (__builtin_sub_overflow(a, b, &r)) throw std::overflow_error("sub overflows long long");
    return r;
}
}  // namespace detail
```

* **价格上界 2^40，天数上界 2^22**：利润最多 2^21 笔 × 2^40 = 2^61 < 2^63，所以 `long long` 的加减在循环里**永远不会溢出**，内循环不需要检查。「从源头消灭溢出」比「到处检查溢出」便宜。
* **`std::span<const long long>`**（`Prices`）：只读视图，不拷贝，`std::vector`、`std::array`、C 数组都能隐式转换。Java 的 `long[]` 可以是 `null`（要测 `NullPointerException`）；`span` 不可能为 null，这一类 bug 在类型层面消失了。
* **有符号溢出是未定义行为（UB）**，不能"先加再检查"。需要检查的地方（`replay` 里累加现金）用编译器内建 `__builtin_add_overflow`，溢出时抛 `std::overflow_error`。
* `overloaded` 是把多个 lambda 拼成一个函数对象的小工具，配合 `std::visit` 用（Part 4）。

接着是数据类型。

```cpp
// ------------------------------------------------------------------------------------------------ data types
/// One complete trade: buy on buy_day, sell on sell_day (days count from 0).
struct Trade {
    int buy_day;
    int sell_day;
    Trade(int buy, int sell) : buy_day(buy), sell_day(sell) {
        if (buy < 0 || sell <= buy)
            throw std::invalid_argument("need 0 <= buy_day < sell_day: " + std::to_string(buy) + "," + std::to_string(sell));
    }
    friend bool operator==(const Trade&, const Trade&) = default;
};

struct Plan {
    long long profit;
    std::vector<Trade> trades;
    friend bool operator==(const Plan&, const Plan&) = default;
};

/// max_transactions: at most this many buys; fee: charged on every sell; cooldown: the day after a sell is rest-only.
struct Rules {
    static constexpr int UNLIMITED = INT_MAX;
    int max_transactions;
    long long fee;
    bool cooldown;

    Rules(int k, long long fee_, bool cooldown_) : max_transactions(k), fee(fee_), cooldown(cooldown_) {
        if (k < 0) throw std::invalid_argument("max_transactions < 0");
        if (fee_ < 0 || fee_ > MAX_PRICE) throw std::invalid_argument("fee out of range: " + std::to_string(fee_));
    }
    static Rules at_most(int k) { return Rules(k, 0, false); }
    static Rules unlimited() { return Rules(UNLIMITED, 0, false); }
    Rules with_fee(long long f) const { return Rules(max_transactions, f, cooldown); }
    Rules with_cooldown(bool on) const { return Rules(max_transactions, fee, on); }
    friend bool operator==(const Rules&, const Rules&) = default;
};

/// An illegal State transition (Java: IllegalStateException).  Not std::invalid_argument: that is a different mistake.
struct IllegalState : std::logic_error {
    using std::logic_error::logic_error;
};

/// The state at the end of a day.  An enum class can hold any int, so even a cast garbage value must not crash the functions below.
enum class State { FREE, HOLD, COOL };

inline const char* name(State s) {
    switch (s) {
        case State::FREE: return "FREE";
        case State::HOLD: return "HOLD";
        case State::COOL: return "COOL";
    }
    return "?";
}

inline State after_rest(State s) { return s == State::COOL ? State::FREE : s; }
inline State after_buy(State s) {
    if (s != State::FREE) throw IllegalState(std::string("cannot buy while ") + name(s));
    return State::HOLD;
}
inline State after_sell(State s, const Rules& rules) {
    if (s != State::HOLD) throw IllegalState(std::string("cannot sell while ") + name(s));
    return rules.cooldown ? State::COOL : State::FREE;
}

/// A day's action: buy or sell (rest = no action).  A closed set, so std::visit is checked exhaustive at compile time.
struct Buy { int day; };
struct Sell { int day; };
using Move = std::variant<Buy, Sell>;
```

* `Trade`、`Rules` 的构造函数守住自己的不变量（`0 <= buy_day < sell_day`，`fee` 在范围内），之后所有代码都可以信任它们。
* `State` 是 `enum class`：`FREE`（空仓，明天可买）、`HOLD`（持有一股）、`COOL`（今天刚卖出，明天只能休息）。三个转移函数 `after_rest` / `after_buy` / `after_sell` 把规则写成表：只有 `FREE` 能买，只有 `HOLD` 能卖，`COOL` 过一天变 `FREE`。
* **`IllegalState` 为什么自己定义**：`std::invalid_argument` 是 `std::logic_error` 的子类。`replay` 要把「状态机转移非法」翻译成 `invalid_argument`，如果状态机直接抛 `logic_error`，`catch (const std::logic_error&)` 就会把别处抛出的 `invalid_argument` 一起吞掉。单独一个类型，才能只接住这一种错误。
* **`enum class` 可以装任何整数**（`static_cast<State>(7)`）。转移函数对这种值要么原样返回（`after_rest`），要么抛 `IllegalState`，不能拿它去索引数组。
* `Move = std::variant<Buy, Sell>`：一天的动作只有两种，「休息」就是这天没有动作（`std::optional<Move>` 为空）。

## 3. Part 1：只能交易一次

```cpp
// ------------------------------------------------------------------------------------------------ validation
inline void check(Prices p) {
    if (p.size() > static_cast<std::size_t>(MAX_DAYS)) throw std::invalid_argument("too many days: " + std::to_string(p.size()));
    for (std::size_t i = 0; i < p.size(); ++i)
        if (p[i] < 0 || p[i] > MAX_PRICE)
            throw std::invalid_argument("price[" + std::to_string(i) + "] out of range: " + std::to_string(p[i]));
}

// ------------------------------------------------------------------------------------------------ Part 1
/// Brute force over every (buy i, sell j > i).  O(n^2); kept as the oracle for the linear version.
inline long long max_profit_brute(Prices p) {
    check(p);
    long long best = 0;  // 0 = do nothing
    for (std::size_t i = 0; i < p.size(); ++i)
        for (std::size_t j = i + 1; j < p.size(); ++j) best = std::max(best, p[j] - p[i]);
    return best;
}

/// O(n) time, O(1) space: scan once, remember the lowest price seen so far.
inline long long max_profit_once(Prices p) {
    check(p);
    long long min_so_far = LLONG_MAX, best = 0;
    for (long long x : p) {
        if (x < min_so_far) min_so_far = x;
        else best = std::max(best, x - min_so_far);
    }
    return best;
}
```

* **暴力**：试遍所有（买入日 i，卖出日 j > i），取 `p[j] - p[i]` 的最大值，至少是 0（可以一笔都不做）。O(n²)，留着当后面解法的标准答案。
* **O(n)**：对每个卖出日 j，最好的买入日就是 j 之前价格最低的那天。所以边扫边记 `min_so_far`。注意是「j **之前**的最低价」，不是全局最低：`[10,9,8,1]` 的答案是 0，不是 9。
* 校验：天数超过 `MAX_DAYS` 或任何价格不在 `[0, MAX_PRICE]` → `std::invalid_argument`。放在所有 Part 的最前面。
* 循环写法：`for (std::size_t j = i + 1; ...)`。`size()` 是**无符号**，`p.size() - 1` 对空输入是 `SIZE_MAX`：

```cpp
// Unsigned and signed arithmetic traps around sizes and k.
#include <climits>
#include <iostream>
#include <vector>

int main() {
    const std::vector<long long> empty;
    std::cout << "empty.size() - 1 = " << empty.size() - 1 << "   <- loop `i < size() - 1` would run ~2^64 times\n";

    int k = INT_MAX, k_plus_one = 0;
    const bool overflowed = __builtin_add_overflow(k, 1, &k_plus_one);
    std::cout << "INT_MAX + 1 overflows: " << std::boolalpha << overflowed << "   <- `vector(k + 1)` is signed overflow (UB) for k = INT_MAX\n";

    const long long cells_wrong_if_int = static_cast<long long>(100'001) * 50'000;
    std::cout << "(n + 1) * (k + 1) = " << cells_wrong_if_int << " does not fit in int (max " << INT_MAX << "): form the product in long long\n";
}
```

```text
empty.size() - 1 = 18446744073709551615   <- loop `i < size() - 1` would run ~2^64 times
INT_MAX + 1 overflows: true   <- `vector(k + 1)` is signed overflow (UB) for k = INT_MAX
(n + 1) * (k + 1) = 5000050000 does not fit in int (max 2147483647): form the product in long long
```

  所以循环都写成 `i = 1; i < size()`，不写 `i < size() - 1`。

## 4. Part 2：次数不限

```cpp
// ------------------------------------------------------------------------------------------------ Part 2
/// Unlimited trades: the sum of every day-over-day rise.  The loop starts at 1, so an empty input never reaches `size() - 1` (which wraps).
inline long long max_profit_unlimited(Prices p) {
    check(p);
    long long sum = 0;
    for (std::size_t i = 1; i < p.size(); ++i)
        if (p[i] > p[i - 1]) sum += p[i] - p[i - 1];
    return sum;
}
```

不限次数时，一段上涨 a < b < c 拆成 (a→b) + (b→c) 利润一样，所以答案 = 所有「今天比昨天贵」的差之和。`[7,1,5,3,6,4]`：1→5 是 4，3→6 是 3，合计 7。

## 5. Part 3：最多 k 笔（状态机 DP + 滚动数组）

**状态**：对每个 j（用了几次买入），记两个数：

* `idle[j]`：手里没股票、**最多**买过 j 次时，最多有多少现金；
* `held[j]`：手里有一股、买入这一股算在 j 次之内时，最多有多少现金（买股票花了钱，所以通常是负的）。

**转移**：每天用「昨天的值」算「今天的值」：

```
idle'[j] = max(idle[j], held[j] + price)        休息，或者今天卖
held'[j] = max(held[j], idle[j-1] - price)      休息（继续持有），或者今天买（买之前只用过 j-1 次）
```

初值：`idle` 全 0（什么都没做），`held` 全是「不可能」的哨兵 `NEG`。答案 `idle[k]`。

手算 k=1，`[3,2,6]`：初值 idle=0，held=NEG。第 1 天（3）：idle=max(0, NEG+3)=0，held=max(NEG, 0−3)=−3。第 2 天（2）：held=max(−3, 0−2)=−2。第 3 天（6）：idle=max(0, −2+6)=4。答案 4（2 买 6 卖）。

**滚动数组（rolling array）**：完整的表是「天数 × k」，明天只依赖今天，所以只留一行 `dp[j]`。`held'[j]` 要读**昨天的** `idle[j-1]`，所以 `j` 从大到小更新：算 j 时 `idle[j-1]` 还没被今天覆盖。

```cpp
// ------------------------------------------------------------------------------------------------ Part 3
/// "Cannot be reached yet".  LLONG_MIN / 4, not LLONG_MIN: NEG - price or NEG + price - fee must not overflow.
inline constexpr long long NEG = LLONG_MIN / 4;

/// dp[j] = {idle, held}: idle = best cash with no share after at most j buys; held = best cash holding a share bought as buy number j.
/// j runs downwards so dp[j - 1] still holds yesterday's values when dp[j] is updated: that is the rolling array.
inline long long max_profit_at_most(int k, Prices p) {
    if (k < 0) throw std::invalid_argument("k < 0");
    check(p);
    const int n = static_cast<int>(p.size());
    if (k == 0 || n < 2) return 0;
    if (k >= n / 2) return max_profit_unlimited(p);  // n days hold at most n/2 trades; also keeps k + 1 (INT_MAX + 1 is UB) away from the allocation
    std::vector<std::array<long long, 2>> dp(static_cast<std::size_t>(k) + 1, std::array<long long, 2>{0, NEG});
    for (long long price : p) {
        for (int j = k; j >= 1; --j) {
            auto& [idle, held] = dp[static_cast<std::size_t>(j)];
            idle = std::max(idle, held + price);                                     // sell: uses yesterday's held[j]
            held = std::max(held, dp[static_cast<std::size_t>(j) - 1][0] - price);  // buy: uses yesterday's idle[j-1]
        }
    }
    return dp[static_cast<std::size_t>(k)][0];
}
```

要点：

1. **`std::vector<std::array<long long, 2>>`**：同一个 j 的 `idle` 和 `held` 挨在一起（16 字节），每次内层循环读写同一个缓存行；用两个独立的 vector 要碰两条。结构化绑定 `auto& [idle, held] = dp[j]` 给它们起名字。
2. **`k >= n / 2` 直接转成「不限次数」**：n 天最多完成 n/2 笔。这一行同时避开了两个坑：`k + 1`（`k = INT_MAX` 时有符号溢出，UB）和一个 k+1 个元素的巨大分配。
3. **哨兵 `NEG = LLONG_MIN / 4`，不是 `LLONG_MIN`**：不可达状态上还会做 `NEG + price`、`NEG - price`、`- fee`，对 `LLONG_MIN` 做 `- price` 就是溢出：

```cpp
// "Not reachable yet" needs a sentinel that survives `+ price - fee` without overflowing.
#include <climits>
#include <iostream>

int main() {
    constexpr long long price = 1LL << 40, fee = 1LL << 40;
    for (long long neg : {LLONG_MIN, LLONG_MIN / 4}) {
        long long a, b;
        const bool o1 = __builtin_add_overflow(neg, price, &a);   // NEG + price
        const bool o2 = __builtin_sub_overflow(a, fee, &b);        // ... - fee
        const bool o3 = __builtin_sub_overflow(neg, price, &a);   // NEG - price (a buy from an unreachable state)
        std::cout << (neg == LLONG_MIN ? "LLONG_MIN     " : "LLONG_MIN / 4 ") << "  NEG+price: " << (o1 ? "overflow" : "ok")
                  << "   -fee: " << (o2 ? "overflow" : "ok") << "   NEG-price: " << (o3 ? "overflow" : "ok") << "\n";
    }
}
```

```text
LLONG_MIN       NEG+price: ok   -fee: ok   NEG-price: overflow
LLONG_MIN / 4   NEG+price: ok   -fee: ok   NEG-price: ok
```

4. 时间 O(n · min(k, n/2))，空间 O(min(k, n/2))。

## 6. Part 4：冷却、手续费、还原交易

**手续费**只改一处：卖出时现金少 `fee`（`held + price - fee`）。

**冷却**多一个状态：卖出不再直接回 `idle`，而是先进 `cool`；下一天 `cool` 才并入 `idle`：

```
cool'[j] = held[j] + price - fee                 今天卖出
idle'[j] = max(idle[j], cool[j])                 休息，或者冷却结束
held'[j] = max(held[j], idle[j-1] - price)       买入只看「昨天的 idle」
```

**更新顺序**：买入必须读**昨天**的 `idle`。如果读今天刚更新的 `idle'`（里面含「昨天卖出、今天冷却结束」的钱），就等于卖出的**第二天**又买：

```cpp
// Rolling DP with a cooldown: every transition must read YESTERDAY's values.  Reading today's already-updated `idle` lets
// a buy happen the day the cooldown ends... or, here, the day after the sale.
#include <algorithm>
#include <array>
#include <climits>
#include <iostream>
#include <vector>

constexpr long long NEG = LLONG_MIN / 4;

long long with_cooldown(const std::vector<long long>& prices, bool read_todays_idle) {
    std::array<long long, 3> s{0, NEG, NEG};  // {idle, held, cool}
    for (long long p : prices) {
        const auto yesterday = s;
        s[2] = yesterday[1] + p;                                   // sold today
        s[0] = std::max(yesterday[0], yesterday[2]);               // rest, or the cooldown ended
        s[1] = std::max(yesterday[1], (read_todays_idle ? s[0] : yesterday[0]) - p);  // buy
    }
    return std::max(s[0], s[2]);
}

int main() {
    const std::vector<long long> prices{1, 2, 3, 0, 2};
    std::cout << "buy from yesterday's idle: " << with_cooldown(prices, false) << "   (correct: 3)\n";
    std::cout << "buy from today's idle:     " << with_cooldown(prices, true) << "   (wrong: sells on day 1 and buys again on day 2, the cooldown day)\n";
}
```

```text
buy from yesterday's idle: 3   (correct: 3)
buy from today's idle:     4   (wrong: sells on day 1 and buys again on day 2, the cooldown day)
```

没有冷却时这两种读法凑巧一样（同价卖了又买，现金不变），所以只靠 Part 3 的测试发现不了；样例 `[1,2,3,0,2]` 能抓到。习惯：**每个转移只用昨天的值**。代码里先把 `old_free / old_hold / old_cool` 存进局部变量。

引擎 `detail::run`，同时支持「有 / 无冷却」「有 / 无次数上限」；`how` 是可选的决策记录，只有 `plan` 才传：

```cpp
// ------------------------------------------------------------------------------------------------ Part 4
namespace detail {
struct Solved {
    long long profit;
    State end;
};
enum Slot : std::size_t { F = 0, H = 1, C = 2 };

/// General DP: dp[j] = {free, hold, cool}.  how (optional, only plan() passes it) stores two bits per cell:
/// bit 0 = this day's hold came from buying today, bit 1 = this day's free was not a plain rest.  Ties pick "rest" (strictly greater wins).
inline Solved run(const Rules& rules, Prices p, std::vector<unsigned char>* how) {
    const int n = static_cast<int>(p.size());
    const bool unbounded = rules.max_transactions >= n / 2;
    const int bound = unbounded ? 0 : rules.max_transactions;  // unlimited: the "how many trades" dimension collapses to one cell
    const std::size_t w = static_cast<std::size_t>(bound) + 1;
    const long long fee = rules.fee;
    std::vector<std::array<long long, 3>> dp(w, std::array<long long, 3>{0, NEG, NEG});
    for (int i = 1; i <= n; ++i) {
        const long long price = p[static_cast<std::size_t>(i) - 1];
        for (int j = bound; j >= 0; --j) {
            const int src = unbounded ? j : j - 1;  // the money for a buy comes from free[src]
            auto& d = dp[static_cast<std::size_t>(j)];
            const long long old_free = d[F], old_hold = d[H], old_cool = d[C];
            const long long buy = src >= 0 ? dp[static_cast<std::size_t>(src)][F] - price : NEG;  // still yesterday's value
            const long long sell = old_hold + price - fee;
            unsigned char bits = 0;
            if (buy > old_hold) { d[H] = buy; bits |= 1; }
            if (rules.cooldown) {
                d[C] = sell;                                         // sold today -> COOL
                if (old_cool > old_free) { d[F] = old_cool; bits |= 2; }  // cooldown over -> FREE
            } else if (sell > old_free) {
                d[F] = sell;                                          // sell straight back to FREE
                bits |= 2;
            }
            if (how) (*how)[static_cast<std::size_t>(i) * w + static_cast<std::size_t>(j)] = bits;
        }
    }
    const auto& last = dp[static_cast<std::size_t>(bound)];
    if (rules.cooldown && last[C] > last[F]) return {last[C], State::COOL};
    return {last[F], State::FREE};
}
}  // namespace detail
```

* `unbounded`（`max_transactions >= n / 2`）时「交易次数」这一维压成 1 格（`bound = 0`）。
* **平局一律选「休息」**（严格大于才改变），所以不会产生零利润的交易。
* `how` 每格两个比特：bit0 = 这一天的 `held` 是「今天买」得来的；bit1 = 这一天的 `idle` 不是单纯休息。

**还原交易（backtracking）**：正向填表时记下每格的决定；填完从终点倒着走，沿决策记录跳回起点，遇到「买」或「卖」就记一笔。倒着走时先碰到卖出日，所以要一个「还没配上买入日的卖出日」——这正是 `std::optional<int>`：

```cpp
/// Max profit, number only.  O(n * min(k, n/2)) time, O(min(k, n/2)) space.
inline long long max_profit(const Rules& rules, Prices p) {
    check(p);
    if (p.size() < 2) return 0;
    return detail::run(rules, p, nullptr).profit;
}

/// Max profit and the trades.  std::nullopt when the decision table would exceed MAX_PLAN_CELLS (the product is formed in long long:
/// (n + 1) * (k + 1) is far beyond int).
inline std::optional<Plan> try_plan(const Rules& rules, Prices p) {
    check(p);
    const int n = static_cast<int>(p.size());
    if (n < 2) return Plan{0, {}};
    const bool unbounded = rules.max_transactions >= n / 2;
    const int bound = unbounded ? 0 : rules.max_transactions;
    const std::size_t w = static_cast<std::size_t>(bound) + 1;
    const long long cells = static_cast<long long>(n + 1) * static_cast<long long>(w);
    if (cells > MAX_PLAN_CELLS) return std::nullopt;
    std::vector<unsigned char> how(static_cast<std::size_t>(cells), 0);
    const detail::Solved solved = detail::run(rules, p, &how);

    std::vector<Trade> reversed;  // walking backwards: the last trade is found first
    State state = solved.end;
    int j = bound;
    std::optional<int> pending_sell;  // the sell day of the trade whose buy we have not met yet
    for (int i = n; i >= 1; --i) {
        const unsigned bits = how[static_cast<std::size_t>(i) * w + static_cast<std::size_t>(j)];
        const int day = i - 1;
        switch (state) {
            case State::HOLD:
                if (bits & 1u) {  // bought today
                    reversed.emplace_back(day, pending_sell.value());  // .value() throws if the DP and the walk ever disagree; * would be UB
                    pending_sell.reset();
                    state = State::FREE;
                    if (!unbounded) --j;
                }
                break;
            case State::COOL:  // being COOL means: sold on this day
                pending_sell = day;
                state = State::HOLD;
                break;
            case State::FREE:
                if (bits & 2u) {
                    if (rules.cooldown) state = State::COOL;  // sold yesterday, cooldown ends today
                    else { pending_sell = day; state = State::HOLD; }  // sold today, straight back to FREE
                }
                break;
        }
    }
    if (state != State::FREE) throw std::logic_error("backtrack ended in " + std::string(name(state)));
    Plan plan{solved.profit, {}};
    long long sum = 0;
    for (const Trade& t : reversed | std::views::reverse) {
        const long long net = detail::checked_sub(p[static_cast<std::size_t>(t.sell_day)] - p[static_cast<std::size_t>(t.buy_day)], rules.fee);
        if (net > 0) {  // ties already prefer rest; a trade with net <= 0 would not change the total anyway
            plan.trades.push_back(t);
            sum = detail::checked_add(sum, net);
        }
    }
    if (sum != solved.profit) throw std::logic_error("plan sum != dp");
    return plan;
}

inline Plan plan(const Rules& rules, Prices p) {
    if (auto r = try_plan(rules, p)) return std::move(*r);
    throw std::invalid_argument("plan too large: more than " + std::to_string(MAX_PLAN_CELLS) + " cells");
}
```

* **`try_plan` 返回 `std::optional<Plan>`**：决策表太大（格子数超过 `MAX_PLAN_CELLS`）不是调用者输入错了，而是「这次给不出答案」，用 `nullopt` 表示；`plan` 是包一层的版本，没有答案就抛 `std::invalid_argument`。输入真的非法（价格越界）仍然是异常。
* **格子数要用 64 位算**：`(n + 1) * (k + 1)` 在 n = 10 万、k = 5 万时约 50 亿，装不进 `int`。先转 `long long` 再乘。
* `pending_sell.value()` 而不是 `*pending_sell`：如果回溯与 DP 不一致，`value()` 抛 `std::bad_optional_access`（响亮的失败），`*` 对空 optional 是 UB：

```cpp
// std::optional for "may not exist": a plan that is too big, or a sell day that has not been seen yet.
#include <iostream>
#include <optional>
#include <string>

std::optional<int> plan_cells(long long n, long long w) {
    const long long cells = (n + 1) * w;               // 64-bit product
    if (cells > (1LL << 28)) return std::nullopt;       // too big: not an error in the caller's input, just "no answer"
    return static_cast<int>(cells);
}

int main() {
    if (const auto c = plan_cells(100'000, 100)) std::cout << "100k days, 100 trades: " << *c << " cells\n";
    if (!plan_cells(100'000, 50'000)) std::cout << "100k days, 50k trades: nullopt\n";

    std::optional<int> pending_sell;   // empty until the walk meets a sell
    try {
        std::cout << pending_sell.value() << "\n";       // throws std::bad_optional_access: a bug becomes a loud failure
    } catch (const std::bad_optional_access& e) {
        std::cout << "value() on an empty optional throws: " << e.what() << "  (`*pending_sell` would be undefined behaviour)\n";
    }
}
```

```text
100k days, 100 trades: 10000100 cells
100k days, 50k trades: nullopt
value() on an empty optional throws: bad_optional_access  (`*pending_sell` would be undefined behaviour)
```

**`replay`**：用 `State` 状态机逐天回放一个方案，检查它合法并算出利润：

```cpp
/// Replay a plan day by day with the State machine; returns the profit (fee charged on every sell).
inline long long replay(const Rules& rules, Prices p, const std::vector<Trade>& trades) {
    check(p);
    const int n = static_cast<int>(p.size());
    if (trades.size() > static_cast<std::size_t>(rules.max_transactions))
        throw std::invalid_argument(std::to_string(trades.size()) + " trades > limit " + std::to_string(rules.max_transactions));
    std::vector<std::optional<Move>> moves(p.size());  // one slot per day; empty = rest
    for (const Trade& t : trades) {
        if (t.sell_day >= n) throw std::invalid_argument("day out of range: " + std::to_string(t.sell_day));
        auto& b = moves[static_cast<std::size_t>(t.buy_day)];
        auto& s = moves[static_cast<std::size_t>(t.sell_day)];
        if (b.has_value() || s.has_value()) throw std::invalid_argument("two actions on one day");
        b = Buy{t.buy_day};
        s = Sell{t.sell_day};
    }
    State state = State::FREE;
    long long cash = 0;
    try {
        for (int day = 0; day < n; ++day) {
            const auto& mv = moves[static_cast<std::size_t>(day)];
            if (!mv) { state = after_rest(state); continue; }
            state = std::visit(detail::overloaded{
                                   [&](const Buy& b) {
                                       cash = detail::checked_sub(cash, p[static_cast<std::size_t>(b.day)]);
                                       return after_buy(state);
                                   },
                                   [&](const Sell& s) {
                                       cash = detail::checked_add(cash, p[static_cast<std::size_t>(s.day)] - rules.fee);
                                       return after_sell(state, rules);
                                   }},
                               *mv);
        }
    } catch (const IllegalState& e) {
        throw std::invalid_argument(std::string("illegal plan: ") + e.what());
    }
    return cash;
}

}  // namespace stock
```

* 先建 `std::vector<std::optional<Move>>`，每天一格；一个格子被占两次就是「同一天两个动作」（包括同一天卖出又买入）。
* `std::visit(overloaded{...}, *mv)`：两个 lambda 分别处理 `Buy`、`Sell`。**漏掉一个类型编译不过**，不需要 `default`；以后加 `Move` 的新类型，这里立刻报错。
* `after_buy` / `after_sell` 抛 `IllegalState`，在边界翻译成 `std::invalid_argument`；重叠、冷却期内买入、没持有就卖都由状态机报出来，`replay` 自己不用分别判断。

## 7. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| 输入 | `long[]`（可为 `null` → `NullPointerException`） | `std::span<const long long>`（不可能为 null，不拷贝，不修改） |
| 溢出 | `Math.addExact` 抛 `ArithmeticException` | 有符号溢出是 UB；用 `__builtin_add_overflow`，或像本题一样从上界保证不会溢出 |
| `k + 1` | 溢出回绕成负数 → `NegativeArraySizeException` | UB（编译器可以假设它不发生）；先 `k >= n/2` 分流 |
| 大小 | `int length`（有符号） | `size_t`（无符号）：`size() - 1` 回绕；格子数用 `long long` |
| 不确定的结果 | 抛异常 | `std::optional`（`try_plan`），输入非法才抛 |
| 状态机 | `enum` + 方法，`IllegalStateException` | `enum class` + 自由函数，自定义 `IllegalState`；`enum class` 里可以有「非法值」 |
| 动作类型 | `sealed interface` + `record` + 模式匹配 `switch` | `std::variant` + `std::visit(overloaded{...})`，同样编译期穷尽 |
| 还原时的 `pendingSell = -1` | 哨兵整数 | `std::optional<int>`，`value()` 在空时抛异常 |
| 逆序遍历 | `list.reversed()`（Sequenced Collections） | `reversed | std::views::reverse` |

## 8. 陷阱

1. `i < p.size() - 1`：空输入回绕成 `SIZE_MAX`。
2. `std::vector<...> dp(k + 1)` 且 `k == INT_MAX`：有符号溢出。
3. `NEG = LLONG_MIN`：`NEG - price` 溢出。
4. `(n + 1) * (k + 1)` 用 `int` 算。
5. `min_so_far` 取全局最小而不是「之前的最小」。
6. `j` 从小到大更新滚动数组，且 Part 4 买入读了今天的 `idle`。
7. 平局时偏向「买 / 卖」，产生零利润的交易，或者同一天既卖又买。
8. `*opt` 解引用空 `optional`（UB）。
9. 把 `IllegalState` 继承 `invalid_argument`，一个 `catch` 吞掉两种错误。
10. 用 `int` 存价格差：价格到 2^40，`int` 装不下。

## 9. 面试官会追问什么（senior）

**Q1. 为什么 k 笔的问题不能贪心？** 贪心只对「不限次数」成立（每段上涨都拿）。有 k 的限制后，哪几段上涨值得占用名额取决于全局，所以需要 DP；也可以用「凸性 + 反悔贪心 / 优先队列」做到 O(n log n)，但面试里先把 DP 讲清楚。

**Q2. 空间能再小吗？** 只要利润数字：O(min(k, n/2))，且 n 天可以流式处理（价格来一个更新一次）。要还原交易就需要决策表，O(n · k) 字节。

**Q3. 价格是流式的、存不下怎么办？** 利润数字：滚动数组天然是一遍扫描。要日期：保留候选买入点（`min_so_far` 对应的日期，或 k 个候选），存下的只有 O(k) 个日期。

**Q4. 有买卖价差（bid / ask）怎么改？** 买用 ask、卖用 bid，把一个价格数组拆成两个，状态机不变。

**Q5. 多只股票共享本金？** 已经是背包 / 带约束的优化，不是同一个问题。

**Q6. 怎么证明你的 DP 对？** 写一个枚举所有（买 < 卖 < 买 < 卖……）序列的朴素解当标准答案，随机小输入对拍（本题的测试就是这么做的）；再加性质检查：k 增大利润单调不降、`Rules` 取极端值时退化成前面的 Part。

**Q7. `plan` 和 `max_profit` 为什么分开？** 只要数字就别付 O(n · k) 字节的决策表；`try_plan` 在格子数超限时返回 `nullopt` 让调用者决定退化策略。

**Q8. 价格不是整数（`double`）怎么办？** 利润的加减会累积舍入误差，平局判断（「严格大于才改变」）不再可靠；金融里用整数 tick 或定点数，这也是题目用 tick 的原因。

**Q9. 为什么 `held` / `idle` 放进 `std::array<long long, 2>`，而不是两个 vector？** 同一个 j 的两个数挨着，一次缓存行读写就够；而且 `dp[j]` 与 `dp[j-1]` 相邻，下一步迭代也在同一行附近。

## 10. 自测

1. `max_profit_at_most(INT_MAX, prices)` 为什么不会在 `dp(k + 1)` 处出问题？
2. 滚动数组里 `j` 为什么从大到小？没有冷却时从小到大会错吗？有冷却呢？
3. `NEG` 取 `LLONG_MIN / 4` 而不是 `LLONG_MIN`，是为了防什么？
4. `try_plan` 为什么返回 `optional`，而价格越界仍然抛异常？
5. `State` 是 `enum class`，`after_buy(static_cast<State>(7))` 应该怎样？
6. `std::visit` 比 `if (std::holds_alternative<Buy>(...))` 好在哪里？

<details><summary>答案</summary>

1. `k >= n / 2` 在分配之前就转成了不限次数，`k + 1` 永远不会被求值；否则 `INT_MAX + 1` 是 UB，而且会尝试分配 2^31 个元素。
2. 因为 `held'[j]` 要读昨天的 `idle[j-1]`；从大到小时 `idle[j-1]` 还没被今天覆盖。没有冷却时从小到大答案碰巧相同（同价卖了又买现金不变），但用到了今天的值，加上冷却就会在第二天买入而出错。
3. `NEG` 还要参与 `+ price`、`- price`、`- fee`；对 `LLONG_MIN` 减一个正数就是有符号溢出（UB）。除以 4 留足余量。
4. 决策表过大是「这次给不出答案」，不是输入错误，用 `nullopt` 让调用者选择退化策略；价格越界是调用者的错误，仍然是异常。
5. 抛 `IllegalState`（它不是 `FREE`）。`enum class` 可以容纳任何整数，不能把它当索引用，也不能假设只有三个值。
6. 编译器检查穷尽：漏掉一个类型、或以后给 `Move` 增加类型，都会编译失败；`holds_alternative` 链不会提醒你，还容易忘写 `else`。

</details>
