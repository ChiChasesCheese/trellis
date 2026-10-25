// ld01 · Shared-memory SPSC message channel — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: the exception types, kCacheLine, Bytes, the LongQueue interface, the signatures.  To write: every TODO.
// You may add private members and helpers; keep the public API.
#pragma once

#include <algorithm>
#include <atomic>
#include <bit>
#include <cerrno>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <memory>
#include <optional>
#include <span>
#include <stdexcept>
#include <string>
#include <system_error>
#include <utility>
#include <vector>

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

namespace spsc {

/// Java: IllegalStateException (finished producer, closed channel, a file that is not a channel).
struct StateError : std::logic_error {
    using std::logic_error::logic_error;
};
/// Java: NoSuchElementException.  poll() on an empty LongQueue throws it: every long is a valid message, so there is no sentinel.
struct EmptyError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

/// Apple M cores have 128-byte cache lines, x86 has 64.  128 is right for both.
inline constexpr std::size_t kCacheLine = 128;

using Bytes = std::vector<std::uint8_t>;

// ============================================================================================ Part 1
/// Interface shared by LongRing and SpscLongRing so one contract test covers both.
class LongQueue {
public:
    virtual ~LongQueue() = default;
    virtual int capacity() const = 0;
    virtual int size() const = 0;
    virtual bool offer(long long value) = 0;  ///< false when full (never overwrites)
    virtual long long poll() = 0;             ///< EmptyError when empty
    virtual bool is_empty() const = 0;
    virtual bool is_full() const { return size() == capacity(); }
};

/// Single-threaded ring.  Capacity: a power of two in [1, MAX_CAPACITY], else std::invalid_argument.
/// head / tail are free-running counters (never reduced modulo capacity): empty <=> head == tail, full <=> tail - head == capacity,
/// slot = counter & mask.  No wasted slot, no separate size field.  offer on a full ring returns false and overwrites nothing.
/// Hint: copying a LongRing is fine (value semantics) - but a defaulted MOVE of a vector-backed ring leaves a stale mask behind.
/// Declaring the copy operations (as below) suppresses the implicit moves, so a "move" copies and the source stays usable.
class LongRing final : public LongQueue {
public:
    static constexpr int MAX_CAPACITY = 1 << 30;

    explicit LongRing(int) { throw std::logic_error("TODO"); }
    LongRing(const LongRing&) = default;
    LongRing& operator=(const LongRing&) = default;

