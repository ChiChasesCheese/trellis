// hc11 · Order interval overlap — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
// Given: value types (Side, Peak, Interval, Place, Cancel, OrderEvent, Report).  To write: everything marked TODO.
#pragma once

#include <algorithm>
#include <array>
#include <climits>
#include <iterator>
#include <cstddef>
#include <map>
#include <span>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace overlap {

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

// ============================================================================================ value types
enum class Side : unsigned char { Buy, Sell };

/// Largest number of simultaneously live orders and the EARLIEST time it is reached.  (0, 0) when nothing was ever live.
struct Peak {
    int count;
    long long time;
    friend bool operator==(const Peak&, const Peak&) = default;
};

/// A half-open lifetime [start, end).  No subtraction anywhere: times may be close to LLONG_MAX.
struct Interval {
    long long start, end;
    friend bool operator==(const Interval&, const Interval&) = default;
};

/// Place: planned lifetime [start, end).  end == start is legal (never live).
struct Place {
    long long id;
    Side side;
    long long start, end;
    Place(long long id, Side side, long long start, long long end) : id(id), side(side), start(start), end(end) {
        if (side != Side::Buy && side != Side::Sell) throw std::invalid_argument("invalid side");  // an enum can hold any value of its type
        if (start < 0) throw std::invalid_argument("negative start: " + std::to_string(start));
        if (end < start) throw std::invalid_argument("end < start: " + std::to_string(end) + " < " + std::to_string(start));
    }
    friend bool operator==(const Place&, const Place&) = default;
};

/// Cancel: from `time` on the order is no longer live (its interval becomes [start, min(end, time))).
struct Cancel {
    long long id;
    long long time;
    Cancel(long long id, long long time) : id(id), time(time) {
        if (time < 0) throw std::invalid_argument("negative time: " + std::to_string(time));
    }
    friend bool operator==(const Cancel&, const Cancel&) = default;
};

/// Closed hierarchy of events: std::visit with `overloaded` does not compile if a case is missing.
using OrderEvent = std::variant<Place, Cancel>;

struct Report {
    Peak buy, sell, all;
    friend bool operator==(const Report&, const Report&) = default;
};

// ============================================================================================ Part 1
/// Peak of simultaneously live orders for half-open [start, end): count and the EARLIEST time it is reached.  Input may be
/// unsorted with duplicates; start == end is ignored; start < 0 or end < start -> std::invalid_argument; nothing live -> {0, 0}.
/// Hints: sort all starts and all ends separately and walk them with two indices; at the same time an end comes BEFORE a
/// start ([1,3) and [3,5) do not overlap); never compute end - start or end + 1 (times may be near LLONG_MAX).
inline Peak peak(std::span<const Interval>) { throw std::logic_error("TODO"); }
inline int max_overlap(std::span<const Interval>) { throw std::logic_error("TODO"); }
/// Closed [start, end]: [1,3] and [3,5] overlap at 3; [5,5] is one live point.
inline int max_overlap_inclusive(std::span<const Interval>) { throw std::logic_error("TODO"); }

/// Variant two: ONE sorted vector of events.  The tie rule can live in the order of the variant's alternatives
/// (Close = index 0 sorts before Open = index 1 at the same time).  Sort with a strict weak order: `<`, never `<=`.
struct Close { long long time; };
struct Open { long long time; };
using SweepEvent = std::variant<Close, Open>;
inline Peak peak_events(std::span<const Interval>) { throw std::logic_error("TODO"); }

/// Variant three: difference array in a std::map<long long, int> (+1 at start, -1 at end), walked in key order.
inline Peak peak_diff_map(std::span<const Interval>) { throw std::logic_error("TODO"); }

