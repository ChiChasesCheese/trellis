// hc05 · Market order book — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 OrderBook maintenance (std::map ladders, std::list FIFO, stored iterators for O(1) cancel), 2 execute()
//        (price-time priority matching, std::variant commands/events), 3 run_batch (hc14), 4 TickBook (integer ticks,
//        arrays instead of trees, preallocated pool, intrusive list, bitmap, zero allocation on the hot path).
#pragma once

#include <algorithm>
#include <array>
#include <bit>
#include <cctype>
#include <charconv>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <format>
#include <iterator>
#include <list>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace book {

// ---- types ----
enum class Side { Buy, Sell };
constexpr Side opposite(Side s) noexcept { return s == Side::Buy ? Side::Sell : Side::Buy; }
constexpr std::string_view name(Side s) noexcept { return s == Side::Buy ? "BUY" : "SELL"; }

/// One price level of the ladder: price in ticks, total resting quantity, number of orders.
struct Level {
    long long price;
    long long total_qty;
    int order_count;
    friend bool operator==(const Level&, const Level&) = default;
};
/// A resting order as seen from outside (qty = what is left).
struct Order {
    long long id;
    Side side;
    long long price;
    long long qty;
    friend bool operator==(const Order&, const Order&) = default;
};

inline constexpr std::string_view INVALID_ID = "invalid id";
inline constexpr std::string_view INVALID_PRICE = "invalid price";
inline constexpr std::string_view INVALID_QTY = "invalid quantity";
inline constexpr std::string_view DUPLICATE_ID = "duplicate id";
inline constexpr std::string_view UNKNOWN_ID = "unknown id";
inline constexpr std::string_view OVERFLOW_REASON = "overflow";

// ---- commands and events (Part 2) ----
struct Limit {
    long long id;
    Side side;
    long long price;
    long long qty;
    friend bool operator==(const Limit&, const Limit&) = default;
};
struct Market {
    long long id;
    Side side;
    long long qty;
    friend bool operator==(const Market&, const Market&) = default;
};
struct Cancel {
    long long id;
    friend bool operator==(const Cancel&, const Cancel&) = default;
};
struct Modify {
    long long id;
    long long new_qty;
    friend bool operator==(const Modify&, const Modify&) = default;
};
using Command = std::variant<Limit, Market, Cancel, Modify>;

/// price = the price of the passive (resting) order.
struct Trade {
    long long taker_id;
    long long maker_id;
    Side taker_side;
    long long price;
    long long qty;
    friend bool operator==(const Trade&, const Trade&) = default;
};
struct Rested {
    long long id;
    Side side;
    long long price;
    long long qty;
    friend bool operator==(const Rested&, const Rested&) = default;
};
struct Cancelled {
    long long id;
    long long remaining;
    friend bool operator==(const Cancelled&, const Cancelled&) = default;
};
struct Modified {
    long long id;
    long long old_qty;
    long long new_qty;
    friend bool operator==(const Modified&, const Modified&) = default;
};
struct Rejected {
    long long id;
    std::string_view reason;  // always one of the constants above: static storage, no allocation
    friend bool operator==(const Rejected&, const Rejected&) = default;
};
using Event = std::variant<Trade, Rested, Cancelled, Modified, Rejected>;

namespace detail {
template <class... Ts>
struct overloaded : Ts... {
    using Ts::operator()...;
};
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

/// a + b into `out`; false on overflow (never relies on signed overflow, which is undefined behaviour).
inline bool add_ok(long long a, long long b, long long& out) { return !__builtin_add_overflow(a, b, &out); }
}  // namespace detail

