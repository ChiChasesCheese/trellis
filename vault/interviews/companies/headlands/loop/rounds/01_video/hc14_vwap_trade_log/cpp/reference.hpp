// hc14 · Trade log -> VWAP and statistics — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 parse_line / analyze (fixed-point long long, hand-written scanners, no regex / from_chars / stod),
//        2 RollingVwap (deque + per-symbol accumulators), 3 RollingVwap::top_k (bounded partial_sort),
//        4 analyze_fast (one pass over the bytes, symbols packed into 6-bit codes, open-addressing table).
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
namespace detail {
inline bool is_digit(char c) noexcept { return c >= '0' && c <= '9'; }

/// [s) holds only '0'..'9', 1..max_digits of them -> value, else -1.
inline long long digits(std::string_view s, int max_digits) noexcept {
    if (s.empty() || s.size() > static_cast<std::size_t>(max_digits)) return -1;
    long long v = 0;
    for (char c : s) {
        if (!is_digit(c)) return -1;
        v = v * 10 + (c - '0');
    }
    return v;
}
}  // namespace detail

inline std::optional<long long> parse_price(std::string_view s) {
    std::size_t i = 0;
    long long whole = 0, frac = 0;
    int int_digits = 0, frac_digits = 0;
    while (i < s.size() && detail::is_digit(s[i])) {
        whole = whole * 10 + (s[i++] - '0');
        if (++int_digits > 9) return std::nullopt;
    }
    if (int_digits == 0) return std::nullopt;
    if (i < s.size() && s[i] == '.') {
        ++i;
        while (i < s.size() && detail::is_digit(s[i])) {
            frac = frac * 10 + (s[i++] - '0');
            if (++frac_digits > 4) return std::nullopt;
        }
        if (frac_digits == 0) return std::nullopt;
    }
    if (i != s.size()) return std::nullopt;
    for (int d = frac_digits; d < 4; ++d) frac *= 10;
    const long long price = whole * SCALE + frac;
    if (price <= 0) return std::nullopt;
    return price;
}

inline std::optional<Trade> parse_line(std::string_view line) {
    const auto c1 = line.find(',');
    if (c1 == std::string_view::npos) return std::nullopt;
    const auto c2 = line.find(',', c1 + 1);
    if (c2 == std::string_view::npos) return std::nullopt;
    const auto c3 = line.find(',', c2 + 1);
    if (c3 == std::string_view::npos || line.find(',', c3 + 1) != std::string_view::npos) return std::nullopt;
    const long long ts = detail::digits(line.substr(0, c1), 18);
    const long long qty = detail::digits(line.substr(c3 + 1), 12);
    if (ts < 0 || qty <= 0) return std::nullopt;
    const auto symbol = line.substr(c1 + 1, c2 - c1 - 1);
    if (!valid_symbol(symbol)) return std::nullopt;
    const auto price = parse_price(line.substr(c2 + 1, c3 - c2 - 1));
    if (!price) return std::nullopt;
    long long unused;
    if (__builtin_mul_overflow(*price, qty, &unused)) return std::nullopt;  // price * qty does not fit: malformed line
    return Trade(ts, std::string(symbol), *price, qty);
}

/// notional / volume rounded half up, without ever overflowing.  volume <= 0 or notional < 0 -> invalid_argument.
inline long long vwap(long long notional, long long volume) {
    if (volume <= 0 || notional < 0) throw std::invalid_argument("volume must be positive, notional non-negative");
    const long long q = notional / volume, r = notional % volume;
    return r >= volume - r ? q + 1 : q;
}

