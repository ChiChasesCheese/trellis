// ld01 · Shared-memory SPSC message channel — C++20 tests.  Same cases as test/LongQueueContract.java, LongRingTest.java,
// SpscLongRingTest.java, MessageRingTest.java, SharedChannelTest.java (the Java child JVM becomes a fork()ed child process)
// plus C++-only edge cases (tag "cpp"): cache-line alignment, non-movable atomics, misaligned segments, optional<empty>
// vs nullopt, move-only channel, errno-carrying exceptions.
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <climits>
#include <cstring>
#include <deque>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <random>
#include <string>
#include <string_view>
#include <thread>
#include <type_traits>

#include <signal.h>
#include <sys/wait.h>
#include <unistd.h>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace spsc;

namespace {
using Clock = std::chrono::steady_clock;

Bytes bytes(std::size_t len, int fill) { return Bytes(len, static_cast<std::uint8_t>(fill)); }
Bytes bytes_of(std::string_view s) { return Bytes(s.begin(), s.end()); }

/// Zeroed, 128-byte aligned native memory (Java: Arena.ofShared().allocate(n, 128)).
class Seg {
public:
    explicit Seg(std::size_t n) : n_(n) {
        const std::size_t rounded = (n + 127) / 128 * 128;  // aligned_alloc wants a multiple of the alignment
        p_ = static_cast<std::byte*>(std::aligned_alloc(128, rounded));
        if (p_ == nullptr) throw std::bad_alloc();
        std::memset(p_, 0, rounded);
    }
    Seg(const Seg&) = delete;
    Seg& operator=(const Seg&) = delete;
    ~Seg() { std::free(p_); }
    std::span<std::byte> span() const { return {p_, n_}; }
private:
    std::byte* p_;
    std::size_t n_;
};
std::unique_ptr<Seg> segment(int capacity) { return std::make_unique<Seg>(MessageRing::segment_bytes(capacity)); }

/// Same deterministic messages as Msgs.java: length 8..56, the first 8 bytes are the sequence number (big-endian).
std::uint64_t mix(std::uint64_t x) {  // splitmix64
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}
Bytes make_msg(std::uint64_t seq) {
    const std::uint64_t m = mix(seq);
    const std::size_t len = 8 + static_cast<std::size_t>((m >> 1) % 49);
    Bytes b(len);
    for (int i = 0; i < 8; ++i) b[i] = static_cast<std::uint8_t>(seq >> (56 - 8 * i));
    for (std::size_t i = 8; i < len; ++i) b[i] = static_cast<std::uint8_t>(m >> ((i & 7) * 8));
    return b;
}
/// "" = correct, otherwise what is wrong.
std::string check_msg(const std::optional<Bytes>& got, std::uint64_t seq) {
    if (!got) return "no message at seq " + std::to_string(seq);
    if (got->size() < 8) return "short message (" + std::to_string(got->size()) + " bytes) at seq " + std::to_string(seq);
    std::uint64_t got_seq = 0;
    for (int i = 0; i < 8; ++i) got_seq = got_seq << 8 | (*got)[i];
    if (got_seq != seq) return "expected seq " + std::to_string(seq) + " but got " + std::to_string(got_seq) + " (lost, duplicated or reordered)";
    if (*got != make_msg(seq)) return "corrupt payload at seq " + std::to_string(seq);
    return "";
}

// ---- spinning with a way out: a stuck ring must fail the test, never hang it ---------------------------------------
inline void cpu_relax() {
#if defined(__aarch64__)
    asm volatile("yield" ::: "memory");
#elif defined(__x86_64__)
    __builtin_ia32_pause();
#endif
}
struct Gate {
    std::atomic<bool> abort{false}, stalled{false};
    Clock::time_point deadline;
    explicit Gate(int seconds = 10) : deadline(Clock::now() + std::chrono::seconds(seconds)) {}
};
/// One spin iteration.  false = give up (the other thread failed or the deadline passed).
struct Spin {
    Gate& g;
    unsigned n = 0;
    bool operator()() {
        cpu_relax();
        if ((++n & 0xFF) != 0) return true;
        std::this_thread::yield();
        if (g.abort.load(std::memory_order_relaxed)) return false;
        if (Clock::now() > g.deadline) { g.stalled = true; g.abort = true; return false; }
        return true;
    }
};
/// std::thread whose uncaught exception is recorded (not std::terminate) and aborts the other side.
template <class F> std::thread spawn(mt::ThreadErrors& errs, Gate& gate, F f) {
    return errs.spawn([&gate, f = std::move(f)]() mutable {
        try { f(); } catch (...) { gate.abort = true; throw; }
    });
}

/// Producer sends 0..n-1, the consumer must receive each exactly once, in order.  "" = fine.
std::string transfer(int capacity, long long n) {
    SpscLongRing ring(capacity);
    Gate gate;
    mt::ThreadErrors errs;
    std::atomic<bool> go{false};
    std::atomic<long long> error{-1};
    auto producer = spawn(errs, gate, [&] {
        while (!go.load(std::memory_order_acquire)) std::this_thread::yield();
        Spin spin{gate};
        for (long long i = 0; i < n; ++i)
            while (!ring.offer(i)) if (!spin()) return;
    });
    auto consumer = spawn(errs, gate, [&] {
        while (!go.load(std::memory_order_acquire)) std::this_thread::yield();
        Spin spin{gate};
        for (long long expect = 0; expect < n; ++expect) {
            while (ring.is_empty()) if (!spin()) return;
            const long long got = ring.poll();
            if (got != expect) { long long none = -1; error.compare_exchange_strong(none, expect); gate.abort = true; return; }
        }
    });
    go = true;
    producer.join();
    consumer.join();
    if (!errs.empty()) return "exception in a thread: " + errs.first();
    if (gate.stalled) return "timeout (ring stalled)";
    return error.load() < 0 ? "" : "first mismatch at seq " + std::to_string(error.load());
}

// ================================================ Parts 1 and 2: one contract, two implementations
using Make = std::unique_ptr<LongQueue> (*)(int);
std::unique_ptr<LongQueue> make_ring(int c) { return std::make_unique<LongRing>(c); }
std::unique_ptr<LongQueue> make_spsc(int c) { return std::make_unique<SpscLongRing>(c); }
}  // namespace