// ---- OrderBook ----
/// Single-instrument limit order book.  Both sides are std::map<price, PriceLevel> in ascending price order (best bid =
/// the last element, best ask = the first); a level is a std::list of orders in arrival order plus a cached total.  The id
/// index stores iterators straight to the order's list node and its level, so cancel needs no search.
/// std::map and std::list never invalidate iterators on insert/erase of OTHER elements -- that is what makes the stored
/// iterators legal.  They would dangle in a copy, so the book is move-only.
class OrderBook {
public:
    OrderBook() = default;
    OrderBook(const OrderBook&) = delete;
    OrderBook& operator=(const OrderBook&) = delete;
    OrderBook(OrderBook&&) noexcept = default;  // node-based containers keep their nodes (and iterators) when moved
    OrderBook& operator=(OrderBook&&) noexcept = default;

    // ---- Part 1: maintenance, no matching ----
    /// Rest an order without matching (the book may end up crossed).  Invalid arguments / duplicate id: std::invalid_argument
    /// (checked in the order id, price, quantity, duplicate); level total overflow: std::overflow_error, book unchanged.
    void add(long long id, Side side, long long price, long long qty) {
        if (id <= 0) throw std::invalid_argument(std::string(INVALID_ID));
        if (price <= 0) throw std::invalid_argument(std::string(INVALID_PRICE));
        if (qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        if (by_id_.contains(id)) throw std::invalid_argument(std::string(DUPLICATE_ID));
        if (level_would_overflow(side, price, qty)) throw std::overflow_error("level total overflows");
        rest(id, side, price, qty);
    }

    bool cancel(long long id) {
        const auto it = by_id_.find(id);
        if (it == by_id_.end()) return false;
        unlink(it->second);
        by_id_.erase(it);
        return true;
    }

    /// Only the quantity changes.  Smaller: keeps its place in the queue.  Equal: nothing.  Larger: goes to the back of the
    /// queue (time priority is lost).  new_qty <= 0 -> std::invalid_argument even for an unknown id; unknown id -> false;
    /// level total overflow -> std::overflow_error (book unchanged).
    bool modify(long long id, long long new_qty) {
        if (new_qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        switch (try_modify(id, new_qty)) {
            case ModifyResult::Ok: return true;
            case ModifyResult::Unknown: return false;
            case ModifyResult::Overflow: break;
        }
        throw std::overflow_error("level total overflows");
    }

    std::optional<long long> best_bid() const {
        if (bids_.empty()) return std::nullopt;
        return bids_.rbegin()->first;
    }
    std::optional<long long> best_ask() const {
        if (asks_.empty()) return std::nullopt;
        return asks_.begin()->first;
    }

    /// The best n levels: bids from the highest price down, asks from the lowest up.  n < 0 -> std::invalid_argument.
    std::vector<Level> depth(Side side, int n) const {
        if (n < 0) throw std::invalid_argument("n < 0");
        std::vector<Level> out;
        const auto push = [&](const auto& entry) {
            out.push_back({entry.first, entry.second.total, static_cast<int>(entry.second.fifo.size())});
        };
        if (side == Side::Buy) {
            for (auto it = bids_.rbegin(); it != bids_.rend() && std::cmp_less(out.size(), n); ++it) push(*it);
        } else {
            for (auto it = asks_.begin(); it != asks_.end() && std::cmp_less(out.size(), n); ++it) push(*it);
        }
        return out;
    }

    std::optional<Order> find(long long id) const {
        const auto it = by_id_.find(id);
        if (it == by_id_.end()) return std::nullopt;
        const Locator& loc = it->second;
        return Order{id, loc.side, loc.level->first, loc.node->qty};
    }

    /// Order ids at one price level, front of the queue first (empty if there is no such level).
    std::vector<long long> queue(Side side, long long price) const {
        const Ladder& lad = ladder(side);
        const auto it = lad.find(price);
        std::vector<long long> ids;
        if (it != lad.end())
            for (const Node& n : it->second.fifo) ids.push_back(n.id);
        return ids;
    }

    std::size_t size() const noexcept { return by_id_.size(); }

    // ---- Part 2: matching ----
    /// Execute one command and return the events it caused, in order.  Failure = one Rejected event and the book is
    /// untouched.  Checks in the order id, price, quantity, book state.
    std::vector<Event> execute(const Command& cmd) {
        if (const auto bad = validate(cmd)) return {Rejected{id_of(cmd), *bad}};
        return std::visit(
            detail::overloaded{
                [&](const Limit& c) -> std::vector<Event> {
                    if (level_would_overflow(c.side, c.price, c.qty)) return {Rejected{c.id, OVERFLOW_REASON}};  // BEFORE matching: all or nothing
                    std::vector<Event> events;
                    const long long left = sweep(c.id, c.side, c.price, c.qty, events);
                    if (left > 0) {
                        rest(c.id, c.side, c.price, left);
                        events.push_back(Rested{c.id, c.side, c.price, left});
                    }
                    return events;
                },
                [&](const Market& c) -> std::vector<Event> {
                    std::vector<Event> events;
                    const long long left = sweep(c.id, c.side, c.side == Side::Buy ? LLONG_MAX : 0, c.qty, events);
                    if (left > 0) events.push_back(Cancelled{c.id, left});  // immediate-or-cancel: the rest is void
                    return events;
                },
                [&](const Cancel& c) -> std::vector<Event> {
                    const auto it = by_id_.find(c.id);
                    const long long left = it->second.node->qty;
                    unlink(it->second);
                    by_id_.erase(it);
                    return {Cancelled{c.id, left}};
                },
                [&](const Modify& c) -> std::vector<Event> {
                    const long long old = by_id_.find(c.id)->second.node->qty;
                    if (try_modify(c.id, c.new_qty) == ModifyResult::Overflow) return {Rejected{c.id, OVERFLOW_REASON}};
                    return {Modified{c.id, old, c.new_qty}};
                },
            },
            cmd);
    }

    std::vector<Event> execute_all(const std::vector<Command>& cmds) {
        std::vector<Event> out;
        for (const Command& c : cmds) {
            std::vector<Event> evs = execute(c);
            out.insert(out.end(), evs.begin(), evs.end());
        }
        return out;
    }

    // ---- OrderBook internals ----
private:
    struct Node {
        long long id;
        long long qty;
    };
    using Fifo = std::list<Node>;
    struct PriceLevel {
        Fifo fifo;
        long long total = 0;  // cached sum of the quantities in fifo
    };
    using Ladder = std::map<long long, PriceLevel>;
    struct Locator {
        Side side;
        Ladder::iterator level;
        Fifo::iterator node;
    };
    enum class ModifyResult { Ok, Unknown, Overflow };

    Ladder& ladder(Side s) { return s == Side::Buy ? bids_ : asks_; }
    const Ladder& ladder(Side s) const { return s == Side::Buy ? bids_ : asks_; }

    static long long id_of(const Command& c) {
        return std::visit([](const auto& x) { return x.id; }, c);
    }

    bool level_would_overflow(Side side, long long price, long long qty) const {
        const Ladder& lad = ladder(side);
        const auto it = lad.find(price);
        long long ignored;
        return it != lad.end() && !detail::add_ok(it->second.total, qty, ignored);
    }

    /// Precondition: the id is free and the level total cannot overflow.
    void rest(long long id, Side side, long long price, long long qty) {
        const auto [level, created] = ladder(side).try_emplace(price);
        (void)created;
        PriceLevel& lvl = level->second;
        lvl.fifo.push_back({id, qty});
        lvl.total += qty;
        by_id_.emplace(id, Locator{side, level, std::prev(lvl.fifo.end())});
    }

    /// Remove the order from its queue and level (the caller erases the id index entry).
    void unlink(const Locator& loc) {
        PriceLevel& lvl = loc.level->second;
        lvl.total -= loc.node->qty;
        lvl.fifo.erase(loc.node);
        if (lvl.fifo.empty()) ladder(loc.side).erase(loc.level);
    }

    ModifyResult try_modify(long long id, long long new_qty) {
        const auto it = by_id_.find(id);
        if (it == by_id_.end()) return ModifyResult::Unknown;
        Locator& loc = it->second;
        PriceLevel& lvl = loc.level->second;
        const long long old = loc.node->qty;
        if (new_qty > old) {
            long long total;
            if (!detail::add_ok(lvl.total, new_qty - old, total)) return ModifyResult::Overflow;  // nothing modified yet
            lvl.total = total;
            loc.node->qty = new_qty;
            lvl.fifo.splice(lvl.fifo.end(), lvl.fifo, loc.node);  // to the back; the node (and our iterator) stay valid
        } else {
            lvl.total -= old - new_qty;
            loc.node->qty = new_qty;
        }
        return ModifyResult::Ok;
    }

    // ---- validate ----
    std::optional<std::string_view> validate(const Command& cmd) const {
        using R = std::optional<std::string_view>;
        return std::visit(
            detail::overloaded{
                [&](const Limit& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    if (c.price <= 0) return INVALID_PRICE;
                    if (c.qty <= 0) return INVALID_QTY;
                    return by_id_.contains(c.id) ? R(DUPLICATE_ID) : std::nullopt;
                },
                [&](const Market& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    if (c.qty <= 0) return INVALID_QTY;
                    return by_id_.contains(c.id) ? R(DUPLICATE_ID) : std::nullopt;
                },
                [&](const Cancel& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    return by_id_.contains(c.id) ? std::nullopt : R(UNKNOWN_ID);
                },
                [&](const Modify& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    if (c.new_qty <= 0) return INVALID_QTY;
                    return by_id_.contains(c.id) ? std::nullopt : R(UNKNOWN_ID);
                },
            },
            cmd);
    }

    // ---- sweep ----
    /// Eat the opposite side while it crosses `limit`; returns the unfilled quantity.  The trade price is the maker's price.
    long long sweep(long long taker_id, Side side, long long limit, long long qty, std::vector<Event>& out) {
        Ladder& opp = ladder(opposite(side));
        long long left = qty;
        while (left > 0 && !opp.empty()) {
            const auto top = side == Side::Buy ? opp.begin() : std::prev(opp.end());  // best opposite level
            const long long px = top->first;
            if (side == Side::Buy ? px > limit : px < limit) break;
            PriceLevel& lvl = top->second;
            Node& maker = lvl.fifo.front();
            const long long fill = std::min(left, maker.qty);
            out.push_back(Trade{taker_id, maker.id, side, px, fill});
            left -= fill;
            maker.qty -= fill;
            lvl.total -= fill;
            if (maker.qty == 0) {
                const long long maker_id = maker.id;
                lvl.fifo.pop_front();
                by_id_.erase(maker_id);
                if (lvl.fifo.empty()) opp.erase(top);
            }
        }
        return left;
    }

    Ladder bids_, asks_;
    std::unordered_map<long long, Locator> by_id_;
};

// ---- text interface ----
namespace detail {
inline bool iequals(std::string_view a, std::string_view b) {
    return std::ranges::equal(a, b, [](unsigned char x, unsigned char y) { return std::toupper(x) == std::toupper(y); });
}
inline bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }
inline std::vector<std::string_view> split_words(std::string_view s) {
    std::vector<std::string_view> words;
    std::size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && is_space(s[i])) ++i;
        const std::size_t start = i;
        while (i < s.size() && !is_space(s[i])) ++i;
        if (i > start) words.push_back(s.substr(start, i - start));
    }
    return words;
}
/// The whole token must be one base-10 integer that fits in long long: from_chars stops at the first bad character
/// ("1.5" -> 1) and reports range errors, so check both.  (std::stoll would accept "12abc" and a leading '+'/space.)
inline long long parse_ll(std::string_view tok) {
    long long v = 0;
    const auto [end, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), v);
    if (ec != std::errc{} || end != tok.data() + tok.size()) throw std::invalid_argument("bad number: " + std::string(tok));
    return v;
}
inline Side parse_side(std::string_view tok) {
    if (iequals(tok, "BUY")) return Side::Buy;
    if (iequals(tok, "SELL")) return Side::Sell;
    throw std::invalid_argument("bad side: " + std::string(tok));
}
inline void need_args(const std::vector<std::string_view>& w, std::size_t n) {
    if (w.size() != n) throw std::invalid_argument(std::string(w[0]) + " expects " + std::to_string(n - 1) + " arguments");
}
}  // namespace detail

