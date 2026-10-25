// ld02 · Trading OOD (order state machine · positions and PnL · pre-trade risk · event-sourced desk) — C++20 reference.
// Statement: ../problem.md.  Parts: 1 OrderManager  2 PositionBook (+ Position)  3 RiskEngine  4 TradingDesk.
#pragma once

#include <algorithm>
#include <array>
#include <cctype>
#include <cstdlib>
#include <deque>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <variant>
#include <vector>

namespace trading {

// ---------------------------------------------------------------------------------------------- errors
/// Java: IllegalTransitionException extends IllegalStateException.  The event is not legal in the order's current state
/// (a Fill after FILLED, an overfill, a fill price beyond the limit).  The order is left exactly as it was.
struct IllegalTransitionException : std::logic_error {
    using std::logic_error::logic_error;
};
// Other Java exceptions, same meaning here:
//   IllegalArgumentException  -> std::invalid_argument      NoSuchElementException -> std::out_of_range
//   ArithmeticException       -> std::overflow_error        (NullPointerException cannot happen: values, not nullable references)

/// Java Math.multiplyExact / addExact / subtractExact: signed overflow is undefined behaviour in C++, so check first.
inline long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error("long overflow");
    return r;
}
inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("long overflow");
    return r;
}
inline long long sub_exact(long long a, long long b) {
    long long r;
    if (__builtin_sub_overflow(a, b, &r)) throw std::overflow_error("long overflow");
    return r;
}

/// The std::visit helper: Overloaded{[](const A&){...}, [](const B&){...}}.  A variant alternative without a matching
/// lambda is a COMPILE error: this is the C++ version of Java's exhaustive `switch` over a sealed interface.
template <class... Ts> struct Overloaded : Ts... { using Ts::operator()...; };

// ---------------------------------------------------------------------------------------------- Side, OrderStatus
enum class Side { Buy, Sell };
/// Buy = +1, Sell = -1: one piece of arithmetic for longs and shorts instead of two if/else branches.
constexpr int sign(Side s) { return s == Side::Buy ? +1 : -1; }
constexpr Side opposite(Side s) { return s == Side::Buy ? Side::Sell : Side::Buy; }

/// PENDING --Ack--> WORKING --Fill--> PARTIALLY_FILLED --Fill--> FILLED;  WORKING --Fill(all)--> FILLED;
/// WORKING / PARTIALLY_FILLED --Cancel--> CANCELED;  PENDING --Reject--> REJECTED.  Everything else is illegal.
enum class OrderStatus { Pending, Working, PartiallyFilled, Filled, Canceled, Rejected };
constexpr bool is_terminal(OrderStatus s) { return s == OrderStatus::Filled || s == OrderStatus::Canceled || s == OrderStatus::Rejected; }
/// The order exists at the exchange (it may trade).  PENDING counts: sent, acknowledgement not back yet.
constexpr bool is_open(OrderStatus s) { return !is_terminal(s); }

// ---------------------------------------------------------------------------------------------- Order
/// A limit order.  Prices are integer ticks, quantities integer shares: integers have no rounding error, so PnL is checkable
/// to the last digit.  The constructor keeps impossible orders out of the type: nobody downstream re-checks qty > 0.
/// (Java record = C++ class with private data + validating constructor + defaulted operator==.)
class Order {
public:
    Order(long long id, std::string symbol, Side side, long long qty, long long px)
        : id_(id), symbol_(std::move(symbol)), side_(side), qty_(qty), px_(px) {
        if (id <= 0) throw std::invalid_argument("id must be > 0: " + std::to_string(id));
        if (std::all_of(symbol_.begin(), symbol_.end(), [](unsigned char c) { return std::isspace(c) != 0; })) throw std::invalid_argument("symbol is blank");
        if (qty <= 0) throw std::invalid_argument("qty must be > 0: " + std::to_string(qty));
        if (px <= 0) throw std::invalid_argument("px must be > 0: " + std::to_string(px));
    }
    long long id() const { return id_; }
    const std::string& symbol() const { return symbol_; }
    Side side() const { return side_; }
    long long qty() const { return qty_; }
    long long px() const { return px_; }
    friend bool operator==(const Order&, const Order&) = default;

private:
    long long id_;
    std::string symbol_;
    Side side_;
    long long qty_, px_;
};

