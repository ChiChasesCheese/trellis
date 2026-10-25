// ld02 · Trading OOD — C++20 tests.  Same cases as test/OrderManagerTest.java, PositionBookTest.java, RiskEngineTest.java,
// TradingDeskTest.java plus C++-only edge cases (tag "cpp"): the closed variant types, value semantics (a desk copy is a
// snapshot), signed-overflow-is-UB in the aggregates and the worst-case position, nothing nullable.
#include <climits>
#include <iostream>
#include <random>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace trading;

namespace trading {
std::ostream& operator<<(std::ostream& os, const Order& o) {
    return os << "Order{" << o.id() << "," << o.symbol() << "," << (o.side() == Side::Buy ? "BUY" : "SELL") << "," << o.qty() << "@" << o.px() << "}";
}
std::ostream& operator<<(std::ostream& os, const OrderView& v) {
    return os << "View{" << v.order << ",status=" << static_cast<int>(v.status) << ",cum=" << v.cum_qty << "/" << v.cum_notional
              << ",reason=" << (v.reject_reason ? *v.reject_reason : std::string("-")) << "}";
}
std::ostream& operator<<(std::ostream& os, const Position& p) {
    return os << "Position{" << p.symbol << "," << p.net_qty << "," << p.open_cost << "," << p.realized_pnl << "}";
}
std::ostream& operator<<(std::ostream& os, const RiskResult& r) {
    return os << (r.is_accepted() ? std::string("ACCEPTED") : "Rejected(" + std::string(to_string(*r.reason())) + ")");
}
std::ostream& operator<<(std::ostream& os, const Halt&) { return os << "Halt"; }
std::ostream& operator<<(std::ostream& os, const Resume&) { return os << "Resume"; }
std::ostream& operator<<(std::ostream& os, const Ack& a) { return os << "Ack{" << a.order_id() << "}"; }
}  // namespace trading

namespace {
Order buy(long long id, const std::string& sym, long long qty, long long px) { return Order(id, sym, Side::Buy, qty, px); }
Order sell(long long id, const std::string& sym, long long qty, long long px) { return Order(id, sym, Side::Sell, qty, px); }
constexpr OrderStatus PENDING = OrderStatus::Pending, WORKING = OrderStatus::Working, PARTIAL = OrderStatus::PartiallyFilled,
                      FILLED = OrderStatus::Filled, CANCELED = OrderStatus::Canceled, REJECTED = OrderStatus::Rejected;
std::vector<long long> ids(const std::vector<OrderView>& vs) {
    std::vector<long long> out;
    for (const auto& v : vs) out.push_back(v.order.id());
    return out;
}
unsigned pick(std::mt19937& rnd, unsigned n) { return static_cast<unsigned>(rnd() % n); }
}  // namespace

// ================================================ Part 1: OrderManager

TEST(happy_path_partial_then_full, "part1") {
    OrderManager mgr;
    mgr.submit(buy(1, "AAPL", 100, 150));
    CHECK_EQ(mgr.get(1).status, PENDING);
    CHECK(mgr.apply(Ack(1)));
    CHECK_EQ(mgr.get(1).status, WORKING);
    CHECK(mgr.apply(Fill(1, 900, 30, 149)));
    auto v = mgr.get(1);
    CHECK_EQ(v.status, PARTIAL);
    CHECK_EQ(v.cum_qty, 30);
    CHECK_EQ(v.cum_notional, 30 * 149);
    CHECK_EQ(v.leaves_qty(), 70);
    CHECK(mgr.apply(Fill(1, 901, 70, 150)));
    v = mgr.get(1);
    CHECK_EQ(v.status, FILLED);
    CHECK_EQ(v.leaves_qty(), 0);
    CHECK_EQ(v.cum_notional, 30 * 149 + 70 * 150);
    CHECK(mgr.open().empty());
    CHECK_EQ(mgr.open_count(), 0);
}

TEST(single_fill_completes_order, "part1") {
    OrderManager mgr;
    mgr.submit(sell(5, "MSFT", 10, 300));
    mgr.apply(Ack(5));
    mgr.apply(Fill(5, 1, 10, 301));
    CHECK_EQ(mgr.get(5).status, FILLED);
}

TEST(duplicate_order_id_rejected, "part1") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 1, 1));
    CHECK_THROWS_AS(mgr.submit(buy(1, "B", 2, 2)), std::invalid_argument);
    CHECK_EQ(mgr.get(1).order.symbol(), "A");  // the original was not overwritten
    CHECK_EQ(mgr.open_count(), 1);
    CHECK_EQ(mgr.open_leaves("B", Side::Buy), 0);
}

TEST(unknown_order, "part1,edge") {
    OrderManager mgr;
    CHECK_THROWS_AS(mgr.get(42), std::out_of_range);
    CHECK_THROWS_AS(mgr.apply(Ack(42)), std::out_of_range);
    CHECK(!mgr.contains(42));
}

TEST(cancel_from_working_and_partial, "part1") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    mgr.apply(Ack(1));
    CHECK(mgr.apply(Cancel(1)));
    CHECK_EQ(mgr.get(1).status, CANCELED);
    CHECK_EQ(mgr.get(1).leaves_qty(), 0);

    mgr.submit(buy(2, "A", 10, 5));
    mgr.apply(Ack(2));
    mgr.apply(Fill(2, 7, 4, 5));
    mgr.apply(Cancel(2));
    const auto v = mgr.get(2);
    CHECK_EQ(v.status, CANCELED);
    CHECK_EQ(v.cum_qty, 4);      // the filled part stays
    CHECK_EQ(v.leaves_qty(), 0);  // the rest is no longer a risk
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), 0);
}

TEST(reject_only_from_pending, "part1") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    CHECK(mgr.apply(Reject(1, "bad symbol")));
    const auto v = mgr.get(1);
    CHECK_EQ(v.status, REJECTED);
    CHECK_EQ(v.reject_reason, std::optional<std::string>("bad symbol"));
    CHECK_EQ(v.leaves_qty(), 0);

    mgr.submit(buy(2, "A", 10, 5));
    mgr.apply(Ack(2));
    CHECK_THROWS_AS(mgr.apply(Reject(2, "late")), IllegalTransitionException);
    CHECK_EQ(mgr.get(2).status, WORKING);
}

