// hc15 · Streaming median — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: nearest_rank and the heap aliases.  To write: everything marked TODO (add your own members to each class).
#pragma once

#include <algorithm>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <queue>
#include <stdexcept>
#include <unordered_map>
#include <vector>

namespace median {

inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow");
    return r;
}

/// Max-heap of the smaller half, min-heap of the larger half.
using MaxHeap = std::priority_queue<long long>;
using MinHeap = std::priority_queue<long long, std::vector<long long>, std::greater<>>;

/// Nearest rank: the p-th percentile of n values is the ceil(p * n / 100)-th smallest.  n >= 0, 1 <= p <= 100,
/// else std::invalid_argument.  Given.  Never overflows: split n into n / 100 and n % 100 instead of computing p * n.
inline long long nearest_rank(long long n, int p) {
    if (n < 0) throw std::invalid_argument("n must be >= 0");
    if (p < 1 || p > 100) throw std::invalid_argument("p must be in 1..100");
    return n / 100 * p + ((n % 100) * p + 99) / 100;
}

// ============================================================================================ Part 1
/// Lower median (the ceil(n/2)-th smallest) of everything added so far.
/// Hint: lo = smaller half (max-heap), hi = larger half (min-heap); every value in lo <= every value in hi,
/// and lo.size() == hi.size() or hi.size() + 1.
class StreamingMedian {
public:
    /// O(log n).
    void add(long long) { throw std::logic_error("TODO"); }
    /// O(1).  std::out_of_range if empty.
    long long median() const { throw std::logic_error("TODO"); }
    /// 2 x the true median: the sum of the two middle values (the one middle value twice if n is odd).
    /// std::overflow_error if that does not fit; std::out_of_range if empty.
    long long doubled_median() const { throw std::logic_error("TODO"); }
    std::size_t size() const noexcept { return 0; }

private:
    // your members here
};

// ============================================================================================ Part 2
/// Lower median of the last k prices.
/// Hint: a heap cannot erase an arbitrary element.  Lazy deletion: record the price that leaves the window in a
/// "delayed" table and pop it only when it reaches the top.  Balance by the number of valid elements, not by
/// heap.size(); keep both tops valid after every add.  A price leaving the window belongs to lo iff old <= lo.top().
class WindowMedian {
public:
    /// k >= 1, else std::invalid_argument.
    explicit WindowMedian(int) { throw std::logic_error("TODO"); }
    /// Amortised O(log k).
    void add(long long) { throw std::logic_error("TODO"); }
    /// std::out_of_range if nothing was added yet.
    long long median() const { throw std::logic_error("TODO"); }
    /// min(adds so far, k).
    std::size_t size() const noexcept { return 0; }
    /// Entries physically held by the two heaps, stale ones included.  Must stay <= 4k however long the stream is.
    /// Hint: on an ascending stream stale entries sink to the bottom of lo and never surface; rebuild when they pile up.
    std::size_t retained() const noexcept { return 0; }
    /// result[i] = median() after adding prices[0..i].
    static std::vector<long long> slide(const std::vector<long long>&, int) { throw std::logic_error("TODO"); }

private:
    // your members here
};

// ============================================================================================ Part 3a
/// Fixed percentile p by two heaps: lo = the nearest_rank(n, p) smallest values, hi = the rest.
class TwoHeapPercentile {
public:
    /// 1 <= p <= 100, else std::invalid_argument.
    explicit TwoHeapPercentile(int) { throw std::logic_error("TODO"); }
    /// O(log n).
    void add(long long) { throw std::logic_error("TODO"); }
    /// O(1).  std::out_of_range if empty.
    long long value() const { throw std::logic_error("TODO"); }
    long long size() const noexcept { return 0; }

private:
    // your members here
};

// ============================================================================================ Part 3b
/// Order-statistics structure: any p at query time.
/// Hint: a balanced BST ordered by value where every node also stores its subtree's element count; the k-th smallest is
/// one walk from the root.  std::set / std::map cannot answer "k-th" in O(log n).  Write a treap (BST by value + heap
/// by random priority, expected height O(log n)), merge equal values into one node with a count, and keep the nodes in
/// vectors (indices, not pointers).  Trap: a reference into a vector dangles when a recursive insert grows it.
class OrderStatistics {
public:
    static long long rank(long long n, int p) { return nearest_rank(n, p); }
    /// Expected O(log n).
    void add(long long) { throw std::logic_error("TODO"); }
    int size() const noexcept { return 0; }
    /// 1-based, duplicates count separately.  std::invalid_argument if rank is not in 1..size().
    long long kth(long long) const { throw std::logic_error("TODO"); }
    /// p outside 1..100 -> std::invalid_argument (checked first); empty -> std::out_of_range.
    long long percentile(int) const { throw std::logic_error("TODO"); }
    /// Number of values <= price.
    long long count_at_most(long long) const { throw std::logic_error("TODO"); }

private:
    // your members here
};

// ============================================================================================ Part 4
/// Prices 0..max_tick-1.  add and percentile are O(log T) and nothing is allocated after the constructor.
/// Hint: counts in a Fenwick tree; the k-th smallest by binary lifting: from the highest power of two down, skip a whole
/// block when tree[pos + step] < r and subtract it from r.
class TickHistogram {
public:
    static constexpr int MAX_TICKS = 1 << 22;

    /// 1 <= max_tick <= MAX_TICKS, else std::invalid_argument.
    explicit TickHistogram(int) { throw std::logic_error("TODO"); }
    /// price outside 0..max_tick-1 -> std::invalid_argument.
    void add(long long) { throw std::logic_error("TODO"); }
    long long count() const noexcept { return 0; }
    /// Values <= price; price < 0 -> 0, price >= max_tick -> count().
    long long count_at_most(long long) const { throw std::logic_error("TODO"); }
    /// 1-based k-th smallest price; rank outside 1..count() -> std::invalid_argument.
    long long kth(long long) const { throw std::logic_error("TODO"); }
    /// Same contract as OrderStatistics::percentile.
    long long percentile(int) const { throw std::logic_error("TODO"); }
    long long median() const { throw std::logic_error("TODO"); }

private:
    // your members here
};

}  // namespace median
