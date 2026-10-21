// hc13 · Fixed-size memory pool — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: FreeResult, StateError, Order, capacity check, handle packing helpers.  To write: everything marked TODO.
#pragma once

#include <atomic>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <memory>
#include <new>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

namespace pool {

/// Result of returning a block.  Not a bool: "you freed it twice" and "this was never mine" are different bugs.
///   Freed       success
///   DoubleFree  the block is not in use right now: already returned, or the handle is stale
///   Invalid     not issued by this pool at all: out of range, NONE, all-zero handle, a generation never issued
enum class FreeResult { Freed, DoubleFree, Invalid };

/// The pool's "illegal state" error (Java: IllegalStateException): stale handle, double free through freeOrThrow, closed pool.
struct StateError : std::logic_error {
    using std::logic_error::logic_error;
};

/// 24 bytes of payload per order (the arena adds an 8-byte header per slot: 32 bytes in total).
struct Order {
    long long id, px;
    int qty, side;
    friend bool operator==(const Order&, const Order&) = default;
};
inline constexpr Order kZeroOrder{0, 0, 0, 0};

inline constexpr int kMaxCapacity = 1 << 28;

inline void check_capacity(int capacity) {
    if (capacity < 1 || capacity > kMaxCapacity) throw std::invalid_argument("capacity: " + std::to_string(capacity));
}

// ============================================================================================ Part 1
/// Blocks are int ids 0..capacity-1.  allocate() hands out 0, 1, 2, ... first, then the most recently freed block (LIFO).
/// Pool exhausted -> NONE (not an exception).  free(): out of range (including negative) -> Invalid; not in use -> DoubleFree;
/// otherwise Freed.  All operations O(1): no scanning for a free block, and a double free must not put a block in the list twice.
/// Hints: ONE std::vector<std::uint32_t> holds the list links and the "in use" flag (a sentinel value); a negative int cast to
/// uint32_t becomes huge, so a single unsigned comparison rejects both ends of the range; the defaulted move constructor
/// leaves a moved-from pool with a stale head - make the moved-from object a valid EMPTY pool.
class IndexPool {
public:
    static constexpr int NONE = -1;
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    /// capacity outside [1, MAX_CAPACITY] -> std::invalid_argument.
    explicit IndexPool(int) { throw std::logic_error("TODO"); }
    int capacity() const { throw std::logic_error("TODO"); }
    int available() const { throw std::logic_error("TODO"); }
    int allocate() { throw std::logic_error("TODO"); }
    FreeResult free(int) { throw std::logic_error("TODO"); }
    bool is_allocated(int) const { throw std::logic_error("TODO"); }
    /// DoubleFree -> StateError, Invalid -> std::invalid_argument.
    void free_or_throw(int) { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 2
/// Generation-tagged handles: handle = generation << 32 | index, a std::uint64_t.  Every slot has a std::uint32_t generation,
/// all equal to initial_generation at the start; EVEN = free, ODD = in use; allocate and free each add 1.  A handle is valid
/// iff index < capacity && its generation is odd && it equals the slot's current generation.
/// free(): index out of range or even generation -> Invalid; odd but different from the slot's -> DoubleFree; else Freed.
/// Unsigned arithmetic wraps in a defined way (signed overflow would be undefined behaviour).
class GenPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit GenPool(int) { throw std::logic_error("TODO"); }
    /// initial_generation must be even, else std::invalid_argument.
    GenPool(int, std::uint32_t) { throw std::logic_error("TODO"); }

    static constexpr std::uint64_t handle(std::uint32_t index, std::uint32_t generation) noexcept {
        return (static_cast<std::uint64_t>(generation) << 32) | index;
    }
    static constexpr std::uint32_t index_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h); }
    static constexpr std::uint32_t generation_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h >> 32); }

    int capacity() const { throw std::logic_error("TODO"); }
    int available() const { throw std::logic_error("TODO"); }
    std::uint64_t allocate() { throw std::logic_error("TODO"); }
    FreeResult free(std::uint64_t) { throw std::logic_error("TODO"); }
    bool is_live(std::uint64_t) const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 3