TEST(illegal_transitions_leave_state_untouched, "part1,edge") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    // PENDING cannot Fill or Cancel
    CHECK_THROWS_AS(mgr.apply(Fill(1, 1, 1, 5)), IllegalTransitionException);
    CHECK_THROWS_AS(mgr.apply(Cancel(1)), IllegalTransitionException);
    CHECK_EQ(mgr.get(1).cum_qty, 0);
    mgr.apply(Ack(1));
    CHECK_THROWS_AS(mgr.apply(Ack(1)), IllegalTransitionException);  // a second Ack
    mgr.apply(Cancel(1));
    // nothing is allowed after a terminal state
    CHECK_THROWS_AS(mgr.apply(Cancel(1)), IllegalTransitionException);
    CHECK_THROWS_AS(mgr.apply(Ack(1)), IllegalTransitionException);
    CHECK_THROWS_AS(mgr.apply(Fill(1, 2, 1, 5)), IllegalTransitionException);
    CHECK_EQ(mgr.get(1).status, CANCELED);
}

TEST(overfill_rejected_and_not_recorded, "part1,edge") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    mgr.apply(Ack(1));
    mgr.apply(Fill(1, 1, 6, 5));
    CHECK_THROWS_AS(mgr.apply(Fill(1, 2, 5, 5)), IllegalTransitionException);  // 6 + 5 > 10
    CHECK_EQ(mgr.get(1).cum_qty, 6);
    // exec id 2 was NOT remembered: the same id with a legal quantity must succeed
    CHECK(mgr.apply(Fill(1, 2, 4, 5)));
    CHECK_EQ(mgr.get(1).status, FILLED);
}

TEST(fill_price_must_respect_limit, "part1,edge") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 100));
    mgr.apply(Ack(1));
    CHECK_THROWS_AS(mgr.apply(Fill(1, 1, 1, 101)), IllegalTransitionException);  // a buy may not pay more than its limit
    CHECK(mgr.apply(Fill(1, 2, 1, 100)));  // equal to the limit is fine
    CHECK(mgr.apply(Fill(1, 3, 1, 90)));   // price improvement is fine

    mgr.submit(sell(2, "A", 10, 100));
    mgr.apply(Ack(2));
    CHECK_THROWS_AS(mgr.apply(Fill(2, 4, 1, 99)), IllegalTransitionException);
    CHECK(mgr.apply(Fill(2, 5, 1, 100)));
    CHECK(mgr.apply(Fill(2, 6, 1, 120)));
}

TEST(duplicate_fill_is_idempotent, "part1,edge") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    mgr.apply(Ack(1));
    CHECK(mgr.apply(Fill(1, 77, 4, 5)));
    CHECK(!mgr.apply(Fill(1, 77, 4, 5)));  // delivered twice
    CHECK_EQ(mgr.get(1).cum_qty, 4);
    CHECK(mgr.apply(Fill(1, 78, 6, 5)));
    CHECK_EQ(mgr.get(1).status, FILLED);
    // old reports again after FILLED: still just duplicates, not illegal transitions
    CHECK(!mgr.apply(Fill(1, 77, 4, 5)));
    CHECK(!mgr.apply(Fill(1, 78, 6, 5)));
    CHECK_EQ(mgr.get(1).cum_qty, 10);
}

TEST(open_orders_listed_by_id_and_exclude_terminal, "part1") {
    OrderManager mgr;
    for (long long id : {9, 3, 7, 1}) mgr.submit(buy(id, "A", 5, 5));
    mgr.apply(Reject(3, "x"));
    CHECK_EQ(ids(mgr.open()), (std::vector<long long>{1, 7, 9}));
    CHECK_EQ(ids(mgr.all()), (std::vector<long long>{1, 3, 7, 9}));
    CHECK_EQ(mgr.open_count(), 3);
}

TEST(open_leaves_by_symbol_and_side, "part1") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    mgr.submit(buy(2, "A", 7, 5));
    mgr.submit(sell(3, "A", 4, 5));
    mgr.submit(buy(4, "B", 100, 5));
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), 17);
    CHECK_EQ(mgr.open_leaves("A", Side::Sell), 4);
    CHECK_EQ(mgr.open_leaves("B", Side::Buy), 100);
    CHECK_EQ(mgr.open_leaves("C", Side::Buy), 0);
    mgr.apply(Ack(1));
    mgr.apply(Fill(1, 1, 3, 5));
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), 14);
    mgr.apply(Cancel(1));
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), 7);
    mgr.apply(Reject(2, "r"));
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), 0);
}

TEST(value_types_reject_invalid_values, "part1,edge") {
    CHECK_THROWS_AS(Order(0, "A", Side::Buy, 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Order(1, "A", Side::Buy, 0, 1), std::invalid_argument);
    CHECK_THROWS_AS(Order(1, "A", Side::Buy, 1, -1), std::invalid_argument);
    CHECK_THROWS_AS(Order(1, " ", Side::Buy, 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Order(1, "", Side::Buy, 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Fill(1, 1, 0, 1), std::invalid_argument);
    CHECK_THROWS_AS(Fill(1, 1, 1, 0), std::invalid_argument);
    CHECK_THROWS_AS(SetReferencePrice("A", 0), std::invalid_argument);
    CHECK_NOTHROW(Order(1, "A", Side::Sell, 1, 1));
}

TEST(notional_overflow_does_not_corrupt_order, "part1,edge") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", LLONG_MAX / 2, LLONG_MAX / 2));
    mgr.apply(Ack(1));
    CHECK_THROWS_AS(mgr.apply(Fill(1, 1, LLONG_MAX / 2, LLONG_MAX / 2)), std::overflow_error);
    CHECK_EQ(mgr.get(1).cum_qty, 0);
    CHECK_EQ(mgr.get(1).status, WORKING);
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), LLONG_MAX / 2);
    CHECK(mgr.apply(Fill(1, 1, 1, 1)));  // exec id 1 was not consumed by the failed attempt
}

