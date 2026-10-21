// hc09 · Top trades by notional — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 top_events (bounded heap, partial_sort / nth_element comparison), 2 top_tickers (hash aggregate + heap),
//        3 SlidingTopK (std::set keyed by (total, ticker)), 4 parallel chunk aggregation with std::jthread.
#pragma once

#include <algorithm>
#include <array>
#include <climits>
#include <cstddef>
#include <deque>
#include <exception>
#include <functional>
#include <future>
#include <mutex>
#include <optional>
#include <queue>
#include <set>
#include <span>
#include <stdexcept>
#include <stop_token>
#include <string>
#include <string_view>
#include <thread>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace toptrades {

// The three parallel arrays.  string_view: the caller owns the text, the functions only borrow it for the call.
using Strings = std::span<const std::string_view>;
using Longs = std::span<const long long>;

// ============================================================================================ checked arithmetic
inline long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error("multiplication overflow: " + std::to_string(a) + " * " + std::to_string(b));
    return r;
}
inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow: " + std::to_string(a) + " + " + std::to_string(b));
    return r;
}

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

// ============================================================================================ value types
/// One trade.  The constructor validates, so an existing Trade never has a negative field or an overflowing notional.
struct Trade {
    int index;
    std::string ticker;  // owned copy: results outlive the input arrays
    long long price, volume;

    Trade(int index, std::string ticker, long long price, long long volume)
        : index(index), ticker(std::move(ticker)), price(price), volume(volume) {
        if (index < 0) throw std::invalid_argument("index must be >= 0: " + std::to_string(index));
        if (price < 0) throw std::invalid_argument("negative price: " + std::to_string(price));
        if (volume < 0) throw std::invalid_argument("negative volume: " + std::to_string(volume));
        mul_exact(price, volume);
    }
    long long notional() const { return mul_exact(price, volume); }
    friend bool operator==(const Trade&, const Trade&) = default;
};

struct TickerTotal {
    std::string ticker;
    long long notional;
    TickerTotal(std::string ticker, long long notional) : ticker(std::move(ticker)), notional(notional) {
        if (notional < 0) throw std::invalid_argument("negative notional: " + std::to_string(notional));
    }
    friend bool operator==(const TickerTotal&, const TickerTotal&) = default;
};

struct Summary {
    long long grand_total;
    std::optional<Trade> largest;
    friend bool operator==(const Summary&, const Summary&) = default;
};

/// "a goes before b": larger notional first, then ticker ascending (bytewise), then index ascending.  A strict total
/// order: no two different trades are equivalent, so every algorithm below returns the same, reproducible list.
struct BestFirst {
    bool operator()(const Trade& a, const Trade& b) const {
        const long long na = a.notional(), nb = b.notional();
        if (na != nb) return na > nb;
        if (const int c = a.ticker.compare(b.ticker); c != 0) return c < 0;
        return a.index < b.index;
    }
};

/// Same idea for ticker totals (tickers are unique in a table, so two criteria are a total order).
struct BestTickerFirst {
    bool operator()(const TickerTotal& a, const TickerTotal& b) const {
        if (a.notional != b.notional) return a.notional > b.notional;
        return a.ticker < b.ticker;
    }
};

// ============================================================================================ shared validation
/// Checks the arrays and k, returns the number of events.
inline std::size_t check_inputs(Strings tickers, Longs prices, Longs volumes, int k) {
    if (tickers.size() != prices.size() || prices.size() != volumes.size())
        throw std::invalid_argument("length mismatch: " + std::to_string(tickers.size()) + " tickers, " +
                                    std::to_string(prices.size()) + " prices, " + std::to_string(volumes.size()) + " volumes");
    if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    if (tickers.size() > static_cast<std::size_t>(INT_MAX)) throw std::invalid_argument("too many events for an int index");
    return tickers.size();
}

/// Notional of event i: non-negative inputs, multiplication overflow -> std::overflow_error.
inline long long notional_at(Strings, Longs prices, Longs volumes, std::size_t i) {
    if (prices[i] < 0) throw std::invalid_argument("negative price at " + std::to_string(i) + ": " + std::to_string(prices[i]));
    if (volumes[i] < 0) throw std::invalid_argument("negative volume at " + std::to_string(i) + ": " + std::to_string(volumes[i]));
    return mul_exact(prices[i], volumes[i]);
}