/// LIMIT id BUY|SELL price qty | MARKET id BUY|SELL qty | CANCEL id | MODIFY id new_qty  (case-insensitive, any whitespace).
inline Command parse(std::string_view line) {
    const auto w = detail::split_words(line);
    if (w.empty()) throw std::invalid_argument("empty command");
    using detail::iequals;
    using detail::parse_ll;
    if (iequals(w[0], "LIMIT")) {
        detail::need_args(w, 5);
        return Limit{parse_ll(w[1]), detail::parse_side(w[2]), parse_ll(w[3]), parse_ll(w[4])};
    }
    if (iequals(w[0], "MARKET")) {
        detail::need_args(w, 4);
        return Market{parse_ll(w[1]), detail::parse_side(w[2]), parse_ll(w[3])};
    }
    if (iequals(w[0], "CANCEL")) {
        detail::need_args(w, 2);
        return Cancel{parse_ll(w[1])};
    }
    if (iequals(w[0], "MODIFY")) {
        detail::need_args(w, 3);
        return Modify{parse_ll(w[1]), parse_ll(w[2])};
    }
    throw std::invalid_argument("unknown command: " + std::string(w[0]));
}

// ---- render and replay ----
/// One line per event.  std::visit with a visitor that handles every alternative: a new Event type would not compile.
inline std::string render(const Event& e) {
    return std::visit(
        detail::overloaded{
            [](const Trade& t) { return std::format("TRADE taker={} maker={} side={} px={} qty={}", t.taker_id, t.maker_id, name(t.taker_side), t.price, t.qty); },
            [](const Rested& r) { return std::format("REST id={} side={} px={} qty={}", r.id, name(r.side), r.price, r.qty); },
            [](const Cancelled& c) { return std::format("CANCEL id={} remaining={}", c.id, c.remaining); },
            [](const Modified& m) { return std::format("MODIFY id={} old={} new={}", m.id, m.old_qty, m.new_qty); },
            [](const Rejected& r) { return std::format("REJECT id={} reason={}", r.id, r.reason); },
        },
        e);
}

