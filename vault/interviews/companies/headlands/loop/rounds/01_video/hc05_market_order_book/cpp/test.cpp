// hc05 · Market order book — C++20 tests.  Same cases as test/OrderBookTest.java and TickBookTest.java plus C++-only edge
// cases (tag "cpp"): a slow brute-force model for differential testing, move-only book, strict from_chars parsing, chars >= 0x80,
// 64-bit values narrowed to int, qty_at truncation, allocation counts (std::map/std::list vs the preallocated TickBook).
#include <algorithm>
#include <array>
#include <atomic>
#include <climits>
#include <cstdlib>
#include <iostream>
#include <map>
#include <new>
#include <random>
#include <type_traits>
#include <unordered_set>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace book;

// ---------------------------------------------------------------- global allocation counter (test infrastructure)
namespace {
std::atomic<std::size_t> g_news{0};
struct AllocCount {
    std::size_t start = g_news.load();
    std::size_t get() const { return g_news.load() - start; }
};
}  // namespace
void* operator new(std::size_t n) {
    g_news.fetch_add(1, std::memory_order_relaxed);
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

// ---------------------------------------------------------------- printing for failure messages
namespace book {
std::ostream& operator<<(std::ostream& os, const Level& l) { return os << "Level(" << l.price << "," << l.total_qty << "," << l.order_count << ")"; }
std::ostream& operator<<(std::ostream& os, const Order& o) { return os << "Order(" << o.id << "," << name(o.side) << "," << o.price << "," << o.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Limit& c) { return os << "Limit(" << c.id << "," << name(c.side) << "," << c.price << "," << c.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Market& c) { return os << "Market(" << c.id << "," << name(c.side) << "," << c.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Cancel& c) { return os << "Cancel(" << c.id << ")"; }
std::ostream& operator<<(std::ostream& os, const Modify& c) { return os << "Modify(" << c.id << "," << c.new_qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Trade& t) { return os << "Trade(taker=" << t.taker_id << ",maker=" << t.maker_id << "," << name(t.taker_side) << "," << t.price << "," << t.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Rested& r) { return os << "Rested(" << r.id << "," << name(r.side) << "," << r.price << "," << r.qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Cancelled& c) { return os << "Cancelled(" << c.id << "," << c.remaining << ")"; }
std::ostream& operator<<(std::ostream& os, const Modified& m) { return os << "Modified(" << m.id << "," << m.old_qty << "," << m.new_qty << ")"; }
std::ostream& operator<<(std::ostream& os, const Rejected& r) { return os << "Rejected(" << r.id << "," << r.reason << ")"; }
}  // namespace book

namespace {

using Rng = std::mt19937_64;
constexpr Side BUY = Side::Buy;
constexpr Side SELL = Side::Sell;
using Events = std::vector<Event>;
using Levels = std::vector<Level>;

Events E(std::initializer_list<Event> l) { return Events(l); }
Command lim(long long id, Side s, long long px, long long q) { return Limit{id, s, px, q}; }
std::vector<std::string> lines_of(const std::string& block) {
    std::vector<std::string> out;
    std::size_t pos = 0;
    while (pos < block.size()) {
        std::size_t nl = block.find('\n', pos);
        if (nl == std::string::npos) nl = block.size();
        out.push_back(block.substr(pos, nl - pos));
        pos = nl + 1;
    }
    return out;
}
template <class E, class F>
std::optional<E> thrown(F&& f) {
    try {
        f();
    } catch (const E& e) {
        return e;
    } catch (...) {
    }
    return std::nullopt;
}
long long total_resting(const OrderBook& b) {
    long long sum = 0;
    for (Side s : {BUY, SELL})
        for (const Level& l : b.depth(s, INT_MAX)) sum += l.total_qty;
    return sum;
}

/// Brute force: a flat vector of orders, every match is a linear scan.  Obviously right, hopelessly slow.
class SlowBook {
public:
    Events execute(const Command& c) {
        if (const auto* l = std::get_if<Limit>(&c)) {
            if (auto bad = check(l->id, l->price, l->qty, true)) return {Rejected{l->id, *bad}};
            if (live(l->id)) return {Rejected{l->id, DUPLICATE_ID}};
            Events ev;
            const long long left = match(l->id, l->side, l->price, l->qty, ev);
            if (left > 0) {
                orders_.push_back({l->id, l->side, l->price, left, seq_++});
                ev.push_back(Rested{l->id, l->side, l->price, left});
            }
            return ev;
        }
        if (const auto* m = std::get_if<Market>(&c)) {
            if (auto bad = check(m->id, 1, m->qty, false)) return {Rejected{m->id, *bad}};
            if (live(m->id)) return {Rejected{m->id, DUPLICATE_ID}};
            Events ev;
            const long long left = match(m->id, m->side, m->side == BUY ? LLONG_MAX : 0, m->qty, ev);
            if (left > 0) ev.push_back(Cancelled{m->id, left});
            return ev;
        }
        if (const auto* x = std::get_if<Cancel>(&c)) {
            if (x->id <= 0) return {Rejected{x->id, INVALID_ID}};
            auto it = find(x->id);
            if (it == orders_.end()) return {Rejected{x->id, UNKNOWN_ID}};
            const long long left = it->qty;
            orders_.erase(it);
            return {Cancelled{x->id, left}};
        }
        const auto& m = std::get<Modify>(c);
        if (m.id <= 0) return {Rejected{m.id, INVALID_ID}};
        if (m.new_qty <= 0) return {Rejected{m.id, INVALID_QTY}};
        auto it = find(m.id);
        if (it == orders_.end()) return {Rejected{m.id, UNKNOWN_ID}};
        const long long old = it->qty;
        if (m.new_qty > old) it->seq = seq_++;  // a larger order goes to the back of the queue
        it->qty = m.new_qty;
        return {Modified{m.id, old, m.new_qty}};
    }
    std::optional<long long> best(Side s) const {
        std::optional<long long> r;
        for (const auto& o : orders_)
            if (o.side == s && (!r || (s == BUY ? o.price > *r : o.price < *r))) r = o.price;
        return r;
    }
    Levels depth(Side s) const {
        std::map<long long, std::pair<long long, int>> m;
        for (const auto& o : orders_)
            if (o.side == s) { m[o.price].first += o.qty; ++m[o.price].second; }
        Levels out;
        for (const auto& [px, v] : m) out.push_back({px, v.first, v.second});
        if (s == BUY) std::reverse(out.begin(), out.end());
        return out;
    }
    std::size_t size() const { return orders_.size(); }

private:
    struct O {
        long long id;
        Side side;
        long long price, qty, seq;
    };
    static std::optional<std::string_view> check(long long id, long long price, long long qty, bool with_price) {
        if (id <= 0) return INVALID_ID;
        if (with_price && price <= 0) return INVALID_PRICE;
        if (qty <= 0) return INVALID_QTY;
        return std::nullopt;
    }
    bool live(long long id) const { return std::any_of(orders_.begin(), orders_.end(), [&](const O& o) { return o.id == id; }); }
    std::vector<O>::iterator find(long long id) {
        return std::find_if(orders_.begin(), orders_.end(), [&](const O& o) { return o.id == id; });
    }
    long long match(long long taker, Side side, long long limit, long long qty, Events& ev) {
        long long left = qty;
        while (left > 0) {
            std::optional<std::size_t> best;
            for (std::size_t i = 0; i < orders_.size(); ++i) {
                const O& o = orders_[i];
                if (o.side == side) continue;
                if (side == BUY ? o.price > limit : o.price < limit) continue;
                if (!best) { best = i; continue; }
                const O& b = orders_[*best];
                const bool better = o.price != b.price ? (side == BUY ? o.price < b.price : o.price > b.price) : o.seq < b.seq;
                if (better) best = i;
            }
            if (!best) break;
            O& m = orders_[*best];
            const long long fill = std::min(left, m.qty);
            ev.push_back(Trade{taker, m.id, side, m.price, fill});
            left -= fill;
            m.qty -= fill;
            if (m.qty == 0) orders_.erase(orders_.begin() + static_cast<std::ptrdiff_t>(*best));
        }
        return left;
    }
    std::vector<O> orders_;
    long long seq_ = 0;
};

}  // namespace

// ===================================================================================== Part 1: maintenance

TEST(empty_book, "part1,edge") {
    OrderBook b;
    CHECK_EQ(b.best_bid(), std::nullopt);
    CHECK_EQ(b.best_ask(), std::nullopt);
    CHECK_EQ(b.depth(BUY, 5), Levels{});
    CHECK_EQ(b.queue(SELL, 100), std::vector<long long>{});
    CHECK_EQ(b.size(), 0u);
    CHECK(!b.cancel(1));
    CHECK(!b.modify(1, 5));
}

TEST(best_bid_is_highest_best_ask_is_lowest, "part1") {
    OrderBook b;
    b.add(1, BUY, 100, 5);
    b.add(2, BUY, 101, 5);
    b.add(3, BUY, 99, 5);
    b.add(4, SELL, 103, 5);
    b.add(5, SELL, 102, 5);
    CHECK_EQ(b.best_bid(), std::optional<long long>(101));
    CHECK_EQ(b.best_ask(), std::optional<long long>(102));
    CHECK_EQ(b.size(), 5u);
}

TEST(depth_aggregates_and_orders_best_first, "part1") {
    OrderBook b;
    b.add(1, BUY, 100, 5);
    b.add(2, BUY, 99, 3);
    b.add(3, BUY, 100, 7);
    b.add(4, SELL, 102, 1);
    b.add(5, SELL, 101, 2);
    b.add(6, SELL, 101, 4);
    const Levels bids{{100, 12, 2}, {99, 3, 1}}, top_bid{{100, 12, 2}}, asks{{101, 6, 2}, {102, 1, 1}};
    CHECK_EQ(b.depth(BUY, 10), bids);
    CHECK_EQ(b.depth(BUY, 1), top_bid);
    CHECK_EQ(b.depth(SELL, 2), asks);
    CHECK_EQ(b.depth(SELL, 0), Levels{});
    CHECK_THROWS_AS(b.depth(BUY, -1), std::invalid_argument);
}

TEST(same_price_is_fifo, "part1") {
    OrderBook b;
    b.add(7, SELL, 50, 1);
    b.add(3, SELL, 50, 1);
    b.add(9, SELL, 50, 1);
    CHECK_EQ(b.queue(SELL, 50), (std::vector<long long>{7, 3, 9}));
}

TEST(cancel_removes_and_best_moves, "part1") {
    OrderBook b;
    b.add(1, BUY, 100, 5);
    b.add(2, BUY, 100, 6);
    b.add(3, BUY, 100, 7);
    b.add(4, BUY, 99, 1);
    CHECK(b.cancel(2));
    CHECK_EQ(b.queue(BUY, 100), (std::vector<long long>{1, 3}));
    CHECK_EQ(b.depth(BUY, 1).front(), (Level{100, 12, 2}));
    CHECK(!b.cancel(2));
    CHECK(b.cancel(1));
    CHECK(b.cancel(3));
    CHECK_EQ(b.best_bid(), std::optional<long long>(99));
    CHECK_EQ(b.queue(BUY, 100), std::vector<long long>{});
    CHECK_EQ(b.size(), 1u);
}

TEST(modify_down_keeps_priority_modify_up_goes_to_the_back, "part1") {
    OrderBook b;
    b.add(1, BUY, 100, 10);
    b.add(2, BUY, 100, 10);
    b.add(3, BUY, 100, 10);
    CHECK(b.modify(1, 4));  // smaller: keeps the front
    CHECK_EQ(b.queue(BUY, 100), (std::vector<long long>{1, 2, 3}));
    CHECK_EQ(b.find(1)->qty, 4);
    CHECK_EQ(b.depth(BUY, 1).front().total_qty, 24);
    CHECK(b.modify(1, 4));  // equal: nothing changes
    CHECK_EQ(b.queue(BUY, 100), (std::vector<long long>{1, 2, 3}));
    CHECK(b.modify(1, 5));  // larger: loses priority
    CHECK_EQ(b.queue(BUY, 100), (std::vector<long long>{2, 3, 1}));
    CHECK_EQ(b.depth(BUY, 1).front().total_qty, 25);
    CHECK(!b.modify(99, 1));
    CHECK(b.modify(1, 6));  // already last: still fine
    CHECK_EQ(b.queue(BUY, 100), (std::vector<long long>{2, 3, 1}));
}

TEST(modify_rejects_non_positive_quantity, "part1,edge") {
    for (long long q : {0LL, -1LL, LLONG_MIN}) {
        OrderBook b;
        b.add(1, BUY, 100, 10);
        CHECK_THROWS_AS(b.modify(1, q), std::invalid_argument);
        CHECK_THROWS_AS(b.modify(404, q), std::invalid_argument);  // an unknown id still reports the bad argument first
        CHECK_EQ(b.find(1)->qty, 10);
    }
}

TEST(add_validates_and_rejects_duplicates, "part1,edge") {
    OrderBook b;
    CHECK_THROWS_AS(b.add(0, BUY, 100, 1), std::invalid_argument);
    CHECK_THROWS_AS(b.add(-5, BUY, 100, 1), std::invalid_argument);
    CHECK_THROWS_AS(b.add(1, BUY, 0, 1), std::invalid_argument);
    CHECK_THROWS_AS(b.add(1, BUY, -3, 1), std::invalid_argument);
    CHECK_THROWS_AS(b.add(1, BUY, 100, 0), std::invalid_argument);
    auto first = thrown<std::invalid_argument>([&] { b.add(0, BUY, 0, 0); });  // everything wrong: the id is reported
    REQUIRE(first.has_value());
    CHECK_EQ(std::string(first->what()), std::string(INVALID_ID));
    b.add(1, BUY, 100, 1);
    CHECK_THROWS_AS(b.add(1, SELL, 200, 1), std::invalid_argument);  // ids are unique across both sides
    CHECK_EQ(b.size(), 1u);
    b.cancel(1);
    b.add(1, SELL, 200, 1);  // a cancelled id can be reused
    CHECK_EQ(b.best_ask(), std::optional<long long>(200));
}

TEST(huge_prices_and_level_overflow, "part1,edge") {
    OrderBook b;
    b.add(1, BUY, LLONG_MAX, LLONG_MAX - 5);
    CHECK_EQ(b.best_bid(), std::optional<long long>(LLONG_MAX));
    CHECK_THROWS_AS(b.add(2, BUY, LLONG_MAX, 6), std::overflow_error);
    CHECK_EQ(b.size(), 1u);  // the book is unchanged after the exception
    CHECK_EQ(b.depth(BUY, 1).front().total_qty, LLONG_MAX - 5);
    b.add(2, BUY, LLONG_MAX, 5);  // exactly to the top: fine
    CHECK_EQ(b.depth(BUY, 1).front().total_qty, LLONG_MAX);
    CHECK_THROWS_AS(b.modify(2, 6), std::overflow_error);
    CHECK_EQ(b.find(2)->qty, 5);
    CHECK_EQ(b.queue(BUY, LLONG_MAX), (std::vector<long long>{1, 2}));
}

TEST(two_hundred_thousand_adds_and_cancels, "part1,perf") {
    Rng g(0);
    OrderBook b;
    CHECK_WITHIN_MS(2000, for (long long i = 1; i <= 200000; ++i) b.add(i, g() % 2 ? BUY : SELL, 1 + static_cast<long long>(g() % 5000), 1 + static_cast<long long>(g() % 100));
                    for (long long i = 1; i <= 200000; i += 2) b.cancel(i););
    CHECK_EQ(b.size(), 100000u);
}

// ===================================================================================== Part 2: matching and events

TEST(sample_replay_matches_the_problem_statement, "part2,fmt") {
    const auto out = replay(lines_of(R"(# sample
LIMIT 1 SELL 101 5
LIMIT 2 SELL 101 3
LIMIT 3 SELL 102 4

LIMIT 4 BUY 101 6
limit 5 buy 103 10
MARKET 6 SELL 5
CANCEL 3
MODIFY 9 1
)"));
    const auto expected = lines_of(R"(REST id=1 side=SELL px=101 qty=5
REST id=2 side=SELL px=101 qty=3
REST id=3 side=SELL px=102 qty=4
TRADE taker=4 maker=1 side=BUY px=101 qty=5
TRADE taker=4 maker=2 side=BUY px=101 qty=1
TRADE taker=5 maker=2 side=BUY px=101 qty=2
TRADE taker=5 maker=3 side=BUY px=102 qty=4
REST id=5 side=BUY px=103 qty=4
TRADE taker=6 maker=5 side=SELL px=103 qty=4
CANCEL id=6 remaining=1
REJECT id=3 reason=unknown id
REJECT id=9 reason=unknown id
)");
    CHECK_EQ(out, expected);
}

TEST(better_price_beats_earlier_arrival, "part2") {
    OrderBook b;
    b.execute(lim(1, SELL, 102, 5));
    b.execute(lim(2, SELL, 101, 5));  // later, but a better price
    CHECK_EQ(b.execute(lim(3, BUY, 110, 5)), E({Trade{3, 2, BUY, 101, 5}}));
    CHECK_EQ(b.best_ask(), std::optional<long long>(102));
}

TEST(same_price_fifo_and_trade_at_the_maker_price, "part2") {
    OrderBook b;
    b.execute(lim(1, BUY, 100, 3));
    b.execute(lim(2, BUY, 100, 3));
    CHECK_EQ(b.execute(lim(3, SELL, 90, 4)), E({Trade{3, 1, SELL, 100, 3}, Trade{3, 2, SELL, 100, 1}}));  // sell at 90, trade at 100
    CHECK_EQ(b.queue(BUY, 100), std::vector<long long>{2});
    CHECK_EQ(b.find(2)->qty, 2);  // the partly filled maker stays at the front with a smaller quantity
}

TEST(partial_fill_rests_the_remainder_and_no_cross_no_trade, "part2") {
    OrderBook b;
    CHECK_EQ(b.execute(lim(1, SELL, 100, 4)), E({Rested{1, SELL, 100, 4}}));
    CHECK_EQ(b.execute(lim(2, BUY, 99, 4)), E({Rested{2, BUY, 99, 4}}));  // 99 < 100: no cross
    CHECK_EQ(b.execute(lim(3, BUY, 100, 10)), E({Trade{3, 1, BUY, 100, 4}, Rested{3, BUY, 100, 6}}));
    CHECK_EQ(b.best_bid(), std::optional<long long>(100));
    CHECK_EQ(b.best_ask(), std::nullopt);
}

TEST(market_orders_sweep_and_expire, "part2") {
    OrderBook b;
    CHECK_EQ(b.execute(Market{1, BUY, 5}), E({Cancelled{1, 5}}));  // empty book
    b.execute(lim(2, SELL, 100, 2));
    b.execute(lim(3, SELL, 105, 2));
    b.execute(lim(4, SELL, 200, 2));
    CHECK_EQ(b.execute(Market{5, BUY, 5}), E({Trade{5, 2, BUY, 100, 2}, Trade{5, 3, BUY, 105, 2}, Trade{5, 4, BUY, 200, 1}}));
    CHECK_EQ(b.find(4)->qty, 1);
    CHECK_EQ(b.execute(Market{6, SELL, 4}), E({Cancelled{6, 4}}));  // no bids
}

TEST(modify_and_cancel_through_execute, "part2") {
    OrderBook b;
    b.execute(lim(1, SELL, 100, 5));
    b.execute(lim(2, SELL, 100, 5));
    CHECK_EQ(b.execute(Modify{1, 8}), E({Modified{1, 5, 8}}));  // larger: now behind order 2
    CHECK_EQ(b.execute(lim(3, BUY, 100, 6)), E({Trade{3, 2, BUY, 100, 5}, Trade{3, 1, BUY, 100, 1}}));
    CHECK_EQ(b.execute(Modify{1, 2}), E({Modified{1, 7, 2}}));
    CHECK_EQ(b.execute(Cancel{1}), E({Cancelled{1, 2}}));
    CHECK_EQ(b.size(), 0u);
}

TEST(rejections_carry_the_reason, "part2,edge") {
    OrderBook b;
    b.execute(lim(1, SELL, 100, 5));
    CHECK_EQ(b.execute(lim(0, BUY, 100, 1)), E({Rejected{0, INVALID_ID}}));
    CHECK_EQ(b.execute(lim(2, BUY, 0, 1)), E({Rejected{2, INVALID_PRICE}}));
    CHECK_EQ(b.execute(lim(2, BUY, 100, 0)), E({Rejected{2, INVALID_QTY}}));
    CHECK_EQ(b.execute(lim(1, BUY, 50, 1)), E({Rejected{1, DUPLICATE_ID}}));
    CHECK_EQ(b.execute(Market{1, BUY, 1}), E({Rejected{1, DUPLICATE_ID}}));
    CHECK_EQ(b.execute(Market{2, BUY, -1}), E({Rejected{2, INVALID_QTY}}));
    CHECK_EQ(b.execute(Cancel{9}), E({Rejected{9, UNKNOWN_ID}}));
    CHECK_EQ(b.execute(Modify{9, 3}), E({Rejected{9, UNKNOWN_ID}}));
    CHECK_EQ(b.execute(Modify{1, 0}), E({Rejected{1, INVALID_QTY}}));
    CHECK_EQ(b.size(), 1u);  // a rejected command changes nothing
    CHECK_EQ(b.find(1)->qty, 5);
}

TEST(overflow_is_rejected_atomically, "part2,edge") {
    OrderBook b;
    b.execute(lim(1, BUY, 100, LLONG_MAX - 1));
    b.execute(lim(2, SELL, 200, 3));
    // buying 2 more at 100 would overflow the 100 level: reject the whole order, and do NOT trade against the 200 ask first
    CHECK_EQ(b.execute(lim(3, BUY, 100, 2)), E({Rejected{3, OVERFLOW_REASON}}));
    CHECK_EQ(b.find(2)->qty, 3);
    CHECK_EQ(b.execute(lim(4, BUY, 100, 1)), E({Rested{4, BUY, 100, 1}}));
    CHECK_EQ(b.execute(Modify{4, 2}), E({Rejected{4, OVERFLOW_REASON}}));
    CHECK_EQ(b.find(4)->qty, 1);
}

TEST(filled_ids_can_be_reused, "part2,edge") {
    OrderBook b;
    b.execute(lim(1, SELL, 100, 1));
    b.execute(lim(2, BUY, 100, 1));  // both are filled
    CHECK_EQ(b.execute(lim(1, BUY, 90, 1)), E({Rested{1, BUY, 90, 1}}));
}

TEST(parse_rejects_malformed_lines, "part2,fmt") {
    for (const char* bad : {"", "   ", "BOGUS 1", "LIMIT 1 BUY 100", "LIMIT 1 BUY 100 5 7", "LIMIT 1 HOLD 100 5", "LIMIT x BUY 100 5",
                            "LIMIT 1 BUY 1.5 5", "MARKET 1 BUY", "CANCEL", "CANCEL 1 2", "MODIFY 1", "LIMIT 99999999999999999999 BUY 1 1"})
        CHECK_THROWS_AS(parse(bad), std::invalid_argument, bad);
}

TEST(parse_and_render_every_kind, "part2,fmt") {
    CHECK(parse("  LIMIT   1 buy 100 5 ") == Command(Limit{1, BUY, 100, 5}));
    CHECK(parse("Market 2 SELL 7") == Command(Market{2, SELL, 7}));
    CHECK(parse("CANCEL 3") == Command(Cancel{3}));
    CHECK(parse("MODIFY 4 9") == Command(Modify{4, 9}));
    CHECK_EQ(render(Trade{3, 1, SELL, 100, 3}), std::string("TRADE taker=3 maker=1 side=SELL px=100 qty=3"));
    CHECK_EQ(render(Rested{1, BUY, 7, 2}), std::string("REST id=1 side=BUY px=7 qty=2"));
    CHECK_EQ(render(Cancelled{1, 2}), std::string("CANCEL id=1 remaining=2"));
    CHECK_EQ(render(Modified{1, 5, 3}), std::string("MODIFY id=1 old=5 new=3"));
    CHECK_EQ(render(Rejected{1, DUPLICATE_ID}), std::string("REJECT id=1 reason=duplicate id"));
}

TEST(replay_reports_the_offending_line, "part2,fmt") {
    auto ex = thrown<std::invalid_argument>([&] { replay({"LIMIT 1 BUY 100 5", "", "LIMIT 2 BUY oops 5"}); });
    REQUIRE(ex.has_value());
    CHECK(std::string(ex->what()).starts_with("line 3"), ex->what());
}

TEST(parse_is_strict_about_numbers, "part2,fmt,cpp") {
    for (const char* bad : {"LIMIT 1 BUY +5 1", "LIMIT 1 BUY 100 5x", "LIMIT 1 BUY 0x10 5", "LIMIT 1 BUY 1e3 5", "CANCEL 1_000", "MODIFY 1 -"})
        CHECK_THROWS_AS(parse(bad), std::invalid_argument, bad);
    CHECK(parse("CANCEL -7") == Command(Cancel{-7}));  // a valid number: the book rejects the id, not the parser
    CHECK(parse("LIMIT 1 BUY 100 5\t\r") == Command(Limit{1, BUY, 100, 5}));
    CHECK(parse("LIMIT 007 BUY 0100 5") == Command(Limit{7, BUY, 100, 5}));
}

TEST(parse_survives_bytes_above_127, "part2,fmt,cpp") {
    // toupper/tolower on a negative `char` is undefined behaviour; the parser must convert through unsigned char first
    CHECK_THROWS_AS(parse("L\xC3\x89MIT 1 BUY 1 1"), std::invalid_argument);
    CHECK_THROWS_AS(parse("LIMIT 1 B\xFFY 1 1"), std::invalid_argument);
}

TEST(random_flow_keeps_the_invariants, "part2,edge") {
    Rng g(0);
    OrderBook b;
    long long submitted = 0, traded = 0, cancelled = 0, next_id = 1;
    for (int step = 0; step < 20000; ++step) {
        const int dice = static_cast<int>(g() % 10);
        Events ev;
        if (dice < 6) {
            const long long q = 1 + static_cast<long long>(g() % 20);
            submitted += q;
            ev = b.execute(lim(next_id++, g() % 2 ? BUY : SELL, 95 + static_cast<long long>(g() % 11), q));
        } else if (dice < 7) {
            const long long q = 1 + static_cast<long long>(g() % 30);
            submitted += q;
            ev = b.execute(Market{next_id++, g() % 2 ? BUY : SELL, q});
        } else {
            ev = b.execute(Cancel{1 + static_cast<long long>(g() % static_cast<unsigned long long>(next_id))});
        }
        for (const Event& e : ev) {
            if (const auto* t = std::get_if<Trade>(&e)) traded += t->qty;
            if (const auto* c = std::get_if<Cancelled>(&e)) cancelled += c->remaining;
        }
        if (b.best_bid() && b.best_ask()) CHECK_LT(*b.best_bid(), *b.best_ask(), "crossed at step " + std::to_string(step));
    }
    CHECK_EQ(submitted, 2 * traded + total_resting(b) + cancelled);  // every unit is traded (twice), resting, or void
    CHECK_GT(traded, 0);
}

TEST(differential_against_a_brute_force_model, "part2,edge,cpp") {
    for (unsigned seed = 1; seed <= 6; ++seed) {
        Rng g(seed);
        OrderBook fast;
        SlowBook slow;
        for (int step = 0; step < 5000; ++step) {
            const long long id = 1 + static_cast<long long>(g() % 120);  // few ids: duplicates, unknown ids and reuse happen a lot
            const Side side = g() % 2 ? BUY : SELL;
            const long long px = 96 + static_cast<long long>(g() % 9), q = 1 + static_cast<long long>(g() % 12);
            Command c = Cancel{id};
            switch (g() % 8) {
                case 0: case 1: case 2: c = Limit{id, side, px, q}; break;
                case 3: c = Market{id, side, q}; break;
                case 4: case 5: c = Modify{id, static_cast<long long>(g() % 14) - 1}; break;
                default: c = Cancel{id};
            }
            const Events a = fast.execute(c), b = slow.execute(c);
            CHECK(a == b, "step " + std::to_string(step));
            if (a != b) break;
            CHECK_EQ(fast.best_bid(), slow.best(BUY));
            CHECK_EQ(fast.best_ask(), slow.best(SELL));
            CHECK_EQ(fast.size(), slow.size());
            if (step % 50 == 0) {
                CHECK_EQ(fast.depth(BUY, INT_MAX), slow.depth(BUY));
                CHECK_EQ(fast.depth(SELL, INT_MAX), slow.depth(SELL));
            }
        }
    }
}

TEST(a_book_is_move_only_and_a_moved_book_still_works, "part2,cpp") {
    static_assert(!std::is_copy_constructible_v<OrderBook>);  // the id index holds iterators into THIS book's containers
    static_assert(!std::is_copy_assignable_v<OrderBook>);
    static_assert(std::is_nothrow_move_constructible_v<OrderBook>);
    OrderBook a;
    for (long long i = 1; i <= 50; ++i) a.add(i, i % 2 ? BUY : SELL, 100 + i % 7, i);
    OrderBook b = std::move(a);
    CHECK_EQ(b.size(), 50u);
    CHECK(b.cancel(10));  // follows a stored iterator into the moved containers (ASan/UBSan would flag a dangling one)
    CHECK(b.modify(11, 99));
    const Events swept = b.execute(lim(100, BUY, 200, 5));  // sweeps the cheapest asks through the moved containers
    CHECK(!swept.empty() && std::holds_alternative<Trade>(swept.front()));
    OrderBook c;
    c = std::move(b);
    CHECK(c.cancel(11));
    CHECK_EQ(a.size(), 0u);
}

TEST(rejection_reasons_are_static_text_not_dangling, "part2,cpp") {
    Events ev;
    {
        OrderBook b;
        ev = b.execute(Cancel{5});
    }  // the book is gone; the reason is a string_view into static storage
    CHECK_EQ(render(ev.front()), std::string("REJECT id=5 reason=unknown id"));
}

TEST(three_hundred_thousand_commands_under_two_seconds, "part2,perf") {
    Rng g(0);
    std::vector<Command> cmds;
    for (long long i = 1; i <= 300000; ++i) {
        const auto dice = g() % 10;
        if (dice < 7) cmds.push_back(lim(i, g() % 2 ? BUY : SELL, 9900 + static_cast<long long>(g() % 201), 1 + static_cast<long long>(g() % 50)));
        else if (dice < 9) cmds.push_back(Cancel{1 + static_cast<long long>(g() % static_cast<unsigned long long>(i))});
        else cmds.push_back(Modify{1 + static_cast<long long>(g() % static_cast<unsigned long long>(i)), 1 + static_cast<long long>(g() % 50)});
    }
    OrderBook b;
    Events events;
    CHECK_WITHIN_MS(2000, events = b.execute_all(cmds););
    CHECK_GE(events.size(), 150000u);
}

// ===================================================================================== Part 3: batch matching

TEST(batch_sample, "part3") {
    const Summary s = run_batch({{0, 100, 5}, {1, 99, 3}, {1, 100, 4}, {0, 101, 10}});
    const std::vector<Trade> trades{{2, 1, SELL, 100, 3}, {3, 1, SELL, 100, 2}, {4, 3, BUY, 100, 2}};
    const Levels bids{{101, 8, 1}};
    CHECK_EQ(s.trades, trades);
    CHECK_EQ(s.filled_qty, 7);
    CHECK_EQ(s.notional, 700);
    CHECK_EQ(s.bids, bids);
    CHECK_EQ(s.asks, Levels{});
}

TEST(batch_empty_and_no_cross, "part3,edge") {
    const Summary empty = run_batch({});
    const Summary none{{}, 0, 0, {}, {}};
    CHECK(empty == none);
    const Summary t = run_batch({{0, 10, 1}, {1, 11, 1}});
    const Levels bids{{10, 1, 1}}, asks{{11, 1, 1}};
    CHECK_EQ(t.trades, std::vector<Trade>{});
    CHECK_EQ(t.bids, bids);
    CHECK_EQ(t.asks, asks);
}

TEST(batch_sweeps_several_levels_in_price_order, "part3,edge") {
    const Summary s = run_batch({{1, 103, 2}, {1, 101, 2}, {1, 102, 2}, {0, 105, 5}});
    const std::vector<Trade> trades{{4, 2, BUY, 101, 2}, {4, 3, BUY, 102, 2}, {4, 1, BUY, 103, 1}};
    const Levels asks{{103, 1, 1}};
    CHECK_EQ(s.trades, trades);
    CHECK_EQ(s.filled_qty, 5);
    CHECK_EQ(s.notional, 2 * 101 + 2 * 102 + 103);
    CHECK_EQ(s.asks, asks);
}

TEST(batch_rejects_bad_rows, "part3,edge") {
    for (const std::vector<long long>& row : {std::vector<long long>{2, 100, 1}, {-1, 100, 1}, {0, 0, 1}, {0, -5, 1}, {0, 100, 0}, {0, 100, -3}}) {
        const std::vector<std::vector<long long>> rows{{0, 1, 1}, row};
        auto ex = thrown<std::invalid_argument>([&] { run_batch(rows); });
        REQUIRE(ex.has_value());
        CHECK(std::string(ex->what()).starts_with("row 1"), ex->what());
    }
}

TEST(batch_rejects_wrong_arity, "part3,edge") {
    const std::vector<std::vector<long long>> short_row{{0, 1}}, long_row{{0, 1, 1, 1}}, empty_row{{}};
    CHECK_THROWS_AS(run_batch(short_row), std::invalid_argument);
    CHECK_THROWS_AS(run_batch(long_row), std::invalid_argument);
    CHECK_THROWS_AS(run_batch(empty_row), std::invalid_argument);
}

TEST(batch_notional_overflow_is_detected, "part3,edge") {
    const long long b3 = 3'000'000'000LL, b4 = 4'000'000'000LL;
    const Summary ok = run_batch({{0, b3, b3}, {1, b3, b3}});
    CHECK_EQ(ok.notional, 9'000'000'000'000'000'000LL);  // 9e18 < 9.22e18
    CHECK_THROWS_AS(run_batch({{0, b4, b3}, {1, b4, b3}}), std::overflow_error);                      // one trade: 1.2e19
    CHECK_THROWS_AS(run_batch({{0, b3, b3}, {1, b3, b3}, {0, b3, b3}, {1, b3, b3}}), std::overflow_error);  // two trades of 9e18
}

TEST(batch_of_two_hundred_thousand_rows, "part3,perf") {
    Rng g(0);
    std::vector<std::vector<long long>> rows(200000);
    for (auto& r : rows) r = {static_cast<long long>(g() % 2), 9900 + static_cast<long long>(g() % 201), 1 + static_cast<long long>(g() % 100)};
    Summary s;
    CHECK_WITHIN_MS(2000, s = run_batch(rows););
    long long buy = 0, sell = 0;
    for (const auto& r : rows) (r[0] == 0 ? buy : sell) += r[2];
    long long rest_bid = 0, rest_ask = 0;
    for (const Level& l : s.bids) rest_bid += l.total_qty;
    for (const Level& l : s.asks) rest_ask += l.total_qty;
    CHECK(s.filled_qty > 0 && s.filled_qty <= std::min(buy, sell));
    CHECK_EQ(buy, s.filled_qty + rest_bid);
    CHECK_EQ(sell, s.filled_qty + rest_ask);
    CHECK(s.bids.empty() || s.asks.empty() || s.bids.front().price < s.asks.front().price);
}

// ===================================================================================== Part 4: TickBook

namespace {
struct Tape {
    std::vector<std::array<long long, 4>> trades;
    void operator()(long long taker, long long maker, long long price, long long qty) { trades.push_back({taker, maker, price, qty}); }
};
using TradeList = std::vector<std::array<long long, 4>>;
struct Counter {
    long long count = 0, qty = 0;
    void operator()(long long, long long, long long, long long q) { ++count; qty += q; }
};
}  // namespace

TEST(tick_rests_and_reports_best_and_level_quantity, "part4") {
    TickBook b(1000, 16);
    Tape t;
    CHECK_EQ(b.best_bid(), TickBook::NONE);
    CHECK_EQ(b.best_ask(), TickBook::NONE);
    CHECK_EQ(b.limit(1, BUY, 100, 5, t), 5);
    CHECK_EQ(b.limit(2, BUY, 100, 3, t), 3);
    CHECK_EQ(b.limit(3, BUY, 98, 2, t), 2);
    CHECK_EQ(b.limit(4, SELL, 105, 4, t), 4);
    CHECK_EQ(b.best_bid(), 100);
    CHECK_EQ(b.best_ask(), 105);
    CHECK_EQ(b.qty_at(BUY, 100), 8);
    CHECK_EQ(b.qty_at(BUY, 101), 0);
    CHECK_EQ(b.qty_at(SELL, 5000), 0);  // outside the band: 0, not an out-of-bounds read
    CHECK_EQ(b.live_orders(), 4);
    CHECK(t.trades.empty());
}

TEST(tick_matches_with_price_time_priority_like_the_event_book, "part4") {
    TickBook b(1000, 16);
    Tape t;
    b.limit(1, SELL, 101, 5, t);
    b.limit(2, SELL, 101, 3, t);
    b.limit(3, SELL, 102, 4, t);
    CHECK_EQ(b.limit(4, BUY, 101, 6, t), 0);
    CHECK_EQ(b.limit(5, BUY, 103, 10, t), 4);  // eats 2 + 4, rests 4
    const TradeList expected{{4, 1, 101, 5}, {4, 2, 101, 1}, {5, 2, 101, 2}, {5, 3, 102, 4}};
    CHECK_EQ(t.trades, expected);
    CHECK_EQ(b.best_bid(), 103);
    CHECK_EQ(b.best_ask(), TickBook::NONE);
    CHECK_EQ(b.live_orders(), 1);
}

TEST(tick_cancel_finds_the_next_best_across_empty_words, "part4") {
    TickBook b(100000, 16);
    Tape t;
    b.limit(1, BUY, 10, 1, t);
    b.limit(2, BUY, 90000, 1, t);
    b.limit(3, SELL, 99999, 1, t);
    b.limit(4, SELL, 95000, 1, t);
    CHECK_EQ(b.best_bid(), 90000);
    CHECK_EQ(b.best_ask(), 95000);
    CHECK(b.cancel(2));
    CHECK_EQ(b.best_bid(), 10);  // across ten thousand empty levels
    CHECK(b.cancel(4));
    CHECK_EQ(b.best_ask(), 99999);
    CHECK(b.cancel(1));
    CHECK(b.cancel(3));
    CHECK_EQ(b.best_bid(), TickBook::NONE);
    CHECK_EQ(b.best_ask(), TickBook::NONE);
    CHECK(!b.cancel(1));
    CHECK_EQ(b.live_orders(), 0);
}

TEST(tick_rejects_invalid_and_duplicate, "part4,edge") {
    TickBook b(1000, 4);
    Tape t;
    CHECK_EQ(b.limit(0, BUY, 100, 1, t), TickBook::REJECTED);
    CHECK_EQ(b.limit(-1, BUY, 100, 1, t), TickBook::REJECTED);
    CHECK_EQ(b.limit(1, BUY, 0, 1, t), TickBook::REJECTED);
    CHECK_EQ(b.limit(1, BUY, 1000, 1, t), TickBook::REJECTED);  // the upper bound is exclusive
    CHECK_EQ(b.limit(1, BUY, LLONG_MAX, 1, t), TickBook::REJECTED);
    CHECK_EQ(b.limit(1, BUY, 100, 0, t), TickBook::REJECTED);
    CHECK_EQ(b.limit(1, BUY, 100, TickBook::MAX_QTY + 1, t), TickBook::REJECTED);
    CHECK_EQ(b.limit(1, BUY, 100, TickBook::MAX_QTY, t), TickBook::MAX_QTY);
    CHECK_EQ(b.limit(1, SELL, 500, 1, t), TickBook::REJECTED);  // id 1 is live
    CHECK_EQ(b.limit(2, SELL, 999, 999, t), 999);               // the highest tick of the band is valid
    CHECK_EQ(b.live_orders(), 2);
}

TEST(a_64_bit_price_is_range_checked_before_narrowing, "part4,edge,cpp") {
    TickBook b(1000, 4);
    Tape t;
    const long long wraps_to_5 = (1LL << 32) + 5;  // static_cast<int> of this is 5
    CHECK_EQ(b.limit(1, BUY, wraps_to_5, 1, t), TickBook::REJECTED);
    CHECK_EQ(b.live_orders(), 0);
    CHECK_EQ(b.limit(2, BUY, 5, 7, t), 7);
    CHECK_EQ(b.qty_at(BUY, wraps_to_5), 0);  // not the 7 resting at tick 5
    CHECK_EQ(b.qty_at(BUY, -1), 0);
    CHECK_EQ(b.qty_at(BUY, 5), 7);
}

TEST(tick_constructor_validates, "part4,edge,cpp") {
    CHECK_THROWS_AS(TickBook(1, 10), std::invalid_argument);
    CHECK_THROWS_AS(TickBook(1000, 0), std::invalid_argument);
    CHECK_THROWS_AS(TickBook(1000, (1 << 22) + 1), std::invalid_argument);
    CHECK_THROWS_AS(TickBook(1000, -5), std::invalid_argument);
}

TEST(pool_full_back_pressures_and_recovers, "part4,edge") {
    TickBook b(1000, 3);
    Tape t;
    CHECK_EQ(b.limit(1, BUY, 10, 1, t), 1);
    CHECK_EQ(b.limit(2, BUY, 11, 1, t), 1);
    CHECK_EQ(b.limit(3, BUY, 12, 1, t), 1);
    CHECK_EQ(b.limit(4, SELL, 500, 1, t), TickBook::FULL);
    CHECK_EQ(b.limit(5, SELL, 5, 1, t), TickBook::FULL);  // full: nothing is matched
    CHECK(t.trades.empty());
    CHECK(b.cancel(2));
    CHECK_EQ(b.limit(6, SELL, 5, 2, t), 0);  // takes 12 and 10 and has nothing left over
    CHECK_EQ(t.trades.size(), 2u);
    CHECK_EQ(b.live_orders(), 0);
    for (long long id = 10; id < 13; ++id) CHECK_EQ(b.limit(id, BUY, 7, 1, t), 1);  // the freed records are reused
}

TEST(id_table_survives_heavy_churn, "part4,edge") {
    Rng g(0);
    TickBook b(10000, 1024);
    Tape t;
    std::unordered_set<long long> live;
    long long next_id = 1;
    for (int i = 0; i < 300000; ++i) {
        if (live.size() < 1000 && g() % 100 < 55) {
            const long long id = next_id++ * 4096;  // a stride that is hostile to a weak hash
            CHECK_EQ(b.limit(id, BUY, 1 + static_cast<long long>(g() % 100), 1, t), 1);  // only buys: nothing trades
            live.insert(id);
        } else if (!live.empty()) {
            const long long id = (g() % 2 && next_id > 1) ? (1 + static_cast<long long>(g() % static_cast<unsigned long long>(next_id - 1))) * 4096 : *live.begin();
            CHECK_EQ(live.erase(id) == 1, b.cancel(id));
        }
        CHECK_EQ(static_cast<std::size_t>(b.live_orders()), live.size());
    }
}

TEST(tick_differential_against_the_event_book, "part4,edge") {
    Rng g(0);
    OrderBook ref;
    TickBook fast(200, 100000);
    long long next_id = 1;
    for (int step = 0; step < 50000; ++step) {
        if (g() % 10 < 7) {
            const Side side = g() % 2 ? BUY : SELL;
            const long long px = 90 + static_cast<long long>(g() % 21), q = 1 + static_cast<long long>(g() % 10), id = next_id++;
            Tape tape;
            const long long rest = fast.limit(id, side, px, q, tape);
            TradeList expect;
            long long expect_rest = 0;
            for (const Event& e : ref.execute(Limit{id, side, px, q})) {
                if (const auto* tr = std::get_if<Trade>(&e)) expect.push_back({tr->taker_id, tr->maker_id, tr->price, tr->qty});
                if (const auto* r = std::get_if<Rested>(&e)) expect_rest = r->qty;
            }
            CHECK(tape.trades == expect, "trades at step " + std::to_string(step));
            CHECK_EQ(rest, expect_rest, "rest at step " + std::to_string(step));
        } else {
            const long long id = 1 + static_cast<long long>(g() % static_cast<unsigned long long>(next_id));
            const Events evs = ref.execute(Cancel{id});
            CHECK_EQ(std::holds_alternative<Cancelled>(evs.front()), fast.cancel(id), "cancel at step " + std::to_string(step));
        }
        CHECK_EQ(ref.best_bid().value_or(TickBook::NONE), fast.best_bid(), "bid at step " + std::to_string(step));
        CHECK_EQ(ref.best_ask().value_or(TickBook::NONE), fast.best_ask(), "ask at step " + std::to_string(step));
        CHECK_EQ(ref.size(), static_cast<std::size_t>(fast.live_orders()));
    }
    for (Side s : {BUY, SELL})
        for (const Level& l : ref.depth(s, INT_MAX)) CHECK_EQ(l.total_qty, fast.qty_at(s, l.price));
}

TEST(any_callable_works_as_the_trade_sink, "part4,cpp") {
    TickBook b(100, 8);
    b.limit(1, SELL, 50, 5, [](long long, long long, long long, long long) {});  // a captureless lambda
    long long seen = 0;
    CHECK_EQ(b.limit(2, BUY, 50, 3, [&seen](long long, long long, long long, long long q) { seen += q; }), 0);  // a capturing one
    CHECK_EQ(seen, 3);
    struct Functor {
        long long* total;
        void operator()(long long, long long, long long, long long q) const { *total += q; }
    };
    long long total = 0;
    CHECK_EQ(b.limit(3, BUY, 50, 2, Functor{&total}), 0);  // a function object passed as an rvalue
    CHECK_EQ(total, 2);
    CHECK_EQ(b.live_orders(), 0);
}

namespace {
struct Ops {  // pre-generated operations: the timed loop only reads arrays
    std::size_t n;
    std::vector<std::uint8_t> type;  // 0 = limit, 1 = cancel
    std::vector<std::uint8_t> buy;
    std::vector<int> px, qty;
    std::vector<long long> id;
    Ops(std::size_t count, Rng& g) : n(count), type(count), buy(count), px(count), qty(count), id(count) {
        long long next = 1;
        for (std::size_t i = 0; i < n; ++i) {
            if (g() % 10 < 6 || next == 1) {
                type[i] = 0;
                id[i] = next++;
                buy[i] = g() % 2;
                px[i] = 49950 + static_cast<int>(g() % 101);
                qty[i] = 1 + static_cast<int>(g() % 100);
            } else {
                type[i] = 1;
                id[i] = 1 + static_cast<long long>(g() % static_cast<unsigned long long>(next - 1));
            }
        }
    }
};
template <class Sink>
void apply(TickBook& b, const Ops& o, std::size_t from, std::size_t to, Sink& sink) {
    for (std::size_t i = from; i < to; ++i) {
        if (o.type[i] == 0) b.limit(o.id[i], o.buy[i] ? BUY : SELL, o.px[i], o.qty[i], sink);
        else b.cancel(o.id[i]);
    }
}
}  // namespace

TEST(two_million_operations_under_two_seconds, "part4,perf") {
    Rng g(0);
    const Ops ops(2'000'000, g);
    TickBook b(100000, 1 << 21);
    Counter sink;
    CHECK_WITHIN_MS(2000, apply(b, ops, 0, ops.n, sink););
    CHECK_GT(sink.count, 100000, "should trade a lot");
}

TEST(steady_state_does_not_allocate, "part4,cpp") {
    Rng g(1);
    const Ops ops(1'000'000, g);
    TickBook b(100000, 1 << 20);
    Counter sink;
    const AllocCount a;  // the constructor has already allocated everything
    apply(b, ops, 0, ops.n, sink);
    CHECK_EQ(a.get(), 0u);
}

TEST(the_tree_book_allocates_per_resting_order_the_tick_book_never, "part4,cpp") {
    OrderBook tree;
    const AllocCount a;
    for (long long i = 1; i <= 1000; ++i) tree.add(i, BUY, 1 + i % 50, 1);
    CHECK_GE(a.get(), 1000u);  // at least one list node (and an index node) per order
    TickBook flat(100, 2000);
    Counter sink;
    const AllocCount b;
    for (long long i = 1; i <= 1000; ++i) flat.limit(i, BUY, 1 + i % 50, 1, sink);
    CHECK_EQ(b.get(), 0u);
}

MT_MAIN()
