// hc07 · Ticker hash map — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 TickerMap (open addressing over std::vector, string keys), 2 codec + LongTickerMap (ticker packed into a
//        uint64_t), 3 SymbolIndex + FrozenTickerMap (minimal perfect hash), 4 FixedTickerMap (one aligned block, no growth).
#pragma once

#include <algorithm>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <functional>
#include <memory>
#include <new>
#include <optional>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <variant>
#include <vector>

namespace tickers {

// ---- common ----
using Key = std::uint64_t;
inline constexpr Key EMPTY = 0;        // a never-used slot
inline constexpr Key TOMB = ~Key{0};   // a deleted slot; every real key lies strictly between EMPTY and TOMB
inline constexpr std::uint64_t GOLDEN = 0x9E3779B97F4A7C15ull;  // 2^64 / golden ratio, odd

/// a + b, or std::overflow_error.  Signed overflow is undefined behaviour, so the builtin does the check.
inline long long add_checked(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("add overflows long long");
    return r;
}

/// Smallest power of two >= max(8, entries * load_inverse); std::length_error when that is absurdly large.
inline std::size_t capacity_for(std::size_t entries, std::size_t load_inverse, std::size_t limit) {
    if (entries > limit / load_inverse) throw std::length_error("table too large");
    return std::bit_ceil(std::max<std::size_t>(8, entries * load_inverse));
}

// ---- Part 1: TickerMap ----
/// Open addressing + linear probing over one std::vector<Slot>.  A slot is Empty (never used: a probe stops here),
/// Full, or Tomb (deleted: a probe must go on).  (full + tombs) / capacity <= 1/2 after every insert.
/// `Hash` hashes the key text; the table mixes it again (Fibonacci hashing), so even a poor Hash stays correct.
template <class Hash = std::hash<std::string_view>>
class BasicTickerMap {
public:
    explicit BasicTickerMap(std::size_t expected_size = 0, Hash hash = {}) : hash_(std::move(hash)) {
        allocate(capacity_for(expected_size, 2, std::size_t{1} << 30));
    }

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return slots_.size(); }
    std::size_t tombstones() const noexcept { return tombs_; }

    bool contains(std::string_view key) const { return locate(key).found; }

    std::optional<long long> get(std::string_view key) const {
        const Probe p = locate(key);
        if (!p.found) return std::nullopt;
        return slots_[p.index].value;
    }

    /// Returns the previous value, if any.
    std::optional<long long> put(std::string_view key, long long value) {
        const Probe p = locate(key);
        if (p.found) return std::exchange(slots_[p.index].value, value);
        insert_new(p.index, key, value);
        return std::nullopt;
    }

    /// value += delta (a missing key counts as 0); returns the new value.  Overflow: std::overflow_error, table unchanged.
    long long add(std::string_view key, long long delta) {
        const Probe p = locate(key);
        if (p.found) return slots_[p.index].value = add_checked(slots_[p.index].value, delta);  // computed first, stored after
        insert_new(p.index, key, delta);
        return delta;
    }

    std::optional<long long> remove(std::string_view key) {
        const Probe p = locate(key);
        if (!p.found) return std::nullopt;
        Slot& s = slots_[p.index];
        const long long old = s.value;
        s.state = State::Tomb;  // NOT Empty: a key that was pushed past this slot would become unreachable
        s.key.clear();
        s.value = 0;
        --size_;
        ++tombs_;
        return old;
    }

    template <class F>
    void for_each(F&& f) const {
        for (const Slot& s : slots_)
            if (s.state == State::Full) f(std::string_view(s.key), s.value);
    }

    /// Distance of the farthest live key from its home slot (0 = every key sits at home).
    std::size_t max_probe_length() const {
        std::size_t worst = 0;
        for (std::size_t i = 0; i < slots_.size(); ++i)
            if (slots_[i].state == State::Full) worst = std::max(worst, (i - home(slots_[i].key)) & mask_);
        return worst;
    }

