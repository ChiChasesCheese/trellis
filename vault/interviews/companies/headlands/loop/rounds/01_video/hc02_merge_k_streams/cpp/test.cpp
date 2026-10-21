// hc02 · Merge K sorted streams — C++20 tests.  Same cases as test/MergeKTest.java plus C++-only edge cases (tag "cpp"):
// a type with only operator<, copies per element, an immovable merger, ranges (views::take), sticky exceptions, owning vs
// borrowing adapters, exceptions that are not std::exception, destructor-joins-threads, stop-token cancellation.
#include <algorithm>
#include <atomic>
#include <chrono>
#include <climits>
#include <condition_variable>
#include <deque>
#include <functional>
#include <latch>
#include <mutex>
#include <random>
#include <thread>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace mergek;

namespace {

using L = std::vector<std::vector<int>>;
using Rng = std::mt19937_64;
int rnd(Rng& g, int n) { return static_cast<int>(g() % static_cast<unsigned>(n)); }

// ---------------------------------------------------------------- helpers
struct Rec {
    int key;
    std::string tag;
};
struct ByKey {  // compares the key only, so ties are visible in the tags
    bool operator()(const Rec& a, const Rec& b) const { return a.key < b.key; }
};
struct OnlyLess {  // the only operation is operator<: merge must not use ==, >, <= or subtraction
    int v;
    bool operator<(const OnlyLess& o) const { return v < o.v; }
};
struct Counted {  // counts copies and moves
    int v;
    static inline int copies = 0, moves = 0;
    explicit Counted(int x) : v(x) {}
    Counted(const Counted& o) : v(o.v) { ++copies; }
    Counted(Counted&& o) noexcept : v(o.v) { ++moves; }
    Counted& operator=(const Counted& o) { v = o.v; ++copies; return *this; }
    Counted& operator=(Counted&& o) noexcept { v = o.v; ++moves; return *this; }
    bool operator<(const Counted& o) const { return v < o.v; }
};

/// Obviously correct reference: concatenate, then stable sort.
template <class T, class Less = std::less<T>>
std::vector<T> oracle(const std::vector<std::vector<T>>& lists, Less less = {}) {
    std::vector<T> all;
    for (const auto& l : lists) all.insert(all.end(), l.begin(), l.end());
    std::stable_sort(all.begin(), all.end(), less);
    return all;
}

L random_sorted_lists(Rng& g, int k, int max_len, int bound) {
    L lists;
    for (int i = 0; i < k; ++i) {
        std::vector<int> l;
        const int n = rnd(g, max_len + 1);
        for (int j = 0; j < n; ++j) l.push_back(rnd(g, bound));
        std::sort(l.begin(), l.end());
        lists.push_back(std::move(l));
    }
    return lists;
}

std::vector<std::vector<long long>> to_longs(const L& lists) {
    std::vector<std::vector<long long>> out;
    for (const auto& l : lists) out.emplace_back(l.begin(), l.end());
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

/// A source that counts how many elements were pulled from it.
struct Counting {
    std::shared_ptr<std::vector<int>> data;
    std::shared_ptr<std::atomic<int>> pulls = std::make_shared<std::atomic<int>>(0);
    explicit Counting(std::vector<int> d) : data(std::make_shared<std::vector<int>>(std::move(d))) {}
    Source<int> source() const {
        return [d = data, p = pulls, i = std::size_t{0}]() mutable -> std::optional<int> {
            if (i == d->size()) return std::nullopt;
            ++*p;
            return (*d)[i++];
        };
    }
    int count() const { return pulls->load(); }
};

Source<int> src_of(std::vector<int> v) { return from_range(std::move(v)); }

std::vector<Source<int>> sources_of(const L& lists) {
    std::vector<Source<int>> out;
    for (const auto& l : lists) out.push_back(src_of(l));
    return out;
}

template <class M>
std::vector<int> drain(M& m) {
    std::vector<int> out;
    while (m.has_next()) out.push_back(m.next());
    return out;
}

template <class P>
bool wait_until(P pred, int ms = 5000) {
    const auto end = std::chrono::steady_clock::now() + std::chrono::milliseconds(ms);
    while (!pred()) {
        if (std::chrono::steady_clock::now() > end) return false;
        std::this_thread::yield();
    }
    return true;
}

/// Kills the process when a test hangs (a deadlocked merge must fail loudly, not stall the suite).
struct Watchdog {
    std::jthread t;
    explicit Watchdog(int ms, const char* what)
        : t([ms, what](std::stop_token st) {
              std::mutex m;
              std::condition_variable_any cv;
              std::unique_lock lk(m);
              cv.wait_for(lk, st, std::chrono::milliseconds(ms), [] { return false; });
              if (!st.stop_requested()) {
                  std::fprintf(stderr, "WATCHDOG: %s still running after %d ms (deadlock?)\n", what, ms);
                  std::_Exit(124);
              }
          }) {}
};

// ---------------------------------------------------------------- blocking sources
BlockingSource<int> plain(std::vector<int> v) {
    return [v = std::move(v), i = std::size_t{0}](std::stop_token) mutable -> std::optional<int> {
        if (i == v.size()) return std::nullopt;
        return v[i++];
    };
}

/// A source fed by the test thread: blocks until a value arrives, wakes up (and notes it) when cancelled.
struct Gated {
    std::mutex mu;
    std::condition_variable_any cv;
    std::deque<std::optional<int>> feed;
    std::atomic<bool> interrupted{false};

    void give(int v) { push(v); }
    void end() { push(std::nullopt); }
    BlockingSource<int> source() {
        return [this](std::stop_token st) -> std::optional<int> {
            std::unique_lock lk(mu);
            if (!cv.wait(lk, st, [&] { return !feed.empty(); })) {
                interrupted = true;
                return std::nullopt;
            }
            auto o = feed.front();
            feed.pop_front();
            return o;
        };
    }

private:
    void push(std::optional<int> o) {
        { std::lock_guard lk(mu); feed.push_back(o); }
        cv.notify_all();
    }
};

/// Waits for the starting gun, then yields at random between elements to shuffle the thread interleavings.
BlockingSource<int> jittery(std::vector<int> data, std::shared_ptr<std::latch> gate, unsigned seed) {
    return [data = std::move(data), gate, g = Rng(seed), i = std::size_t{0}, passed = false](std::stop_token) mutable -> std::optional<int> {
        if (!passed) { gate->wait(); passed = true; }
        if (g() % 4 == 0) std::this_thread::yield();
        if (i == data.size()) return std::nullopt;
        return data[i++];
    };
}

std::vector<BlockingSource<int>> plain_sources(const L& lists) {
    std::vector<BlockingSource<int>> out;
    for (const auto& l : lists) out.push_back(plain(l));
    return out;
}

template <class M>
std::vector<int> drain_blocking(M& m, std::vector<int>* streams = nullptr) {
    std::vector<int> out;
    for (;;) {
        Poll<int> p = m.next();
        if (auto* r = std::get_if<Ready<int>>(&p)) {
            out.push_back(r->value);
            if (streams) streams->push_back(r->stream);
        } else if (std::holds_alternative<Done>(p)) {
            return out;
        } else {
            throw std::logic_error("next() must not return Pending");
        }
    }
}

}  // namespace

// ===================================================================================== Part 1: merge k lists

TEST(sample_from_problem_statement, "part1") {
    const L a{{1, 4, 7}, {2, 5, 8}, {3, 6, 9}};
    CHECK_EQ(merge(a), (std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8, 9}));
    const L b{{1, 4, 5}, {1, 3, 4}, {2, 6}};
    CHECK_EQ(merge(b), (std::vector<int>{1, 1, 2, 3, 4, 4, 5, 6}));
}

