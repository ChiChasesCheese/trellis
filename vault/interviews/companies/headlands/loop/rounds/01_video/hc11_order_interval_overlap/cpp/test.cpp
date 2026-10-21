// hc11 · Order interval overlap — C++20 tests.  Same cases as test/OrderIntervalsTest.java, OnlineOverlapTest.java and
// IntervalIndexTest.java plus C++-only edge cases (tag "cpp"): the tie rule encoded in a std::variant, strict weak ordering
// of the sort comparator, enum values outside the enumerators, operator[] that inserts on reads, copies of a map-based
// object, end + 1 overflow in closed intervals, binary searches near LLONG_MAX, unknown endpoints that must not half-update.
#include <array>
#include <climits>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <set>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace overlap;

namespace overlap {
std::ostream& operator<<(std::ostream& os, const Peak& p) { return os << "Peak(" << p.count << "@" << p.time << ")"; }
std::ostream& operator<<(std::ostream& os, const Report& r) { return os << "Report{buy=" << r.buy << ", sell=" << r.sell << ", all=" << r.all << "}"; }
}  // namespace overlap

namespace {

constexpr long long LMAX = LLONG_MAX;
constexpr Side BUY = Side::Buy;
constexpr Side SELL = Side::Sell;

Peak pk(int c, long long t) { return Peak{c, t}; }
std::vector<Interval> iv(std::initializer_list<Interval> l) { return std::vector<Interval>(l); }
Place place(long long id, Side s, long long a, long long b) { return Place(id, s, a, b); }
Cancel cancel(long long id, long long t) { return Cancel(id, t); }

/// Brute force: count live orders at every integer time below `horizon`.
Peak brute(const std::vector<Interval>& v, int horizon) {
    int best = 0;
    long long when = 0;
    for (int t = 0; t < horizon; ++t) {
        int live = 0;
        for (const Interval& x : v)
            if (x.start <= t && t < x.end) ++live;
        if (live > best) { best = live; when = t; }
    }
    return {best, when};
}

}  // namespace

// ================================================ Part 1: max overlap

TEST(problem_samples, "part1") {
    CHECK_EQ(max_overlap(iv({{1, 5}, {2, 6}, {4, 8}})), 3);
    CHECK_EQ(peak(iv({{1, 5}, {2, 6}, {4, 8}})), pk(3, 4));
    CHECK_EQ(peak(iv({{0, 10}, {2, 3}, {2, 3}, {5, 7}})), pk(3, 2));
}

TEST(end_before_start_tie_rule_touching_intervals_do_not_overlap, "part1,edge") {
    const auto touching = iv({{1, 3}, {3, 5}});
    CHECK_EQ(max_overlap(touching), 1);
    CHECK_EQ(peak(touching), pk(1, 1));
    CHECK_EQ(max_overlap_inclusive(touching), 2);  // closed [s, e]: same data, different convention, different answer
    CHECK_EQ(max_overlap(iv({{0, 1}, {1, 2}, {2, 3}, {3, 4}})), 1);  // chained hand-offs: never two at once
}

TEST(empty_single_and_identical, "part1,edge") {
    CHECK_EQ(max_overlap(std::vector<Interval>{}), 0);
    CHECK_EQ(peak(std::vector<Interval>{}), pk(0, 0));
    CHECK_EQ(peak(iv({{7, 9}})), pk(1, 7));
    CHECK_EQ(max_overlap(iv({{2, 5}, {2, 5}, {2, 5}, {2, 5}})), 4);
}

TEST(zero_length_intervals_never_live, "part1,edge") {
    CHECK_EQ(max_overlap(iv({{5, 5}})), 0);
    CHECK_EQ(max_overlap(iv({{5, 5}, {0, 10}, {5, 5}})), 1);
    CHECK_EQ(max_overlap_inclusive(iv({{5, 5}, {0, 10}})), 2);  // closed: [5,5] is one live point
}

TEST(unsorted_input_and_input_is_not_modified, "part1,edge") {
    const auto v = iv({{8, 9}, {1, 4}, {3, 6}, {0, 2}, {5, 7}});
    const auto copy = v;
    CHECK_EQ(peak(v), pk(2, 1));
    CHECK(v == copy);
}

TEST(earliest_time_is_reported_when_the_max_repeats, "part1,edge") {
    CHECK_EQ(peak(iv({{1, 3}, {1, 3}, {10, 12}, {10, 12}})), pk(2, 1));
}

TEST(invalid_intervals, "part1,edge") {
    CHECK_THROWS_AS(max_overlap(iv({{5, 4}})), std::invalid_argument);
    CHECK_THROWS_AS(max_overlap(iv({{-1, 4}})), std::invalid_argument);
    CHECK_THROWS_AS(max_overlap_inclusive(iv({{5, 4}})), std::invalid_argument);
    // Java's "row has 3 elements" / "null row" cannot happen: an Interval has exactly two fields.
    static_assert(sizeof(Interval) == 2 * sizeof(long long));
}

TEST(huge_coordinates_never_overflow, "part1,edge") {
    const auto v = iv({{0, LMAX}, {LMAX - 2, LMAX}, {LMAX - 1, LMAX}, {LMAX - 5, LMAX - 1}});
    // t = max-2: {0,max}, {max-2,max}, {max-5,max-1} -> 3 (earliest); t = max-1 also 3
    CHECK_EQ(peak(v), pk(3, LMAX - 2));
    CHECK_EQ(peak_events(v), pk(3, LMAX - 2));
    CHECK_EQ(peak_diff_map(v), pk(3, LMAX - 2));
    CHECK_EQ(max_overlap(iv({{0, LMAX}})), 1);
}