/// Read-only snapshot of an order (OrderManager::get).  Plain data with no invariant of its own: a struct with public fields
/// is the C++ record.  reject_reason is empty unless the order was rejected.
struct OrderView {
    Order order;
    OrderStatus status;
    long long cum_qty;
    long long cum_notional;
    std::optional<std::string> reject_reason;

    /// What can still trade: 0 for CANCELED / REJECTED (the unfilled rest is no longer a risk), 0 for FILLED because cum_qty == qty.
    long long leaves_qty() const { return is_terminal(status) && status != OrderStatus::Filled ? 0 : order.qty() - cum_qty; }
    friend bool operator==(const OrderView&, const OrderView&) = default;
};

// ---------------------------------------------------------------------------------------------- events
/// Execution reports from the exchange / gateway, and the inputs of TradingDesk.  Java: sealed interfaces + records.
/// C++: one small class per event, and std::variant as the closed sum type.
class Ack {
public:
    explicit Ack(long long order_id) : order_id_(order_id) {}
    long long order_id() const { return order_id_; }
    friend bool operator==(const Ack&, const Ack&) = default;
private:
    long long order_id_;
};
/// One trade.  exec_id is globally unique: reports can be delivered twice (at-least-once), the id is how we de-duplicate.
class Fill {
public:
    Fill(long long order_id, long long exec_id, long long qty, long long px) : order_id_(order_id), exec_id_(exec_id), qty_(qty), px_(px) {
        if (qty <= 0) throw std::invalid_argument("fill qty must be > 0: " + std::to_string(qty));
        if (px <= 0) throw std::invalid_argument("fill px must be > 0: " + std::to_string(px));
    }
    long long order_id() const { return order_id_; }
    long long exec_id() const { return exec_id_; }
    long long qty() const { return qty_; }
    long long px() const { return px_; }
    friend bool operator==(const Fill&, const Fill&) = default;
private:
    long long order_id_, exec_id_, qty_, px_;
};
/// The exchange CONFIRMS a cancel (this is not a cancel request).
class Cancel {
public:
    explicit Cancel(long long order_id) : order_id_(order_id) {}
    long long order_id() const { return order_id_; }
    friend bool operator==(const Cancel&, const Cancel&) = default;
private:
    long long order_id_;
};
/// Rejected by the exchange (or by our own risk check).
class Reject {
public:
    Reject(long long order_id, std::string reason) : order_id_(order_id), reason_(std::move(reason)) {}
    long long order_id() const { return order_id_; }
    const std::string& reason() const { return reason_; }
    friend bool operator==(const Reject&, const Reject&) = default;
private:
    long long order_id_;
    std::string reason_;
};
using ExecEvent = std::variant<Ack, Fill, Cancel, Reject>;

class Submit {
public:
    explicit Submit(Order order) : order_(std::move(order)) {}
    const Order& order() const { return order_; }
    friend bool operator==(const Submit&, const Submit&) = default;
private:
    Order order_;
};
class SetReferencePrice {
public:
    SetReferencePrice(std::string symbol, long long px) : symbol_(std::move(symbol)), px_(px) {
        if (px <= 0) throw std::invalid_argument("px must be > 0: " + std::to_string(px));
    }
    const std::string& symbol() const { return symbol_; }
    long long px() const { return px_; }
    friend bool operator==(const SetReferencePrice&, const SetReferencePrice&) = default;
private:
    std::string symbol_;
    long long px_;
};
/// Kill switch: afterwards every Submit is rejected by the risk check until Resume.
struct Halt {
    friend bool operator==(const Halt&, const Halt&) = default;
};
struct Resume {
    friend bool operator==(const Resume&, const Resume&) = default;
};

/// ALL inputs of the desk - what the journal stores and replay feeds again.  Risk verdicts, positions and PnL are not inputs:
/// they are outputs, recomputed on replay.  (Java: ExecEvent extends DeskEvent.  A variant cannot extend another variant, so the
/// four execution events are alternatives of both; to_desk_event converts.)
using DeskEvent = std::variant<Submit, SetReferencePrice, Halt, Resume, Ack, Fill, Cancel, Reject>;

