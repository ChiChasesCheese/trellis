// hc02 · Merge K sorted streams — C++20 reference.  Statement: ../problem.md (Java: reference/*.java).
// Parts: 1 merge / merge_longs (priority_queue, hand-written int heap), 2 Merger (lazy, pull-based, input iterator),
//        3 ConcurrentMerge (std::jthread producers + bounded queues), 4 merge_all (RAII scope: first failure cancels the rest).
#pragma once

#include <algorithm>
#include <atomic>
#include <condition_variable>
#include <cstddef>
#include <deque>
#include <exception>
#include <functional>
#include <iterator>
#include <memory>
#include <mutex>
#include <optional>
#include <queue>
#include <ranges>
#include <stdexcept>
#include <stop_token>
#include <string>
#include <thread>
#include <type_traits>
#include <utility>
#include <variant>
#include <vector>

namespace mergek {

// ---- errors ----
/// An input sequence is not ascending.  `stream` = index of the sequence, `position` = index of the offending element in it.
class UnsortedInputException : public std::runtime_error {
public:
    UnsortedInputException(int stream, std::size_t position)
        : std::runtime_error("stream " + std::to_string(stream) + " is not sorted at position " + std::to_string(position)),
          stream_(stream), position_(position) {}
    int stream() const noexcept { return stream_; }
    std::size_t position() const noexcept { return position_; }

private:
    int stream_;
    std::size_t position_;
};

// ---- Part 1: merge ----
/// Merge k sorted vectors.  Equal elements come out in stream order (stable).  Only `less` is used: no ==, no >, no a - b.
/// The heap holds (stream, position) pairs, never copies of elements; the only copy of each element is the one into the result.
template <class T, class Less = std::less<T>>
std::vector<T> merge(const std::vector<std::vector<T>>& lists, Less less = {}) {
    struct Head {
        int stream;
        std::size_t pos;
    };
    // std::priority_queue pops the LARGEST element under its comparator, so the comparator says "a comes LATER than b".
    auto later = [&](const Head& a, const Head& b) {
        const T& x = lists[a.stream][a.pos];
        const T& y = lists[b.stream][b.pos];
        if (less(y, x)) return true;
        if (less(x, y)) return false;
        return a.stream > b.stream;  // tie: the smaller stream index wins; priority_queue itself is not stable
    };
    std::priority_queue<Head, std::vector<Head>, decltype(later)> heap(later);
    std::size_t total = 0;
    for (std::size_t s = 0; s < lists.size(); ++s) {
        total += lists[s].size();
        if (!lists[s].empty()) heap.push({static_cast<int>(s), 0});
    }
    std::vector<T> out;
    out.reserve(total);
    while (!heap.empty()) {
        const Head h = heap.top();  // copy the 16 bytes: pop() destroys the element top() refers to
        heap.pop();
        const auto& list = lists[h.stream];
        out.push_back(list[h.pos]);
        if (h.pos + 1 < list.size()) {
            if (less(list[h.pos + 1], list[h.pos])) throw UnsortedInputException(h.stream, h.pos + 1);
            heap.push({h.stream, h.pos + 1});
        }
    }
    return out;
}

// ---- Part 1: merge_longs ----
/// Performance version: a hand-written heap of stream indices over the original arrays.  No element is copied into the heap.
inline std::vector<long long> merge_longs(const std::vector<std::vector<long long>>& arrays) {
    const std::size_t k = arrays.size();
    std::size_t total = 0;
    for (const auto& a : arrays) total += a.size();
    std::vector<long long> out;
    out.reserve(total);
    std::vector<std::size_t> pos(k, 0);
    std::vector<int> heap;
    heap.reserve(k);
    for (std::size_t s = 0; s < k; ++s)
        if (!arrays[s].empty()) heap.push_back(static_cast<int>(s));

    auto less = [&](int a, int b) {
        const long long va = arrays[a][pos[a]], vb = arrays[b][pos[b]];
        return va < vb || (va == vb && a < b);  // compare, never subtract: LLONG_MAX - LLONG_MIN overflows
    };
    auto sift_down = [&](std::size_t i, std::size_t n) {
        if (n == 0) return;
        const int s = heap[i];
        for (;;) {
            std::size_t child = 2 * i + 1;
            if (child >= n) break;
            if (child + 1 < n && less(heap[child + 1], heap[child])) ++child;
            if (!less(heap[child], s)) break;
            heap[i] = heap[child];
            i = child;
        }
        heap[i] = s;
    };
    std::size_t n = heap.size();
    for (std::size_t i = n / 2; i-- > 0;) sift_down(i, n);  // bottom-up heapify, O(k); `i-- > 0` is the safe unsigned loop
    while (n > 0) {
        const int s = heap[0];
        const long long v = arrays[s][pos[s]];
        out.push_back(v);
        if (++pos[s] < arrays[s].size()) {
            if (arrays[s][pos[s]] < v) throw UnsortedInputException(s, pos[s]);
        } else {
            heap[0] = heap[--n];  // stream exhausted: move the last heap entry to the top
        }
        sift_down(0, n);
    }
    return out;
}

// ---- Part 2: sources ----
/// A pull source: each call yields the next element, or std::nullopt at the end.  Calling it again after the end is
/// not allowed (the merger never does).
template <class T>
using Source = std::function<std::optional<T>()>;

/// Adapt any input range to a Source.  An lvalue range is borrowed (the caller keeps it alive); an rvalue range is
/// moved in and owned.  The state lives on the heap so that copying/moving the std::function cannot invalidate the iterator.
template <std::ranges::viewable_range R>
auto from_range(R&& r) {
    using View = std::views::all_t<R>;
    using V = std::ranges::range_value_t<View>;
    struct State {
        View view;
        std::ranges::iterator_t<View> it;
        explicit State(View v) : view(std::move(v)), it(std::ranges::begin(view)) {}
    };
    auto st = std::make_shared<State>(std::views::all(std::forward<R>(r)));
    return Source<V>([st]() -> std::optional<V> {
        if (st->it == std::ranges::end(st->view)) return std::nullopt;
        std::optional<V> v(*st->it);
        ++st->it;
        return v;
    });
}

// ---- Part 2: Merger ----
/// Lazy k-way merge, written by hand as an input range.  Nothing is pulled at construction; the first has_next()/next()
/// pulls one head per source; the source that just produced the output is refilled only on the NEXT call.
/// After a source (or the order check) throws, the merger is finished: every later call rethrows the same exception.
/// Requires T to be copy-constructible (the previous element of each stream is kept for the order check).
template <class T, class Less = std::less<T>>
class Merger {
public:
    struct sentinel {};

