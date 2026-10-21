// hc08 · Order sequence API — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Part 1: get the semantics right (a std::vector scan is fine).  Part 2: Fenwick trees make count / quantity / id_at O(log n).
// Part 3: partial removal + compaction of the index space.
#pragma once

#include <cstddef>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
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

// ------------------------------------------------------------------------------------------------ the sequence (to write)
/// Live orders in insertion order.
/// Hint for Part 2: give every order an ever-increasing insertion index 1..capacity; removal only zeroes it (a hole).  Two Fenwick
/// trees over the indices: the number of live orders and the remaining quantity.  Index lookup by id: std::unordered_map
/// (find, never operator[]; rehash / reserve it).  std::hash<long long> is the identity function and libc++ may use power-of-two
/// bucket counts: ids that differ only in their high bits can all collide, so supply your own mixing hash.
class OrderSequence {
public:
    OrderSequence() : OrderSequence(16) {}

    /// Index space rounded up to a power of two (std::bit_ceil); <= 0 -> std::invalid_argument.
    explicit OrderSequence(int) { throw std::logic_error("TODO"); }

    /// Append at the end.  qty <= 0 / id already live -> std::invalid_argument; the live total would exceed LLONG_MAX -> std::overflow_error.
    /// A failing put must leave the object unchanged.
    void put(long long, long long) { throw std::logic_error("TODO"); }

    /// Remove qty units from an order; returns what is left (0 = the order is gone).  The position never changes.
    /// qty <= 0 -> invalid_argument; unknown id -> UnknownId; qty > left -> invalid_argument (state unchanged).
    /// Part 1-2 only remove whole orders; partial removal is tested in Part 3.  (`delete` is a C++ keyword.)
    long long remove(long long, long long) { throw std::logic_error("TODO"); }

    /// Live orders from the head up to and including this one.  Unknown id -> UnknownId.
    long long count_up_to(long long) const { throw std::logic_error("TODO"); }
    /// Remaining quantity over the same range.
    long long qty_up_to(long long) const { throw std::logic_error("TODO"); }
    /// Id of the k-th live order (1-based); out of range -> std::out_of_range.  Part 2: binary descent on the Fenwick tree.
    long long id_at(int) const { throw std::logic_error("TODO"); }

    std::size_t size() const { throw std::logic_error("TODO"); }
    long long total_qty() const { throw std::logic_error("TODO"); }

    /// Part 3: size of the index space (a power of two) and how many compactions happened.  A naive Part 1 may return anything.
    int capacity() const { throw std::logic_error("TODO"); }
    int compactions() const { throw std::logic_error("TODO"); }
    /// Part 3 (C++): bucket count of the id -> index map.  unordered_map keeps its bucket array until you rehash.
    std::size_t index_buckets() const { throw std::logic_error("TODO"); }

    /// All live orders in insertion order.
    std::vector<Entry> entries() const { throw std::logic_error("TODO"); }

    // ---- text interface
    /// PUT id qty | DELETE id qty | COUNT id | QTY id | AT k (case-insensitive, any whitespace).  Bad format -> std::invalid_argument.
    /// Hint: std::from_chars succeeds on a valid prefix ("12abc"): check the end pointer; it rejects '+'.
    static Op parse(std::string_view) { throw std::logic_error("TODO"); }

    /// Execute one command; business errors (invalid_argument, UnknownId, out_of_range, overflow_error) become Err(message).
    /// Do not catch std::exception: std::bad_alloc must still propagate.
    Result apply(const Op&) { throw std::logic_error("TODO"); }

    /// Ok -> "OK", Num(v) -> "v", Err(m) -> "ERR m".
    static std::string render(const Result&) { throw std::logic_error("TODO"); }

    /// Run a script (blank lines and '#' lines skipped).  Malformed line -> std::invalid_argument starting with "line N" (1-based).
    static std::vector<std::string> replay(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

private:
    // your fields here
};

}  // namespace oseq