inline DeskEvent to_desk_event(const ExecEvent& e) {
    return std::visit([](const auto& x) -> DeskEvent { return x; }, e);
}
inline long long order_id_of(const ExecEvent& e) {
    return std::visit([](const auto& x) { return x.order_id(); }, e);
}

// ---------------------------------------------------------------------------------------------- risk types
/// All limits strictly positive (a limit of 0 can only be a configuration mistake).
///   max_order_qty / max_order_notional (px * qty) per order;  max_position: worst-case |net position| per symbol including open orders;
///   max_open_orders: across the account;  price_band_bps: |px - ref| / ref may not exceed this many basis points (1 bp = 0.01 %).
class RiskLimits {
public:
    RiskLimits(long long max_order_qty, long long max_order_notional, long long max_position, int max_open_orders, long long price_band_bps)
        : max_order_qty_(max_order_qty), max_order_notional_(max_order_notional), max_position_(max_position),
          max_open_orders_(max_open_orders), price_band_bps_(price_band_bps) {
        if (max_order_qty <= 0 || max_order_notional <= 0 || max_position <= 0 || max_open_orders <= 0 || price_band_bps <= 0)
            throw std::invalid_argument("all risk limits must be > 0");
    }
    long long max_order_qty() const { return max_order_qty_; }
    long long max_order_notional() const { return max_order_notional_; }
    long long max_position() const { return max_position_; }
    int max_open_orders() const { return max_open_orders_; }
    long long price_band_bps() const { return price_band_bps_; }
    friend bool operator==(const RiskLimits&, const RiskLimits&) = default;

private:
    long long max_order_qty_, max_order_notional_, max_position_;
    int max_open_orders_;
    long long price_band_bps_;
};

/// Declaration order = check order: when several rules are broken, the FIRST is reported (deterministic: replay must give the same reason).
enum class RiskReason { Halted, NoReferencePrice, QtyLimit, NotionalLimit, PriceBand, OpenOrdersLimit, PositionLimit };
/// The upper-case name used as OrderView::reject_reason ("QTY_LIMIT"), the same strings as the Java enum names.
constexpr std::string_view to_string(RiskReason r) {
    switch (r) {
        case RiskReason::Halted: return "HALTED";
        case RiskReason::NoReferencePrice: return "NO_REFERENCE_PRICE";
        case RiskReason::QtyLimit: return "QTY_LIMIT";
        case RiskReason::NotionalLimit: return "NOTIONAL_LIMIT";
        case RiskReason::PriceBand: return "PRICE_BAND";
        case RiskReason::OpenOrdersLimit: return "OPEN_ORDERS_LIMIT";
        case RiskReason::PositionLimit: return "POSITION_LIMIT";
    }
    return "?";
}

/// Accepted, or rejected with a reason.  Java: sealed interface + two records; here the sum type is just optional<reason>.
class RiskResult {
public:
    static RiskResult accepted() { return RiskResult(std::nullopt); }
    static RiskResult rejected(RiskReason reason) { return RiskResult(reason); }
    bool is_accepted() const { return !reason_.has_value(); }
    /// The reason for a rejection; empty when accepted.
    std::optional<RiskReason> reason() const { return reason_; }
    friend bool operator==(const RiskResult&, const RiskResult&) = default;

private:
    explicit RiskResult(std::optional<RiskReason> r) : reason_(r) {}
    std::optional<RiskReason> reason_;
};

// ---------------------------------------------------------------------------------------------- Position
/// Position of one symbol.  net_qty: long positive, short negative.  open_cost: sum of qty * px over the open lots (always >= 0).
/// realized_pnl: FIFO (the oldest lot is closed first).
struct Position {
    std::string symbol;
    long long net_qty = 0;
    long long open_cost = 0;
    long long realized_pnl = 0;

    static Position flat(std::string symbol) { return Position{std::move(symbol), 0, 0, 0}; }
    /// Unrealized PnL at mark_px.  Long: net_qty * mark - open_cost.  Short: open_cost - |net_qty| * mark.  Flat: 0.  Overflow -> std::overflow_error.
    long long unrealized_pnl(long long mark_px) const;
    friend bool operator==(const Position&, const Position&) = default;
};

}  // namespace trading

