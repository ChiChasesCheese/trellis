// hc13 · Fixed-size memory pool — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 IndexPool (free list threaded through a std::vector<uint32_t>), 2 GenPool (generation-tagged uint64_t handles),
//        3 ArenaOrderPool (one aligned arena, 32-byte records, placement construction), 4 ConcurrentPool (Treiber stack,
//        std::atomic<uint64_t> tagged head, compare_exchange_weak with explicit memory orders).
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
/// Blocks are int ids 0..capacity-1.  The free list lives INSIDE one std::vector<uint32_t>:
///   next_[i] = the next free block after i   (i is free; end of list = kEnd)
///   next_[i] = kAllocated                    (i is in use)
/// One word per block is both the list link and the "in use" flag: a free block has no use for anything else, and a block in
/// use has no use for a link.  Initially next_[i] = i + 1, so blocks come out as 0, 1, 2, ...; free() pushes on the head,
/// so the most recently freed block is allocated next (LIFO: still warm in the cache).  All operations O(1).
class IndexPool {
public:
    static constexpr int NONE = -1;
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit IndexPool(int capacity) {
        check_capacity(capacity);
        const auto n = static_cast<std::uint32_t>(capacity);
        next_.resize(n);
        for (std::uint32_t i = 0; i + 1 < n; ++i) next_[i] = i + 1;
        next_[n - 1] = kEnd;
        head_ = 0;
        available_ = n;
    }
    IndexPool(const IndexPool&) = default;
    IndexPool& operator=(const IndexPool&) = default;
    /// A moved-from pool must be a valid EMPTY pool: the defaulted move would leave head_ pointing into a vector that is gone.
    IndexPool(IndexPool&& o) noexcept : next_(std::move(o.next_)), head_(o.head_), available_(o.available_) { o.reset_empty(); }
    IndexPool& operator=(IndexPool&& o) noexcept {
        if (this != &o) {
            next_ = std::move(o.next_);
            head_ = o.head_;
            available_ = o.available_;
            o.reset_empty();
        }
        return *this;
    }

    int capacity() const { return static_cast<int>(next_.size()); }
    int available() const { return static_cast<int>(available_); }

    /// A free block, or NONE when the pool is exhausted (a full pool is a normal state, not an error).
    int allocate() {
        const std::uint32_t block = head_;
        if (block == kEnd) return NONE;
        head_ = next_[block];
        next_[block] = kAllocated;
        --available_;
        return static_cast<int>(block);
    }

    FreeResult free(int block) {
        // One unsigned comparison covers both "negative" and "too large": -1 becomes 0xFFFFFFFF.
        const auto b = static_cast<std::uint32_t>(block);
        if (b >= next_.size()) return FreeResult::Invalid;
        if (next_[b] != kAllocated) return FreeResult::DoubleFree;
        next_[b] = head_;
        head_ = b;
        ++available_;
        return FreeResult::Freed;
    }

    bool is_allocated(int block) const {
        const auto b = static_cast<std::uint32_t>(block);
        return b < next_.size() && next_[b] == kAllocated;
    }

    /// Like free(), but failure throws: double free -> StateError, invalid block -> std::invalid_argument.
    void free_or_throw(int block) {
        switch (free(block)) {
            case FreeResult::Freed: return;
            case FreeResult::DoubleFree: throw StateError("block not allocated (double free?): " + std::to_string(block));
            case FreeResult::Invalid: throw std::invalid_argument("block out of range: " + std::to_string(block));
        }
    }

private:
    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;
    static constexpr std::uint32_t kAllocated = 0xFFFFFFFEu;  // no valid index can be this large (capacity <= 2^28)

    void reset_empty() noexcept {
        next_.clear();
        head_ = kEnd;
        available_ = 0;
    }

    std::vector<std::uint32_t> next_;
    std::uint32_t head_ = kEnd;
    std::uint32_t available_ = 0;
};