// CONTRACT(name, extra tags, body): the body takes `Make make`; LongRing runs it as part1, SpscLongRing (single thread) as part2.
#define CONTRACT(name, extra, ...)                                                    \
    namespace { void contract_##name(Make make) __VA_ARGS__ }                         \
    TEST(ring_##name, "part1" extra) { contract_##name(make_ring); }                  \
    TEST(spsc_sequential_##name, "part2" extra) { contract_##name(make_spsc); }

CONTRACT(fifo_order, "", {
    auto q = make(8);
    for (long long i = 1; i <= 5; ++i) CHECK(q->offer(i * 10));
    CHECK_EQ(q->size(), 5);
    for (long long i = 1; i <= 5; ++i) CHECK_EQ(q->poll(), i * 10);
    CHECK(q->is_empty());
    CHECK_EQ(q->size(), 0);
})

CONTRACT(full_and_empty_rules, ",edge", {
    auto q = make(4);
    CHECK(q->is_empty());
    CHECK(!q->is_full());
    for (int i = 0; i < 4; ++i) CHECK(q->offer(i));
    CHECK(q->is_full());
    CHECK(!q->is_empty());
    CHECK(!q->offer(99), "full must refuse, never overwrite the oldest element");
    CHECK_EQ(q->size(), 4);
    CHECK_EQ(q->poll(), 0);  // free one slot
    CHECK(!q->is_full());
    CHECK(q->offer(4));  // wraps to the start of the array
    CHECK(q->is_full());
    for (int i = 1; i <= 4; ++i) CHECK_EQ(q->poll(), i);
    CHECK(q->is_empty());
})

CONTRACT(poll_on_empty_throws, ",edge", {
    auto q = make(2);
    CHECK_THROWS_AS(q->poll(), EmptyError);
    q->offer(1);
    q->poll();
    CHECK_THROWS_AS(q->poll(), EmptyError);
})

CONTRACT(capacity_one_works, ",edge", {
    auto q = make(1);
    CHECK_EQ(q->capacity(), 1);
    for (int round = 0; round < 10; ++round) {
        CHECK(q->offer(round));
        CHECK(!q->offer(-1));
        CHECK_EQ(q->poll(), round);
    }
})

CONTRACT(every_long_is_a_valid_message, ",edge", {
    // no sentinel value: LLONG_MIN, -1, 0 and LLONG_MAX all go in and out unchanged
    auto q = make(4);
    const long long vs[] = {LLONG_MIN, -1, 0, LLONG_MAX};
    for (long long v : vs) q->offer(v);
    for (long long v : vs) CHECK_EQ(q->poll(), v);
})

CONTRACT(counters_keep_working_after_many_wraps, ",edge", {
    auto q = make(4);
    long long next = 0, expect = 0;
    for (int i = 0; i < 1'000'000; ++i) {  // far more than capacity, far more than 2^16: the counters keep growing
        q->offer(next++);
        q->offer(next++);
        CHECK_EQ(q->poll(), expect++);
        CHECK_EQ(q->poll(), expect++);
    }
    CHECK(q->is_empty());
})

CONTRACT(rejects_non_power_of_two_capacity, ",edge", {
    for (int bad : {0, -1, -8, 3, 6, 12, 1000, (1 << 30) + 1, INT_MAX, INT_MIN})
        CHECK_THROWS_AS(make(bad), std::invalid_argument, "capacity " + std::to_string(bad));
})

CONTRACT(random_ops_match_a_deque, "", {
    std::mt19937_64 rnd(0);
    auto q = make(16);
    std::deque<long long> model;
    for (int step = 0; step < 200'000; ++step) {
        if (rnd() % 100 < 55) {
            const long long v = static_cast<long long>(rnd());
            const bool ok = q->offer(v);
            CHECK_EQ(ok, model.size() < 16);
            if (ok) model.push_back(v);
        } else if (model.empty()) {
            CHECK_THROWS_AS(q->poll(), EmptyError);
        } else {
            CHECK_EQ(q->poll(), model.front());
            model.pop_front();
        }
        CHECK_EQ(q->size(), static_cast<int>(model.size()));
    }
})

CONTRACT(twenty_million_ops_single_thread, ",perf", {
    auto q = make(1024);
    long long sum = 0;
    CHECK_WITHIN_MS(2000,
        for (int i = 0; i < 10'000'000; ++i) {
            q->offer(i);
            sum += q->poll();
        });
    CHECK_EQ(sum, 49'999'995'000'000LL);
})

TEST(max_capacity_constant, "part1") {
    CHECK_EQ(LongRing::MAX_CAPACITY, 1 << 30);
    CHECK_EQ(SpscLongRing::MAX_CAPACITY, 1 << 30);
}

// ================================================ Part 2: one producer thread + one consumer thread

TEST(in_order_exactly_once_tiny_ring, "part2,conc") {
    for (int rep = 0; rep < 10; ++rep) REQUIRE_EQ(transfer(2, 200'000), "", "capacity 2: nearly every message wraps and tests full/empty; rep " + std::to_string(rep));
}

TEST(in_order_exactly_once_medium_ring, "part2,conc") {
    for (int rep = 0; rep < 10; ++rep) REQUIRE_EQ(transfer(64, 300'000), "", "rep " + std::to_string(rep));
}

TEST(capacity_one_ring_between_threads, "part2,conc") { REQUIRE_EQ(transfer(1, 100'000), ""); }

TEST(consumer_never_sees_a_stale_slot, "part2,conc") {
    // Visibility: every value carries its own check - what the consumer reads must be what the producer wrote for that
    // sequence number (not the previous lap's value, not zero).  Break release/acquire and ARM fails this at once.
    constexpr long long n = 200'000;
    constexpr std::uint64_t K = 0x9E3779B97F4A7C15ULL;
    for (int rep = 0; rep < 10; ++rep) {
        SpscLongRing ring(8);
        Gate gate;
        mt::ThreadErrors errs;
        std::atomic<bool> go{false};
        std::atomic<long long> bad{0};
        auto p = spawn(errs, gate, [&] {
            while (!go.load()) std::this_thread::yield();
            Spin spin{gate};
            for (long long i = 1; i <= n; ++i) {
                const long long v = static_cast<long long>(static_cast<std::uint64_t>(i) * K);
                while (!ring.offer(v)) if (!spin()) return;
            }
        });
        auto c = spawn(errs, gate, [&] {
            while (!go.load()) std::this_thread::yield();
            Spin spin{gate};
            for (long long i = 1; i <= n; ++i) {
                while (ring.is_empty()) if (!spin()) return;
                if (ring.poll() != static_cast<long long>(static_cast<std::uint64_t>(i) * K)) ++bad;
            }
        });
        go = true;
        p.join();
        c.join();
        CHECK_NO_THREAD_ERRORS(errs);
        REQUIRE(!gate.stalled, "ring stalled");
        REQUIRE_EQ(bad.load(), 0);
        CHECK(ring.is_empty());
    }
}

TEST(size_from_any_thread_stays_within_bounds, "part2,edge") {
    SpscLongRing ring(16);
    Gate gate;
    mt::ThreadErrors errs;
    std::atomic<bool> stop{false};
    std::atomic<long long> bad{0};
    auto observer = spawn(errs, gate, [&] {
        while (!stop.load(std::memory_order_relaxed)) {
            const int s = ring.size();
            if (s < 0 || s > 16) ++bad;
        }
    });
    auto producer = spawn(errs, gate, [&] {
        Spin spin{gate};
        for (long long i = 0; i < 300'000; ++i)
            while (!ring.offer(i)) if (!spin()) return;
    });
    Spin spin{gate};
    for (long long i = 0; i < 300'000; ++i) {
        while (ring.is_empty()) if (!spin()) break;
        if (gate.abort) break;
        ring.poll();
    }
    producer.join();
    stop = true;
    observer.join();
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK(!gate.stalled);
    CHECK_EQ(bad.load(), 0);
}

TEST(ten_million_messages_between_two_threads, "part2,perf,conc") {
    std::string err;
    CHECK_WITHIN_MS(2000, err = transfer(1 << 14, 10'000'000););
    CHECK_EQ(err, "");
}

// ---- C++-only: layout and ownership of the ring object

static_assert(std::atomic<std::uint64_t>::is_always_lock_free, "a lock hiding behind std::atomic would break the 'no locks' promise");
static_assert(std::atomic_ref<std::uint64_t>::is_always_lock_free, "the shared header words must be real atomic instructions");
static_assert(!std::is_copy_constructible_v<SpscLongRing> && !std::is_move_constructible_v<SpscLongRing>,
              "std::atomic members: the ring's identity is its address");

TEST(spsc_ring_keeps_producer_and_consumer_state_on_separate_cache_lines, "part2,cpp") {
    // head and tail are each declared alignas(kCacheLine), so they cannot share a line; the class alignment and size follow.
    CHECK_GE(kCacheLine, 64u);
    CHECK_GE(alignof(SpscLongRing), kCacheLine);
    CHECK_GE(sizeof(SpscLongRing), 2 * kCacheLine);
    auto ring = std::make_unique<SpscLongRing>(8);  // over-aligned new (C++17): the heap object honours alignof
    CHECK_EQ(reinterpret_cast<std::uintptr_t>(ring.get()) % kCacheLine, 0u);
}

TEST(ring_copy_is_independent_and_move_falls_back_to_copy, "part1,cpp") {
    LongRing a(4);
    a.offer(1);
    a.offer(2);
    LongRing b = a;  // deep copy
    b.offer(3);
    CHECK_EQ(a.size(), 2);
    CHECK_EQ(b.size(), 3);
    LongRing c = std::move(a);  // no move constructor is declared: this copies, and `a` stays a valid ring
    CHECK_EQ(c.size(), 2);
    CHECK_EQ(a.size(), 2);
    CHECK(a.offer(7));
    CHECK_EQ(a.poll(), 1);
}

// ================================================ Part 3: variable-length messages

TEST(init_then_attach_sees_the_same_ring, "part3") {
    auto seg = segment(64);
    auto producer = MessageRing::init(seg->span(), 64);
    auto consumer = MessageRing::attach(seg->span());
    CHECK_EQ(consumer.capacity(), 64);
    CHECK_EQ(consumer.max_payload(), 60);
    CHECK(producer.offer(bytes_of("hello")));
    CHECK_EQ(consumer.poll(), std::optional<Bytes>(bytes_of("hello")));
    CHECK(!consumer.poll());
}

TEST(attach_rejects_garbage, "part3,edge") {
    CHECK_THROWS_AS(MessageRing::attach(segment(64)->span()), StateError);  // all zero: no magic
    auto seg = segment(64);
    MessageRing::init(seg->span(), 64);
    CHECK_THROWS_AS(MessageRing::attach(seg->span().first(100)), StateError);  // size does not match the header
    Seg tiny(8);
    CHECK_THROWS_AS(MessageRing::attach(tiny.span()), StateError);
}

TEST(init_rejects_bad_capacity, "part3,edge") {
    auto seg = segment(64);
    for (int bad : {0, 1, 8, 15, 17, 24, 100, -16, (1 << 30) + 1, INT_MIN})
        CHECK_THROWS_AS(MessageRing::init(seg->span(), bad), std::invalid_argument, "capacity " + std::to_string(bad));
}

TEST(init_rejects_a_too_small_segment, "part3,edge") {
    Seg small(MessageRing::HEADER_BYTES + 32);
    CHECK_THROWS_AS(MessageRing::init(small.span(), 64), std::invalid_argument);
}

TEST(header_layout_constants, "part3") {
    CHECK_EQ(MessageRing::HEADER_BYTES, 512);
    CHECK_EQ(MessageRing::segment_bytes(1024), 512u + 1024u);
    CHECK_THROWS_AS(MessageRing::segment_bytes(100), std::invalid_argument);
}

TEST(fifo_with_varied_lengths_including_empty_and_binary, "part3") {
    auto seg = segment(256);
    auto ring = MessageRing::init(seg->span(), 256);
    const std::vector<Bytes> msgs = {Bytes{}, Bytes{0}, Bytes{0xFF, 0, 0x80}, bytes(5, 7), bytes(100, 0xAB), bytes(4, 1), bytes(3, 2)};
    for (const auto& m : msgs) CHECK(ring.offer(m));
    for (const auto& m : msgs) CHECK_EQ(ring.poll(), std::optional<Bytes>(m));
    CHECK(!ring.poll());
}

TEST(offer_copies_the_callers_bytes, "part3,edge") {
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    Bytes m = {1, 2, 3};
    ring.offer(m);
    m[0] = 99;  // the span only borrowed the vector: the ring holds its own copy
    auto got = ring.poll();
    REQUIRE(got.has_value());
    CHECK_EQ(*got, (Bytes{1, 2, 3}));
    (*got)[1] = 42;  // the returned vector is owned by the caller: touching it must not hurt the ring
    CHECK(!ring.poll());
}

TEST(full_rule_uses_aligned_record_sizes, "part3,edge") {
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    for (int i = 0; i < 4; ++i) CHECK(ring.offer(bytes(12, i)), "record " + std::to_string(i));  // len 12 -> 4 + 12 = 16 bytes; 64 / 16 = 4
    CHECK(!ring.offer(bytes(12, 9)));
    CHECK(!ring.offer(Bytes{}), "not one byte left: even an empty message does not fit");
    CHECK_EQ(ring.bytes_pending(), 64);
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(12, 0)));
    CHECK(ring.offer(bytes(12, 9)));  // exactly 16 bytes free, and the write wraps
    for (int i = 1; i < 4; ++i) CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(12, i)));
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(12, 9)));
    CHECK(!ring.poll());
}

TEST(records_pad_to_eight_bytes, "part3,edge") {
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    for (int i = 0; i < 8; ++i) CHECK(ring.offer(Bytes{}));  // an empty message takes 8 bytes
    CHECK(!ring.offer(Bytes{}));
    for (int i = 0; i < 8; ++i) CHECK_EQ(ring.poll()->size(), 0u);
    for (int i = 0; i < 8; ++i) CHECK(ring.offer(bytes(4, 1)));  // 4 + 4 = 8, still 8
    CHECK(!ring.offer(bytes(4, 1)));
    for (int i = 0; i < 8; ++i) ring.poll();
    for (int i = 0; i < 4; ++i) CHECK(ring.offer(bytes(5, 1)));  // 4 + 5 = 9 -> 16
    CHECK(!ring.offer(bytes(0, 1)));
}

TEST(max_payload_fits_an_empty_ring_and_one_more_byte_never, "part3,edge") {
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    const Bytes max = bytes(static_cast<std::size_t>(ring.max_payload()), 0x5A);
    CHECK(ring.offer(max));
    CHECK_EQ(ring.bytes_pending(), 64);
    CHECK_EQ(ring.poll(), std::optional<Bytes>(max));
    CHECK_THROWS_AS(ring.offer(bytes(static_cast<std::size_t>(ring.max_payload()) + 1, 1)), std::invalid_argument);  // never fits != merely full
}

TEST(wrap_around_writes_pad_then_record_at_start, "part3,edge") {
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    CHECK(ring.offer(bytes(20, 1)));  // 24 bytes
    CHECK(ring.offer(bytes(20, 2)));  // 24 bytes, tail = 48
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(20, 1)));
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(20, 2)));
    CHECK_EQ(ring.bytes_pending(), 0);
    CHECK(ring.offer(bytes(20, 3)));  // 16 bytes left < 24: a 16-byte PAD first, then 24 bytes from offset 0
    CHECK_EQ(ring.bytes_pending(), 16 + 24);
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(20, 3)));  // the consumer steps over the PAD
    CHECK_EQ(ring.bytes_pending(), 0);
    CHECK(!ring.poll());
}