namespace trading {

inline long long Position::unrealized_pnl(long long mark_px) const {
    if (net_qty > 0) return sub_exact(mul_exact(net_qty, mark_px), open_cost);
    if (net_qty < 0) return sub_exact(open_cost, mul_exact(-net_qty, mark_px));  // -net_qty: net_qty is never LLONG_MIN (it is a sum of lots)
    return 0;
}

// ============================================================================================ Part 1
/// Order state machine.  Single-threaded (TradingDesk is the single writer).  Two rules:
///  1. validate first, mutate after: no throwing path changes any state (replay depends on it);
///  2. the aggregates risk needs (open quantity per symbol and side, number of open orders) are maintained incrementally, O(1) to read.
class OrderManager {
public:
    /// Register a new order as PENDING.  Duplicate id -> std::invalid_argument.  The aggregates are summed with checked
    /// arithmetic: a quantity that would overflow them is refused before anything changes (std::overflow_error).
    void submit(const Order& order) {
        if (orders_.contains(order.id())) throw std::invalid_argument("duplicate order id " + std::to_string(order.id()));
        auto& leaves = open_leaves_[order.symbol()];  // a zero entry is harmless if the next line throws
        const long long updated = add_exact(leaves[slot(order.side())], order.qty());
        orders_.emplace(order.id(), State(order));
        leaves[slot(order.side())] = updated;
        ++open_count_;
    }

    /// true = applied; false = duplicate Fill (exec id already seen), no effect.
    /// std::out_of_range unknown order; IllegalTransitionException illegal transition / overfill / price beyond limit (state unchanged).
    bool apply(const ExecEvent& event) {
        const auto it = orders_.find(order_id_of(event));
        if (it == orders_.end()) throw std::out_of_range("unknown order " + std::to_string(order_id_of(event)));
        State& s = it->second;
        return std::visit(
            Overloaded{
                [&](const Ack&) {
                    require(s.status == OrderStatus::Pending, s, "Ack");
                    s.status = OrderStatus::Working;
                    return true;
                },
                [&](const Fill& f) {
                    if (seen_exec_ids_.contains(f.exec_id())) return false;  // duplicate: BEFORE the state check (an old report replayed after FILLED is only a duplicate)
                    require(s.status == OrderStatus::Working || s.status == OrderStatus::PartiallyFilled, s, "Fill");
                    if (f.qty() > s.leaves()) throw IllegalTransitionException("overfill on order " + std::to_string(s.order.id()));
                    const bool outside = s.order.side() == Side::Buy ? f.px() > s.order.px() : f.px() < s.order.px();
                    if (outside) throw IllegalTransitionException("fill px " + std::to_string(f.px()) + " outside limit " + std::to_string(s.order.px()));
                    const long long new_cum_notional = add_exact(s.cum_notional, mul_exact(f.qty(), f.px()));  // may throw: nothing has changed yet
                    seen_exec_ids_.insert(f.exec_id());  // only after every check passed: an overfill's exec id stays unseen
                    s.cum_qty += f.qty();
                    s.cum_notional = new_cum_notional;
                    reduce_open(s, f.qty());
                    if (s.cum_qty == s.order.qty()) {
                        s.status = OrderStatus::Filled;
                        --open_count_;
                    } else {
                        s.status = OrderStatus::PartiallyFilled;
                    }
                    return true;
                },
                [&](const Cancel&) {
                    require(s.status == OrderStatus::Working || s.status == OrderStatus::PartiallyFilled, s, "Cancel");
                    reduce_open(s, s.leaves());
                    s.status = OrderStatus::Canceled;
                    --open_count_;
                    return true;
                },
                [&](const Reject& r) {
                    require(s.status == OrderStatus::Pending, s, "Reject");
                    reduce_open(s, s.leaves());
                    s.status = OrderStatus::Rejected;
                    s.reject_reason = r.reason();
                    --open_count_;
                    return true;
                },
            },
            event);
    }

    bool contains(long long order_id) const { return orders_.contains(order_id); }

    OrderView get(long long order_id) const {
        const auto it = orders_.find(order_id);
        if (it == orders_.end()) throw std::out_of_range("unknown order " + std::to_string(order_id));
        return it->second.view();
    }