TEST(degenerate_shapes, "part1,edge") {
    CHECK_EQ(merge(L{}), std::vector<int>{});                  // k = 0
    CHECK_EQ(merge(L{{}, {}}), std::vector<int>{});            // every list empty
    CHECK_EQ(merge(L{{}, {3}, {}}), std::vector<int>{3});
    CHECK_EQ(merge(L{{1, 2, 3}}), (std::vector<int>{1, 2, 3}));  // k = 1
    CHECK_EQ(merge(L{{-5, 7, 7}, {-5, 0, 7}}), (std::vector<int>{-5, -5, 0, 7, 7, 7}));
}

TEST(extremes_do_not_overflow_comparisons, "part1,edge") {
    // a - b < 0 overflows here (and signed overflow is undefined behaviour in C++)
    using LL = std::vector<std::vector<long long>>;
    const LL a{{LLONG_MIN, LLONG_MAX}, {-1, LLONG_MAX}};
    CHECK_EQ(merge(a), (std::vector<long long>{LLONG_MIN, -1, LLONG_MAX, LLONG_MAX}));
    const LL b{{LLONG_MIN, LLONG_MAX}, {0}};
    CHECK_EQ(merge_longs(b), (std::vector<long long>{LLONG_MIN, 0, LLONG_MAX}));
}