// ============================================================================================ Part 2
/// Handles carry a generation, so a stale handle is recognised even after its slot has been handed to someone else.
///   handle = generation << 32 | index          (a std::uint64_t)
///   gens_[i] even = slot free, odd = slot in use; allocate and free each add 1
/// Valid <=> index < capacity && generation odd && generation == gens_[index].
/// Unsigned 32-bit generations wrap around in a DEFINED way (a signed int would be undefined behaviour); 2^32 is even, so the
/// parity rule survives the wrap.
class GenPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit GenPool(int capacity) : GenPool(capacity, 0u) {}
    /// initial_generation must be even (every slot starts free); tests use it to start close to the 32-bit wrap.
    GenPool(int capacity, std::uint32_t initial_generation) {
        check_capacity(capacity);
        if ((initial_generation & 1u) != 0) throw std::invalid_argument("initial_generation must be even");
        const auto n = static_cast<std::uint32_t>(capacity);
        gens_.assign(n, initial_generation);
        next_.resize(n);
        for (std::uint32_t i = 0; i + 1 < n; ++i) next_[i] = i + 1;
        next_[n - 1] = kEnd;
        head_ = 0;
        available_ = n;
    }

    /// Pack.  Both inputs are already unsigned 32-bit, so there is no sign extension to undo (with a signed int index,
    /// (uint64_t)index would smear 1-bits over the generation).
    static constexpr std::uint64_t handle(std::uint32_t index, std::uint32_t generation) noexcept {
        return (static_cast<std::uint64_t>(generation) << 32) | index;
    }
    static constexpr std::uint32_t index_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h); }
    static constexpr std::uint32_t generation_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h >> 32); }

    int capacity() const { return static_cast<int>(gens_.size()); }
    int available() const { return static_cast<int>(available_); }

    std::uint64_t allocate() {
        const std::uint32_t index = head_;
        if (index == kEnd) return NONE;
        head_ = next_[index];
        const std::uint32_t g = ++gens_[index];  // even -> odd
        --available_;
        return handle(index, g);
    }

    FreeResult free(std::uint64_t h) {
        const std::uint32_t index = index_of(h), g = generation_of(h);
        if (index >= gens_.size() || (g & 1u) == 0) return FreeResult::Invalid;
        if (gens_[index] != g) return FreeResult::DoubleFree;
        gens_[index] = g + 1;  // odd -> even
        next_[index] = head_;
        head_ = index;
        ++available_;
        return FreeResult::Freed;
    }

    bool is_live(std::uint64_t h) const {
        const std::uint32_t index = index_of(h), g = generation_of(h);
        return index < gens_.size() && (g & 1u) == 1 && gens_[index] == g;
    }

private:
    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;
    std::vector<std::uint32_t> gens_, next_;
    std::uint32_t head_ = kEnd;
    std::uint32_t available_ = 0;
};

// ============================================================================================ Part 3
/// The pool owns ONE aligned allocation (the "arena") holding capacity records of 32 bytes:
///     offset  0  gen   uint32   even free / odd in use (as in GenPool)
///     offset  4  next  uint32   free-list link (meaningful while free)
///     offset  8  id    int64  \.
///     offset 16  px    int64   | the Order payload (zeroed on allocate)
///     offset 24  qty   int32   |
///     offset 28  side  int32  /
/// The arena starts on a 64-byte boundary and a record is 32 bytes with 32-byte alignment, so no record straddles two cache
/// lines and two records fill exactly one.  std::aligned_alloc gives raw bytes; the records are then created in them with
/// std::uninitialized_value_construct_n (placement construction, which also zeroes them) so the objects really exist.
/// Not thread-safe; it may be handed to another thread when the hand-off itself is synchronised.
struct PoolClosed : StateError {
    using StateError::StateError;
};

class ArenaOrderPool {
public:
    static constexpr int MAX_CAPACITY = kMaxCapacity;
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr std::size_t kAlignment = 64;