    class iterator {
    public:
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        iterator() = default;
        explicit iterator(Merger* m) : m_(m) { fetch(); }
        const T& operator*() const { return *cur_; }
        iterator& operator++() { fetch(); return *this; }
        void operator++(int) { fetch(); }
        friend bool operator==(const iterator& it, sentinel) { return !it.cur_.has_value(); }

    private:
        void fetch() { cur_ = m_->has_next() ? std::optional<T>(m_->next()) : std::nullopt; }
        Merger* m_ = nullptr;
        std::optional<T> cur_;
    };

    explicit Merger(std::vector<Source<T>> sources, Less less = {})
        : src_(std::move(sources)), head_(src_.size()), prev_(src_.size()), count_(src_.size(), 0),
          less_(std::move(less)), heap_(ByHead{this}) {}

    // The heap's comparator holds `this`: copying or moving a Merger would leave it pointing at the old object.
    Merger(const Merger&) = delete;
    Merger& operator=(const Merger&) = delete;

    bool has_next() {
        prime();
        return !heap_.empty();
    }

    T next() {
        prime();
        if (heap_.empty()) throw std::out_of_range("merge exhausted");
        const int s = heap_.top();
        heap_.pop();
        T out = *head_[s];
        prev_[s] = std::move(head_[s]);  // remembered for the order check; also the stream to refill on the next call
        head_[s].reset();
        refill_ = s;
        return out;
    }

    iterator begin() { return iterator(this); }
    sentinel end() { return {}; }

private:
    // "a comes later than b" (priority_queue pops the largest): value first, then the stream index
    struct ByHead {
        const Merger* m;
        bool operator()(int a, int b) const {
            const T& x = *m->head_[a];
            const T& y = *m->head_[b];
            if (m->less_(y, x)) return true;
            if (m->less_(x, y)) return false;
            return a > b;
        }
    };