TEST(random_against_brute_force, "part1") {
    for (unsigned seed = 1; seed <= 10; ++seed) {
        std::mt19937 rnd(seed);
        const int n = static_cast<int>(rnd() % 60);
        std::vector<Interval> v;
        for (int i = 0; i < n; ++i) {
            const long long a = static_cast<long long>(rnd() % 40);
            v.push_back({a, a + static_cast<long long>(rnd() % 15)});
        }
        const Peak expect = brute(v, 60);
        CHECK_EQ(peak(v), expect, "two vectors, seed " + std::to_string(seed));
        CHECK_EQ(peak_events(v), expect, "variant events, seed " + std::to_string(seed));
        CHECK_EQ(peak_diff_map(v), expect, "difference map, seed " + std::to_string(seed));
    }
}

TEST(million_intervals_in_under_two_seconds, "part1,perf") {
    const int n = 1'000'000;
    std::mt19937 rnd(0);
    std::vector<Interval> v;
    v.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        const long long a = static_cast<long long>(rnd() % 10'000'000);
        v.push_back({a, a + 1 + static_cast<long long>(rnd() % 1000)});
    }
    CHECK_WITHIN_MS(2000, {
        CHECK_GT(peak(v).count, 50);
        CHECK_EQ(peak_events(v), peak(v));
        CHECK_EQ(peak_diff_map(v), peak(v));
    });
}

// ---- C++-only Part 1

TEST(the_tie_rule_is_the_alternative_order_of_the_variant, "part1,edge,cpp") {
    static_assert(std::is_same_v<std::variant_alternative_t<0, SweepEvent>, Close>);
    static_assert(std::is_same_v<std::variant_alternative_t<1, SweepEvent>, Open>);
    CHECK_EQ(peak_events(iv({{1, 3}, {3, 5}})), pk(1, 1));
    CHECK_EQ(peak_events(iv({{1, 3}, {3, 5}, {3, 4}})), pk(2, 3));
}

TEST(sort_comparators_must_be_strict_weak_orders_with_many_equal_times, "part1,edge,cpp") {
    // 60000 events on only 3 distinct times: a `<=` comparator makes std::sort read out of bounds on equal elements.
    std::mt19937 rnd(9);
    std::vector<Interval> v;
    for (int i = 0; i < 30000; ++i) {
        const long long a = static_cast<long long>(rnd() % 2);
        v.push_back({a, a + 1 + static_cast<long long>(rnd() % 2)});
    }
    CHECK_EQ(peak_events(v), peak(v));
    CHECK_EQ(peak_diff_map(v), peak(v));
}

TEST(closed_intervals_at_llong_max_do_not_compute_end_plus_one, "part1,edge,cpp") {
    // [s, e] -> [s, e + 1) would be signed overflow (UB) at e = LLONG_MAX; the closed sweep compares `end < start` instead.
    CHECK_EQ(max_overlap_inclusive(iv({{LMAX, LMAX}, {0, LMAX}})), 2);
    CHECK_EQ(max_overlap_inclusive(iv({{0, LMAX - 1}, {LMAX, LMAX}})), 1);
}

TEST(difference_map_adds_the_net_delta_of_a_key, "part1,edge,cpp") {
    // key 3 gets -1 (from [1,3)) and +1 (from [3,5)): net 0, the live count never reaches 2 there.
    CHECK_EQ(peak_diff_map(iv({{1, 3}, {3, 5}})), pk(1, 1));
    CHECK_EQ(peak_diff_map(iv({{1, 3}, {3, 5}, {3, 4}})), pk(2, 3));  // net +1 at key 3: 1 -> 2
    CHECK_EQ(peak_diff_map(iv({{4, 4}})), pk(0, 0));
}

// ================================================ Part 2: buy / sell / cancels

namespace {
std::vector<OrderEvent> sample() {
    return {place(1, BUY, 0, 10), place(2, BUY, 2, 8), place(3, SELL, 3, 6), place(4, SELL, 4, 12),
            place(5, BUY, 5, 9),  cancel(2, 6),        cancel(4, 5)};
}
}  // namespace

TEST(problem_sample, "part2") {
    // effective: 1 BUY [0,10)  2 BUY [2,6)  3 SELL [3,6)  4 SELL [4,5)  5 BUY [5,9)
    const Report r = analyze(sample());
    CHECK_EQ(r.buy, pk(3, 5));   // t=5: orders 1, 2, 5
    CHECK_EQ(r.sell, pk(2, 4));  // t=4: orders 3, 4
    CHECK_EQ(r.all, pk(4, 4));   // t=4: 1,2,3,4; t=5: 1,2,3,5 also 4 -> earliest
}

TEST(cancellations_matter, "part2") {
    const auto evs = sample();
    const Report r = analyze(std::span<const OrderEvent>(evs).first(5));  // without the two cancels
    CHECK_EQ(r.all, pk(5, 5));
    CHECK_EQ(r.buy, pk(3, 5));
    CHECK_EQ(r.sell, pk(2, 4));
}

TEST(empty_input_and_one_side_only, "part2,edge") {
    CHECK_EQ(analyze(std::vector<OrderEvent>{}), (Report{pk(0, 0), pk(0, 0), pk(0, 0)}));
    const std::vector<OrderEvent> sells = {place(1, SELL, 3, 9), place(2, SELL, 4, 5)};
    CHECK_EQ(analyze(sells), (Report{pk(0, 0), pk(2, 4), pk(2, 4)}));
}