    explicit ArenaOrderPool(int capacity) {
        check_capacity(capacity);
        capacity_ = static_cast<std::uint32_t>(capacity);
        bytes_ = static_cast<std::size_t>(capacity_) * sizeof(Slot);
        // std::aligned_alloc requires the size to be a multiple of the alignment.
        const std::size_t rounded = (bytes_ + kAlignment - 1) / kAlignment * kAlignment;
        void* raw = std::aligned_alloc(kAlignment, rounded);
        if (raw == nullptr) throw std::bad_alloc();
        arena_.reset(raw);  // from here on the unique_ptr frees it, whatever happens below
        slots_ = static_cast<Slot*>(raw);
        std::uninitialized_value_construct_n(slots_, capacity_);
        for (std::uint32_t i = 0; i < capacity_; ++i) slots_[i].next = i + 1 < capacity_ ? i + 1 : kEnd;
        head_ = 0;
        available_ = capacity_;
    }
    ArenaOrderPool(const ArenaOrderPool&) = delete;
    ArenaOrderPool& operator=(const ArenaOrderPool&) = delete;
    /// A moved-from pool is closed: every operation that needs the arena throws PoolClosed.
    ArenaOrderPool(ArenaOrderPool&& o) noexcept
        : arena_(std::move(o.arena_)), slots_(std::exchange(o.slots_, nullptr)), capacity_(std::exchange(o.capacity_, 0)),
          bytes_(std::exchange(o.bytes_, 0)), head_(o.head_), available_(std::exchange(o.available_, 0)) {}
    ArenaOrderPool& operator=(ArenaOrderPool&& o) noexcept {
        if (this != &o) {
            arena_ = std::move(o.arena_);
            slots_ = std::exchange(o.slots_, nullptr);
            capacity_ = std::exchange(o.capacity_, 0);
            bytes_ = std::exchange(o.bytes_, 0);
            head_ = o.head_;
            available_ = std::exchange(o.available_, 0);
        }
        return *this;
    }
    ~ArenaOrderPool() { close(); }

    int capacity() const { return static_cast<int>(capacity_); }
    int available() const { return static_cast<int>(available_); }
    /// Bytes in use by records (size_t: capacity * 32 can exceed 2^31).
    std::size_t byte_size() const { return bytes_; }
    static constexpr std::size_t record_bytes() { return sizeof(Slot); }
    /// Address of the arena (for alignment checks); 0 when closed.
    std::uintptr_t base_address() const { return reinterpret_cast<std::uintptr_t>(slots_); }

    std::uint64_t allocate() {
        require_open();
        const std::uint32_t index = head_;
        if (index == kEnd) return NONE;
        Slot& s = slots_[index];
        head_ = s.next;
        ++s.gen;  // even -> odd
        s.id = 0;  // the previous owner's data must not leak to the next one
        s.px = 0;
        s.qty = 0;
        s.side = 0;
        --available_;
        return handle(index, s.gen);
    }

    FreeResult free(std::uint64_t h) {
        require_open();
        const std::uint32_t index = index_of(h), g = generation_of(h);
        if (index >= capacity_ || (g & 1u) == 0) return FreeResult::Invalid;
        Slot& s = slots_[index];
        if (s.gen != g) return FreeResult::DoubleFree;
        s.gen = g + 1;  // odd -> even
        s.next = head_;
        head_ = index;
        ++available_;
        return FreeResult::Freed;
    }

    bool is_live(std::uint64_t h) const {
        require_open();
        const std::uint32_t index = index_of(h), g = generation_of(h);
        return index < capacity_ && (g & 1u) == 1 && slots_[index].gen == g;
    }

    /// Hot-path write: four stores, no object is created.
    void put(std::uint64_t h, long long id, long long px, int qty, int side) {
        Slot& s = live_slot(h);
        s.id = id;
        s.px = px;
        s.qty = qty;
        s.side = side;
    }
    void put(std::uint64_t h, const Order& o) { put(h, o.id, o.px, o.qty, o.side); }

    /// Zero-copy reads of one field.
    long long px(std::uint64_t h) const { return live_slot(h).px; }
    int qty(std::uint64_t h) const { return live_slot(h).qty; }
    /// Convenience copy of the whole payload (not for the hot path).
    Order get(std::uint64_t h) const {
        const Slot& s = live_slot(h);
        return Order{s.id, s.px, s.qty, s.side};
    }

    /// Release the arena now.  Idempotent; the destructor calls it too.
    void close() noexcept {
        arena_.reset();
        slots_ = nullptr;
        available_ = 0;
    }
    bool closed() const { return slots_ == nullptr; }

