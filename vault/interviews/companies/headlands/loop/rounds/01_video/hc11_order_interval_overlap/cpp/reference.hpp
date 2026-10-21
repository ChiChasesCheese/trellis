// hc11 · Order interval overlap — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 max overlap (sweep line: two sorted vectors / sorted variant events / std::map difference array),
//        2 analyze (buy / sell / all peaks, cancels, std::variant events), 3 OnlineOverlap (incremental),
//        4 IntervalIndex (coordinate compression + lazy segment tree on std::vector).
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
namespace detail {

/// Core of the two-vector sweep.  Sort all starts and all ends separately; for the i-th start (ascending), j counts the
/// ends that already happened.  Half-open: an end at or before s has happened (end first, then start, at the same time).
/// Closed: only an end strictly before s has happened.  live = (i + 1) - j.  A maximum can only appear at a start.
inline Peak peak_of(std::vector<long long> starts, std::vector<long long> ends, bool inclusive) {
    if (starts.empty()) return {0, 0};
    std::sort(starts.begin(), starts.end());
    std::sort(ends.begin(), ends.end());
    int best = 0;
    long long best_time = 0;
    std::size_t j = 0;
    for (std::size_t i = 0; i < starts.size(); ++i) {
        const long long s = starts[i];
        while (j < ends.size() && (inclusive ? ends[j] < s : ends[j] <= s)) ++j;
        const int live = static_cast<int>(i + 1 - j);
        if (live > best) {  // strictly greater: among equal maxima keep the earliest time
            best = live;
            best_time = s;
        }
    }
    return {best, best_time};
}

inline Peak sweep(std::span<const Interval> intervals, bool inclusive) {
    std::vector<long long> starts, ends;
    starts.reserve(intervals.size());
    ends.reserve(intervals.size());
    for (const Interval& iv : intervals) {
        if (iv.start < 0) throw std::invalid_argument("negative start: " + std::to_string(iv.start));
        if (iv.end < iv.start) throw std::invalid_argument("end < start: " + std::to_string(iv.end) + " < " + std::to_string(iv.start));
        if (!inclusive && iv.end == iv.start) continue;  // an empty half-open interval was never live
        starts.push_back(iv.start);
        ends.push_back(iv.end);
    }
    return peak_of(std::move(starts), std::move(ends), inclusive);
}

}  // namespace detail

/// Peak of simultaneously live orders for half-open [start, end).  Unsorted input and duplicates are fine.
inline Peak peak(std::span<const Interval> intervals) { return detail::sweep(intervals, false); }
inline int max_overlap(std::span<const Interval> intervals) { return peak(intervals).count; }
/// Closed [start, end]: [1,3] and [3,5] overlap at 3; [5,5] is a single live point.
inline int max_overlap_inclusive(std::span<const Interval> intervals) { return detail::sweep(intervals, true).count; }

/// Variant two: ONE vector of events, sorted by (time, kind).  The tie rule "end before start" is the alternative order
/// of the variant: Close is index 0, Open is index 1.
struct Close { long long time; };
struct Open { long long time; };
using SweepEvent = std::variant<Close, Open>;

inline Peak peak_events(std::span<const Interval> intervals) {
    std::vector<SweepEvent> events;
    events.reserve(intervals.size() * 2);
    for (const Interval& iv : intervals) {
        if (iv.start < 0) throw std::invalid_argument("negative start: " + std::to_string(iv.start));
        if (iv.end < iv.start) throw std::invalid_argument("end < start: " + std::to_string(iv.end) + " < " + std::to_string(iv.start));
        if (iv.end == iv.start) continue;
        events.emplace_back(Open{iv.start});
        events.emplace_back(Close{iv.end});
    }
    auto time_of = [](const SweepEvent& e) { return std::visit([](const auto& x) { return x.time; }, e); };
    std::sort(events.begin(), events.end(), [&](const SweepEvent& a, const SweepEvent& b) {
        return std::pair(time_of(a), a.index()) < std::pair(time_of(b), b.index());  // strict weak order: < never <=
    });
    int live = 0, best = 0;
    long long best_time = 0;
    for (const SweepEvent& e : events) {
        std::visit(overloaded{[&](const Close&) { --live; },
                              [&](const Open& o) {
                                  if (++live > best) { best = live; best_time = o.time; }
                              }},
                   e);
    }
    return {best, best_time};
}

