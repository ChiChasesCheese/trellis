// hc01 · Best time to buy and sell stock family — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <climits>
#include <cstddef>
#include <optional>
#include <span>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace stock {

/// Price bound 2^40: keeps every profit (at most 2^21 trades * 2^40) inside long long, so the inner loops need no overflow checks.
inline constexpr long long MAX_PRICE = 1LL << 40;
inline constexpr int MAX_DAYS = 1 << 22;
/// try_plan() / plan() refuse a table with more than this many (day, transaction count) cells.
inline constexpr long long MAX_PLAN_CELLS = 1LL << 28;

/// Read-only view of the prices: a vector, a std::array or a C array all convert.  A span cannot be null.
using Prices = std::span<const long long>;

// ------------------------------------------------------------------------------------------------ data types (given)
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

/// An illegal State transition (Java: IllegalStateException).
struct IllegalState : std::logic_error {
    using std::logic_error::logic_error;
};

/// FREE: no share, may buy.  HOLD: one share.  COOL: sold today, tomorrow is rest-only.
enum class State { FREE, HOLD, COOL };

/// A day's action: buy or sell (rest = no action).
struct Buy { int day; };
struct Sell { int day; };
using Move = std::variant<Buy, Sell>;

// ------------------------------------------------------------------------------------------------ State machine (to write)
/// COOL -> FREE, everything else unchanged.
inline State after_rest(State) { throw std::logic_error("TODO"); }
/// Only FREE may buy -> HOLD; any other state throws IllegalState.
inline State after_buy(State) { throw std::logic_error("TODO"); }
/// Only HOLD may sell -> COOL (rules.cooldown) or FREE; any other state throws IllegalState.
inline State after_sell(State, const Rules&) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 1
/// Brute force O(n^2).  Input validation (all Parts): more than MAX_DAYS days or a price outside [0, MAX_PRICE] -> std::invalid_argument.
inline long long max_profit_brute(Prices) { throw std::logic_error("TODO"); }
/// O(n) time, O(1) space: remember the lowest price so far.
inline long long max_profit_once(Prices) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 2
inline long long max_profit_unlimited(Prices) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 3
/// k < 0 -> std::invalid_argument.  k >= n / 2 is the unlimited case: never allocate k + 1 slots (k can be INT_MAX).
inline long long max_profit_at_most(int, Prices) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 4
inline long long max_profit(const Rules&, Prices) { throw std::logic_error("TODO"); }

/// Profit + trades (time-ordered, each with net profit > 0).  std::nullopt when (n + 1) * (min(k, n/2) + 1) > MAX_PLAN_CELLS.
inline std::optional<Plan> try_plan(const Rules&, Prices) { throw std::logic_error("TODO"); }

/// Like try_plan, but a too-large table throws std::invalid_argument.
inline Plan plan(const Rules&, Prices) { throw std::logic_error("TODO"); }

/// Replay a plan day by day with the State machine; returns the profit (fee charged on every sell).
/// Illegal plan (more than max_transactions trades, a day >= n, two actions on one day, overlap, buy during cooldown,
/// sell without a share) -> std::invalid_argument.
inline long long replay(const Rules&, Prices, const std::vector<Trade>&) { throw std::logic_error("TODO"); }

}  // namespace stock
