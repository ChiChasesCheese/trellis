// hc08 · Order sequence API — C++20 reference.  Statement: ../problem.md (Java: reference/OrderSequence.java).
// Parts: 1 semantics + text interface, 2 Fenwick trees (prefix count / quantity / k-th id in O(log n)),
//        3 partial removal + compaction of the index space (memory follows the live orders, not the history).
#pragma once

#include <algorithm>
#include <bit>
#include <charconv>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>
#include <system_error>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace oseq {

// ------------------------------------------------------------------------------------------------ messages and errors
inline constexpr std::string_view INVALID_QTY = "invalid quantity";
inline constexpr std::string_view DUPLICATE_ID = "duplicate id";
inline constexpr std::string_view UNKNOWN_ID = "unknown id";
inline constexpr std::string_view QTY_EXCEEDS = "quantity exceeds remaining";
inline constexpr std::string_view INDEX_RANGE = "index out of range";
inline constexpr std::string_view SUM_OVERFLOW = "overflow";  // not OVERFLOW: <math.h> defines that macro on some platforms

/// Java NoSuchElementException.  The other mappings: IllegalArgumentException -> std::invalid_argument,
/// IndexOutOfBoundsException -> std::out_of_range, ArithmeticException -> std::overflow_error.
struct UnknownId : std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct Entry {
    long long id;
    long long qty;
    friend bool operator==(const Entry&, const Entry&) = default;
};

// ------------------------------------------------------------------------------------------------ text commands
struct Put { long long id; long long qty; friend bool operator==(const Put&, const Put&) = default; };
struct Delete { long long id; long long qty; friend bool operator==(const Delete&, const Delete&) = default; };
struct CountUpTo { long long id; friend bool operator==(const CountUpTo&, const CountUpTo&) = default; };
struct QtyUpTo { long long id; friend bool operator==(const QtyUpTo&, const QtyUpTo&) = default; };
struct IdAt { int k; friend bool operator==(const IdAt&, const IdAt&) = default; };
using Op = std::variant<Put, Delete, CountUpTo, QtyUpTo, IdAt>;

struct Ok { friend bool operator==(const Ok&, const Ok&) = default; };
struct Num { long long value; friend bool operator==(const Num&, const Num&) = default; };
struct Err { std::string message; friend bool operator==(const Err&, const Err&) = default; };
using Result = std::variant<Ok, Num, Err>;

namespace detail {
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
constexpr bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }
constexpr char to_upper(char c) { return c >= 'a' && c <= 'z' ? static_cast<char>(c - 'a' + 'A') : c; }
inline std::string_view strip(std::string_view s) {
    while (!s.empty() && is_space(s.front())) s.remove_prefix(1);
    while (!s.empty() && is_space(s.back())) s.remove_suffix(1);
    return s;
}
inline std::vector<std::string_view> split_words(std::string_view s) {
    std::vector<std::string_view> out;
    std::size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && is_space(s[i])) ++i;
        const std::size_t start = i;
        while (i < s.size() && !is_space(s[i])) ++i;
        if (i > start) out.push_back(s.substr(start, i - start));
    }
    return out;
}
/// std::hash<long long> is the identity function.  libc++ keeps a power-of-two bucket count when it is asked for one (and maps
/// hash & mask), so ids that differ only in the high bits (i << 32) would all share bucket 0 and every lookup becomes a linear scan.
/// splitmix64's finaliser spreads every input bit over all output bits.
struct IdHash {
    std::size_t operator()(long long id) const noexcept {
        auto x = static_cast<std::uint64_t>(id);
        x ^= x >> 30; x *= 0xBF58476D1CE4E5B9ull;
        x ^= x >> 27; x *= 0x94D049BB133111EBull;
        x ^= x >> 31;
        return static_cast<std::size_t>(x);
    }
};
/// std::from_chars succeeds on a valid prefix ("12abc" -> 12): the end pointer must be the end of the token.  It also rejects '+'.
template <class T> T parse_number(std::string_view tok, std::string_view line) {
    T v{};
    const auto [end, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), v);
    if (ec != std::errc{} || end != tok.data() + tok.size()) throw std::invalid_argument("bad number in: " + std::string(line));
    return v;
}
inline void expect_args(const std::vector<std::string_view>& t, std::size_t n) {
    if (t.size() != n) throw std::invalid_argument(std::string(t[0]) + " expects " + std::to_string(n - 1) + " arguments");
}
}  // namespace detail

