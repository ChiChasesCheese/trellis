// hc15 · Streaming median — C++20 tests.  Same cases as test/StreamingMedianTest.java, WindowMedianTest.java,
// PercentileTest.java, TickHistogramTest.java and MedianPerfTest.java plus C++-only edge cases (tag "cpp"):
// a dangling reference when a recursive insert grows a vector, std::abs(LLONG_MIN), (lo + hi) / 2 overflow,
// signed/unsigned comparisons in rank checks, zero allocations after the histogram is built.
#include <algorithm>
#include <atomic>
#include <climits>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <new>
#include <random>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace median;
using LL = long long;
using V = std::vector<long long>;

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

namespace {

/// Obviously correct: sort and index.
LL oracle_percentile(V values, int p) {
    std::sort(values.begin(), values.end());
    const LL n = static_cast<LL>(values.size());
    const LL rank = (static_cast<LL>(p) * n + 99) / 100;
    return values[static_cast<std::size_t>(rank - 1)];
}
LL oracle_median(const V& v) { return oracle_percentile(v, 50); }
V last_k(const V& all, std::size_t k) { return V(all.size() > k ? all.end() - static_cast<std::ptrdiff_t>(k) : all.begin(), all.end()); }

V medians_of(const V& prices) {
    StreamingMedian m;
    V out;
    for (LL x : prices) {
        m.add(x);
        out.push_back(m.median());
    }
    return out;
}

V expected_window(const V& prices, int k) {
    V seen, out;
    for (LL x : prices) {
        seen.push_back(x);
        out.push_back(oracle_median(last_k(seen, static_cast<std::size_t>(k))));
    }
    return out;
}

// ================================================================================================ Part 1
TEST(sample, "part1") { CHECK_EQ(medians_of({5, 15, 1, 3}), (V{5, 5, 5, 3})); }

TEST(single_and_pair, "part1") {
    StreamingMedian m;
    m.add(42);
    CHECK_EQ(m.median(), 42LL);
    CHECK_EQ(m.size(), 1u);
    m.add(10);
    CHECK_EQ(m.median(), 10LL);  // {10, 42}: lower median
    m.add(50);
    CHECK_EQ(m.median(), 42LL);
    CHECK_EQ(m.size(), 3u);
}

TEST(empty_throws, "part1,edge") {
    StreamingMedian m;
    CHECK_EQ(m.size(), 0u);
    CHECK_THROWS_AS(m.median(), std::out_of_range);
    CHECK_THROWS_AS(m.doubled_median(), std::out_of_range);
}

TEST(ascending_descending_and_constant, "part1,edge") {
    V asc, desc;
    for (int i = 1; i <= 10; ++i) {
        asc.push_back(i);
        desc.push_back(11 - i);
    }
    CHECK_EQ(medians_of(asc), (V{1, 1, 2, 2, 3, 3, 4, 4, 5, 5}));
    CHECK_EQ(medians_of(desc), (V{10, 9, 9, 8, 8, 7, 7, 6, 6, 5}));
    CHECK_EQ(medians_of(V(7, 9)), (V{9, 9, 9, 9, 9, 9, 9}));
}

TEST(negatives_and_extremes, "part1,edge") {
    CHECK_EQ(medians_of({-5, -1, 3}), (V{-5, -5, -1}));
    CHECK_EQ(medians_of({LLONG_MIN, LLONG_MAX})[1], LLONG_MIN);
    CHECK_EQ(medians_of({LLONG_MAX, LLONG_MAX})[1], LLONG_MAX);
    CHECK_EQ(medians_of({LLONG_MIN, LLONG_MIN, LLONG_MAX})[2], LLONG_MIN);
    CHECK_EQ(medians_of({LLONG_MIN, 0, LLONG_MAX})[2], 0LL);
}

TEST(duplicates_on_both_sides_of_the_middle, "part1,edge") {
    CHECK_EQ(medians_of({2, 2, 2, 2, 2, 2}), (V{2, 2, 2, 2, 2, 2}));
    CHECK_EQ(medians_of({3, 1, 3, 1, 3}), (V{3, 1, 3, 1, 3}));
}

TEST(doubled_median_is_the_exact_median_times_two, "part1") {
    StreamingMedian m;
    m.add(1);
    CHECK_EQ(m.doubled_median(), 2LL);
    m.add(2);
    CHECK_EQ(m.doubled_median(), 3LL);  // 1.5 doubled
    m.add(10);
    CHECK_EQ(m.doubled_median(), 4LL);
    m.add(20);
    CHECK_EQ(m.doubled_median(), 12LL);  // (2 + 10) / 2 = 6 doubled
    CHECK_EQ(m.median(), 2LL);
}

TEST(doubled_median_overflows, "part1,edge") {
    StreamingMedian one;
    one.add(LLONG_MAX);
    CHECK_THROWS_AS(one.doubled_median(), std::overflow_error);
    StreamingMedian neg;
    neg.add(LLONG_MIN);
    CHECK_THROWS_AS(neg.doubled_median(), std::overflow_error);
    StreamingMedian two;
    two.add(LLONG_MAX);
    two.add(LLONG_MIN);
    CHECK_EQ(two.doubled_median(), -1LL);
    two.add(5);
    CHECK_EQ(two.doubled_median(), 10LL);
    StreamingMedian big;
    big.add(LLONG_MAX);
    big.add(LLONG_MAX);
    CHECK_THROWS_AS(big.doubled_median(), std::overflow_error);
    CHECK_EQ(big.median(), LLONG_MAX);
}

TEST(random_streams_match_the_sorting_oracle, "part1") {
    for (LL bound : {3LL, 10LL, 1'000'000LL, LLONG_MAX}) {
        std::mt19937_64 rnd(static_cast<unsigned long long>(bound));
        StreamingMedian m;
        V seen;
        for (int i = 0; i < 3000; ++i) {
            const LL x = static_cast<LL>(rnd() % static_cast<unsigned long long>(bound)) - bound / 2;
            m.add(x);
            seen.push_back(x);
            CHECK_EQ(m.median(), oracle_median(seen), "bound " + std::to_string(bound) + " step " + std::to_string(i));
            CHECK_EQ(m.size(), seen.size());
        }
    }
}

TEST(querying_does_not_change_state, "part1,edge") {
    StreamingMedian m;
    for (LL x : {4, 8, 15, 16, 23, 42}) m.add(x);
    const LL first = m.median();
    for (int i = 0; i < 5; ++i) CHECK_EQ(m.median(), first);
    CHECK_EQ(first, 15LL);
    CHECK_EQ(m.size(), 6u);
}

TEST(no_midpoint_overflow_or_abs_trap, "part1,edge,cpp") {
    // (lo + hi) / 2 overflows for two large values, std::abs(LLONG_MIN) is UB: neither may appear in median()
    StreamingMedian m;
    m.add(LLONG_MAX - 1);
    m.add(LLONG_MAX);
    CHECK_EQ(m.median(), LLONG_MAX - 1);
    StreamingMedian n;
    n.add(LLONG_MIN);
    n.add(LLONG_MIN + 1);
    CHECK_EQ(n.median(), LLONG_MIN);
}

// ================================================================================================ Part 2
TEST(slide_sample, "part2") {
    CHECK_EQ(WindowMedian::slide({1, 3, -1, -3, 5, 3, 6, 7}, 3), (V{1, 1, 1, -1, -1, 3, 5, 6}));
}

TEST(size_grows_to_k_then_stays, "part2") {
    WindowMedian w(3);
    CHECK_EQ(w.size(), 0u);
    w.add(10);
    w.add(20);
    CHECK_EQ(w.size(), 2u);
    CHECK_EQ(w.median(), 10LL);
    w.add(30);
    w.add(40);
    w.add(50);
    CHECK_EQ(w.size(), 3u);
    CHECK_EQ(w.median(), 40LL);
}

TEST(window_one_is_the_last_price, "part2,edge") { CHECK_EQ(WindowMedian::slide({7, -2, 9, 9, 0}, 1), (V{7, -2, 9, 9, 0})); }

TEST(window_two_is_the_smaller_of_the_last_two, "part2,edge") { CHECK_EQ(WindowMedian::slide({5, 9, 1, 4, 3}, 2), (V{5, 5, 1, 1, 3})); }

TEST(window_larger_than_the_stream_equals_part1, "part2,edge") { CHECK_EQ(WindowMedian::slide({5, 15, 1, 3}, 100), (V{5, 5, 5, 3})); }

TEST(window_empty_and_arguments, "part2,edge") {
    WindowMedian w(4);
    CHECK_THROWS_AS(w.median(), std::out_of_range);
    CHECK_THROWS_AS(WindowMedian(0), std::invalid_argument);
    CHECK_THROWS_AS(WindowMedian(-3), std::invalid_argument);
    CHECK_THROWS_AS(WindowMedian::slide({1}, 0), std::invalid_argument);
    CHECK_EQ(WindowMedian::slide({}, 3), V{});
}

TEST(duplicates_equal_to_both_heap_tops, "part2,edge") {
    const V p = {5, 5, 5, 1, 1, 1, 9, 9, 9, 9, 9, 5, 5, 1, 1, 9};
    for (int k : {2, 3, 4, 5}) CHECK_EQ(WindowMedian::slide(p, k), expected_window(p, k), "k " + std::to_string(k));
}

TEST(extreme_values_in_the_window, "part2,edge") {
    const V p = {LLONG_MAX, LLONG_MIN, 0, LLONG_MAX, LLONG_MAX, LLONG_MIN, LLONG_MIN, 7};
    for (int k : {1, 2, 3, 4}) CHECK_EQ(WindowMedian::slide(p, k), expected_window(p, k), "k " + std::to_string(k));
}

TEST(window_random_streams_match_the_sorting_oracle, "part2") {
    for (int k : {1, 2, 3, 4, 5, 10, 50}) {
        for (LL bound : {2LL, 5LL, 1000LL, LLONG_MAX}) {
            std::mt19937_64 rnd(static_cast<unsigned long long>(k) * 31 + static_cast<unsigned long long>(bound));
            V prices(2500);
            for (auto& x : prices) x = static_cast<LL>(rnd() % static_cast<unsigned long long>(bound)) - bound / 2;
            CHECK_EQ(WindowMedian::slide(prices, k), expected_window(prices, k), "k " + std::to_string(k) + " bound " + std::to_string(bound));
        }
    }
}

TEST(window_ordered_streams_match_the_sorting_oracle, "part2") {
    V up(600), down(600), zigzag(600);
    for (int i = 0; i < 600; ++i) {
        up[static_cast<std::size_t>(i)] = i;
        down[static_cast<std::size_t>(i)] = 600 - i;
        zigzag[static_cast<std::size_t>(i)] = i % 2 == 0 ? i : -i;
    }
    for (int k : {2, 3, 8, 99}) {
        CHECK_EQ(WindowMedian::slide(up, k), expected_window(up, k), "up k " + std::to_string(k));
        CHECK_EQ(WindowMedian::slide(down, k), expected_window(down, k), "down k " + std::to_string(k));
        CHECK_EQ(WindowMedian::slide(zigzag, k), expected_window(zigzag, k), "zigzag k " + std::to_string(k));
    }
}

TEST(lazy_deletion_keeps_memory_bounded_on_an_ascending_stream, "part2,edge") {
    const int k = 100;
    WindowMedian w(k);
    std::size_t worst = 0;
    for (int i = 0; i < 100'000; ++i) {
        w.add(i);
        worst = std::max(worst, w.retained());
    }
    CHECK(worst <= 4u * k, "retained up to " + std::to_string(worst) + " entries for k = 100");
    CHECK_EQ(w.median(), 99'949LL);  // window 99900..99999, the 50th smallest
}

// ================================================================================================ Part 3
TEST(rank_table, "part3") {
    const LL cases[][3] = {{0, 50, 0},  {1, 1, 1},   {1, 100, 1}, {2, 50, 1},   {3, 50, 2},    {4, 50, 2},    {5, 50, 3},
                           {7, 50, 4},  {10, 50, 5}, {5, 30, 2},  {5, 40, 2},   {5, 100, 5},   {5, 1, 1},     {100, 99, 99},
                           {101, 99, 100}, {100, 1, 1}, {101, 1, 2}, {10, 95, 10}, {20, 95, 19}, {200, 95, 190}, {199, 95, 190}};
    for (const auto& c : cases) {
        CHECK_EQ(OrderStatistics::rank(c[0], static_cast<int>(c[1])), c[2], "rank(" + std::to_string(c[0]) + "," + std::to_string(c[1]) + ")");
    }
}

TEST(rank_does_not_overflow, "part3,edge") {
    CHECK_EQ(OrderStatistics::rank(LLONG_MAX, 100), LLONG_MAX);
    CHECK_EQ(OrderStatistics::rank(LLONG_MAX, 50), 4'611'686'018'427'387'904LL);
    CHECK_EQ(OrderStatistics::rank(LLONG_MAX, 1), 92'233'720'368'547'759LL);
    CHECK_THROWS_AS(OrderStatistics::rank(10, 0), std::invalid_argument);
    CHECK_THROWS_AS(OrderStatistics::rank(10, 101), std::invalid_argument);
    CHECK_THROWS_AS(OrderStatistics::rank(10, -5), std::invalid_argument);
    CHECK_THROWS_AS(OrderStatistics::rank(-1, 50), std::invalid_argument);
}

OrderStatistics tree_of(const V& xs) {
    OrderStatistics t;
    for (LL x : xs) t.add(x);
    return t;
}

TEST(nearest_rank_example, "part3") {
    const OrderStatistics t = tree_of({35, 20, 50, 15, 40});
    CHECK_EQ(t.percentile(5), 15LL);
    CHECK_EQ(t.percentile(30), 20LL);
    CHECK_EQ(t.percentile(40), 20LL);
    CHECK_EQ(t.percentile(50), 35LL);
    CHECK_EQ(t.percentile(100), 50LL);
    CHECK_EQ(t.size(), 5);
}

TEST(kth_and_count_at_most_with_duplicates, "part3") {
    const OrderStatistics t = tree_of({5, 1, 5, 3, 5, 3, 9});
    const V sorted = {1, 3, 3, 5, 5, 5, 9};
    for (int r = 1; r <= 7; ++r) CHECK_EQ(t.kth(r), sorted[static_cast<std::size_t>(r - 1)], "kth " + std::to_string(r));
    CHECK_EQ(t.count_at_most(0), 0LL);
    CHECK_EQ(t.count_at_most(1), 1LL);
    CHECK_EQ(t.count_at_most(2), 1LL);
    CHECK_EQ(t.count_at_most(3), 3LL);
    CHECK_EQ(t.count_at_most(5), 6LL);
    CHECK_EQ(t.count_at_most(8), 6LL);
    CHECK_EQ(t.count_at_most(9), 7LL);
    CHECK_EQ(t.count_at_most(LLONG_MAX), 7LL);
    CHECK_EQ(t.count_at_most(LLONG_MIN), 0LL);
}

TEST(order_statistics_empty_and_errors, "part3,edge") {
    OrderStatistics t;
    CHECK_EQ(t.size(), 0);
    CHECK_THROWS_AS(t.percentile(50), std::out_of_range);
    CHECK_THROWS_AS(t.percentile(0), std::invalid_argument);  // p is checked first, even when empty
    CHECK_THROWS_AS(t.percentile(101), std::invalid_argument);
    CHECK_THROWS_AS(t.kth(1), std::invalid_argument);
    CHECK_EQ(t.count_at_most(5), 0LL);
    t.add(7);
    CHECK_THROWS_AS(t.kth(0), std::invalid_argument);
    CHECK_THROWS_AS(t.kth(2), std::invalid_argument);
    CHECK_THROWS_AS(t.kth(-1), std::invalid_argument);
    CHECK_EQ(t.kth(1), 7LL);
    CHECK_EQ(t.percentile(1), 7LL);
    CHECK_EQ(t.percentile(100), 7LL);
}

TEST(order_statistics_extremes_and_negatives, "part3,edge") {
    const OrderStatistics t = tree_of({LLONG_MAX, LLONG_MIN, 0, -1, 1, LLONG_MIN});
    CHECK_EQ(t.kth(1), LLONG_MIN);
    CHECK_EQ(t.kth(2), LLONG_MIN);
    CHECK_EQ(t.kth(3), -1LL);
    CHECK_EQ(t.kth(4), 0LL);
    CHECK_EQ(t.kth(5), 1LL);
    CHECK_EQ(t.kth(6), LLONG_MAX);
    CHECK_EQ(t.percentile(50), -1LL);
}

TEST(order_statistics_match_the_sorting_oracle, "part3") {
    for (LL bound : {4LL, 50LL, 100'000LL}) {
        std::mt19937_64 rnd(static_cast<unsigned long long>(bound));
        OrderStatistics t;
        V seen;
        for (int i = 0; i < 1500; ++i) {
            const LL x = static_cast<LL>(rnd() % static_cast<unsigned long long>(bound)) - bound / 3;
            t.add(x);
            seen.push_back(x);
            for (int p : {1, 10, 25, 50, 75, 90, 99, 100}) {
                if (i % 37 == 0 || p == 50) CHECK_EQ(t.percentile(p), oracle_percentile(seen, p), "bound " + std::to_string(bound) + " n " + std::to_string(i + 1) + " p " + std::to_string(p));
            }
            const LL probe = static_cast<LL>(rnd() % static_cast<unsigned long long>(bound)) - bound / 3;
            if (i % 11 == 0) CHECK_EQ(t.count_at_most(probe), static_cast<LL>(std::count_if(seen.begin(), seen.end(), [&](LL v) { return v <= probe; })));
        }
    }
}

TEST(sorted_input_does_not_degenerate, "part3,perf") {
    OrderStatistics t;
    CHECK_WITHIN_MS(2000, {
        for (int i = 0; i < 200'000; ++i) t.add(i);
        for (int i = 1; i <= 200'000; ++i) t.add(-i);
    });
    CHECK_EQ(t.size(), 400'000);
    CHECK_EQ(t.kth(1), -200'000LL);
    CHECK_EQ(t.kth(400'000), 199'999LL);
}

TEST(growing_the_node_vectors_inside_a_recursive_insert, "part3,cpp") {
    // 4000 inserts force many vector reallocations while insert() is on the stack: a reference taken before the
    // recursive call (auto& n = nodes[t]) dangles afterwards, and AddressSanitizer reports it here.
    OrderStatistics t;
    for (int i = 0; i < 4000; ++i) t.add((static_cast<LL>(i) * 7919) % 4001);
    CHECK_EQ(t.size(), 4000);
    CHECK_EQ(t.kth(1), 0LL);
    CHECK_EQ(t.count_at_most(LLONG_MAX), 4000LL);
}

TEST(two_heap_nearest_rank_example, "part3") {
    const V stream = {35, 20, 50, 15, 40};
    const int ps[] = {5, 30, 40, 50, 100};
    const V want = {15, 20, 20, 35, 50};
    for (std::size_t j = 0; j < 5; ++j) {
        TwoHeapPercentile h(ps[j]);
        for (LL x : stream) h.add(x);
        CHECK_EQ(h.value(), want[j], "p " + std::to_string(ps[j]));
        CHECK_EQ(h.size(), 5LL);
    }
}

TEST(two_heap_empty_and_arguments, "part3,edge") {
    CHECK_THROWS_AS(TwoHeapPercentile(0), std::invalid_argument);
    CHECK_THROWS_AS(TwoHeapPercentile(101), std::invalid_argument);
    TwoHeapPercentile h(90);
    CHECK_THROWS_AS(h.value(), std::out_of_range);
    h.add(LLONG_MIN);
    CHECK_EQ(h.value(), LLONG_MIN);
    h.add(LLONG_MAX);
    CHECK_EQ(h.value(), LLONG_MAX);  // n = 2, p = 90: rank ceil(1.8) = 2
    CHECK_EQ(h.size(), 2LL);
}

TEST(p50_is_the_part1_median, "part3") {
    std::mt19937 rnd(5);
    TwoHeapPercentile h(50);
    StreamingMedian m;
    for (int i = 0; i < 2000; ++i) {
        const LL x = static_cast<LL>(rnd() % 100) - 50;
        h.add(x);
        m.add(x);
        CHECK_EQ(h.value(), m.median());
    }
}

TEST(two_heap_matches_the_sorting_oracle_for_every_p, "part3") {
    for (int p : {1, 2, 10, 25, 50, 66, 75, 90, 95, 99, 100}) {
        std::mt19937 rnd(static_cast<unsigned>(p));
        TwoHeapPercentile h(p);
        V seen;
        for (int i = 0; i < 1200; ++i) {
            const LL x = static_cast<LL>(rnd() % (i % 3 == 0 ? 6u : 100'000u)) - 3;
            h.add(x);
            seen.push_back(x);
            CHECK_EQ(h.value(), oracle_percentile(seen, p), "p " + std::to_string(p) + " n " + std::to_string(i + 1));
        }
    }
}

TEST(both_structures_agree_on_the_same_stream, "part3") {
    std::mt19937 rnd(99);
    OrderStatistics tree;
    TwoHeapPercentile h95(95), h5(5);
    for (int i = 0; i < 20'000; ++i) {
        const LL x = rnd() % 1000;
        tree.add(x);
        h95.add(x);
        h5.add(x);
        if (i % 101 == 0) {
            CHECK_EQ(tree.percentile(95), h95.value());
            CHECK_EQ(tree.percentile(5), h5.value());
        }
    }
}

// ================================================================================================ Part 4
TEST(histogram_nearest_rank_example, "part4") {
    TickHistogram h(100);
    for (LL x : {35, 20, 50, 15, 40}) h.add(x);
    CHECK_EQ(h.count(), 5LL);
    CHECK_EQ(h.percentile(5), 15LL);
    CHECK_EQ(h.percentile(30), 20LL);
    CHECK_EQ(h.percentile(40), 20LL);
    CHECK_EQ(h.percentile(50), 35LL);
    CHECK_EQ(h.median(), 35LL);
    CHECK_EQ(h.percentile(100), 50LL);
}

TEST(histogram_kth_and_count_at_most_with_duplicates, "part4") {
    TickHistogram h(10);
    for (LL x : {5, 1, 5, 3, 5, 3, 9}) h.add(x);
    const V sorted = {1, 3, 3, 5, 5, 5, 9};
    for (int r = 1; r <= 7; ++r) CHECK_EQ(h.kth(r), sorted[static_cast<std::size_t>(r - 1)], "kth " + std::to_string(r));
    CHECK_EQ(h.count_at_most(0), 0LL);
    CHECK_EQ(h.count_at_most(1), 1LL);
    CHECK_EQ(h.count_at_most(3), 3LL);
    CHECK_EQ(h.count_at_most(8), 6LL);
    CHECK_EQ(h.count_at_most(9), 7LL);
}

TEST(histogram_count_at_most_outside_the_band, "part4,edge") {
    TickHistogram h(10);
    h.add(0);
    h.add(9);
    CHECK_EQ(h.count_at_most(-1), 0LL);
    CHECK_EQ(h.count_at_most(LLONG_MIN), 0LL);
    CHECK_EQ(h.count_at_most(0), 1LL);
    CHECK_EQ(h.count_at_most(10), 2LL);
    CHECK_EQ(h.count_at_most(LLONG_MAX), 2LL);
}

TEST(histogram_arguments_and_empty, "part4,edge") {
    CHECK_THROWS_AS(TickHistogram(0), std::invalid_argument);
    CHECK_THROWS_AS(TickHistogram(-1), std::invalid_argument);
    CHECK_THROWS_AS(TickHistogram(TickHistogram::MAX_TICKS + 1), std::invalid_argument);
    TickHistogram h(8);
    CHECK_EQ(h.count(), 0LL);
    CHECK_THROWS_AS(h.median(), std::out_of_range);
    CHECK_THROWS_AS(h.percentile(99), std::out_of_range);
    CHECK_THROWS_AS(h.percentile(0), std::invalid_argument);
    CHECK_THROWS_AS(h.percentile(101), std::invalid_argument);
    CHECK_THROWS_AS(h.add(-1), std::invalid_argument);
    CHECK_THROWS_AS(h.add(8), std::invalid_argument);
    CHECK_THROWS_AS(h.add(LLONG_MAX), std::invalid_argument);
    CHECK_THROWS_AS(h.add(LLONG_MIN), std::invalid_argument);
    CHECK_EQ(h.count(), 0LL);  // rejected adds are not counted
    CHECK_THROWS_AS(h.kth(1), std::invalid_argument);
    h.add(7);
    CHECK_THROWS_AS(h.kth(0), std::invalid_argument);
    CHECK_THROWS_AS(h.kth(2), std::invalid_argument);
    CHECK_EQ(h.kth(1), 7LL);
}

TEST(histogram_single_tick_band, "part4,edge") {
    TickHistogram h(1);
    for (int i = 0; i < 5; ++i) h.add(0);
    CHECK_EQ(h.median(), 0LL);
    CHECK_EQ(h.percentile(100), 0LL);
    CHECK_EQ(h.count(), 5LL);
    CHECK_THROWS_AS(h.add(1), std::invalid_argument);
}

TEST(histogram_band_edges_and_the_largest_band, "part4,edge") {
    TickHistogram h(TickHistogram::MAX_TICKS);
    h.add(0);
    h.add(TickHistogram::MAX_TICKS - 1);
    CHECK_EQ(h.kth(1), 0LL);
    CHECK_EQ(h.kth(2), static_cast<LL>(TickHistogram::MAX_TICKS - 1));
    CHECK_EQ(h.median(), 0LL);
    CHECK_EQ(h.percentile(51), static_cast<LL>(TickHistogram::MAX_TICKS - 1));
}

TEST(histogram_matches_the_sorting_oracle_for_every_band_size, "part4") {
    for (int band : {1, 2, 3, 7, 8, 9, 100, 1000, 1024, 1025}) {
        std::mt19937 rnd(static_cast<unsigned>(band));
        TickHistogram h(band);
        V seen;
        for (int i = 0; i < 800; ++i) {
            const LL x = static_cast<LL>(rnd() % static_cast<unsigned>(band));
            h.add(x);
            seen.push_back(x);
            for (int p : {1, 25, 50, 75, 99, 100}) {
                if (i % 13 == 0 || p == 50) CHECK_EQ(h.percentile(p), oracle_percentile(seen, p), "band " + std::to_string(band) + " n " + std::to_string(i + 1) + " p " + std::to_string(p));
            }
        }
    }
}

TEST(histogram_agrees_with_the_order_statistics_tree, "part4") {
    std::mt19937 rnd(3);
    std::normal_distribution<double> gauss(0.0, 800.0);
    TickHistogram h(5000);
    OrderStatistics t;
    for (int i = 0; i < 20'000; ++i) {
        const LL x = static_cast<LL>(std::fabs(gauss(rnd))) % 5000;
        h.add(x);
        t.add(x);
        if (i % 97 == 0) {
            for (int p : {1, 50, 95, 100}) CHECK_EQ(h.percentile(p), t.percentile(p));
            CHECK_EQ(h.count_at_most(x), t.count_at_most(x));
        }
    }
}

TEST(histogram_allocates_nothing_after_construction, "part4,cpp") {
    TickHistogram h(1 << 16);
    std::mt19937 rnd(1);
    const AllocCount a;
    LL acc = 0;
    for (int i = 0; i < 200'000; ++i) {
        h.add(rnd() % (1 << 16));
        acc += h.percentile(1 + i % 100);
    }
    CHECK_EQ(a.get(), 0u, "allocations after the constructor");
    CHECK(acc > 0);
}

// ---------------------------------------------------------------- 1e6 operations
constexpr int N = 1'000'000;
constexpr int BAND = 1 << 20;

const V& data() {
    static const V d = [] {
        std::mt19937_64 rnd(0);
        std::normal_distribution<double> gauss(BAND / 2.0, BAND / 8.0);
        V out(N);
        for (auto& x : out) {
            const LL v = static_cast<LL>(gauss(rnd));
            x = ((v % BAND) + BAND) % BAND;
        }
        return out;
    }();
    return d;
}

V sorted_data() {
    V s = data();
    std::sort(s.begin(), s.end());
    return s;
}

TEST(histogram_million_adds_and_queries, "part4,perf") {
    const V& d = data();
    TickHistogram h(BAND);
    LL acc = 0;
    CHECK_WITHIN_MS(1000, {
        for (int i = 0; i < N; ++i) {
            h.add(d[static_cast<std::size_t>(i)]);
            acc += h.percentile(1 + i % 100);
        }
    });
    const V s = sorted_data();
    CHECK(acc > 0);
    CHECK_EQ(h.count(), static_cast<LL>(N));
    CHECK_EQ(h.median(), s[N / 2 - 1]);
    CHECK_EQ(h.percentile(95), s[static_cast<std::size_t>(0.95 * N) - 1]);
}

TEST(two_heap_median_million_adds, "part4,perf") {
    const V& d = data();
    StreamingMedian m;
    LL acc = 0;
    CHECK_WITHIN_MS(2000, {
        for (LL x : d) {
            m.add(x);
            acc ^= m.median();
        }
    });
    CHECK(acc >= 0);
    CHECK_EQ(m.median(), sorted_data()[N / 2 - 1]);
    CHECK_EQ(m.size(), static_cast<std::size_t>(N));
}

TEST(window_median_million_adds_window_ten_thousand, "part4,perf") {
    const V& d = data();
    const int k = 10'000;
    WindowMedian w(k);
    CHECK_WITHIN_MS(2000, {
        for (LL x : d) {
            w.add(x);
            (void)w.median();
        }
    });
    CHECK_EQ(w.median(), oracle_median(V(d.end() - k, d.end())));
    CHECK_EQ(w.size(), static_cast<std::size_t>(k));
    CHECK(w.retained() <= 4u * k, "retained " + std::to_string(w.retained()));
}

TEST(fixed_percentile_heaps_million_adds, "part4,perf") {
    const V& d = data();
    TwoHeapPercentile h(95);
    CHECK_WITHIN_MS(2000, {
        for (LL x : d) {
            h.add(x);
            (void)h.value();
        }
    });
    CHECK_EQ(h.value(), sorted_data()[static_cast<std::size_t>(0.95 * N) - 1]);
}

TEST(order_statistics_tree_million_adds_and_queries, "part4,perf") {
    const V& d = data();
    OrderStatistics t;
    LL acc = 0;
    CHECK_WITHIN_MS(3000, {
        for (int i = 0; i < N; ++i) {
            t.add(d[static_cast<std::size_t>(i)]);
            acc += t.percentile(1 + i % 100);
        }
    });
    CHECK(acc > 0);
    const V s = sorted_data();
    for (int p : {1, 50, 95, 100}) CHECK_EQ(t.percentile(p), s[static_cast<std::size_t>((static_cast<LL>(p) * N + 99) / 100) - 1], "p " + std::to_string(p));
}

}  // namespace

MT_MAIN()