    void prime() {
        if (failure_) std::rethrow_exception(failure_);
        try {
            if (!started_) {
                started_ = true;
                for (int s = 0; s < static_cast<int>(src_.size()); ++s)
                    if (advance(s)) heap_.push(s);
            }
            if (refill_ >= 0) {
                const int s = refill_;
                refill_ = -1;
                if (advance(s)) heap_.push(s);
            }
        } catch (...) {
            failure_ = std::current_exception();
            throw;
        }
    }

    bool advance(int s) {
        std::optional<T> v = src_[s]();
        if (!v) return false;
        if (prev_[s] && less_(*v, *prev_[s])) throw UnsortedInputException(s, count_[s]);
        ++count_[s];
        head_[s] = std::move(v);
        return true;
    }

    std::vector<Source<T>> src_;
    std::vector<std::optional<T>> head_;   // the current head of each stream (empty if exhausted or just emitted)
    std::vector<std::optional<T>> prev_;   // the last element emitted from each stream
    std::vector<std::size_t> count_;       // elements pulled from each stream so far
    Less less_;
    bool started_ = false;
    int refill_ = -1;
    std::exception_ptr failure_;
    std::priority_queue<int, std::vector<int>, ByHead> heap_;
};

// ---- Part 3: result types ----
template <class T>
struct Ready {
    T value;
    int stream;
};
struct Pending {};
struct Done {};
/// try_next() result.  Pending = some live stream has no head yet, so no element can be output safely.
template <class T>
using Poll = std::variant<Ready<T>, Pending, Done>;

/// A source failed (it threw, or its stream is not sorted).  cause() is the original exception.
class MergeException : public std::runtime_error {
public:
    MergeException(int stream, std::exception_ptr cause)
        : std::runtime_error("stream " + std::to_string(stream) + " failed: " + describe(cause)), stream_(stream),
          cause_(std::move(cause)) {}
    int stream() const noexcept { return stream_; }
    const std::exception_ptr& cause() const noexcept { return cause_; }

private:
    static std::string describe(const std::exception_ptr& p) {
        if (!p) return "unknown";
        try {
            std::rethrow_exception(p);
        } catch (const std::exception& e) {
            return e.what();
        } catch (...) {
            return "non-std exception";
        }
    }
    int stream_;
    std::exception_ptr cause_;
};

/// A source that may block.  It receives the stop token and must return std::nullopt promptly once stop is requested.
template <class T>
using BlockingSource = std::function<std::optional<T>(std::stop_token)>;

namespace detail {

template <class... Ts>
struct overloaded : Ts... {
    using Ts::operator()...;
};

// ---- Part 3: bounded queue ----
/// Bounded blocking queue.  Every blocking call also wakes up when the stop token fires (condition_variable_any).
template <class M>
class BoundedQueue {
public:
    explicit BoundedQueue(std::size_t capacity) : cap_(capacity) {}

    /// Blocks while full.  Returns false if cancelled before the message could be enqueued.
    bool push(M m, std::stop_token st) {
        std::unique_lock lk(mu_);
        if (!not_full_.wait(lk, st, [&] { return q_.size() < cap_; })) return false;
        q_.push_back(std::move(m));
        lk.unlock();
        not_empty_.notify_one();
        return true;
    }

    std::optional<M> try_pop() {
        std::unique_lock lk(mu_);
        if (q_.empty()) return std::nullopt;
        return take(lk);
    }

    /// Blocks while empty.  Returns std::nullopt if cancelled while waiting.
    std::optional<M> pop(std::stop_token st) {
        std::unique_lock lk(mu_);
        if (!not_empty_.wait(lk, st, [&] { return !q_.empty(); })) return std::nullopt;
        return take(lk);
    }

private:
    M take(std::unique_lock<std::mutex>& lk) {
        M m = std::move(q_.front());
        q_.pop_front();
        lk.unlock();
        not_full_.notify_one();
        return m;
    }