TEST(equal_elements_come_out_in_stream_order, "part1,edge") {
    const std::vector<std::vector<Rec>> in{{{1, "a1"}, {2, "a2"}, {2, "a3"}}, {{1, "b1"}, {2, "b2"}}, {{2, "c1"}}};
    auto tags = [](const std::vector<Rec>& v) {
        std::vector<std::string> t;
        for (const auto& r : v) t.push_back(r.tag);
        return t;
    };
    CHECK_EQ(tags(merge(in, ByKey{})), (std::vector<std::string>{"a1", "b1", "a2", "a3", "b2", "c1"}));
    const std::vector<std::vector<Rec>> swapped{in[2], in[1], in[0]};
    CHECK_EQ(tags(merge(swapped, ByKey{})), (std::vector<std::string>{"b1", "a1", "c1", "b2", "a2", "a3"}));
}

TEST(unsorted_input_is_reported_with_location, "part1,edge") {
    const L bad{{1, 2, 3}, {5, 9, 4, 10}};
    auto ex = thrown<UnsortedInputException>([&] { merge(bad); });
    REQUIRE(ex.has_value());
    CHECK_EQ(ex->stream(), 1);
    CHECK_EQ(ex->position(), 2u);
    const std::vector<std::vector<long long>> bad2{{1, 2}, {3, 2}};
    auto ex2 = thrown<UnsortedInputException>([&] { merge_longs(bad2); });
    REQUIRE(ex2.has_value());
    CHECK_EQ(ex2->stream(), 1);
    CHECK_EQ(ex2->position(), 1u);
}

TEST(inputs_are_not_modified, "part1,edge") {
    const L in{{1, 3}, {2}};
    const L copy = in;
    (void)merge(in);
    CHECK(in == copy);
    static_assert(std::is_same_v<decltype(merge(in)), std::vector<int>>);
}

TEST(random_matches_stable_sort_oracle_and_primitive_version, "part1,edge") {
    Rng g(11);
    for (int round = 0; round < 300; ++round) {
        const L lists = random_sorted_lists(g, rnd(g, 12), 30, 15);
        const auto expected = oracle(lists);
        CHECK_EQ(merge(lists), expected);
        const auto longs = to_longs(lists);
        const auto got = merge_longs(longs);
        CHECK_EQ(got, std::vector<long long>(expected.begin(), expected.end()));
    }
}

TEST(a_type_with_only_operator_less_works, "part1,cpp") {
    const std::vector<std::vector<OnlyLess>> in{{{1}, {3}}, {{2}, {3}}};
    const auto out = merge(in);
    std::vector<int> vs;
    for (const auto& x : out) vs.push_back(x.v);
    CHECK_EQ(vs, (std::vector<int>{1, 2, 3, 3}));
}

TEST(descending_streams_with_a_custom_comparator, "part1,cpp") {
    const L in{{9, 5, 1}, {8, 5, 2}, {}};
    CHECK_EQ(merge(in, std::greater<int>{}), (std::vector<int>{9, 8, 5, 5, 2, 1}));
    const L bad{{9, 5, 7}};
    CHECK_THROWS_AS(merge(bad, std::greater<int>{}), UnsortedInputException);
}

TEST(each_element_is_copied_exactly_once, "part1,cpp") {
    std::vector<std::vector<Counted>> in(3);
    for (int s = 0; s < 3; ++s)
        for (int i = 0; i < 100; ++i) in[s].emplace_back(i * 3 + s);
    Counted::copies = Counted::moves = 0;
    const auto out = merge(in);
    CHECK_EQ(out.size(), 300u);
    CHECK_EQ(Counted::copies, 300);  // the one copy into the result; the heap held indices
    CHECK_EQ(Counted::moves, 0);     // reserve(total): no reallocation
    CHECK(std::is_sorted(out.begin(), out.end()));
}

TEST(comparison_count_is_n_log_k_not_n_log_n, "part1,cpp") {
    Rng g(3);
    const L in = random_sorted_lists(g, 2, 40000, 1'000'000);
    long calls = 0;
    const auto out = merge(in, [&](int a, int b) { ++calls; return a < b; });
    const long n = static_cast<long>(out.size());
    CHECK_GT(n, 10000);
    CHECK_LE(calls, 8 * n);  // k = 2: a handful of comparisons per element; concatenate-and-sort needs ~log2(n) = 16+
}

