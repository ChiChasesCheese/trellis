// ld01 · Shared-memory SPSC message channel — C++20 reference.  Statement: ../problem.md.
//
// Parts: 1 LongRing (single-threaded ring)  2 SpscLongRing (two threads, release/acquire, cached indices, padding)
//        3 MessageRing (variable-length records + wrap-around + drained)  4 SharedChannel (the ring in an mmap'ed file).
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

/// Java: IllegalStateException (finished producer, closed channel, file that is not a channel).
struct StateError : std::logic_error {
    using std::logic_error::logic_error;
};
/// Java: NoSuchElementException.  poll() on an empty LongQueue: every long is a valid message, so there is no sentinel.
struct EmptyError : std::runtime_error {
    using std::runtime_error::runtime_error;
};

/// Apple M cores have 128-byte cache lines, x86 has 64.  128 is right for both (a little wasteful on x86).
inline constexpr std::size_t kCacheLine = 128;

using Bytes = std::vector<std::uint8_t>;

inline bool is_pow2_in(long long v, long long lo, long long hi) {
    return v >= lo && v <= hi && std::has_single_bit(static_cast<unsigned long long>(v));
}

// ============================================================================================ Part 1
/// Interface shared by LongRing and SpscLongRing so one contract test can cover both.
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

/// Single-threaded ring.  head/tail are free-running counters: empty <=> head == tail, full <=> tail - head == capacity.
class LongRing final : public LongQueue {
public:
    static constexpr int MAX_CAPACITY = 1 << 30;

    explicit LongRing(int capacity) : buf_(check(capacity)), mask_(static_cast<std::uint64_t>(capacity) - 1) {}
    // Declaring the copy operations suppresses the implicit moves, so a moved-from ring is simply an untouched original
    // (a defaulted move would leave buf_ empty but mask_ stale: the next offer would write out of bounds).
    LongRing(const LongRing&) = default;
    LongRing& operator=(const LongRing&) = default;

    int capacity() const override { return static_cast<int>(buf_.size()); }
    int size() const override { return static_cast<int>(tail_ - head_); }
    bool is_empty() const override { return head_ == tail_; }

    bool offer(long long value) override {
        if (tail_ - head_ == buf_.size()) return false;
        buf_[tail_ & mask_] = value;
        ++tail_;
        return true;
    }
    long long poll() override {
        if (head_ == tail_) throw EmptyError("ring is empty");
        return buf_[head_++ & mask_];
    }

private:
    static std::size_t check(int capacity) {
        if (!is_pow2_in(capacity, 1, MAX_CAPACITY)) throw std::invalid_argument("capacity must be a power of two in [1, 2^30]: " + std::to_string(capacity));
        return static_cast<std::size_t>(capacity);
    }
    std::vector<long long> buf_;
    std::uint64_t mask_;
    std::uint64_t head_ = 0, tail_ = 0;
};

// ============================================================================================ Part 2
/// Thread-safe single-producer single-consumer ring.  Exactly one thread calls offer/is_full (producer), exactly one calls
/// poll/is_empty (consumer); size() may be called from any thread (approximate).  No locks and no CAS: tail has one writer
/// (the producer), head has one writer (the consumer), so release/acquire is all that is needed:
///   producer: slot = v;  tail.store(t + 1, release)         consumer: t = tail.load(acquire);  v = slot;  head.store(h + 1, release)
class SpscLongRing final : public LongQueue {
public:
    static constexpr int MAX_CAPACITY = 1 << 30;

    explicit SpscLongRing(int capacity) : buf_(check(capacity)), mask_(static_cast<std::uint64_t>(capacity) - 1) {}
    // std::atomic is neither copyable nor movable, so neither is the ring: its identity is its address.

    int capacity() const override { return static_cast<int>(buf_.size()); }

    int size() const override {  // approximate, any thread: read head first, then tail (tail only grows, so the difference is >= 0)
        const std::uint64_t h = head_.load(std::memory_order_acquire);
        const std::uint64_t t = tail_.load(std::memory_order_acquire);
        return static_cast<int>(std::min<std::uint64_t>(t - h, buf_.size()));
    }
    bool is_empty() const override { return consumer_head_ == tail_.load(std::memory_order_acquire); }  // consumer only
    bool is_full() const override { return producer_tail_ - head_.load(std::memory_order_acquire) == buf_.size(); }  // producer only