/// One aligned arena (std::aligned_alloc, 64-byte alignment) with capacity records of 32 bytes (alignas(32)):
/// gen:uint32, next:uint32, id:int64, px:int64, qty:int32, side:int32.  Create the records in the raw bytes with placement
/// construction (std::uninitialized_value_construct_n); free the arena through a unique_ptr with a deleter calling std::free.
/// Handles and free() follow GenPool.  allocate() zeroes the payload.  put/get/px/qty on a stale or invalid handle -> StateError.
/// After close() (or after being moved from) every operation except capacity()/available()/byte_size() throws PoolClosed.
/// close() is idempotent and the destructor calls it.  Not copyable; movable.
struct PoolClosed : StateError {
    using StateError::StateError;
};

class ArenaOrderPool {
public:
    static constexpr int MAX_CAPACITY = kMaxCapacity;
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr std::size_t kAlignment = 64;

    explicit ArenaOrderPool(int) { throw std::logic_error("TODO"); }
    ArenaOrderPool(const ArenaOrderPool&) = delete;
    ArenaOrderPool& operator=(const ArenaOrderPool&) = delete;
    ArenaOrderPool(ArenaOrderPool&&) { throw std::logic_error("TODO"); }
    ArenaOrderPool& operator=(ArenaOrderPool&&) { throw std::logic_error("TODO"); }
    ~ArenaOrderPool() = default;

    int capacity() const { throw std::logic_error("TODO"); }
    int available() const { throw std::logic_error("TODO"); }
    /// capacity * 32 as size_t.
    std::size_t byte_size() const { throw std::logic_error("TODO"); }
    static constexpr std::size_t record_bytes() { return 32; }
    /// Address of the arena (0 when closed); lets tests check the alignment.
    std::uintptr_t base_address() const { throw std::logic_error("TODO"); }

    std::uint64_t allocate() { throw std::logic_error("TODO"); }
    FreeResult free(std::uint64_t) { throw std::logic_error("TODO"); }
    bool is_live(std::uint64_t) const { throw std::logic_error("TODO"); }
    /// Hot path: four stores, no object created.
    void put(std::uint64_t, long long, long long, int, int) { throw std::logic_error("TODO"); }
    void put(std::uint64_t, const Order&) { throw std::logic_error("TODO"); }
    long long px(std::uint64_t) const { throw std::logic_error("TODO"); }
    int qty(std::uint64_t) const { throw std::logic_error("TODO"); }
    /// Copy of the payload.
    Order get(std::uint64_t) const { throw std::logic_error("TODO"); }
    void close() noexcept {}
    bool closed() const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 4
/// Thread-safe pool, same handles as GenPool, same sequential behaviour (including LIFO).  Free list = Treiber stack:
/// ONE std::atomic<std::uint64_t> head (high 32 bits tag, +1 on every successful push/pop; low 32 bits top slot, 0xFFFFFFFF
/// = empty) updated with compare_exchange_weak; no mutex.  The next-links are std::atomic<std::uint32_t> (relaxed): a popper may read
/// next[i] while another thread re-pushes i, and a plain uint32_t would be a data race.  Choose explicit memory orders: acquire
/// when loading / popping the head, release when pushing, relaxed for the links.
/// free() flips the slot's generation g -> g + 1 with compare_exchange_strong BEFORE pushing: of two racing frees of the same handle
/// exactly one returns Freed, the other DoubleFree.  available() may be approximate while threads run, exact when they are quiet.
/// initial_tag lets a test start the tag near 2^32 to exercise its wrap-around.
class ConcurrentPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit ConcurrentPool(int, std::uint32_t = 0) { throw std::logic_error("TODO"); }
    int capacity() const { throw std::logic_error("TODO"); }
    int available() const { throw std::logic_error("TODO"); }
    static bool head_is_lock_free() { return std::atomic<std::uint64_t>::is_always_lock_free; }
    std::uint64_t allocate() { throw std::logic_error("TODO"); }
    FreeResult free(std::uint64_t) { throw std::logic_error("TODO"); }
    bool is_live(std::uint64_t) const { throw std::logic_error("TODO"); }
};

}  // namespace pool