    // ---- TickerMap: internals ----
private:
    enum class State : std::uint8_t { Empty, Full, Tomb };
    struct Slot {
        std::string key;  // a short key (<= 15 chars everywhere) lives inside the string object (small-string optimisation): no allocation
        long long value = 0;
        State state = State::Empty;
    };
    struct Probe {
        std::size_t index;  // found: the key's slot.  Otherwise: where to insert (first tombstone on the way, else the empty slot)
        bool found;
    };

    std::size_t home(std::string_view key) const { return static_cast<std::size_t>((std::uint64_t{hash_(key)} * GOLDEN) >> shift_); }

    Probe locate(std::string_view key) const {
        std::size_t i = home(key);
        std::optional<std::size_t> first_tomb;
        for (;;) {  // terminates: the load factor keeps empty slots around
            const Slot& s = slots_[i];
            if (s.state == State::Empty) return {first_tomb.value_or(i), false};
            if (s.state == State::Tomb) {
                if (!first_tomb) first_tomb = i;
            } else if (s.key == key) {
                return {i, true};
            }
            i = (i + 1) & mask_;
        }
    }

    void insert_new(std::size_t i, std::string_view key, long long value) {
        if (slots_[i].state == State::Tomb) {
            slots_[i].key.assign(key);  // may allocate for long keys: do it before touching the counters
            --tombs_;
        } else {
            if ((size_ + tombs_ + 1) * 2 > slots_.size()) {  // taking an empty slot would use more than half of the table
                rehash();
                i = home(key);
                while (slots_[i].state != State::Empty) i = (i + 1) & mask_;
            }
            slots_[i].key.assign(key);
        }
        slots_[i].value = value;
        slots_[i].state = State::Full;
        ++size_;
    }

    /// Rebuild with capacity >= 4 * live entries.  Tombstones disappear, so insert/delete churn cannot bloat the table.
    void rehash() {
        std::vector<Slot> old = std::move(slots_);
        allocate(capacity_for(size_, 4, std::size_t{1} << 30));
        for (Slot& s : old) {
            if (s.state != State::Full) continue;
            std::size_t i = home(s.key);
            while (slots_[i].state != State::Empty) i = (i + 1) & mask_;
            slots_[i] = std::move(s);
        }
        // allocate() reset the counters; the live entries were re-inserted
    }

    void allocate(std::size_t cap) {
        const std::size_t live = size_;
        slots_ = std::vector<Slot>(cap);
        mask_ = cap - 1;
        shift_ = 64 - std::countr_zero(cap);
        tombs_ = 0;
        size_ = live;
    }

    Hash hash_;
    std::vector<Slot> slots_;
    std::size_t size_ = 0, tombs_ = 0, mask_ = 0;
    int shift_ = 0;
};

using TickerMap = BasicTickerMap<>;

