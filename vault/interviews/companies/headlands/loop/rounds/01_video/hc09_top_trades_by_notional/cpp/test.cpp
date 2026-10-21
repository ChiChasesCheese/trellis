// hc09 · Top trades by notional — C++20 tests.  Same cases as test/TopTradesTest.java, SlidingTopKTest.java and
// ParallelNotionalTest.java plus C++-only edge cases (tag "cpp"): bytewise ticker order, embedded NULs, results that
// outlive the borrowed input, k = INT_MAX, checked arithmetic, the equal-key trap in std::set, a non-movable class that
// holds string_views, exceptions in worker threads, cooperative cancellation.
#include <algorithm>
#include <atomic>
#include <chrono>
#include <climits>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <random>
#include <sstream>
#include <thread>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace toptrades;

namespace toptrades {
std::ostream& operator<<(std::ostream& os, const Trade& t) {
    return os << "Trade{i=" << t.index << "," << t.ticker << "," << t.price << "x" << t.volume << "}";
}
std::ostream& operator<<(std::ostream& os, const TickerTotal& t) { return os << t.ticker << "=" << t.notional; }
std::ostream& operator<<(std::ostream& os, const Answer& a) {
    os << "Answer{t=" << a.time << ",[";
    for (const auto& x : a.top) os << x << ";";
    return os << "]}";
}
std::ostream& operator<<(std::ostream& os, const Summary& s) {
    os << "Summary{" << s.grand_total << ",";
    if (s.largest) os << *s.largest; else os << "none";
    return os << "}";
}
}  // namespace toptrades

namespace {

using SV = std::vector<std::string_view>;
using LL = std::vector<long long>;
constexpr long long LMAX = LLONG_MAX;

// problem.md sample
const SV T = {"AAPL", "MSFT", "AAPL", "GOOG", "MSFT", "TSLA"};
const LL P = {18000, 40000, 18100, 14000, 40000, 25000};
const LL V = {10, 3, 5, 9, 3, 8};
// notional: 180000 120000 90500 126000 120000 200000

/// vector::resize needs a default constructor, which the validated value types deliberately lack.
template <class C> void truncate(C& c, std::size_t k) {
    if (c.size() > k) c.erase(c.begin() + static_cast<std::ptrdiff_t>(k), c.end());
}

Trade trade(int i) { return Trade(i, std::string(T[static_cast<std::size_t>(i)]), P[static_cast<std::size_t>(i)], V[static_cast<std::size_t>(i)]); }

std::vector<int> indices(const std::vector<Trade>& v) {
    std::vector<int> out;
    for (const auto& t : v) out.push_back(t.index);
    return out;
}
std::vector<std::string> tickers_of(const std::vector<TickerTotal>& v) {
    std::vector<std::string> out;
    for (const auto& t : v) out.push_back(t.ticker);
    return out;
}
TickerTotal tt(const char* t, long long n) { return TickerTotal(t, n); }

/// Obviously-correct reference: sort all indices with the three-key order (small values only: no overflow).
std::vector<int> oracle_events(const SV& t, const LL& p, const LL& v, std::size_t k) {
    std::vector<int> idx(t.size());
    std::iota(idx.begin(), idx.end(), 0);
    std::sort(idx.begin(), idx.end(), [&](int a, int b) {
        const long long na = p[static_cast<std::size_t>(a)] * v[static_cast<std::size_t>(a)];
        const long long nb = p[static_cast<std::size_t>(b)] * v[static_cast<std::size_t>(b)];
        if (na != nb) return na > nb;
        if (t[static_cast<std::size_t>(a)] != t[static_cast<std::size_t>(b)]) return t[static_cast<std::size_t>(a)] < t[static_cast<std::size_t>(b)];
        return a < b;
    });
    idx.resize(std::min(k, idx.size()));
    return idx;
}

std::vector<TickerTotal> oracle_tickers(const SV& t, const LL& p, const LL& v, std::size_t k) {
    std::map<std::string, long long> m;
    for (std::size_t i = 0; i < t.size(); ++i) m[std::string(t[i])] += p[i] * v[i];
    std::vector<TickerTotal> all;
    for (const auto& [name, total] : m) all.emplace_back(name, total);
    std::sort(all.begin(), all.end(), BestTickerFirst{});
    truncate(all, k);
    return all;
}

/// Name pool with stable storage: string_views taken from it stay valid for the whole run.
const std::vector<std::string>& names_of(int count) {
    static std::map<int, std::vector<std::string>> cache;
    static std::mutex m;
    std::lock_guard<std::mutex> g(m);
    auto it = cache.find(count);
    if (it == cache.end()) {
        std::vector<std::string> v;
        for (int i = 0; i < count; ++i) v.push_back("T" + std::to_string(i));
        it = cache.emplace(count, std::move(v)).first;
    }
    return it->second;
}

struct Data {
    SV t;
    LL p, v;
    static Data random(unsigned seed, int n, int tickers, int max_price, int max_vol) {
        std::mt19937 rnd(seed);
        const auto& names = names_of(tickers);
        Data d;
        for (int i = 0; i < n; ++i) {
            d.t.push_back(names[rnd() % static_cast<unsigned>(tickers)]);
            d.p.push_back(static_cast<long long>(rnd() % static_cast<unsigned>(max_price + 1)));
            d.v.push_back(static_cast<long long>(rnd() % static_cast<unsigned>(max_vol + 1)));
        }
        return d;
    }
};

std::string dump(const Totals& m) {
    std::map<std::string, long long> s(m.begin(), m.end());
    std::string out;
    for (const auto& [k, v] : s) out += k + "=" + std::to_string(v) + ",";
    return out;
}

}  // namespace

// ================================================ Part 1: top-k events

TEST(sample_top_three, "part1") {
    const auto top = top_events(T, P, V, 3);
    CHECK_EQ(top, (std::vector<Trade>{trade(5), trade(0), trade(3)}));
    CHECK_EQ(top[0].notional(), 200000);
    CHECK_EQ(top[1].notional(), 180000);
    CHECK_EQ(top[2].notional(), 126000);
}

TEST(tie_on_notional_and_ticker_falls_back_to_index, "part1") {
    CHECK_EQ(indices(top_events(T, P, V, 4)), (std::vector<int>{5, 0, 3, 1}));
    CHECK_EQ(indices(top_events(T, P, V, 6)), (std::vector<int>{5, 0, 3, 1, 4, 2}));
}