/// Parses and aggregates.  Empty lines are skipped without being counted; a sum that overflows throws std::overflow_error.
inline Report analyze(const std::vector<std::string>& lines) {
    struct Acc {
        long long count = 0, volume = 0, notional = 0, min = 0, max = 0;
    };
    std::map<std::string, Acc> by;
    long long accepted = 0, malformed = 0;
    for (const auto& line : lines) {
        if (line.empty()) continue;
        const auto t = parse_line(line);
        if (!t) {
            ++malformed;
            continue;
        }
        auto [it, fresh] = by.try_emplace(t->symbol);
        Acc& a = it->second;
        a.volume = add_exact(a.volume, t->qty);
        a.notional = add_exact(a.notional, t->notional());
        a.min = fresh ? t->price : std::min(a.min, t->price);
        a.max = fresh ? t->price : std::max(a.max, t->price);
        ++a.count;
        ++accepted;
    }
    Report r{{}, accepted, malformed};
    r.symbols.reserve(by.size());
    for (const auto& [sym, a] : by) r.symbols.push_back({sym, a.count, a.volume, a.notional, vwap(a.notional, a.volume), a.min, a.max});
    return r;
}

/// 1872500 -> "187.2500".  Negative -> invalid_argument.
inline std::string format_price(long long units) {
    if (units < 0) throw std::invalid_argument("negative");
    std::string frac = std::to_string(units % SCALE);
    return std::to_string(units / SCALE) + "." + std::string(4 - frac.size(), '0') + frac;
}

inline std::vector<std::string> render(const Report& r) {
    std::vector<std::string> out;
    for (const auto& s : r.symbols) {
        out.push_back(s.symbol + " count=" + std::to_string(s.count) + " volume=" + std::to_string(s.volume) +
                      " notional=" + format_price(s.notional) + " vwap=" + format_price(s.vwap) +
                      " min=" + format_price(s.min_price) + " max=" + format_price(s.max_price));
    }
    out.push_back("accepted=" + std::to_string(r.accepted) + " malformed=" + std::to_string(r.malformed));
    return out;
}

// ============================================================================================ Part 2 + 3
struct SymbolNotional {
    std::string symbol;
    long long notional;
    friend bool operator==(const SymbolNotional&, const SymbolNotional&) = default;
};

/// Sliding-window VWAP.  A trade is live at time `now` iff now - ts_ms < window_ms.
class RollingVwap {
public:
    /// window_ms >= 1, else invalid_argument.
    explicit RollingVwap(long long window_ms) : window_(window_ms) {
        if (window_ms < 1) throw std::invalid_argument("window must be >= 1");
    }

    /// Advance the clock to t.ts_ms (earlier than the clock -> invalid_argument), then add.  An overflowing sum
    /// -> std::overflow_error and the trade is not added (the clock has advanced, expired trades are gone).
    void on_trade(const Trade& t) {
        advance(t.ts_ms);
        auto it = by_symbol_.find(std::string_view(t.symbol));
        const long long volume = add_exact(it == by_symbol_.end() ? 0 : it->second.volume, t.qty);
        const long long notional = add_exact(it == by_symbol_.end() ? 0 : it->second.notional, t.notional());
        if (it == by_symbol_.end()) it = by_symbol_.emplace(t.symbol, Acc{}).first;
        ++it->second.count;
        it->second.volume = volume;
        it->second.notional = notional;
        live_.push_back(t);
    }

    /// VWAP of `symbol` over the window ending at now_ms; nullopt if it has no live trade.  Advances the clock.
    std::optional<long long> vwap(std::string_view symbol, long long now_ms) {
        advance(now_ms);
        const auto it = by_symbol_.find(symbol);
        if (it == by_symbol_.end()) return std::nullopt;
        return tradelog::vwap(it->second.notional, it->second.volume);
    }

    long long volume(std::string_view symbol) const {
        const auto it = by_symbol_.find(symbol);
        return it == by_symbol_.end() ? 0 : it->second.volume;
    }
    long long notional(std::string_view symbol) const {
        const auto it = by_symbol_.find(symbol);
        return it == by_symbol_.end() ? 0 : it->second.notional;
    }
    std::size_t live_trades() const noexcept { return live_.size(); }
    std::size_t live_symbols() const noexcept { return by_symbol_.size(); }
    long long now() const noexcept { return now_; }