    static constexpr std::uint64_t handle(std::uint32_t index, std::uint32_t generation) noexcept { return GenPool::handle(index, generation); }
    static constexpr std::uint32_t index_of(std::uint64_t h) noexcept { return GenPool::index_of(h); }
    static constexpr std::uint32_t generation_of(std::uint64_t h) noexcept { return GenPool::generation_of(h); }

private:
    struct alignas(32) Slot {
        std::uint32_t gen;
        std::uint32_t next;
        long long id;
        long long px;
        int qty;
        int side;
    };
    static_assert(sizeof(Slot) == 32 && alignof(Slot) == 32, "two records per 64-byte cache line, none straddling");
    static_assert(offsetof(Slot, id) == 8 && offsetof(Slot, px) == 16 && offsetof(Slot, qty) == 24 && offsetof(Slot, side) == 28);
    static_assert(std::is_trivially_copyable_v<Slot> && std::is_trivially_destructible_v<Slot>, "the arena is freed without running destructors");

    struct FreeDeleter {
        void operator()(void* p) const noexcept { std::free(p); }
    };

    static constexpr std::uint32_t kEnd = 0xFFFFFFFFu;

    void require_open() const {
        if (slots_ == nullptr) throw PoolClosed("pool is closed");
    }
    Slot& live_slot(std::uint64_t h) {
        require_open();
        const std::uint32_t index = index_of(h), g = generation_of(h);
        if (index >= capacity_ || (g & 1u) == 0 || slots_[index].gen != g) throw StateError("stale or invalid handle: " + std::to_string(h));
        return slots_[index];
    }
    const Slot& live_slot(std::uint64_t h) const { return const_cast<ArenaOrderPool*>(this)->live_slot(h); }

    std::unique_ptr<void, FreeDeleter> arena_;
    Slot* slots_ = nullptr;
    std::uint32_t capacity_ = 0;
    std::size_t bytes_ = 0;
    std::uint32_t head_ = kEnd;
    std::uint32_t available_ = 0;
};