TEST(tie_on_notional_falls_back_to_ticker_ascending, "part1,edge") {
    const SV t = {"ZZZ", "AAA", "MMM", "AAA"};
    const LL p = {10, 10, 10, 10}, v = {5, 5, 5, 5};
    CHECK_EQ(indices(top_events(t, p, v, 4)), (std::vector<int>{1, 3, 2, 0}));
    CHECK_EQ(indices(top_events(t, p, v, 2)), (std::vector<int>{1, 3}));
}

TEST(k_larger_than_n_returns_everything_sorted, "part1,edge") {
    const auto top = top_events(T, P, V, 100);
    CHECK_EQ(top.size(), 6u);
    CHECK_EQ(oracle_events(T, P, V, 100), indices(top));
}

TEST(k_zero_and_empty_input, "part1,edge") {
    const SV et;
    const LL el;
    CHECK(top_events(T, P, V, 0).empty());
    CHECK(top_events(et, el, el, 5).empty());
    CHECK(top_events(et, el, el, 0).empty());
}

TEST(single_event, "part1,edge") {
    const SV t = {"X"};
    const LL p = {7}, v = {3};
    const auto top = top_events(t, p, v, 1);
    CHECK_EQ(top, (std::vector<Trade>{Trade(0, "X", 7, 3)}));
    CHECK_EQ(top.front().notional(), 21);
}

TEST(zero_volume_and_zero_price_are_legal_and_rank_last, "part1,edge") {
    const SV t = {"A", "B", "C"};
    const LL p = {0, 5, 9}, v = {100, 0, 1};
    CHECK_EQ(indices(top_events(t, p, v, 3)), (std::vector<int>{2, 0, 1}));  // 9, then 0 (A), 0 (B)
}

TEST(invalid_inputs, "part1,edge") {
    const LL p5(P.begin(), P.begin() + 5), v7 = [] { LL x = V; x.push_back(1); return x; }();
    CHECK_THROWS_AS(top_events(T, P, V, -1), std::invalid_argument);
    CHECK_THROWS_AS(top_events(T, p5, V, 2), std::invalid_argument);
    CHECK_THROWS_AS(top_events(T, P, v7, 2), std::invalid_argument);
    const SV a = {"A"};
    const LL neg = {-1}, one = {1};
    CHECK_THROWS_AS(top_events(a, neg, one, 1), std::invalid_argument);
    CHECK_THROWS_AS(top_events(a, one, neg, 1), std::invalid_argument);
}

TEST(invalid_event_is_rejected_even_if_it_could_never_make_the_top_k, "part1,edge") {
    const SV t = {"A", "B", "C"};
    const LL p = {1000, 5, -1}, v = {1000, 5, 1};
    CHECK_THROWS_AS(top_events(t, p, v, 1), std::invalid_argument);
}

TEST(multiplication_overflow_is_detected_not_wrapped, "part1,edge") {
    const SV t = {"BIG", "SMALL"};
    // the overflowing event is last in rank order and k = 1: it must still be found
    const LL p = {1, LMAX}, v = {1, 2};
    CHECK_THROWS_AS(top_events(t, p, v, 1), std::overflow_error);
    const SV a = {"A"};
    const LL pa = {LMAX}, va = {2};
    CHECK_THROWS_AS(top_events(a, pa, va, 1), std::overflow_error);  // wrapped, this would be -2
    CHECK_THROWS_AS(top_events_sorted(a, pa, va, 1), std::overflow_error);
    CHECK_THROWS_AS(top_events_partial_sort(a, pa, va, 1), std::overflow_error);
    CHECK_THROWS_AS(top_events_nth_element(a, pa, va, 1), std::overflow_error);
}

TEST(notional_exactly_llong_max_is_fine_and_square_root_boundary, "part1,edge") {
    const SV t = {"A", "B"};
    const LL p = {LMAX, 1}, v = {1, 1};
    CHECK_EQ(top_events(t, p, v, 2).front().notional(), LMAX);
    // floor(sqrt(LLONG_MAX)) = 3037000499
    const SV a = {"A"};
    const LL ok = {3'037'000'499LL}, bad = {3'037'000'500LL};
    CHECK_EQ(top_events(a, ok, ok, 1).front().notional(), 3'037'000'499LL * 3'037'000'499LL);
    CHECK_THROWS_AS(top_events(a, bad, bad, 1), std::overflow_error);
}

TEST(input_arrays_are_not_modified, "part1,edge") {
    const SV t = T;
    const LL p = P, v = V;
    (void)top_events(t, p, v, 3);
    (void)top_tickers(t, p, v, 3);
    (void)top_events_nth_element(t, p, v, 3);
    CHECK(t == T && p == P && v == V);
}

TEST(random_against_oracle_with_heavy_ties, "part1") {
    for (unsigned seed = 1; seed <= 8; ++seed) {
        std::mt19937 rnd(seed);
        const int n = 1 + static_cast<int>(rnd() % 300);
        SV t;
        LL p, v;
        const auto& names = names_of(6);
        for (int i = 0; i < n; ++i) {
            t.push_back(names[rnd() % 6]);
            p.push_back(1 + static_cast<long long>(rnd() % 4));  // tiny value range: lots of equal notionals
            v.push_back(static_cast<long long>(rnd() % 4));
        }
        for (int k : {1, 2, 5, 17, n, n + 3}) {
            const auto expect = oracle_events(t, p, v, static_cast<std::size_t>(k));
            const auto heap = top_events(t, p, v, k);
            CHECK_EQ(expect, indices(heap), "seed " + std::to_string(seed) + " k " + std::to_string(k));
            CHECK_EQ(heap, top_events_sorted(t, p, v, k));
            CHECK_EQ(heap, top_events_partial_sort(t, p, v, k));
            CHECK_EQ(heap, top_events_nth_element(t, p, v, k));
        }
    }
}