// ============================================================================================ Part 2
/// Buy / sell / all peaks of a batch of Place and Cancel events in any order.  Effective interval of an order is
/// [start, min(end, earliest cancel)); a cancel at or before start means it never lived.  Cancel of an unknown id or two
/// Places with the same id -> std::invalid_argument.  Hint: std::visit(overloaded{...}, event).
inline Report analyze(std::span<const OrderEvent>) { throw std::logic_error("TODO"); }

// ============================================================================================ Part 3
/// Online: events arrive in time order (equal timestamps allowed); every call O(log n).
/// Hints: per lane (buy, sell, all) a std::map of future ends (planned end -> count), a std::map step function of settled
/// live counts (upper_bound + prev answers live_at), the current live count and a committed maximum.  Events with the same
/// timestamp are one batch: the maximum is committed only when the clock moves past that timestamp, and peak() also considers
/// the still-open current one.  Do not use operator[] in a const read path (it inserts).
class OnlineOverlap {
public:
    /// start earlier than the last event, duplicate id, end < start, negative start or invalid side -> std::invalid_argument.
    void place(long long, Side, long long, long long) { throw std::logic_error("TODO"); }
    /// true if it shortened a live order; false if already ended or cancelled; unknown id or time going back -> invalid_argument.
    bool cancel(long long, long long) { throw std::logic_error("TODO"); }
    /// Place -> true; Cancel -> cancel()'s result.
    bool apply(const OrderEvent&) { throw std::logic_error("TODO"); }
    /// Move the clock; going back -> invalid_argument.
    void advance_to(long long) { throw std::logic_error("TODO"); }
    long long now() const { throw std::logic_error("TODO"); }
    int live_now() const { throw std::logic_error("TODO"); }
    int live_now(Side) const { throw std::logic_error("TODO"); }
    /// 0 <= t <= now, else invalid_argument.
    int live_at(long long) const { throw std::logic_error("TODO"); }
    int live_at(Side, long long) const { throw std::logic_error("TODO"); }
    Peak peak() const { throw std::logic_error("TODO"); }
    Peak peak(Side) const { throw std::logic_error("TODO"); }
    int max_so_far() const { throw std::logic_error("TODO"); }
    int max_so_far(Side) const { throw std::logic_error("TODO"); }
    /// Number of recorded steps over all lanes; reads must never add one.
    std::size_t history_size() const { throw std::logic_error("TODO"); }
};

// ============================================================================================ Part 4
/// Coordinate compression + lazy segment tree (range add, range max) on std::vector<int>.
/// Hints: sorted unique endpoints c[0] < ... < c[m-1]; [c[j], c[j+1]) is an elementary segment; [s, e) covers idx(s)..idx(e)-1;
/// binary search with std::lower_bound / std::upper_bound (comparisons only, no subtraction).
class IntervalIndex {
public:
    /// Every endpoint that will ever be used (any order, duplicates allowed).
    explicit IntervalIndex(std::span<const long long>) { throw std::logic_error("TODO"); }
    /// Collect endpoints, compress, add each interval.
    static IntervalIndex of(std::span<const Interval>) { throw std::logic_error("TODO"); }
    /// Part 1's answer via compression + segment tree; must equal the sweep.
    static int max_overlap(std::span<const Interval>) { throw std::logic_error("TODO"); }

    /// Both ends must be known endpoints (else invalid_argument); end < start -> invalid_argument; start == end does nothing.
    void add(long long, long long) { throw std::logic_error("TODO"); }
    void remove(long long, long long) { throw std::logic_error("TODO"); }
    int max() const { throw std::logic_error("TODO"); }
    /// Live count at t; 0 outside all endpoints; right end exclusive.
    int live_at(long long) const { throw std::logic_error("TODO"); }
    /// Max live count at any time in [from, to).  to < from -> invalid_argument; to == from -> 0.
    int max_in(long long, long long) const { throw std::logic_error("TODO"); }
    int coordinate_count() const { throw std::logic_error("TODO"); }
    int segment_count() const { throw std::logic_error("TODO"); }
};

}  // namespace overlap