// ============================================================================================ Part 1
namespace detail {

struct Key {  // what the heap stores: 16 bytes, no string copy
    long long notional;
    int index;
};

inline Trade make_trade(Strings t, Longs p, Longs v, int i) {
    return Trade(i, std::string(t[static_cast<std::size_t>(i)]), p[static_cast<std::size_t>(i)], v[static_cast<std::size_t>(i)]);
}

/// All notionals (validating every event) plus the full-order comparison on event indices: O(n) space, used by the
/// sort-based variants.
struct Ranked {
    Strings tickers;
    std::vector<long long> notional;
    Ranked(Strings t, Longs p, Longs v) : tickers(t) {
        notional.reserve(t.size());
        for (std::size_t i = 0; i < t.size(); ++i) notional.push_back(notional_at(t, p, v, i));
    }
    bool better(int a, int b) const {
        const long long na = notional[static_cast<std::size_t>(a)], nb = notional[static_cast<std::size_t>(b)];
        if (na != nb) return na > nb;
        if (const int c = tickers[static_cast<std::size_t>(a)].compare(tickers[static_cast<std::size_t>(b)]); c != 0) return c < 0;
        return a < b;
    }
    std::vector<int> indices() const {
        std::vector<int> idx(notional.size());
        for (std::size_t i = 0; i < idx.size(); ++i) idx[i] = static_cast<int>(i);
        return idx;
    }
};

inline std::vector<Trade> materialize(const std::vector<int>& idx, std::size_t m, Strings t, Longs p, Longs v) {
    std::vector<Trade> out;
    out.reserve(m);
    for (std::size_t i = 0; i < m; ++i) out.push_back(make_trade(t, p, v, idx[i]));
    return out;
}

}  // namespace detail

/// The k best events, best first.  A bounded heap whose top is the WORST event kept so far: O(n log k) time, O(k) space.
/// Every event is validated and its notional computed, even when it cannot make the top k.
inline std::vector<Trade> top_events(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const auto cap = static_cast<std::size_t>(k);
    auto better = [&](const detail::Key& a, const detail::Key& b) {  // "a is better than b"
        if (a.notional != b.notional) return a.notional > b.notional;
        if (const int c = tickers[static_cast<std::size_t>(a.index)].compare(tickers[static_cast<std::size_t>(b.index)]); c != 0) return c < 0;
        return a.index < b.index;
    };
    // priority_queue's top() is the element that compares greatest.  "Greatest" under `better` = the worst event.
    std::vector<detail::Key> storage;
    storage.reserve(std::min(cap, n));  // never reserve k itself: k may be INT_MAX
    std::priority_queue<detail::Key, std::vector<detail::Key>, decltype(better)> heap(better, std::move(storage));
    for (std::size_t i = 0; i < n; ++i) {
        const long long notional = notional_at(tickers, prices, volumes, i);
        if (cap == 0) continue;
        if (heap.size() == cap && notional < heap.top().notional) continue;  // fast reject: no allocation, no string compare
        const detail::Key cand{notional, static_cast<int>(i)};
        if (heap.size() < cap) {
            heap.push(cand);
        } else if (better(cand, heap.top())) {
            heap.pop();
            heap.push(cand);
        }
    }
    std::vector<int> worst_first;
    worst_first.reserve(heap.size());
    while (!heap.empty()) { worst_first.push_back(heap.top().index); heap.pop(); }
    std::reverse(worst_first.begin(), worst_first.end());
    return detail::materialize(worst_first, worst_first.size(), tickers, prices, volumes);
}

/// Baseline: sort every event index, take the prefix.  O(n log n) time, O(n) space.
inline std::vector<Trade> top_events_sorted(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const detail::Ranked r(tickers, prices, volumes);
    auto idx = r.indices();
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { return r.better(a, b); });
    return detail::materialize(idx, std::min(static_cast<std::size_t>(k), n), tickers, prices, volumes);
}

/// std::partial_sort: a heap of the first m, sifted by the rest, then sorted.  O(n log m) time, O(n) space for the indices.
inline std::vector<Trade> top_events_partial_sort(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const detail::Ranked r(tickers, prices, volumes);
    auto idx = r.indices();
    const std::size_t m = std::min(static_cast<std::size_t>(k), n);
    std::partial_sort(idx.begin(), idx.begin() + static_cast<std::ptrdiff_t>(m), idx.end(), [&](int a, int b) { return r.better(a, b); });
    return detail::materialize(idx, m, tickers, prices, volumes);
}

