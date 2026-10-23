// hc13 · Fixed-size memory pool — C++20 tests.  Same cases as test/IndexPoolTest.java, GenPoolTest.java,
// OffHeapOrderPoolTest.java (here: ArenaOrderPool) and ConcurrentPoolTest.java plus C++-only edge cases (tag "cpp"):
// moved-from objects, deep copies, defined unsigned wrap-around, no sign extension in the packed handle, arena and record
// alignment, aligned_alloc size rounding, closed/moved-from arenas, lock-free atomics, a wrapping ABA tag under contention.
#include <algorithm>
#include <atomic>
#include <climits>
#include <cstring>
#include <future>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <thread>
#include <type_traits>

#include "minitest.hpp"

#include IMPL_HEADER

using namespace pool;

namespace pool {
std::ostream& operator<<(std::ostream& os, FreeResult r) {
    return os << (r == FreeResult::Freed ? "Freed" : r == FreeResult::DoubleFree ? "DoubleFree" : "Invalid");
}
std::ostream& operator<<(std::ostream& os, const Order& o) { return os << "Order{" << o.id << "," << o.px << "," << o.qty << "," << o.side << "}"; }
}  // namespace pool

namespace {
constexpr FreeResult FREED = FreeResult::Freed, DOUBLE_FREE = FreeResult::DoubleFree, INVALID = FreeResult::Invalid;

std::uint64_t H(std::uint32_t index, std::uint32_t generation) { return GenPool::handle(index, generation); }
}  // namespace

// ================================================ Part 1: IndexPool

TEST(allocates_ascending_then_reports_exhaustion, "part1") {
    IndexPool p(3);
    CHECK_EQ(p.capacity(), 3);
    CHECK_EQ(p.allocate(), 0);
    CHECK_EQ(p.allocate(), 1);
    CHECK_EQ(p.allocate(), 2);
    CHECK_EQ(p.available(), 0);
    CHECK_EQ(p.allocate(), IndexPool::NONE);
    CHECK_EQ(p.allocate(), IndexPool::NONE);  // asking again does no harm
}

TEST(reuses_most_recently_freed_first, "part1") {
    IndexPool p(4);
    for (int i = 0; i < 4; ++i) p.allocate();
    CHECK_EQ(p.free(1), FREED);
    CHECK_EQ(p.free(3), FREED);
    CHECK_EQ(p.allocate(), 3);  // LIFO
    CHECK_EQ(p.allocate(), 1);
    CHECK_EQ(p.allocate(), IndexPool::NONE);
}

TEST(detects_double_free, "part1,edge") {
    IndexPool p(2);
    const int a = p.allocate();
    CHECK_EQ(p.free(a), FREED);
    CHECK_EQ(p.free(a), DOUBLE_FREE);
    CHECK_EQ(p.available(), 2);  // a repeated free must not push available above capacity
    CHECK_EQ(p.free(1), DOUBLE_FREE);  // never allocated = not in use either
    CHECK_EQ(p.available(), 2);
}

TEST(detects_invalid_blocks, "part1,edge") {
    for (int bad : {-1, -2, 4, 5, INT_MAX, INT_MIN}) {
        IndexPool p(4);
        for (int i = 0; i < 4; ++i) p.allocate();
        CHECK_EQ(p.free(bad), INVALID, "block " + std::to_string(bad));
        CHECK_EQ(p.available(), 0);
        CHECK(!p.is_allocated(bad));
    }
}

TEST(double_free_does_not_corrupt_the_free_list, "part1,edge") {
    // The classic bug: freeing twice links the block into the list twice, and two callers later get the same block.
    IndexPool p(3);
    const int a = p.allocate(), b = p.allocate(), c = p.allocate();
    p.free(b);
    p.free(b);
    p.free(b);
    std::set<int> seen;
    for (int i = 0; i < 5; ++i) {
        const int x = p.allocate();
        if (x != IndexPool::NONE) CHECK(seen.insert(x).second, "handed out twice: " + std::to_string(x));
    }
    CHECK_EQ(seen.size(), 1u);
    CHECK(seen.count(b) == 1);
    CHECK_NE(a, c);
}

TEST(rejects_bad_capacity, "part1,edge") {
    for (int cap : {0, -1, INT_MIN, (1 << 28) + 1, INT_MAX}) CHECK_THROWS_AS(IndexPool(cap), std::invalid_argument, "cap " + std::to_string(cap));
}

TEST(capacity_one, "part1,edge") {
    IndexPool p(1);
    CHECK_EQ(p.allocate(), 0);
    CHECK_EQ(p.allocate(), IndexPool::NONE);
    CHECK_EQ(p.free(0), FREED);
    CHECK_EQ(p.allocate(), 0);
}

TEST(is_allocated_tracks_state, "part1") {
    IndexPool p(2);
    CHECK(!p.is_allocated(0));
    const int a = p.allocate();
    CHECK(p.is_allocated(a));
    p.free(a);
    CHECK(!p.is_allocated(a));
}

TEST(free_or_throw_maps_results_to_exceptions, "part1") {
    IndexPool p(2);
    const int a = p.allocate();
    CHECK_NOTHROW(p.free_or_throw(a));
    CHECK_THROWS_AS(p.free_or_throw(a), StateError);
    CHECK_THROWS_AS(p.free_or_throw(99), std::invalid_argument);
}

