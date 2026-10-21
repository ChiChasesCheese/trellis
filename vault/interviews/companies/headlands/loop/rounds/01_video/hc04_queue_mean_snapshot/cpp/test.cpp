// hc04 · Queue mean + corrective snapshot — C++20 tests.  Same cases as test/QueueMeanTest.java plus C++-only edge
// cases (tag "cpp"): moved-from objects, deep copies, correctly-rounded double conversion, LLONG_MIN, dangling references
// after vector growth, strict integer parsing, data races (torn reads) and lock-freedom.
#include <climits>
#include <cmath>
#include <cstdlib>
#include <deque>
#include <iostream>
#include <mutex>
#include <random>
#include <thread>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace qmean;

namespace qmean {
std::ostream& operator<<(std::ostream& os, const Mean& m) { return os << i128_to_string(m.numerator) << "/" << m.denominator; }
std::ostream& operator<<(std::ostream& os, const Value& v) { return os << "Value(" << v.mean << ")"; }
std::ostream& operator<<(std::ostream& os, const Empty&) { return os << "Empty"; }
std::ostream& operator<<(std::ostream& os, const Stat& s) { return os << "Stat{seq=" << s.seq << ",size=" << s.size << ",sum=" << i128_to_string(s.sum) << "}"; }
}  // namespace qmean

namespace {

constexpr long long MAX = LLONG_MAX;
constexpr long long MIN = LLONG_MIN;

Mean frac(long long n, long long d) { return Mean(n, d); }
using Lines = std::vector<std::string>;
Lines lines_of(const std::string& block) {
    Lines out;
    std::size_t pos = 0;
    while (pos < block.size()) {
        std::size_t nl = block.find('\n', pos);
        if (nl == std::string::npos) nl = block.size();
        out.push_back(block.substr(pos, nl - pos));
        pos = nl + 1;
    }
    return out;
}

/// Slow, obviously-correct reference: sum from scratch.
Mean oracle(const std::deque<long long>& q) {
    i128 s = 0;
    for (long long x : q) s += x;
    return Mean(s, static_cast<long long>(q.size()));
}

/// Independent correctly-rounded n/d: decimal long division (200 fraction digits) then libc strtod, which rounds
/// correctly.  A non-terminating expansion can never sit within 1e-200 of a rounding boundary when d < 2^63.
double nearest_double(i128 n, long long d) {
    const bool neg = n < 0;
    u128 m = neg ? u128{0} - static_cast<u128>(n) : static_cast<u128>(n);
    std::string text = neg ? "-" : "";
    text += mt::to_string(m / static_cast<u128>(d)) + ".";
    u128 r = m % static_cast<u128>(d);
    for (int i = 0; i < 200; ++i) {
        r *= 10;
        text.push_back(static_cast<char>('0' + static_cast<int>(r / static_cast<u128>(d))));
        r %= static_cast<u128>(d);
    }
    return std::strtod(text.c_str(), nullptr);
}

}  // namespace

// ================================================ Part 1: push / pop / get_mean

TEST(sample_from_problem_statement, "part1") {
    QueueMean q;
    q.push(1); q.push(2); q.push(3);
    CHECK_EQ(q.get_mean(), 2.0);
    q.push(4);
    CHECK_EQ(q.get_mean(), 2.5);
    CHECK_EQ(q.pop(), 1);  // FIFO: oldest first
    CHECK_EQ(q.get_mean(), 3.0);
    CHECK_EQ(q.size(), 3u);
}

TEST(empty_queue_rejects_pop_and_mean, "part1,edge") {
    QueueMean q;
    CHECK(q.empty());
    CHECK_THROWS_AS(q.pop(), std::out_of_range);
    CHECK_THROWS_AS(q.get_mean(), std::out_of_range);
    CHECK_THROWS_AS(q.mean(), std::out_of_range);
    q.push(5);
    q.pop();
    CHECK_THROWS_AS(q.mean(), std::out_of_range);  // also after draining
    CHECK_THROWS_AS(q.pop(), std::out_of_range);
}