// ------------------------------------------------------------------------------------------------ the sequence
/// Live orders in insertion order.  Every order owns an ever-increasing "insertion index" 1..capacity; removal only zeroes it
/// (leaves a hole).  Two Fenwick trees over that index space: cnt_ (number of live orders) and sum_ (remaining quantity).
/// When the index space is full, compact(): renumber the live orders 1..m in their original order.
class OrderSequence {
public:
    OrderSequence() : OrderSequence(16) {}

    /// Index space rounded up to a power of two; compaction never goes below it.  <= 0 or > 2^29 -> std::invalid_argument.
    explicit OrderSequence(int initial_capacity) {
        if (initial_capacity < 1 || initial_capacity > (1 << 29)) throw std::invalid_argument("capacity out of range");
        min_capacity_ = static_cast<int>(std::bit_ceil(static_cast<unsigned>(initial_capacity)));  // bit_ceil(x) is UB when the result is not representable: the range check came first
        allocate(min_capacity_);
        index_of_.rehash(static_cast<std::size_t>(min_capacity_));  // enough buckets for a full index space: puts never rehash
    }

    OrderSequence(const OrderSequence&) = default;
    OrderSequence& operator=(const OrderSequence&) = default;
    // The generated move would move the vectors but COPY capacity_, next_index_ and the counters: the moved-from object
    // would claim a full index space and then index into empty vectors.  Moved-from = valid, empty, capacity 0 (the first put
    // finds next_index_ > capacity_ and compacts into a fresh min_capacity_ space).
    OrderSequence(OrderSequence&& o) noexcept
        : min_capacity_(o.min_capacity_),
          capacity_(std::exchange(o.capacity_, 0)),
          cnt_(std::move(o.cnt_)),
          sum_(std::move(o.sum_)),
          id_by_idx_(std::move(o.id_by_idx_)),
          qty_by_idx_(std::move(o.qty_by_idx_)),
          next_index_(std::exchange(o.next_index_, 1)),
          index_of_(std::move(o.index_of_)),
          total_qty_(std::exchange(o.total_qty_, 0)),
          compactions_(std::exchange(o.compactions_, 0)) {
        o.reset_containers();
    }
    OrderSequence& operator=(OrderSequence&& o) noexcept {
        if (this != &o) {
            min_capacity_ = o.min_capacity_;
            capacity_ = std::exchange(o.capacity_, 0);
            cnt_ = std::move(o.cnt_);
            sum_ = std::move(o.sum_);
            id_by_idx_ = std::move(o.id_by_idx_);
            qty_by_idx_ = std::move(o.qty_by_idx_);
            next_index_ = std::exchange(o.next_index_, 1);
            index_of_ = std::move(o.index_of_);
            total_qty_ = std::exchange(o.total_qty_, 0);
            compactions_ = std::exchange(o.compactions_, 0);
            o.reset_containers();
        }
        return *this;
    }