TEST(random_million_events_top_100_in_under_two_seconds, "part1,perf") {
    const Data d = Data::random(0, 1'000'000, 5000, 1'000'000, 10'000);
    CHECK_WITHIN_MS(2000, {
        const auto top = top_events(d.t, d.p, d.v, 100);
        CHECK_EQ(top.size(), 100u);
        for (std::size_t i = 1; i < top.size(); ++i) CHECK_GE(top[i - 1].notional(), top[i].notional());
    });
}

TEST(adversarial_ascending_order_every_event_enters_the_heap, "part1,perf") {
    const int n = 1'000'000;
    SV t(static_cast<std::size_t>(n), std::string_view("X"));
    LL p(static_cast<std::size_t>(n)), v(static_cast<std::size_t>(n), 1000);
    for (int i = 0; i < n; ++i) p[static_cast<std::size_t>(i)] = i + 1;
    CHECK_WITHIN_MS(2000, {
        const auto top = top_events(t, p, v, 1000);
        CHECK_EQ(top.front().index, n - 1);
        CHECK_EQ(top.back().index, n - 1000);
    });
}

// ---- C++-only Part 1

TEST(ticker_order_is_bytewise_unsigned, "part1,edge,cpp") {
    // "\xC3\xA9" (UTF-8 for e-acute) must sort AFTER "Z": comparing as signed char would put it first.
    const SV t = {"\xC3\xA9", "Z", "", "A"};
    const LL p = {1, 1, 1, 1}, v = {1, 1, 1, 1};
    CHECK_EQ(indices(top_events(t, p, v, 4)), (std::vector<int>{2, 3, 1, 0}));  // "", "A", "Z", "\xC3\xA9"
    CHECK_EQ(indices(top_events_nth_element(t, p, v, 4)), (std::vector<int>{2, 3, 1, 0}));
}

TEST(embedded_nul_is_part_of_the_ticker, "part1,edge,cpp") {
    // string_view with an explicit length keeps the NUL; a char* / strcmp based implementation would see "A" three times.
    const SV t = {std::string_view("A\0C", 3), std::string_view("A\0B", 3), "A"};
    const LL p = {5, 5, 5}, v = {1, 1, 1};
    const auto top = top_events(t, p, v, 3);
    CHECK_EQ(indices(top), (std::vector<int>{2, 1, 0}));
    CHECK_EQ(top[1].ticker.size(), 3u);
    const auto totals = top_tickers(t, p, v, 3);
    CHECK_EQ(totals.size(), 3u);  // three different names
}

TEST(results_own_their_strings_after_the_input_is_gone, "part1,edge,cpp") {
    std::vector<Trade> events;
    std::vector<TickerTotal> totals;
    {
        auto storage = std::make_unique<std::vector<std::string>>();
        for (int i = 0; i < 5; ++i) storage->push_back("a-rather-long-ticker-name-that-is-not-sso-" + std::to_string(i));
        SV t;
        for (const auto& s : *storage) t.push_back(s);
        const LL p = {3, 1, 4, 1, 5}, v = {1, 1, 1, 1, 1};
        events = top_events(t, p, v, 3);
        totals = top_tickers(t, p, v, 3);
    }  // storage freed: a result holding string_views would now dangle (ASan: heap-use-after-free)
    CHECK_EQ(events.front().ticker, std::string("a-rather-long-ticker-name-that-is-not-sso-4"));
    CHECK_EQ(totals.front().ticker, std::string("a-rather-long-ticker-name-that-is-not-sso-4"));
    CHECK_EQ(totals.back().notional, 3);
}

TEST(huge_k_does_not_preallocate, "part1,edge,cpp") {
    // reserve(k) with k = INT_MAX would ask for tens of gigabytes; the container must be sized by min(k, n).
    CHECK_EQ(top_events(T, P, V, INT_MAX).size(), 6u);
    CHECK_EQ(top_events_partial_sort(T, P, V, INT_MAX).size(), 6u);
    CHECK_EQ(top_events_nth_element(T, P, V, INT_MAX).size(), 6u);
    CHECK_EQ(top_tickers(T, P, V, INT_MAX).size(), 4u);
}

TEST(partition_boundaries_of_nth_element_and_partial_sort, "part1,edge,cpp") {
    // k = n (nothing to partition), k = n - 1, k = 1: the off-by-one places for nth_element(first, first + m - 1, last)
    for (int k : {1, 5, 6, 7}) {
        const auto expect = top_events(T, P, V, k);
        CHECK_EQ(expect, top_events_nth_element(T, P, V, k), "k " + std::to_string(k));
        CHECK_EQ(expect, top_events_partial_sort(T, P, V, k), "k " + std::to_string(k));
        CHECK_EQ(expect, top_events_sorted(T, P, V, k), "k " + std::to_string(k));
    }
}

TEST(checked_arithmetic_never_reaches_signed_overflow_ub, "part1,edge,cpp") {
    // UBSan (halt on error) would abort the run if any of these multiplied or added without the builtin.
    CHECK_EQ(mul_exact(LMAX, 1), LMAX);
    CHECK_EQ(mul_exact(LMAX, 0), 0);
    CHECK_EQ(mul_exact(1LL << 31, (1LL << 31) - 1), (1LL << 62) - (1LL << 31));
    CHECK_THROWS_AS(mul_exact(1LL << 32, 1LL << 31), std::overflow_error);  // exactly 2^63
    CHECK_THROWS_AS(add_exact(LMAX, 1), std::overflow_error);
    CHECK_EQ(add_exact(LMAX - 1, 1), LMAX);
    // negative inputs are rejected before they reach the multiplication (LLONG_MIN * -1 would be UB)
    const SV a = {"A"};
    const LL m = {LLONG_MIN}, n1 = {-1};
    CHECK_THROWS_AS(top_events(a, m, n1, 1), std::invalid_argument);
}

TEST(trade_is_cheap_to_move_and_validates_on_construction, "part1,edge,cpp") {
    static_assert(std::is_nothrow_move_constructible_v<Trade>, "vector<Trade> growth must move, not copy");
    CHECK_THROWS_AS(Trade(-1, "A", 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "A", -1, 1), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "A", 1, -1), std::invalid_argument);
    CHECK_THROWS_AS(Trade(0, "A", LMAX, 2), std::overflow_error);
    CHECK_THROWS_AS(TickerTotal("A", -1), std::invalid_argument);
}

// ================================================ Part 2: top-k tickers

TEST(sample_top_two_tickers, "part2") {
    // AAPL 270500, MSFT 240000, TSLA 200000, GOOG 126000
    CHECK_EQ(top_tickers(T, P, V, 2), (std::vector<TickerTotal>{tt("AAPL", 270'500), tt("MSFT", 240'000)}));
    CHECK_EQ(top_tickers(T, P, V, 10).size(), 4u);
}

TEST(top_ticker_can_differ_from_the_top_event, "part2") {
    CHECK_EQ(top_events(T, P, V, 1).front().ticker, std::string("TSLA"));
    CHECK_EQ(top_tickers(T, P, V, 1).front().ticker, std::string("AAPL"));
}

TEST(equal_totals_break_ties_by_ticker_ascending, "part2,edge") {
    const SV t = {"B", "A", "C", "A"};
    const LL p = {10, 4, 10, 6}, v = {1, 1, 1, 1};
    CHECK_EQ(tickers_of(top_tickers(t, p, v, 3)), (std::vector<std::string>{"A", "B", "C"}));
    CHECK_EQ(tickers_of(top_tickers(t, p, v, 1)), (std::vector<std::string>{"A"}));
}

