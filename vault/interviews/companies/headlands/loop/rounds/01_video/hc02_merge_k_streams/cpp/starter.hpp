// hc02 · Merge K sorted streams — C++20 starter.  Statement: ../problem.md.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <atomic>
#include <cstddef>
#include <exception>
#include <functional>
#include <iterator>
#include <memory>
#include <optional>
#include <queue>
#include <ranges>
#include <stdexcept>
#include <stop_token>
#include <string>
#include <thread>
#include <utility>
#include <variant>
#include <vector>

namespace mergek {

/// An input sequence is not ascending.  `stream` = index of the sequence, `position` = index of the offending element.
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

// ------------------------------------------------------------------------------------------------ Part 1
/// Merge k sorted vectors; equal elements come out in stream order (stable).  Use only `less` (no ==, no >, no a - b).
/// Not ascending -> UnsortedInputException(stream, position).  The input is not modified.
/// Hint: std::priority_queue pops the LARGEST element under its comparator; the heap can hold (stream, position) pairs.
template <class T, class Less = std::less<T>>
std::vector<T> merge(const std::vector<std::vector<T>>&, Less = {}) {
    throw std::logic_error("TODO");
}

/// Performance version: no boxing, no per-element objects in the heap.  Hint: a hand-written heap of stream indices.
inline std::vector<long long> merge_longs(const std::vector<std::vector<long long>>&) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 2
/// A pull source: each call yields the next element, or std::nullopt at the end.
template <class T>
using Source = std::function<std::optional<T>()>;

/// Adapt any input range to a Source (given).  An lvalue range is borrowed, an rvalue range is owned.
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

/// Lazy k-way merge.  Nothing is pulled at construction; the first has_next()/next() pulls one head per source; the source
/// that just produced the output is refilled only on the NEXT call.  Equal elements: lower stream first.  An order violation
/// is detected when the element is read (UnsortedInputException from has_next()/next()).  After any exception from a source,
/// every later call rethrows it.  next() on an exhausted merger -> std::out_of_range.
/// Hint: the heap can hold stream indices with a comparator that looks at the heads; remember what the comparator captures
/// if you ever copy or move the object (the iterator below is given).
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

    explicit Merger(std::vector<Source<T>>, Less = {}) {}
    Merger(const Merger&) = delete;
    Merger& operator=(const Merger&) = delete;

    bool has_next() { throw std::logic_error("TODO"); }
    T next() { throw std::logic_error("TODO"); }

    iterator begin() { return iterator(this); }
    sentinel end() { return {}; }
};

// ------------------------------------------------------------------------------------------------ Part 3 (types given)
template <class T>
struct Ready {
    T value;
    int stream;
};
struct Pending {};
struct Done {};
/// Pending = some live stream has no head yet, so no element can be output safely (it is NOT "no data").
template <class T>
using Poll = std::variant<Ready<T>, Pending, Done>;

/// A source failed (it threw, or its stream is not sorted).  cause() is the original exception.
class MergeException : public std::runtime_error {
public:
    MergeException(int stream, std::exception_ptr cause)
        : std::runtime_error("stream " + std::to_string(stream) + " failed"), stream_(stream), cause_(std::move(cause)) {}
    int stream() const noexcept { return stream_; }
    const std::exception_ptr& cause() const noexcept { return cause_; }

private:
    int stream_;
    std::exception_ptr cause_;
};

/// A source that may block.  It gets the stop token and must return std::nullopt promptly once stop is requested.
template <class T>
using BlockingSource = std::function<std::optional<T>(std::stop_token)>;

/// One std::jthread producer per source, each feeding its own bounded queue (capacity >= 1, else std::invalid_argument).
///  * try_next(): never blocks; Ready / Pending / Done.  next(): blocks until Ready or Done.
///  * A failed source (threw, or unsorted -> UnsortedInputException as the cause) surfaces as MergeException(stream, cause)
///    AFTER the elements it produced before failing; the merge then closes itself and later calls throw std::logic_error.
///  * close() is idempotent: cancel all producers (stop token) and join them; the destructor does the same.
///  * Output never depends on thread scheduling (stable merge); a thread body must never throw (std::terminate).
/// Hint: std::condition_variable_any::wait(lock, stop_token, pred) wakes up when the token fires.
template <class T, class Less = std::less<T>>
class ConcurrentMerge {
public:
    ConcurrentMerge(std::vector<BlockingSource<T>>, int, Less = {}) { throw std::logic_error("TODO"); }
    ConcurrentMerge(const ConcurrentMerge&) = delete;
    ConcurrentMerge& operator=(const ConcurrentMerge&) = delete;

    Poll<T> try_next() { throw std::logic_error("TODO"); }
    Poll<T> next() { throw std::logic_error("TODO"); }
    void close() {}
};

// ------------------------------------------------------------------------------------------------ Part 4
/// Merge everything and return the result.  The first failing source cancels the others (blocked sources wake up through
/// their stop token) and merge_all throws MergeException with that stream's index.  Whether it returns or throws, every
/// thread has finished when it exits.  Hint: an object whose destructor requests stop and joins.
template <class T, class Less = std::less<T>>
std::vector<T> merge_all(std::vector<BlockingSource<T>>, int, Less = {}) {
    throw std::logic_error("TODO");
}

}  // namespace mergek