TEST(cancel_timing_relative_to_the_interval, "part2,edge") {
    // before the start or exactly at it -> never lived; at/after the end -> no effect; in between -> shortened
    for (long long c : {0LL, 4LL, 5LL}) {
        const std::vector<OrderEvent> e = {place(1, BUY, 5, 10), cancel(1, c)};
        CHECK_EQ(analyze(e).all, pk(0, 0), "cancel at " + std::to_string(c));
    }
    const std::vector<OrderEvent> at_end = {place(1, BUY, 5, 10), cancel(1, 10)};
    const std::vector<OrderEvent> after_end = {place(1, BUY, 5, 10), cancel(1, 99)};
    CHECK_EQ(analyze(at_end).all, pk(1, 5));
    CHECK_EQ(analyze(after_end).all, pk(1, 5));
    // A [0,10) cut to [0,5) makes room for B [5,8) -> at most 1
    const std::vector<OrderEvent> handoff = {place(1, BUY, 0, 10), place(2, BUY, 5, 8), cancel(1, 5)};
    CHECK_EQ(analyze(handoff).buy, pk(1, 0));
}

TEST(duplicate_cancels_earliest_wins_and_list_order_does_not_matter, "part2,edge") {
    const std::vector<OrderEvent> e = {cancel(1, 7), cancel(1, 3), cancel(1, 9), place(1, BUY, 0, 10), place(2, BUY, 5, 6)};
    CHECK_EQ(analyze(e).all, pk(1, 0));  // order 1 is really [0,3): it never meets order 2 [5,6)
}

TEST(zero_length_place_is_legal_but_never_live, "part2,edge") {
    const std::vector<OrderEvent> e = {place(1, BUY, 4, 4)};
    CHECK_EQ(analyze(e).all, pk(0, 0));
}

TEST(invalid_events, "part2,edge") {
    const std::vector<OrderEvent> dup = {place(1, BUY, 0, 5), place(1, SELL, 1, 2)};
    const std::vector<OrderEvent> unknown = {cancel(9, 1)};
    CHECK_THROWS_AS(analyze(dup), std::invalid_argument);
    CHECK_THROWS_AS(analyze(unknown), std::invalid_argument);
    CHECK_THROWS_AS(place(1, BUY, 5, 4), std::invalid_argument);
    CHECK_THROWS_AS(place(1, BUY, -1, 4), std::invalid_argument);
    CHECK_THROWS_AS(cancel(1, -1), std::invalid_argument);
}

TEST(huge_times_in_the_batch_version, "part2,edge") {
    const std::vector<OrderEvent> e = {place(1, BUY, 0, LMAX), place(2, SELL, LMAX - 1, LMAX), cancel(1, LMAX - 1)};
    const Report r = analyze(e);
    CHECK_EQ(r.buy, pk(1, 0));
    CHECK_EQ(r.sell, pk(1, LMAX - 1));
    CHECK_EQ(r.all, pk(1, 0));  // order 1 is cancelled at max-1 and order 2 takes over exactly then
}

TEST(random_against_brute_force_per_side, "part2") {
    for (unsigned seed = 51; seed <= 58; ++seed) {
        std::mt19937 rnd(seed);
        const int n = static_cast<int>(rnd() % 50);
        std::vector<OrderEvent> events;
        std::map<long long, Interval> eff;
        std::map<long long, Side> sides;
        for (long long id = 0; id < n; ++id) {
            const Side side = rnd() % 2 ? BUY : SELL;
            const long long a = static_cast<long long>(rnd() % 30), b = a + static_cast<long long>(rnd() % 12);
            events.emplace_back(place(id, side, a, b));
            eff[id] = {a, b};
            sides[id] = side;
        }
        for (int c = 0; c < n / 2; ++c) {
            const long long id = static_cast<long long>(rnd() % static_cast<unsigned>(std::max(1, n)));
            if (!eff.count(id)) continue;
            const long long t = static_cast<long long>(rnd() % 40);
            events.emplace_back(cancel(id, t));
            eff[id].end = std::min(eff[id].end, t);
        }
        std::shuffle(events.begin(), events.end(), rnd);
        std::vector<Interval> buy, sell, all;
        for (const auto& [id, x] : eff) {
            (sides[id] == BUY ? buy : sell).push_back(x);
            all.push_back(x);
        }
        const Report r = analyze(events);
        CHECK_EQ(r.buy, brute(buy, 50), "buy, seed " + std::to_string(seed));
        CHECK_EQ(r.sell, brute(sell, 50), "sell, seed " + std::to_string(seed));
        CHECK_EQ(r.all, brute(all, 50), "all, seed " + std::to_string(seed));
    }
}

TEST(half_a_million_orders_with_cancellations_in_under_two_seconds, "part2,perf") {
    const int n = 500'000;
    std::mt19937 rnd(0);
    std::vector<OrderEvent> events;
    events.reserve(static_cast<std::size_t>(n + n / 2));
    for (int i = 0; i < n; ++i) {
        const long long a = static_cast<long long>(rnd() % 5'000'000);
        events.emplace_back(place(i, rnd() % 2 ? BUY : SELL, a, a + 1 + static_cast<long long>(rnd() % 2000)));
    }
    for (int i = 0; i < n / 2; ++i) events.emplace_back(cancel(static_cast<long long>(rnd() % static_cast<unsigned>(n)), static_cast<long long>(rnd() % 5'000'000)));
    CHECK_WITHIN_MS(2000, {
        const Report r = analyze(events);
        CHECK_GE(r.all.count, std::max(r.buy.count, r.sell.count));
    });
}