TEST(mean_is_a_reduced_fraction_with_positive_denominator, "part1,edge") {
    QueueMean q;
    q.push(2); q.push(4);
    CHECK_EQ(q.mean(), frac(3, 1));
    CHECK_EQ(frac(6, 4), frac(3, 2));  // reduced on construction, so == compares values
    CHECK_EQ(frac(6, 4).numerator, static_cast<i128>(3));
    CHECK_EQ(frac(6, 4).denominator, 2);
    q.pop(); q.pop();
    q.push(1); q.push(2);
    CHECK_EQ(q.mean(), frac(3, 2));
    q.pop(); q.pop();
    q.push(-1); q.push(-2);
    CHECK_EQ(q.mean(), frac(-3, 2));  // sign only on the numerator
    CHECK_EQ(q.get_mean(), -1.5);
    CHECK_THROWS_AS(Mean(1, 0), std::invalid_argument);
    CHECK_THROWS_AS(Mean(1, -2), std::invalid_argument);
}

TEST(zero_and_negative_values, "part1,edge") {
    QueueMean q;
    q.push(-3); q.push(3);
    CHECK_EQ(q.mean(), frac(0, 1));
    CHECK_EQ(q.get_mean(), 0.0);
    q.push(0);
    CHECK_EQ(q.mean(), frac(0, 1));
}