TEST(million_elements_in_thousand_lists_under_two_seconds, "part1,perf") {
    Rng g(0);
    L lists;
    for (int i = 0; i < 1000; ++i) {
        std::vector<int> v(1000);
        for (auto& x : v) x = rnd(g, 1'000'000);
        std::sort(v.begin(), v.end());
        lists.push_back(std::move(v));
    }
    const auto longs = to_longs(lists);
    CHECK_WITHIN_MS(2000, auto merged = merge(lists); CHECK_EQ(merged.size(), 1'000'000u); CHECK(std::is_sorted(merged.begin(), merged.end())););
    CHECK_WITHIN_MS(2000, auto merged = merge_longs(longs); CHECK_EQ(merged.size(), 1'000'000u); CHECK(std::is_sorted(merged.begin(), merged.end())););
}

// ===================================================================================== Part 2: lazy merger

TEST(construction_pulls_nothing_and_pulls_are_minimal, "part2") {
    Counting a({1, 4, 7}), b({2, 5, 8}), c({});
    std::vector<Source<int>> srcs{a.source(), b.source(), c.source()};
    Merger<int> m(std::move(srcs));
    CHECK_EQ(a.count() + b.count(), 0);  // nothing at construction
    CHECK_EQ(m.next(), 1);
    CHECK_EQ(a.count(), 1);              // one head per non-empty source
    CHECK_EQ(b.count(), 1);
    CHECK_EQ(m.next(), 2);               // only now does a get its replacement head
    CHECK_EQ(a.count(), 2);
    CHECK_EQ(b.count(), 1);              // b just produced the output: its refill waits for the next call
    CHECK(m.has_next());
    CHECK_EQ(b.count(), 2);
}

TEST(total_pulls_never_exceed_k_plus_consumed, "part2") {
    Rng g(5);
    const L data = random_sorted_lists(g, 7, 40, 100);
    std::vector<Counting> cs;
    for (const auto& d : data) cs.emplace_back(d);
    std::vector<Source<int>> srcs;
    for (auto& c : cs) srcs.push_back(c.source());
    Merger<int> m(std::move(srcs));
    int consumed = 0;
    while (consumed < 50 && m.has_next()) {
        (void)m.next();
        ++consumed;
        int pulls = 0;
        for (auto& c : cs) pulls += c.count();
        CHECK_LE(pulls, static_cast<int>(cs.size()) + consumed - 1, "pulls=" + std::to_string(pulls) + " consumed=" + std::to_string(consumed));
    }
}

TEST(works_on_infinite_streams, "part2") {
    std::vector<Source<int>> srcs;
    srcs.push_back([i = 0]() mutable -> std::optional<int> { int v = i; i += 2; return v; });
    srcs.push_back([i = 0]() mutable -> std::optional<int> { int v = i; i += 3; return v; });
    Merger<int> m(std::move(srcs));
    std::vector<int> first_ten;
    for (int i = 0; i < 10; ++i) first_ten.push_back(m.next());
    CHECK_EQ(first_ten, (std::vector<int>{0, 0, 2, 3, 4, 6, 6, 8, 9, 10}));
}

TEST(has_next_is_idempotent_and_the_end_is_sticky, "part2,edge") {
    std::vector<Source<int>> srcs;
    srcs.push_back(src_of({1}));
    srcs.push_back(src_of({}));
    Merger<int> m(std::move(srcs));
    CHECK(m.has_next());
    CHECK(m.has_next());
    CHECK_EQ(m.next(), 1);
    CHECK(!m.has_next());
    CHECK(!m.has_next());
    CHECK_THROWS_AS(m.next(), std::out_of_range);
    Merger<int> none{std::vector<Source<int>>{}};
    CHECK(!none.has_next());
}

TEST(ties_go_to_the_lower_stream_index, "part2,edge") {
    const std::vector<Rec> a{{1, "a1"}, {1, "a2"}}, b{{1, "b1"}};
    std::vector<Source<Rec>> srcs;
    srcs.push_back(from_range(a));  // lvalue: borrowed
    srcs.push_back(from_range(b));
    Merger<Rec, ByKey> m(std::move(srcs), ByKey{});
    std::vector<std::string> tags;
    while (m.has_next()) tags.push_back(m.next().tag);
    CHECK_EQ(tags, (std::vector<std::string>{"a1", "a2", "b1"}));
}