    /// Every non-terminal order, ascending id.
    std::vector<OrderView> open() const {
        std::vector<OrderView> out;
        for (const auto& [id, s] : orders_)
            if (is_open(s.status)) out.push_back(s.view());
        std::sort(out.begin(), out.end(), [](const OrderView& a, const OrderView& b) { return a.order.id() < b.order.id(); });
        return out;
    }
    /// Every order, terminal ones included, ascending id.
    std::vector<OrderView> all() const {
        std::vector<OrderView> out;
        out.reserve(orders_.size());
        for (const auto& [id, s] : orders_) out.push_back(s.view());
        std::sort(out.begin(), out.end(), [](const OrderView& a, const OrderView& b) { return a.order.id() < b.order.id(); });
        return out;
    }

    int open_count() const { return open_count_; }

    /// Remaining quantity over all non-terminal orders of this symbol and side (PENDING included).
    long long open_leaves(const std::string& symbol, Side side) const {
        const auto it = open_leaves_.find(symbol);
        return it == open_leaves_.end() ? 0 : it->second[slot(side)];
    }

private:
    struct State {
        explicit State(Order o) : order(std::move(o)) {}
        Order order;
        OrderStatus status = OrderStatus::Pending;
        long long cum_qty = 0, cum_notional = 0;
        std::optional<std::string> reject_reason;
        long long leaves() const { return order.qty() - cum_qty; }
        OrderView view() const { return OrderView{order, status, cum_qty, cum_notional, reject_reason}; }
    };
    static constexpr std::size_t slot(Side side) { return side == Side::Buy ? 0 : 1; }
    static void require(bool ok, const State& s, const char* what) {
        if (!ok) throw IllegalTransitionException(std::string(what) + " not allowed in state " + std::to_string(static_cast<int>(s.status)) + " (order " + std::to_string(s.order.id()) + ")");
    }
    void reduce_open(const State& s, long long qty) { open_leaves_.at(s.order.symbol())[slot(s.order.side())] -= qty; }

    std::unordered_map<long long, State> orders_;
    std::unordered_set<long long> seen_exec_ids_;
    std::unordered_map<std::string, std::array<long long, 2>> open_leaves_;  // symbol -> {buy leaves, sell leaves}, non-terminal orders only
    int open_count_ = 0;
};

// ============================================================================================ Part 2
/// Positions and PnL, FIFO.  Per symbol a queue of open lots (qty, px), all on the same side.  A fill on the same side (or while flat)
/// appends a lot; an opposite fill closes lots from the front, realising dir * (fill px - lot px) * closed qty per slice; whatever
/// is left over FLIPS the position: it becomes the first lot of the new direction.  All integers; on overflow the position is left as it was
/// (the PnL is first computed read-only, then committed in one go).
class PositionBook {
public:
    /// qty <= 0 or px <= 0 -> std::invalid_argument.  Overflow -> std::overflow_error (position unchanged).
    void on_fill(const std::string& symbol, Side side, long long qty, long long px) {
        if (qty <= 0 || px <= 0) throw std::invalid_argument("qty and px must be > 0");
        Book& b = books_[symbol];
        const int s = sign(side);
        if (b.dir == 0 || b.dir == s) {
            b.lots.push_back(Lot{qty, px});
            b.dir = s;
            return;
        }
        // read-only pass first: an overflow here throws while nothing has been touched
        long long remaining = qty, pnl = 0;
        for (const Lot& lot : b.lots) {
            if (remaining == 0) break;
            const long long c = std::min(remaining, lot.qty);
            pnl = add_exact(pnl, mul_exact(b.dir * (px - lot.px), c));
            remaining -= c;
        }
        const long long new_realized = add_exact(b.realized, pnl);
        // commit (cannot throw from here on)
        remaining = qty;
        while (remaining > 0 && !b.lots.empty()) {
            Lot& lot = b.lots.front();
            const long long c = std::min(remaining, lot.qty);
            lot.qty -= c;
            remaining -= c;
            if (lot.qty == 0) b.lots.pop_front();
        }
        b.realized = new_realized;
        if (remaining > 0) {
            b.lots.push_back(Lot{remaining, px});
            b.dir = s;  // flip
        } else if (b.lots.empty()) {
            b.dir = 0;
        }
    }