TEST(random_events_keep_aggregates_consistent, "part1,edge") {
    // Random event stream against a naive model: after every step the O(1) aggregates equal a re-computation over all orders,
    // and an illegal event changes nothing.
    OrderManager mgr;
    std::mt19937 rnd(7);
    long long exec_id = 0;
    const std::string syms[] = {"A", "B", "C"};
    for (long long id = 1; id <= 300; ++id) mgr.submit(Order(id, syms[pick(rnd, 3)], pick(rnd, 2) ? Side::Buy : Side::Sell, 1 + pick(rnd, 20), 100));
    auto check_aggregates = [&] {
        for (const auto& s : syms)
            for (Side side : {Side::Buy, Side::Sell}) {
                long long sum = 0;
                for (const auto& v : mgr.open())
                    if (v.order.symbol() == s && v.order.side() == side) sum += v.leaves_qty();
                CHECK_EQ(sum, mgr.open_leaves(s, side));
            }
        CHECK_EQ(mgr.open().size(), static_cast<std::size_t>(mgr.open_count()));
    };
    for (int step = 0; step < 4000; ++step) {
        const long long id = 1 + pick(rnd, 300);
        ExecEvent e = Ack(id);
        switch (pick(rnd, 4)) {
            case 0: e = Ack(id); break;
            case 1: e = Fill(id, ++exec_id, 1 + pick(rnd, 5), 100); break;
            case 2: e = Cancel(id); break;
            default: e = Reject(id, "r"); break;
        }
        const auto before = mgr.get(id);
        try {
            mgr.apply(e);
        } catch (const IllegalTransitionException&) {
            CHECK_EQ(before, mgr.get(id));
        }
        if (step % 97 == 0) check_aggregates();
    }
    check_aggregates();
}

// ---- C++-only, Part 1

static_assert(std::variant_size_v<ExecEvent> == 4, "Ack, Fill, Cancel, Reject: the closed set of execution reports");
static_assert(std::variant_size_v<DeskEvent> == 8, "the four execution reports + Submit, SetReferencePrice, Halt, Resume");
static_assert(!std::is_default_constructible_v<Order>, "there is no 'empty' order: every Order that exists passed the constructor's checks");
static_assert(std::is_nothrow_move_constructible_v<Order> && std::is_nothrow_move_constructible_v<DeskEvent>,
              "std::vector moves (instead of copying) its elements on growth only when the move cannot throw");

TEST(overflowing_open_quantity_is_refused_before_any_change, "part1,cpp,edge") {
    // Java wraps silently; in C++ signed overflow is undefined behaviour, so the aggregate is summed with a checked add BEFORE the order is stored.
    OrderManager mgr;
    mgr.submit(buy(1, "A", LLONG_MAX / 2 + 1, 1));
    CHECK_THROWS_AS(mgr.submit(buy(2, "A", LLONG_MAX / 2 + 1, 1)), std::overflow_error);
    CHECK(!mgr.contains(2));
    CHECK_EQ(mgr.open_count(), 1);
    CHECK_EQ(mgr.open_leaves("A", Side::Buy), LLONG_MAX / 2 + 1);
    CHECK_NOTHROW(mgr.submit(sell(3, "A", LLONG_MAX / 2 + 1, 1)));  // the other side is a different bucket
}

TEST(views_are_snapshots_not_references, "part1,cpp") {
    OrderManager mgr;
    mgr.submit(buy(1, "A", 10, 5));
    auto before = mgr.get(1);  // a copy: later changes must not show through
    mgr.apply(Ack(1));
    CHECK_EQ(before.status, PENDING);
    CHECK_EQ(mgr.get(1).status, WORKING);
    before.cum_qty = 999;  // and writing to the copy must not reach the manager
    CHECK_EQ(mgr.get(1).cum_qty, 0);
}

// ================================================ Part 2: PositionBook

TEST(unknown_symbol_is_flat, "part2") {
    PositionBook book;
    CHECK_EQ(book.get("X"), Position::flat("X"));
    CHECK_EQ(book.net_qty("X"), 0);
    CHECK_EQ(book.total_realized(), 0);
    CHECK(book.symbols().empty());
}

TEST(build_long_then_close_at_profit, "part2") {
    PositionBook book;
    book.on_fill("A", Side::Buy, 10, 100);
    book.on_fill("A", Side::Buy, 10, 110);
    auto p = book.get("A");
    CHECK_EQ(p.net_qty, 20);
    CHECK_EQ(p.open_cost, 10 * 100 + 10 * 110);
    CHECK_EQ(p.realized_pnl, 0);
    book.on_fill("A", Side::Sell, 15, 120);  // FIFO: 10@100 first, then 5@110
    p = book.get("A");
    CHECK_EQ(p.net_qty, 5);
    CHECK_EQ(p.open_cost, 5 * 110);
    CHECK_EQ(p.realized_pnl, 10 * (120 - 100) + 5 * (120 - 110));
    book.on_fill("A", Side::Sell, 5, 100);  // close at a loss
    p = book.get("A");
    CHECK_EQ(p.net_qty, 0);
    CHECK_EQ(p.open_cost, 0);
    CHECK_EQ(p.realized_pnl, 250 + 5 * (100 - 110));
}

TEST(short_position_pnl_signs_are_mirrored, "part2") {
    PositionBook book;
    book.on_fill("A", Side::Sell, 10, 100);
    CHECK_EQ(book.net_qty("A"), -10);
    CHECK_EQ(book.get("A").open_cost, 1000);
    book.on_fill("A", Side::Buy, 4, 90);  // cover cheaper -> profit
    CHECK_EQ(book.get("A").realized_pnl, 4 * 10);
    book.on_fill("A", Side::Buy, 6, 130);  // cover dearer -> loss
    const auto p = book.get("A");
    CHECK_EQ(p.net_qty, 0);
    CHECK_EQ(p.realized_pnl, 40 + 6 * (100 - 130));
}

TEST(flip_through_zero_opens_opposite_lot_at_fill_price, "part2,edge") {
    PositionBook book;
    book.on_fill("A", Side::Buy, 10, 100);
    book.on_fill("A", Side::Sell, 25, 110);  // closes 10 (+100), flips to short 15 @110
    auto p = book.get("A");
    CHECK_EQ(p.net_qty, -15);
    CHECK_EQ(p.open_cost, 15 * 110);
    CHECK_EQ(p.realized_pnl, 100);
    book.on_fill("A", Side::Buy, 15, 105);  // cover 15 @105: +15*5
    p = book.get("A");
    CHECK_EQ(p.net_qty, 0);
    CHECK_EQ(p.realized_pnl, 100 + 75);
    CHECK_EQ(p.open_cost, 0);
    book.on_fill("A", Side::Sell, 1, 50);  // from flat, either direction
    CHECK_EQ(book.net_qty("A"), -1);
}