/// Variant three: a difference array in an ordered map.  +1 at start, -1 at end; walking the keys in order and adding
/// the NET delta of each key makes the tie rule automatic: a +1 and a -1 on the same key cancel before anyone looks.
inline Peak peak_diff_map(std::span<const Interval> intervals) {
    std::map<long long, int> delta;
    for (const Interval& iv : intervals) {
        if (iv.start < 0) throw std::invalid_argument("negative start: " + std::to_string(iv.start));
        if (iv.end < iv.start) throw std::invalid_argument("end < start: " + std::to_string(iv.end) + " < " + std::to_string(iv.start));
        if (iv.end == iv.start) continue;
        ++delta[iv.start];
        --delta[iv.end];
    }
    int live = 0, best = 0;
    long long best_time = 0;
    for (const auto& [time, d] : delta) {
        live += d;
        if (live > best) { best = live; best_time = time; }
    }
    return {best, best_time};
}

// ============================================================================================ Part 2
/// Buy / sell / all peaks of a batch of Place and Cancel events (any order).  The effective interval of an order is
/// [start, min(end, earliest cancel)); a cancel at or before start means it never lived.
inline Report analyze(std::span<const OrderEvent> events) {
    std::unordered_map<long long, Place> places;
    std::unordered_map<long long, long long> cancel_at;
    for (const OrderEvent& e : events) {
        std::visit(overloaded{[&](const Place& p) {
                                  if (!places.emplace(p.id, p).second) throw std::invalid_argument("duplicate order id " + std::to_string(p.id));
                              },
                              [&](const Cancel& c) {
                                  auto [it, fresh] = cancel_at.try_emplace(c.id, c.time);
                                  if (!fresh) it->second = std::min(it->second, c.time);  // the earliest cancel wins
                              }},
                   e);
    }
    for (const auto& [id, time] : cancel_at) {
        (void)time;
        if (!places.contains(id)) throw std::invalid_argument("cancel of unknown order " + std::to_string(id));
    }
    std::vector<long long> buy_s, buy_e, sell_s, sell_e, all_s, all_e;
    for (const auto& [id, p] : places) {
        long long end = p.end;
        if (auto c = cancel_at.find(id); c != cancel_at.end()) end = std::min(end, c->second);
        if (end <= p.start) continue;  // empty, or cancelled before it began
        auto& s = p.side == Side::Buy ? buy_s : sell_s;
        auto& e = p.side == Side::Buy ? buy_e : sell_e;
        s.push_back(p.start);
        e.push_back(end);
        all_s.push_back(p.start);
        all_e.push_back(end);
    }
    return {detail::peak_of(std::move(buy_s), std::move(buy_e), false), detail::peak_of(std::move(sell_s), std::move(sell_e), false),
            detail::peak_of(std::move(all_s), std::move(all_e), false)};
}

// ============================================================================================ Part 3
/// Online version: events arrive in time order (equal timestamps allowed) and every call is O(log n).
///
/// Per lane (buy, sell, all) it keeps a difference array in two ordered maps:
///   expiries  future decrements: planned end time -> how many orders end then (begin() = the next end);
///   history   settled step function: time -> live count from that time on (upper_bound + prev answers "live at t").
/// Events with the same timestamp form one batch: place two orders, cancel one of them at the same instant, and that order's
/// interval is empty, so the instantaneous 2 must not become the maximum.  Hence a timestamp's value is committed to
/// the running maximum only when the clock moves past it; peak() also looks at the still-open current timestamp.
class OnlineOverlap {
public:
    /// Order at time `start` (not before the last event), planned to end at `end` (exclusive).
    void place(long long id, Side side, long long start, long long end) {
        (void)Place(id, side, start, end);  // validation only: non-negative, end >= start, valid enum
        if (start < now_) throw std::invalid_argument("event out of order: " + std::to_string(start) + " < " + std::to_string(now_));
        if (orders_.contains(id)) throw std::invalid_argument("duplicate order id " + std::to_string(id));
        advance_to(start);
        orders_.emplace(id, Order{side, start, end});
        if (end > start) {  // an empty interval changes no count
            Lane& lane = lane_of(side);
            lane.open(end);
            all_.open(end);
            lane.stamp();
            all_.stamp();
        }
    }

    /// Cancel at `time`: true if it really shortened a live order; false if it had already ended or been cancelled.
    bool cancel(long long id, long long time) {
        auto it = orders_.find(id);
        if (it == orders_.end()) throw std::invalid_argument("cancel of unknown order " + std::to_string(id));
        if (time < now_) throw std::invalid_argument("event out of order: " + std::to_string(time) + " < " + std::to_string(now_));
        advance_to(time);
        Order& o = it->second;
        const bool effective = o.end > time;  // start <= now == time, so end > time means still live
        if (effective) {
            Lane& lane = lane_of(o.side);
            lane.cancel(o.end);
            all_.cancel(o.end);
            lane.stamp();
            all_.stamp();
            o.end = time;  // a second cancel (or the planned end) now sees "already ended"
        }
        return effective;
    }