    bool offer(long long value) override {  // producer only
        const std::uint64_t t = producer_tail_;  // we are the only writer of tail: a plain read of our own copy is enough
        if (t - cached_head_ == buf_.size()) {   // looks full by the stale snapshot -> only now touch the consumer's cache line
            cached_head_ = head_.load(std::memory_order_acquire);
            if (t - cached_head_ == buf_.size()) return false;
        }
        buf_[t & mask_] = value;                                  // (1) data
        producer_tail_ = t + 1;
        tail_.store(t + 1, std::memory_order_release);            // (2) publish
        return true;
    }
    long long poll() override {  // consumer only
        const std::uint64_t h = consumer_head_;
        if (h == cached_tail_) {  // looks empty by the stale snapshot -> refresh
            cached_tail_ = tail_.load(std::memory_order_acquire);
            if (h == cached_tail_) throw EmptyError("ring is empty");
        }
        const long long v = buf_[h & mask_];                      // (3) data, after the acquire that saw (2)
        consumer_head_ = h + 1;
        head_.store(h + 1, std::memory_order_release);            // (4) give the slot back only after (3) is done
        return v;
    }

private:
    static std::size_t check(int capacity) {
        if (!is_pow2_in(capacity, 1, MAX_CAPACITY)) throw std::invalid_argument("capacity must be a power of two in [1, 2^30]: " + std::to_string(capacity));
        return static_cast<std::size_t>(capacity);
    }

    // Read-only after construction: both threads read it, nobody writes it.
    std::vector<long long> buf_;
    std::uint64_t mask_;
    // Everything the producer writes lives on its own cache line(s) ...
    alignas(kCacheLine) std::atomic<std::uint64_t> tail_{0};
    std::uint64_t producer_tail_ = 0;  // the producer's private copy of tail_ (so it never reads its own atomic)
    std::uint64_t cached_head_ = 0;
    // ... everything the consumer writes on others.
    alignas(kCacheLine) std::atomic<std::uint64_t> head_{0};
    std::uint64_t consumer_head_ = 0;
    std::uint64_t cached_tail_ = 0;
};

// ============================================================================================ Part 3
/// Variable-length messages on a raw byte span (heap, shm, or an mmap'ed file).
///
/// Layout (offsets from the start of the span):
///     0 magic u64 ("SPSCRING", written LAST, release)   8 capacity u32   12 version u32
///   128 head u64 (consumer only)   256 tail u64 (producer only)   264 closed u64   512 data area, `capacity` bytes
/// Record = [len:int32][payload][zero padding to a multiple of 8] (size (4 + len + 7) & ~7); PAD record = len -1, fills the
/// rest of the data area so that no record is split across the end.  The PAD is published on its own, even when the real
/// record then does not fit (otherwise: empty ring + tail near the end + big message = deadlock).
/// The head/tail/closed words live inside memory shared with other threads or processes, so they are accessed with
/// std::atomic_ref (C++20): the span's memory stays plain bytes, each access names its memory order.
class MessageRing {
public:
    static constexpr int HEADER_BYTES = 512;
    static constexpr int MIN_CAPACITY = 16;
    static constexpr int MAX_CAPACITY = 1 << 30;

    /// HEADER_BYTES + capacity.  Illegal capacity -> std::invalid_argument (lets SharedChannel validate before touching the file).
    static std::size_t segment_bytes(int capacity) {
        check_capacity(capacity);
        return HEADER_BYTES + static_cast<std::size_t>(capacity);
    }

    /// Fresh ring on `seg` (must be 8-byte aligned and >= segment_bytes(capacity), else std::invalid_argument).
    static MessageRing init(std::span<std::byte> seg, int capacity) {
        check_capacity(capacity);
        if (seg.size() < segment_bytes(capacity)) throw std::invalid_argument("segment too small: " + std::to_string(seg.size()));
        if (reinterpret_cast<std::uintptr_t>(seg.data()) % alignof(std::uint64_t) != 0) throw std::invalid_argument("segment must be 8-byte aligned");
        std::memset(seg.data(), 0, HEADER_BYTES);
        store32(seg, OFF_CAPACITY, static_cast<std::uint32_t>(capacity));
        store32(seg, OFF_VERSION, VERSION);
        word(seg, OFF_MAGIC).store(MAGIC, std::memory_order_release);  // last: whoever sees the magic sees the capacity
        return MessageRing(seg, capacity);
    }

