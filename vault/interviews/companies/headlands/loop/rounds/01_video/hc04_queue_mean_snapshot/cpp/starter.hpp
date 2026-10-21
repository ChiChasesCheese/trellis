// hc04 · Queue mean + corrective snapshot — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <atomic>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <stdexcept>
#include <string>
#include <thread>
#include <variant>
#include <vector>

namespace qmean {

using i128 = __int128;
using u128 = unsigned __int128;

/// Decimal text of an __int128 (given; libc++ has no operator<< for it).
inline std::string i128_to_string(i128 v) {
    const bool neg = v < 0;
    u128 m = neg ? u128{0} - static_cast<u128>(v) : static_cast<u128>(v);
    std::string s;
    do { s.push_back(static_cast<char>('0' + static_cast<int>(m % 10))); m /= 10; } while (m != 0);
    if (neg) s.push_back('-');
    return {s.rbegin(), s.rend()};
}

// ------------------------------------------------------------------------------------------------ Mean
/// Exact mean: reduced fraction, denominator > 0, sign on the numerator.  The constructor must throw
/// std::invalid_argument for d <= 0 and reduce by the gcd (gcd(0, d) = d, so zero is 0/1).
/// Hint: std::gcd on __int128 is not portable; write the Euclid loop on unsigned __int128.
struct Mean {
    i128 numerator;
    long long denominator;
    Mean(i128, long long) : numerator(0), denominator(1) { throw std::logic_error("TODO"); }
    /// The double nearest to numerator/denominator.  Hint: if both fit in 53 bits one division is exact-rounded;
    /// otherwise build a 54-bit quotient by long division, keep a sticky bit, round half to even once.
    double to_double() const { throw std::logic_error("TODO"); }
    friend bool operator==(const Mean&, const Mean&) = default;
};

// ------------------------------------------------------------------------------------------------ Part 1
/// FIFO of long long: O(1) push / pop / mean, exact, no overflow.  Empty pop/mean -> std::out_of_range.
/// Hints: ring buffer with power-of-two capacity (grow in LOGICAL order), __int128 sum, and think about what the
/// compiler-generated move constructor does to head_/size_/sum_ of the moved-from object.
class QueueMean {
public:
    void push(long long) { throw std::logic_error("TODO"); }
    long long pop() { throw std::logic_error("TODO"); }
    std::size_t size() const { throw std::logic_error("TODO"); }
    bool empty() const { throw std::logic_error("TODO"); }
    i128 sum() const { throw std::logic_error("TODO"); }
    Mean mean() const { throw std::logic_error("TODO"); }
    double get_mean() const { throw std::logic_error("TODO"); }
};

// ------------------------------------------------------------------------------------------------ Part 2 (types given)
struct Push { long long value; friend bool operator==(const Push&, const Push&) = default; };
struct Pop { friend bool operator==(const Pop&, const Pop&) = default; };
struct Query { friend bool operator==(const Query&, const Query&) = default; };
/// Corrective snapshot: forget the history so far; the queue becomes `contents` (front first).
struct Correct { std::vector<long long> contents; friend bool operator==(const Correct&, const Correct&) = default; };
using Event = std::variant<Push, Pop, Query, Correct>;

struct Value { Mean mean; friend bool operator==(const Value&, const Value&) = default; };
struct Empty { friend bool operator==(const Empty&, const Empty&) = default; };
using Answer = std::variant<Value, Empty>;

/// Apply the events; each Query yields one Answer.  Pop on an empty queue -> std::out_of_range.  Hint: std::visit.
inline std::vector<Answer> run(const std::vector<Event>&) { throw std::logic_error("TODO"); }

/// push N | pop | mean | snapshot [N ...]; blank lines ignored; errors std::invalid_argument("line k: ...") (k from 1).
/// Hint: std::from_chars, and check that the whole token was consumed.
inline std::vector<Event> parse(const std::vector<std::string>&) { throw std::logic_error("TODO"); }

/// "7", "-7/2" or "empty".
inline std::string render(const Answer&) { throw std::logic_error("TODO"); }

inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    std::vector<std::string> out;
    for (const Answer& a : run(parse(lines))) out.push_back(render(a));
    return out;
}

// ------------------------------------------------------------------------------------------------ Part 3
/// Persistent queue: every operation returns a NEW version number; old versions never change.  O(log n) per operation,
/// no per-version copy of the contents.  Unknown version -> std::invalid_argument; pop/mean of an empty version -> std::out_of_range.
/// Hint: the pushed values form a tree; a version is (tail node, popped count, sum).  pop needs a level-ancestor query.
/// Careful: push_back on a vector invalidates references into it.
class VersionedQueue {
public:
    static constexpr int EMPTY = 0;
    int push(int, long long) { throw std::logic_error("TODO"); }
    int pop(int) { throw std::logic_error("TODO"); }
    int correct(const std::vector<long long>&) { throw std::logic_error("TODO"); }
    std::size_t size(int) const { throw std::logic_error("TODO"); }
    Mean mean(int) const { throw std::logic_error("TODO"); }
    std::vector<long long> contents(int) const { throw std::logic_error("TODO"); }
};

// ------------------------------------------------------------------------------------------------ Part 4
struct SingleWriterViolation : std::logic_error {
    using std::logic_error::logic_error;
};

struct Stat {
    std::uint64_t seq;  // modification count, starts at 0
    std::size_t size;
    i128 sum;
    std::optional<Mean> mean() const { throw std::logic_error("TODO"); }
    friend bool operator==(const Stat&, const Stat&) = default;
};

/// The first thread to push/pop becomes the only writer (another one -> SingleWriterViolation).  Any thread may call
/// read(): lock-free, never blocks the writer, never sees a torn (sum from one instant, size from another) state.
/// Hint: a seqlock (odd/even version counter, relaxed-atomic fields, acquire/release fences) or an atomically
/// published immutable snapshot.  Plain fields read during a write are a data race = UB.
class SharedMean {
public:
    void push(long long) { throw std::logic_error("TODO"); }
    long long pop() { throw std::logic_error("TODO"); }
    Stat read() const { throw std::logic_error("TODO"); }
    std::optional<Mean> mean() const { return read().mean(); }
};

}  // namespace qmean
