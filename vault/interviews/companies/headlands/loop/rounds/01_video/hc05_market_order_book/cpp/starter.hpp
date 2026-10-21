// hc05 · Market order book — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <climits>
#include <cstddef>
#include <cstdint>
#include <list>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
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

// ------------------------------------------------------------------------------------------------ Parts 1 and 2
/// Single-instrument limit order book.
/// Hint: both sides as std::map<price, level>; a level = a std::list of orders in arrival order + a cached total; an id index
/// that stores ITERATORS to the order and its level makes cancel O(1) -- legal because std::map / std::list never invalidate
/// iterators on insert/erase of other elements.  Those iterators would dangle in a copy: the book is move-only.
class OrderBook {
public:
    OrderBook() = default;
    OrderBook(const OrderBook&) = delete;
    OrderBook& operator=(const OrderBook&) = delete;
    OrderBook(OrderBook&&) noexcept = default;
    OrderBook& operator=(OrderBook&&) noexcept = default;

    // ---- Part 1: maintenance, no matching ----
    /// Rest an order at the BACK of its price level without matching (the book may end up crossed).  Checks in this order:
    /// id <= 0, price <= 0, qty <= 0, duplicate id (any side): std::invalid_argument with the INVALID_* / DUPLICATE_ID text.
    /// Level total overflow: std::overflow_error and the book is unchanged (use __builtin_add_overflow; signed overflow is UB).
    void add(long long, Side, long long, long long) { throw std::logic_error("TODO"); }
    /// true if it existed.  The id can be reused afterwards.
    bool cancel(long long) { throw std::logic_error("TODO"); }
    /// Only the quantity changes.  Smaller: keeps its place.  Equal: nothing.  Larger: goes to the back of its level (hint:
    /// std::list::splice keeps the node and its iterators valid).  new_qty <= 0 -> std::invalid_argument even for an unknown
    /// id; unknown id -> false; level total overflow -> std::overflow_error (book unchanged).
    bool modify(long long, long long) { throw std::logic_error("TODO"); }
    std::optional<long long> best_bid() const { throw std::logic_error("TODO"); }
    std::optional<long long> best_ask() const { throw std::logic_error("TODO"); }
    /// The best n levels: bids from the highest price down, asks from the lowest up.  n < 0 -> std::invalid_argument.
    std::vector<Level> depth(Side, int) const { throw std::logic_error("TODO"); }
    std::optional<Order> find(long long) const { throw std::logic_error("TODO"); }
    /// Order ids at one price level, front of the queue first (empty if there is no such level).
    std::vector<long long> queue(Side, long long) const { throw std::logic_error("TODO"); }
    std::size_t size() const noexcept { return 0; }

    // ---- Part 2: matching ----
    /// Execute one command and return the events it caused, in order.  Limit: eat the opposite side while it crosses (best
    /// price first, oldest first within a price, trade price = the resting order's price), rest the remainder (Rested).
    /// Market: same without a limit; an unfilled remainder is dropped (Cancelled).  Cancel -> Cancelled{id, remaining}.
    /// Modify -> Modified{id, old, new}, never matches.  Any failure = ONE Rejected event and the book is untouched, checks in
    /// the order id, price, quantity, book state (DUPLICATE_ID for a new order whose id is live, UNKNOWN_ID for cancel/modify
    /// of an id that is not live).  OVERFLOW_REASON: the order would overflow its OWN side's level total (rejected BEFORE
    /// matching, so nothing trades); an increasing Modify that would overflow its level.
    /// Hint: std::visit with an overloaded{...} visitor; the compiler then checks that every alternative is handled.
    std::vector<Event> execute(const Command&) { throw std::logic_error("TODO"); }
    std::vector<Event> execute_all(const std::vector<Command>&) { throw std::logic_error("TODO"); }
};

/// LIMIT id BUY|SELL price qty | MARKET id BUY|SELL qty | CANCEL id | MODIFY id new_qty  (case-insensitive, any whitespace).
/// Malformed -> std::invalid_argument.  Hint: std::from_chars, and check that the WHOLE token was consumed ("1.5" parses
/// as 1 and stops); it also reports out-of-range values.
inline Command parse(std::string_view) { throw std::logic_error("TODO"); }

/// "TRADE taker=3 maker=1 side=SELL px=100 qty=3" | "REST id=1 side=BUY px=7 qty=2" | "CANCEL id=1 remaining=2" |
/// "MODIFY id=1 old=5 new=3" | "REJECT id=1 reason=duplicate id".  Side prints as BUY / SELL.
inline std::string render(const Event&) { throw std::logic_error("TODO"); }

/// Run a script on a fresh book (blank lines and lines starting with '#' are skipped); returns the rendered events.
/// A malformed line -> std::invalid_argument whose message starts with "line N" (N counts from 1, skipped lines included).
inline std::vector<std::string> replay(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 3
struct Summary {
    std::vector<Trade> trades;
    long long filled_qty;
    long long notional;  // sum of price * qty over all trades
    std::vector<Level> bids, asks;
    friend bool operator==(const Summary&, const Summary&) = default;
};

/// rows[i] = {side, price, qty}, side 0 = BUY, 1 = SELL; order id = i + 1; processed as limit orders in order (reuse
/// OrderBook).  Validate every row FIRST: std::invalid_argument whose message starts with "row i" (i from 0) for a row whose
/// size is not 3, side not 0/1, price <= 0 or qty <= 0.  notional / filled_qty overflow -> std::overflow_error.  bids / asks
/// = the final book, all levels, best first.
inline Summary run_batch(const std::vector<std::vector<long long>>&) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 4
/// Hot-path order book.  Prices are integer ticks 1..max_ticks-1, at most `capacity` live orders; everything is allocated in
/// the constructor (max_ticks < 2 or capacity outside 1..2^22 -> std::invalid_argument) and limit()/cancel() NEVER allocate.
///  * limit(): same matching as OrderBook (price-time priority, trade at the maker's price), each trade reported through
///    sink(taker_id, maker_id, price, qty); returns the rested quantity (0 = fully filled), REJECTED for id <= 0, a live id,
///    a price outside 1..max_ticks-1, qty outside 1..MAX_QTY (check the 64-bit values BEFORE narrowing to int), FULL when the
///    pool is exhausted (then nothing is matched and the book is unchanged).
///  * cancel(): O(1).  best_bid()/best_ask(): NONE when empty.  qty_at(): level total, 0 outside the price band.
/// Hint: array of order records linked by int indices + free list, one record per tick and side, a bitmap of non-empty levels
/// with std::countr_zero / std::countl_zero to find the next best price, open addressing for id -> record with
/// backward-shift deletion.
class TickBook {
public:
    static constexpr long long NONE = -1;
    static constexpr long long REJECTED = -1;
    static constexpr long long FULL = -2;
    static constexpr long long MAX_QTY = 1LL << 40;

    TickBook(int, int) { throw std::logic_error("TODO"); }

    template <class Sink>
    long long limit(long long, Side, long long, long long, Sink&&) { throw std::logic_error("TODO"); }
    bool cancel(long long) { throw std::logic_error("TODO"); }
    long long best_bid() const noexcept { return NONE; }
    long long best_ask() const noexcept { return NONE; }
    int live_orders() const noexcept { return 0; }
    long long qty_at(Side, long long) const noexcept { return 0; }
};

}  // namespace book
