// hc07 · Ticker hash map — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <bit>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <memory>
#include <new>
#include <optional>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <variant>
#include <vector>

namespace tickers {

using Key = std::uint64_t;
inline constexpr Key EMPTY = 0;       // a never-used slot
inline constexpr Key TOMB = ~Key{0};  // a deleted slot; every real key lies strictly between EMPTY and TOMB
inline constexpr std::uint64_t GOLDEN = 0x9E3779B97F4A7C15ull;

/// a + b, or std::overflow_error (given).  Signed overflow is undefined behaviour, so the builtin does the check.
inline long long add_checked(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("add overflows long long");
    return r;
}

// ------------------------------------------------------------------------------------------------ Part 1
/// Open addressing + linear probing in a std::vector; NO std::unordered_map / std::map.  `Hash` hashes the key text, but
/// the table must stay correct (just slower) even when Hash returns the same value for every key.
///  * the empty string is an ordinary key; values 0 / negative are real values (get() returns std::optional).
///  * (full + tombstones) / capacity <= 3/4 after every operation; delete leaves a tombstone, rehash clears them;
///    endless "insert new key, delete old key" must neither grow the table without bound nor loop forever.
///  * add(): overflow -> std::overflow_error and the table is unchanged (use add_checked).
///  * BasicTickerMap(expected_size): room for that many entries without a rehash; absurd sizes -> std::length_error.
///  * lookups take std::string_view and must not allocate.
///  * max_probe_length(): distance of the farthest live key from its home slot.
template <class Hash = std::hash<std::string_view>>
class BasicTickerMap {
public:
    explicit BasicTickerMap(std::size_t = 0, Hash = {}) { throw std::logic_error("TODO"); }

    std::size_t size() const noexcept { return 0; }
    std::size_t capacity() const noexcept { return 0; }
    std::size_t tombstones() const noexcept { return 0; }

    bool contains(std::string_view) const { throw std::logic_error("TODO"); }
    std::optional<long long> get(std::string_view) const { throw std::logic_error("TODO"); }
    /// Returns the previous value, if any.
    std::optional<long long> put(std::string_view, long long) { throw std::logic_error("TODO"); }
    /// value += delta (missing = 0); returns the new value.
    long long add(std::string_view, long long) { throw std::logic_error("TODO"); }
    std::optional<long long> remove(std::string_view) { throw std::logic_error("TODO"); }
    /// f(std::string_view key, long long value) once per live entry.
    template <class F>
    void for_each(F&&) const { throw std::logic_error("TODO"); }
    std::size_t max_probe_length() const { throw std::logic_error("TODO"); }
};

using TickerMap = BasicTickerMap<>;

// ------------------------------------------------------------------------------------------------ Part 2
/// 1..8 uppercase ASCII letters packed into the low 40 bits of a uint64_t: A..Z = 1..26, 5 bits per letter, the first
/// letter in the highest field (bits 35..39), unused trailing fields 0.  "AAPL" = (1<<35) | (1<<30) | (16<<25) | (12<<20).
namespace codec {

inline constexpr int MAX_LEN = 8;
inline constexpr int BITS = 5;

enum class Error { Empty, TooLong, BadChar };
inline const char* what(Error e) {
    switch (e) {
        case Error::Empty: return "empty ticker";
        case Error::TooLong: return "ticker longer than 8 characters";
        case Error::BadChar: return "not an uppercase ASCII letter";
    }
    return "?";
}
struct Ticker {
    Key key;
    friend bool operator==(const Ticker&, const Ticker&) = default;
};
struct Invalid {
    Error error;
    std::size_t position;  // index of the offending character
    friend bool operator==(const Invalid&, const Invalid&) = default;
};
using Parsed = std::variant<Ticker, Invalid>;

/// Empty -> Invalid{Empty, 0}; longer than 8 -> Invalid{TooLong, 8}; the first byte outside A..Z -> Invalid{BadChar, index}
/// (bytes >= 0x80 and NUL included).  Hint: `char` may be signed; widen to Key BEFORE shifting.  (Make it constexpr!)
inline Parsed parse(std::string_view) { throw std::logic_error("TODO"); }
/// Same as parse but throws std::invalid_argument.
inline Key pack(std::string_view) { throw std::logic_error("TODO"); }
/// 1 <= key < 2^40, every field <= 26, no letter after a 0 field.
inline bool is_valid_key(Key) { throw std::logic_error("TODO"); }
/// Inverse of pack; an invalid key -> std::invalid_argument.
inline std::string unpack(Key) { throw std::logic_error("TODO"); }
/// Ticker field of a wire message: 8 bytes, uppercase letters, right-padded with spaces ("AAPL    ") starting at `off`.
/// Blank, leading/inner space, lowercase, NUL, non-letter -> std::invalid_argument.  Does not fit in the buffer ->
/// std::out_of_range (beware: `off + 8` can wrap around for a huge off).
/// Hint: the low 5 bits of a letter are its code and the low 5 bits of a space are 0.
inline Key pack_wire(std::span<const std::byte>, std::size_t) { throw std::logic_error("TODO"); }

}  // namespace codec

/// Key = packed ticker, any uint64_t except 0 and ~0 (std::invalid_argument).  Open addressing, linear probing, tombstones,
/// (full + tombstones) / capacity <= 3/4.  Steady-state get()/add() must allocate nothing.
/// The hash must not be `key & mask` (packed short tickers have zero low bits) and std::hash<uint64_t> is the identity.
/// LongTickerMap(expected_size): room for that many entries without a rehash; absurd sizes -> std::length_error.
class LongTickerMap {
public:
    explicit LongTickerMap(std::size_t = 0) { throw std::logic_error("TODO"); }

