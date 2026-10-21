// hc03 · recursive sum — C++20 tests.  Same cases as test/RecursiveSumTest.java plus C++-only edge cases (tag "cpp"):
// signed-overflow UB (the binary runs under UBSan with -fno-sanitize-recover), stack overflow as a crash not an exception,
// __int128 bounds, copy/move of the trampoline, span views, thread safety.
#include <array>
#include <atomic>
#include <climits>
#include <iostream>
#include <latch>
#include <memory>
#include <random>
#include <thread>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace recsum;

namespace recsum {
std::ostream& operator<<(std::ostream& os, const Ok& o) { return os << "Ok(" << o.value << ")"; }
std::ostream& operator<<(std::ostream& os, const Overflow& o) { return os << "Overflow(" << mt::to_string(o.exact) << ")"; }
}  // namespace recsum

namespace {

constexpr long long MAX = LLONG_MAX;
constexpr long long MIN = LLONG_MIN;

SumResult ok(long long v) { return Ok{v}; }
SumResult overflow(const char* exact) { return Overflow{mt::i128(exact)}; }

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

std::atomic<int> sink{0};  // keeps the optimiser from discarding a result nobody reads

constexpr std::size_t BIG = std::size_t{1} << 26;  // 64 MiB of stack: far more than 65536 frames need, committed lazily

template <class F> auto on_stack(std::size_t bytes, F body) {
    using R = decltype(body());
    std::optional<R> result;
    mt::run_on_stack(bytes, [&] { result = body(); });
    return *result;
}

}  // namespace

// ================================================ Part 1: naive recursion + checked

TEST(small_values, "part1") {
    for (Width w : {Width::Int, Width::Long}) {
        CHECK_EQ(sum_recursive(0, w), ok(0));
        CHECK_EQ(sum_recursive(1, w), ok(1));
        CHECK_EQ(sum_recursive(10, w), ok(55));
        CHECK_EQ(sum_recursive(100, w), ok(5050));
    }
}

TEST(negative_n_is_rejected, "part1,edge") {
    for (Width w : {Width::Int, Width::Long}) {
        CHECK_THROWS_AS(sum_recursive(-1, w), std::invalid_argument);
        CHECK_THROWS_AS(sum_recursive(LLONG_MIN, w), std::invalid_argument);
    }
}