    /// Part 3: the k symbols with the largest notional in the window ending at now_ms; notional descending, ties by symbol
    /// ascending.  k < 0 -> invalid_argument (checked before the clock).  Advances the clock.
    std::vector<SymbolNotional> top_k(int k, long long now_ms) {
        if (k < 0) throw std::invalid_argument("k must be >= 0");
        advance(now_ms);
        std::vector<SymbolNotional> all;
        all.reserve(by_symbol_.size());
        for (const auto& [sym, a] : by_symbol_) all.push_back({sym, a.notional});
        const auto best_first = [](const SymbolNotional& x, const SymbolNotional& y) {
            return x.notional != y.notional ? x.notional > y.notional : x.symbol < y.symbol;
        };
        const auto keep = std::min<std::size_t>(static_cast<std::size_t>(k), all.size());
        std::partial_sort(all.begin(), all.begin() + static_cast<std::ptrdiff_t>(keep), all.end(), best_first);
        all.resize(keep);
        return all;
    }

private:
    struct Acc {
        long long count = 0, volume = 0, notional = 0;
    };
    struct SvHash {  // transparent: lookups by string_view do not build a std::string
        using is_transparent = void;
        std::size_t operator()(std::string_view s) const noexcept { return std::hash<std::string_view>{}(s); }
    };

    void advance(long long t) {
        if (t < now_) throw std::invalid_argument("time went backwards");
        now_ = t;
        while (!live_.empty() && now_ - live_.front().ts_ms >= window_) {
            const Trade& old = live_.front();
            const auto it = by_symbol_.find(std::string_view(old.symbol));
            it->second.volume -= old.qty;
            it->second.notional -= old.notional();
            if (--it->second.count == 0) by_symbol_.erase(it);
            live_.pop_front();
        }
    }

    long long window_;
    long long now_ = 0;
    std::deque<Trade> live_;
    std::unordered_map<std::string, Acc, SvHash, std::equal_to<>> by_symbol_;
};

// ============================================================================================ Part 4
namespace detail {
inline constexpr std::uint64_t GOLDEN = 0x9E3779B97F4A7C15ull;

inline const std::array<std::uint8_t, 256>& symbol_codes() {
    static const auto table = [] {
        std::array<std::uint8_t, 256> t{};
        for (int c = 'A'; c <= 'Z'; ++c) t[static_cast<std::size_t>(c)] = static_cast<std::uint8_t>(1 + c - 'A');
        for (int c = '0'; c <= '9'; ++c) t[static_cast<std::size_t>(c)] = static_cast<std::uint8_t>(27 + c - '0');
        t[static_cast<std::size_t>('.')] = 37;
        return t;
    }();
    return table;
}

inline std::string decode_symbol(std::uint64_t key) {
    std::string s;
    while (key != 0) {
        const auto code = static_cast<int>(key & 63);
        s.push_back(code <= 26 ? static_cast<char>('A' + code - 1) : code <= 36 ? static_cast<char>('0' + code - 27) : '.');
        key >>= 6;
    }
    std::reverse(s.begin(), s.end());
    return s;
}

/// Open-addressing table: symbol key (60 bits, never 0) -> accumulators in parallel arrays.
class SymbolTable {
public:
    SymbolTable() { resize(1024); }

    void add(std::uint64_t key, long long price, long long qty, long long value) {
        std::size_t i = slot(key, keys_.size());
        while (keys_[i] != 0 && keys_[i] != key) i = (i + 1) & (keys_.size() - 1);
        if (keys_[i] == 0) {
            keys_[i] = key;
            count_[i] = 1;
            volume_[i] = qty;
            notional_[i] = value;
            min_[i] = max_[i] = price;
            if (++used_ * 2 > keys_.size()) grow();
            return;
        }
        volume_[i] = add_exact(volume_[i], qty);
        notional_[i] = add_exact(notional_[i], value);
        ++count_[i];
        min_[i] = std::min(min_[i], price);
        max_[i] = std::max(max_[i], price);
    }