TEST(no_float_drift_from_a_running_double_sum, "part1,edge") {
    // A double running sum: 1e16 + 1 + 1 == 1e16 (each +1 is rounded away), so after popping 1e16 it says 0 instead of 2.
    QueueMean q;
    q.push(10'000'000'000'000'000LL);
    q.push(1);
    q.push(1);
    q.pop();
    CHECK_EQ(q.mean(), frac(1, 1));
    CHECK_EQ(q.get_mean(), 1.0);
}

TEST(sum_overflowing_long_is_exact, "part1,edge") {
    QueueMean q;
    q.push(MAX);
    q.push(MAX);
    CHECK_EQ(q.mean(), frac(MAX, 1));  // sum = 2^64 - 2 does not fit a long long
    q.push(MAX);
    CHECK_EQ(q.mean(), frac(MAX, 1));
    q.pop(); q.pop(); q.pop();
    q.push(5);
    CHECK_EQ(q.mean(), frac(5, 1));  // back to small values, nothing stuck in the accumulator
    QueueMean neg;
    neg.push(MIN);
    neg.push(MIN);
    CHECK_EQ(neg.mean(), frac(MIN, 1));
    neg.push(MAX);  // MIN + MIN + MAX = -2^63 - 1
    CHECK_EQ(neg.mean(), Mean(static_cast<i128>(MIN) - 1, 3));
}

TEST(get_mean_is_the_nearest_double, "part1,edge") {
    QueueMean q;
    q.push(MAX);
    q.push(MAX - 1);  // exact mean MAX - 0.5; the nearest double is 2^63
    CHECK_EQ(q.get_mean(), 0x1p63);
    QueueMean r;
    r.push(1); r.push(2);
    CHECK_EQ(r.get_mean(), 1.5);
    QueueMean s;
    s.push(1); s.push(1); s.push(2);  // 4/3: one division is correctly rounded
    CHECK_EQ(s.get_mean(), 4.0 / 3.0);
}

TEST(ring_buffer_wraps_and_grows_in_fifo_order, "part1,edge") {
    QueueMean q;
    for (int i = 0; i < 1000; ++i) q.push(i);
    for (int i = 0; i < 1000; ++i) CHECK_EQ(q.pop(), i);
    CHECK(q.empty());
    // park head in the middle of the buffer, then force a grow: it must copy in logical order
    for (int i = 0; i < 12; ++i) q.push(i);
    for (int i = 0; i < 10; ++i) q.pop();
    for (int i = 100; i < 140; ++i) q.push(i);
    CHECK_EQ(q.pop(), 10);
    CHECK_EQ(q.pop(), 11);
    CHECK_EQ(q.pop(), 100);
}

TEST(random_ops_match_the_from_scratch_oracle, "part1,edge") {
    std::mt19937_64 rnd(1);
    QueueMean q;
    std::deque<long long> ref;
    for (int i = 0; i < 20'000; ++i) {
        if (ref.empty() || rnd() % 100 < 55) {
            long long x;
            switch (rnd() % 4) {
                case 0: x = static_cast<long long>(rnd()); break;
                case 1: x = MAX - static_cast<long long>(rnd() % 3); break;
                case 2: x = MIN + static_cast<long long>(rnd() % 3); break;
                default: x = static_cast<long long>(rnd() % 21) - 10; break;
            }
            q.push(x);
            ref.push_back(x);
        } else {
            CHECK_EQ(q.pop(), ref.front());
            ref.pop_front();
        }
        if (i % 97 == 0 && !ref.empty()) {
            const Mean expected = oracle(ref);
            CHECK_EQ(q.mean(), expected);
            CHECK_EQ(q.get_mean(), nearest_double(expected.numerator, expected.denominator));
        }
    }
}

TEST(million_operations_in_under_two_seconds, "part1,perf") {
    std::mt19937_64 rnd(0);
    QueueMean q;
    double acc = 0;
    CHECK_WITHIN_MS(2000, for (int i = 0; i < 1'000'000; ++i) {
        if (q.empty() || rnd() % 100 < 52) q.push(static_cast<long long>(rnd()) >> (rnd() % 40));
        else q.pop();
        if ((i & 7) == 0 && !q.empty()) acc += q.get_mean();
    });
    CHECK(!std::isnan(acc));
}

// ---- C++-only Part 1

TEST(moved_from_queue_is_a_valid_empty_queue, "part1,edge,cpp") {
    // The compiler-generated move constructor moves the vector but copies size_/head_/sum_: the moved-from queue would
    // claim elements that are not there.
    QueueMean a;
    for (int i = 1; i <= 5; ++i) a.push(i);
    QueueMean b = std::move(a);
    CHECK_EQ(b.size(), 5u);
    CHECK_EQ(b.mean(), frac(3, 1));
    CHECK(a.empty());  // NOLINT(bugprone-use-after-move): that is the point
    CHECK(a.sum() == 0);
    CHECK_THROWS_AS(a.pop(), std::out_of_range);
    CHECK_THROWS_AS(a.mean(), std::out_of_range);
    a.push(9);  // usable again
    CHECK_EQ(a.mean(), frac(9, 1));
    CHECK_EQ(a.pop(), 9);
    QueueMean c;
    c.push(100);
    c = std::move(b);  // move assignment
    CHECK_EQ(c.size(), 5u);
    CHECK_EQ(c.pop(), 1);
    CHECK(b.empty());
    b.push(1);
    CHECK_EQ(b.pop(), 1);
    QueueMean& alias = c;
    c = std::move(alias);  // self-move: must leave a valid object (contents unspecified)
    c.push(7);
    CHECK_GE(c.size(), 1u);
}

TEST(copy_is_deep_and_independent, "part1,edge,cpp") {
    QueueMean a;
    for (int i = 0; i < 40; ++i) a.push(i);
    for (int i = 0; i < 25; ++i) a.pop();  // head is mid-buffer, so a copy must preserve the wrap state
    QueueMean b = a;
    a.push(1000);
    a.pop();
    CHECK_EQ(b.size(), 15u);
    CHECK_EQ(b.pop(), 25);
    CHECK_EQ(a.pop(), 26);
    QueueMean c;
    c = b;
    b.push(-1);
    CHECK_EQ(c.size(), 14u);
    CHECK_EQ(c.mean(), oracle(std::deque<long long>{26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39}));
}

TEST(llong_min_is_not_negated_anywhere, "part1,edge,cpp") {
    // -LLONG_MIN, std::abs(LLONG_MIN) and (x > 0 ? x : -x) are all signed-overflow UB; UBSan aborts if the code does that.
    QueueMean q;
    for (int i = 0; i < 3; ++i) q.push(MIN);
    CHECK_EQ(q.mean(), frac(MIN, 1));
    CHECK_EQ(q.get_mean(), -0x1p63);
    q.push(MAX);
    CHECK_EQ(q.mean(), oracle(std::deque<long long>{MIN, MIN, MIN, MAX}));
    CHECK_EQ(q.pop(), MIN);
    CHECK_EQ(Mean(static_cast<i128>(MIN), 2), frac(MIN / 2, 1));
}

TEST(get_mean_fast_path_boundary_2_pow_53, "part1,edge,cpp") {
    const long long p53 = 1LL << 53;
    QueueMean q;
    q.push(p53);
    CHECK_EQ(q.get_mean(), 0x1p53);
    q.push(1);  // sum 2^53 + 1 is not a double; mean (2^53+1)/2 is
    CHECK_EQ(q.get_mean(), nearest_double(static_cast<i128>(p53) + 1, 2));
    QueueMean r;
    r.push(-p53);
    r.push(-1);  // sum -(2^53+1)
    CHECK_EQ(r.get_mean(), nearest_double(-static_cast<i128>(p53) - 1, 2));
    QueueMean s;
    s.push(p53 + 1);
    CHECK_EQ(s.get_mean(), 0x1p53);  // 2^53 + 1 ties to even
    QueueMean t;
    t.push(p53 + 3);
    CHECK_EQ(t.get_mean(), 0x1p53 + 4);
}

TEST(get_mean_is_correct_for_sums_between_2_pow_53_and_2_pow_62, "part1,edge,cpp") {
    // Dividing (double)sum by size rounds twice once the sum is not exactly representable; the oracle rounds once.
    std::mt19937_64 rnd(11);
    for (int i = 0; i < 20'000; ++i) {
        QueueMean q;
        const int n = 2 + static_cast<int>(rnd() % 8);
        i128 sum = 0;
        for (int k = 0; k < n; ++k) {
            const long long x = static_cast<long long>(rnd() >> (3 + rnd() % 8)) - (1LL << 55);
            q.push(x);
            sum += x;
        }
        CHECK_EQ(q.get_mean(), nearest_double(sum, n), "n=" + std::to_string(n));
    }
}

TEST(to_double_rounds_once_and_matches_strtod, "part1,edge,cpp") {
    CHECK_EQ(Mean(1, 3).to_double(), 1.0 / 3.0);
    CHECK_EQ(Mean(-1, 3).to_double(), -1.0 / 3.0);
    CHECK_EQ(Mean(0, 5).to_double(), 0.0);
    CHECK_EQ(Mean(static_cast<i128>(1) << 126, 1).to_double(), 0x1p126);
    CHECK_EQ(Mean(1, MAX).to_double(), nearest_double(1, MAX));
    CHECK_EQ(Mean((static_cast<i128>(1) << 100) + 1, 3).to_double(), nearest_double((static_cast<i128>(1) << 100) + 1, 3));
    std::mt19937_64 rnd(5);
    for (int i = 0; i < 20'000; ++i) {
        const int bits = 1 + static_cast<int>(rnd() % 125);
        u128 mag = (static_cast<u128>(rnd()) << 64 | rnd()) >> (128 - bits);
        i128 n = static_cast<i128>(mag);
        if (rnd() & 1) n = -n;
        const long long d = static_cast<long long>(rnd() >> (1 + rnd() % 62)) | 1;  // positive, 1..2^63-1
        const Mean m(n, d);
        CHECK_EQ(m.to_double(), nearest_double(m.numerator, m.denominator), i128_to_string(n) + "/" + std::to_string(d));
    }
}

// ================================================ Part 2: corrective snapshot event stream

TEST(sample_session_exact_output, "part2,fmt") {
    auto out = solve(lines_of("push 1\npush 2\nmean\npop\nmean\nsnapshot 10 20 30\nmean\npop\nmean\npop\npop\nmean\n"));
    CHECK_EQ(out, (Lines{"3/2", "2", "20", "25", "empty"}));
}

TEST(snapshot_replaces_the_whole_logical_history, "part2") {
    auto answers = run({Push{1}, Push{2}, Query{}, Correct{{10}}, Query{}, Pop{}, Query{}});
    CHECK_EQ(answers, (std::vector<Answer>{Value{frac(3, 2)}, Value{frac(10, 1)}, Empty{}}));
}

TEST(snapshot_keeps_fifo_order_and_can_be_empty, "part2,edge") {
    CHECK_EQ(solve(lines_of("snapshot 5 6 7\npop\nmean\nsnapshot\nmean\n")), (Lines{"13/2", "empty"}));
}

TEST(snapshot_with_overflowing_sum, "part2,edge") {
    const std::string big = std::to_string(MAX);
    CHECK_EQ(solve({"snapshot " + big + " " + big + " " + big, "mean"}), (Lines{big}));
}

TEST(correct_event_owns_its_contents, "part2,edge") {
    // Java needs List.copyOf to stop the caller mutating the event later; a std::vector member is a value, copied on construction.
    std::vector<long long> src{1, 2};
    Correct event{src};
    src.push_back(99);
    CHECK_EQ(event.contents, (std::vector<long long>{1, 2}));
    Correct moved{std::move(event)};
    CHECK_EQ(moved.contents.size(), 2u);
    CHECK(moved == (Correct{{1, 2}}));
}

TEST(pop_on_empty_is_an_error, "part2,edge") {
    CHECK_THROWS_AS(run({Pop{}}), std::out_of_range);
    CHECK_THROWS_AS(solve({"snapshot 1", "pop", "pop"}), std::out_of_range);
}

TEST(no_queries_no_answers, "part2,edge") {
    CHECK_EQ(run({}), std::vector<Answer>{});
    CHECK_EQ(solve({"push 1", "", "pop"}), Lines{});
}

namespace {
bool rejected_with_line_2(const std::string& bad) {
    try { parse({"push 1", bad}); } catch (const std::invalid_argument& e) { return std::string(e.what()).rfind("line 2:", 0) == 0; }
    return false;
}
}  // namespace

TEST(parse_rejects_malformed_lines_with_the_line_number, "part2,edge") {
    for (const char* bad : {"push", "push x", "push 1 2", "push 99999999999999999999", "pop 3", "mean 1", "snapshot a", "PUSH 1", "peek"})
        CHECK(rejected_with_line_2(bad), bad);
}

TEST(render_formats, "part2,fmt") {
    CHECK_EQ(render(Value{frac(7, 1)}), "7");
    CHECK_EQ(render(Value{frac(-7, 2)}), "-7/2");
    CHECK_EQ(render(Value{frac(0, 5)}), "0");
    CHECK_EQ(render(Empty{}), "empty");
}

TEST(million_events_with_snapshots_in_under_two_seconds, "part2,perf") {
    std::mt19937_64 rnd(0);
    std::vector<Event> events;
    events.reserve(1'000'000);
    std::size_t size = 0;
    for (int i = 0; i < 1'000'000; ++i) {
        const auto r = rnd() % 100;
        if (r < 45 || size == 0) { events.push_back(Push{static_cast<long long>(rnd())}); ++size; }
        else if (r < 85) { events.push_back(Pop{}); --size; }
        else if (r < 99) events.push_back(Query{});
        else {
            Correct c;
            const auto m = rnd() % 5;
            for (unsigned j = 0; j < m; ++j) c.contents.push_back(static_cast<long long>(rnd()));
            size = c.contents.size();
            events.push_back(std::move(c));
        }
    }
    CHECK_WITHIN_MS(2000, auto answers = run(events); CHECK(!answers.empty()););
}

// ---- C++-only Part 2

TEST(parse_is_strict_about_integers_and_whitespace, "part2,edge,cpp") {
    // std::stoll("12abc") == 12 and strtoll accepts '+', leading spaces and hex; from_chars + full-token check does not.
    for (const char* bad : {"push +5", "push 0x10", "push 1.5", "push -", "push 9223372036854775808", "push -9223372036854775809", "snapshot 1 2 x",
                            "snapshot 1,2", "push 1x", "push \xC3\xA9", "\xFF" "push 1"})
        CHECK(rejected_with_line_2(bad), bad);
    CHECK(rejected_with_line_2(std::string("push 1\0", 7)));  // embedded NUL is not whitespace
    auto events = parse({"push -9223372036854775808", "\tpush\t7  ", "  pop  ", "mean\r", "snapshot\t1  2\r", "   "});
    CHECK_EQ(events, (std::vector<Event>{Push{MIN}, Push{7}, Pop{}, Query{}, Correct{{1, 2}}}));
}

TEST(parse_counts_blank_lines_in_the_line_number, "part2,edge,cpp") {
    try {
        parse({"push 1", "", "   ", "bad"});
        CHECK(false, "should have thrown");
    } catch (const std::invalid_argument& e) {
        CHECK(std::string(e.what()).rfind("line 4:", 0) == 0, e.what());
    }
}

TEST(correct_with_an_empty_vector_and_back_to_back_snapshots, "part2,edge,cpp") {
    auto answers = run({Push{1}, Correct{}, Query{}, Correct{{4, 6}}, Correct{{8}}, Query{}, Push{2}, Query{}});
    CHECK_EQ(answers, (std::vector<Answer>{Empty{}, Value{frac(8, 1)}, Value{frac(5, 1)}}));
}

// ================================================ Part 3: persistent / versioned queue

TEST(old_versions_stay_usable, "part3") {
    VersionedQueue vq;
    int v1 = vq.push(VersionedQueue::EMPTY, 1);
    int v2 = vq.push(v1, 2);
    int v3 = vq.pop(v2);
    CHECK_EQ(vq.contents(v3), (std::vector<long long>{2}));
    CHECK_EQ(vq.mean(v2), frac(3, 2));  // an older version is untouched by the later pop
    CHECK_EQ(vq.size(v2), 2u);
    CHECK_EQ(vq.size(VersionedQueue::EMPTY), 0u);
    int a = vq.push(v2, 10), b = vq.push(v2, 20);  // fork from the same old version
    CHECK_EQ(vq.contents(a), (std::vector<long long>{1, 2, 10}));
    CHECK_EQ(vq.contents(b), (std::vector<long long>{1, 2, 20}));
    CHECK_EQ(vq.mean(a), frac(13, 3));
}

TEST(correct_starts_an_independent_history, "part3") {
    VersionedQueue vq;
    int base = vq.push(VersionedQueue::EMPTY, 100);
    int fixed = vq.correct({1, 2, 3});
    CHECK_EQ(vq.mean(fixed), frac(2, 1));
    int popped = vq.pop(fixed);
    CHECK_EQ(vq.contents(popped), (std::vector<long long>{2, 3}));
    CHECK_EQ(vq.contents(base), (std::vector<long long>{100}));
    CHECK_EQ(vq.size(vq.correct({})), 0u);
}

TEST(empty_and_unknown_versions_are_rejected, "part3,edge") {
    VersionedQueue vq;
    CHECK_THROWS_AS(vq.pop(VersionedQueue::EMPTY), std::out_of_range);
    CHECK_THROWS_AS(vq.mean(VersionedQueue::EMPTY), std::out_of_range);
    int v = vq.pop(vq.push(VersionedQueue::EMPTY, 7));
    CHECK_THROWS_AS(vq.pop(v), std::out_of_range);
    CHECK_THROWS_AS(vq.push(-1, 1), std::invalid_argument);
    CHECK_THROWS_AS(vq.size(99), std::invalid_argument);
    CHECK_THROWS_AS(vq.mean(99), std::invalid_argument);
}

TEST(exact_sums_survive_overflow_across_versions, "part3,edge") {
    VersionedQueue vq;
    int v = VersionedQueue::EMPTY;
    for (int i = 0; i < 3; ++i) v = vq.push(v, MAX);
    CHECK_EQ(vq.mean(v), frac(MAX, 1));
    int w = vq.pop(vq.pop(v));
    CHECK_EQ(vq.mean(w), frac(MAX, 1));
    int z = vq.push(w, MIN);  // [MAX, MIN]: sum -1
    CHECK_EQ(vq.mean(z), frac(-1, 2));
}

TEST(random_branching_matches_the_copying_model, "part3,edge") {
    std::mt19937_64 rnd(7);
    VersionedQueue vq;
    std::vector<std::vector<long long>> model{{}};
    for (int step = 0; step < 6000; ++step) {
        const std::size_t base = rnd() % model.size();
        const auto content = model[base];  // copy: push_back below may reallocate `model`
        const auto r = rnd() % 10;
        int got;
        std::vector<long long> expected;
        if (r < 5 || (content.empty() && r < 9)) {
            const long long x = rnd() % 5 == 0 ? MAX : static_cast<long long>(rnd() % 2001) - 1000;
            got = vq.push(static_cast<int>(base), x);
            expected = content;
            expected.push_back(x);
        } else if (r < 9) {
            got = vq.pop(static_cast<int>(base));
            expected.assign(content.begin() + 1, content.end());
        } else {
            expected = {static_cast<long long>(rnd() % 10), static_cast<long long>(rnd() % 10)};
            got = vq.correct(expected);
        }
        CHECK_EQ(got, static_cast<int>(model.size()), "version ids are dense and increasing");
        model.push_back(expected);
        CHECK_EQ(vq.contents(got), expected);
        CHECK_EQ(vq.size(got), expected.size());
        if (!expected.empty()) {
            i128 s = 0;
            for (long long x : expected) s += x;
            CHECK_EQ(vq.mean(got), Mean(s, static_cast<long long>(expected.size())));
        }
    }
}

TEST(deep_chains_and_wide_branching_in_under_two_seconds, "part3,perf") {
    std::mt19937_64 rnd(0);
    VersionedQueue vq;
    const int n = 300'000;
    int v = VersionedQueue::EMPTY;
    int first = 0;
    CHECK_WITHIN_MS(2000, {
        for (int i = 0; i < n; ++i) v = vq.push(v, i);
        first = v;
        for (int i = 0; i < n; ++i) v = vq.pop(v);  // each pop needs the depth-(i+1) ancestor
        CHECK_EQ(vq.size(v), 0u);
        CHECK_EQ(vq.mean(first), Mean(static_cast<i128>(n) * (n - 1) / 2, n));
        std::vector<int> ids(200'000);
        ids[0] = first;
        for (std::size_t i = 1; i < ids.size(); ++i) {
            const int base = ids[rnd() % i];
            ids[i] = vq.size(base) == 0 || (rnd() & 1) ? vq.push(base, static_cast<long long>(rnd())) : vq.pop(base);
        }
    });
}

// ---- C++-only Part 3

TEST(growing_the_node_vector_never_leaves_a_dangling_reference, "part3,edge,cpp") {
    // push_back reallocates; any `const Node& p = nodes_[i]` held across it would read freed memory (ASan reports it).
    VersionedQueue vq;
    int v = VersionedQueue::EMPTY;
    std::vector<int> versions{v};
    for (int i = 0; i < 70'000; ++i) {
        v = vq.push(v, i);
        versions.push_back(v);
    }
    for (int i = 0; i < 70'000; i += 9'973) CHECK_EQ(vq.size(versions[static_cast<std::size_t>(i)]), static_cast<std::size_t>(i));
    int w = versions.back();
    for (int i = 0; i < 70'000; ++i) w = vq.pop(w);
    CHECK_EQ(vq.size(w), 0u);
    CHECK_EQ(vq.mean(versions.back()), Mean(static_cast<i128>(70'000) * 69'999 / 2, 70'000));
    CHECK_EQ(vq.contents(versions[3]), (std::vector<long long>{0, 1, 2}));
}

TEST(large_correct_and_pops_through_the_jump_pointers, "part3,edge,cpp") {
    VersionedQueue vq;
    std::vector<long long> big(100'000);
    for (std::size_t i = 0; i < big.size(); ++i) big[i] = static_cast<long long>(i) * 3 - 5;
    int v = vq.correct(big);
    CHECK_EQ(vq.contents(v), big);
    for (int i = 0; i < 99'990; ++i) v = vq.pop(v);
    CHECK_EQ(vq.contents(v), std::vector<long long>(big.end() - 10, big.end()));
}

// ================================================ Part 4: single writer, many lock-free readers

TEST(single_threaded_behaviour, "part4") {
    SharedMean sm;
    CHECK_EQ(sm.read().seq, 0u);
    CHECK(!sm.mean().has_value());
    sm.push(1); sm.push(2);
    CHECK_EQ(sm.mean(), std::optional<Mean>(frac(3, 2)));
    CHECK_EQ(sm.pop(), 1);
    CHECK_EQ(sm.read().seq, 3u);
    CHECK_EQ(sm.read().size, 1u);
    sm.pop();
    CHECK(!sm.mean().has_value());
    CHECK_THROWS_AS(sm.pop(), std::out_of_range);
}

TEST(second_writer_thread_is_rejected, "part4,edge") {
    SharedMean sm;
    sm.push(1);
    bool rejected = false;
    mt::ThreadErrors errors;
    std::thread t = errors.spawn([&] {
        try { sm.push(2); } catch (const SingleWriterViolation&) { rejected = true; }
    });
    t.join();
    CHECK_NO_THREAD_ERRORS(errors);
    CHECK(rejected);
    CHECK_EQ(sm.read().size, 1u);
    sm.push(3);  // the original writer is unaffected
    CHECK_EQ(sm.read().size, 2u);
}

/// Invariant: the queue only ever holds 7s, so every consistent snapshot has mean 7/1 (or is empty) and sum == 7*size.
/// A torn read (new sum with old size, or half of a 128-bit sum) breaks it.
TEST(readers_always_see_a_consistent_mean, "part4,conc") {
    constexpr int readers = 4, ops = 3000, rounds = 25;
    for (int round = 0; round < rounds; ++round) {
        SharedMean sm;
        std::atomic<bool> start{false}, done{false};
        std::atomic<int> problems{0};
        std::string first_problem;
        std::mutex problem_mutex;
        auto report = [&](const std::string& what) {
            if (problems.fetch_add(1) == 0) { std::lock_guard<std::mutex> g(problem_mutex); first_problem = what; }
        };
        std::vector<std::thread> threads;
        mt::ThreadErrors errors;
        auto guard_done = [&] { done.store(true); };  // a failing writer must still release the spinning readers
        for (int r = 0; r < readers; ++r)
            threads.push_back(errors.spawn([&] {
                while (!start.load()) std::this_thread::yield();
                std::uint64_t last_seq = 0;
                std::uint64_t reads = 0;
                while (!done.load() || reads < 1) {
                    const Stat st = sm.read();
                    ++reads;
                    if (st.seq < last_seq) report("seq went backwards");
                    last_seq = st.seq;
                    const auto m = st.mean();
                    if (st.size == 0 ? m.has_value() : !(m && *m == frac(7, 1))) report("torn read: size=" + std::to_string(st.size));
                    if (st.sum != static_cast<i128>(7) * static_cast<i128>(st.size)) report("sum/size mismatch");
                }
            }));
        std::size_t final_size = 0;
        std::thread writer = errors.spawn([&] {
            std::mt19937_64 rnd(42);
            while (!start.load()) std::this_thread::yield();
            std::size_t size = 0;
            try {
                for (int i = 0; i < ops; ++i) {
                    if (size == 0 || rnd() % 100 < 55) { sm.push(7); ++size; }
                    else { sm.pop(); --size; }
                }
            } catch (...) { guard_done(); throw; }
            final_size = size;
            guard_done();
        });
        start.store(true);
        writer.join();
        for (auto& t : threads) t.join();
        CHECK_NO_THREAD_ERRORS(errors);
        if (!errors.empty()) break;
        CHECK_EQ(problems.load(), 0, first_problem);
        CHECK_EQ(sm.read().size, final_size);
        CHECK_EQ(sm.read().seq, static_cast<std::uint64_t>(ops));
    }
}

// ---- C++-only Part 4

TEST(stat_is_a_plain_value_and_the_counters_are_lock_free, "part4,edge,cpp") {
    static_assert(std::is_trivially_copyable_v<Stat>, "a snapshot must be copyable with memcpy semantics");
    static_assert(std::atomic<std::uint64_t>::is_always_lock_free, "readers must not take a hidden lock");
    SharedMean sm;
    sm.push(5);
    Stat a = sm.read();
    sm.push(6);
    Stat b = sm.read();
    CHECK_EQ(a.size, 1u);  // a snapshot is a copy: later writes do not change it
    CHECK_EQ(b.size, 2u);
    CHECK_NE(a, b);
}

TEST(failed_pop_publishes_nothing, "part4,edge,cpp") {
    SharedMean sm;
    const Stat before = sm.read();
    CHECK_THROWS_AS(sm.pop(), std::out_of_range);
    CHECK_EQ(sm.read(), before);  // the failed operation did not bump seq
    sm.push(1);
    CHECK_EQ(sm.read().seq, 1u);
}

TEST(sums_beyond_64_bits_are_published_whole, "part4,edge,cpp") {
    SharedMean sm;
    for (int i = 0; i < 3; ++i) sm.push(MAX);
    const Stat s = sm.read();
    CHECK(s.sum == static_cast<i128>(MAX) * 3);  // needs both 64-bit halves
    CHECK_EQ(sm.mean(), std::optional<Mean>(frac(MAX, 1)));
    for (int i = 0; i < 3; ++i) sm.pop();
    CHECK(sm.read().sum == 0);
}

MT_MAIN()