/// Run a script (blank lines and '#' lines are skipped).  A malformed line -> std::invalid_argument("line N: ..."), N from 1.
inline std::vector<std::string> replay(const std::vector<std::string>& lines) {
    OrderBook b;
    std::vector<std::string> out;
    for (std::size_t i = 0; i < lines.size(); ++i) {
        const auto w = detail::split_words(lines[i]);
        if (w.empty() || w[0].front() == '#') continue;
        Command cmd;
        try {
            cmd = parse(lines[i]);
        } catch (const std::invalid_argument& e) {
            throw std::invalid_argument("line " + std::to_string(i + 1) + ": " + e.what());
        }
        for (const Event& ev : b.execute(cmd)) out.push_back(render(ev));
    }
    return out;
}

// ---- Part 3: batch matching (hc14) ----
struct Summary {
    std::vector<Trade> trades;
    long long filled_qty;
    long long notional;  // sum of price * qty over all trades
    std::vector<Level> bids, asks;
    friend bool operator==(const Summary&, const Summary&) = default;
};

/// rows[i] = {side, price, qty}, side 0 = BUY, 1 = SELL; order id = i + 1; processed as limit orders in order.
/// Every row is validated first (std::invalid_argument "row i: ..."); notional overflow -> std::overflow_error.
inline Summary run_batch(const std::vector<std::vector<long long>>& rows) {
    for (std::size_t i = 0; i < rows.size(); ++i) {
        const auto& r = rows[i];
        const std::string at = "row " + std::to_string(i) + ": ";
        if (r.size() != 3) throw std::invalid_argument(at + "expected [side, price, quantity]");
        if (r[0] != 0 && r[0] != 1) throw std::invalid_argument(at + "bad side");
        if (r[1] <= 0) throw std::invalid_argument(at + std::string(INVALID_PRICE));
        if (r[2] <= 0) throw std::invalid_argument(at + std::string(INVALID_QTY));
    }
    OrderBook b;
    std::vector<Trade> trades;
    for (std::size_t i = 0; i < rows.size(); ++i) {
        const Side side = rows[i][0] == 0 ? Side::Buy : Side::Sell;
        for (const Event& e : b.execute(Limit{static_cast<long long>(i) + 1, side, rows[i][1], rows[i][2]})) {
            if (const auto* t = std::get_if<Trade>(&e)) trades.push_back(*t);
            else if (const auto* rej = std::get_if<Rejected>(&e)) throw std::overflow_error("row " + std::to_string(i) + ": " + std::string(rej->reason));
        }
    }
    long long filled = 0, notional = 0;
    for (const Trade& t : trades) {
        long long value;
        if (__builtin_mul_overflow(t.price, t.qty, &value) || __builtin_add_overflow(notional, value, &notional) ||
            __builtin_add_overflow(filled, t.qty, &filled))
            throw std::overflow_error("notional overflows long long");
    }
    return {std::move(trades), filled, notional, b.depth(Side::Buy, INT_MAX), b.depth(Side::Sell, INT_MAX)};
}