TEST(a_stale_index_cannot_be_told_apart_from_the_new_owner, "part1,edge") {
    // This test RECORDS the limit of Part 1; it does not ask the implementation to fix it.  An index has no identity: after a
    // frees the block and b gets it, a's old copy of the index frees b's block.  Part 2's generations close this hole.
    IndexPool p(1);
    const int a = p.allocate();
    p.free(a);
    const int b = p.allocate();
    CHECK_EQ(a, b);
    CHECK_EQ(p.free(a), FREED);
    CHECK(!p.is_allocated(b));
}

TEST(every_block_is_handed_out_exactly_once_after_churn, "part1") {
    std::mt19937 rnd(0);
    IndexPool p(100);
    std::vector<int> held;
    for (int step = 0; step < 10'000; ++step) {
        if (rnd() % 2 == 0 && !held.empty()) {
            const std::size_t k = rnd() % held.size();
            CHECK_EQ(p.free(held[k]), FREED);
            held.erase(held.begin() + static_cast<std::ptrdiff_t>(k));
        } else {
            const int x = p.allocate();
            if (x != IndexPool::NONE) held.push_back(x);
        }
    }
    for (int x : std::vector<int>(held)) p.free(x);
    std::set<int> seen;
    for (int i = 0; i < 100; ++i) {
        const int x = p.allocate();
        CHECK_NE(x, IndexPool::NONE);
        CHECK(seen.insert(x).second);
    }
    CHECK_EQ(p.allocate(), IndexPool::NONE);
}

TEST(near_full_churn_is_fast, "part1,perf") {
    // The pool is almost always full and every step replaces a random block: a free-block SCAN would cost n/2 per step.
    const int cap = 1 << 16;
    std::mt19937 rnd(0);
    IndexPool p(cap);
    std::vector<int> held(static_cast<std::size_t>(cap));
    for (auto& h : held) h = p.allocate();
    CHECK_EQ(p.allocate(), IndexPool::NONE);
    CHECK_WITHIN_MS(2000, {
        for (int step = 0; step < 1'500'000; ++step) {
            const std::size_t k = rnd() % held.size();
            REQUIRE_EQ(p.free(held[k]), FREED);
            const int b = p.allocate();
            REQUIRE(b != IndexPool::NONE);
            held[k] = b;
        }
    });
    CHECK_EQ(p.available(), 0);
    std::vector<bool> seen(static_cast<std::size_t>(cap));
    for (int b : held) { CHECK(!seen[static_cast<std::size_t>(b)]); seen[static_cast<std::size_t>(b)] = true; }
}

TEST(random_ops_match_a_model_and_are_fast, "part1,perf") {
    const int cap = 1 << 16;
    std::mt19937 rnd(0);
    IndexPool p(cap);
    std::vector<bool> live(static_cast<std::size_t>(cap));
    std::vector<int> stack;
    CHECK_WITHIN_MS(2000, {
        for (int step = 0; step < 3'000'000; ++step) {
            if (!stack.empty() && (stack.size() == static_cast<std::size_t>(cap) || rnd() % 2 == 0)) {
                const std::size_t k = rnd() % stack.size();
                const int b = stack[k];
                stack[k] = stack.back();
                stack.pop_back();
                live[static_cast<std::size_t>(b)] = false;
                REQUIRE_EQ(p.free(b), FREED);
            } else {
                const int b = p.allocate();
                REQUIRE(b != IndexPool::NONE);
                REQUIRE(!live[static_cast<std::size_t>(b)]);
                live[static_cast<std::size_t>(b)] = true;
                stack.push_back(b);
            }
        }
    });
    CHECK_EQ(p.available(), cap - static_cast<int>(stack.size()));
}

// ---- C++-only Part 1

TEST(a_moved_from_pool_is_a_valid_empty_pool, "part1,edge,cpp") {
    IndexPool a(4);
    a.allocate();
    IndexPool b = std::move(a);
    CHECK_EQ(b.capacity(), 4);
    CHECK_EQ(b.available(), 3);
    // With the compiler-generated move, a.head_ would still point at a block of a vector that is now empty: allocate() reads
    // next_[head_] out of bounds.  A moved-from pool must simply be empty.
    CHECK_EQ(a.capacity(), 0);
    CHECK_EQ(a.available(), 0);
    CHECK_EQ(a.allocate(), IndexPool::NONE);
    CHECK_EQ(a.free(0), INVALID);
    CHECK(!a.is_allocated(0));
    IndexPool c(2);
    c = std::move(b);  // move assignment: same story
    CHECK_EQ(c.capacity(), 4);
    CHECK_EQ(b.allocate(), IndexPool::NONE);
    CHECK_EQ(b.capacity(), 0);
}

TEST(copy_is_deep_and_independent, "part1,edge,cpp") {
    IndexPool a(3);
    const int x = a.allocate();
    IndexPool b = a;
    CHECK_EQ(b.free(x), FREED);
    CHECK(a.is_allocated(x));  // freeing in the copy does not free in the original
    CHECK_EQ(a.available(), 2);
    CHECK_EQ(b.available(), 3);
    CHECK_EQ(a.allocate(), 1);
    CHECK_EQ(b.allocate(), x);  // b has x on top of its list, a does not
}

TEST(index_conversions_are_exact_at_the_extremes, "part1,edge,cpp") {
    // free(int) takes a signed int; the pool compares it as unsigned.  -1 -> 0xFFFFFFFF must not alias the end-of-list marker.
    IndexPool p(2);
    p.allocate();
    p.allocate();
    CHECK_EQ(p.free(-1), INVALID);
    CHECK_EQ(p.free(static_cast<int>(0xFFFFFFFEu)), INVALID);  // == -2, the "allocated" sentinel as an int
    CHECK_EQ(p.available(), 0);
    CHECK_EQ(p.allocate(), IndexPool::NONE);
}