// ============================================================================================ Part 4
/// Thread-safe pool: any thread may allocate, any thread may free.  The free list is a Treiber stack.
///
///   head_  one std::atomic<uint64_t>:  high 32 bits = tag (+1 on every successful push/pop), low 32 bits = top slot (kEmpty = none)
///   next_  next_[i] = the slot below i; std::atomic<uint32_t> too, because a popper may read next_[i] while another thread is
///          re-pushing i: with a plain uint32_t that is a data race (undefined behaviour)
///
///   push(i):  loop { h = head; next[i] = idx(h);            CAS(head, h -> (tag(h)+1, i)) }
///   pop():    loop { h = head; i = idx(h); n = next[i];     CAS(head, h -> (tag(h)+1, n)) }
///
/// Why the tag (ABA): thread A reads head = X, next[X] = Y and is suspended.  B pops X, pops Y, pushes X back.  head is X again, so
/// A's CAS(X -> Y) succeeds, but Y is in use by B: the free list now hands out Y a second time.  With the tag, B's three operations
/// moved head from (t, X) to (t+3, X) and A's CAS fails.
///
/// Handles follow GenPool.  free() first flips the slot's generation from odd g to g + 1 with a CAS: when two threads free the same
/// handle exactly one CAS wins (Freed), the other sees the generation moved (DoubleFree), and the slot enters the list once.
///
/// Memory orders:
///   * head_ load + CAS on pop: acquire.  It pairs with the release CAS of the push that made the slot visible, so the pusher's
///     store to next_[i] happens-before the popper's read of it.  (Later pops are read-modify-writes in the release sequence.)
///   * head_ CAS on push: release (publishes next_[i]); failure order relaxed, the loop just retries with the fresh value.
///   * next_ accesses: relaxed.  A stale value is harmless: if next_[i] changed, head_'s tag changed too and the CAS fails.
///   * gens_: the popper owns the slot exclusively, so it stores the new generation with release (readers acquire in is_live);
///     free's CAS is acq_rel.
class ConcurrentPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};
    static constexpr int MAX_CAPACITY = kMaxCapacity;

    explicit ConcurrentPool(int capacity, std::uint32_t initial_tag = 0) : gens_(checked(capacity)), next_(gens_.size()) {
        const auto n = static_cast<std::uint32_t>(capacity);
        for (std::uint32_t i = 0; i < n; ++i) {
            gens_[i].store(0, std::memory_order_relaxed);
            next_[i].store(i + 1 < n ? i + 1 : kEmpty, std::memory_order_relaxed);
        }
        head_.store(pack(initial_tag, 0), std::memory_order_release);
    }

    int capacity() const { return static_cast<int>(gens_.size()); }
    /// Approximate while other threads are running; exact once they are quiet.
    int available() const { return capacity() - in_use_.load(std::memory_order_relaxed); }
    /// True when the tagged head compiles to a real atomic instruction rather than a hidden lock.
    static bool head_is_lock_free() { return std::atomic<std::uint64_t>::is_always_lock_free; }

    std::uint64_t allocate() {
        std::uint64_t h = head_.load(std::memory_order_acquire);
        for (;;) {
            const std::uint32_t index = index_of_head(h);
            if (index == kEmpty) return NONE;
            const std::uint32_t below = next_[index].load(std::memory_order_relaxed);
            // On failure compare_exchange_weak reloads `h` (with the failure order) and we go around again.  "Weak" may fail
            // spuriously, which is fine inside a loop and cheaper on LL/SC machines such as ARM.
            if (head_.compare_exchange_weak(h, pack(tag_of(h) + 1, below), std::memory_order_acquire, std::memory_order_acquire)) {
                const std::uint32_t g = gens_[index].load(std::memory_order_relaxed) + 1;  // we own the slot: even -> odd
                gens_[index].store(g, std::memory_order_release);
                in_use_.fetch_add(1, std::memory_order_relaxed);
                return GenPool::handle(index, g);
            }
        }
    }

    FreeResult free(std::uint64_t handle) {
        const std::uint32_t index = GenPool::index_of(handle), g = GenPool::generation_of(handle);
        if (index >= gens_.size() || (g & 1u) == 0) return FreeResult::Invalid;
        std::uint32_t expected = g;
        if (!gens_[index].compare_exchange_strong(expected, g + 1, std::memory_order_acq_rel, std::memory_order_relaxed)) return FreeResult::DoubleFree;
        in_use_.fetch_sub(1, std::memory_order_relaxed);
        std::uint64_t h = head_.load(std::memory_order_relaxed);
        for (;;) {
            next_[index].store(index_of_head(h), std::memory_order_relaxed);
            if (head_.compare_exchange_weak(h, pack(tag_of(h) + 1, index), std::memory_order_release, std::memory_order_relaxed)) return FreeResult::Freed;
        }
    }

    bool is_live(std::uint64_t handle) const {
        const std::uint32_t index = GenPool::index_of(handle), g = GenPool::generation_of(handle);
        return index < gens_.size() && (g & 1u) == 1 && gens_[index].load(std::memory_order_acquire) == g;
    }

private:
    static constexpr std::uint32_t kEmpty = 0xFFFFFFFFu;
    static constexpr std::uint64_t pack(std::uint32_t tag, std::uint32_t index) noexcept { return (static_cast<std::uint64_t>(tag) << 32) | index; }
    static constexpr std::uint32_t tag_of(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h >> 32); }
    static constexpr std::uint32_t index_of_head(std::uint64_t h) noexcept { return static_cast<std::uint32_t>(h); }
    static std::size_t checked(int capacity) {
        check_capacity(capacity);
        return static_cast<std::size_t>(capacity);
    }
    static_assert(std::atomic<std::uint64_t>::is_always_lock_free && std::atomic<std::uint32_t>::is_always_lock_free);

    std::vector<std::atomic<std::uint32_t>> gens_;
    std::vector<std::atomic<std::uint32_t>> next_;
    alignas(64) std::atomic<std::uint64_t> head_{0};  // its own cache line: not shared with the vectors' control blocks
    alignas(64) std::atomic<int> in_use_{0};          // and the counter on another one
};

}  // namespace pool