/// std::nth_element (introselect, O(n) average) puts the m best in front in ANY order; then sort just that prefix.
inline std::vector<Trade> top_events_nth_element(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const detail::Ranked r(tickers, prices, volumes);
    auto idx = r.indices();
    const std::size_t m = std::min(static_cast<std::size_t>(k), n);
    auto cmp = [&](int a, int b) { return r.better(a, b); };
    if (m > 0 && m < n) std::nth_element(idx.begin(), idx.begin() + static_cast<std::ptrdiff_t>(m - 1), idx.end(), cmp);
    std::sort(idx.begin(), idx.begin() + static_cast<std::ptrdiff_t>(m), cmp);
    return detail::materialize(idx, m, tickers, prices, volumes);
}

// ============================================================================================ Part 2
/// Hash of string_view so that map.find(std::string_view) needs no temporary std::string (C++20 heterogeneous lookup).
struct StringHash {
    using is_transparent = void;
    std::size_t operator()(std::string_view s) const noexcept { return std::hash<std::string_view>{}(s); }
};
using Totals = std::unordered_map<std::string, long long, StringHash, std::equal_to<>>;

/// totals[ticker] += amount, checked.  Throws before touching the table.
inline void add_to(Totals& totals, std::string_view ticker, long long amount) {
    if (auto it = totals.find(ticker); it != totals.end()) it->second = add_exact(it->second, amount);
    else totals.emplace(std::string(ticker), amount);
}

/// Top k of a ticker -> total table (bounded heap of pointers into the table's nodes: no string copies until the end).
inline std::vector<TickerTotal> top_of(const Totals& totals, int k) {
    if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    const auto cap = static_cast<std::size_t>(k);
    if (cap == 0) return {};
    using Entry = Totals::value_type;
    auto better = [](const Entry* a, const Entry* b) {
        if (a->second != b->second) return a->second > b->second;
        return a->first < b->first;
    };
    std::vector<const Entry*> storage;
    storage.reserve(std::min(cap, totals.size()));
    std::priority_queue<const Entry*, std::vector<const Entry*>, decltype(better)> heap(better, std::move(storage));
    for (const Entry& e : totals) {
        if (heap.size() < cap) heap.push(&e);
        else if (better(&e, heap.top())) { heap.pop(); heap.push(&e); }
    }
    std::vector<TickerTotal> out;
    out.reserve(heap.size());
    while (!heap.empty()) { out.emplace_back(heap.top()->first, heap.top()->second); heap.pop(); }
    std::reverse(out.begin(), out.end());
    return out;
}

/// Aggregate per ticker, then take the top k.  O(n) hashing + O(m log k) selection.
inline std::vector<TickerTotal> top_tickers(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    Totals totals;
    for (std::size_t i = 0; i < n; ++i) add_to(totals, tickers[i], notional_at(tickers, prices, volumes, i));
    return top_of(totals, k);
}

/// Same answer by sorting: partial_sort of all m entries' pointers.  O(m log k) too, but with a bigger constant than the heap.
inline std::vector<TickerTotal> top_tickers_sorted(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    Totals totals;
    for (std::size_t i = 0; i < n; ++i) add_to(totals, tickers[i], notional_at(tickers, prices, volumes, i));
    using Entry = Totals::value_type;
    std::vector<const Entry*> all;
    all.reserve(totals.size());
    for (const Entry& e : totals) all.push_back(&e);
    const std::size_t m = std::min(static_cast<std::size_t>(k), all.size());
    std::partial_sort(all.begin(), all.begin() + static_cast<std::ptrdiff_t>(m), all.end(), [](const Entry* a, const Entry* b) {
        if (a->second != b->second) return a->second > b->second;
        return a->first < b->first;
    });
    std::vector<TickerTotal> out;
    for (std::size_t i = 0; i < m; ++i) out.emplace_back(all[i]->first, all[i]->second);
    return out;
}