    /// Join a ring somebody else initialised.  Wrong magic / version / size / alignment -> StateError.
    static MessageRing attach(std::span<std::byte> seg) {
        if (seg.size() < HEADER_BYTES || reinterpret_cast<std::uintptr_t>(seg.data()) % alignof(std::uint64_t) != 0 ||
            word(seg, OFF_MAGIC).load(std::memory_order_acquire) != MAGIC)
            throw StateError("not an initialised SPSC ring");
        const std::uint32_t version = load32(seg, OFF_VERSION), capacity = load32(seg, OFF_CAPACITY);
        if (version != VERSION) throw StateError("unsupported version " + std::to_string(version));
        if (capacity < MIN_CAPACITY || capacity > MAX_CAPACITY || !std::has_single_bit(capacity) || seg.size() < HEADER_BYTES + std::size_t{capacity})
            throw StateError("corrupt header: capacity=" + std::to_string(capacity) + ", segment=" + std::to_string(seg.size()));
        return MessageRing(seg, static_cast<int>(capacity));
    }

    int capacity() const { return capacity_; }
    int max_payload() const { return capacity_ - 4; }  ///< a record must fit into an empty ring

    // ---- producer -----------------------------------------------------------------------------------------------
    /// false = no room right now.  Longer than max_payload() can never fit -> std::invalid_argument.  After finish() -> StateError.
    bool offer(std::span<const std::uint8_t> msg) {
        const std::size_t len = msg.size();
        if (len > static_cast<std::size_t>(max_payload())) throw std::invalid_argument("message too large: " + std::to_string(len));
        if (finished_) throw StateError("producer already finished");
        const std::uint32_t rec = record_size(static_cast<std::uint32_t>(len));
        std::uint64_t t = tail_;
        std::uint32_t idx = static_cast<std::uint32_t>(t & mask_);
        const std::uint32_t to_end = static_cast<std::uint32_t>(capacity_) - idx;
        if (rec > to_end) {  // no contiguous room for the record: publish a PAD that fills the rest, on its own
            if (!has_room(t, to_end)) return false;
            store32(seg_, HEADER_BYTES + idx, static_cast<std::uint32_t>(PAD));
            t += to_end;
            tail_ = t;
            word(seg_, OFF_TAIL).store(t, std::memory_order_release);
            idx = 0;
        }
        if (!has_room(t, rec)) return false;
        std::byte* at = seg_.data() + HEADER_BYTES + idx;
        if (len != 0) std::memcpy(at + 4, msg.data(), len);
        store32(seg_, HEADER_BYTES + idx, static_cast<std::uint32_t>(len));
        tail_ = t + rec;
        word(seg_, OFF_TAIL).store(t + rec, std::memory_order_release);  // publish
        return true;
    }
    /// "No more messages."  Idempotent.  Written after the last tail publication.
    void finish() {
        finished_ = true;
        word(seg_, OFF_CLOSED).store(1, std::memory_order_release);
    }

    // ---- consumer -----------------------------------------------------------------------------------------------
    /// Next message, or nullopt when there is none right now.  nullopt is NOT the end of the stream: that is is_drained().
    std::optional<Bytes> poll() {
        std::uint64_t h = head_;
        while (true) {
            if (h == cached_tail_) {
                cached_tail_ = word(seg_, OFF_TAIL).load(std::memory_order_acquire);
                if (h == cached_tail_) return std::nullopt;
            }
            const std::uint32_t idx = static_cast<std::uint32_t>(h & mask_);
            const std::int32_t len = static_cast<std::int32_t>(load32(seg_, HEADER_BYTES + idx));
            if (len == PAD) {  // jump to the start of the data area
                h += static_cast<std::uint64_t>(capacity_) - idx;
                head_ = h;
                word(seg_, OFF_HEAD).store(h, std::memory_order_release);
                continue;
            }
            const std::byte* at = seg_.data() + HEADER_BYTES + idx + 4;
            Bytes out(static_cast<std::size_t>(len));
            if (len != 0) std::memcpy(out.data(), at, out.size());
            h += record_size(static_cast<std::uint32_t>(len));
            head_ = h;
            word(seg_, OFF_HEAD).store(h, std::memory_order_release);  // hand the space back only after the copy
            return out;
        }
    }
    /// Producer finished AND the consumer has caught up (a trailing PAD counts).  Read closed FIRST, then tail.
    bool is_drained() const {
        if (word(seg_, OFF_CLOSED).load(std::memory_order_acquire) == 0) return false;
        return head_ == word(seg_, OFF_TAIL).load(std::memory_order_acquire);
    }