TEST(pad_is_published_even_if_the_record_does_not_fit, "part3,edge") {
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    CHECK(ring.offer(bytes(20, 1)));
    CHECK(ring.offer(bytes(20, 2)));  // tail = 48, nothing consumed yet
    CHECK(!ring.offer(bytes(20, 3)));  // the PAD fits (16 free bytes), the record after it does not -> false
    CHECK_EQ(ring.bytes_pending(), 48 + 16);  // but the PAD is already published
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(20, 1)));
    CHECK(ring.offer(bytes(20, 3)));  // 24 bytes free, already at offset 0: fits
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(20, 2)));
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes(20, 3)));
    CHECK(!ring.poll());
}

TEST(an_empty_ring_accepts_a_max_size_message_from_every_position, "part3,edge") {
    // Liveness: wherever tail stops (even 8 bytes before the end), on an empty ring offer -> (consumer steps over the PAD)
    // -> offer must take the largest message.  Otherwise: deadlock.
    std::mt19937 rnd(0);
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    const Bytes max = bytes(static_cast<std::size_t>(ring.max_payload()), 0x33);
    for (int round = 0; round < 500; ++round) {
        const int steps = static_cast<int>(rnd() % 5);
        for (int i = 0; i < steps; ++i) {
            const Bytes m = bytes(rnd() % 30, round);
            if (!ring.offer(m)) {  // a PAD was published first: the consumer has to step over it
                CHECK(!ring.poll());
                CHECK(ring.offer(m));
            }
            CHECK_EQ(ring.poll(), std::optional<Bytes>(m));
        }
        CHECK(!ring.poll());
        bool ok = ring.offer(max);
        if (!ok) {
            CHECK(!ring.poll());
            ok = ring.offer(max);
        }
        REQUIRE(ok, "round " + std::to_string(round) + ": offer, poll, offer on an empty ring still cannot place the max message -> deadlock");
        CHECK_EQ(ring.poll(), std::optional<Bytes>(max));
    }
}