TEST(zero_notional_tickers_still_exist, "part2,edge") {
    const SV t = {"A", "B"};
    const LL p = {0, 3}, v = {5, 1};
    CHECK_EQ(top_tickers(t, p, v, 5), (std::vector<TickerTotal>{tt("B", 3), tt("A", 0)}));
}

TEST(empty_k_zero_and_invalid, "part2,edge") {
    const SV et;
    const LL el;
    CHECK(top_tickers(et, el, el, 3).empty());
    CHECK(top_tickers(T, P, V, 0).empty());
    CHECK_THROWS_AS(top_tickers(T, P, V, -1), std::invalid_argument);
    const LL p2(P.begin(), P.begin() + 2);
    CHECK_THROWS_AS(top_tickers(T, p2, V, 1), std::invalid_argument);
}

TEST(aggregate_overflow_is_detected_even_when_each_event_fits, "part2,edge") {
    const long long half = LMAX / 2 + 1;  // 2 * half overflows
    const SV same = {"A", "A"}, diff = {"A", "B"};
    const LL p = {half, half}, v = {1, 1};
    CHECK_THROWS_AS(top_tickers(same, p, v, 1), std::overflow_error);
    CHECK_THROWS_AS(top_tickers_sorted(same, p, v, 1), std::overflow_error);
    CHECK_EQ(top_tickers(diff, p, v, 2).front().notional, half);  // different tickers never merge
    const LL p3 = {LMAX - 5, 5}, v3 = {1, 1};
    CHECK_EQ(top_tickers(same, p3, v3, 1).front().notional, LMAX);  // exactly LLONG_MAX is fine
}

TEST(heap_sort_and_oracle_agree, "part2") {
    for (unsigned seed = 11; seed <= 16; ++seed) {
        std::mt19937 rnd(seed);
        const int n = 1 + static_cast<int>(rnd() % 400);
        const auto& names = names_of(40);
        SV t;
        LL p, v;
        for (int i = 0; i < n; ++i) {
            t.push_back(names[rnd() % 40]);
            p.push_back(static_cast<long long>(rnd() % 5));
            v.push_back(static_cast<long long>(rnd() % 5));
        }
        for (int k : {0, 1, 3, 10, 40, 100}) {
            const auto expect = oracle_tickers(t, p, v, static_cast<std::size_t>(k));
            CHECK_EQ(expect, top_tickers(t, p, v, k), "heap, seed " + std::to_string(seed) + " k " + std::to_string(k));
            CHECK_EQ(expect, top_tickers_sorted(t, p, v, k), "sorted, seed " + std::to_string(seed) + " k " + std::to_string(k));
        }
    }
}

TEST(top_of_works_on_a_prebuilt_table, "part2") {
    Totals m;
    m.emplace("A", 5);
    m.emplace("B", 9);
    m.emplace("C", 5);
    m.emplace("D", 1);
    CHECK_EQ(tickers_of(top_of(m, 3)), (std::vector<std::string>{"B", "A", "C"}));
    CHECK(top_of(Totals{}, 3).empty());
    CHECK_THROWS_AS(top_of(m, -1), std::invalid_argument);
}

TEST(summarize_computes_two_aggregates_in_one_pass, "part2") {
    const Summary s = summarize(T, P, V);
    CHECK_EQ(s.grand_total, 180'000 + 120'000 + 90'500 + 126'000 + 120'000 + 200'000);
    CHECK_EQ(s.largest, std::optional<Trade>(trade(5)));
    const SV et;
    const LL el;
    const Summary e = summarize(et, el, el);
    CHECK_EQ(e.grand_total, 0);
    CHECK(!e.largest.has_value());
    const long long half = LMAX / 2 + 1;
    const SV ab = {"A", "B"};
    const LL p = {half, half}, v = {1, 1};
    CHECK_THROWS_AS(summarize(ab, p, v), std::overflow_error);
    // a full tie on notional and ticker: the earlier index is the largest event
    const SV tie = {"X", "X"};
    const LL tp = {4, 4}, tv = {1, 1};
    CHECK_EQ(summarize(tie, tp, tv).largest->index, 0);
}

TEST(million_events_hundred_thousand_tickers_in_under_two_seconds, "part2,perf") {
    const Data d = Data::random(0, 1'000'000, 100'000, 100'000, 1000);
    CHECK_WITHIN_MS(2000, {
        const auto top = top_tickers(d.t, d.p, d.v, 50);
        CHECK_EQ(top.size(), 50u);
        for (std::size_t i = 1; i < top.size(); ++i) CHECK_GE(top[i - 1].notional, top[i].notional);
    });
}

// ---- C++-only Part 2

TEST(add_to_borrows_the_key_and_leaves_the_table_untouched_on_overflow, "part2,edge,cpp") {
    Totals m;
    std::string buffer = "AAPLMSFT";
    add_to(m, std::string_view(buffer).substr(0, 4), 5);  // heterogeneous find: no temporary std::string on a hit
    add_to(m, std::string_view(buffer).substr(0, 4), 7);
    buffer[0] = 'X';  // the table owns a copy of its key
    CHECK_EQ(m.size(), 1u);
    CHECK_EQ(m.at("AAPL"), 12);
    add_to(m, "MSFT", LMAX);
    CHECK_THROWS_AS(add_to(m, "AAPL", LMAX), std::overflow_error);
    CHECK_EQ(m.at("AAPL"), 12);  // unchanged
    CHECK_THROWS_AS(add_to(m, "MSFT", 1), std::overflow_error);
    CHECK_EQ(m.at("MSFT"), LMAX);
    CHECK_EQ(m.size(), 2u);
}

TEST(top_of_results_outlive_the_table, "part2,edge,cpp") {
    std::vector<TickerTotal> out;
    {
        Totals m;
        for (int i = 0; i < 50; ++i) m.emplace("a-long-ticker-name-beyond-sso-" + std::to_string(i), i);
        out = top_of(m, 3);
    }  // table (and the nodes the heap pointed into) destroyed
    CHECK_EQ(out.size(), 3u);
    CHECK_EQ(out[0], tt("a-long-ticker-name-beyond-sso-49", 49));
    CHECK_EQ(out[2], tt("a-long-ticker-name-beyond-sso-47", 47));
}

// ================================================ Part 3: sliding window