// ---- C++-only Part 2

TEST(an_enum_can_hold_values_without_an_enumerator, "part2,edge,cpp") {
    // static_cast<Side>(7) is a legal value of the type and would index past a two-element array of lanes.
    CHECK_THROWS_AS(Place(1, static_cast<Side>(7), 0, 1), std::invalid_argument);
    OnlineOverlap o;
    CHECK_THROWS_AS(o.place(1, static_cast<Side>(2), 0, 1), std::invalid_argument);
    CHECK_EQ(o.now(), 0);
    o.place(1, BUY, 0, 1);  // the failed call registered nothing: id 1 is still free
}

TEST(order_ids_may_be_any_long_long, "part2,edge,cpp") {
    const std::vector<OrderEvent> e = {place(LLONG_MIN, BUY, 0, 5), place(-1, BUY, 1, 5), place(0, SELL, 2, 5), place(LMAX, SELL, 3, 5),
                                       cancel(LLONG_MIN, 4)};
    const Report r = analyze(e);
    CHECK_EQ(r.all, pk(4, 3));
    OnlineOverlap o;
    o.place(LLONG_MIN, BUY, 0, 9);
    CHECK(o.cancel(LLONG_MIN, 3));
}

TEST(analyze_accepts_vectors_arrays_and_subspans, "part2,edge,cpp") {
    const std::array<OrderEvent, 2> arr = {place(1, BUY, 0, 4), place(2, BUY, 2, 6)};
    CHECK_EQ(analyze(arr).buy, pk(2, 2));
    const auto v = sample();
    CHECK_EQ(analyze(std::span<const OrderEvent>(v).subspan(0, 2)).buy, pk(2, 2));
}

// ================================================ Part 3: online

TEST(problem_sample_step_by_step, "part3") {
    // the Part 2 sample, ordered by arrival time, asked as it goes
    OnlineOverlap o;
    o.place(1, BUY, 0, 10);
    CHECK_EQ(o.peak(), pk(1, 0));
    o.place(2, BUY, 2, 8);
    CHECK_EQ(o.peak(), pk(2, 2));
    o.place(3, SELL, 3, 6);
    CHECK_EQ(o.peak(), pk(3, 3));
    o.place(4, SELL, 4, 12);
    CHECK_EQ(o.peak(), pk(4, 4));
    o.place(5, BUY, 5, 9);
    CHECK_EQ(o.peak(), pk(5, 5));  // all five live at t = 5, so far
    CHECK(o.cancel(4, 5));         // cancelled at the same instant: the final count at t=5 is 4
    CHECK_EQ(o.peak(), pk(4, 4));  // retroactive fix: the max 4 is earliest at t=4, not polluted by the transient 5
    CHECK(o.cancel(2, 6));
    CHECK_EQ(o.peak(), pk(4, 4));
    CHECK_EQ(o.peak(BUY), pk(3, 5));
    CHECK_EQ(o.peak(SELL), pk(2, 4));
    CHECK_EQ(o.now(), 6);
    const int expect[] = {1, 1, 2, 3, 4, 4, 2};  // t = 0..6
    for (int t = 0; t <= 6; ++t) CHECK_EQ(o.live_at(t), expect[t], "t=" + std::to_string(t));
    CHECK_EQ(o.live_now(), 2);
    CHECK_EQ(o.live_at(BUY, 1), 1);
    CHECK_EQ(o.live_at(SELL, 4), 2);
}

TEST(same_timestamp_place_then_cancel_does_not_inflate_the_max, "part3,edge") {
    OnlineOverlap o;
    o.place(1, BUY, 5, 9);
    o.place(2, BUY, 5, 9);
    CHECK_EQ(o.max_so_far(), 2);
    CHECK(o.cancel(1, 5));  // order 1 is really [5,5): empty
    CHECK_EQ(o.max_so_far(), 1);
    CHECK_EQ(o.peak(), pk(1, 5));
}

TEST(expiry_is_exclusive_and_folds_lazily, "part3,edge") {
    OnlineOverlap o;
    o.place(1, SELL, 0, 5);
    o.place(2, SELL, 1, 5);
    o.place(3, SELL, 2, 6);
    CHECK_EQ(o.live_now(), 3);
    o.advance_to(4);
    CHECK_EQ(o.live_now(), 3);
    o.advance_to(5);  // orders 1 and 2 end at 5 (exclusive)
    CHECK_EQ(o.live_now(), 1);
    CHECK_EQ(o.live_at(4), 3);
    CHECK_EQ(o.live_at(5), 1);
    o.advance_to(100);
    CHECK_EQ(o.live_now(), 0);
    CHECK_EQ(o.live_at(5), 1);  // history does not change
    CHECK_EQ(o.live_at(6), 0);
    CHECK_EQ(o.peak(), pk(3, 2));
}

TEST(cancel_return_values, "part3,edge") {
    OnlineOverlap o;
    o.place(1, BUY, 0, 5);
    o.place(2, BUY, 1, 100);
    CHECK(o.cancel(2, 3));
    CHECK(!o.cancel(2, 4));  // already cancelled
    CHECK(!o.cancel(1, 5));  // exactly at the planned end: already over
    CHECK(!o.cancel(1, 9));  // after the end
    CHECK_THROWS_AS(o.cancel(99, 10), std::invalid_argument);
    CHECK_EQ(o.live_now(), 0);
}