TEST(exact_close_goes_flat, "part2,edge") {
    PositionBook book;
    book.on_fill("A", Side::Buy, 7, 10);
    book.on_fill("A", Side::Sell, 7, 10);
    CHECK_EQ(book.get("A").net_qty, 0);
    CHECK_EQ(book.get("A").realized_pnl, 0);
    book.on_fill("A", Side::Buy, 3, 11);
    CHECK_EQ(book.net_qty("A"), 3);
    CHECK_EQ(book.get("A").open_cost, 33);
}

TEST(symbols_are_independent_and_sorted, "part2") {
    PositionBook book;
    book.on_fill("MSFT", Side::Buy, 1, 10);
    book.on_fill("AAPL", Side::Sell, 2, 20);
    book.on_fill("GOOG", Side::Buy, 3, 30);
    book.on_fill("AAPL", Side::Buy, 2, 15);
    CHECK_EQ(book.symbols(), (std::vector<std::string>{"AAPL", "GOOG", "MSFT"}));
    CHECK_EQ(book.get("AAPL").realized_pnl, 10);
    CHECK_EQ(book.total_realized(), 10);
    CHECK_EQ(book.net_qty("MSFT"), 1);
}

TEST(unrealized_pnl, "part2") {
    PositionBook book;
    book.on_fill("A", Side::Buy, 10, 100);
    book.on_fill("A", Side::Buy, 10, 120);
    CHECK_EQ(book.get("A").unrealized_pnl(130), 20 * 130 - 2200);
    CHECK_EQ(book.get("A").unrealized_pnl(90), 20 * 90 - 2200);  // negative
    book.on_fill("B", Side::Sell, 5, 200);
    CHECK_EQ(book.get("B").unrealized_pnl(190), 1000 - 5 * 190);  // short: price down -> profit
    CHECK_EQ(book.get("B").unrealized_pnl(210), 1000 - 5 * 210);
    CHECK_EQ(book.get("Z").unrealized_pnl(1234), 0);
}

