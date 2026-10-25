// ld02 · Trading OOD (order state machine · positions and PnL · pre-trade risk · event-sourced desk) — C++20 starter.
// Statement: ../problem.md.  Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: every value type (Order, OrderView, events, DeskEvent, RiskLimits, RiskReason, RiskResult, Position), the exception notes and the checked-arithmetic helpers.
// To write: OrderManager, PositionBook, Position::unrealized_pnl, RiskEngine, TradingDesk.
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

// ================================================================================================ To write
namespace trading {

inline long long Position::unrealized_pnl(long long) const { throw std::logic_error("TODO"); }

// ============================================================================================ Part 1
/// Order state machine.  Single-threaded.  Rules in ../problem.md ("状态转移表" and "规则").  Key points:
///  * validate first, mutate after: any throwing path leaves every field unchanged;
///  * a duplicate exec id is detected BEFORE the state check, and an exec id is recorded only after every check passed;
///  * open_count() and open_leaves() are maintained incrementally, O(1);
///  * the visitor over ExecEvent is std::visit(Overloaded{...}): one lambda per alternative, so a missing case does not compile.
/// Errors: submit duplicate id -> std::invalid_argument; apply unknown order -> std::out_of_range; illegal transition, overfill, fill price
/// beyond the limit (buy px > limit, sell px < limit) -> IllegalTransitionException; cum_notional overflow -> std::overflow_error (use mul_exact / add_exact).
class OrderManager {
public:
    /// New order, state PENDING.
    void submit(const Order&) { throw std::logic_error("TODO"); }
    /// true = applied; false = duplicate Fill (exec id seen before), no effect.
    bool apply(const ExecEvent&) { throw std::logic_error("TODO"); }
    bool contains(long long) const { throw std::logic_error("TODO"); }
    /// Unknown order -> std::out_of_range.
    OrderView get(long long) const { throw std::logic_error("TODO"); }
    /// Non-terminal orders (PENDING / WORKING / PARTIALLY_FILLED), ascending id.
    std::vector<OrderView> open() const { throw std::logic_error("TODO"); }
    /// All orders, ascending id.
    std::vector<OrderView> all() const { throw std::logic_error("TODO"); }
    /// O(1).
    int open_count() const { throw std::logic_error("TODO"); }
    /// Remaining quantity over the non-terminal orders of this symbol and side, PENDING included.  O(1).
    long long open_leaves(const std::string&, Side) const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 2
/// Positions and PnL, FIFO matching, integers only.  Per symbol a queue of open lots (qty, px), all on one side.
/// Same side (or flat): append a lot.  Opposite side: close lots from the front, realising dir * (fill px - lot px) * closed qty;
/// leftover quantity flips the position (it becomes the first lot of the new direction at the fill price).
/// Overflow -> std::overflow_error and the position stays as it was: compute the PnL read-only first, commit afterwards.
class PositionBook {
public:
    /// qty <= 0 or px <= 0 -> std::invalid_argument.
    void on_fill(const std::string&, Side, long long, long long) { throw std::logic_error("TODO"); }
    /// A symbol never seen -> Position::flat(symbol).
    Position get(const std::string&) const { throw std::logic_error("TODO"); }
    long long net_qty(const std::string&) const { throw std::logic_error("TODO"); }
    long long total_realized() const { throw std::logic_error("TODO"); }
    /// Lexicographic order.
    std::vector<std::string> symbols() const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 3
/// Pre-trade risk.  check() only reads.  Order of the checks = declaration order of RiskReason, the first violation wins:
/// halted; no reference price (fail closed); qty > max_order_qty; px * qty > max_order_notional (an overflowing product is also
/// NotionalLimit, never wrapped into a small number); price band, integer cross-multiplication |px - ref| * 10'000 <= ref * bps
/// (boundary passes); open orders >= max_open_orders (all symbols, PENDING counts, this order not yet registered);
/// worst-case position: net + open buys (+ this order if a buy) <= max_position and net - open sells (+ this order if a sell) >= -max_position.
/// Signed overflow is undefined behaviour in C++: use __builtin_*_overflow where an input can be huge.
class RiskEngine {
public:
    explicit RiskEngine(RiskLimits) { throw std::logic_error("TODO"); }
    /// px <= 0 -> std::invalid_argument.
    void set_reference_price(const std::string&, long long) { throw std::logic_error("TODO"); }
    void halt() { throw std::logic_error("TODO"); }
    void resume() { throw std::logic_error("TODO"); }
    bool halted() const { throw std::logic_error("TODO"); }
    RiskResult check(const Order&, const PositionBook&, const OrderManager&) const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 4
/// Event-sourced single-writer desk.  Every mutating method: (1) append the input to the journal, (2) change the in-memory state through a
/// deterministic handle(DeskEvent), (3) return.  An input that throws is still in the journal.
///  * submit: duplicate id -> std::invalid_argument (state unchanged).  Run risk.check BEFORE orders.submit (else the order counts itself).
///    Accepted: orders.submit.  Rejected: orders.submit, then immediately orders.apply(Reject(id, name of the reason)), so the order is REJECTED
///    with reject_reason "QTY_LIMIT" etc.  That internal Reject is an output: it is NOT journaled.
///  * on_exec: a successfully applied Fill also updates the PositionBook (the order's symbol and side, the fill's qty and px); a duplicate does not.
///  * replay: a new desk, feed every journal entry through handle(); an input that threw before throws again and is swallowed again
///    (catch std::logic_error and std::overflow_error, nothing wider).  journal(), all_orders(), position(s) must equal the original's.
/// Hint: the visitor over DeskEvent is another Overloaded; a defaulted copy of the desk is a legitimate independent snapshot.
class TradingDesk {
public:
    explicit TradingDesk(RiskLimits) { throw std::logic_error("TODO"); }
    RiskResult submit(const Order&) { throw std::logic_error("TODO"); }
    /// false = duplicate Fill.
    bool on_exec(const ExecEvent&) { throw std::logic_error("TODO"); }
    void set_reference_price(const std::string&, long long) { throw std::logic_error("TODO"); }
    void halt() { throw std::logic_error("TODO"); }
    void resume() { throw std::logic_error("TODO"); }
    OrderView order(long long) const { throw std::logic_error("TODO"); }
    std::vector<OrderView> all_orders() const { throw std::logic_error("TODO"); }
    Position position(const std::string&) const { throw std::logic_error("TODO"); }
    std::vector<std::string> symbols() const { throw std::logic_error("TODO"); }
    /// A copy of the journal, input order, failed inputs included.
    std::vector<DeskEvent> journal() const { throw std::logic_error("TODO"); }
    static TradingDesk replay(const RiskLimits&, const std::vector<DeskEvent>&) { throw std::logic_error("TODO"); }
};

}  // namespace trading