TEST(zero_length_order_is_registered_but_never_live, "part3,edge") {
    OnlineOverlap o;
    o.place(1, BUY, 3, 3);
    CHECK_EQ(o.live_now(), 0);
    CHECK_EQ(o.peak(), pk(0, 0));
    CHECK(!o.cancel(1, 3));
    CHECK_THROWS_AS(o.place(1, SELL, 4, 9), std::invalid_argument);  // the id is taken
}

TEST(out_of_order_and_invalid_arguments, "part3,edge") {
    OnlineOverlap o;
    o.place(1, BUY, 10, 20);
    CHECK_THROWS_AS(o.place(2, BUY, 9, 12), std::invalid_argument);
    CHECK_THROWS_AS(o.cancel(1, 9), std::invalid_argument);
    CHECK_THROWS_AS(o.advance_to(9), std::invalid_argument);
    CHECK_THROWS_AS(o.place(3, BUY, 12, 11), std::invalid_argument);
    CHECK_THROWS_AS(o.place(3, BUY, -1, 11), std::invalid_argument);
    CHECK_THROWS_AS(o.live_at(11), std::invalid_argument);  // looking ahead is not supported
    CHECK_THROWS_AS(o.live_at(-1), std::invalid_argument);
    CHECK_EQ(o.now(), 10);  // failed calls changed nothing
    CHECK_EQ(o.live_now(), 1);
    o.place(2, SELL, 10, 15);  // same timestamp is fine
    CHECK_EQ(o.peak(), pk(2, 10));
}

TEST(many_orders_ending_at_the_same_instant, "part3,edge") {
    OnlineOverlap o;
    for (int i = 0; i < 1000; ++i) o.place(i, i % 2 == 0 ? BUY : SELL, i / 100, 50);
    CHECK_EQ(o.live_now(), 1000);
    CHECK_EQ(o.live_now(BUY), 500);
    CHECK(o.cancel(0, 20));  // the planned end 50 must lose these two
    CHECK(o.cancel(1, 20));
    o.advance_to(50);
    CHECK_EQ(o.live_now(), 0);
    CHECK_EQ(o.live_at(49), 998);
    CHECK_EQ(o.peak(), pk(1000, 9));
}

TEST(apply_dispatches_the_variant, "part3,edge") {
    OnlineOverlap o;
    CHECK(o.apply(Place(1, BUY, 1, 9)));
    CHECK(o.apply(Cancel(1, 4)));
    CHECK(!o.apply(Cancel(1, 5)));
    CHECK_EQ(o.live_now(), 0);
}

TEST(text_script_drives_the_same_sample, "part3") {
    // P id side start end | C id time
    const char* script[][5] = {{"P", "1", "BUY", "0", "10"}, {"P", "2", "BUY", "2", "8"},  {"P", "3", "SELL", "3", "6"}, {"P", "4", "SELL", "4", "12"},
                               {"P", "5", "BUY", "5", "9"},  {"C", "4", "5", nullptr, nullptr}, {"C", "2", "6", nullptr, nullptr}};
    OnlineOverlap o;
    std::vector<bool> results;
    for (const auto& line : script) {
        if (std::string(line[0]) == "P")
            results.push_back(o.apply(Place(std::stoll(line[1]), std::string(line[2]) == "BUY" ? BUY : SELL, std::stoll(line[3]), std::stoll(line[4]))));
        else
            results.push_back(o.apply(Cancel(std::stoll(line[1]), std::stoll(line[2]))));
    }
    CHECK_EQ(results, (std::vector<bool>(7, true)));
    CHECK_EQ(o.peak(), pk(4, 4));
    CHECK_EQ(o.peak(BUY), pk(3, 5));
    CHECK_EQ(o.peak(SELL), pk(2, 4));
}

TEST(huge_timestamps, "part3,edge") {
    OnlineOverlap o;
    o.place(1, BUY, 0, LMAX);
    o.place(2, SELL, LMAX - 3, LMAX - 1);
    CHECK_EQ(o.peak(), pk(2, LMAX - 3));
    CHECK_EQ(o.live_at(LMAX - 3), 2);
    o.advance_to(LMAX - 1);
    CHECK_EQ(o.live_at(LMAX - 2), 2);  // the 2 recorded at max-3 holds until the step down at max-1
    CHECK_EQ(o.live_now(), 1);
    CHECK_EQ(o.live_at(LMAX - 1), 1);
}

TEST(every_prefix_agrees_with_the_batch_solution, "part3") {
    for (unsigned seed = 61; seed <= 66; ++seed) {
        std::mt19937 rnd(seed);
        std::vector<OrderEvent> feed;
        std::vector<long long> placed;
        long long time = 0, next_id = 0;
        for (int step = 0; step < 220; ++step) {
            time += static_cast<long long>(rnd() % 3);
            if (placed.empty() || rnd() % 3 != 0) {
                const long long id = next_id++;
                placed.push_back(id);
                feed.emplace_back(Place(id, rnd() % 2 ? BUY : SELL, time, time + static_cast<long long>(rnd() % 14)));
            } else {
                feed.emplace_back(Cancel(placed[rnd() % placed.size()], time));
            }
        }
        OnlineOverlap o;
        for (std::size_t i = 0; i < feed.size(); ++i) {
            o.apply(feed[i]);
            const Report batch = analyze(std::span<const OrderEvent>(feed).first(i + 1));
            const std::string where = ", seed " + std::to_string(seed) + " prefix " + std::to_string(i + 1);
            CHECK_EQ(batch.all, o.peak(), "all" + where);
            CHECK_EQ(batch.buy, o.peak(BUY), "buy" + where);
            CHECK_EQ(batch.sell, o.peak(SELL), "sell" + where);
        }
        std::map<long long, Interval> final_eff;
        for (const OrderEvent& e : feed) {
            if (const auto* p = std::get_if<Place>(&e)) final_eff[p->id] = {p->start, p->end};
            else if (const auto* c = std::get_if<Cancel>(&e)) final_eff[c->id].end = std::min(final_eff[c->id].end, c->time);
        }
        for (long long t = 0; t <= o.now(); ++t) {
            int live = 0;
            for (const auto& [id, x] : final_eff)
                if (x.start <= t && t < x.end) ++live;
            CHECK_EQ(live, o.live_at(t), "live_at " + std::to_string(t) + ", seed " + std::to_string(seed));
        }
    }
}