TEST(unsorted_is_detected_only_when_reached_and_stays_failed, "part2,edge") {
    std::vector<Source<int>> srcs;
    srcs.push_back(src_of({1, 5, 3}));
    srcs.push_back(src_of({2, 4}));
    Merger<int> m(std::move(srcs));
    CHECK_EQ(m.next(), 1);
    CHECK_EQ(m.next(), 2);
    CHECK_EQ(m.next(), 4);
    CHECK_EQ(m.next(), 5);  // the 3 after the 5 has not been read yet
    auto ex = thrown<UnsortedInputException>([&] { m.has_next(); });
    REQUIRE(ex.has_value());
    CHECK_EQ(ex->stream(), 0);
    CHECK_EQ(ex->position(), 2u);
    CHECK_THROWS_AS(m.has_next(), UnsortedInputException);  // sticky: no silently skipping the bad element
    CHECK_THROWS_AS(m.next(), UnsortedInputException);
}

TEST(a_source_exception_propagates_unchanged_and_sticks, "part2,cpp") {
    std::vector<Source<int>> srcs;
    srcs.push_back([i = 0]() mutable -> std::optional<int> {
        if (i == 2) throw std::runtime_error("boom");
        return ++i;
    });
    Merger<int> m(std::move(srcs));
    CHECK_EQ(m.next(), 1);
    CHECK_EQ(m.next(), 2);
    auto ex = thrown<std::runtime_error>([&] { m.next(); });
    REQUIRE(ex.has_value());
    CHECK_EQ(std::string(ex->what()), "boom");
    CHECK_THROWS_AS(m.has_next(), std::runtime_error);
}

TEST(merger_is_an_immovable_input_range, "part2,cpp") {
    static_assert(std::ranges::input_range<Merger<int>>);
    static_assert(!std::is_copy_constructible_v<Merger<int>>);
    static_assert(!std::is_move_constructible_v<Merger<int>>);  // its heap comparator holds `this`
    static_assert(std::input_iterator<Merger<int>::iterator>);
    const L in{{1, 4}, {2, 3}};
    Merger<int> m(sources_of(in));
    std::vector<int> got;
    for (int x : m) got.push_back(x);
    CHECK_EQ(got, (std::vector<int>{1, 2, 3, 4}));
}

TEST(ranges_adapters_make_infinite_streams_and_take_a_prefix, "part2,cpp") {
    auto evens = from_range(std::views::iota(0) | std::views::transform([](int x) { return 2 * x; }));
    auto threes = from_range(std::views::iota(0) | std::views::transform([](int x) { return 3 * x; }));
    std::vector<Source<int>> srcs;
    srcs.push_back(std::move(evens));
    srcs.push_back(std::move(threes));
    Merger<int> m(std::move(srcs));
    std::vector<int> got;
    for (int x : m | std::views::take(8)) got.push_back(x);
    CHECK_EQ(got, (std::vector<int>{0, 0, 2, 3, 4, 6, 6, 8}));
}

TEST(from_range_owns_an_rvalue_and_borrows_an_lvalue, "part2,cpp") {
    auto owned = from_range(std::vector<int>{5, 6});  // the temporary vector is moved into the source
    CHECK_EQ(owned().value(), 5);
    CHECK_EQ(owned().value(), 6);
    CHECK(!owned().has_value());
    std::vector<int> mine{7, 8};
    auto borrowed = from_range(mine);
    CHECK_EQ(borrowed().value(), 7);  // reads the caller's vector in place; the caller must keep it alive
    CHECK_EQ(mine.size(), 2u);        // and it is untouched
}

TEST(the_merger_copies_each_element_at_most_once, "part2,cpp") {
    auto make = [](int base) {
        auto data = std::make_shared<std::vector<Counted>>();
        for (int i = 0; i < 50; ++i) data->emplace_back(base + 3 * i);
        return Source<Counted>([data, i = std::size_t{0}]() mutable -> std::optional<Counted> {
            if (i == data->size()) return std::nullopt;
            return std::optional<Counted>(std::move((*data)[i++]));
        });
    };
    std::vector<Source<Counted>> srcs{make(0), make(1), make(2)};
    Merger<Counted> m(std::move(srcs));
    Counted::copies = Counted::moves = 0;
    int n = 0, prev = -1;
    while (m.has_next()) {
        const int v = m.next().v;
        CHECK_GT(v, prev);
        prev = v;
        ++n;
    }
    CHECK_EQ(n, 150);
    CHECK_LE(Counted::copies, 150);
}

TEST(stream_version_matches_oracle, "part2,edge") {
    Rng g(3);
    for (int round = 0; round < 100; ++round) {
        const L lists = random_sorted_lists(g, rnd(g, 8), 20, 10);
        Merger<int> m(sources_of(lists));
        CHECK_EQ(drain(m), oracle(lists));
    }
}