    /// Dispatch a variant event.  Place -> true; Cancel -> the result of cancel().
    bool apply(const OrderEvent& e) {
        return std::visit(overloaded{[&](const Place& p) {
                                         place(p.id, p.side, p.start, p.end);
                                         return true;
                                     },
                                     [&](const Cancel& c) { return cancel(c.id, c.time); }},
                          e);
    }

    /// Move the clock without an event so that orders ending by `t` leave the live count.
    void advance_to(long long t) {
        if (t < now_) throw std::invalid_argument("time went backwards: " + std::to_string(t) + " < " + std::to_string(now_));
        if (t > now_) {
            for (Lane& l : lanes_) l.advance(t);
            all_.advance(t);
            now_ = t;
        }
    }

    long long now() const { return now_; }
    int live_now() const { return all_.live; }
    int live_now(Side s) const { return lane_of(s).live; }
    /// Live count at time t (0 <= t <= now).  Looking ahead is not supported.
    int live_at(long long t) const { check_past(t); return all_.live_at(t); }
    int live_at(Side s, long long t) const { check_past(t); return lane_of(s).live_at(t); }
    /// Maximum so far (including the current timestamp) and its earliest time.
    Peak peak() const { return all_.peak(); }
    Peak peak(Side s) const { return lane_of(s).peak(); }
    int max_so_far() const { return peak().count; }
    int max_so_far(Side s) const { return peak(s).count; }
    /// Number of recorded steps (all lanes); a read must never add one.
    std::size_t history_size() const { return all_.history.size() + lanes_[0].history.size() + lanes_[1].history.size(); }

private:
    struct Order {
        Side side;
        long long start, end;
    };

    struct Lane {
        std::map<long long, int> expiries;
        std::map<long long, int> history;
        int live = 0;
        int committed_max = 0;  // best value over timestamps the clock has already passed
        long long committed_time = 0;
        long long last_tick = 0;

        /// Clock moves from last_tick to `to` (> last_tick): commit last_tick's final value, fold in the ends <= to.
        void advance(long long to) {
            if (live > committed_max) { committed_max = live; committed_time = last_tick; }
            while (!expiries.empty() && expiries.begin()->first <= to) {
                auto node = expiries.extract(expiries.begin());
                live -= node.mapped();
                history.insert_or_assign(node.key(), live);  // the step down happens at the end time
            }
            last_tick = to;
        }
        void open(long long end) { ++live; ++expiries[end]; }
        void cancel(long long end) {
            --live;
            auto it = expiries.find(end);
            if (--it->second == 0) expiries.erase(it);
        }
        void stamp() { history.insert_or_assign(last_tick, live); }
        int live_at(long long t) const {
            auto it = history.upper_bound(t);  // first step strictly after t
            return it == history.begin() ? 0 : std::prev(it)->second;
        }
        Peak peak() const { return live > committed_max ? Peak{live, last_tick} : Peak{committed_max, committed_time}; }
    };

    Lane& lane_of(Side s) { return lanes_[static_cast<std::size_t>(s)]; }
    const Lane& lane_of(Side s) const { return lanes_[static_cast<std::size_t>(s)]; }
    void check_past(long long t) const {
        if (t < 0 || t > now_) throw std::invalid_argument("t must be in [0, now=" + std::to_string(now_) + "]: " + std::to_string(t));
    }

    std::unordered_map<long long, Order> orders_;
    std::array<Lane, 2> lanes_;
    Lane all_;
    long long now_ = 0;
};

// ============================================================================================ Part 4
/// Interval counting over huge coordinates: coordinate compression + a lazy segment tree with "permanent" tags.
///
/// Compression: the live count only changes at endpoints.  Sort and dedupe them into c[0] < ... < c[m-1]; the gap
/// [c[j], c[j+1]) is an elementary segment with a constant count.  [s, e) covers segments idx(s) .. idx(e)-1.
/// Segment tree over those segments, stored in two std::vector<int> (heap layout, children of i are 2i and 2i+1):
///   add[i]  the amount still owed to the whole range of node i (never pushed down),
///   mx[i]   the maximum over node i's range, including add[i] and everything below, excluding ancestors' tags.
/// A query walks down and adds each visited node's tag on the way back up: no push-down, so queries stay const.
class IntervalIndex {
public:
    /// Every endpoint that will ever be used (any order, duplicates allowed).
    explicit IntervalIndex(std::span<const long long> coordinates) : coords_(coordinates.begin(), coordinates.end()) {
        std::sort(coords_.begin(), coords_.end());
        coords_.erase(std::unique(coords_.begin(), coords_.end()), coords_.end());
        segs_ = coords_.empty() ? 0 : static_cast<int>(coords_.size()) - 1;
        size_ = 1;
        while (size_ < std::max(1, segs_)) size_ <<= 1;
        mx_.assign(2 * static_cast<std::size_t>(size_), 0);
        add_.assign(2 * static_cast<std::size_t>(size_), 0);
    }