// ---- Part 4: TickBook ----
/// Hot-path order book: prices are integer ticks 1..max_ticks-1, so a price level is an array index, not a tree node.
/// Everything is allocated in the constructor: a pool of order records linked by 32-bit indices (intrusive doubly linked
/// list per level, free list for spare records), one {head, tail, qty} record per tick and side, a bitmap of non-empty
/// levels to find the next best price, and an open-addressing id -> record table with backward-shift deletion.
/// limit()/cancel() never allocate.  Trades go to a callable: no event objects.
class TickBook {
public:
    static constexpr long long NONE = -1;
    static constexpr long long REJECTED = -1;
    static constexpr long long FULL = -2;
    /// 2^22 live orders * 2^40 = 2^62 < 2^63: a level total can never overflow.
    static constexpr long long MAX_QTY = 1LL << 40;

    /// max_ticks >= 2; 1 <= capacity <= 2^22 (maximum number of live orders), else std::invalid_argument.
    TickBook(int max_ticks, int capacity)
        : max_ticks_(check_ticks(max_ticks)), capacity_(check_capacity(capacity)), pool_(static_cast<std::size_t>(capacity)),
          ids_(std::bit_ceil(std::max<std::size_t>(16, static_cast<std::size_t>(capacity) * 2))), bid_best_(0), ask_best_(max_ticks) {
        id_mask_ = ids_.size() - 1;
        for (int i = 0; i < capacity_; ++i) pool_[static_cast<std::size_t>(i)].next = i + 1 < capacity_ ? i + 1 : -1;
        free_head_ = 0;
        for (auto& s : side_) {
            s.levels.assign(static_cast<std::size_t>(max_ticks_), LevelRec{});
            s.bits.assign((static_cast<std::size_t>(max_ticks_) + 63) / 64, 0);
        }
    }