TEST(million_elements_through_the_merger_under_two_seconds, "part2,perf") {
    Rng g(0);
    L lists;
    for (int i = 0; i < 100; ++i) {
        std::vector<int> v(10000);
        for (auto& x : v) x = rnd(g, 1'000'000);
        std::sort(v.begin(), v.end());
        lists.push_back(std::move(v));
    }
    CHECK_WITHIN_MS(2000, Merger<int> m(sources_of(lists)); long n = 0; int prev = INT_MIN; while (m.has_next()) {
        const int v = m.next();
        CHECK_GE(v, prev);
        prev = v;
        ++n;
    } CHECK_EQ(n, 1'000'000););
}

// ===================================================================================== Part 3: producers + bounded queues

TEST(blocking_next_produces_the_merged_sequence, "part3,conc") {
    Watchdog wd(20000, "blocking_next");
    const L lists{{1, 4, 7}, {2, 5, 8}, {3, 6, 9}};
    ConcurrentMerge<int> m(plain_sources(lists), 2);
    CHECK_EQ(drain_blocking(m), (std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8, 9}));
    CHECK(std::holds_alternative<Done>(m.next()));  // Done stays Done
}

TEST(empty_and_zero_sources_and_bad_capacity, "part3,edge") {
    Watchdog wd(20000, "empty_and_zero");
    {
        ConcurrentMerge<int> m(std::vector<BlockingSource<int>>{}, 1);
        CHECK_EQ(drain_blocking(m), std::vector<int>{});
    }
    {
        ConcurrentMerge<int> m(plain_sources(L{{}, {}}), 1);
        CHECK_EQ(drain_blocking(m), std::vector<int>{});
    }
    CHECK_THROWS_AS(ConcurrentMerge<int>(plain_sources(L{{1}}), 0), std::invalid_argument);
    CHECK_THROWS_AS(ConcurrentMerge<int>(plain_sources(L{{1}}), -3), std::invalid_argument);
}

TEST(try_next_is_pending_until_every_live_stream_has_a_head, "part3,edge,conc") {
    Watchdog wd(20000, "try_next_pending");
    Gated fast, slow;
    fast.give(1);
    fast.give(3);
    fast.end();
    ConcurrentMerge<int> m({fast.source(), slow.source()}, 4);
    // slow has produced nothing: the 1 in `fast` cannot be output (slow may deliver a 0 any moment)
    for (int i = 0; i < 2000; ++i) CHECK(std::holds_alternative<Pending>(m.try_next()));
    slow.give(2);
    slow.end();
    std::vector<int> got;
    CHECK(wait_until([&] {
        Poll<int> p = m.try_next();
        if (auto* r = std::get_if<Ready<int>>(&p)) got.push_back(r->value);
        return std::holds_alternative<Done>(p);  // Pending: let the producers run
    }));
    CHECK_EQ(got, (std::vector<int>{1, 2, 3}));
}

TEST(ready_carries_the_stream_index, "part3,edge") {
    Watchdog wd(20000, "ready_index");
    ConcurrentMerge<int> m(plain_sources(L{{5}, {5}}), 1);
    auto first = std::get<Ready<int>>(m.next());
    auto second = std::get<Ready<int>>(m.next());
    CHECK_EQ(first.stream, 0);  // equal values: the lower stream first
    CHECK_EQ(second.stream, 1);
}

TEST(backpressure_bounds_the_read_ahead, "part3,edge,conc") {
    Watchdog wd(20000, "backpressure");
    auto pulls = std::make_shared<std::atomic<int>>(0);
    BlockingSource<int> src = [pulls, i = 0](std::stop_token) mutable -> std::optional<int> {
        if (i == 1000) return std::nullopt;
        ++*pulls;
        return i++;
    };
    constexpr int capacity = 4;
    ConcurrentMerge<int> m({src}, capacity);
    CHECK(wait_until([&] { return pulls->load() >= capacity + 1; }));  // queue full + one element in the producer's hand
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    CHECK_EQ(pulls->load(), capacity + 1);  // nobody consumes: the producer is stuck in push
    CHECK_EQ(std::get<Ready<int>>(m.next()).value, 0);
}