TEST(six_hundred_thousand_events_in_under_two_seconds, "part3,perf") {
    const int n = 600'000;
    std::mt19937 rnd(0);
    CHECK_WITHIN_MS(2000, {
        OnlineOverlap o;
        long long time = 0;
        for (int i = 0; i < n; ++i) {
            time += static_cast<long long>(rnd() % 3);
            o.place(i, (i & 1) == 0 ? BUY : SELL, time, time + 1 + static_cast<long long>(rnd() % 5000));
            if (i % 3 == 2) o.cancel(static_cast<long long>(rnd() % static_cast<unsigned>(i + 1)), time);
            if (i % 1000 == 0) o.live_at(static_cast<long long>(rnd() % static_cast<unsigned long long>(time + 1)));
        }
        CHECK_GT(o.max_so_far(), 100);
    });
}

// ---- C++-only Part 3

TEST(reads_never_grow_the_history, "part3,edge,cpp") {
    // std::map::operator[] on a missing key INSERTS it.  A const read path must use find / upper_bound.
    OnlineOverlap o;
    o.place(1, BUY, 5, 9);
    o.place(2, SELL, 6, 12);
    const std::size_t before = o.history_size();
    for (long long t = 0; t <= o.now(); ++t) {
        (void)o.live_at(t);
        (void)o.live_at(BUY, t);
        (void)o.live_at(SELL, t);
    }
    (void)o.peak();
    (void)o.peak(BUY);
    CHECK_EQ(o.history_size(), before);
}

TEST(live_at_before_the_first_recorded_step_is_zero, "part3,edge,cpp") {
    // upper_bound == begin() means "no step at or before t": prev(begin()) would be undefined behaviour.
    OnlineOverlap o;
    o.place(1, BUY, 5, 9);
    CHECK_EQ(o.live_at(0), 0);
    CHECK_EQ(o.live_at(4), 0);
    CHECK_EQ(o.live_at(5), 1);
    const OnlineOverlap& c = o;
    CHECK_EQ(c.live_at(BUY, 4), 0);
}

TEST(copy_is_deep_and_independent, "part3,edge,cpp") {
    OnlineOverlap a;
    a.place(1, BUY, 0, 10);
    a.place(2, BUY, 1, 10);
    OnlineOverlap b = a;  // maps and the order table are copied by value
    a.cancel(1, 2);
    a.advance_to(50);
    CHECK_EQ(b.live_now(), 2);
    CHECK_EQ(b.now(), 1);
    b.advance_to(10);
    CHECK_EQ(b.live_now(), 0);
    CHECK_EQ(a.peak(), pk(2, 1));
    CHECK_EQ(b.peak(), pk(2, 1));
    b.place(3, SELL, 10, 11);
    CHECK_THROWS_AS(a.cancel(3, 60), std::invalid_argument);  // unknown in the original
}

TEST(draining_the_expiry_map_while_new_ends_keep_arriving, "part3,edge,cpp") {
    // extract(begin()) in a loop must not leave a dangling iterator behind; ASan would catch a use of an erased node.
    OnlineOverlap o;
    long long id = 0;
    for (long long t = 0; t < 400; ++t) {
        o.place(id++, BUY, t, t + 1 + (t % 7));
        o.place(id++, SELL, t, t + 3);
        if (t % 5 == 0) (void)o.cancel(id - 2, t);  // sometimes shorten an order whose end is still queued
    }
    o.advance_to(1000);
    CHECK_EQ(o.live_now(), 0);
    CHECK_GT(o.max_so_far(), 5);
}

// ================================================ Part 4: compression + segment tree

namespace {
int brute_live(const std::vector<Interval>& v, long long t) {
    int c = 0;
    for (const Interval& x : v)
        if (x.start <= t && t < x.end) ++c;
    return c;
}
int brute_max_in(const std::vector<Interval>& v, long long from, long long to) {
    int best = 0;
    for (long long t = from; t < to; ++t) best = std::max(best, brute_live(v, t));
    return best;
}
IntervalIndex index_of(const std::vector<Interval>& v) { return IntervalIndex::of(v); }
IntervalIndex index_from(std::initializer_list<long long> c) {
    const std::vector<long long> v(c);
    return IntervalIndex(std::span<const long long>(v));
}
}  // namespace