TEST(int_width_overflows_exactly_at_65536, "part1,edge") {
    // 1+...+65535 = 2147450880 <= INT_MAX; adding 65536 gives 2147516416
    CHECK_EQ(on_stack(BIG, [] { return sum_recursive(65'535, Width::Int); }), ok(2'147'450'880LL));
    CHECK_EQ(on_stack(BIG, [] { return sum_recursive(65'536, Width::Int); }), overflow("2147516416"));
}

TEST(long_width_holds_what_int_cannot, "part1,edge") {
    CHECK_EQ(on_stack(BIG, [] { return sum_recursive(65'536, Width::Long); }), ok(2'147'516'416LL));
    CHECK_EQ(on_stack(BIG, [] { return sum_recursive(100'000, Width::Long); }), ok(5'000'050'000LL));
}

TEST(result_type_is_a_closed_variant, "part1") {
    // std::visit must name every alternative: a third alternative would break this build, like a sealed switch in Java.
    static_assert(std::variant_size_v<SumResult> == 2);
    SumResult r = sum_recursive(10, Width::Long);
    std::string text = std::visit(overloaded{[](const Ok& o) { return "ok " + std::to_string(o.value); },
                                             [](const Overflow& o) { return "overflow " + mt::to_string(o.exact); }}, r);
    CHECK_EQ(text, "ok 55");
}

// ---- C++-only Part 1

TEST(exact_to_is_exact_up_to_llong_max, "part1,edge,cpp") {
    CHECK(exact_to(0) == 0);
    CHECK(exact_to(1) == 1);
    CHECK(exact_to(65'536) == mt::i128("2147516416"));
    CHECK(exact_to(4'294'967'295LL) == mt::i128("9223372034707292160"));
    CHECK(exact_to(MAX) == mt::i128("42535295865117307928310139910543638528"));  // (2^63-1) * 2^62
}

TEST(checked_add_has_no_ub_at_the_edges, "part1,edge,cpp") {
    CHECK(add(Width::Long, MAX, 1) == std::nullopt);
    CHECK(add(Width::Long, MIN, -1) == std::nullopt);
    CHECK(add(Width::Long, MAX, MIN) == std::optional<long long>(-1));
    CHECK(add(Width::Long, MAX, 0) == std::optional<long long>(MAX));
    CHECK(add(Width::Int, INT_MAX, 1) == std::nullopt);
    CHECK(add(Width::Int, INT_MAX, 0) == std::optional<long long>(INT_MAX));
    CHECK(add(Width::Int, INT_MIN, -1) == std::nullopt);
    CHECK(add(Width::Int, INT_MIN, INT_MAX) == std::optional<long long>(-1));
    CHECK(add(Width::Int, 2'147'450'880LL, 65'536) == std::nullopt);
}

// ================================================ Part 2: stack depth, iterative, trampoline

TEST(measured_depth_grows_with_stack_size, "part2") {
    int small = measure_depth(512 * 1024);
    int large = measure_depth(std::size_t{64} * 1024 * 1024);
    CHECK_GT(small, 1'000, "a 512 KiB stack holds thousands of frames");
    CHECK_GT(static_cast<long long>(large), 4LL * small, "64 MiB should be far deeper than 512 KiB");
}

TEST(naive_recursion_blows_the_stack_but_trampoline_does_not, "part2,edge") {
    constexpr std::size_t small = 512 * 1024;
    // A stack overflow is SIGSEGV/SIGBUS in C++, not an exception: it can only be observed from another process.
    bool survived = mt::child_survives([] { mt::run_on_stack(small, [] { sink = static_cast<int>(sum_recursive(50'000'000, Width::Long).index()); }); });
    CHECK(!survived, "50M frames cannot fit in 512 KiB: the child must die");
    CHECK_EQ(on_stack(small, [] { return sum_trampoline(1'000'000, Width::Long); }), ok(500'000'500'000LL));
    CHECK_EQ(on_stack(small, [] { return sum_iterative(1'000'000, Width::Long); }), ok(500'000'500'000LL));
}

TEST(iterative_and_trampoline_agree_with_recursion, "part2") {
    for (Width w : {Width::Int, Width::Long})
        for (long long n : {0LL, 1LL, 2LL, 10LL, 999LL}) {
            auto expected = sum_recursive(n, w);
            CHECK_EQ(sum_iterative(n, w), expected, "iterative n=" + std::to_string(n));
            CHECK_EQ(sum_trampoline(n, w), expected, "trampoline n=" + std::to_string(n));
        }
}

TEST(stack_safe_versions_detect_overflow_and_reject_negatives, "part2,edge") {
    for (long long n : {65'536LL, 70'000LL, 1'000'000LL}) {
        SumResult expected = Overflow{exact_to(n)};
        CHECK_EQ(sum_iterative(n, Width::Int), expected, "iterative " + std::to_string(n));
        CHECK_EQ(sum_trampoline(n, Width::Int), expected, "trampoline " + std::to_string(n));
    }
    CHECK_EQ(sum_iterative(65'535, Width::Int), ok(2'147'450'880LL));
    CHECK_EQ(sum_trampoline(65'535, Width::Int), ok(2'147'450'880LL));
    CHECK_THROWS_AS(sum_iterative(-1, Width::Long), std::invalid_argument);
    CHECK_THROWS_AS(sum_trampoline(-1, Width::Long), std::invalid_argument);
}

namespace {
Trampoline<int> count_up(int i, int limit) {
    return i == limit ? Trampoline<int>::done(i) : Trampoline<int>::more([i, limit] { return count_up(i + 1, limit); });
}
}  // namespace

TEST(trampoline_run_loop, "part2") {
    CHECK_EQ(run(Trampoline<int>::done(5)), 5);
    CHECK_EQ(run(Trampoline<std::string>::more([] { return Trampoline<std::string>::done("x"); })), "x");
    // a million chained steps on a 512 KiB stack
    CHECK_EQ(on_stack(512 * 1024, [] { return run(count_up(0, 1'000'000)); }), 1'000'000);
}

TEST(mutual_recursion_is_even, "part2") {
    CHECK(is_even(0));
    CHECK(!is_even(1));
    CHECK(is_even(10));
    CHECK(!is_even(7));
    CHECK(on_stack(512 * 1024, [] { return is_even(2'000'000); }));
    CHECK(!on_stack(512 * 1024, [] { return is_even(2'000'001); }));
    CHECK_THROWS_AS(is_even(-2), std::invalid_argument);
}

TEST(perf_stack_safe_sums, "part2,perf") {
    CHECK_WITHIN_MS(2000, CHECK_EQ(sum_iterative(300'000'000, Width::Long), ok(45'000'000'150'000'000LL)););
    CHECK_WITHIN_MS(2000, CHECK_EQ(sum_trampoline(5'000'000, Width::Long), ok(12'500'002'500'000LL)););
}

// ---- C++-only Part 2

TEST(trampoline_is_copyable_and_move_only_results_work, "part2,edge,cpp") {
    // A perfect-forwarding constructor `template<class... A> Trampoline(A&&...)` would hijack copying of a non-const lvalue.
    auto a = Trampoline<int>::done(41);
    Trampoline<int> b = a;  // copy of a non-const lvalue
    const Trampoline<int> c = b;
    CHECK_EQ(run(a), 41);
    CHECK_EQ(run(b), 41);
    CHECK_EQ(run(c), 41);
    // move-only payload: run() must move it out, not copy
    auto p = run(Trampoline<std::unique_ptr<int>>::more([] { return Trampoline<std::unique_ptr<int>>::done(std::make_unique<int>(7)); }));
    REQUIRE(p != nullptr);
    CHECK_EQ(*p, 7);
}

TEST(tail_recursive_source_form_is_correct, "part2,edge,cpp") {
    // Whether the compiler turns it into a loop is not specified by the standard, so only correctness is tested here
    // (on a big stack, so a compiler that keeps the frames still passes).
    for (Width w : {Width::Int, Width::Long})
        for (long long n : {0LL, 1LL, 10LL, 999LL}) CHECK_EQ(sum_tail_recursive(n, w), sum_recursive(n, w));
    CHECK_EQ(on_stack(BIG, [] { return sum_tail_recursive(100'000, Width::Long); }), ok(5'000'050'000LL));
    CHECK_EQ(on_stack(BIG, [] { return sum_tail_recursive(65'536, Width::Int); }), overflow("2147516416"));
    CHECK_THROWS_AS(sum_tail_recursive(-1, Width::Long), std::invalid_argument);
}

// ================================================ Part 3: ranges [a, b], negatives, closed form

TEST(range_sum_examples, "part3") {
    CHECK_EQ(range_sum(1, 100), ok(5050));
    CHECK_EQ(range_sum(-5, 5), ok(0));
    CHECK_EQ(range_sum(-10, -1), ok(-55));
    CHECK_EQ(range_sum(-3, 4), ok(4));
    CHECK_EQ(range_sum(7, 7), ok(7));
    CHECK_EQ(range_sum(0, 0), ok(0));
    CHECK_EQ(range_sum(-7, -7), ok(-7));
    CHECK(range_sum_exact(1, 100) == 5050);
}

TEST(empty_range_is_rejected, "part3,edge") {
    CHECK_THROWS_AS(range_sum(2, 1), std::invalid_argument);
    CHECK_THROWS_AS(range_sum_exact(MAX, MIN), std::invalid_argument);
}

TEST(naive_closed_form_wraps_where_the_real_one_does_not, "part3,edge") {
    // n*(n+1) = 2^64 - 2^32 does not fit a signed 64-bit integer: wrapped, it is negative.
    const long long n = 4'294'967'295LL;
    CHECK_EQ(naive_closed_form(n), -2'147'483'648LL, "the naive formula silently gives a wrong, negative answer");
    CHECK_EQ(range_sum(1, n), ok(9'223'372'034'707'292'160LL));
    CHECK_EQ(range_sum(1, n + 1), overflow("9223372039002259456"));  // one more really does not fit
}

TEST(intermediate_overflow_is_not_result_overflow, "part3,edge") {
    CHECK_EQ(range_sum(MIN, MAX), ok(MIN));  // count = 2^64 does not fit; the sum is exactly LLONG_MIN
    CHECK_EQ(range_sum(-MAX, MAX), ok(0));
    CHECK_EQ(range_sum(MAX, MAX), ok(MAX));  // a+b overflows, the sum is just a
    CHECK_EQ(range_sum(MIN, MIN), ok(MIN));
    CHECK_EQ(range_sum(MAX - 1, MAX), overflow("18446744073709551613"));  // 2^64 - 3: really too big
}

TEST(huge_range_carries_the_exact_value, "part3,edge") {
    auto r = range_sum(MIN, 0);
    const auto* o = std::get_if<Overflow>(&r);
    REQUIRE(o != nullptr);
    CHECK(o->exact == mt::i128("-42535295865117307937533511947398414336"));
}

TEST(small_ranges_match_brute_force, "part3,edge") {
    for (long long a = -40; a <= 40; ++a)
        for (long long b = a; b <= 40; ++b) {
            long long expected = 0;
            for (long long i = a; i <= b; ++i) expected += i;
            CHECK_EQ(range_sum(a, b), ok(expected), std::to_string(a) + ".." + std::to_string(b));
        }
}

namespace {
// Independent oracle: split at zero and use T(m) = m(m+1)/2 on non-negative m (m <= 2^63, so m*(m+1) < 2^127).
__int128 tri(unsigned long long m) { return static_cast<__int128>(m) * (static_cast<__int128>(m) + 1) / 2; }
__int128 oracle(long long a, long long b) {
    auto mag = [](long long x) { return x < 0 ? 0ULL - static_cast<unsigned long long>(x) : static_cast<unsigned long long>(x); };
    if (a >= 0) return a == 0 ? tri(mag(b)) : tri(mag(b)) - tri(mag(a) - 1);
    if (b < 0) return -(tri(mag(a)) - (b == -1 ? 0 : tri(mag(b) - 1)));
    return tri(mag(b)) - tri(mag(a));
}
}  // namespace

TEST(random_ranges_across_the_whole_long_range, "part3,edge") {
    std::mt19937_64 rnd(0);
    int overflows = 0, oks = 0;
    for (int i = 0; i < 20'000; ++i) {
        auto draw = [&] { return static_cast<long long>(rnd()) >> (rnd() % 64); };  // arithmetic shift of a signed value
        long long a = draw(), b = draw();
        if (a > b) std::swap(a, b);
        const __int128 expected = oracle(a, b);
        SumResult got = range_sum(a, b);
        if (expected >= MIN && expected <= MAX) {
            ++oks;
            CHECK_EQ(got, ok(static_cast<long long>(expected)), std::to_string(a) + ".." + std::to_string(b));
        } else {
            ++overflows;
            CHECK_EQ(got, SumResult{Overflow{expected}}, std::to_string(a) + ".." + std::to_string(b));
        }
    }
    CHECK(oks > 1'000 && overflows > 1'000, "random cases should cover both outcomes: " + std::to_string(oks) + "/" + std::to_string(overflows));
}

TEST(corner_grid_has_no_signed_overflow_and_matches_the_oracle, "part3,edge,cpp") {
    // Every pair of "interesting" endpoints; UBSan (-fno-sanitize-recover) kills the binary if any intermediate overflows.
    const long long pts[] = {MIN, MIN + 1, -(1LL << 62), -4'294'967'296LL, -4'294'967'295LL, -2, -1, 0, 1, 2, 4'294'967'295LL, 4'294'967'296LL, 1LL << 62, MAX - 1, MAX};
    for (long long a : pts)
        for (long long b : pts) {
            if (a > b) continue;
            REQUIRE(range_sum_exact(a, b) == oracle(a, b), std::to_string(a) + ".." + std::to_string(b));
        }
}

// ================================================ Part 4: parallel sum over contiguous data

namespace {
std::vector<long long> random_data(std::size_t n, long long bound) {
    std::mt19937_64 rnd(0);
    std::uniform_int_distribution<long long> dist(-bound, bound - 1);
    std::vector<long long> d(n);
    for (auto& x : d) x = dist(rnd);
    return d;
}
long long plain_sum(std::span<const long long> d) {
    unsigned long long s = 0;  // unsigned: wrapping is defined; callers keep totals in range anyway
    for (long long x : d) s += static_cast<unsigned long long>(x);
    return static_cast<long long>(s);
}
using Impl = std::function<SumResult(std::span<const long long>)>;
std::vector<std::pair<const char*, Impl>> parallel_impls() {
    return {{"fork_join(1000)", [](auto d) { return parallel_sum_fork_join(d, 1'000); }},
            {"fork_join(1)", [](auto d) { return parallel_sum_fork_join(d, 1); }},
            {"async", [](auto d) { return parallel_sum_async(d); }},
            {"workers(7)", [](auto d) { return parallel_sum_workers(d, 7); }},
            {"workers(1)", [](auto d) { return parallel_sum_workers(d, 1); }}};
}
}  // namespace

TEST(wide_accumulator_basics, "part4") {
    auto w = Wide::zero().plus(MAX).plus(MAX);
    CHECK(!w.fits_long());
    CHECK(w.exact() == static_cast<__int128>(MAX) * 2);
    CHECK(w.plus(MIN).fits_long());
    CHECK(Wide::zero().plus(-1).exact() == -1);
    auto merged = Wide::zero().plus(MIN).merge(Wide::zero().plus(MIN));
    CHECK(merged.exact() == static_cast<__int128>(MIN) * 2);
    CHECK(!merged.fits_long());
}

TEST(checked_sum_depends_on_the_true_total_not_the_order, "part4,edge") {
    auto sum = [](std::vector<long long> v) { return checked_sum(v); };
    CHECK_EQ(sum({}), ok(0));
    CHECK_EQ(sum({MAX, 1, -1}), ok(MAX));  // step-by-step checked adds would fail on the second element
    CHECK_EQ(sum({1, MAX, -1}), ok(MAX));
    CHECK_EQ(sum({MIN, MAX}), ok(-1));
    CHECK_EQ(sum({MAX, 1}), overflow("9223372036854775808"));
    CHECK_EQ(sum({MIN, -1}), overflow("-9223372036854775809"));
    CHECK_EQ(sum({MAX, MAX, MIN, MIN, 1, -1}), ok(-2));
}

TEST(parallel_implementations_match_sequential, "part4") {
    auto data = random_data(100'003, 1'000'000);
    SumResult expected = ok(plain_sum(data));
    CHECK_EQ(checked_sum(data), expected);
    for (auto& [name, impl] : parallel_impls()) CHECK_EQ(impl(data), expected, name);
}

TEST(parallel_edge_shapes, "part4,edge") {
    const std::vector<std::vector<long long>> shapes{{}, {42}, {-1, 1}, {MAX}, {MIN}, {0, 0, 0}};
    for (const auto& data : shapes) {
        SumResult expected = checked_sum(data);
        for (auto& [name, impl] : parallel_impls()) CHECK_EQ(impl(data), expected, name);
    }
    CHECK_EQ(parallel_sum_workers(std::vector<long long>{}, 16), ok(0));            // more chunks than elements
    CHECK_EQ(parallel_sum_workers(std::vector<long long>{1, 2, 3}, 100), ok(6));
    CHECK_THROWS_AS(parallel_sum_fork_join(std::vector<long long>(1), 0), std::invalid_argument);
    CHECK_THROWS_AS(parallel_sum_workers(std::vector<long long>(1), 0), std::invalid_argument);
}

TEST(parallel_overflow_is_decided_by_the_true_total, "part4,edge") {
    // each chunk alone may overflow a long long, the whole does not: chunk boundaries must not change the answer
    std::vector<long long> cancel(4'000), over(4'000, MAX);
    for (std::size_t i = 0; i < cancel.size(); ++i) cancel[i] = i < 2'000 ? MAX : MIN;
    SumResult cancel_expected = checked_sum(cancel), big_over = checked_sum(over);
    CHECK_EQ(cancel_expected, ok(-2'000));
    CHECK(std::holds_alternative<Overflow>(big_over));
    for (auto& [name, impl] : parallel_impls()) {
        CHECK_EQ(impl(cancel), cancel_expected, name);
        CHECK_EQ(impl(over), big_over, name);
    }
}

TEST(concurrent_callers_all_get_the_same_answer, "part4,conc") {
    auto data = random_data(200'001, 1LL << 40);
    SumResult expected = ok(plain_sum(data));
    constexpr int callers = 6;
    for (int round = 0; round < 8; ++round) {
        std::latch gate(1);
        std::vector<SumResult> results(callers * 3, ok(-1));
        std::vector<std::thread> threads;
        mt::ThreadErrors errors;
        for (int c = 0; c < callers; ++c)
            threads.push_back(errors.spawn([&, slot = c * 3] {
                gate.wait();
                results[slot] = parallel_sum_fork_join(data, 5'000);
                results[slot + 1] = parallel_sum_async(data);
                results[slot + 2] = parallel_sum_workers(data, 16);
            }));
        gate.count_down();
        for (auto& t : threads) t.join();
        CHECK_NO_THREAD_ERRORS(errors);
        for (std::size_t i = 0; i < results.size(); ++i) CHECK_EQ(results[i], expected, "round " + std::to_string(round) + " slot " + std::to_string(i));
    }
}

TEST(perf_ten_million_elements, "part4,perf") {
    auto data = random_data(10'000'000, 1LL << 30);
    SumResult expected = ok(plain_sum(data));
    CHECK_WITHIN_MS(2000, CHECK_EQ(checked_sum(data), expected); CHECK_EQ(parallel_sum_fork_join(data, 100'000), expected);
                    CHECK_EQ(parallel_sum_async(data), expected););
    CHECK_WITHIN_MS(2000, CHECK_EQ(parallel_sum_workers(data, 10'000), expected););  // 10,000 chunks, still only ~cores threads
}

// ---- C++-only Part 4

TEST(span_views_cover_subranges_arrays_and_vectors, "part4,edge,cpp") {
    // span is pointer + length: no copy, any contiguous storage, sub-ranges starting at odd addresses.
    auto data = random_data(10'001, 1000);
    std::span<const long long> all(data);
    for (std::size_t from : {0u, 1u, 3u, 5'000u, 10'000u}) {
        auto view = all.subspan(from);
        SumResult expected = ok(plain_sum(view));
        CHECK_EQ(checked_sum(view), expected);
        CHECK_EQ(parallel_sum_workers(view, 5), expected);
        CHECK_EQ(parallel_sum_fork_join(view, 17), expected);
    }
    std::array<long long, 4> arr{MAX, 1, -1, 2};
    CHECK_EQ(checked_sum(arr), overflow("9223372036854775809"));
    const long long raw[] = {5, 6, 7};
    CHECK_EQ(checked_sum(raw), ok(18));
    CHECK_EQ(checked_sum(std::span<const long long>{}), ok(0));
}

MT_MAIN()