TEST(a_failing_source_surfaces_after_its_earlier_items, "part3,edge,conc") {
    Watchdog wd(20000, "failing_source");
    BlockingSource<int> boom = [i = 0](std::stop_token) mutable -> std::optional<int> {
        if (i++ == 2) throw std::runtime_error("disk on fire");
        return 10 * i;
    };
    Gated other;  // never ends: only cancellation can free its producer
    other.give(100);
    ConcurrentMerge<int> m({boom, other.source()}, 4);
    std::vector<int> seen;
    auto ex = thrown<MergeException>([&] {
        for (int i = 0; i < 10; ++i) seen.push_back(std::get<Ready<int>>(m.next()).value);
    });
    REQUIRE(ex.has_value());
    CHECK_EQ(seen, (std::vector<int>{10, 20}));  // what boom produced before failing is not lost
    CHECK_EQ(ex->stream(), 0);
    try {
        std::rethrow_exception(ex->cause());
    } catch (const std::runtime_error& e) {
        CHECK_EQ(std::string(e.what()), "disk on fire");
    } catch (...) {
        CHECK(false, "cause has the wrong type");
    }
    CHECK(wait_until([&] { return other.interrupted.load(); }));  // the surviving producer was cancelled
    CHECK_THROWS_AS(m.try_next(), std::logic_error);               // the merge has closed itself
}

TEST(an_unsorted_source_fails_with_an_unsorted_cause, "part3,edge") {
    Watchdog wd(20000, "unsorted_source");
    ConcurrentMerge<int> m(plain_sources(L{{1, 3, 2}}), 2);
    auto ex = thrown<MergeException>([&] { drain_blocking(m); });
    REQUIRE(ex.has_value());
    auto cause = thrown<UnsortedInputException>([&] { std::rethrow_exception(ex->cause()); });
    REQUIRE(cause.has_value());
    CHECK_EQ(cause->position(), 2u);
}

TEST(close_cancels_blocked_producers_and_is_idempotent, "part3,edge,conc") {
    Watchdog wd(20000, "close");
    Gated stuck;
    ConcurrentMerge<int> m({stuck.source()}, 1);
    CHECK(std::holds_alternative<Pending>(m.try_next()));
    m.close();
    m.close();
    CHECK(stuck.interrupted.load());  // close() returns only after the producer has finished
    CHECK_THROWS_AS(m.next(), std::logic_error);
}

TEST(a_throw_that_is_not_a_std_exception_does_not_terminate, "part3,cpp") {
    Watchdog wd(20000, "non_std_throw");
    BlockingSource<int> bad = [](std::stop_token) -> std::optional<int> { throw 42; };
    ConcurrentMerge<int> m({bad}, 1);
    auto ex = thrown<MergeException>([&] { (void)m.next(); });
    REQUIRE(ex.has_value());
    try {
        std::rethrow_exception(ex->cause());
    } catch (int v) {
        CHECK_EQ(v, 42);
    } catch (...) {
        CHECK(false, "cause has the wrong type");
    }
}

TEST(the_destructor_cancels_and_joins_the_producers, "part3,cpp,conc") {
    Watchdog wd(20000, "destructor");
    Gated stuck;
    {
        ConcurrentMerge<int> m({stuck.source()}, 1);
        CHECK(std::holds_alternative<Pending>(m.try_next()));
    }  // no close() call: leaving the scope must not hang and must not leak the thread
    CHECK(stuck.interrupted.load());
}

TEST(close_on_another_thread_wakes_a_blocked_next, "part3,cpp,conc") {
    Watchdog wd(20000, "close_wakes_next");
    Gated stuck;
    ConcurrentMerge<int> m({stuck.source()}, 1);
    std::jthread closer([&] {
        std::this_thread::sleep_for(std::chrono::milliseconds(30));
        m.close();
    });
    CHECK_THROWS_AS(m.next(), std::logic_error);  // would block forever without the stop token in the wait
}

TEST(random_interleavings_give_the_deterministic_stable_merge, "part3,conc") {
    for (unsigned seed = 1; seed <= 25; ++seed) {
        Watchdog wd(30000, "random_interleavings");
        Rng g(seed);
        const L lists = random_sorted_lists(g, 2 + rnd(g, 8), 400, 50);  // small value range: lots of equal elements
        auto gate = std::make_shared<std::latch>(1);
        std::vector<BlockingSource<int>> sources;
        for (std::size_t i = 0; i < lists.size(); ++i) sources.push_back(jittery(lists[i], gate, seed * 100 + static_cast<unsigned>(i)));
        ConcurrentMerge<int> m(std::move(sources), 1 + rnd(g, 6));
        gate->count_down();
        std::vector<int> streams;
        const auto out = drain_blocking(m, &streams);
        CHECK_EQ(out, oracle(lists), "seed " + std::to_string(seed));
        for (std::size_t i = 1; i < out.size(); ++i)
            if (out[i] == out[i - 1]) CHECK_GE(streams[i], streams[i - 1], "tie order at " + std::to_string(i));
    }
}