    std::vector<SymbolStats> stats() const {
        std::vector<SymbolStats> out;
        out.reserve(used_);
        for (std::size_t i = 0; i < keys_.size(); ++i) {
            if (keys_[i] == 0) continue;
            out.push_back({decode_symbol(keys_[i]), count_[i], volume_[i], notional_[i], vwap(notional_[i], volume_[i]), min_[i], max_[i]});
        }
        std::sort(out.begin(), out.end(), [](const SymbolStats& a, const SymbolStats& b) { return a.symbol < b.symbol; });
        return out;
    }

private:
    static std::size_t slot(std::uint64_t key, std::size_t cap) noexcept {
        return static_cast<std::size_t>((key * GOLDEN) >> (64 - std::countr_zero(cap)));
    }
    void grow() {
        SymbolTable bigger;
        bigger.resize(keys_.size() * 2);
        for (std::size_t j = 0; j < keys_.size(); ++j) {
            if (keys_[j] == 0) continue;
            std::size_t i = slot(keys_[j], bigger.keys_.size());
            while (bigger.keys_[i] != 0) i = (i + 1) & (bigger.keys_.size() - 1);
            bigger.keys_[i] = keys_[j];
            bigger.count_[i] = count_[j];
            bigger.volume_[i] = volume_[j];
            bigger.notional_[i] = notional_[j];
            bigger.min_[i] = min_[j];
            bigger.max_[i] = max_[j];
        }
        bigger.used_ = used_;
        *this = std::move(bigger);
    }
    void resize(std::size_t cap) {
        keys_.assign(cap, 0);
        count_.assign(cap, 0);
        volume_.assign(cap, 0);
        notional_.assign(cap, 0);
        min_.assign(cap, 0);
        max_.assign(cap, 0);
    }

    std::vector<std::uint64_t> keys_;
    std::vector<long long> count_, volume_, notional_, min_, max_;
    std::size_t used_ = 0;
};
}  // namespace detail

/// One pass over the raw bytes; same result as analyze() on the '\n'-separated lines of `data`.
inline Report analyze_fast(std::string_view data) {
    const auto& codes = detail::symbol_codes();
    detail::SymbolTable table;
    long long accepted = 0, malformed = 0;
    const auto* base = reinterpret_cast<const unsigned char*>(data.data());
    const std::size_t n = data.size();
    std::size_t pos = 0;
    const auto digit = [](unsigned char b) { return b >= '0' && b <= '9'; };

    const auto line = [&](std::size_t p, std::size_t e) -> bool {
        int d = 0;
        while (p < e && digit(base[p])) {  // ts: 1..18 digits
            ++p;
            if (++d > 18) return false;
        }
        if (d == 0 || p >= e || base[p] != ',') return false;
        ++p;
        std::uint64_t key = 0;
        int len = 0;
        while (p < e && base[p] != ',') {  // symbol: 1..10 valid characters, packed
            const unsigned code = codes[base[p]];
            if (code == 0 || ++len > MAX_SYMBOL_LEN) return false;
            key = (key << 6) | code;
            ++p;
        }
        if (len == 0 || p >= e) return false;
        ++p;
        long long whole = 0, frac = 0;
        int wd = 0, fd = 0;
        while (p < e && digit(base[p])) {
            whole = whole * 10 + (base[p++] - '0');
            if (++wd > 9) return false;
        }
        if (wd == 0) return false;
        if (p < e && base[p] == '.') {
            ++p;
            while (p < e && digit(base[p])) {
                frac = frac * 10 + (base[p++] - '0');
                if (++fd > 4) return false;
            }
            if (fd == 0) return false;
        }
        if (p >= e || base[p] != ',') return false;
        ++p;
        for (int i = fd; i < 4; ++i) frac *= 10;
        const long long price = whole * SCALE + frac;
        if (price <= 0) return false;
        long long qty = 0;
        int qd = 0;
        while (p < e && digit(base[p])) {
            qty = qty * 10 + (base[p++] - '0');
            if (++qd > 12) return false;
        }
        if (qd == 0 || p != e || qty == 0) return false;
        long long value;
        if (__builtin_mul_overflow(price, qty, &value)) return false;
        table.add(key, price, qty, value);
        return true;
    };

    while (pos < n) {
        std::size_t end = pos;
        while (end < n && base[end] != '\n') ++end;
        if (end > pos) {
            if (line(pos, end)) ++accepted;
            else ++malformed;
        }
        pos = end + 1;
    }
    return Report{table.stats(), accepted, malformed};
}

}  // namespace tradelog