// ---- Part 2: codec ----
/// 1..8 uppercase ASCII letters packed into the low 40 bits of a uint64_t: A..Z = 1..26, 5 bits per letter, the first
/// letter in the highest field, unused trailing fields 0.  "AAPL" = (1<<35) | (1<<30) | (16<<25) | (12<<20).
namespace codec {

inline constexpr int MAX_LEN = 8;
inline constexpr int BITS = 5;
inline constexpr Key FIELD_MASK = 0x1F;

enum class Error { Empty, TooLong, BadChar };
constexpr const char* what(Error e) {
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
/// Bad input is routine on a market-data feed, so parse() reports it as a value; pack() throws.
using Parsed = std::variant<Ticker, Invalid>;

constexpr Parsed parse(std::string_view s) noexcept {
    if (s.empty()) return Invalid{Error::Empty, 0};
    if (s.size() > static_cast<std::size_t>(MAX_LEN)) return Invalid{Error::TooLong, MAX_LEN};
    Key key = 0;
    for (std::size_t i = 0; i < s.size(); ++i) {
        const auto c = static_cast<unsigned char>(s[i]);  // plain `char` may be signed: bytes >= 0x80 would compare as negative
        if (c < 'A' || c > 'Z') return Invalid{Error::BadChar, i};
        key |= static_cast<Key>(c - 'A' + 1) << (BITS * (MAX_LEN - 1 - static_cast<int>(i)));  // widen BEFORE shifting
    }
    return Ticker{key};
}

constexpr Key pack(std::string_view s) {
    const Parsed p = parse(s);
    if (const auto* t = std::get_if<Ticker>(&p)) return t->key;
    throw std::invalid_argument(what(std::get<Invalid>(p).error));
}

constexpr bool is_valid_key(Key key) noexcept {
    if (key == 0 || (key >> (BITS * MAX_LEN)) != 0) return false;
    bool ended = false;
    for (int i = 0; i < MAX_LEN; ++i) {
        const Key f = (key >> (BITS * (MAX_LEN - 1 - i))) & FIELD_MASK;
        if (f > 26) return false;
        if (f == 0) ended = true;
        else if (ended) return false;  // no letter after a 0 field
    }
    return true;
}

inline std::string unpack(Key key) {
    if (!is_valid_key(key)) throw std::invalid_argument("not a packed ticker: " + std::to_string(key));
    std::string s;
    for (int i = 0; i < MAX_LEN; ++i) {
        const Key f = (key >> (BITS * (MAX_LEN - 1 - i))) & FIELD_MASK;
        if (f == 0) break;
        s.push_back(static_cast<char>('A' + f - 1));
    }
    return s;
}

// ---- codec: pack_wire ----
/// Ticker field of a wire message: 8 bytes, uppercase letters, right-padded with spaces ("AAPL    ").
/// Invalid (blank, leading/inner space, lowercase, NUL, non-letter) -> std::invalid_argument.
/// Does not fit in the buffer -> std::out_of_range.  The low 5 bits of a letter are exactly its code (0x41 -> 1 ... 0x5A -> 26)
/// and the low 5 bits of a space are 0, so the packed value is just the low 5 bits of every byte laid side by side.
inline Key pack_wire(std::span<const std::byte> buf, std::size_t off) {
    if (buf.size() < 8 || off > buf.size() - 8)  // `off + 8 > size` would wrap around for a huge off
        throw std::out_of_range("ticker field does not fit in the buffer");
    std::uint64_t word;
    std::memcpy(&word, buf.data() + off, 8);  // no aliasing or alignment problem, and the compiler emits one load
    if constexpr (std::endian::native == std::endian::little) word = __builtin_bswap64(word);  // byte 0 -> most significant
    if ((word >> 56) == ' ') throw std::invalid_argument("empty ticker field");
    bool seen_space = false;
    Key key = 0;
    for (int i = 0; i < MAX_LEN; ++i) {
        const auto b = static_cast<unsigned>((word >> (8 * (MAX_LEN - 1 - i))) & 0xFF);
        if (b == ' ') seen_space = true;
        else if (seen_space || b < 'A' || b > 'Z') throw std::invalid_argument("bad ticker field at byte " + std::to_string(i));
        key |= static_cast<Key>(b & FIELD_MASK) << (BITS * (MAX_LEN - 1 - i));
    }
    return key;
}

}  // namespace codec

// ---- Part 2: LongTickerMap ----
/// Key = packed ticker (anything but 0 and ~0), value = long long.  Open addressing, linear probing, tombstones, one
/// std::vector<Slot> of 16-byte {key, value} pairs: a probe that finds the key has the value in the same cache line.
/// In steady state add()/get() allocate nothing.
class LongTickerMap {
public:
    explicit LongTickerMap(std::size_t expected_size = 0) { allocate(capacity_for(expected_size, 2, std::size_t{1} << 29)); }

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return slots_.size(); }
    std::size_t tombstones() const noexcept { return tombs_; }

    bool contains(Key key) const {
        check(key);
        return locate(key).found;
    }

    long long get(Key key, long long if_absent) const {
        check(key);
        const Probe p = locate(key);
        return p.found ? slots_[p.index].value : if_absent;
    }

    /// true = new key, false = overwrote.
    bool put(Key key, long long value) {
        check(key);
        const Probe p = locate(key);
        if (p.found) {
            slots_[p.index].value = value;
            return false;
        }
        insert_new(p.index, key, value);
        return true;
    }

