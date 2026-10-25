// hc14 · Trade log -> VWAP and statistics — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: value types, validation, checked arithmetic.  To write: everything marked TODO (and the members of RollingVwap).
// Hints: no regex, no std::stod / std::from_chars (floating point, locale, leniency) — scan the characters yourself and
// accept only '0'..'9'.  `char` may be signed: index tables with static_cast<unsigned char>.
#pragma once

#include <algorithm>
#include <array>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <deque>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <vector>

namespace tradelog {

inline constexpr long long SCALE = 10'000;  // price 187.25 is stored as 1'872'500
inline constexpr int MAX_SYMBOL_LEN = 10;

// ============================================================================================ checked arithmetic
inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow");
    return r;
}
inline long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error("multiplication overflow");
    return r;
}

// ============================================================================================ value types
inline bool valid_symbol(std::string_view s) noexcept {
    if (s.empty() || s.size() > static_cast<std::size_t>(MAX_SYMBOL_LEN)) return false;
    for (char c : s) {
        const bool ok = (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '.';
        if (!ok) return false;
    }
    return true;
}

/// One valid trade.  The constructor validates, so an existing Trade never has a bad field or an overflowing notional.
struct Trade {
    long long ts_ms;
    std::string symbol;
    long long price;
    long long qty;

    Trade(long long ts_ms_, std::string symbol_, long long price_, long long qty_)
        : ts_ms(ts_ms_), symbol(std::move(symbol_)), price(price_), qty(qty_) {
        if (ts_ms < 0) throw std::invalid_argument("negative timestamp");
        if (!valid_symbol(symbol)) throw std::invalid_argument("invalid symbol");
        if (price <= 0) throw std::invalid_argument("non-positive price");
        if (qty <= 0) throw std::invalid_argument("non-positive quantity");
        mul_exact(price, qty);
    }
    /// price * qty in units of 0.0001.
    long long notional() const noexcept { return price * qty; }
    friend bool operator==(const Trade&, const Trade&) = default;
};

struct SymbolStats {
    std::string symbol;
    long long count;
    long long volume;
    long long notional;
    long long vwap;  // notional / volume rounded half up
    long long min_price;
    long long max_price;
    friend bool operator==(const SymbolStats&, const SymbolStats&) = default;
};

/// symbols sorted by symbol; accepted + malformed = number of non-empty lines.
struct Report {
    std::vector<SymbolStats> symbols;
    long long accepted;
    long long malformed;
    friend bool operator==(const Report&, const Report&) = default;
};

// ============================================================================================ Part 1
/// Price text -> fixed point; nullopt if it breaks the grammar in problem.md.  Never throws.
inline std::optional<long long> parse_price(std::string_view) { throw std::logic_error("TODO"); }

/// One line -> Trade; nullopt if any rule in problem.md is broken.  Never throws.
inline std::optional<Trade> parse_line(std::string_view) { throw std::logic_error("TODO"); }

/// notional / volume rounded half up, never overflowing.  volume <= 0 or notional < 0 -> std::invalid_argument.
inline long long vwap(long long /*notional*/, long long /*volume*/) { throw std::logic_error("TODO"); }

/// Parse and aggregate.  Empty lines are skipped without being counted; a sum that overflows -> std::overflow_error.
inline Report analyze(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

/// 1872500 -> "187.2500".  Negative -> std::invalid_argument.
inline std::string format_price(long long) { throw std::logic_error("TODO"); }

/// One line per symbol ("AAPL count=3 volume=12 notional=... vwap=... min=... max=..."), then "accepted=N malformed=M".
inline std::vector<std::string> render(const Report&) { throw std::logic_error("TODO"); }

// ============================================================================================ Part 2 + 3
struct SymbolNotional {
    std::string symbol;
    long long notional;
    friend bool operator==(const SymbolNotional&, const SymbolNotional&) = default;
};

/// Sliding-window VWAP.  A trade is live at time `now` iff now - ts_ms < window_ms.
/// Hint: one FIFO of all live trades (oldest at the front) + one accumulator per symbol; each trade enters and leaves once.
class RollingVwap {
public:
    /// window_ms >= 1, else std::invalid_argument.
    explicit RollingVwap(long long /*window_ms*/) { throw std::logic_error("TODO"); }

    /// Advance the clock to t.ts_ms (earlier than the clock -> std::invalid_argument), expire old trades, then add.
    /// A symbol sum that overflows -> std::overflow_error and the trade is not added (clock advanced, expired trades gone).
    void on_trade(const Trade&) { throw std::logic_error("TODO"); }

    /// VWAP of `symbol` over the window ending at now_ms; nullopt if it has no live trade.  Advances the clock
    /// (now_ms earlier than the clock -> std::invalid_argument).
    std::optional<long long> vwap(std::string_view /*symbol*/, long long /*now_ms*/) { throw std::logic_error("TODO"); }

    /// Volume / notional of the symbol in the window as of the last clock advance; 0 if none.  Does not advance the clock.
    long long volume(std::string_view) const { throw std::logic_error("TODO"); }
    long long notional(std::string_view) const { throw std::logic_error("TODO"); }
    std::size_t live_trades() const noexcept { return 0; }
    std::size_t live_symbols() const noexcept { return 0; }
    /// Current clock; 0 before any event.
    long long now() const noexcept { return 0; }

    /// Part 3: the k symbols with the largest notional in the window ending at now_ms; notional descending, ties by symbol
    /// ascending.  k < 0 -> std::invalid_argument (checked before the clock).  k = 0 -> empty.  Advances the clock.
    std::vector<SymbolNotional> top_k(int /*k*/, long long /*now_ms*/) { throw std::logic_error("TODO"); }

private:
    // your members here
};

// ============================================================================================ Part 4
/// One pass over the raw bytes of a log file; the same result as analyze() on the '\n'-separated lines of `data`
/// (same grammar, same bad lines, same overflow exception).  1e6 lines < 1 s and no per-line allocation.
/// Hint: pack the symbol (<= 10 characters x 6 bits) into one uint64_t and use it as an open-addressing key.
inline Report analyze_fast(std::string_view) { throw std::logic_error("TODO"); }

}  // namespace tradelog