    /// Match against the opposite side (price-time priority, trade price = maker's price), call
    /// `sink(taker_id, maker_id, price, qty)` per trade, rest the remainder.  Returns the rested quantity (0 = fully filled),
    /// REJECTED for an invalid argument (id <= 0, id already live, price outside 1..max_ticks-1, qty outside 1..MAX_QTY), or
    /// FULL when the pool has no free record (nothing is matched in that case).
    template <class Sink>
    long long limit(long long id, Side side, long long price, long long qty, Sink&& sink) {
        // range-check the 64-bit values BEFORE narrowing to int: (1<<32) + 5 would otherwise become price 5
        if (id <= 0 || price <= 0 || price >= max_ticks_ || qty <= 0 || qty > MAX_QTY) return REJECTED;
        if (find_id(id) >= 0) return REJECTED;
        if (free_head_ < 0) return FULL;
        const int p = static_cast<int>(price);
        const bool buy = side == Side::Buy;
        const int me = buy ? 0 : 1, other = 1 - me;
        long long left = qty;
        while (left > 0 && (buy ? ask_best_ <= p : bid_best_ >= p)) {
            const int bp = buy ? ask_best_ : bid_best_;
            const int slot = side_[other].levels[static_cast<std::size_t>(bp)].head;
            Rec& maker = pool_[static_cast<std::size_t>(slot)];
            const long long fill = std::min(left, maker.qty);
            sink(id, maker.id, static_cast<long long>(bp), fill);
            left -= fill;
            maker.qty -= fill;
            side_[other].levels[static_cast<std::size_t>(bp)].qty -= fill;
            if (maker.qty == 0) unlink(slot);
        }
        if (left > 0) rest(id, me, p, left);
        return left;
    }