    int capacity() const override { throw std::logic_error("TODO"); }
    int size() const override { throw std::logic_error("TODO"); }
    bool is_empty() const override { throw std::logic_error("TODO"); }
    bool offer(long long) override { throw std::logic_error("TODO"); }
    long long poll() override { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 2
/// Thread-safe single-producer single-consumer ring.  Same semantics as LongRing, plus:
///  * exactly one thread calls offer / is_full (producer), exactly one calls poll / is_empty (consumer), size() any thread (approximate,
///    clamped to [0, capacity]);
///  * no locks, no compare-and-swap: tail has one writer, head has one writer.  std::atomic<std::uint64_t> with explicit orders:
///    write the slot, then tail.store(release); the consumer tail.load(acquire), then reads the slot, then head.store(release);
///  * cached indices: the producer keeps a stale copy of head and re-reads the real one only when the stale copy says "full";
///    the consumer does the same with tail;
///  * false sharing: everything the producer writes and everything the consumer writes sit on different cache lines
///    (alignas(kCacheLine) on the first member of each group).
/// std::atomic is not copyable or movable, so neither is the ring (stated below so that the class has the same shape as the real one).
class SpscLongRing final : public LongQueue {
public:
    static constexpr int MAX_CAPACITY = 1 << 30;

    explicit SpscLongRing(int) { throw std::logic_error("TODO"); }
    SpscLongRing(const SpscLongRing&) = delete;
    SpscLongRing& operator=(const SpscLongRing&) = delete;

    int capacity() const override { throw std::logic_error("TODO"); }
    int size() const override { throw std::logic_error("TODO"); }
    bool is_empty() const override { throw std::logic_error("TODO"); }
    bool is_full() const override { throw std::logic_error("TODO"); }
    bool offer(long long) override { throw std::logic_error("TODO"); }
    long long poll() override { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 3
/// Variable-length messages on a raw byte span (heap, shared memory, or an mmap'ed file).
///
/// Layout (offsets from the start of the span, the same contract as the Java version):
///     0 magic u64 0x5350534352494E47 ("SPSCRING"), written LAST with release     8 capacity u32     12 version u32 = 1
///   128 head u64 (consumer only)   256 tail u64 (producer only)   264 closed u64 (1 after finish())   512 data area, `capacity` bytes
/// Record = [len:int32][payload][zero padding to a multiple of 8], size (4 + len + 7) & ~7.  A record is never split across the end of
/// the data area: if it does not fit contiguously, first write a PAD record (len = -1) that fills the rest, then the record at offset 0.
/// The PAD is published on its own even if the real record then does not fit (offer returns false): otherwise an empty ring whose tail is
/// near the end can never take a big message.
///
/// head / tail / closed are shared with another thread or process: access them through std::atomic_ref<std::uint64_t> (C++20) with
/// explicit orders; the data bytes are plain memory protected by tail's release / acquire.  Consumer: acquire tail, read, release head.
/// Rules: init - capacity not a power of two in [16, 2^30], segment too small or not 8-byte aligned -> std::invalid_argument;
/// attach - wrong magic / version / size / alignment -> StateError;
/// offer - longer than max_payload() (= capacity - 4) -> std::invalid_argument (never fits), no room now -> false, after finish() -> StateError;
/// poll - nullopt when there is nothing (stepping over a PAD silently); an EMPTY message is a present, empty vector;
/// is_drained - producer finished AND head == tail (a trailing PAD counts); read `closed` first, then tail.
class MessageRing {
public:
    static constexpr int HEADER_BYTES = 512;
    static constexpr int MIN_CAPACITY = 16;
    static constexpr int MAX_CAPACITY = 1 << 30;

    /// HEADER_BYTES + capacity; an illegal capacity -> std::invalid_argument (so SharedChannel can validate before touching a file).
    static std::size_t segment_bytes(int) { throw std::logic_error("TODO"); }
    static MessageRing init(std::span<std::byte>, int) { throw std::logic_error("TODO"); }
    static MessageRing attach(std::span<std::byte>) { throw std::logic_error("TODO"); }

    int capacity() const { throw std::logic_error("TODO"); }
    int max_payload() const { throw std::logic_error("TODO"); }

    // producer
    bool offer(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    void finish() { throw std::logic_error("TODO"); }

    // consumer
    std::optional<Bytes> poll() { throw std::logic_error("TODO"); }
    bool is_drained() const { throw std::logic_error("TODO"); }

    /// Published but not consumed bytes, PAD included; approximate, clamped to [0, capacity].
    long long bytes_pending() const { throw std::logic_error("TODO"); }

private:
    MessageRing() = default;  // only init / attach make rings
};

// ============================================================================================ Part 4
/// MessageRing inside a memory-mapped file (mmap MAP_SHARED), RAII: the destructor unmaps.  Move-only.
///  * create(file, capacity): new or truncated file of segment_bytes(capacity) bytes (open O_CREAT|O_TRUNC, ftruncate, mmap),
///    MessageRing::init.  Illegal capacity -> std::invalid_argument BEFORE the file is touched.  OS errors -> std::system_error(errno).
///  * open(file): map an existing file + MessageRing::attach.  Missing file -> std::system_error with errc::no_such_file_or_directory;
///    too small / not a channel -> StateError.  Never leak the mapping or the descriptor when attach throws (RAII, not cleanup code).
///  * send / finish = producer role, receive / is_drained = consumer role.
///  * close(): unmap, idempotent, keep the file; afterwards (and in a moved-from channel) every access throws StateError.
class SharedChannel {
public:
    static SharedChannel create(const std::filesystem::path&, int) { throw std::logic_error("TODO"); }
    static SharedChannel open(const std::filesystem::path&) { throw std::logic_error("TODO"); }

    SharedChannel(const SharedChannel&) = delete;
    SharedChannel& operator=(const SharedChannel&) = delete;
    SharedChannel(SharedChannel&&) noexcept = default;  // with a RAII member that nulls itself on move, the default is right
    SharedChannel& operator=(SharedChannel&&) noexcept = default;

    int capacity() const { throw std::logic_error("TODO"); }
    int max_payload() const { throw std::logic_error("TODO"); }
    bool send(std::span<const std::uint8_t>) { throw std::logic_error("TODO"); }
    void finish() { throw std::logic_error("TODO"); }
    std::optional<Bytes> receive() { throw std::logic_error("TODO"); }
    bool is_drained() const { throw std::logic_error("TODO"); }
    void close() noexcept {}

private:
    SharedChannel() = default;
};

}  // namespace spsc