namespace {

Fill fill(long long time, const char* t, long long p, long long v) { return Fill(time, t, p, v); }

/// One line per Feed: F time ticker price volume | T time | Q time.
std::vector<Feed> parse(const std::string& script) {
    std::vector<Feed> out;
    std::istringstream in(script);
    std::string line;
    while (std::getline(in, line)) {
        std::istringstream ls(line);
        std::string op;
        if (!(ls >> op)) continue;
        if (op == "F") {
            long long time, price, volume;
            std::string ticker;
            ls >> time >> ticker >> price >> volume;
            out.emplace_back(Fill(time, ticker, price, volume));
        } else if (op == "T") {
            long long time;
            ls >> time;
            out.emplace_back(Tick{time});
        } else if (op == "Q") {
            long long time;
            ls >> time;
            out.emplace_back(Ask{time});
        } else {
            throw std::invalid_argument(line);
        }
    }
    return out;
}

using Top = std::vector<TickerTotal>;

}  // namespace

TEST(problem_sample_replay, "part3") {
    // window 10, k 2
    const auto feed = parse(
        "F 1 AAPL 100 2\nF 3 MSFT 50 10\nF 5 AAPL 100 3\nQ 5\nF 12 TSLA 10 10\nQ 12\nQ 15\nQ 40\n");
    const auto answers = SlidingTopK::replay(10, 2, feed);
    CHECK_EQ(answers, (std::vector<Answer>{
                          Answer{5, Top{tt("AAPL", 500), tt("MSFT", 500)}},  // tie: ticker ascending
                          Answer{12, Top{tt("MSFT", 500), tt("AAPL", 300)}},  // t=1 AAPL expired (12-1 >= 10)
                          Answer{15, Top{tt("TSLA", 100)}},                  // 15-5 = 10 >= 10: the boundary expires
                          Answer{40, Top{}}}));
}

TEST(expiry_boundary_is_exactly_the_window_length, "part3,edge") {
    SlidingTopK w(10, 5);
    w.add(fill(100, "A", 1, 1));
    w.advance_to(109);
    CHECK_EQ(w.live_events(), 1);  // 109 - 100 = 9 < 10: alive
    CHECK_EQ(w.total_of("A"), 1);
    w.advance_to(110);
    CHECK_EQ(w.live_events(), 0);  // 110 - 100 = 10 >= 10: expired
    CHECK_EQ(w.total_of("A"), 0);
    CHECK_EQ(w.distinct_tickers(), 0);
}

TEST(window_of_one_keeps_only_the_current_instant, "part3,edge") {
    SlidingTopK w(1, 3);
    w.add(fill(5, "A", 2, 2));
    w.add(fill(5, "B", 1, 1));
    CHECK_EQ(w.top(), (Top{tt("A", 4), tt("B", 1)}));
    w.advance_to(6);
    CHECK(w.top().empty());
}

TEST(same_timestamp_is_allowed_and_time_cannot_go_backwards, "part3,edge") {
    SlidingTopK w(10, 2);
    w.add(fill(7, "A", 1, 1));
    w.add(fill(7, "A", 1, 1));
    CHECK_EQ(w.total_of("A"), 2);
    CHECK_THROWS_AS(w.add(fill(6, "A", 1, 1)), std::invalid_argument);
    CHECK_THROWS_AS(w.advance_to(6), std::invalid_argument);
    CHECK_EQ(w.total_of("A"), 2);  // failed calls changed nothing
    CHECK_EQ(w.now(), 7);
}

TEST(ranking_changes_as_old_fills_expire, "part3,edge") {
    SlidingTopK w(10, 2);
    w.add(fill(0, "BIG", 1000, 1));
    w.add(fill(4, "MID", 100, 1));
    w.add(fill(8, "SMALL", 10, 1));
    CHECK_EQ(w.top(), (Top{tt("BIG", 1000), tt("MID", 100)}));
    w.advance_to(10);  // BIG expires
    CHECK_EQ(w.top(), (Top{tt("MID", 100), tt("SMALL", 10)}));
    w.add(fill(11, "BIG", 50, 1));  // BIG is back with a smaller total
    CHECK_EQ(w.top(), (Top{tt("MID", 100), tt("BIG", 50)}));
}

TEST(partial_expiry_of_one_ticker_lowers_its_total_but_keeps_it, "part3,edge") {
    SlidingTopK w(10, 3);
    w.add(fill(0, "A", 100, 1));
    w.add(fill(5, "A", 7, 1));
    w.advance_to(10);
    CHECK_EQ(w.total_of("A"), 7);
    CHECK_EQ(w.top(), (Top{tt("A", 7)}));
    CHECK_EQ(w.distinct_tickers(), 1);
}

TEST(equal_totals_are_ordered_by_ticker, "part3,edge") {
    SlidingTopK w(100, 3);
    w.add(fill(1, "C", 5, 1));
    w.add(fill(1, "A", 5, 1));
    w.add(fill(1, "B", 5, 1));
    CHECK_EQ(w.top(), (Top{tt("A", 5), tt("B", 5), tt("C", 5)}));
}

TEST(zero_notional_fill_keeps_the_ticker_alive_until_it_expires, "part3,edge") {
    SlidingTopK w(10, 5);
    w.add(fill(0, "A", 0, 100));
    CHECK_EQ(w.top(), (Top{tt("A", 0)}));
    CHECK_EQ(w.distinct_tickers(), 1);
    w.advance_to(10);
    CHECK_EQ(w.distinct_tickers(), 0);
}

TEST(k_zero_and_bad_constructor_arguments, "part3,edge") {
    SlidingTopK w(10, 0);
    w.add(fill(1, "A", 1, 1));
    CHECK(w.top().empty());
    CHECK_THROWS_AS(SlidingTopK(0, 1), std::invalid_argument);
    CHECK_THROWS_AS(SlidingTopK(10, -1), std::invalid_argument);
    CHECK_THROWS_AS(fill(-1, "A", 1, 1), std::invalid_argument);
    CHECK_THROWS_AS(fill(1, "A", -1, 1), std::invalid_argument);
    CHECK_THROWS_AS(fill(1, "A", 1, -1), std::invalid_argument);
    CHECK_THROWS_AS(fill(1, "A", LMAX, 2), std::overflow_error);
}

TEST(total_overflow_inside_the_window_is_atomic_and_recovers_after_expiry, "part3,edge") {
    const long long half = LMAX / 2 + 1;
    SlidingTopK w(10, 3);
    w.add(fill(0, "A", half, 1));
    CHECK_THROWS_AS(w.add(fill(1, "A", half, 1)), std::overflow_error);
    // nothing was damaged: A is still `half`, one live fill, exactly one ranking entry
    CHECK_EQ(w.total_of("A"), half);
    CHECK_EQ(w.live_events(), 1);
    CHECK_EQ(w.top(), (Top{tt("A", half)}));
    w.add(fill(10, "A", half, 1));  // the first fill expires at t = 10, so this one fits
    CHECK_EQ(w.total_of("A"), half);
    CHECK_EQ(w.top(), (Top{tt("A", half)}));
}