/// One pass, two independent aggregates: the grand total and the best single event (built once, at the end).
inline Summary summarize(Strings tickers, Longs prices, Longs volumes) {
    const std::size_t n = check_inputs(tickers, prices, volumes, 0);
    long long grand = 0;
    std::optional<std::size_t> best;
    long long best_notional = 0;
    for (std::size_t i = 0; i < n; ++i) {
        const long long nt = notional_at(tickers, prices, volumes, i);
        grand = add_exact(grand, nt);
        // strictly better only: on a full tie the earlier index (already in `best`) wins
        if (!best || nt > best_notional || (nt == best_notional && tickers[i] < tickers[*best])) {
            best = i;
            best_notional = nt;
        }
    }
    if (!best) return Summary{grand, std::nullopt};
    return Summary{grand, detail::make_trade(tickers, prices, volumes, static_cast<int>(*best))};
}

// ============================================================================================ Part 3
struct Fill {
    long long time;
    std::string ticker;
    long long price, volume;
    Fill(long long time, std::string ticker, long long price, long long volume)
        : time(time), ticker(std::move(ticker)), price(price), volume(volume) {
        if (time < 0) throw std::invalid_argument("negative time: " + std::to_string(time));
        if (price < 0) throw std::invalid_argument("negative price: " + std::to_string(price));
        if (volume < 0) throw std::invalid_argument("negative volume: " + std::to_string(volume));
        mul_exact(price, volume);
    }
    long long notional() const { return mul_exact(price, volume); }
    friend bool operator==(const Fill&, const Fill&) = default;
};
struct Tick { long long time; friend bool operator==(const Tick&, const Tick&) = default; };
struct Ask { long long time; friend bool operator==(const Ask&, const Ask&) = default; };
using Feed = std::variant<Fill, Tick, Ask>;

struct Answer {
    long long time;
    std::vector<TickerTotal> top;
    friend bool operator==(const Answer&, const Answer&) = default;
};

/// Top-k tickers over the last `window` time units.  A fill at time t is live while now - t < window.
///
/// Why not a heap alone: a ticker's total changes in both directions (new fills, expiries), i.e. "change the key of
/// an arbitrary element", and a priority_queue cannot find or edit anything but its top.  std::set can: erase the old
/// (total, ticker) key, insert the new one, O(log m) each.
///
/// ranking_ stores string_views into the keys of acc_ (unordered_map nodes never move), so this class is neither copyable nor
/// movable, and a ranking entry is always erased BEFORE its acc_ node is.
class SlidingTopK {
public:
    SlidingTopK(long long window, int k) : window_(window), k_(k) {
        if (window < 1) throw std::invalid_argument("window must be >= 1: " + std::to_string(window));
        if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    }
    SlidingTopK(const SlidingTopK&) = delete;
    SlidingTopK& operator=(const SlidingTopK&) = delete;

    /// Advance the clock to f.time (expiring old fills), then count f.  Overflow -> std::overflow_error, state unchanged.
    void add(const Fill& f) {
        advance_to(f.time);
        auto it = acc_.find(std::string_view(f.ticker));
        const long long old_total = it == acc_.end() ? 0 : it->second.total;
        const long long new_total = add_exact(old_total, f.notional());  // overflow_error here: nothing has been touched
        live_.push_back(f);                                              // bad_alloc here: nothing else has been touched
        if (it == acc_.end()) {
            try {
                it = acc_.try_emplace(f.ticker).first;
                ranking_.insert(Rank{new_total, it->first});
            } catch (...) {
                if (it != acc_.end()) acc_.erase(it);
                live_.pop_back();
                throw;
            }
        } else {
            rekey(it->first, old_total, new_total);
        }
        it->second.total = new_total;
        ++it->second.count;
    }

    /// Move the clock to t (t < now throws) and expire every fill with now - time >= window.
    void advance_to(long long t) {
        if (t < now_) throw std::invalid_argument("time went backwards: " + std::to_string(t) + " < " + std::to_string(now_));
        now_ = t;
        while (!live_.empty() && now_ - live_.front().time >= window_) {
            const Fill& f = live_.front();
            auto it = acc_.find(std::string_view(f.ticker));
            if (it->second.count == 1) {
                ranking_.erase(Rank{it->second.total, it->first});  // erase the view's entry before its owner dies
                acc_.erase(it);
            } else {
                const long long nt = it->second.total - f.notional();
                rekey(it->first, it->second.total, nt);
                it->second.total = nt;
                --it->second.count;
            }
            live_.pop_front();
        }
    }