    /// O(1): the id table gives the record, the record knows its neighbours.
    bool cancel(long long id) {
        const int slot = find_id(id);
        if (slot < 0) return false;
        unlink(slot);
        return true;
    }

    long long best_bid() const noexcept { return bid_best_ == 0 ? NONE : bid_best_; }
    long long best_ask() const noexcept { return ask_best_ == max_ticks_ ? NONE : ask_best_; }
    int live_orders() const noexcept { return live_; }

    /// Total quantity at a price; 0 for a price outside the band (no out-of-bounds read, no truncation).
    long long qty_at(Side side, long long price) const noexcept {
        if (price <= 0 || price >= max_ticks_) return 0;
        return side_[side == Side::Buy ? 0 : 1].levels[static_cast<std::size_t>(price)].qty;
    }

    // ---- TickBook internals ----
private:
    struct Rec {  // 32 bytes: id, qty, price, prev, next, side
        long long id = 0;
        long long qty = 0;
        std::int32_t price = 0;
        std::int32_t prev = -1;
        std::int32_t next = -1;  // next in the level's queue; in a free record: next free record
        std::uint8_t side = 0;
    };
    struct LevelRec {
        std::int32_t head = -1, tail = -1;
        long long qty = 0;
    };
    struct SideData {
        std::vector<LevelRec> levels;
        std::vector<std::uint64_t> bits;  // bit p set = level p is not empty
    };
    struct IdSlot {
        long long key = 0;  // 0 = empty (ids are > 0)
        std::int32_t slot = 0;
    };

    static int check_ticks(int t) {
        if (t < 2) throw std::invalid_argument("max_ticks < 2");
        return t;
    }
    static int check_capacity(int c) {
        if (c < 1 || c > (1 << 22)) throw std::invalid_argument("capacity out of range");
        return c;
    }

    void rest(long long id, int s, int p, long long qty) {
        const int slot = free_head_;
        Rec& r = pool_[static_cast<std::size_t>(slot)];
        free_head_ = r.next;
        ++live_;
        r.id = id;
        r.qty = qty;
        r.price = p;
        r.side = static_cast<std::uint8_t>(s);
        LevelRec& lv = side_[s].levels[static_cast<std::size_t>(p)];
        r.prev = lv.tail;
        r.next = -1;
        if (lv.tail >= 0) {
            pool_[static_cast<std::size_t>(lv.tail)].next = slot;
        } else {  // the level was empty
            lv.head = slot;
            side_[s].bits[static_cast<std::size_t>(p) >> 6] |= 1ull << (p & 63);
            if (s == 0) bid_best_ = std::max(bid_best_, p);
            else ask_best_ = std::min(ask_best_, p);
        }
        lv.tail = slot;
        lv.qty += qty;
        put_id(id, slot);
    }