// ================================================ Part 2: GenPool

TEST(handle_packing_round_trips, "part2") {
    const std::uint64_t h = H(5, 7);
    CHECK_EQ(GenPool::index_of(h), 5u);
    CHECK_EQ(GenPool::generation_of(h), 7u);
    CHECK_EQ(h, (std::uint64_t{7} << 32) | 5u);
    const std::uint64_t h2 = H(INT_MAX, 0xFFFFFFFFu);  // generation with its top bit set, index at int max
    CHECK_EQ(GenPool::index_of(h2), static_cast<std::uint32_t>(INT_MAX));
    CHECK_EQ(GenPool::generation_of(h2), 0xFFFFFFFFu);
    const std::uint64_t h3 = H(0, 0x80000000u);
    CHECK_EQ(GenPool::index_of(h3), 0u);
    CHECK_EQ(GenPool::generation_of(h3), 0x80000000u);
}

TEST(first_handles_are_generation_one_ascending_index, "part2") {
    GenPool p(3);
    CHECK_EQ(p.allocate(), H(0, 1));
    CHECK_EQ(p.allocate(), H(1, 1));
    CHECK_EQ(p.allocate(), H(2, 1));
    CHECK_EQ(p.allocate(), GenPool::NONE);
    CHECK_EQ(p.available(), 0);
}

TEST(free_then_allocate_bumps_the_generation_by_two, "part2") {
    GenPool p(1);
    const auto a = p.allocate();
    CHECK_EQ(p.free(a), FREED);
    const auto b = p.allocate();
    CHECK_EQ(GenPool::index_of(a), GenPool::index_of(b));
    CHECK_EQ(GenPool::generation_of(a) + 2, GenPool::generation_of(b));
    CHECK_NE(a, b);
}

TEST(use_after_free_is_detected, "part2,edge") {
    GenPool p(2);
    const auto a = p.allocate();
    CHECK(p.is_live(a));
    p.free(a);
    CHECK(!p.is_live(a));
    CHECK_EQ(p.free(a), DOUBLE_FREE);
    CHECK_EQ(p.available(), 2);
}

TEST(a_stale_handle_of_a_reused_slot_is_rejected, "part2,edge") {
    // Same story as the IndexPool test that documents the hole; here the old handle cannot touch the new owner's block.
    GenPool p(1);
    const auto a = p.allocate();
    p.free(a);
    const auto b = p.allocate();
    CHECK_EQ(GenPool::index_of(a), GenPool::index_of(b));
    CHECK_EQ(p.free(a), DOUBLE_FREE);
    CHECK(p.is_live(b));
    CHECK(!p.is_live(a));
    CHECK_EQ(p.free(b), FREED);
}