    std::size_t size() const noexcept { return 0; }
    std::size_t capacity() const noexcept { return 0; }
    std::size_t tombstones() const noexcept { return 0; }

    bool contains(Key) const { throw std::logic_error("TODO"); }
    long long get(Key, long long) const { throw std::logic_error("TODO"); }
    /// true = new key, false = overwrote.
    bool put(Key, long long) { throw std::logic_error("TODO"); }
    /// value += delta (missing = 0); overflow -> std::overflow_error, value unchanged.
    long long add(Key, long long) { throw std::logic_error("TODO"); }
    bool remove(Key) { throw std::logic_error("TODO"); }
    /// f(Key, long long) once per live entry.
    template <class F>
    void for_each(F&&) const { throw std::logic_error("TODO"); }
    std::size_t max_probe_length() const { throw std::logic_error("TODO"); }
};

// ------------------------------------------------------------------------------------------------ Part 3
/// Minimal perfect hash for a fixed universe of keys: the n keys map one-to-one onto 0..n-1, any other key -> NPOS.
/// build(): keys must be unique and not 0 / ~0 (std::invalid_argument); an empty universe is fine; 100,000 keys in
/// well under 2 seconds.  Hint: hash-and-displace; index_of must compare the stored key (a key outside the universe
/// still hashes to some slot).  Hint: std::vector<bool> is a bit-packed proxy container: use std::vector<std::uint8_t>.
class SymbolIndex {
public:
    static constexpr int NPOS = -1;
    static SymbolIndex build(std::span<const Key>) { throw std::logic_error("TODO"); }
    std::size_t size() const noexcept { return 0; }
    int index_of(Key) const noexcept { return NPOS; }
    Key key_at(std::size_t) const { throw std::logic_error("TODO"); }
};

/// The key set (ticker strings in codec format) is fixed at construction; invalid or duplicate -> std::invalid_argument.
/// Values start at 0 ("in the universe but never written" is 0, not absent).  put() of an unknown key -> false; add() of an
/// unknown key -> std::invalid_argument; overflow -> std::overflow_error, value unchanged.  add_at/get_at/key_at with an
/// index outside 0..size()-1 -> std::out_of_range (never undefined behaviour).
class FrozenTickerMap {
public:
    explicit FrozenTickerMap(const std::vector<std::string>&) { throw std::logic_error("TODO"); }
    std::size_t size() const noexcept { return 0; }
    int index_of(Key) const noexcept { return -1; }
    bool contains(Key) const noexcept { return false; }
    long long get(Key, long long) const noexcept { return 0; }
    bool put(Key, long long) noexcept { return false; }
    long long add(Key, long long) { throw std::logic_error("TODO"); }
    long long add_at(int, long long) { throw std::logic_error("TODO"); }
    long long get_at(int) const { throw std::logic_error("TODO"); }
    Key key_at(int) const { throw std::logic_error("TODO"); }
};

// ------------------------------------------------------------------------------------------------ Part 4
/// Fixed capacity, one allocation, never grows: 64-byte aligned storage of 16-byte slots {key, value}; slots =
/// bit_ceil(2 * max_entries), at least 8; key 0 = empty slot.  max_entries outside 1..2^28 -> std::invalid_argument.
/// A NEW key beyond max_entries -> std::length_error; existing keys can still be updated.  Keys 0 and ~0 ->
/// std::invalid_argument.  No remove.  Move-only; after a move or close() the object is empty: size() == 0 and every
/// access throws std::logic_error.  close() is idempotent.  data() = start of the slot array (for the alignment check).
/// Hint: ::operator new(bytes, std::align_val_t{64}) and the matching aligned delete.
class FixedTickerMap {
public:
    explicit FixedTickerMap(std::size_t) { throw std::logic_error("TODO"); }
    FixedTickerMap(FixedTickerMap&&) noexcept {}
    FixedTickerMap& operator=(FixedTickerMap&&) noexcept { return *this; }
    FixedTickerMap(const FixedTickerMap&) = delete;
    FixedTickerMap& operator=(const FixedTickerMap&) = delete;

    std::size_t size() const noexcept { return 0; }
    std::size_t capacity() const noexcept { return 0; }
    std::size_t max_entries() const noexcept { return 0; }
    const void* data() const noexcept { return nullptr; }
    bool contains(Key) const { throw std::logic_error("TODO"); }
    long long get(Key, long long) const { throw std::logic_error("TODO"); }
    bool put(Key, long long) { throw std::logic_error("TODO"); }
    long long add(Key, long long) { throw std::logic_error("TODO"); }
    void close() noexcept {}
};

}  // namespace tickers