    /// A symbol never seen is flat.
    Position get(const std::string& symbol) const {
        const auto it = books_.find(symbol);
        if (it == books_.end()) return Position::flat(symbol);
        const Book& b = it->second;
        long long qty = 0, cost = 0;
        for (const Lot& l : b.lots) {
            qty = add_exact(qty, l.qty);
            cost = add_exact(cost, mul_exact(l.qty, l.px));
        }
        return Position{symbol, b.dir * qty, cost, b.realized};
    }
    long long net_qty(const std::string& symbol) const {
        const auto it = books_.find(symbol);
        if (it == books_.end()) return 0;
        long long qty = 0;
        for (const Lot& l : it->second.lots) qty = add_exact(qty, l.qty);
        return it->second.dir * qty;
    }
    long long total_realized() const {
        long long t = 0;
        for (const auto& [symbol, b] : books_) t = add_exact(t, b.realized);
        return t;
    }
    /// Every symbol ever seen, in lexicographic order (std::map iterates sorted: no separate sort step).
    std::vector<std::string> symbols() const {
        std::vector<std::string> out;
        out.reserve(books_.size());
        for (const auto& [symbol, b] : books_) out.push_back(symbol);
        return out;
    }

private:
    struct Lot {
        long long qty, px;
    };
    struct Book {
        std::deque<Lot> lots;
        int dir = 0;  // +1 long, -1 short, 0 flat
        long long realized = 0;
    };
    std::map<std::string, Book> books_;
};

// ============================================================================================ Part 3
/// Pre-trade risk.  check() only reads; TradingDesk changes state.  The checks run in RiskReason declaration order, the first violation
/// is the answer.
class RiskEngine {
public:
    explicit RiskEngine(RiskLimits limits) : limits_(limits) {}

    void set_reference_price(const std::string& symbol, long long px) {
        if (px <= 0) throw std::invalid_argument("px must be > 0");
        ref_px_[symbol] = px;
    }
    void halt() { halted_ = true; }
    void resume() { halted_ = false; }
    bool halted() const { return halted_; }