    /// value += delta (a missing key counts as 0).  Overflow: std::overflow_error, value unchanged.
    long long add(Key key, long long delta) {
        check(key);
        const Probe p = locate(key);
        if (p.found) return slots_[p.index].value = add_checked(slots_[p.index].value, delta);
        insert_new(p.index, key, delta);
        return delta;
    }

    bool remove(Key key) {
        check(key);
        const Probe p = locate(key);
        if (!p.found) return false;
        slots_[p.index] = {TOMB, 0};
        --size_;
        ++tombs_;
        return true;
    }

    template <class F>
    void for_each(F&& f) const {
        for (const Slot& s : slots_)
            if (s.key != EMPTY && s.key != TOMB) f(s.key, s.value);
    }

    std::size_t max_probe_length() const {
        std::size_t worst = 0;
        for (std::size_t i = 0; i < slots_.size(); ++i)
            if (slots_[i].key != EMPTY && slots_[i].key != TOMB) worst = std::max(worst, (i - home(slots_[i].key)) & mask_);
        return worst;
    }

    // ---- LongTickerMap: internals ----
private:
    struct Slot {
        Key key;
        long long value;
    };
    struct Probe {
        std::size_t index;
        bool found;
    };

    static void check(Key key) {
        if (key == EMPTY || key == TOMB) throw std::invalid_argument("key must not be 0 or ~0 (empty / tombstone marker)");
    }

    // Never `key & mask`: a packed short ticker has zeros in its low bits.  And std::hash<uint64_t> is the identity.
    std::size_t home(Key key) const noexcept { return static_cast<std::size_t>((key * GOLDEN) >> shift_); }

    Probe locate(Key key) const noexcept {
        std::size_t i = home(key);
        std::optional<std::size_t> first_tomb;
        for (;;) {
            const Key k = slots_[i].key;
            if (k == key) return {i, true};
            if (k == EMPTY) return {first_tomb.value_or(i), false};
            if (k == TOMB && !first_tomb) first_tomb = i;
            i = (i + 1) & mask_;
        }
    }

    void insert_new(std::size_t i, Key key, long long value) {
        if (slots_[i].key == TOMB) {
            --tombs_;
        } else if ((size_ + tombs_ + 1) * 2 > slots_.size()) {
            rehash();
            i = home(key);
            while (slots_[i].key != EMPTY) i = (i + 1) & mask_;
        }
        slots_[i] = {key, value};
        ++size_;
    }

    void rehash() {
        std::vector<Slot> old = std::move(slots_);
        allocate(capacity_for(size_, 4, std::size_t{1} << 29));
        for (const Slot& s : old) {
            if (s.key == EMPTY || s.key == TOMB) continue;
            std::size_t i = home(s.key);
            while (slots_[i].key != EMPTY) i = (i + 1) & mask_;
            slots_[i] = s;
        }
    }

    void allocate(std::size_t cap) {
        slots_.assign(cap, Slot{EMPTY, 0});
        mask_ = cap - 1;
        shift_ = 64 - std::countr_zero(cap);
        tombs_ = 0;
    }

    std::vector<Slot> slots_;
    std::size_t size_ = 0, tombs_ = 0, mask_ = 0;
    int shift_ = 0;
};

// ---- Part 3: SymbolIndex ----
/// Minimal perfect hash (hash-and-displace, a simplified CHD): the n keys of a fixed universe map one-to-one onto 0..n-1.
/// 1. split the keys into ~n/4 buckets by hash; 2. largest bucket first, find a displacement d that sends every key of the
/// bucket to a free slot; 3. single-key buckets last: take the next free slot (stored as ~slot, a negative number).
/// index_of() must compare the stored key: a key outside the universe still hashes to SOME slot.
class SymbolIndex {
public:
    static constexpr int NPOS = -1;