    /// Published but not consumed bytes, PAD included.  Any role, approximate, clamped to [0, capacity].
    long long bytes_pending() const {
        const std::uint64_t h = word(seg_, OFF_HEAD).load(std::memory_order_acquire);
        const std::uint64_t t = word(seg_, OFF_TAIL).load(std::memory_order_acquire);
        return static_cast<long long>(std::min<std::uint64_t>(t - h, static_cast<std::uint64_t>(capacity_)));
    }

private:
    static constexpr std::uint64_t MAGIC = 0x5350534352494E47ULL;
    static constexpr std::uint32_t VERSION = 1;
    static constexpr std::size_t OFF_MAGIC = 0, OFF_CAPACITY = 8, OFF_VERSION = 12, OFF_HEAD = 128, OFF_TAIL = 256, OFF_CLOSED = 264;
    static constexpr std::int32_t PAD = -1;

    MessageRing(std::span<std::byte> seg, int capacity)
        : seg_(seg), capacity_(capacity), mask_(static_cast<std::uint64_t>(capacity) - 1) {
        tail_ = word(seg_, OFF_TAIL).load(std::memory_order_acquire);
        head_ = word(seg_, OFF_HEAD).load(std::memory_order_acquire);
        cached_head_ = head_;
        cached_tail_ = tail_;
    }

    static void check_capacity(int capacity) {
        if (!is_pow2_in(capacity, MIN_CAPACITY, MAX_CAPACITY)) throw std::invalid_argument("capacity must be a power of two in [16, 2^30]: " + std::to_string(capacity));
    }
    static std::uint32_t record_size(std::uint32_t len) { return (4 + len + 7) & ~7u; }

    // A span is a shallow view, so even a const MessageRing may load through it.
    static std::atomic_ref<std::uint64_t> word(std::span<std::byte> seg, std::size_t off) {
        return std::atomic_ref<std::uint64_t>(*reinterpret_cast<std::uint64_t*>(seg.data() + off));
    }
    static void store32(std::span<std::byte> seg, std::size_t off, std::uint32_t v) { std::memcpy(seg.data() + off, &v, 4); }
    static std::uint32_t load32(std::span<std::byte> seg, std::size_t off) {
        std::uint32_t v;
        std::memcpy(&v, seg.data() + off, 4);
        return v;
    }

    /// `need` more bytes available?  Try the cached head first, read the real one only when that says no.
    bool has_room(std::uint64_t t, std::uint32_t need) {
        if (static_cast<std::uint64_t>(capacity_) - (t - cached_head_) >= need) return true;
        cached_head_ = word(seg_, OFF_HEAD).load(std::memory_order_acquire);
        return static_cast<std::uint64_t>(capacity_) - (t - cached_head_) >= need;
    }

    std::span<std::byte> seg_;
    int capacity_;
    std::uint64_t mask_;
    // producer role
    std::uint64_t tail_ = 0, cached_head_ = 0;
    bool finished_ = false;
    // consumer role
    std::uint64_t head_ = 0, cached_tail_ = 0;
};