    RiskResult check(const Order& o, const PositionBook& positions, const OrderManager& orders) const {
        if (halted_) return reject(RiskReason::Halted);
        const auto it = ref_px_.find(o.symbol());
        if (it == ref_px_.end()) return reject(RiskReason::NoReferencePrice);  // fail closed: no way to judge the price -> no
        const long long ref = it->second;
        if (o.qty() > limits_.max_order_qty()) return reject(RiskReason::QtyLimit);
        long long notional;
        if (__builtin_mul_overflow(o.px(), o.qty(), &notional) || notional > limits_.max_order_notional()) return reject(RiskReason::NotionalLimit);
        // |px - ref| / ref <= bps / 10000   <=>   |px - ref| * 10000 <= ref * bps   (cross-multiplied: no division, no rounding)
        long long dev, band;
        if (__builtin_mul_overflow(std::llabs(o.px() - ref), 10'000LL, &dev) || __builtin_mul_overflow(ref, limits_.price_band_bps(), &band))
            return reject(RiskReason::NotionalLimit);
        if (dev > band) return reject(RiskReason::PriceBand);
        if (orders.open_count() >= limits_.max_open_orders()) return reject(RiskReason::OpenOrdersLimit);
        // Worst-case net position: every open buy fills, or every open sell fills (this order included).  Signed overflow would be
        // undefined behaviour here, so any sum that does not fit counts as a breach.
        long long buy_leaves, sell_leaves, high, low;
        const bool overflow =
            __builtin_add_overflow(orders.open_leaves(o.symbol(), Side::Buy), o.side() == Side::Buy ? o.qty() : 0, &buy_leaves) ||
            __builtin_add_overflow(orders.open_leaves(o.symbol(), Side::Sell), o.side() == Side::Sell ? o.qty() : 0, &sell_leaves) ||
            __builtin_add_overflow(positions.net_qty(o.symbol()), buy_leaves, &high) ||
            __builtin_sub_overflow(positions.net_qty(o.symbol()), sell_leaves, &low);
        if (overflow || high > limits_.max_position() || low < -limits_.max_position()) return reject(RiskReason::PositionLimit);
        return RiskResult::accepted();
    }

private:
    static RiskResult reject(RiskReason r) { return RiskResult::rejected(r); }

    RiskLimits limits_;
    std::unordered_map<std::string, long long> ref_px_;
    bool halted_ = false;
};

// ============================================================================================ Part 4
/// Order state machine + positions + risk, assembled as ONE single-writer, event-sourced object.  All state changes come from
/// DeskEvents.  Every mutating method does three things in this order: append the input to the journal, call handle() to change the
/// in-memory state, return the result.  replay() does step 2 again on an empty desk and must arrive at an identical state, so
/// handle() must be deterministic: no clock, no randomness, no dependence on hash-table iteration order.
/// A TradingDesk is a plain value: copying one gives an independent snapshot.
class TradingDesk {
public:
    explicit TradingDesk(RiskLimits limits) : risk_(limits) {}

    /// Duplicate id -> std::invalid_argument.  A risk-rejected order is still registered, as REJECTED with reject_reason = the reason name.
    RiskResult submit(const Order& order) {
        journal_.emplace_back(Submit(order));
        return handle_submit(order);
    }
    /// false = duplicate Fill.  Illegal events throw (state unchanged) but stay in the journal.
    bool on_exec(const ExecEvent& event) {
        journal_.push_back(to_desk_event(event));
        return handle_exec(event);
    }
    void set_reference_price(const std::string& symbol, long long px) {
        journal_.emplace_back(SetReferencePrice(symbol, px));  // the event validates px (throws before it is journaled)
        risk_.set_reference_price(symbol, px);
    }
    void halt() { journal_.emplace_back(Halt{}); risk_.halt(); }
    void resume() { journal_.emplace_back(Resume{}); risk_.resume(); }

    OrderView order(long long id) const { return orders_.get(id); }
    std::vector<OrderView> all_orders() const { return orders_.all(); }
    Position position(const std::string& symbol) const { return positions_.get(symbol); }
    std::vector<std::string> symbols() const { return positions_.symbols(); }

    /// A copy of the journal (Java: List.copyOf).  By value, so later calls cannot change what the caller holds.
    std::vector<DeskEvent> journal() const { return journal_; }

    /// Rebuild a desk from a journal.  An input that threw the first time throws again and is swallowed again: same state.
    static TradingDesk replay(const RiskLimits& limits, const std::vector<DeskEvent>& journal) {
        TradingDesk d(limits);
        for (const DeskEvent& e : journal) {
            d.journal_.push_back(e);
            try {
                d.handle(e);
            } catch (const std::logic_error&) {  // invalid_argument, out_of_range, IllegalTransitionException: the caller saw it the first time
            } catch (const std::overflow_error&) {
            }
        }
        return d;
    }

private:
    template <class E> static constexpr bool is_exec_v = std::is_constructible_v<ExecEvent, const E&>;

    /// The deterministic transition function.  Overloaded over a variant: a new DeskEvent alternative without a handler does not compile.
    void handle(const DeskEvent& e) {
        std::visit(
            Overloaded{
                [&](const Submit& s) { (void)handle_submit(s.order()); },
                [&](const SetReferencePrice& r) { risk_.set_reference_price(r.symbol(), r.px()); },
                [&](const Halt&) { risk_.halt(); },
                [&](const Resume&) { risk_.resume(); },
                [&]<class E>(const E& x) requires is_exec_v<E> { (void)handle_exec(ExecEvent(x)); },
            },
            e);
    }

    RiskResult handle_submit(const Order& o) {
        if (orders_.contains(o.id())) throw std::invalid_argument("duplicate order id " + std::to_string(o.id()));
        const RiskResult r = risk_.check(o, positions_, orders_);  // BEFORE registering: otherwise the order counts itself as open
        orders_.submit(o);
        if (!r.is_accepted()) orders_.apply(Reject(o.id(), std::string(to_string(*r.reason()))));  // an output, not an input: not journaled
        return r;
    }

    bool handle_exec(const ExecEvent& x) {
        const bool applied = orders_.apply(x);
        if (applied) {
            if (const auto* f = std::get_if<Fill>(&x)) {
                const Order o = orders_.get(f->order_id()).order;
                positions_.on_fill(o.symbol(), o.side(), f->qty(), f->px());
            }
        }
        return applied;
    }

    OrderManager orders_;
    PositionBook positions_;
    RiskEngine risk_;
    std::vector<DeskEvent> journal_;
};

}  // namespace trading