    /// Keys must be unique and not 0 / ~0, else std::invalid_argument.  The universe may be empty.
    static SymbolIndex build(std::span<const Key> universe) {
        for (Key k : universe)
            if (k == EMPTY || k == TOMB) throw std::invalid_argument("key must not be 0 or ~0");
        std::vector<Key> sorted(universe.begin(), universe.end());
        std::sort(sorted.begin(), sorted.end());
        if (std::adjacent_find(sorted.begin(), sorted.end()) != sorted.end()) throw std::invalid_argument("duplicate key");
        if (universe.empty()) return SymbolIndex({}, {}, 0);
        for (int seed = 0; seed < MAX_SEEDS; ++seed)
            if (auto built = try_build(universe, seed)) return std::move(*built);
        throw std::runtime_error("no perfect hash found");
    }

    std::size_t size() const noexcept { return keys_.size(); }

    /// Index of `key` in 0..size()-1, or NPOS if it is not in the universe.
    int index_of(Key key) const noexcept {
        if (keys_.empty()) return NPOS;
        const std::uint64_t h = hash(key, seed_);
        const std::int32_t d = disp_[bucket(h, disp_.size())];
        const std::size_t s = d < 0 ? static_cast<std::size_t>(~d) : slot(h, d, keys_.size());
        return keys_[s] == key ? static_cast<int>(s) : NPOS;
    }

    Key key_at(std::size_t index) const { return keys_.at(index); }

private:
    static constexpr int MAX_SEEDS = 64;
    static constexpr int MAX_DISPLACEMENT = 1 << 22;

    SymbolIndex(std::vector<Key> keys, std::vector<std::int32_t> disp, int seed)
        : keys_(std::move(keys)), disp_(std::move(disp)), seed_(seed) {}

    // splitmix64 finalizer: a bijection with good avalanche, so keys differing in one letter get unrelated hashes
    static std::uint64_t mix(std::uint64_t z) noexcept {
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBull;
        return z ^ (z >> 31);
    }
    static std::uint64_t hash(Key key, int seed) noexcept { return mix(key ^ (static_cast<std::uint64_t>(seed) * GOLDEN)); }
    /// Map a 32-bit value into [0, range) with a multiply and a shift instead of a division (Lemire's fastrange).
    static std::size_t bucket(std::uint64_t h, std::size_t r) noexcept { return static_cast<std::size_t>(((h >> 32) * r) >> 32); }
    /// Candidate slot number d.  Mixing d in (instead of adding d * c) makes the candidates behave independently.
    static std::size_t slot(std::uint64_t h, std::int32_t d, std::size_t m) noexcept {
        const std::uint64_t x = (h ^ (static_cast<std::uint64_t>(d) * GOLDEN)) * 0xD6E8FEB86659FD93ull;
        return static_cast<std::size_t>(((x >> 32) * m) >> 32);
    }

    // ---- SymbolIndex: try_build ----
    static std::optional<SymbolIndex> try_build(std::span<const Key> universe, int seed) {
        const std::size_t n = universe.size();
        const std::size_t r = std::max<std::size_t>(1, (n + 3) / 4);
        std::vector<std::uint64_t> h(n);
        std::vector<std::size_t> start(r + 1, 0);
        for (std::size_t i = 0; i < n; ++i) {
            h[i] = hash(universe[i], seed);
            ++start[bucket(h[i], r) + 1];
        }
        for (std::size_t b = 0; b < r; ++b) start[b + 1] += start[b];  // counting sort: bucket b = members[start[b] .. start[b+1])
        std::vector<std::size_t> fill(start.begin(), start.end() - 1), members(n);
        for (std::size_t i = 0; i < n; ++i) members[fill[bucket(h[i], r)]++] = i;
        std::vector<std::uint64_t> order(r);  // (size << 32 | bucket): sorting puts the biggest buckets last
        for (std::size_t b = 0; b < r; ++b) order[b] = ((start[b + 1] - start[b]) << 32) | b;
        std::sort(order.begin(), order.end());

        std::vector<Key> slot_keys(n, EMPTY);
        std::vector<std::uint8_t> used(n, 0);  // not vector<bool>
        std::vector<std::int32_t> disp(r, 0);
        std::vector<std::size_t> tmp(n);
        std::size_t cursor = 0;
        for (std::size_t idx = r; idx-- > 0;) {
            const std::size_t b = order[idx] & 0xFFFFFFFFull;
            const std::size_t from = start[b], to = start[b + 1], size = to - from;
            if (size == 0) continue;
            if (size == 1) {
                while (used[cursor]) ++cursor;
                used[cursor] = 1;
                slot_keys[cursor] = universe[members[from]];
                disp[b] = ~static_cast<std::int32_t>(cursor);
                continue;
            }
            bool placed = false;
            for (std::int32_t d = 0; d < MAX_DISPLACEMENT && !placed; ++d) {
                std::size_t ok = 0;
                for (std::size_t p = from; p < to; ++p) {
                    const std::size_t s = slot(h[members[p]], d, n);
                    if (used[s]) break;
                    used[s] = 1;  // claim at once, so two keys of the same bucket landing on one slot are noticed
                    tmp[ok++] = s;
                }
                if (ok == size) {
                    for (std::size_t p = 0; p < size; ++p) slot_keys[tmp[p]] = universe[members[from + p]];
                    disp[b] = d;
                    placed = true;
                } else {
                    for (std::size_t p = 0; p < ok; ++p) used[tmp[p]] = 0;  // roll back, try the next d
                }
            }
            if (!placed) return std::nullopt;  // this seed failed: the caller tries the next one
        }
        return SymbolIndex(std::move(slot_keys), std::move(disp), seed);
    }