    /// Build from intervals: collect endpoints, compress, add each.
    static IntervalIndex of(std::span<const Interval> intervals) {
        std::vector<long long> pts;
        pts.reserve(intervals.size() * 2);
        for (const Interval& iv : intervals) { pts.push_back(iv.start); pts.push_back(iv.end); }
        IntervalIndex idx{std::span<const long long>(pts)};
        for (const Interval& iv : intervals) idx.add(iv.start, iv.end);
        return idx;
    }

    /// Part 1's answer through compression + segment tree; must equal the sweep.
    static int max_overlap(std::span<const Interval> intervals) { return of(intervals).max(); }

    void add(long long start, long long end) { update(start, end, 1); }
    /// Undo a previous add of the same interval (caller's responsibility).
    void remove(long long start, long long end) { update(start, end, -1); }

    int max() const { return segs_ == 0 ? 0 : mx_[1]; }

    /// Live count at time t; 0 outside all endpoints; the right end is exclusive.
    int live_at(long long t) const {
        const int j = floor_index(t);
        if (j < 0 || j >= segs_) return 0;
        return range_max(1, 0, size_ - 1, j, j);
    }

    /// Maximum live count at any time in [from, to).  to < from -> invalid_argument; to == from -> 0.
    int max_in(long long from, long long to) const {
        if (to < from) throw std::invalid_argument("to < from: " + std::to_string(to) + " < " + std::to_string(from));
        if (to == from || segs_ == 0) return 0;
        const int lo = std::max(0, floor_index(from));  // the segment containing `from` (or the first one)
        const int hi = std::min(segs_ - 1, lower_bound_index(to) - 1);  // the last segment starting before `to`
        if (lo > hi) return 0;
        return std::max(0, range_max(1, 0, size_ - 1, lo, hi));
    }

    int coordinate_count() const { return static_cast<int>(coords_.size()); }
    int segment_count() const { return segs_; }

private:
    void update(long long start, long long end, int delta) {
        if (end < start) throw std::invalid_argument("end < start: " + std::to_string(end) + " < " + std::to_string(start));
        const int lo = exact_index(start);
        const int hi = exact_index(end);
        if (lo == hi) return;  // empty interval
        range_add(1, 0, size_ - 1, lo, hi - 1, delta);
    }

    void range_add(int node, int nl, int nr, int l, int r, int delta) {
        const auto n = static_cast<std::size_t>(node);
        if (l <= nl && nr <= r) {  // fully covered: tag this node only
            add_[n] += delta;
            mx_[n] += delta;
            return;
        }
        const int mid = nl + (nr - nl) / 2;
        if (l <= mid) range_add(2 * node, nl, mid, l, r, delta);
        if (r > mid) range_add(2 * node + 1, mid + 1, nr, l, r, delta);
        mx_[n] = add_[n] + std::max(mx_[2 * n], mx_[2 * n + 1]);
    }

    int range_max(int node, int nl, int nr, int l, int r) const {
        const auto n = static_cast<std::size_t>(node);
        if (l <= nl && nr <= r) return mx_[n];
        const int mid = nl + (nr - nl) / 2;
        int best = INT_MIN;  // at least one branch below runs (l <= r), so this is always replaced
        if (l <= mid) best = std::max(best, range_max(2 * node, nl, mid, l, r));
        if (r > mid) best = std::max(best, range_max(2 * node + 1, mid + 1, nr, l, r));
        return best + add_[n];  // this node's tag applies to its whole range and was never pushed down
    }

    // Binary searches use comparisons only: no subtraction, no overflow near LLONG_MAX.
    int exact_index(long long x) const {
        auto it = std::lower_bound(coords_.begin(), coords_.end(), x);
        if (it == coords_.end() || *it != x) throw std::invalid_argument("unknown coordinate: " + std::to_string(x));
        return static_cast<int>(it - coords_.begin());
    }
    /// Largest j with coords[j] <= x, or -1.
    int floor_index(long long x) const { return static_cast<int>(std::upper_bound(coords_.begin(), coords_.end(), x) - coords_.begin()) - 1; }
    /// Smallest j with coords[j] >= x, or coords.size().
    int lower_bound_index(long long x) const { return static_cast<int>(std::lower_bound(coords_.begin(), coords_.end(), x) - coords_.begin()); }

    std::vector<long long> coords_;
    int segs_ = 0;
    int size_ = 1;
    std::vector<int> mx_, add_;
};

}  // namespace overlap