    /// Detach the record from its queue, give it back to the pool, forget its id; if the level became empty, find the next best price.
    void unlink(int slot) {
        Rec& r = pool_[static_cast<std::size_t>(slot)];
        const int s = r.side, p = r.price;
        LevelRec& lv = side_[s].levels[static_cast<std::size_t>(p)];
        if (r.prev >= 0) pool_[static_cast<std::size_t>(r.prev)].next = r.next; else lv.head = r.next;
        if (r.next >= 0) pool_[static_cast<std::size_t>(r.next)].prev = r.prev; else lv.tail = r.prev;
        lv.qty -= r.qty;
        if (lv.head < 0) {
            side_[s].bits[static_cast<std::size_t>(p) >> 6] &= ~(1ull << (p & 63));
            if (s == 0 && p == bid_best_) {
                const int n = p > 0 ? at_or_below(side_[0].bits, p - 1) : -1;
                bid_best_ = n < 0 ? 0 : n;
            } else if (s == 1 && p == ask_best_) {
                const int n = p + 1 < max_ticks_ ? at_or_above(side_[1].bits, p + 1) : -1;
                ask_best_ = n < 0 ? max_ticks_ : n;
            }
        }
        erase_id(r.id);
        r.next = free_head_;
        free_head_ = slot;
        --live_;
    }

    // first non-empty level at or above / below `from`: mask the word, then countr_zero / countl_zero (one instruction each)
    static int at_or_above(const std::vector<std::uint64_t>& b, int from) {
        std::size_t w = static_cast<std::size_t>(from) >> 6;
        std::uint64_t word = b[w] & (~0ull << (from & 63));
        for (;;) {
            if (word != 0) return static_cast<int>(w * 64) + std::countr_zero(word);
            if (++w >= b.size()) return -1;
            word = b[w];
        }
    }
    static int at_or_below(const std::vector<std::uint64_t>& b, int from) {
        std::size_t w = static_cast<std::size_t>(from) >> 6;
        std::uint64_t word = b[w] & (~0ull >> (63 - (from & 63)));
        for (;;) {
            if (word != 0) return static_cast<int>(w * 64) + 63 - std::countl_zero(word);
            if (w == 0) return -1;
            word = b[--w];
        }
    }

    // id table: ids are often consecutive, so multiply by an odd constant and fold the high half into the low half
    std::size_t id_hash(long long id) const noexcept {
        const std::uint64_t h = static_cast<std::uint64_t>(id) * 0x9E3779B97F4A7C15ull;
        return static_cast<std::size_t>(h ^ (h >> 32)) & id_mask_;
    }
    int find_id(long long id) const noexcept {
        for (std::size_t i = id_hash(id); ids_[i].key != 0; i = (i + 1) & id_mask_)
            if (ids_[i].key == id) return ids_[i].slot;
        return -1;
    }
    void put_id(long long id, int slot) noexcept {
        std::size_t i = id_hash(id);
        while (ids_[i].key != 0) i = (i + 1) & id_mask_;
        ids_[i] = {id, slot};
    }
    /// Backward-shift deletion: no tombstones.  Emptying the slot would cut the probe chain of keys pushed past it, so slide
    /// each later key of the cluster back into the hole when its home slot does not lie cyclically in (hole, its position].
    void erase_id(long long id) noexcept {
        std::size_t i = id_hash(id);
        while (ids_[i].key != id) i = (i + 1) & id_mask_;
        std::size_t j = i;
        for (;;) {
            j = (j + 1) & id_mask_;
            if (ids_[j].key == 0) break;
            const std::size_t home = id_hash(ids_[j].key);
            if (((j - home) & id_mask_) >= ((j - i) & id_mask_)) {
                ids_[i] = ids_[j];
                i = j;
            }
        }
        ids_[i].key = 0;
    }

    int max_ticks_;
    int capacity_;
    std::vector<Rec> pool_;
    std::vector<IdSlot> ids_;
    std::size_t id_mask_ = 0;
    std::array<SideData, 2> side_;
    int free_head_ = -1;
    int live_ = 0;
    int bid_best_;  // 0 = no bids
    int ask_best_;  // max_ticks_ = no asks
};

}  // namespace book