    std::mutex mu_;
    std::condition_variable_any not_full_, not_empty_;
    std::deque<M> q_;
    const std::size_t cap_;
};

// ---- Part 3: messages and producer ----
template <class T>
struct Item {
    T value;
};
struct End {};
struct Failed {
    std::exception_ptr cause;
};
/// Every producer ends with End or Failed, so the consumer never waits for a producer that is already dead.
template <class T>
using Msg = std::variant<Item<T>, End, Failed>;
template <class T>
using Queue = BoundedQueue<Msg<T>>;

/// Pull from `src`, check the order, push into `q`.  Returns normally at the end of the source and when cancelled;
/// throws when the source throws or is unsorted (the caller decides what a failure means).
template <class T, class Less>
void produce(int idx, const BlockingSource<T>& src, Queue<T>& q, std::stop_token st, const Less& less) {
    std::optional<T> prev;
    std::size_t pos = 0;
    for (;;) {
        std::optional<T> v = src(st);
        if (!v) {
            if (!st.stop_requested()) q.push(End{}, st);
            return;
        }
        if (prev && less(*v, *prev)) throw UnsortedInputException(idx, pos);
        prev = *v;
        if (!q.push(Item<T>{std::move(*v)}, st)) return;
        ++pos;
    }
}

// ---- Part 3: ThreadGroup ----
/// Owns the stop source and the threads.  Destruction = request stop, then join every thread (jthread's destructor):
/// no producer can outlive the scope that created the group.
struct ThreadGroup {
    std::stop_source stop;
    std::vector<std::jthread> threads;
    ThreadGroup() = default;
    ThreadGroup(const ThreadGroup&) = delete;
    ThreadGroup& operator=(const ThreadGroup&) = delete;
    ~ThreadGroup() { stop.request_stop(); }
};

// ---- Part 3: combiner ----
/// Consumer side only; not thread-safe.  The rule: an output is decided only when EVERY live stream has a head.
template <class T, class Less>
class Combiner {
public:
    Combiner(std::vector<Queue<T>*> queues, Less less)
        : queues_(std::move(queues)), heads_(queues_.size()), finished_(queues_.size(), 0), less_(std::move(less)) {}

    /// block = false: never waits (Pending if a head is missing).  block = true: waits for missing heads; returns
    /// std::nullopt if the stop token fired while waiting.
    std::optional<Poll<T>> poll(bool block, std::stop_token st) {
        bool pending = false;
        for (std::size_t i = 0; i < queues_.size(); ++i) {
            if (finished_[i] || heads_[i]) continue;
            std::optional<Msg<T>> m = block ? queues_[i]->pop(st) : queues_[i]->try_pop();
            if (!m) {
                if (block) return std::nullopt;
                pending = true;  // keep looking at the other streams: their failures must surface too
                continue;
            }
            std::visit(overloaded{[&](Item<T>& item) { heads_[i] = std::move(item.value); },
                                  [&](End&) { finished_[i] = 1; },
                                  [&](Failed& f) { throw MergeException(static_cast<int>(i), f.cause); }},
                       *m);
        }
        if (pending) return Poll<T>{Pending{}};
        int best = -1;
        for (std::size_t i = 0; i < heads_.size(); ++i)
            if (heads_[i] && (best < 0 || less_(*heads_[i], *heads_[best]))) best = static_cast<int>(i);  // strict <: ties keep the lower stream
        if (best < 0) return Poll<T>{Done{}};
        Ready<T> out{std::move(*heads_[best]), best};
        heads_[best].reset();
        return Poll<T>{std::move(out)};
    }

private:
    std::vector<Queue<T>*> queues_;
    std::vector<std::optional<T>> heads_;
    std::vector<char> finished_;  // not vector<bool>: that one is a bit-packed proxy container
    Less less_;
};

}  // namespace detail

// ---- Part 3: ConcurrentMerge ----
/// One std::jthread producer per source, each feeding its own bounded queue (capacity >= 1); the consumer merges.
/// Output is independent of thread scheduling.  Destroying the object cancels and joins the producers.
/// A source that ignores its stop token makes close() (and the destructor) wait for it: a thread cannot be killed.
template <class T, class Less = std::less<T>>
class ConcurrentMerge {
public:
    ConcurrentMerge(std::vector<BlockingSource<T>> sources, int capacity, Less less = {})
        : sources_(std::move(sources)), combiner_(make_queues(sources_.size(), capacity), less) {
        for (std::size_t i = 0; i < sources_.size(); ++i) {
            group_.threads.emplace_back([this, i, less, st = group_.stop.get_token()] {
                try {
                    detail::produce<T>(static_cast<int>(i), sources_[i], *queues_[i], st, less);
                } catch (...) {
                    // A thread body must never throw (that is std::terminate): leave the exception as the last message.
                    queues_[i]->push(detail::Failed{std::current_exception()}, st);
                }
            });
        }
    }