TEST(replay_tick_guard_and_backwards_time, "part3,edge") {
    const auto answers = SlidingTopK::replay(5, 1, parse("T 0\nF 0 A 1 1\nT 0\nQ 0\n"));
    CHECK_EQ(answers, (std::vector<Answer>{Answer{0, Top{tt("A", 1)}}}));
    CHECK_THROWS_AS(SlidingTopK::replay(5, 1, parse("T 9\nQ 3\n")), std::invalid_argument);
    CHECK(SlidingTopK::replay(5, 1, {}).empty());
}

TEST(random_against_recompute_from_scratch, "part3") {
    for (unsigned seed = 21; seed <= 28; ++seed) {
        std::mt19937 rnd(seed);
        const long long window = 1 + static_cast<long long>(rnd() % 30);
        const int k = static_cast<int>(rnd() % 6);
        SlidingTopK w(window, k);
        std::vector<Fill> fills;
        long long time = 0;
        const auto& names = names_of(8);
        for (int step = 0; step < 1500; ++step) {
            time += static_cast<long long>(rnd() % 4);  // equal timestamps happen
            if (rnd() % 4 == 0) {
                w.advance_to(time);
            } else {
                Fill f(time, names[rnd() % 8], static_cast<long long>(rnd() % 4), static_cast<long long>(rnd() % 4));
                w.add(f);
                fills.push_back(std::move(f));
            }
            std::map<std::string, long long> totals;
            int live = 0;
            for (const Fill& f : fills)
                if (time - f.time < window) { totals[f.ticker] += f.notional(); ++live; }
            Top expect;
            for (const auto& [name, total] : totals) expect.emplace_back(name, total);
            std::sort(expect.begin(), expect.end(), BestTickerFirst{});
            truncate(expect, static_cast<std::size_t>(k));
            CHECK_EQ(expect, w.top(), "seed " + std::to_string(seed) + " step " + std::to_string(step));
            CHECK_EQ(live, w.live_events());
            CHECK_EQ(static_cast<int>(totals.size()), w.distinct_tickers());
        }
    }
}

TEST(million_fills_with_a_sliding_window_in_under_two_seconds, "part3,perf") {
    const int n = 1'000'000;
    std::mt19937 rnd(0);
    const auto& names = names_of(2000);
    std::vector<Feed> feed;
    feed.reserve(static_cast<std::size_t>(n + n / 100));
    long long time = 0;
    for (int i = 0; i < n; ++i) {
        time += static_cast<long long>(rnd() % 3);
        feed.emplace_back(Fill(time, names[rnd() % 2000], 1 + static_cast<long long>(rnd() % 1000), 1 + static_cast<long long>(rnd() % 100)));
        if (i % 100 == 99) feed.emplace_back(Ask{time});
    }
    CHECK_WITHIN_MS(2000, {
        const auto answers = SlidingTopK::replay(5000, 10, feed);
        CHECK_EQ(answers.size(), static_cast<std::size_t>(n / 100));
        CHECK_LE(answers.back().top.size(), 10u);
    });
}

// ---- C++-only Part 3

TEST(the_class_holds_views_into_its_own_nodes_so_it_is_not_copyable_or_movable, "part3,edge,cpp") {
    static_assert(!std::is_copy_constructible_v<SlidingTopK>);
    static_assert(!std::is_copy_assignable_v<SlidingTopK>);
    static_assert(!std::is_move_constructible_v<SlidingTopK>);
    static_assert(!std::is_move_assignable_v<SlidingTopK>);
    CHECK(true);
}

TEST(zero_notional_fill_on_a_live_ticker_does_not_lose_its_ranking_entry, "part3,edge,cpp") {
    // The trap: "insert the new key, then erase the old one" with old == new erases the only entry.
    SlidingTopK w(100, 5);
    w.add(fill(0, "A", 5, 2));
    w.add(fill(1, "A", 0, 9));  // total stays 10
    CHECK_EQ(w.top(), (Top{tt("A", 10)}));
    CHECK_EQ(w.total_of("A"), 10);
    w.advance_to(100);  // the first fill expires (100 - 0 >= 100): the zero fill now carries the ticker alone
    CHECK_EQ(w.top(), (Top{tt("A", 0)}));
    CHECK_EQ(w.distinct_tickers(), 1);
    w.advance_to(101);
    CHECK(w.top().empty());
}

TEST(ranking_entries_never_dangle_when_ticker_nodes_come_and_go, "part3,edge,cpp") {
    // Hundreds of distinct tickers entering and leaving a short window: every map node is erased and recreated many
    // times while the set still holds views into the surviving ones.  ASan finds a view into a freed node.
    SlidingTopK w(7, 4);
    std::mt19937 rnd(5);
    const auto& names = names_of(300);
    std::vector<Fill> fills;
    long long time = 0;
    for (int step = 0; step < 4000; ++step) {
        time += static_cast<long long>(rnd() % 3);
        Fill f(time, names[rnd() % 300], 1 + static_cast<long long>(rnd() % 9), 1 + static_cast<long long>(rnd() % 3));
        w.add(f);
        fills.push_back(std::move(f));
        if (step % 50 == 0) {
            std::map<std::string, long long> totals;
            for (const Fill& x : fills)
                if (time - x.time < 7) totals[x.ticker] += x.notional();
            Top expect;
            for (const auto& [name, total] : totals) expect.emplace_back(name, total);
            std::sort(expect.begin(), expect.end(), BestTickerFirst{});
            truncate(expect, 4);
            CHECK_EQ(expect, w.top(), "step " + std::to_string(step));
        }
    }
}

TEST(ranking_compares_tickers_bytewise, "part3,edge,cpp") {
    SlidingTopK w(10, 3);
    w.add(fill(0, "\xC3\xA9", 1, 1));
    w.add(fill(0, "Z", 1, 1));
    w.add(fill(0, "", 1, 1));
    CHECK_EQ(tickers_of(w.top()), (std::vector<std::string>{"", "Z", "\xC3\xA9"}));
}

TEST(a_throwing_fill_construction_never_reaches_the_window, "part3,edge,cpp") {
    SlidingTopK w(10, 2);
    w.add(fill(1, "A", 1, 1));
    CHECK_THROWS_AS(w.add(Fill(2, "B", LMAX, 2)), std::overflow_error);  // thrown while building the argument
    CHECK_EQ(w.live_events(), 1);
    CHECK_EQ(w.now(), 1);
}