TEST(invalid_handles, "part2,edge") {
    // all-zero, NONE, even generation (never issued), index out of range (including indexes whose top bit is set)
    const std::uint64_t bad[] = {0ull, ~0ull, 1ull, 0x0000'0002'0000'0000ull, 0x0000'0001'0000'0003ull, 0x0000'0001'FFFF'FFFFull,
                                 0x0000'0001'8000'0000ull, 0x8000'0000'0000'0000ull, 0x7FFF'FFFF'FFFF'FFFFull};
    GenPool p(3);
    p.allocate();
    for (std::uint64_t h : bad) {
        CHECK_EQ(p.free(h), INVALID, "handle " + std::to_string(h));
        CHECK(!p.is_live(h));
    }
    CHECK_EQ(p.available(), 2);
}

TEST(none_is_never_a_valid_handle, "part2,edge") {
    GenPool p(1);
    CHECK_EQ(p.free(GenPool::NONE), INVALID);
    const auto a = p.allocate();
    CHECK_NE(a, GenPool::NONE);
    CHECK(!p.is_live(GenPool::NONE));
}

TEST(generation_wraps_around_correctly, "part2,edge") {
    // Start at 2^32 - 2: the first allocation is 0xFFFFFFFF (odd), freeing wraps to 0 (even = free), the next allocation is 1.
    GenPool p(1, 0xFFFFFFFEu);
    const auto a = p.allocate();
    CHECK_EQ(GenPool::generation_of(a), 0xFFFFFFFFu);
    CHECK(p.is_live(a));
    CHECK_EQ(p.free(a), FREED);
    const auto b = p.allocate();
    CHECK_EQ(GenPool::generation_of(b), 1u);
    CHECK_EQ(p.free(a), DOUBLE_FREE);
    CHECK(p.is_live(b));
    CHECK_THROWS_AS(GenPool(1, 1), std::invalid_argument);
}

TEST(gen_pool_rejects_bad_capacity, "part2,edge") {
    for (int cap : {0, -1, (1 << 28) + 1}) CHECK_THROWS_AS(GenPool(cap), std::invalid_argument);
}

TEST(interleaved_lifetimes_stay_independent, "part2") {
    GenPool p(4);
    std::vector<std::uint64_t> hs;
    for (int i = 0; i < 4; ++i) hs.push_back(p.allocate());
    p.free(hs[1]);
    p.free(hs[2]);
    const auto x = p.allocate();
    CHECK_EQ(GenPool::index_of(hs[2]), GenPool::index_of(x));  // LIFO
    CHECK(p.is_live(hs[0]));
    CHECK(!p.is_live(hs[1]));
    CHECK(!p.is_live(hs[2]));
    CHECK(p.is_live(hs[3]));
    CHECK(p.is_live(x));
}

TEST(gen_near_full_churn_is_fast, "part2,perf") {
    const int cap = 1 << 16;
    std::mt19937 rnd(0);
    GenPool p(cap);
    std::vector<std::uint64_t> held(static_cast<std::size_t>(cap));
    for (auto& h : held) h = p.allocate();
    CHECK_EQ(p.allocate(), GenPool::NONE);
    CHECK_WITHIN_MS(2000, {
        for (int step = 0; step < 1'500'000; ++step) {
            const std::size_t k = rnd() % held.size();
            REQUIRE_EQ(p.free(held[k]), FREED);
            REQUIRE_EQ(p.free(held[k]), DOUBLE_FREE);
            const auto h = p.allocate();
            REQUIRE(h != GenPool::NONE);
            held[k] = h;
        }
    });
    CHECK_EQ(p.available(), 0);
}

TEST(gen_random_ops_against_a_model_are_fast, "part2,perf") {
    const int cap = 1 << 16;
    std::mt19937 rnd(0);
    GenPool p(cap);
    std::vector<std::uint64_t> held;
    std::uint64_t graveyard[1024] = {};
    std::size_t g = 0;
    CHECK_WITHIN_MS(2000, {
        for (int step = 0; step < 3'000'000; ++step) {
            if (!held.empty() && (held.size() == static_cast<std::size_t>(cap) || rnd() % 2 == 0)) {
                const std::size_t k = rnd() % held.size();
                const auto h = held[k];
                held[k] = held.back();
                held.pop_back();
                REQUIRE_EQ(p.free(h), FREED);
                graveyard[g++ & 1023] = h;
            } else {
                const auto h = p.allocate();
                REQUIRE(h != GenPool::NONE);
                held.push_back(h);
            }
            if ((step & 1023) == 0 && g > 0) {  // poke a dead handle now and then: it must be refused every time
                const auto dead = graveyard[rnd() % std::min<std::size_t>(g, 1024)];
                REQUIRE(!p.is_live(dead));
                REQUIRE_EQ(p.free(dead), DOUBLE_FREE);
            }
        }
    });
    CHECK_EQ(p.available(), cap - static_cast<int>(held.size()));
}

// ---- C++-only Part 2

TEST(packing_is_constexpr_and_has_no_sign_extension, "part2,edge,cpp") {
    static_assert(GenPool::handle(5, 7) == ((std::uint64_t{7} << 32) | 5u));
    static_assert(GenPool::generation_of(GenPool::handle(0xFFFFFFFFu, 0)) == 0, "an index with its top bit set must not smear into the generation");
    static_assert(GenPool::index_of(GenPool::handle(0, 0xFFFFFFFFu)) == 0);
    // The trap, for contrast: widening a SIGNED index sign-extends it.
    const int signed_index = -1;
    CHECK_EQ(static_cast<std::uint64_t>(signed_index) >> 32, 0xFFFFFFFFull);
    CHECK_EQ(GenPool::generation_of(GenPool::handle(static_cast<std::uint32_t>(signed_index), 0)), 0u);
}

TEST(wrapping_many_times_is_defined_behaviour, "part2,edge,cpp") {
    // 0xFFFFFFFC + 2 per cycle: wraps within a few cycles; with a signed 32-bit generation this would be undefined behaviour
    // (the sanitizer build aborts on it).
    GenPool p(1, 0xFFFFFFFCu);
    std::uint32_t last = 0;
    for (int i = 0; i < 8; ++i) {
        const auto h = p.allocate();
        REQUIRE(h != GenPool::NONE);
        CHECK_EQ(GenPool::generation_of(h) & 1u, 1u);
        CHECK_EQ(p.free(h), FREED);
        CHECK_EQ(p.free(h), DOUBLE_FREE);
        last = GenPool::generation_of(h);
    }
    CHECK_EQ(last, 0xFFFFFFFCu + 2u * 7u + 1u);  // unsigned arithmetic, wrapped
}

TEST(initial_generation_parity_is_checked_at_the_extremes, "part2,edge,cpp") {
    CHECK_NOTHROW(GenPool(2, 0xFFFFFFFEu));
    CHECK_THROWS_AS(GenPool(2, 0xFFFFFFFFu), std::invalid_argument);
    CHECK_NOTHROW(GenPool(2, 0u));
}

// ================================================ Part 3: ArenaOrderPool

TEST(put_get_round_trip, "part3") {
    ArenaOrderPool p(4);
    const auto h = p.allocate();
    const Order o{123'456'789'012LL, 18'950, 100, 1};
    p.put(h, o);
    CHECK_EQ(p.get(h), o);
    p.put(h, Order{1, 2, 3, 4});
    CHECK_EQ(p.get(h), (Order{1, 2, 3, 4}));
}

TEST(fieldwise_access_matches_whole_record_access, "part3") {
    ArenaOrderPool p(2);
    const auto h = p.allocate();
    p.put(h, 11LL, 22LL, 33, 1);
    CHECK_EQ(p.get(h), (Order{11, 22, 33, 1}));
    CHECK_EQ(p.px(h), 22LL);
    CHECK_EQ(p.qty(h), 33);
    p.put(h, Order{5, 6, 7, 0});
    CHECK_EQ(p.px(h), 6LL);
    CHECK_EQ(p.qty(h), 7);
    p.free(h);
    CHECK_THROWS_AS(p.px(h), StateError);
    CHECK_THROWS_AS(p.qty(h), StateError);
    CHECK_THROWS_AS(p.put(h, 1LL, 1LL, 1, 1), StateError);
}

TEST(extreme_values_survive_a_round_trip, "part3,edge") {
    ArenaOrderPool p(2);
    const auto h = p.allocate();
    const Order o{LLONG_MIN, LLONG_MAX, INT_MIN, INT_MAX};
    p.put(h, o);
    CHECK_EQ(p.get(h), o);
    const Order neg{-1, -1, -1, -1};
    p.put(h, neg);
    CHECK_EQ(p.get(h), neg);
}

TEST(neighbouring_records_do_not_overlap, "part3") {
    const int n = 1000;
    ArenaOrderPool p(n);
    std::vector<std::uint64_t> hs;
    for (int i = 0; i < n; ++i) {
        hs.push_back(p.allocate());
        p.put(hs.back(), Order{i, -i, i * 3, i % 2});
    }
    for (int i = 0; i < n; ++i) CHECK_EQ(p.get(hs[static_cast<std::size_t>(i)]), (Order{i, -i, i * 3, i % 2}), "slot " + std::to_string(i));
    CHECK_EQ(p.allocate(), ArenaOrderPool::NONE);
}

TEST(a_reused_record_is_zeroed, "part3,edge") {
    ArenaOrderPool p(1);
    const auto a = p.allocate();
    p.put(a, Order{7, 8, 9, 10});
    p.free(a);
    const auto b = p.allocate();
    CHECK_EQ(p.get(b), kZeroOrder);  // the previous owner's data must not leak
}

TEST(stale_and_invalid_handles_are_rejected, "part3,edge") {
    ArenaOrderPool p(2);
    const auto a = p.allocate();
    p.put(a, Order{1, 1, 1, 1});
    CHECK_EQ(p.free(a), FREED);
    CHECK_EQ(p.free(a), DOUBLE_FREE);
    CHECK_THROWS_AS(p.get(a), StateError);
    CHECK_THROWS_AS(p.put(a, kZeroOrder), StateError);
    const auto b = p.allocate();  // same slot, new generation
    p.put(b, Order{2, 2, 2, 2});
    CHECK_THROWS_AS(p.get(a), StateError);  // the old handle cannot read the new owner's data
    CHECK_EQ(p.free(a), DOUBLE_FREE);
    CHECK_EQ(p.get(b), (Order{2, 2, 2, 2}));
    for (std::uint64_t bad : {ArenaOrderPool::NONE, std::uint64_t{0}, std::uint64_t{1}, std::uint64_t{0x1'0000'0063}}) {
        CHECK_EQ(p.free(bad), INVALID);
        CHECK_THROWS_AS(p.get(bad), StateError);
    }
}

TEST(layout_is_one_contiguous_block_of_32_byte_records, "part3") {
    CHECK_EQ(ArenaOrderPool::record_bytes(), 32u);
    ArenaOrderPool p(1000);
    CHECK_EQ(p.byte_size(), 32'000u);
    CHECK_EQ(p.capacity(), 1000);
    CHECK_EQ(p.available(), 1000);
    p.allocate();
    CHECK_EQ(p.available(), 999);
}

TEST(close_is_idempotent_and_blocks_further_access, "part3,edge") {
    ArenaOrderPool p(2);
    const auto h = p.allocate();
    p.close();
    p.close();  // the second call is a no-op
    CHECK_THROWS_AS(p.get(h), PoolClosed);
    CHECK_THROWS_AS(p.allocate(), PoolClosed);
    CHECK(p.closed());
}

TEST(arena_rejects_bad_capacity, "part3,edge") {
    CHECK_THROWS_AS(ArenaOrderPool(0), std::invalid_argument);
    CHECK_THROWS_AS(ArenaOrderPool(-5), std::invalid_argument);
    CHECK_THROWS_AS(ArenaOrderPool((1 << 28) + 1), std::invalid_argument);
}

TEST(usable_from_another_thread_after_a_synchronised_hand_off, "part3") {
    ArenaOrderPool p(2);
    const auto h = p.allocate();
    p.put(h, Order{9, 9, 9, 9});
    // std::async's start synchronises-with the task body: the writes above are visible there (no concurrent access).
    const Order seen = std::async(std::launch::async, [&] { return p.get(h); }).get();
    CHECK_EQ(seen, (Order{9, 9, 9, 9}));
}

TEST(million_records_churn_in_under_two_seconds, "part3,perf") {
    const int cap = 1'000'000;
    std::mt19937 rnd(0);
    ArenaOrderPool p(cap);
    std::vector<std::uint64_t> hs(static_cast<std::size_t>(cap));
    CHECK_WITHIN_MS(2000, {
        for (int i = 0; i < cap; ++i) {
            hs[static_cast<std::size_t>(i)] = p.allocate();
            p.put(hs[static_cast<std::size_t>(i)], i, i * 2LL, i & 0xFFFF, i & 1);
        }
        CHECK_EQ(p.allocate(), ArenaOrderPool::NONE);
        long long sum = 0;
        for (int i = 0; i < cap; ++i) sum += p.px(hs[static_cast<std::size_t>(i)]);
        CHECK_EQ(sum, static_cast<long long>(cap) * (cap - 1));
        int freed = 0;
        for (int i = 0; i < 200'000; ++i) {
            const std::size_t k = rnd() % static_cast<unsigned>(cap);
            if (hs[k] != 0 && p.free(hs[k]) == FREED) { hs[k] = 0; ++freed; }
        }
        CHECK_EQ(p.available(), freed);
    });
}

// ---- C++-only Part 3

TEST(arena_and_records_are_aligned, "part3,edge,cpp") {
    ArenaOrderPool p(64);
    CHECK_EQ(p.base_address() % 64, 0u);  // starts on a cache-line boundary
    static_assert(ArenaOrderPool::kAlignment == 64);
    // 32-byte records at 32-byte alignment: two per 64-byte line, none straddling a line.
    static_assert(ArenaOrderPool::record_bytes() == 32);
    CHECK_EQ((p.base_address() + 5 * ArenaOrderPool::record_bytes()) % 32, 0u);
}

TEST(sizes_that_are_not_a_multiple_of_the_alignment_still_work, "part3,edge,cpp") {
    // std::aligned_alloc needs size % alignment == 0 (capacity 1 = 32 bytes, capacity 3 = 96 bytes): the pool rounds up.
    // AddressSanitizer flags a write past the end of the allocation if the rounding were wrong.
    for (int cap : {1, 3, 5, 7}) {
        ArenaOrderPool p(cap);
        std::vector<std::uint64_t> hs;
        for (int i = 0; i < cap; ++i) { hs.push_back(p.allocate()); p.put(hs.back(), Order{i, i, i, i}); }
        CHECK_EQ(p.allocate(), ArenaOrderPool::NONE);
        for (int i = 0; i < cap; ++i) CHECK_EQ(p.get(hs[static_cast<std::size_t>(i)]), (Order{i, i, i, i}));
        CHECK_EQ(p.byte_size(), static_cast<std::size_t>(cap) * 32);
    }
}

TEST(byte_size_is_size_t_not_int, "part3,edge,cpp") {
    ArenaOrderPool p(1);
    static_assert(std::is_same_v<decltype(p.byte_size()), std::size_t>);
    // capacity * 32 passes 2^31 at about 67 million records: a 32-bit product would overflow.
    CHECK_EQ(static_cast<std::size_t>(70'000'000) * ArenaOrderPool::record_bytes(), 2'240'000'000u);
}

TEST(a_moved_from_arena_is_closed_and_the_new_one_owns_the_memory, "part3,edge,cpp") {
    ArenaOrderPool a(8);
    const auto h = a.allocate();
    a.put(h, Order{4, 5, 6, 1});
    ArenaOrderPool b = std::move(a);
    CHECK(a.closed());
    CHECK_THROWS_AS(a.allocate(), PoolClosed);
    CHECK_EQ(b.get(h), (Order{4, 5, 6, 1}));  // handles issued before the move stay valid in the new owner
    ArenaOrderPool c(2);
    c = std::move(b);  // c's old arena is released, b's is adopted
    CHECK(b.closed());
    CHECK_EQ(c.get(h), (Order{4, 5, 6, 1}));
    CHECK_EQ(c.capacity(), 8);
    static_assert(!std::is_copy_constructible_v<ArenaOrderPool>);
    CHECK(std::is_nothrow_move_constructible_v<ArenaOrderPool>);
}

TEST(close_then_destroy_frees_the_arena_exactly_once, "part3,edge,cpp") {
    // AddressSanitizer reports a double free if close() and the destructor both release the memory.
    for (int i = 0; i < 100; ++i) {
        ArenaOrderPool p(16);
        p.allocate();
        if (i % 2 == 0) p.close();
    }
    CHECK(true);
}

TEST(get_returns_a_copy, "part3,edge,cpp") {
    ArenaOrderPool p(1);
    const auto h = p.allocate();
    p.put(h, Order{1, 2, 3, 4});
    Order copy = p.get(h);
    copy.px = 999;
    CHECK_EQ(copy.px, 999LL);
    CHECK_EQ(p.px(h), 2LL);
}

// ================================================ Part 4: ConcurrentPool

namespace {

/// After all threads are quiet: exactly `capacity` distinct slots can be allocated, one more is NONE, freeing them restores everything.
void assert_all_slots_recoverable(ConcurrentPool& p, int capacity) {
    CHECK_EQ(p.available(), capacity);
    std::set<std::uint32_t> seen;
    std::vector<std::uint64_t> hs;
    for (int i = 0; i < capacity; ++i) {
        const auto h = p.allocate();
        REQUIRE(h != ConcurrentPool::NONE, "lost a slot: only " + std::to_string(i) + " could be allocated");
        CHECK(seen.insert(GenPool::index_of(h)).second, "slot issued twice: " + std::to_string(GenPool::index_of(h)));
        hs.push_back(h);
    }
    CHECK_EQ(p.allocate(), ConcurrentPool::NONE);
    CHECK_EQ(p.available(), 0);
    for (auto h : hs) CHECK_EQ(p.free(h), FREED);
    CHECK_EQ(p.available(), capacity);
}

/// Threads start together on a flag and each runs body(thread_no).
template <class Body>
void run_threads(int count, Body body) {
    std::atomic<bool> go{false};
    mt::ThreadErrors errors;
    std::vector<std::thread> threads;
    for (int t = 0; t < count; ++t)
        threads.push_back(errors.spawn([&, t] {
            while (!go.load(std::memory_order_acquire)) std::this_thread::yield();
            body(t);
        }));
    go.store(true, std::memory_order_release);
    for (auto& th : threads) th.join();
    CHECK_NO_THREAD_ERRORS(errors);
}

/// Small pool + many threads allocate / use / free in a loop: no slot may ever have two owners at once.
int contention_violations(ConcurrentPool& pool, int capacity, int threads, int iterations) {
    std::vector<std::atomic<int>> owner(static_cast<std::size_t>(capacity));
    for (auto& o : owner) o.store(0);
    std::atomic<int> violations{0};
    run_threads(threads, [&](int t) {
        const int me = t + 1;
        for (int i = 0; i < iterations; ++i) {
            const auto h = pool.allocate();
            if (h == ConcurrentPool::NONE) { std::this_thread::yield(); continue; }
            auto& slot = owner[GenPool::index_of(h)];
            int expected = 0;
            if (!slot.compare_exchange_strong(expected, me)) violations.fetch_add(1);  // someone else already holds it
            if (!pool.is_live(h)) violations.fetch_add(1);
            expected = me;
            if (!slot.compare_exchange_strong(expected, 0)) violations.fetch_add(1);
            if (pool.free(h) != FREED) violations.fetch_add(1);
        }
    });
    return violations.load();
}

}  // namespace

TEST(sequential_semantics_match_gen_pool, "part4") {
    ConcurrentPool p(3);
    const auto a = p.allocate(), b = p.allocate(), c = p.allocate();
    CHECK_EQ(a, H(0, 1));
    CHECK_EQ(b, H(1, 1));
    CHECK_EQ(c, H(2, 1));
    CHECK_EQ(p.allocate(), ConcurrentPool::NONE);
    CHECK_EQ(p.available(), 0);
    CHECK_EQ(p.free(b), FREED);
    CHECK_EQ(p.free(b), DOUBLE_FREE);
    CHECK(!p.is_live(b));
    const auto b2 = p.allocate();  // LIFO: the slot just freed
    CHECK_EQ(GenPool::index_of(b2), 1u);
    CHECK_EQ(GenPool::generation_of(b2), 3u);
    CHECK_EQ(p.free(b), DOUBLE_FREE);  // the old handle cannot touch the new owner
    CHECK(p.is_live(b2));
    CHECK_EQ(p.free(0ull), INVALID);
    CHECK_EQ(p.free(ConcurrentPool::NONE), INVALID);
    CHECK_EQ(p.free(H(3, 1)), INVALID);
    CHECK_EQ(p.free(H(1, 4)), INVALID);
    CHECK_EQ(p.available(), 0);
}

TEST(concurrent_capacity_one_and_bad_capacity, "part4,edge") {
    ConcurrentPool p(1);
    const auto a = p.allocate();
    CHECK_EQ(p.allocate(), ConcurrentPool::NONE);
    CHECK_EQ(p.free(a), FREED);
    CHECK_NE(p.allocate(), ConcurrentPool::NONE);
    CHECK_THROWS_AS(ConcurrentPool(0), std::invalid_argument);
    CHECK_THROWS_AS(ConcurrentPool((1 << 28) + 1), std::invalid_argument);
}

TEST(exclusive_ownership_under_contention, "part4,conc") {
    for (int rep = 0; rep < 12; ++rep) {
        ConcurrentPool pool(3);
        CHECK_EQ(contention_violations(pool, 3, 8, 8000), 0, "rep " + std::to_string(rep));
        assert_all_slots_recoverable(pool, 3);
    }
}

TEST(racing_double_free_has_exactly_one_winner, "part4,conc") {
    for (int rep = 0; rep < 12; ++rep) {
        const int n = 2000;
        ConcurrentPool pool(n);
        std::vector<std::uint64_t> hs;
        for (int i = 0; i < n; ++i) hs.push_back(pool.allocate());
        std::atomic<int> wins{0}, doubles{0}, invalid{0};
        run_threads(3, [&](int) {
            for (auto h : hs) {
                switch (pool.free(h)) {
                    case FREED: wins.fetch_add(1); break;
                    case DOUBLE_FREE: doubles.fetch_add(1); break;
                    case INVALID: invalid.fetch_add(1); break;
                }
            }
        });
        CHECK_EQ(wins.load(), n, "each handle is freed exactly once");
        CHECK_EQ(doubles.load(), 2 * n);
        CHECK_EQ(invalid.load(), 0);
        CHECK_EQ(pool.available(), n);
        assert_all_slots_recoverable(pool, n);  // no slot entered the free list twice
    }
}

TEST(allocate_in_one_thread_free_in_another, "part4,conc") {
    for (int rep = 0; rep < 8; ++rep) {
        const int capacity = 64, producers = 3, consumers = 3, per_producer = 8000;
        ConcurrentPool pool(capacity);
        std::mutex m;
        std::queue<std::uint64_t> handoff;
        std::atomic<long long> produced{0}, freed{0};
        std::atomic<int> bad_frees{0};
        const long long total = static_cast<long long>(producers) * per_producer;
        run_threads(producers + consumers, [&](int t) {
            if (t < producers) {
                int done = 0;
                while (done < per_producer) {
                    const auto h = pool.allocate();
                    if (h == ConcurrentPool::NONE) { std::this_thread::yield(); continue; }
                    { std::lock_guard<std::mutex> g(m); handoff.push(h); }
                    ++done;
                    produced.fetch_add(1);
                }
            } else {
                while (freed.load() < total) {
                    std::uint64_t h;
                    {
                        std::lock_guard<std::mutex> g(m);
                        if (handoff.empty()) h = 0;
                        else { h = handoff.front(); handoff.pop(); }
                    }
                    if (h == 0) { std::this_thread::yield(); continue; }
                    if (pool.free(h) != FREED) bad_frees.fetch_add(1);
                    freed.fetch_add(1);
                }
            }
        });
        CHECK_EQ(produced.load(), total);
        CHECK_EQ(freed.load(), total);
        CHECK_EQ(bad_frees.load(), 0);
        assert_all_slots_recoverable(pool, capacity);
    }
}

TEST(many_short_lived_threads, "part4,conc") {
    // 400 threads in waves of 50, each doing a few allocate / free pairs (the C++ stand-in for "many virtual threads").
    const int capacity = 16;
    ConcurrentPool pool(capacity);
    std::vector<std::atomic<int>> owner(capacity);
    for (auto& o : owner) o.store(0);
    std::atomic<int> violations{0};
    for (int wave = 0; wave < 8; ++wave) {
        std::vector<std::jthread> threads;
        for (int t = 1; t <= 50; ++t)
            threads.emplace_back([&, me = wave * 50 + t] {
                for (int i = 0; i < 200; ++i) {
                    const auto h = pool.allocate();
                    if (h == ConcurrentPool::NONE) continue;
                    auto& slot = owner[GenPool::index_of(h)];
                    int expected = 0;
                    if (!slot.compare_exchange_strong(expected, me)) violations.fetch_add(1);
                    slot.store(0);
                    if (pool.free(h) != FREED) violations.fetch_add(1);
                }
            });
    }
    CHECK_EQ(violations.load(), 0);
    assert_all_slots_recoverable(pool, capacity);
}

TEST(four_threads_hammering_one_pool, "part4,perf") {
    ConcurrentPool pool(1024);
    std::atomic<int> bad{0};
    CHECK_WITHIN_MS(2000, {
        run_threads(4, [&](int) {
            std::uint64_t mine[16];
            for (int i = 0; i < 50'000; ++i) {
                int k = 0;
                for (; k < 16; ++k) {
                    const auto h = pool.allocate();
                    if (h == ConcurrentPool::NONE) break;
                    mine[k] = h;
                }
                for (int j = 0; j < k; ++j)
                    if (pool.free(mine[j]) != FREED) bad.fetch_add(1);
            }
        });
    });
    CHECK_EQ(bad.load(), 0);
    CHECK_EQ(pool.available(), 1024);
}

// ---- C++-only Part 4

TEST(the_tagged_head_is_a_lock_free_atomic, "part4,edge,cpp") {
    static_assert(std::atomic<std::uint64_t>::is_always_lock_free, "a 64-bit tagged head must not secretly take a lock");
    CHECK(ConcurrentPool::head_is_lock_free());
    std::atomic<std::uint64_t> probe{0};
    CHECK(probe.is_lock_free());
}

TEST(the_aba_tag_wraps_around_under_contention, "part4,conc,cpp") {
    // Start the 32-bit tag 16 steps before the wrap: the contention run below crosses 2^32 many times.  The tag arithmetic is
    // unsigned, so wrapping is defined and the CAS keeps working.
    for (int rep = 0; rep < 6; ++rep) {
        ConcurrentPool pool(3, 0xFFFFFFF0u);
        CHECK_EQ(contention_violations(pool, 3, 6, 6000), 0, "rep " + std::to_string(rep));
        assert_all_slots_recoverable(pool, 3);
    }
}

TEST(spurious_cas_failures_are_harmless_on_one_thread, "part4,edge,cpp") {
    // compare_exchange_weak may fail without a competitor; allocate / free loop until it works.  Do a lot of single-threaded rounds.
    ConcurrentPool pool(5);
    std::vector<std::uint64_t> hs;
    for (int round = 0; round < 20'000; ++round) {
        while (true) {
            const auto h = pool.allocate();
            if (h == ConcurrentPool::NONE) break;
            hs.push_back(h);
        }
        CHECK_EQ(hs.size(), 5u);
        for (auto it = hs.rbegin(); it != hs.rend(); ++it) REQUIRE_EQ(pool.free(*it), FREED);
        hs.clear();
    }
    CHECK_EQ(pool.available(), 5);
}

TEST(stale_handles_never_free_a_new_owner_even_across_threads, "part4,conc,cpp") {
    // One thread keeps a dead handle and frees it again and again while another cycles the same slot.
    ConcurrentPool pool(1);
    const auto dead = pool.allocate();
    pool.free(dead);
    std::atomic<bool> stop{false};
    std::atomic<int> victims{0};
    mt::ThreadErrors errors;
    std::thread cycler = errors.spawn([&] {
        for (int i = 0; i < 20'000; ++i) {
            const auto h = pool.allocate();
            if (h == ConcurrentPool::NONE) continue;
            if (!pool.is_live(h)) victims.fetch_add(1);  // someone freed our block from under us
            if (pool.free(h) != FREED) victims.fetch_add(1);
        }
        stop.store(true);
    });
    std::thread attacker = errors.spawn([&] {
        while (!stop.load()) pool.free(dead);
    });
    cycler.join();
    attacker.join();
    CHECK_NO_THREAD_ERRORS(errors);
    CHECK_EQ(victims.load(), 0);
    assert_all_slots_recoverable(pool, 1);
}

MT_MAIN()