    /// Current top k, best first (total descending, ticker ascending).
    std::vector<TickerTotal> top() const {
        std::vector<TickerTotal> out;
        std::size_t left = static_cast<std::size_t>(k_);
        for (auto it = ranking_.begin(); it != ranking_.end() && left > 0; ++it, --left) out.emplace_back(std::string(it->ticker), it->total);
        return out;
    }
    long long total_of(std::string_view ticker) const {
        auto it = acc_.find(ticker);
        return it == acc_.end() ? 0 : it->second.total;
    }
    int live_events() const { return static_cast<int>(live_.size()); }
    int distinct_tickers() const { return static_cast<int>(acc_.size()); }
    long long now() const { return now_; }

    /// Process a feed; every Ask yields one Answer.  std::visit over the variant: a missing overload is a compile error.
    static std::vector<Answer> replay(long long window, int k, const std::vector<Feed>& feed) {
        SlidingTopK w(window, k);
        std::vector<Answer> answers;
        for (const Feed& item : feed) {
            std::visit(overloaded{
                           [&](const Fill& f) { w.add(f); },
                           [&](const Tick& t) { if (t.time != w.now()) w.advance_to(t.time); },
                           [&](const Ask& a) {
                               w.advance_to(a.time);
                               answers.push_back(Answer{a.time, w.top()});
                           }},
                       item);
        }
        return answers;
    }

private:
    struct Acc { long long total = 0; int count = 0; };
    struct Rank {
        long long total;
        std::string_view ticker;  // points into the key of an acc_ node
    };
    struct RankOrder {
        bool operator()(const Rank& a, const Rank& b) const {
            if (a.total != b.total) return a.total > b.total;
            return a.ticker < b.ticker;
        }
    };

    /// Change one ranking key without allocating: extract the node, edit the key (C++17 node handles allow it), re-insert.
    /// Also correct when the key does not change (a zero-notional fill): erase+insert of equal keys would be a trap.
    void rekey(std::string_view ticker, long long from, long long to) {
        auto node = ranking_.extract(Rank{from, ticker});
        node.value().total = to;
        ranking_.insert(std::move(node));
    }

    long long window_;
    int k_;
    std::deque<Fill> live_;  // arrival order = time order: only the front can expire
    std::unordered_map<std::string, Acc, StringHash, std::equal_to<>> acc_;
    std::set<Rank, RankOrder> ranking_;
    long long now_ = 0;
};

// ============================================================================================ Part 4
namespace detail {

struct Cancelled {};  // thrown inside a worker when a sibling failed; never escapes a worker

/// Add events [from, to) into m.  Looks at the stop token every 4096 events: cooperative cancellation.
inline void accumulate(Totals& m, Strings t, Longs p, Longs v, std::size_t from, std::size_t to, const std::stop_token& stop = {}) {
    for (std::size_t i = from; i < to; ++i) {
        if ((i & 0xFFF) == 0 && stop.stop_requested()) throw Cancelled{};
        add_to(m, t[i], notional_at(t, p, v, i));
    }
}

/// Merge two tables (small into large).  Both belong to the caller, who must not use them afterwards.
inline Totals merge_into(Totals a, Totals b) {
    if (a.size() < b.size()) a.swap(b);
    for (auto& [ticker, amount] : b) add_to(a, ticker, amount);
    return a;
}

/// Start of chunk c: n * c / chunks computed in 64 bits.
inline std::size_t boundary_impl(std::size_t n, int chunks, int c) {
    return static_cast<std::size_t>(static_cast<unsigned long long>(n) * static_cast<unsigned long long>(c) / static_cast<unsigned long long>(chunks));
}

/// Run body(c, from, to, stop) on one jthread per chunk.  A worker that throws records its exception and asks the others
/// to stop; after all workers are joined the lowest-numbered recorded exception is rethrown.  Exceptions never escape
/// a thread body (that would call std::terminate).
template <class Body>
void run_chunks(std::size_t n, int chunks, Body body) {
    std::vector<std::exception_ptr> errors(static_cast<std::size_t>(chunks));
    std::stop_source stop;
    {
        std::vector<std::jthread> workers;
        workers.reserve(static_cast<std::size_t>(chunks));
        try {
            for (int c = 0; c < chunks; ++c) {
                workers.emplace_back([&, c] {
                    try {
                        body(c, boundary_impl(n, chunks, c), boundary_impl(n, chunks, c + 1), stop.get_token());
                    } catch (const Cancelled&) {
                    } catch (...) {
                        errors[static_cast<std::size_t>(c)] = std::current_exception();
                        stop.request_stop();
                    }
                });
            }
        } catch (...) {  // could not start a thread: stop the ones already running, join them (vector dtor), rethrow
            stop.request_stop();
            throw;
        }
    }  // every jthread is joined here
    for (const auto& e : errors)
        if (e) std::rethrow_exception(e);
}

inline Totals sum_range(Strings t, Longs p, Longs v, std::size_t from, std::size_t to, std::size_t threshold) {
    if (to - from <= threshold) {
        Totals m;
        accumulate(m, t, p, v, from, to);
        return m;
    }
    const std::size_t mid = from + (to - from) / 2;  // not (from + to) / 2: that can overflow
    auto left = std::async(std::launch::async, [=] { return sum_range(t, p, v, from, mid, threshold); });
    Totals right = sum_range(t, p, v, mid, to, threshold);  // if this throws, ~future waits for the left task
    return merge_into(left.get(), std::move(right));
}

}  // namespace detail