// ================================================ Part 4: parallel chunks

namespace {

using Fn = Totals (*)(Strings, Longs, Longs, int);

struct Impl {
    const char* name;
    Totals (*run)(Strings, Longs, Longs, int chunks);
};

Totals run_chunked(Strings t, Longs p, Longs v, int chunks) { return totals_chunked(t, p, v, chunks); }
Totals run_recursive(Strings t, Longs p, Longs v, int chunks) {
    return totals_recursive(t, p, v, static_cast<int>(std::max<std::size_t>(1, t.size() / static_cast<std::size_t>(std::max(1, chunks)))));
}
Totals run_sharded(Strings t, Longs p, Longs v, int chunks) { return totals_sharded(t, p, v, chunks); }

const Impl IMPLS[] = {{"chunked", run_chunked}, {"recursive", run_recursive}, {"sharded", run_sharded}};

}  // namespace

TEST(sample_totals, "part4") {
    Totals expect;
    expect.emplace("AAPL", 270'500);
    expect.emplace("MSFT", 240'000);
    expect.emplace("TSLA", 200'000);
    expect.emplace("GOOG", 126'000);
    for (const Impl& impl : IMPLS)
        for (int chunks : {1, 2, 3, 6, 10}) CHECK_EQ(dump(impl.run(T, P, V, chunks)), dump(expect), std::string(impl.name) + " chunks=" + std::to_string(chunks));
    CHECK_EQ(dump(totals_sequential(T, P, V)), dump(expect));
}

TEST(empty_input_and_more_chunks_than_events, "part4,edge") {
    const SV et;
    const LL el;
    const SV a = {"A"};
    const LL p = {2}, v = {3};
    for (const Impl& impl : IMPLS) {
        CHECK(impl.run(et, el, el, 4).empty(), impl.name);
        CHECK_EQ(dump(impl.run(a, p, v, 16)), std::string("A=6,"), impl.name);
    }
}

TEST(invalid_events_fail_the_whole_call, "part4,edge") {
    const SV t = {"A", "B", "C", "D"};
    const LL ok = {1, 1, 1, 1}, negp = {1, 1, -1, 1}, negv = {1, 1, 1, -1}, short1 = {1};
    for (const Impl& impl : IMPLS) {
        CHECK_THROWS_AS(impl.run(t, negp, ok, 2), std::invalid_argument, impl.name);
        CHECK_THROWS_AS(impl.run(t, ok, negv, 2), std::invalid_argument, impl.name);
        CHECK_THROWS_AS(impl.run(t, short1, ok, 2), std::invalid_argument, impl.name);
    }
}

TEST(overflow_inside_one_event_and_only_at_merge_time_are_both_detected, "part4,edge") {
    const long long half = LMAX / 2 + 1;
    const SV ab = {"A", "B"}, aa = {"A", "A"};
    for (const Impl& impl : IMPLS) {
        const LL p1 = {LMAX, 1}, v1 = {2, 1};
        CHECK_THROWS_AS(impl.run(ab, p1, v1, 2), std::overflow_error, impl.name);  // one event overflows
        // each event and each chunk's partial sum fits; only combining the two chunks overflows
        const LL p2 = {half, half}, v2 = {1, 1};
        CHECK_THROWS_AS(impl.run(aa, p2, v2, 2), std::overflow_error, impl.name);
        CHECK_EQ(dump(impl.run(ab, p2, v2, 2)), "A=" + std::to_string(half) + ",B=" + std::to_string(half) + ",", impl.name);
    }
}

TEST(total_exactly_llong_max_is_accepted_whatever_the_split, "part4,edge") {
    const SV t = {"A", "A", "A", "A"};
    const LL ok = {LMAX - 6, 1, 2, 3}, over = {LMAX - 6, 1, 2, 4}, v = {1, 1, 1, 1};
    for (const Impl& impl : IMPLS)
        for (int chunks : {1, 2, 3, 4}) {
            CHECK_EQ(dump(impl.run(t, ok, v, chunks)), "A=" + std::to_string(LMAX) + ",", std::string(impl.name) + " chunks=" + std::to_string(chunks));
            CHECK_THROWS_AS(impl.run(t, over, v, chunks), std::overflow_error, std::string(impl.name) + " chunks=" + std::to_string(chunks));
        }
}

TEST(shuffle_and_chunking_never_change_the_answer, "part4") {
    for (unsigned seed = 31; seed <= 35; ++seed) {
        const Data d = Data::random(seed, 5000, 50, 1000, 100);
        const std::string expect = dump(totals_sequential(d.t, d.p, d.v));
        std::vector<std::size_t> order(d.t.size());
        std::iota(order.begin(), order.end(), std::size_t{0});
        std::shuffle(order.begin(), order.end(), std::mt19937(seed));
        SV t;
        LL p, v;
        for (std::size_t i : order) { t.push_back(d.t[i]); p.push_back(d.p[i]); v.push_back(d.v[i]); }
        for (const Impl& impl : IMPLS)
            for (int chunks : {1, 2, 7, 64}) CHECK_EQ(dump(impl.run(t, p, v, chunks)), expect, std::string(impl.name) + " chunks=" + std::to_string(chunks));
    }
}

TEST(parallel_top_k_equals_sequential_top_k_even_with_many_ties, "part4") {
    for (unsigned seed = 41; seed <= 44; ++seed) {
        const Data d = Data::random(seed, 3000, 200, 3, 3);  // tiny value range: many equal totals
        for (int k : {1, 5, 50, 500})
            CHECK_EQ(top_tickers(d.t, d.p, d.v, k), top_tickers_parallel(d.t, d.p, d.v, k, 8), "k " + std::to_string(k));
    }
}

TEST(argument_checks, "part4,edge") {
    CHECK_THROWS_AS(totals_chunked(T, P, V, 0), std::invalid_argument);
    CHECK_THROWS_AS(totals_sharded(T, P, V, 0), std::invalid_argument);
    CHECK_THROWS_AS(totals_recursive(T, P, V, 0), std::invalid_argument);
    CHECK_THROWS_AS(top_tickers_parallel(T, P, V, -1, 2), std::invalid_argument);
}

TEST(chunk_boundaries_cover_every_index_exactly_once, "part4,edge") {
    for (std::size_t n : {std::size_t{0}, std::size_t{1}, std::size_t{5}, std::size_t{10}, std::size_t{1'000'003}})
        for (int chunks : {1, 2, 3, 7, 64}) {
            CHECK_EQ(boundary(n, chunks, 0), 0u);
            CHECK_EQ(boundary(n, chunks, chunks), n);
            for (int c = 0; c < chunks; ++c) CHECK_LE(boundary(n, chunks, c), boundary(n, chunks, c + 1));
        }
    CHECK_EQ(boundary(2'000'000'000, 4, 3), 1'500'000'000u);
    // n * c does not fit in 32 bits, and not even in 63 bits' worth of signed int arithmetic if done carelessly
    CHECK_EQ(boundary(std::size_t{1} << 40, 1000, 999), (std::size_t{1} << 40) / 1000 * 999 + ((std::size_t{1} << 40) % 1000) * 999 / 1000);
}

// ---- concurrency

TEST(many_callers_at_once_all_get_the_sequential_answer, "part4,conc") {
    for (int rep = 1; rep <= 8; ++rep) {
        const Data d = Data::random(static_cast<unsigned>(rep), 8000, 300, 5000, 200);
        const std::string expect = dump(totals_sequential(d.t, d.p, d.v));
        constexpr int callers = 6;
        std::atomic<bool> go{false};
        std::atomic<int> failures{0};
        mt::ThreadErrors errors;
        std::vector<std::thread> threads;
        for (int c = 0; c < callers; ++c) {
            const Impl& impl = IMPLS[c % 3];
            threads.push_back(errors.spawn([&, impl] {
                while (!go.load()) std::this_thread::yield();
                for (int round = 0; round < 3; ++round)
                    if (dump(impl.run(d.t, d.p, d.v, 4 + round)) != expect) failures.fetch_add(1);
            }));
        }
        go.store(true);
        for (auto& th : threads) th.join();
        CHECK_NO_THREAD_ERRORS(errors);
        CHECK_EQ(failures.load(), 0);
    }
}

TEST(failing_calls_do_not_contaminate_concurrent_good_calls, "part4,conc") {
    for (int rep = 1; rep <= 8; ++rep) {
        const Data good = Data::random(100 + static_cast<unsigned>(rep), 6000, 100, 1000, 100);
        const std::string expect = dump(totals_sequential(good.t, good.p, good.v));
        LL bad_p = good.p, bad_v = good.v;
        bad_p[bad_p.size() / 2] = LMAX;
        bad_v[bad_v.size() / 2] = 2;
        std::atomic<bool> go{false};
        std::atomic<int> wrong{0};
        mt::ThreadErrors errors;
        std::vector<std::thread> threads;
        for (int c = 0; c < 6; ++c) {
            const bool bad = c % 2 == 0;
            const Impl& impl = IMPLS[c % 3];
            threads.push_back(errors.spawn([&, bad, impl] {
                while (!go.load()) std::this_thread::yield();
                if (bad) {
                    try {
                        (void)impl.run(good.t, bad_p, bad_v, 5);
                        wrong.fetch_add(1);  // must throw
                    } catch (const std::overflow_error&) {
                    }
                } else if (dump(impl.run(good.t, good.p, good.v, 5)) != expect) {
                    wrong.fetch_add(1);
                }
            }));
        }
        go.store(true);
        for (auto& th : threads) th.join();
        CHECK_NO_THREAD_ERRORS(errors);
        CHECK_EQ(wrong.load(), 0);
    }
}

TEST(a_failing_chunk_stops_the_others_without_hanging_or_terminating, "part4,conc") {
    // Chunk 0 fails on its first event; the other chunks are long.  200 calls: each must throw overflow_error, join every
    // thread, and leave the process alive (an exception escaping a std::thread body would call std::terminate).
    const std::size_t n = 200'000;
    SV t(n, std::string_view("A"));
    LL p(n, 1), v(n, 1);
    p[0] = LMAX;
    v[0] = 2;
    for (int i = 0; i < 200; ++i) {
        CHECK_THROWS_AS(totals_chunked(t, p, v, 4), std::overflow_error);
        CHECK_THROWS_AS(totals_sharded(t, p, v, 4), std::overflow_error);
    }
}

TEST(several_chunks_failing_at_once_report_one_of_the_errors, "part4,conc,cpp") {
    // Chunk 0 overflows, chunk 1 has a negative price.  Either may be reported (the loser may be cancelled before it
    // looks at its bad event) but exactly one exception comes out and nothing is leaked.
    const std::size_t n = 20'000;
    SV t(n, std::string_view("A"));
    LL p(n, 1), v(n, 1);
    p[0] = LMAX;
    v[0] = 2;
    p[n / 2 + 1] = -5;
    for (int i = 0; i < 100; ++i) {
        bool got_overflow = false, got_invalid = false, other = false;
        try {
            (void)totals_chunked(t, p, v, 2);
        } catch (const std::overflow_error&) { got_overflow = true; }
        catch (const std::invalid_argument&) { got_invalid = true; }
        catch (...) { other = true; }
        CHECK(got_overflow != got_invalid, "exactly one of the two errors");
        CHECK(!other);
    }
}

TEST(worker_threads_are_joined_before_the_function_returns, "part4,conc,cpp") {
    // If a worker outlived the call it would write into `parts` after the vector was destroyed (ASan / TSan).  Many
    // short calls with more chunks than events make the window obvious.
    const SV a = {"A", "B", "C"};
    const LL p = {1, 2, 3}, v = {1, 1, 1};
    for (int i = 0; i < 300; ++i) CHECK_EQ(dump(totals_chunked(a, p, v, 16)), std::string("A=1,B=2,C=3,"));
}

// ---- performance

TEST(two_million_events_in_under_two_seconds, "part4,perf") {
    const Data d = Data::random(0, 2'000'000, 50'000, 100'000, 1000);
    for (const Impl& impl : IMPLS) {
        CHECK_WITHIN_MS(2000, {
            const Totals m = impl.run(d.t, d.p, d.v, 8);
            CHECK_GT(m.size(), 40'000u);
        });
    }
}

TEST(cancellation_is_much_faster_than_finishing_the_work, "part4,perf,conc") {
    const std::size_t n = 4'000'000;
    SV t(n, std::string_view("A"));
    LL p(n, 1), v(n, 1);
    using Clock = std::chrono::steady_clock;
    auto time_of = [&](auto&& fn) {
        const auto t0 = Clock::now();
        fn();
        return std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
    };
    const double ok_ms = time_of([&] { (void)totals_chunked(t, p, v, 4); });
    p[0] = LMAX;
    v[0] = 2;
    const double fail_ms = time_of([&] { CHECK_THROWS_AS(totals_chunked(t, p, v, 4), std::overflow_error); });
    CHECK(fail_ms < ok_ms / 2 + 5, "failed call " + std::to_string(fail_ms) + " ms vs full run " + std::to_string(ok_ms) + " ms");
}

MT_MAIN()