    std::vector<Key> keys_;           // keys_[slot] = the key assigned to that slot
    std::vector<std::int32_t> disp_;  // per bucket: displacement d, or ~slot for single-key buckets
    int seed_ = 0;
};

// ---- Part 3: FrozenTickerMap ----
/// The key set is fixed at construction; only the values change.  A key of the universe that was never written has value 0.
/// get/put/add take a packed key; index_of + add_at/get_at let a caller cache the index and skip hashing altogether.
class FrozenTickerMap {
public:
    explicit FrozenTickerMap(const std::vector<std::string>& universe)
        : index_(SymbolIndex::build(pack_all(universe))), values_(index_.size(), 0) {}  // duplicates -> invalid_argument

    std::size_t size() const noexcept { return values_.size(); }
    int index_of(Key key) const noexcept { return index_.index_of(key); }
    bool contains(Key key) const noexcept { return index_of(key) >= 0; }

    long long get(Key key, long long if_absent) const noexcept {
        const int i = index_of(key);
        return i < 0 ? if_absent : values_[static_cast<std::size_t>(i)];
    }

    /// false if the key is not in the universe.
    bool put(Key key, long long value) noexcept {
        const int i = index_of(key);
        if (i < 0) return false;
        values_[static_cast<std::size_t>(i)] = value;
        return true;
    }

    /// Unknown key: std::invalid_argument.  Overflow: std::overflow_error, value unchanged.
    long long add(Key key, long long delta) {
        const int i = index_of(key);
        if (i < 0) throw std::invalid_argument("unknown ticker key: " + std::to_string(key));
        return add_at(i, delta);
    }

    long long add_at(int index, long long delta) {
        long long& v = values_.at(checked(index));
        return v = add_checked(v, delta);  // the sum is computed before the store: overflow leaves the value alone
    }
    long long get_at(int index) const { return values_.at(checked(index)); }
    Key key_at(int index) const { return index_.key_at(checked(index)); }

private:
    static std::size_t checked(int index) {
        if (index < 0) throw std::out_of_range("negative index");
        return static_cast<std::size_t>(index);
    }
    static std::vector<Key> pack_all(const std::vector<std::string>& universe) {
        std::vector<Key> keys;
        keys.reserve(universe.size());
        for (const std::string& t : universe) keys.push_back(codec::pack(t));  // invalid -> invalid_argument
        return keys;
    }
    SymbolIndex index_;
    std::vector<long long> values_;
};