inline std::size_t boundary(std::size_t n, int chunks, int c) { return detail::boundary_impl(n, chunks, c); }

inline Totals totals_sequential(Strings t, Longs p, Longs v) {
    const std::size_t n = check_inputs(t, p, v, 0);
    Totals m;
    detail::accumulate(m, t, p, v, 0, n);
    return m;
}

/// One jthread per chunk, one private table per chunk (nothing shared, no lock), merge at the end.
inline Totals totals_chunked(Strings t, Longs p, Longs v, int chunks) {
    const std::size_t n = check_inputs(t, p, v, 0);
    if (chunks < 1) throw std::invalid_argument("chunks must be >= 1: " + std::to_string(chunks));
    std::vector<Totals> parts(static_cast<std::size_t>(chunks));
    detail::run_chunks(n, chunks, [&](int c, std::size_t from, std::size_t to, const std::stop_token& stop) {
        detail::accumulate(parts[static_cast<std::size_t>(c)], t, p, v, from, to, stop);
    });
    Totals acc = std::move(parts[0]);
    for (std::size_t c = 1; c < parts.size(); ++c) acc = detail::merge_into(std::move(acc), std::move(parts[c]));
    return acc;
}

/// Divide and conquer (the fork/join shape): halves until the range is <= threshold, the left half on std::async.
/// No thread pool in the standard library: this starts roughly n / threshold threads, so threshold must not be tiny.
inline Totals totals_recursive(Strings t, Longs p, Longs v, int threshold) {
    const std::size_t n = check_inputs(t, p, v, 0);
    if (threshold < 1) throw std::invalid_argument("threshold must be >= 1: " + std::to_string(threshold));
    return detail::sum_range(t, p, v, 0, n, static_cast<std::size_t>(threshold));
}

/// Control group: every thread adds into one shared table.  The standard library has no concurrent hash map, so the
/// table is split into 16 shards (hash % 16), each with its own mutex.  Correct, but hot tickers serialize on a lock.
inline Totals totals_sharded(Strings t, Longs p, Longs v, int chunks) {
    const std::size_t n = check_inputs(t, p, v, 0);
    if (chunks < 1) throw std::invalid_argument("chunks must be >= 1: " + std::to_string(chunks));
    struct alignas(64) Shard {  // one cache line each: no false sharing between shard mutexes
        std::mutex mutex;
        Totals map;
    };
    std::array<Shard, 16> shards;
    detail::run_chunks(n, chunks, [&](int, std::size_t from, std::size_t to, const std::stop_token& stop) {
        for (std::size_t i = from; i < to; ++i) {
            if ((i & 0xFFF) == 0 && stop.stop_requested()) throw detail::Cancelled{};
            const long long amount = notional_at(t, p, v, i);
            Shard& s = shards[StringHash{}(t[i]) % shards.size()];
            std::lock_guard<std::mutex> lock(s.mutex);
            add_to(s.map, t[i], amount);
        }
    });
    Totals all;
    for (Shard& s : shards) all.merge(s.map);  // shards hold disjoint keys: node splice, no rehash of values
    return all;
}

inline std::vector<TickerTotal> top_tickers_parallel(Strings t, Longs p, Longs v, int k, int chunks) {
    if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    return top_of(totals_chunked(t, p, v, chunks), k);
}

}  // namespace toptrades