TEST(eight_streams_of_fifty_thousand_under_two_seconds, "part3,perf") {
    Watchdog wd(30000, "perf_part3");
    Rng g(0);
    L lists;
    for (int i = 0; i < 8; ++i) {
        std::vector<int> v(50000);
        for (auto& x : v) x = rnd(g, 1'000'000);
        std::sort(v.begin(), v.end());
        lists.push_back(std::move(v));
    }
    CHECK_WITHIN_MS(2000, ConcurrentMerge<int> m(plain_sources(lists), 1024); auto out = drain_blocking(m); CHECK_EQ(out.size(), 400000u); CHECK(std::is_sorted(out.begin(), out.end())););
}

// ===================================================================================== Part 4: merge_all (RAII scope)

TEST(merge_all_returns_the_merged_list, "part4") {
    Watchdog wd(20000, "merge_all");
    CHECK_EQ(merge_all<int>(plain_sources(L{{1, 4, 7}, {}, {2, 5, 8}, {3, 6, 9}}), 2), (std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8, 9}));
    CHECK_EQ(merge_all<int>({}, 1), std::vector<int>{});
    CHECK_THROWS_AS(merge_all<int>(plain_sources(L{{1}}), 0), std::invalid_argument);
}

TEST(one_failing_producer_cancels_the_others, "part4,edge,conc") {
    Watchdog wd(20000, "one_failing");
    Gated stuck, stuck2;  // wait forever for data
    BlockingSource<int> boom = [](std::stop_token) -> std::optional<int> { throw std::invalid_argument("bad record"); };
    auto ex = thrown<MergeException>([&] { merge_all<int>({stuck.source(), boom, stuck2.source()}, 2); });
    REQUIRE(ex.has_value());
    CHECK_EQ(ex->stream(), 1);
    try {
        std::rethrow_exception(ex->cause());
    } catch (const std::invalid_argument& e) {
        CHECK_EQ(std::string(e.what()), "bad record");
    } catch (...) {
        CHECK(false, "cause has the wrong type");
    }
    // when merge_all has exited, the other producers are already cancelled AND joined
    CHECK(stuck.interrupted.load());
    CHECK(stuck2.interrupted.load());
}

TEST(unsorted_input_fails_merge_all, "part4,edge") {
    Watchdog wd(20000, "unsorted_merge_all");
    auto ex = thrown<MergeException>([&] { merge_all<int>(plain_sources(L{{1, 2}, {5, 4}}), 2); });
    REQUIRE(ex.has_value());
    CHECK_EQ(ex->stream(), 1);
    CHECK(thrown<UnsortedInputException>([&] { std::rethrow_exception(ex->cause()); }).has_value());
}

TEST(merge_all_works_with_a_descending_comparator, "part4,cpp") {
    Watchdog wd(20000, "merge_all_desc");
    const L lists{{9, 5, 1}, {8, 5, 2}};
    CHECK_EQ(merge_all<int>(plain_sources(lists), 2, std::greater<int>{}), (std::vector<int>{9, 8, 5, 5, 2, 1}));
}

TEST(merge_all_matches_the_oracle_under_random_interleavings, "part4,conc") {
    for (unsigned seed = 1001; seed <= 1025; ++seed) {
        Watchdog wd(30000, "merge_all_random");
        Rng g(seed);
        const L lists = random_sorted_lists(g, 1 + rnd(g, 9), 300, 40);
        auto gate = std::make_shared<std::latch>(1);
        std::vector<BlockingSource<int>> sources;
        for (std::size_t i = 0; i < lists.size(); ++i) sources.push_back(jittery(lists[i], gate, seed * 100 + static_cast<unsigned>(i)));
        gate->count_down();
        CHECK_EQ(merge_all<int>(std::move(sources), 1 + rnd(g, 5)), oracle(lists), "seed " + std::to_string(seed));
    }
}

TEST(merge_all_eight_by_fifty_thousand_under_two_seconds, "part4,perf") {
    Watchdog wd(30000, "perf_part4");
    Rng g(0);
    L lists;
    for (int i = 0; i < 8; ++i) {
        std::vector<int> v(50000);
        for (auto& x : v) x = rnd(g, 1'000'000);
        std::sort(v.begin(), v.end());
        lists.push_back(std::move(v));
    }
    CHECK_WITHIN_MS(2000, auto out = merge_all<int>(plain_sources(lists), 1024); CHECK_EQ(out.size(), 400000u););
}

MT_MAIN()