TEST(unrealized_pnl_overflow_throws, "part2,edge") {
    PositionBook book;
    book.on_fill("A", Side::Buy, 1'000'000'000, 1);
    CHECK_THROWS_AS(book.get("A").unrealized_pnl(LLONG_MAX / 2), std::overflow_error);
}

TEST(invalid_inputs_rejected, "part2,edge") {
    PositionBook book;
    CHECK_THROWS_AS(book.on_fill("A", Side::Buy, 0, 10), std::invalid_argument);
    CHECK_THROWS_AS(book.on_fill("A", Side::Buy, 1, 0), std::invalid_argument);
    CHECK_THROWS_AS(book.on_fill("A", Side::Buy, -5, 10), std::invalid_argument);
    CHECK(book.symbols().empty(), "a rejected fill must not create the symbol");
}

TEST(overflow_throws_and_leaves_position_unchanged, "part2,edge") {
    PositionBook book;
    book.on_fill("A", Side::Buy, 4'000'000'000LL, 1);
    book.on_fill("A", Side::Sell, 1, 4'000'000'000LL * 3);  // a normal state first: closes 1 lot, realises 12e9 - 1
    const auto before = book.get("A");
    // (px - lot px) * qty exceeds LLONG_MAX
    CHECK_THROWS_AS(book.on_fill("A", Side::Sell, 3'000'000'000LL, LLONG_MAX / 2), std::overflow_error);
    CHECK_EQ(before, book.get("A"));
}

TEST(random_fills_match_unit_by_unit_model, "part2,edge") {
    // Reference model: expand every fill into single units and match them one by one, FIFO.
    PositionBook book;
    std::mt19937 rnd(11);
    std::deque<long long> units;  // opening price of each open unit
    int dir = 0;
    long long realized = 0;
    for (int i = 0; i < 2000; ++i) {
        const Side side = pick(rnd, 2) ? Side::Buy : Side::Sell;
        const long long qty = 1 + pick(rnd, 8), px = 90 + pick(rnd, 21);
        book.on_fill("A", side, qty, px);
        for (long long u = 0; u < qty; ++u) {
            if (dir == 0 || dir == sign(side)) {
                units.push_back(px);
                dir = sign(side);
            } else {
                const long long open = units.front();
                units.pop_front();
                realized += dir * (px - open);
                if (units.empty()) dir = 0;
            }
        }
        const auto p = book.get("A");
        long long cost = 0;
        for (long long u : units) cost += u;
        CHECK_EQ(p.net_qty, dir * static_cast<long long>(units.size()));
        CHECK_EQ(p.realized_pnl, realized);
        CHECK_EQ(p.open_cost, cost);
    }
}

TEST(many_fills_fast, "part2,perf") {
    PositionBook book;
    std::mt19937 rnd(0);
    CHECK_WITHIN_MS(2000,
        for (int i = 0; i < 300'000; ++i)
            book.on_fill("S" + std::to_string(i % 50), pick(rnd, 2) ? Side::Buy : Side::Sell, 1 + pick(rnd, 5), 100 + pick(rnd, 10)););
}

// ================================================ Part 3: RiskEngine
// maxQty 1000, maxNotional 1_000_000, maxPos 5000, maxOpen 3, band 500 bp (5 %)

namespace {
const RiskLimits RISK_LIMITS(1'000, 1'000'000, 5'000, 3, 500);

struct RiskFixture {
    PositionBook positions;
    OrderManager orders;
    RiskEngine risk{RISK_LIMITS};
    RiskFixture() { risk.set_reference_price("A", 100); }
    RiskResult check(const Order& o) const { return risk.check(o, positions, orders); }
    void expect_rejected(RiskReason reason, const Order& o) const { CHECK_EQ(check(o), RiskResult::rejected(reason), "order " + std::to_string(o.id())); }
};
Order rbuy(long long id, long long qty, long long px) { return buy(id, "A", qty, px); }
Order rsell(long long id, long long qty, long long px) { return sell(id, "A", qty, px); }
}  // namespace

TEST(accepts_ordinary_order, "part3") {
    RiskFixture f;
    CHECK(f.check(rbuy(1, 100, 100)).is_accepted());
    CHECK_EQ(f.check(rbuy(1, 100, 100)), RiskResult::accepted());
}

TEST(quantity_limit_boundary, "part3") {
    RiskFixture f;
    CHECK_EQ(f.check(rbuy(1, 1'000, 100)), RiskResult::accepted());
    f.expect_rejected(RiskReason::QtyLimit, rbuy(2, 1'001, 100));
}

TEST(notional_limit_boundary, "part3") {
    RiskFixture f;
    RiskEngine r(RiskLimits(1'000'000, 10'000, 1'000'000, 10, 10'000));
    r.set_reference_price("A", 100);
    CHECK_EQ(r.check(rbuy(1, 100, 100), f.positions, f.orders), RiskResult::accepted());  // 10_000 == limit passes
    CHECK_EQ(r.check(rbuy(2, 101, 100), f.positions, f.orders), RiskResult::rejected(RiskReason::NotionalLimit));
}

TEST(notional_overflow_is_rejected_not_wrapped, "part3,edge") {
    RiskFixture f;
    RiskEngine r(RiskLimits(LLONG_MAX, LLONG_MAX, LLONG_MAX, 10, 10'000));
    r.set_reference_price("A", LLONG_MAX / 2);
    // px * qty overflows a long: it must not wrap into a small number and pass
    CHECK_EQ(r.check(Order(1, "A", Side::Buy, 1LL << 40, 1LL << 40), f.positions, f.orders), RiskResult::rejected(RiskReason::NotionalLimit));
}

TEST(price_band_boundary_is_inclusive, "part3") {
    RiskFixture f;
    CHECK_EQ(f.check(rbuy(1, 10, 105)), RiskResult::accepted());  // +5.00 % == the band
    CHECK_EQ(f.check(rbuy(2, 10, 95)), RiskResult::accepted());   // -5.00 %
    f.expect_rejected(RiskReason::PriceBand, rbuy(3, 10, 106));
    f.expect_rejected(RiskReason::PriceBand, rsell(4, 10, 94));
    f.expect_rejected(RiskReason::PriceBand, rsell(5, 10, 1));  // fat finger: one zero short
}

TEST(price_band_uses_integer_arithmetic_no_rounding, "part3,edge") {
    RiskFixture f;
    f.risk.set_reference_price("B", 10'007);  // 5 % = 500.35: 501 is outside, 500 is inside
    CHECK_EQ(f.risk.check(Order(1, "B", Side::Buy, 1, 10'507), f.positions, f.orders), RiskResult::accepted());
    CHECK_EQ(f.risk.check(Order(2, "B", Side::Buy, 1, 10'508), f.positions, f.orders), RiskResult::rejected(RiskReason::PriceBand));
    f.risk.set_reference_price("B", 3);  // 5 % of 3 = 0.15 -> only px == 3 passes
    CHECK_EQ(f.risk.check(Order(3, "B", Side::Buy, 1, 3), f.positions, f.orders), RiskResult::accepted());
    CHECK_EQ(f.risk.check(Order(4, "B", Side::Buy, 1, 4), f.positions, f.orders), RiskResult::rejected(RiskReason::PriceBand));
}

TEST(missing_reference_price_fails_closed, "part3") {
    RiskFixture f;
    CHECK_EQ(f.check(Order(1, "ZZZ", Side::Buy, 1, 1)), RiskResult::rejected(RiskReason::NoReferencePrice));
}

TEST(reference_price_can_be_updated, "part3") {
    RiskFixture f;
    f.expect_rejected(RiskReason::PriceBand, rbuy(1, 1, 200));
    f.risk.set_reference_price("A", 200);
    CHECK_EQ(f.check(rbuy(2, 1, 200)), RiskResult::accepted());
    CHECK_THROWS_AS(f.risk.set_reference_price("A", 0), std::invalid_argument);
}

TEST(open_orders_limit_counts_all_symbols_and_pending_orders, "part3") {
    RiskFixture f;
    f.orders.submit(rbuy(1, 1, 100));  // PENDING counts
    f.orders.submit(Order(2, "B", Side::Sell, 1, 100));
    f.orders.submit(rbuy(3, 1, 100));
    f.expect_rejected(RiskReason::OpenOrdersLimit, rbuy(4, 1, 100));
    f.orders.apply(Reject(2, "x"));  // a terminal order frees its slot
    CHECK_EQ(f.check(rbuy(4, 1, 100)), RiskResult::accepted());
}

TEST(position_limit_counts_existing_net_position, "part3") {
    RiskFixture f;
    f.positions.on_fill("A", Side::Buy, 4'500, 100);
    CHECK_EQ(f.check(rbuy(1, 500, 100)), RiskResult::accepted());  // 4500 + 500 == 5000
    f.expect_rejected(RiskReason::PositionLimit, rbuy(2, 501, 100));
    // selling reduces the position, long limits do not bind; only selling past zero into the short side is limited
    CHECK_EQ(f.check(rsell(3, 1'000, 100)), RiskResult::accepted());
}

TEST(position_limit_counts_open_orders_worst_case, "part3") {
    RiskFixture f;
    f.orders.submit(rbuy(1, 1'000, 100));
    f.orders.submit(rbuy(2, 1'000, 100));
    f.orders.apply(Ack(1));
    f.orders.apply(Ack(2));
    f.positions.on_fill("A", Side::Buy, 2'500, 100);
    // net 2500 + open buys 2000 = 4500: 500 more is exactly at the limit, 501 is over (looking at the net alone, 2500 + 501 is fine)
    CHECK_EQ(f.check(rbuy(3, 500, 100)), RiskResult::accepted());
    f.expect_rejected(RiskReason::PositionLimit, rbuy(3, 501, 100));
    // order 1 fills completely: 1000 moves from "open" to "net", total exposure unchanged, verdict unchanged
    f.orders.apply(Fill(1, 1, 1'000, 100));
    f.positions.on_fill("A", Side::Buy, 1'000, 100);
    CHECK_EQ(f.check(rbuy(3, 500, 100)), RiskResult::accepted());
    f.expect_rejected(RiskReason::PositionLimit, rbuy(3, 501, 100));
    // order 2 is canceled: 1000 freed
    f.orders.apply(Cancel(2));
    CHECK_EQ(f.check(rbuy(3, 1'000, 100)), RiskResult::accepted());
}

TEST(position_limit_worst_case_short_side, "part3,edge") {
    RiskFixture f;
    RiskEngine r(RiskLimits(1'000, 1'000'000, 5'000, 10, 500));
    r.set_reference_price("A", 100);
    f.orders.submit(rsell(1, 1'000, 100));
    f.orders.submit(rsell(2, 1'000, 100));
    f.positions.on_fill("A", Side::Sell, 2'500, 100);  // net -2500, open sells 2000: worst case -4500
    CHECK_EQ(r.check(rsell(3, 500, 100), f.positions, f.orders), RiskResult::accepted());  // -5000 == the floor
    f.orders.submit(rsell(3, 500, 100));
    CHECK_EQ(r.check(rsell(4, 1, 100), f.positions, f.orders), RiskResult::rejected(RiskReason::PositionLimit));
    CHECK_EQ(r.check(rbuy(5, 1, 100), f.positions, f.orders), RiskResult::accepted());  // a buy adds no short exposure
}

TEST(position_limit_is_per_symbol, "part3") {
    RiskFixture f;
    f.risk.set_reference_price("B", 50);
    f.positions.on_fill("A", Side::Buy, 5'000, 100);
    CHECK_EQ(f.risk.check(Order(1, "B", Side::Buy, 1'000, 50), f.positions, f.orders), RiskResult::accepted());
    f.expect_rejected(RiskReason::PositionLimit, rbuy(2, 1, 100));
}

TEST(halt_rejects_everything_until_resume, "part3") {
    RiskFixture f;
    f.risk.halt();
    CHECK(f.risk.halted());
    f.expect_rejected(RiskReason::Halted, rbuy(1, 1, 100));
    f.expect_rejected(RiskReason::Halted, rsell(2, 1, 100));  // reducing orders too: the kill switch does not pick
    f.risk.resume();
    CHECK(!f.risk.halted());
    CHECK_EQ(f.check(rbuy(3, 1, 100)), RiskResult::accepted());
}

TEST(first_violated_check_is_reported_in_declared_order, "part3,edge") {
    RiskFixture f;
    // quantity, notional and price band all violated -> QtyLimit
    f.expect_rejected(RiskReason::QtyLimit, rbuy(1, 2'000, 1'000));
    // notional and price band violated -> NotionalLimit
    RiskEngine r(RiskLimits(1'000, 1'000, 5'000, 3, 500));
    r.set_reference_price("A", 100);
    CHECK_EQ(r.check(rbuy(2, 10, 1'000), f.positions, f.orders), RiskResult::rejected(RiskReason::NotionalLimit));
    // halted beats everything, even a missing reference price
    f.risk.halt();
    f.expect_rejected(RiskReason::Halted, Order(3, "ZZZ", Side::Buy, 5'000'000, 1));
}

TEST(check_does_not_mutate_anything, "part3") {
    RiskFixture f;
    f.orders.submit(rbuy(1, 10, 100));
    const auto before = f.orders.all();
    for (int i = 0; i < 10; ++i) f.check(rbuy(100 + i, 10, 100));
    CHECK_EQ(f.orders.all(), before);
    CHECK_EQ(f.orders.open_count(), 1);
    CHECK_EQ(f.positions.net_qty("A"), 0);
}

TEST(limits_must_be_positive, "part3,edge") {
    CHECK_THROWS_AS(RiskLimits(0, 1, 1, 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(RiskLimits(1, 1, 1, 0, 1), std::invalid_argument);
    CHECK_THROWS_AS(RiskLimits(1, 1, 1, 1, 0), std::invalid_argument);
    CHECK_THROWS_AS(RiskLimits(1, 0, 1, 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(RiskLimits(1, 1, -1, 1, 1), std::invalid_argument);
}

TEST(worst_case_position_arithmetic_never_overflows, "part3,cpp,edge") {
    // open buys already add up to LLONG_MAX; one more share does not fit in a long.  Java wraps to a huge negative number and ACCEPTS;
    // in C++ the sum would be undefined behaviour (UBSan aborts).  The correct answer: treat "does not fit" as a breach.
    PositionBook positions;
    OrderManager orders;
    RiskEngine r(RiskLimits(LLONG_MAX, LLONG_MAX, LLONG_MAX, 10, 10'000));
    r.set_reference_price("A", 1);
    orders.submit(buy(1, "A", LLONG_MAX, 1));
    CHECK_EQ(r.check(buy(2, "A", 1, 1), positions, orders), RiskResult::rejected(RiskReason::PositionLimit));
    // and the same on the sell side
    orders.submit(sell(3, "A", LLONG_MAX, 1));
    CHECK_EQ(r.check(sell(4, "A", 1, 1), positions, orders), RiskResult::rejected(RiskReason::PositionLimit));
}

TEST(risk_result_is_a_value_with_a_reason, "part3,cpp") {
    const auto ok = RiskResult::accepted();
    const auto no = RiskResult::rejected(RiskReason::QtyLimit);
    CHECK(ok.is_accepted() && !ok.reason().has_value());
    CHECK(!no.is_accepted() && no.reason() == RiskReason::QtyLimit);
    CHECK(ok != no);
    CHECK_EQ(std::string(to_string(RiskReason::OpenOrdersLimit)), "OPEN_ORDERS_LIMIT");
}

// ================================================ Part 4: TradingDesk

namespace {
const RiskLimits DESK_LIMITS(1'000, 10'000'000, 3'000, 50, 1'000);
TradingDesk make_desk() {
    TradingDesk d(DESK_LIMITS);
    d.set_reference_price("A", 100);
    d.set_reference_price("B", 50);
    return d;
}
void expect_same_state(const TradingDesk& a, const TradingDesk& b) {
    CHECK_EQ(a.all_orders(), b.all_orders());
    CHECK_EQ(a.symbols(), b.symbols());
    for (const auto& s : a.symbols()) CHECK_EQ(a.position(s), b.position(s), s);
}
}  // namespace

TEST(full_lifecycle_updates_order_and_position, "part4") {
    auto desk = make_desk();
    CHECK_EQ(desk.submit(buy(1, "A", 100, 100)), RiskResult::accepted());
    CHECK_EQ(desk.order(1).status, PENDING);
    desk.on_exec(Ack(1));
    CHECK(desk.on_exec(Fill(1, 10, 60, 99)));
    CHECK_EQ(desk.position("A").net_qty, 60);
    CHECK_EQ(desk.position("A").open_cost, 60 * 99);
    desk.on_exec(Fill(1, 11, 40, 100));
    CHECK_EQ(desk.order(1).status, FILLED);
    CHECK_EQ(desk.position("A").net_qty, 100);
    // close it
    desk.submit(sell(2, "A", 100, 101));
    desk.on_exec(Ack(2));
    desk.on_exec(Fill(2, 12, 100, 105));
    CHECK_EQ(desk.position("A").net_qty, 0);
    CHECK_EQ(desk.position("A").realized_pnl, 60 * (105 - 99) + 40 * (105 - 100));
}

TEST(risk_rejected_order_is_recorded_as_rejected_with_reason, "part4") {
    auto desk = make_desk();
    const auto r = desk.submit(buy(1, "A", 2'000, 100));
    CHECK_EQ(r, RiskResult::rejected(RiskReason::QtyLimit));
    const auto v = desk.order(1);
    CHECK_EQ(v.status, REJECTED);
    CHECK_EQ(v.reject_reason, std::optional<std::string>("QTY_LIMIT"));
    CHECK_EQ(v.cum_qty, 0);
    // a rejected order no longer uses an open-order slot or position headroom: a full-size order goes straight in
    CHECK_EQ(desk.submit(buy(2, "A", 1'000, 100)), RiskResult::accepted());
    CHECK_EQ(desk.submit(buy(3, "A", 1'000, 100)), RiskResult::accepted());
    CHECK_EQ(desk.submit(buy(4, "A", 1'000, 100)), RiskResult::accepted());  // total exposure 3000 == the limit
    CHECK_EQ(desk.submit(buy(5, "A", 1, 100)), RiskResult::rejected(RiskReason::PositionLimit));
}

TEST(order_does_not_count_itself_against_the_position_limit, "part4") {
    // If the order were registered before the check it would be counted twice, and a limit-sized order would be refused.
    auto desk = make_desk();
    CHECK_EQ(desk.submit(buy(1, "A", 1'000, 100)), RiskResult::accepted());
    CHECK_EQ(desk.submit(buy(2, "A", 1'000, 100)), RiskResult::accepted());
}

TEST(halt_and_resume_are_events_too, "part4") {
    auto desk = make_desk();
    desk.halt();
    CHECK_EQ(desk.submit(buy(1, "A", 1, 100)), RiskResult::rejected(RiskReason::Halted));
    desk.resume();
    CHECK_EQ(desk.submit(buy(2, "A", 1, 100)), RiskResult::accepted());
    CHECK_EQ(desk.order(1).status, REJECTED);
}

TEST(duplicate_order_id_throws_and_does_not_change_the_existing_order, "part4,edge") {
    auto desk = make_desk();
    desk.submit(buy(1, "A", 10, 100));
    CHECK_THROWS_AS(desk.submit(sell(1, "B", 5, 50)), std::invalid_argument);
    CHECK_EQ(desk.order(1).order.symbol(), "A");
}

TEST(duplicate_fill_does_not_double_the_position, "part4,edge") {
    auto desk = make_desk();
    desk.submit(buy(1, "A", 100, 100));
    desk.on_exec(Ack(1));
    CHECK(desk.on_exec(Fill(1, 5, 30, 100)));
    CHECK(!desk.on_exec(Fill(1, 5, 30, 100)));
    CHECK_EQ(desk.position("A").net_qty, 30);
}

TEST(illegal_event_throws_leaves_state_but_stays_in_journal, "part4,edge") {
    auto desk = make_desk();
    desk.submit(buy(1, "A", 10, 100));
    CHECK_THROWS_AS(desk.on_exec(Fill(1, 1, 1, 100)), IllegalTransitionException);  // not acknowledged yet
    CHECK_THROWS_AS(desk.on_exec(Ack(99)), std::out_of_range);
    CHECK_EQ(desk.position("A").net_qty, 0);
    CHECK_EQ(desk.order(1).status, PENDING);
    long long exec_events = 0;
    for (const auto& e : desk.journal()) exec_events += std::holds_alternative<Ack>(e) || std::holds_alternative<Fill>(e);
    CHECK_EQ(exec_events, 2);  // the inputs were recorded before they were processed
}

TEST(journal_is_a_copy_in_input_order, "part4") {
    auto desk = make_desk();
    desk.submit(buy(1, "A", 10, 100));
    desk.on_exec(Ack(1));
    auto j = desk.journal();
    CHECK_EQ(j, (std::vector<DeskEvent>{SetReferencePrice("A", 100), SetReferencePrice("B", 50), Submit(buy(1, "A", 10, 100)), Ack(1)}));
    j.push_back(Halt{});  // changing the copy ...
    CHECK_EQ(desk.journal().size(), 4u);  // ... does not change the desk
    desk.halt();
    CHECK_EQ(j.size(), 5u);  // and later desk activity does not change the copy
    CHECK_EQ(desk.journal().size(), 5u);
}

TEST(replay_reproduces_state_exactly, "part4") {
    auto desk = make_desk();
    desk.submit(buy(1, "A", 500, 100));
    desk.submit(sell(2, "B", 200, 50));
    desk.submit(buy(3, "A", 5'000, 100));  // rejected
    desk.on_exec(Ack(1));
    desk.on_exec(Ack(2));
    desk.on_exec(Fill(1, 1, 300, 99));
    desk.on_exec(Fill(2, 2, 200, 51));
    desk.on_exec(Cancel(1));
    desk.halt();
    desk.submit(buy(4, "A", 1, 100));  // HALTED

    auto copy = TradingDesk::replay(DESK_LIMITS, desk.journal());
    expect_same_state(desk, copy);
    CHECK_EQ(desk.journal(), copy.journal());
    CHECK_EQ(copy.order(4).reject_reason, std::optional<std::string>("HALTED"));
    // the rebuilt desk keeps working
    copy.resume();
    CHECK_EQ(copy.submit(buy(5, "A", 1, 100)), RiskResult::accepted());
}

TEST(replay_swallows_inputs_that_failed_the_first_time, "part4,edge") {
    auto desk = make_desk();
    desk.submit(buy(1, "A", 10, 100));
    try { desk.on_exec(Fill(1, 1, 1, 100)); } catch (const IllegalTransitionException&) {}
    try { desk.submit(buy(1, "A", 10, 100)); } catch (const std::invalid_argument&) {}
    try { desk.on_exec(Cancel(77)); } catch (const std::out_of_range&) {}
    desk.on_exec(Ack(1));
    auto copy = TradingDesk::replay(DESK_LIMITS, desk.journal());
    expect_same_state(desk, copy);
    CHECK_EQ(copy.order(1).status, WORKING);
}

TEST(replay_equals_original_on_random_event_streams, "part4,edge") {
    for (unsigned seed = 0; seed < 25; ++seed) {
        std::mt19937 rnd(seed);
        TradingDesk d(DESK_LIMITS);
        d.set_reference_price("A", 100);
        d.set_reference_price("B", 50);
        long long next_id = 1, exec_id = 1;
        for (int step = 0; step < 600; ++step) {
            try {
                switch (pick(rnd, 10)) {
                    case 0: case 1: case 2: {
                        const bool a = pick(rnd, 2) == 0;
                        const std::string sym = a ? "A" : "B";
                        const long long ref = a ? 100 : 50;
                        const Side side = pick(rnd, 2) ? Side::Buy : Side::Sell;
                        const long long qty = 1 + pick(rnd, 1'200);
                        const long long jitter = pick(rnd, 12);
                        const long long wide = pick(rnd, 8) == 0 ? 20 : 1;
                        d.submit(Order(next_id++, sym, side, qty, ref - 5 + jitter * wide));
                        break;
                    }
                    case 3: case 4: d.on_exec(Ack(1 + pick(rnd, static_cast<unsigned>(next_id)))); break;
                    case 5: case 6: case 7: {
                        const long long order = 1 + pick(rnd, static_cast<unsigned>(next_id));
                        const long long exec = pick(rnd, 8) == 0 ? exec_id : exec_id++;  // sometimes a duplicate id
                        const long long qty = 1 + pick(rnd, 200);
                        const long long px = 40 + pick(rnd, 70);
                        d.on_exec(Fill(order, exec, qty, px));
                        break;
                    }
                    case 8: d.on_exec(Cancel(1 + pick(rnd, static_cast<unsigned>(next_id)))); break;
                    default: if (pick(rnd, 6) == 0) d.halt(); else d.resume(); break;
                }
            } catch (const std::logic_error&) {
            } catch (const std::overflow_error&) {
            }
        }
        expect_same_state(d, TradingDesk::replay(DESK_LIMITS, d.journal()));
        if (mt::ctx().failed_checks != 0) break;
    }
}

TEST(multiple_symbols_and_sorted_symbol_list, "part4") {
    auto desk = make_desk();
    desk.submit(buy(1, "B", 10, 50));
    desk.submit(buy(2, "A", 10, 100));
    desk.on_exec(Ack(1));
    desk.on_exec(Ack(2));
    desk.on_exec(Fill(1, 1, 10, 50));
    desk.on_exec(Fill(2, 2, 10, 100));
    CHECK_EQ(desk.symbols(), (std::vector<std::string>{"A", "B"}));
    CHECK_EQ(ids(desk.all_orders()), (std::vector<long long>{1, 2}));
}

TEST(two_hundred_thousand_events_replay_fast, "part4,perf") {
    const RiskLimits limits(1'000, LLONG_MAX, 1'000'000'000LL, 1'000'000, 10'000);
    TradingDesk d(limits);
    d.set_reference_price("A", 100);
    CHECK_WITHIN_MS(3000,
        long long exec = 1;
        for (long long id = 1; id <= 50'000; ++id) {
            d.submit(Order(id, "A", id % 2 == 0 ? Side::Buy : Side::Sell, 10, 100));
            d.on_exec(Ack(id));
            d.on_exec(Fill(id, exec++, 4, 100));
            d.on_exec(Fill(id, exec++, 6, 100));
        }
        const auto copy = TradingDesk::replay(limits, d.journal());
        CHECK_EQ(d.position("A"), copy.position("A")););
}

// ---- C++-only, Part 4

TEST(a_desk_copy_is_an_independent_snapshot, "part4,cpp") {
    // Java shares the object reference; C++ copies the value.  The whole desk (orders, positions, risk state, journal) is plain
    // members, so the defaulted copy is a complete, independent what-if sandbox.
    auto desk = make_desk();
    desk.submit(buy(1, "A", 100, 100));
    desk.on_exec(Ack(1));
    TradingDesk what_if = desk;
    what_if.on_exec(Fill(1, 1, 100, 100));
    what_if.halt();
    CHECK_EQ(what_if.position("A").net_qty, 100);
    CHECK_EQ(desk.position("A").net_qty, 0);
    CHECK_EQ(desk.order(1).status, WORKING);
    CHECK_EQ(desk.journal().size(), what_if.journal().size() - 2);
    CHECK_EQ(desk.submit(buy(2, "A", 1, 100)), RiskResult::accepted());  // the original was not halted
}

TEST(replay_only_swallows_the_desks_own_error_types, "part4,cpp") {
    // replay catches std::logic_error and std::overflow_error - the types the desk's inputs can raise - and nothing wider: a
    // catch (...) would also hide std::bad_alloc or a bug that throws something unrelated.
    static_assert(std::is_base_of_v<std::logic_error, IllegalTransitionException>);
    static_assert(std::is_base_of_v<std::logic_error, std::out_of_range> && std::is_base_of_v<std::logic_error, std::invalid_argument>);
    static_assert(!std::is_base_of_v<std::logic_error, std::overflow_error>);
    CHECK_THROWS_AS(mul_exact(LLONG_MAX, 2), std::overflow_error);
    CHECK_THROWS_AS(add_exact(LLONG_MAX, 1), std::overflow_error);
    CHECK_THROWS_AS(sub_exact(LLONG_MIN, 1), std::overflow_error);
    CHECK_EQ(mul_exact(3'000'000'000LL, 3), 9'000'000'000LL);
}

TEST(exec_events_convert_to_desk_events, "part4,cpp") {
    // A variant cannot extend another variant (Java: ExecEvent extends DeskEvent), so the conversion is explicit and total.
    const ExecEvent events[] = {Ack(1), Fill(1, 2, 3, 4), Cancel(5), Reject(6, "r")};
    for (const auto& e : events) {
        const DeskEvent d = to_desk_event(e);
        CHECK_EQ(d.index(), e.index() + 4);  // Ack..Reject are alternatives 4..7 of DeskEvent and 0..3 of ExecEvent
    }
}

MT_MAIN()