TEST(index_problem_sample, "part4") {
    const long long u = 1'000'000'000'000'000LL;  // coordinates of order 10^15: no array indexed by time can exist
    const auto v = iv({{1 * u, 5 * u}, {2 * u, 6 * u}, {4 * u, 8 * u}});
    const auto idx = index_of(v);
    CHECK_EQ(idx.max(), 3);
    CHECK_EQ(idx.coordinate_count(), 6);
    CHECK_EQ(idx.segment_count(), 5);
    CHECK_EQ(idx.live_at(0), 0);
    CHECK_EQ(idx.live_at(1 * u), 1);
    CHECK_EQ(idx.live_at(2 * u + 12'345), 2);
    CHECK_EQ(idx.live_at(4 * u), 3);
    CHECK_EQ(idx.live_at(5 * u), 2);  // [1,5) ends at 5u
    CHECK_EQ(idx.live_at(8 * u - 1), 1);
    CHECK_EQ(idx.live_at(8 * u), 0);
    CHECK_EQ(idx.max_in(5 * u, 100 * u), 2);
    CHECK_EQ(idx.max_in(0, 5 * u), 3);
    CHECK_EQ(idx.max_in(0, 2 * u), 1);
}

TEST(index_max_is_the_same_as_the_sweep_line, "part4,edge") {
    const auto v = iv({{0, 10}, {2, 3}, {2, 3}, {5, 7}});
    CHECK_EQ(IntervalIndex::max_overlap(v), max_overlap(v));
    CHECK_EQ(IntervalIndex::max_overlap(iv({{1, 3}, {3, 5}})), 1);  // half-open: a hand-off is not an overlap
}

TEST(degenerate_indexes, "part4,edge") {
    auto none = index_from({});
    CHECK_EQ(none.max(), 0);
    CHECK_EQ(none.live_at(5), 0);
    CHECK_EQ(none.max_in(0, 100), 0);
    auto one = index_from({7, 7, 7});
    CHECK_EQ(one.coordinate_count(), 1);
    CHECK_EQ(one.segment_count(), 0);
    one.add(7, 7);
    CHECK_EQ(one.max(), 0);
    CHECK_EQ(IntervalIndex::max_overlap(std::vector<Interval>{}), 0);
    CHECK_EQ(IntervalIndex::max_overlap(iv({{4, 4}})), 0);
}

TEST(coordinates_near_llong_max, "part4,edge") {
    const auto v = iv({{0, LMAX}, {LMAX - 2, LMAX}, {LMAX - 1, LMAX}, {LMAX - 5, LMAX - 1}});
    const auto idx = index_of(v);
    CHECK_EQ(idx.max(), 3);
    CHECK_EQ(idx.live_at(LMAX - 2), 3);
    CHECK_EQ(idx.live_at(LMAX - 1), 3);
    CHECK_EQ(idx.live_at(LMAX), 0);  // right end exclusive
    CHECK_EQ(idx.live_at(LMAX - 5), 2);
    CHECK_EQ(idx.live_at(LMAX - 6), 1);
    CHECK_EQ(idx.max_in(LMAX - 10, LMAX), 3);
    CHECK_EQ(idx.max_in(1, LMAX - 5), 1);  // `to` is exclusive
}

TEST(max_in_range_boundaries, "part4,edge") {
    const auto idx = index_of(iv({{10, 20}, {15, 30}}));
    CHECK_EQ(idx.max_in(0, 10), 0);  // `to` exclusive
    CHECK_EQ(idx.max_in(0, 11), 1);
    CHECK_EQ(idx.max_in(19, 21), 2);  // 19 is inside [15,20)
    CHECK_EQ(idx.max_in(20, 21), 1);  // from 20 on, [10,20) is over
    CHECK_EQ(idx.max_in(30, 99), 0);
    CHECK_EQ(idx.max_in(12, 12), 0);  // empty range
    CHECK_EQ(idx.max_in(0, 1000), 2);  // range sticks out on both sides: outside counts as 0
}

TEST(add_and_remove_are_inverses, "part4,edge") {
    auto idx = index_from({0, 5, 10, 20, 100});
    idx.add(0, 10);
    idx.add(5, 20);
    idx.add(5, 100);
    CHECK_EQ(idx.max(), 3);
    CHECK_EQ(idx.live_at(7), 3);
    idx.remove(5, 20);
    CHECK_EQ(idx.max(), 2);
    CHECK_EQ(idx.live_at(7), 2);
    CHECK_EQ(idx.live_at(30), 1);
    idx.remove(0, 10);
    idx.remove(5, 100);
    CHECK_EQ(idx.max(), 0);
    for (long long t : {0LL, 5LL, 7LL, 10LL, 50LL, 100LL}) CHECK_EQ(idx.live_at(t), 0);
}

TEST(index_invalid_arguments, "part4,edge") {
    auto idx = index_from({1, 5, 9});
    CHECK_THROWS_AS(idx.add(1, 6), std::invalid_argument);  // 6 is not a known endpoint
    CHECK_THROWS_AS(idx.add(2, 5), std::invalid_argument);
    CHECK_THROWS_AS(idx.add(5, 1), std::invalid_argument);  // end < start
    CHECK_THROWS_AS(idx.max_in(9, 1), std::invalid_argument);
}

TEST(index_random_against_brute_force, "part4") {
    for (unsigned seed = 71; seed <= 78; ++seed) {
        std::mt19937 rnd(seed);
        const int n = 1 + static_cast<int>(rnd() % 40);
        std::vector<Interval> v;
        for (int i = 0; i < n; ++i) {
            const long long a = static_cast<long long>(rnd() % 50);
            v.push_back({a, a + static_cast<long long>(rnd() % 20)});
        }
        const auto idx = index_of(v);
        CHECK_EQ(idx.max(), brute_max_in(v, 0, 80), "max, seed " + std::to_string(seed));
        CHECK_EQ(idx.max(), max_overlap(v));
        for (long long t = -2; t < 75; ++t) CHECK_EQ(idx.live_at(t), brute_live(v, t), "live_at " + std::to_string(t) + ", seed " + std::to_string(seed));
        for (int q = 0; q < 300; ++q) {
            const long long from = static_cast<long long>(rnd() % 80) - 5, to = from + static_cast<long long>(rnd() % 30);
            CHECK_EQ(idx.max_in(from, to), brute_max_in(v, from, to), "max_in [" + std::to_string(from) + "," + std::to_string(to) + "), seed " + std::to_string(seed));
        }
    }
}

TEST(dynamic_add_remove_against_recount, "part4") {
    for (unsigned seed = 81; seed <= 83; ++seed) {
        std::mt19937 rnd(seed);
        std::vector<long long> coords(30);
        for (auto& c : coords) c = static_cast<long long>(rnd() % 60);
        IntervalIndex idx{std::span<const long long>(coords)};
        std::vector<Interval> active;
        for (int step = 0; step < 400; ++step) {
            if (active.empty() || rnd() % 3 != 0) {
                const long long a = coords[rnd() % coords.size()], b = coords[rnd() % coords.size()];
                const Interval x{std::min(a, b), std::max(a, b)};
                idx.add(x.start, x.end);
                active.push_back(x);
            } else {
                const std::size_t k = rnd() % active.size();
                const Interval x = active[k];
                active.erase(active.begin() + static_cast<std::ptrdiff_t>(k));
                idx.remove(x.start, x.end);
            }
            CHECK_EQ(idx.max(), brute_max_in(active, 0, 61), "step " + std::to_string(step));
            const long long t = static_cast<long long>(rnd() % 61);
            CHECK_EQ(idx.live_at(t), brute_live(active, t), "step " + std::to_string(step) + " t " + std::to_string(t));
        }
    }
}

TEST(three_hundred_thousand_huge_intervals_and_queries_in_under_two_seconds, "part4,perf") {
    const int n = 300'000;
    std::mt19937_64 rnd(0);
    const long long range = 1'000'000'000'000'000'000LL;
    std::vector<Interval> v;
    v.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        const long long a = static_cast<long long>((rnd() >> 1) % static_cast<unsigned long long>(range));
        const long long len = 1 + static_cast<long long>((rnd() >> 1) % static_cast<unsigned long long>(range / 1000));
        v.push_back({a, a + len});
    }
    CHECK_WITHIN_MS(2000, {
        const auto idx = IntervalIndex::of(v);
        CHECK_EQ(idx.max(), max_overlap(v));
        int best = 0;
        for (int q = 0; q < 100'000; ++q) {
            const long long from = static_cast<long long>((rnd() >> 1) % static_cast<unsigned long long>(range));
            best = std::max(best, idx.max_in(from, from + range / 100));
        }
        CHECK_GE(best, 1);
    });
}

// ---- C++-only Part 4

TEST(queries_work_on_a_const_index_and_whole_range_does_not_overflow, "part4,edge,cpp") {
    const auto idx = index_of(iv({{0, 10}, {5, 15}}));
    const IntervalIndex& c = idx;  // queries are const: they never push tags down
    CHECK_EQ(c.max(), 2);
    CHECK_EQ(c.max_in(LLONG_MIN, LMAX), 2);  // no `to - from` anywhere
    CHECK_EQ(c.max_in(LMAX - 1, LMAX), 0);
    CHECK_EQ(c.live_at(LLONG_MIN), 0);
    CHECK_EQ(c.live_at(LMAX), 0);
}

TEST(negative_coordinates_are_ordinary_endpoints, "part4,edge,cpp") {
    auto idx = index_from({-5, 0, 5});
    idx.add(-5, 5);
    idx.add(0, 5);
    CHECK_EQ(idx.live_at(-5), 1);
    CHECK_EQ(idx.live_at(0), 2);
    CHECK_EQ(idx.max_in(-100, 0), 1);
    CHECK_EQ(idx.max_in(-100, -5), 0);
}

TEST(a_rejected_add_leaves_the_tree_untouched, "part4,edge,cpp") {
    // 3 is unknown: the start (1) is valid but the call must fail BEFORE any range update.
    auto idx = index_from({1, 5, 9});
    CHECK_THROWS_AS(idx.add(1, 3), std::invalid_argument);
    CHECK_THROWS_AS(idx.add(3, 9), std::invalid_argument);
    CHECK_THROWS_AS(idx.remove(0, 9), std::invalid_argument);
    CHECK_EQ(idx.max(), 0);
    idx.add(1, 9);
    CHECK_EQ(idx.max(), 1);
}

TEST(tree_sizes_around_powers_of_two, "part4,edge,cpp") {
    // 2, 3, 4, 5, 8, 9 elementary segments: the padded leaf count (2^k) leaves unused leaves that must never count.
    for (int m : {2, 3, 4, 5, 6, 9, 10}) {
        std::vector<long long> c;
        for (int i = 0; i < m; ++i) c.push_back(10 * i);
        IntervalIndex idx{std::span<const long long>(c)};
        CHECK_EQ(idx.segment_count(), m - 1);
        CHECK_EQ(idx.max(), 0);
        idx.add(c.front(), c.back());
        CHECK_EQ(idx.max(), 1, "m " + std::to_string(m));
        CHECK_EQ(idx.max_in(c.back() - 1, c.back() + 1000), 1);
        CHECK_EQ(idx.max_in(c.back(), c.back() + 1000), 0);
    }
}

MT_MAIN()