// ---- Part 4: FixedTickerMap ----
/// Fixed capacity, one allocation, never grows or moves: 64-byte aligned storage of 16-byte slots {key, value}
/// (four slots per cache line), slots = bit_ceil(2 * max_entries).  A new key beyond max_entries -> std::length_error,
/// existing keys can still be updated.  No remove.  Move-only; a moved-from or closed map throws std::logic_error.
class FixedTickerMap {
public:
    explicit FixedTickerMap(std::size_t max_entries) {
        if (max_entries < 1 || max_entries > (std::size_t{1} << 28)) throw std::invalid_argument("max_entries out of range");
        max_entries_ = max_entries;
        capacity_ = std::bit_ceil(std::max<std::size_t>(8, 2 * max_entries));
        mask_ = capacity_ - 1;
        shift_ = 64 - std::countr_zero(capacity_);
        const std::size_t bytes = capacity_ * sizeof(Slot);
        void* raw = ::operator new(bytes, std::align_val_t{64});
        std::memset(raw, 0, bytes);  // key == 0 means empty
        slots_.reset(static_cast<Slot*>(raw));
    }

    FixedTickerMap(FixedTickerMap&& o) noexcept
        : slots_(std::move(o.slots_)), capacity_(std::exchange(o.capacity_, 0)), max_entries_(std::exchange(o.max_entries_, 0)),
          size_(std::exchange(o.size_, 0)), mask_(std::exchange(o.mask_, 0)), shift_(std::exchange(o.shift_, 0)) {}
    FixedTickerMap& operator=(FixedTickerMap&& o) noexcept {
        if (this != &o) {
            slots_ = std::move(o.slots_);
            capacity_ = std::exchange(o.capacity_, 0);
            max_entries_ = std::exchange(o.max_entries_, 0);
            size_ = std::exchange(o.size_, 0);
            mask_ = std::exchange(o.mask_, 0);
            shift_ = std::exchange(o.shift_, 0);
        }
        return *this;
    }
    FixedTickerMap(const FixedTickerMap&) = delete;
    FixedTickerMap& operator=(const FixedTickerMap&) = delete;

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return capacity_; }
    std::size_t max_entries() const noexcept { return max_entries_; }
    const void* data() const noexcept { return slots_.get(); }

    bool contains(Key key) const { return probe(key).found; }

    long long get(Key key, long long if_absent) const {
        const Probe p = probe(key);
        return p.found ? slots_[p.index].value : if_absent;
    }

    bool put(Key key, long long value) {
        const Probe p = probe(key);
        if (!p.found) {
            claim(p.index, key);
            slots_[p.index].value = value;
            return true;
        }
        slots_[p.index].value = value;
        return false;
    }

    long long add(Key key, long long delta) {
        const Probe p = probe(key);
        if (p.found) return slots_[p.index].value = add_checked(slots_[p.index].value, delta);
        claim(p.index, key);
        return slots_[p.index].value = delta;
    }

    /// Idempotent: release the storage.  Every later access throws std::logic_error.
    void close() noexcept {
        slots_.reset();
        capacity_ = max_entries_ = size_ = mask_ = 0;
    }

private:
    struct Slot {
        Key key;
        long long value;
    };
    struct AlignedDelete {
        void operator()(Slot* p) const noexcept { ::operator delete(p, std::align_val_t{64}); }
    };
    struct Probe {
        std::size_t index;
        bool found;
    };

    Probe probe(Key key) const {
        if (!slots_) throw std::logic_error("closed or moved-from");
        if (key == EMPTY || key == TOMB) throw std::invalid_argument("key must not be 0 or ~0");
        std::size_t i = static_cast<std::size_t>((key * GOLDEN) >> shift_);
        for (;;) {
            const Key k = slots_[i].key;
            if (k == key) return {i, true};
            if (k == EMPTY) return {i, false};
            i = (i + 1) & mask_;
        }
    }

    void claim(std::size_t i, Key key) {
        if (size_ == max_entries_) throw std::length_error("full: " + std::to_string(max_entries_) + " entries");
        slots_[i].key = key;
        ++size_;
    }

    std::unique_ptr<Slot[], AlignedDelete> slots_;
    std::size_t capacity_ = 0, max_entries_ = 0, size_ = 0, mask_ = 0;
    int shift_ = 0;
};

}  // namespace tickers
