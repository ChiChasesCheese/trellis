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

// ------------------------------------------------------------------------------------------------ Part 2
/// Unlimited trades: the sum of every day-over-day rise.  The loop starts at 1, so an empty input never reaches `size() - 1` (which wraps).
inline long long max_profit_unlimited(Prices p) {
    check(p);
    long long sum = 0;
    for (std::size_t i = 1; i < p.size(); ++i)
        if (p[i] > p[i - 1]) sum += p[i] - p[i - 1];
    return sum;
}

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