TEST(random_operations_keep_fifo_and_never_lose_a_message, "part3") {
    std::mt19937 rnd(0);
    auto seg = segment(256);
    auto ring = MessageRing::init(seg->span(), 256);
    std::deque<Bytes> model;
    long long accepted = 0, rejected = 0;
    for (int step = 0; step < 300'000; ++step) {
        if (rnd() % 100 < 52) {
            const Bytes m = bytes(rnd() % static_cast<unsigned>(ring.max_payload() / 3), step);
            if (ring.offer(m)) { model.push_back(m); ++accepted; } else ++rejected;
        } else {
            const auto got = ring.poll();
            if (model.empty()) {
                CHECK(!got);
            } else {
                CHECK_EQ(got, std::optional<Bytes>(model.front()), "step " + std::to_string(step));
                model.pop_front();
            }
        }
        CHECK_LE(ring.bytes_pending(), 256);
    }
    CHECK(accepted > 10'000 && rejected > 100, "the test must really reach full and wrap-around: accepted=" + std::to_string(accepted) + " rejected=" + std::to_string(rejected));
    while (!model.empty()) { CHECK_EQ(ring.poll(), std::optional<Bytes>(model.front())); model.pop_front(); }
    CHECK(!ring.poll());
}

TEST(drained_means_finished_and_empty, "part3") {
    auto seg = segment(64);
    auto producer = MessageRing::init(seg->span(), 64);
    auto consumer = MessageRing::attach(seg->span());
    CHECK(!consumer.is_drained(), "empty but the producer has not said 'done' != drained");
    producer.offer(bytes(3, 1));
    producer.offer(bytes(3, 2));
    producer.finish();
    producer.finish();  // idempotent
    CHECK(!consumer.is_drained(), "two messages still unread");
    CHECK(consumer.poll().has_value());
    CHECK(!consumer.is_drained());
    CHECK(consumer.poll().has_value());
    CHECK(consumer.is_drained());
    CHECK(!consumer.poll());
    CHECK(consumer.is_drained());
    CHECK_THROWS_AS(producer.offer(bytes(1, 1)), StateError);
}

TEST(trailing_pad_is_consumed_before_drained, "part3,edge") {
    auto seg = segment(64);
    auto producer = MessageRing::init(seg->span(), 64);
    auto consumer = MessageRing::attach(seg->span());
    producer.offer(bytes(20, 1));
    producer.offer(bytes(20, 2));
    CHECK(!producer.offer(bytes(20, 3)));  // leaves a lone PAD behind
    producer.finish();
    CHECK(consumer.poll().has_value());
    CHECK(consumer.poll().has_value());
    CHECK(!consumer.is_drained(), "a PAD at the end has not been stepped over yet");
    CHECK(!consumer.poll());  // poll steps over the PAD and reports 'no message'
    CHECK(consumer.is_drained());
}

TEST(producer_and_consumer_threads_exchange_in_order_exactly_once, "part3,conc") {
    constexpr long long n = 20'000;
    for (int rep = 0; rep < 10; ++rep) {
        auto seg = segment(256);  // small ring: it wraps every few messages
        auto producer = MessageRing::init(seg->span(), 256);
        auto consumer = MessageRing::attach(seg->span());
        Gate gate;
        mt::ThreadErrors errs;
        std::atomic<bool> go{false};
        std::string error;
        long long received = 0;
        auto p = spawn(errs, gate, [&] {
            while (!go.load()) std::this_thread::yield();
            Spin spin{gate};
            for (long long i = 0; i < n; ++i) {
                const Bytes m = make_msg(static_cast<std::uint64_t>(i));
                while (!producer.offer(m)) if (!spin()) return;
            }
            producer.finish();
        });
        auto c = spawn(errs, gate, [&] {
            while (!go.load()) std::this_thread::yield();
            Spin spin{gate};
            long long expect = 0;
            while (!consumer.is_drained()) {
                auto m = consumer.poll();
                if (!m) { if (!spin()) return; continue; }
                error = check_msg(m, static_cast<std::uint64_t>(expect));
                if (!error.empty()) { gate.abort = true; return; }
                ++expect;
            }
            received = expect;
        });
        go = true;
        p.join();
        c.join();
        CHECK_NO_THREAD_ERRORS(errs);
        REQUIRE(!gate.stalled, "ring stalled");
        REQUIRE_EQ(error, "");
        REQUIRE_EQ(received, n);
    }
}

TEST(two_million_messages_single_thread, "part3,perf") {
    auto seg = segment(1 << 12);
    auto ring = MessageRing::init(seg->span(), 1 << 12);
    const Bytes m = bytes(24, 7);
    long long total = 0;
    CHECK_WITHIN_MS(2000,
        for (int i = 0; i < 2'000'000; ++i) {
            if (!ring.offer(m)) { total = -1; break; }
            total += static_cast<long long>(ring.poll()->size());
        });
    CHECK_EQ(total, 48'000'000LL);
}

TEST(two_million_messages_between_threads, "part3,perf,conc") {
    auto seg = segment(1 << 16);
    auto producer = MessageRing::init(seg->span(), 1 << 16);
    auto consumer = MessageRing::attach(seg->span());
    constexpr long long n = 2'000'000;
    Gate gate;
    mt::ThreadErrors errs;
    std::string error;
    long long expect = 0;
    CHECK_WITHIN_MS(3000,
        auto p = spawn(errs, gate, [&] {
            Spin spin{gate};
            for (long long i = 0; i < n; ++i) {
                const Bytes m = make_msg(static_cast<std::uint64_t>(i));
                while (!producer.offer(m)) if (!spin()) return;
            }
            producer.finish();
        });
        Spin spin{gate};
        while (!consumer.is_drained()) {
            auto m = consumer.poll();
            if (!m) { if (!spin()) break; continue; }
            error = check_msg(m, static_cast<std::uint64_t>(expect));
            if (!error.empty()) { gate.abort = true; break; }
            ++expect;
        }
        p.join(););
    CHECK_NO_THREAD_ERRORS(errs);
    CHECK_EQ(error, "");
    CHECK_EQ(expect, n);
}

// ---- C++-only: the byte-span API

static_assert(std::is_same_v<decltype(std::declval<MessageRing&>().poll()), std::optional<Bytes>>);

TEST(an_empty_message_is_not_the_same_as_no_message, "part3,cpp") {
    // Java: byte[0] vs null.  Here: optional holding an empty vector vs nullopt - two different values by construction.
    auto seg = segment(64);
    auto ring = MessageRing::init(seg->span(), 64);
    CHECK(ring.offer(Bytes{}));
    auto got = ring.poll();
    REQUIRE(got.has_value());
    CHECK(got->empty());
    CHECK(!ring.poll().has_value());
}

TEST(misaligned_segments_are_refused_up_front, "part3,cpp,edge") {
    // The header words are accessed through std::atomic_ref<uint64_t>, which requires 8-byte alignment: a segment that starts
    // at an odd address would be undefined behaviour on the first load, so init/attach check it.
    Seg big(MessageRing::segment_bytes(64) + 16);
    auto shifted = big.span().subspan(4);  // 128-aligned + 4
    CHECK_THROWS_AS(MessageRing::init(shifted, 64), std::invalid_argument);
    CHECK_THROWS_AS(MessageRing::attach(shifted), StateError);
    // the aligned version of the same memory works
    CHECK_NOTHROW(MessageRing::init(big.span().subspan(8), 64));
}

TEST(offer_accepts_any_contiguous_byte_range, "part3,cpp") {
    auto seg = segment(128);
    auto ring = MessageRing::init(seg->span(), 128);
    const std::uint8_t raw[3] = {9, 8, 7};
    CHECK(ring.offer(std::span<const std::uint8_t>(raw)));  // C array
    std::array<std::uint8_t, 2> arr = {1, 2};
    CHECK(ring.offer(arr));                                  // std::array
    CHECK(ring.offer(bytes_of("xyz")));                      // vector
    CHECK_EQ(ring.poll(), std::optional<Bytes>(Bytes(std::begin(raw), std::end(raw))));
    CHECK_EQ(ring.poll(), std::optional<Bytes>(Bytes{1, 2}));
    CHECK_EQ(ring.poll(), std::optional<Bytes>(bytes_of("xyz")));
}

// ================================================ Part 4: memory-mapped file, two processes

namespace {
namespace fs = std::filesystem;

class TempDir {
public:
    TempDir() {
        auto pattern = (fs::temp_directory_path() / "ld01_spsc_XXXXXX").string();
        if (::mkdtemp(pattern.data()) == nullptr) throw std::runtime_error("mkdtemp failed");
        path_ = pattern;
    }
    TempDir(const TempDir&) = delete;
    TempDir& operator=(const TempDir&) = delete;
    ~TempDir() { std::error_code ec; fs::remove_all(path_, ec); }
    fs::path operator/(const char* name) const { return path_ / name; }
private:
    fs::path path_;
};

void write_file(const fs::path& p, const Bytes& b) {
    std::ofstream out(p, std::ios::binary | std::ios::trunc);
    out.write(reinterpret_cast<const char*>(b.data()), static_cast<std::streamsize>(b.size()));
}
Bytes read_file(const fs::path& p) {
    std::ifstream in(p, std::ios::binary);
    return Bytes(std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>());
}

constexpr int CHILD_TIMEOUT_MS = 20'000;

/// Same logic on both sides of the process boundary (Java: SpscChild.consume / produce).  "" = success.
std::string consume(SharedChannel& ch, long long count, Clock::time_point deadline) {
    long long expect = 0;
    unsigned spins = 0;
    while (expect < count) {
        auto m = ch.receive();
        if (!m) {
            cpu_relax();
            if ((++spins & 0x3FF) == 0) {
                std::this_thread::yield();
                if (Clock::now() > deadline) return "timeout after " + std::to_string(expect) + " of " + std::to_string(count) + " messages";
            }
            continue;
        }
        if (auto err = check_msg(m, static_cast<std::uint64_t>(expect)); !err.empty()) return err;
        ++expect;
    }
    while (!ch.is_drained()) {  // exactly `count` messages: nothing extra afterwards, and the producer must have finished
        if (ch.receive()) return "unexpected extra message after " + std::to_string(count) + " (duplicate?)";
        if (Clock::now() > deadline) return "producer never finished";
        cpu_relax();
    }
    return "";
}
std::string produce(SharedChannel& ch, long long count, Clock::time_point deadline) {
    unsigned spins = 0;
    for (long long i = 0; i < count; ++i) {
        const Bytes m = make_msg(static_cast<std::uint64_t>(i));
        while (!ch.send(m)) {
            cpu_relax();
            if ((++spins & 0x3FF) == 0) {
                std::this_thread::yield();
                if (Clock::now() > deadline) return "timeout: consumer too slow at seq " + std::to_string(i);
            }
        }
    }
    ch.finish();
    return "";
}

/// A child process (fork).  The body runs in the child and returns "" on success; its verdict travels over a pipe.
struct Child {
    pid_t pid = -1;
    int rfd = -1;
};
Child spawn_child(const std::function<std::string()>& body) {
    int fds[2];
    if (::pipe(fds) != 0) throw std::runtime_error("pipe failed");
    std::cout.flush();
    std::cerr.flush();
    const pid_t pid = ::fork();
    if (pid < 0) throw std::runtime_error("fork failed");
    if (pid == 0) {
        ::close(fds[0]);
        std::string verdict;
        try { verdict = body(); }
        catch (const std::exception& e) { verdict = std::string("exception: ") + e.what(); }
        catch (...) { verdict = "non-std exception"; }
        const std::string line = verdict.empty() ? "OK" : "FAIL " + verdict;
        [[maybe_unused]] const auto rc = ::write(fds[1], line.data(), line.size());
        ::_exit(verdict.empty() ? 0 : 1);  // _exit: no atexit handlers, no flushing the parent's stdio copies
    }
    ::close(fds[1]);
    return {pid, fds[0]};
}
/// "" = the child finished in time and reported OK.  A child that hangs is killed.
std::string join_child(const Child& c) {
    int status = 0;
    const auto deadline = Clock::now() + std::chrono::milliseconds(CHILD_TIMEOUT_MS + 2000);
    bool timed_out = false;
    while (true) {
        const pid_t r = ::waitpid(c.pid, &status, WNOHANG);
        if (r == c.pid) break;
        if (r < 0 && errno != EINTR) { status = -1; break; }
        if (Clock::now() > deadline) { ::kill(c.pid, SIGKILL); ::waitpid(c.pid, &status, 0); timed_out = true; break; }
        std::this_thread::sleep_for(std::chrono::milliseconds(2));
    }
    char buf[512] = {};
    const auto got = ::read(c.rfd, buf, sizeof buf - 1);
    ::close(c.rfd);
    if (timed_out) return "child did not finish in time";
    const std::string out(buf, got > 0 ? static_cast<std::size_t>(got) : 0);
    if (!WIFEXITED(status)) return "child crashed (status " + std::to_string(status) + ") " + out;
    if (WEXITSTATUS(status) != 0 || out != "OK") return "child output: " + out;
    return "";
}
Clock::time_point child_deadline() { return Clock::now() + std::chrono::milliseconds(CHILD_TIMEOUT_MS); }
}  // namespace

TEST(two_mappings_of_one_file_share_data, "part4") {
    TempDir dir;
    const auto file = dir / "chan.bin";
    auto producer = SharedChannel::create(file, 1024);
    auto consumer = SharedChannel::open(file);
    CHECK_EQ(fs::file_size(file), MessageRing::segment_bytes(1024));
    CHECK_EQ(consumer.capacity(), 1024);
    CHECK(!consumer.receive());
    CHECK(producer.send(bytes_of("hello")));
    CHECK(producer.send(Bytes{}));
    CHECK_EQ(consumer.receive(), std::optional<Bytes>(bytes_of("hello")));
    CHECK_EQ(consumer.receive(), std::optional<Bytes>(Bytes{}));
    CHECK(!consumer.receive());
    CHECK(!consumer.is_drained());
    producer.finish();
    CHECK(consumer.is_drained());
}

TEST(full_channel_rejects_and_recovers, "part4,edge") {
    TempDir dir;
    auto a = SharedChannel::create(dir / "c", 64);
    auto b = SharedChannel::open(dir / "c");
    int sent = 0;
    while (a.send(Bytes(12))) ++sent;
    CHECK_EQ(sent, 4);
    CHECK(b.receive().has_value());
    CHECK(a.send(Bytes(12)));
}

TEST(backlog_survives_close_and_reopen, "part4,edge") {
    TempDir dir;
    const auto file = dir / "persist.bin";
    {
        auto p = SharedChannel::create(file, 4096);
        for (std::uint64_t i = 0; i < 20; ++i) CHECK(p.send(make_msg(i)));
    }  // the destructor unmaps; the data is in the file
    auto c = SharedChannel::open(file);
    for (std::uint64_t i = 0; i < 20; ++i) CHECK_EQ(check_msg(c.receive(), i), "");
    CHECK(!c.receive());
}

TEST(open_rejects_files_that_are_not_channels, "part4,edge") {
    TempDir dir;
    try {
        SharedChannel::open(dir / "missing");
        CHECK(false, "opening a missing file must throw");
    } catch (const std::system_error& e) {
        CHECK(e.code() == std::errc::no_such_file_or_directory, e.what());
    }
    write_file(dir / "tiny", Bytes(10));
    CHECK_THROWS_AS(SharedChannel::open(dir / "tiny"), StateError);
    write_file(dir / "zeros", Bytes(4096));
    CHECK_THROWS_AS(SharedChannel::open(dir / "zeros"), StateError);
    Bytes junk(4096);
    std::mt19937 rnd(0);
    for (auto& b : junk) b = static_cast<std::uint8_t>(rnd());
    write_file(dir / "noise", junk);
    CHECK_THROWS_AS(SharedChannel::open(dir / "noise"), StateError);
}

TEST(create_rejects_bad_capacity_without_touching_files_and_close_is_idempotent, "part4,edge") {
    TempDir dir;
    CHECK_THROWS_AS(SharedChannel::create(dir / "x", 100), std::invalid_argument);
    CHECK(!fs::exists(dir / "x"), "an illegal capacity must not leave a file behind");
    const auto existing = dir / "existing.bin";
    write_file(existing, Bytes{1, 2, 3});
    CHECK_THROWS_AS(SharedChannel::create(existing, 1000), std::invalid_argument);
    CHECK_EQ(read_file(existing), (Bytes{1, 2, 3}), "an illegal capacity must not truncate an existing file");
    auto ch = SharedChannel::create(dir / "y", 64);
    ch.close();
    ch.close();
    CHECK_THROWS_AS(ch.send(Bytes(1)), StateError);
    CHECK_THROWS_AS(ch.receive(), StateError);
    CHECK(fs::exists(dir / "y"), "close only unmaps, it does not delete the file");
}

TEST(channel_is_move_only_and_a_moved_from_channel_is_closed, "part4,cpp") {
    static_assert(!std::is_copy_constructible_v<SharedChannel>, "two owners of one mapping would unmap it twice");
    static_assert(std::is_nothrow_move_constructible_v<SharedChannel>);
    TempDir dir;
    auto a = SharedChannel::create(dir / "m", 64);
    SharedChannel b = std::move(a);
    CHECK_THROWS_AS(a.send(Bytes(1)), StateError);  // NOLINT(bugprone-use-after-move): the point of the test
    CHECK(b.send(Bytes(1)));
    SharedChannel c = SharedChannel::open(dir / "m");
    c = std::move(b);  // move-assignment unmaps what c held
    CHECK(c.receive().has_value());
}

TEST(child_process_consumes_what_the_parent_produces, "part4,io,conc") {
    TempDir dir;
    const auto file = dir / "p2c.bin";
    constexpr long long n = 100'000;
    auto ch = SharedChannel::create(file, 1 << 14);  // 16 KiB, far below the ~3 MB of traffic: wraps hundreds of times
    const auto child = spawn_child([&] {
        auto mine = SharedChannel::open(file);  // the child maps the file on its own
        return consume(mine, n, child_deadline());
    });
    const auto err = produce(ch, n, child_deadline());
    CHECK_EQ(err, "", "parent");
    CHECK_EQ(join_child(child), "");
}

TEST(parent_consumes_what_a_child_process_produces, "part4,io,conc") {
    TempDir dir;
    const auto file = dir / "c2p.bin";
    constexpr long long n = 100'000;
    auto ch = SharedChannel::create(file, 1 << 12);  // 4 KiB: even more wrap-arounds
    const auto child = spawn_child([&] {
        auto mine = SharedChannel::open(file);
        return produce(mine, n, child_deadline());
    });
    const auto err = consume(ch, n, child_deadline());
    CHECK_EQ(err, "", "parent");
    CHECK_EQ(join_child(child), "");
}

TEST(child_reads_the_backlog_a_parent_left_behind, "part4,io") {
    TempDir dir;
    const auto file = dir / "backlog.bin";
    constexpr long long n = 50;
    {
        auto ch = SharedChannel::create(file, 1 << 12);
        CHECK_EQ(produce(ch, n, Clock::now() + std::chrono::seconds(1)), "");
    }  // the parent has unmapped and holds no channel any more
    const auto child = spawn_child([&] {  // the child starts afterwards: the data can only come from the file
        auto mine = SharedChannel::open(file);
        return consume(mine, n, child_deadline());
    });
    CHECK_EQ(join_child(child), "");
}

TEST(a_dead_child_does_not_hang_the_parent, "part4,io,edge") {
    // The harness itself: a child that never finishes is killed, and its absence shows up as a failed check, not a stuck test.
    TempDir dir;
    auto ch = SharedChannel::create(dir / "z.bin", 64);
    const auto child = spawn_child([&]() -> std::string { ::_exit(7); });
    const auto verdict = join_child(child);
    CHECK_NE(verdict, "");
}

MT_MAIN()