    /// Append at the end.  qty <= 0 / id live -> invalid_argument; the total would exceed LLONG_MAX -> overflow_error.
    /// Every check that can throw comes before the first mutation, so a failed put changes nothing (not even the compaction count).
    void put(long long id, long long qty) {
        if (qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        if (index_of_.contains(id)) throw std::invalid_argument(std::string(DUPLICATE_ID));
        long long new_total;
        if (__builtin_add_overflow(total_qty_, qty, &new_total)) throw std::overflow_error(std::string(SUM_OVERFLOW));
        if (next_index_ > capacity_) compact();  // behaviour-preserving, so it is fine that it happens before the insert below
        const int i = next_index_;
        index_of_.try_emplace(id, i);  // the only remaining call that can throw (bad_alloc); nothing else has changed yet
        ++next_index_;
        id_by_idx_[idx(i)] = id;
        qty_by_idx_[idx(i)] = qty;
        add_cnt(i, 1);
        add_sum(i, qty);
        total_qty_ = new_total;
    }

    /// Remove qty units from an order; returns what is left (0 = the order is gone).  The position never changes.
    /// (`delete` is a C++ keyword, hence the name.)  qty <= 0 -> invalid_argument; unknown id -> UnknownId; qty > left -> invalid_argument.
    long long remove(long long id, long long qty) {
        if (qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        const int i = index_or_throw(id);
        const long long have = qty_by_idx_[idx(i)];
        if (qty > have) throw std::invalid_argument(std::string(QTY_EXCEEDS));
        const long long left = have - qty;
        qty_by_idx_[idx(i)] = left;
        add_sum(i, -qty);  // qty > 0, so -qty cannot be LLONG_MIN
        total_qty_ -= qty;
        if (left == 0) {
            add_cnt(i, -1);
            index_of_.erase(id);
        }
        return left;
    }

    /// Live orders from the head up to and including this one.
    long long count_up_to(long long id) const { return prefix_cnt(index_or_throw(id)); }
    /// Remaining quantity over the same range.
    long long qty_up_to(long long id) const { return prefix_sum(index_or_throw(id)); }

    /// Id of the k-th live order (1-based).  O(log n) binary descent on the cnt_ tree: tree[pos + 2^j] covers (pos, pos + 2^j].
    long long id_at(int k) const {
        if (k < 1 || static_cast<std::size_t>(k) > index_of_.size()) throw std::out_of_range(std::string(INDEX_RANGE));  // k < 1 first: a negative k would convert to a huge size_t
        int pos = 0, rem = k;
        for (int pw = capacity_; pw > 0; pw >>= 1) {
            const int nxt = pos + pw;
            if (nxt <= capacity_ && cnt_[idx(nxt)] < rem) {
                pos = nxt;
                rem -= cnt_[idx(nxt)];
            }
        }
        return id_by_idx_[idx(pos + 1)];
    }

    std::size_t size() const { return index_of_.size(); }
    long long total_qty() const { return total_qty_; }
    int capacity() const { return capacity_; }
    int compactions() const { return compactions_; }
    /// Bucket count of the id -> index hash map (unordered_map never gives bucket memory back by itself; compaction rehashes it).
    std::size_t index_buckets() const { return index_of_.bucket_count(); }

    /// All live orders in insertion order.  O(capacity).
    std::vector<Entry> entries() const {
        std::vector<Entry> out;
        out.reserve(index_of_.size());
        for (int i = 1; i < next_index_; ++i)
            if (qty_by_idx_[idx(i)] > 0) out.push_back({id_by_idx_[idx(i)], qty_by_idx_[idx(i)]});
        return out;
    }

    // -------------------------------------------------------------------------------------------- text interface
    /// PUT id qty | DELETE id qty | COUNT id | QTY id | AT k (case-insensitive, any whitespace).  Bad format -> invalid_argument.
    static Op parse(std::string_view line) {
        const auto t = detail::split_words(line);
        if (t.empty()) throw std::invalid_argument("empty command");
        const std::string_view shown = detail::strip(line);
        std::string cmd(t[0]);
        for (char& c : cmd) c = detail::to_upper(c);
        if (cmd == "PUT" || cmd == "DELETE") {
            detail::expect_args(t, 3);
            const auto id = detail::parse_number<long long>(t[1], shown);
            const auto qty = detail::parse_number<long long>(t[2], shown);
            if (cmd == "PUT") return Put{id, qty};
            return Delete{id, qty};
        }
        if (cmd == "COUNT" || cmd == "QTY") {
            detail::expect_args(t, 2);
            const auto id = detail::parse_number<long long>(t[1], shown);
            if (cmd == "COUNT") return CountUpTo{id};
            return QtyUpTo{id};
        }
        if (cmd == "AT") {
            detail::expect_args(t, 2);
            return IdAt{detail::parse_number<int>(t[1], shown)};
        }
        throw std::invalid_argument("unknown command: " + std::string(t[0]));
    }

    /// Execute one command; business errors become Err, they do not escape.  Only the four expected exception types are caught:
    /// std::bad_alloc and friends must still propagate.
    Result apply(const Op& op) {
        try {
            return std::visit(detail::overloaded{[&](const Put& p) -> Result { put(p.id, p.qty); return Ok{}; },
                                                 [&](const Delete& d) -> Result { return Num{remove(d.id, d.qty)}; },
                                                 [&](const CountUpTo& c) -> Result { return Num{count_up_to(c.id)}; },
                                                 [&](const QtyUpTo& q) -> Result { return Num{qty_up_to(q.id)}; },
                                                 [&](const IdAt& a) -> Result { return Num{id_at(a.k)}; }},
                              op);
        } catch (const std::invalid_argument& e) {
            return Err{e.what()};
        } catch (const UnknownId& e) {
            return Err{e.what()};
        } catch (const std::out_of_range& e) {
            return Err{e.what()};
        } catch (const std::overflow_error& e) {
            return Err{e.what()};
        }
    }

    static std::string render(const Result& r) {
        return std::visit(detail::overloaded{[](const Ok&) { return std::string("OK"); },
                                             [](const Num& n) { return std::to_string(n.value); },
                                             [](const Err& e) { return "ERR " + e.message; }},
                          r);
    }

    /// Run a script (blank lines and '#' lines skipped).  A malformed line throws invalid_argument starting with "line N" (1-based).
    static std::vector<std::string> replay(const std::vector<std::string>& lines) {
        OrderSequence seq;
        std::vector<std::string> out;
        for (std::size_t i = 0; i < lines.size(); ++i) {
            const std::string_view line = detail::strip(lines[i]);
            if (line.empty() || line.front() == '#') continue;
            Op op;
            try {
                op = parse(line);
            } catch (const std::invalid_argument& e) {
                throw std::invalid_argument("line " + std::to_string(i + 1) + ": " + e.what());
            }
            out.push_back(render(seq.apply(op)));
        }
        return out;
    }

private:
    static std::size_t idx(int i) { return static_cast<std::size_t>(i); }

    void allocate(int cap) {
        capacity_ = cap;
        cnt_.assign(idx(cap) + 1, 0);
        sum_.assign(idx(cap) + 1, 0);
        id_by_idx_.assign(idx(cap) + 1, 0);
        qty_by_idx_.assign(idx(cap) + 1, 0);
    }

    void reset_containers() noexcept {
        cnt_.clear();
        sum_.clear();
        id_by_idx_.clear();
        qty_by_idx_.clear();
        index_of_.clear();  // a moved-from unordered_map is "valid but unspecified"
    }

    int index_or_throw(long long id) const {
        const auto it = index_of_.find(id);  // find, never operator[]: operator[] would INSERT the missing id
        if (it == index_of_.end()) throw UnknownId(std::string(UNKNOWN_ID));
        return it->second;
    }

    // i & -i is the lowest set bit of i.  tree[i] covers (i - lowbit(i), i]; update climbs with i += lowbit, query descends with i -= lowbit.
    // int is enough: capacity <= 2^29, so i + lowbit(i) <= 2^30 never overflows.
    void add_cnt(int i, int delta) {
        for (; i <= capacity_; i += i & -i) cnt_[idx(i)] += delta;
    }
    void add_sum(int i, long long delta) {
        for (; i <= capacity_; i += i & -i) sum_[idx(i)] += delta;
    }
    long long prefix_cnt(int i) const {
        long long r = 0;
        for (; i > 0; i -= i & -i) r += cnt_[idx(i)];
        return r;
    }
    long long prefix_sum(int i) const {
        long long r = 0;
        for (; i > 0; i -= i & -i) r += sum_[idx(i)];
        return r;
    }

    /// Renumber the live orders 1..m in order; new capacity = power of two >= max(min_capacity, 1.5m + 1), so at least ~m/2 slots are
    /// free afterwards (amortised O(1) per put) and the space shrinks back when few orders are live.
    /// Strong guarantee: all allocation happens first; the commit at the end cannot throw.
    void compact() {
        const int m = static_cast<int>(index_of_.size());
        const int new_cap = static_cast<int>(std::bit_ceil(static_cast<unsigned>(std::max(min_capacity_, m + (m >> 1) + 1))));
        std::vector<int> n_cnt(idx(new_cap) + 1, 0);
        std::vector<long long> n_sum(idx(new_cap) + 1, 0), n_id(idx(new_cap) + 1, 0), n_qty(idx(new_cap) + 1, 0);
        index_of_.rehash(static_cast<std::size_t>(new_cap));  // grows or SHRINKS the bucket array to follow the index space

        int j = 0;
        for (int i = 1; i < next_index_; ++i) {
            if (qty_by_idx_[idx(i)] == 0) continue;
            ++j;
            n_id[idx(j)] = id_by_idx_[idx(i)];
            n_qty[idx(j)] = qty_by_idx_[idx(i)];
            n_cnt[idx(j)] = 1;
            n_sum[idx(j)] = qty_by_idx_[idx(i)];
        }
        for (int i = 1; i <= new_cap; ++i) {  // linear Fenwick build: every node adds itself to its parent
            const int p = i + (i & -i);
            if (p <= new_cap) {
                n_cnt[idx(p)] += n_cnt[idx(i)];
                n_sum[idx(p)] += n_sum[idx(i)];
            }
        }
        for (int k = 1; k <= j; ++k) index_of_.find(n_id[idx(k)])->second = k;  // existing keys only: no allocation
        cnt_ = std::move(n_cnt);
        sum_ = std::move(n_sum);
        id_by_idx_ = std::move(n_id);
        qty_by_idx_ = std::move(n_qty);
        capacity_ = new_cap;
        next_index_ = j + 1;
        ++compactions_;
    }

    int min_capacity_ = 16;
    int capacity_ = 0;  // power of two (0 only in a moved-from object)
    std::vector<int> cnt_;       // Fenwick: live orders
    std::vector<long long> sum_;  // Fenwick: remaining quantity
    std::vector<long long> id_by_idx_;
    std::vector<long long> qty_by_idx_;  // 0 = hole
    int next_index_ = 1;                 // next free index; never reused until compaction
    std::unordered_map<long long, int, detail::IdHash> index_of_;
    long long total_qty_ = 0;
    int compactions_ = 0;
};

}  // namespace oseq