    ConcurrentMerge(const ConcurrentMerge&) = delete;
    ConcurrentMerge& operator=(const ConcurrentMerge&) = delete;
    ~ConcurrentMerge() { close(); }

    /// Never blocks.  Throws MergeException (and closes) on a failed stream; std::logic_error once closed.
    Poll<T> try_next() {
        if (closed_.load()) throw std::logic_error("closed");
        try {
            auto p = combiner_.poll(false, {});
            return std::move(*p);  // a non-blocking poll always has a result
        } catch (const MergeException&) {
            close();
            throw;
        }
    }

    /// Blocks until Ready or Done (never Pending).  If close() runs on another thread meanwhile: std::logic_error.
    Poll<T> next() {
        if (closed_.load()) throw std::logic_error("closed");
        try {
            auto p = combiner_.poll(true, group_.stop.get_token());
            if (!p) throw std::logic_error("closed");
            return std::move(*p);
        } catch (const MergeException&) {
            close();
            throw;
        }
    }

    /// Idempotent: cancel every producer and wait for them to finish.
    void close() {
        if (closed_.exchange(true)) return;
        group_.stop.request_stop();
        group_.threads.clear();  // jthread destructors join
    }

private:
    std::vector<detail::Queue<T>*> make_queues(std::size_t n, int capacity) {
        if (capacity < 1) throw std::invalid_argument("capacity must be >= 1: " + std::to_string(capacity));
        for (std::size_t i = 0; i < n; ++i) queues_.push_back(std::make_unique<detail::Queue<T>>(static_cast<std::size_t>(capacity)));
        std::vector<detail::Queue<T>*> raw;
        for (auto& q : queues_) raw.push_back(q.get());
        return raw;
    }

    // Declaration order is destruction order in reverse: group_ (joins the threads) dies BEFORE the queues and sources they use.
    std::vector<BlockingSource<T>> sources_;
    std::vector<std::unique_ptr<detail::Queue<T>>> queues_;
    detail::Combiner<T, Less> combiner_;
    std::atomic<bool> closed_{false};
    detail::ThreadGroup group_;
};

// ---- Part 4: merge_all ----
/// Merge everything and return the result.  Producers run in a ThreadGroup that lives inside this function: the first
/// failure is recorded and cancels the others (their stop token fires, blocked sources wake up), and leaving the function
/// by return or by exception always joins every thread.  Throws MergeException with the failing stream's index.
template <class T, class Less = std::less<T>>
std::vector<T> merge_all(std::vector<BlockingSource<T>> sources, int capacity, Less less = {}) {
    if (capacity < 1) throw std::invalid_argument("capacity must be >= 1: " + std::to_string(capacity));
    std::vector<std::unique_ptr<detail::Queue<T>>> queues;
    std::vector<detail::Queue<T>*> raw;
    for (std::size_t i = 0; i < sources.size(); ++i) {
        queues.push_back(std::make_unique<detail::Queue<T>>(static_cast<std::size_t>(capacity)));
        raw.push_back(queues.back().get());
    }
    std::mutex failure_mu;
    std::optional<std::pair<int, std::exception_ptr>> failure;
    detail::ThreadGroup group;  // declared last: destroyed first, so the threads end before the things they reference
    for (std::size_t i = 0; i < sources.size(); ++i) {
        group.threads.emplace_back([&, i, st = group.stop.get_token()] {
            try {
                detail::produce<T>(static_cast<int>(i), sources[i], *queues[i], st, less);
            } catch (...) {
                {
                    std::lock_guard lk(failure_mu);
                    if (!failure) failure.emplace(static_cast<int>(i), std::current_exception());  // the first failure wins
                }
                group.stop.request_stop();
            }
        });
    }
    auto rethrow_failure = [&]() -> void {
        std::lock_guard lk(failure_mu);
        if (!failure) throw std::logic_error("cancelled without a failure");
        throw MergeException(failure->first, failure->second);
    };

    detail::Combiner<T, Less> combiner(raw, less);
    std::vector<T> out;
    for (;;) {
        if (group.stop.stop_requested()) rethrow_failure();
        auto p = combiner.poll(true, group.stop.get_token());
        if (!p) rethrow_failure();
        if (auto* r = std::get_if<Ready<T>>(&*p)) out.push_back(std::move(r->value));
        else if (std::holds_alternative<Done>(*p)) return out;
        else throw std::logic_error("a blocking poll never returns Pending");
    }
}

}  // namespace mergek