// ============================================================================================ Part 4
/// MessageRing inside a memory-mapped file: two processes map the same pages (MAP_SHARED).  RAII: the destructor unmaps.
/// Move-only.  One object plays one role: send/finish (producer) or receive/is_drained (consumer).
class SharedChannel {
public:
    /// New (or truncated) file of segment_bytes(capacity) bytes, header initialised.  Illegal capacity -> invalid_argument,
    /// raised BEFORE the file is touched.  OS failures -> std::system_error.
    static SharedChannel create(const std::filesystem::path& file, int capacity) {
        const std::size_t size = MessageRing::segment_bytes(capacity);
        Fd fd(::open(file.c_str(), O_RDWR | O_CREAT | O_TRUNC, 0644));
        if (fd.get() < 0) throw_errno("open " + file.string());
        if (::ftruncate(fd.get(), static_cast<off_t>(size)) != 0) throw_errno("ftruncate");
        Mapping map(fd.get(), size);
        auto ring = MessageRing::init(map.span(), capacity);
        return SharedChannel(std::move(map), ring);
    }
    /// Map an existing file.  Missing -> std::system_error(no_such_file_or_directory); too small / not a channel -> StateError.
    static SharedChannel open(const std::filesystem::path& file) {
        Fd fd(::open(file.c_str(), O_RDWR));
        if (fd.get() < 0) throw_errno("open " + file.string());
        struct stat st {};
        if (::fstat(fd.get(), &st) != 0) throw_errno("fstat");
        const auto size = static_cast<std::size_t>(st.st_size);
        if (size < MessageRing::HEADER_BYTES) throw StateError("file too small to be a channel: " + std::to_string(size));
        Mapping map(fd.get(), size);
        auto ring = MessageRing::attach(map.span());
        return SharedChannel(std::move(map), ring);
    }

    SharedChannel(SharedChannel&&) noexcept = default;
    SharedChannel& operator=(SharedChannel&& o) noexcept {
        if (this != &o) {
            map_ = std::move(o.map_);
            ring_ = o.ring_;
        }
        return *this;
    }
    SharedChannel(const SharedChannel&) = delete;
    SharedChannel& operator=(const SharedChannel&) = delete;

    int capacity() const { return ring().capacity(); }
    int max_payload() const { return ring().max_payload(); }
    bool send(std::span<const std::uint8_t> msg) { return ring().offer(msg); }
    void finish() { ring().finish(); }
    std::optional<Bytes> receive() { return ring().poll(); }
    bool is_drained() const { return ring().is_drained(); }

    /// Unmap.  Idempotent; the file stays on disk.  Afterwards every access throws StateError (and a moved-from channel too).
    void close() noexcept { map_.reset(); }

private:
    struct Fd {
        explicit Fd(int fd) : fd_(fd) {}
        ~Fd() { if (fd_ >= 0) ::close(fd_); }
        Fd(const Fd&) = delete;
        Fd& operator=(const Fd&) = delete;
        int get() const { return fd_; }
        int fd_;
    };
    /// Owns one mmap'ed region; moved-from / reset = empty.
    class Mapping {
    public:
        Mapping(int fd, std::size_t size) : size_(size) {
            void* p = ::mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
            if (p == MAP_FAILED) throw_errno("mmap");
            p_ = static_cast<std::byte*>(p);
        }
        Mapping(Mapping&& o) noexcept : p_(std::exchange(o.p_, nullptr)), size_(std::exchange(o.size_, 0)) {}
        Mapping& operator=(Mapping&& o) noexcept {
            if (this != &o) { reset(); p_ = std::exchange(o.p_, nullptr); size_ = std::exchange(o.size_, 0); }
            return *this;
        }
        ~Mapping() { reset(); }
        void reset() noexcept {
            if (p_ != nullptr) ::munmap(p_, size_);
            p_ = nullptr;
            size_ = 0;
        }
        bool open() const { return p_ != nullptr; }
        std::span<std::byte> span() const { return {p_, size_}; }
    private:
        std::byte* p_ = nullptr;
        std::size_t size_ = 0;
    };

    SharedChannel(Mapping map, MessageRing ring) : map_(std::move(map)), ring_(ring) {}
    MessageRing& ring() { require_open(); return ring_; }
    const MessageRing& ring() const { require_open(); return ring_; }
    void require_open() const {
        if (!map_.open()) throw StateError("channel is closed");
    }
    [[noreturn]] static void throw_errno(const std::string& what) { throw std::system_error(errno, std::generic_category(), what); }

    Mapping map_;
    MessageRing ring_;
};

}  // namespace spsc
