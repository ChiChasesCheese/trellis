// hc03 · recursive sum 1..n — C++20 starter.  Statement: ../problem.md.  One Part at a time, like in the interview.
// Copy to work.hpp with `python3 tools/cpptest.py start <dir>`; run with `... run <dir> --impl work --tag part1`.
#pragma once

#include <climits>
#include <cstddef>
#include <functional>
#include <optional>
#include <pthread.h>
#include <span>
#include <stdexcept>
#include <string>
#include <unistd.h>
#include <utility>
#include <variant>
#include <vector>

namespace recsum {

// ------------------------------------------------------------------------------------------------ result type (given)
/// Sum result: fits, or overflows (with the mathematically exact value).  __int128 is this suite's BigInteger.
struct Ok {
    long long value;
    friend bool operator==(const Ok&, const Ok&) = default;
};
struct Overflow {
    __int128 exact;
    friend bool operator==(const Overflow&, const Overflow&) = default;
};
using SumResult = std::variant<Ok, Overflow>;

enum class Width { Int, Long };  // accumulator width; Int overflows at n = 65536

/// Checked addition in the width; nullopt = does not fit.  Hint: __builtin_add_overflow; signed overflow is UB in C++.
inline std::optional<long long> add(Width, long long, long long) { throw std::logic_error("TODO"); }

/// Exact 1+2+...+n as __int128.
inline __int128 exact_to(long long) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 1
/// sum(n) = n + sum(n-1).  n < 0 -> std::invalid_argument; overflow -> Overflow{exact_to(n)}.  Do not try to catch a stack overflow.
inline SumResult sum_recursive(long long, Width) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 2
/// Run fn on a thread with a stack of exactly `bytes` (given: std::thread cannot choose its stack size).  fn must not throw.
inline void run_with_stack(std::size_t bytes, std::function<void()> fn) {
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    const auto page = static_cast<std::size_t>(sysconf(_SC_PAGESIZE));
    pthread_attr_setstacksize(&attr, (bytes + page - 1) / page * page);
    pthread_t th;
    int rc = pthread_create(&th, &attr, [](void* p) -> void* { (*static_cast<std::function<void()>*>(p))(); return nullptr; }, &fn);
    pthread_attr_destroy(&attr);
    if (rc != 0) throw std::runtime_error("pthread_create failed: " + std::to_string(rc));
    pthread_join(th, nullptr);
}

/// Depth reachable by plain recursion on a thread with `stack_bytes` of stack.  A stack overflow cannot be caught in C++,
/// so stop ~32 KiB before the end.  Hints: run_with_stack, __builtin_frame_address(0), make the recursion non-tail.
inline int measure_depth(std::size_t) { throw std::logic_error("TODO"); }

/// Iterative version, O(1) stack, same semantics as sum_recursive.
inline SumResult sum_iterative(long long, Width) { throw std::logic_error("TODO"); }

/// Trampoline (given): done(value) or more(next).  Each step returns at once and hands back the next step.
template <class T>
class Trampoline {
public:
    using Next = std::function<Trampoline()>;
    static Trampoline done(T value) { return Trampoline(std::in_place_index<0>, std::move(value)); }
    static Trampoline more(Next next) { return Trampoline(std::in_place_index<1>, std::move(next)); }
    bool is_done() const { return state_.index() == 0; }
    T take() && { return std::move(std::get<0>(state_)); }
    Trampoline step() const { return std::get<1>(state_)(); }

private:
    template <std::size_t I, class A>
    Trampoline(std::in_place_index_t<I> tag, A&& a) : state_(tag, std::forward<A>(a)) {}
    std::variant<T, Next> state_;
};

/// Run a trampoline with a loop (no recursion).
template <class T>
T run(Trampoline<T>) { throw std::logic_error("TODO"); }

/// Tail-recursive form (accumulator parameter) + trampoline.  Same semantics as sum_recursive.
inline SumResult sum_trampoline(long long, Width) { throw std::logic_error("TODO"); }

/// Mutual recursion is_even/is_odd through a trampoline; must survive n = 2,000,000 on a 512 KiB stack.  n < 0 -> invalid_argument.
inline bool is_even(long long) { throw std::logic_error("TODO"); }

/// Plain tail-recursive source form; the optimiser may or may not turn it into a loop.
inline SumResult sum_tail_recursive(long long, Width) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 3
/// The classic wrong answer (given, for comparison; do not use).  Signed n*(n+1) would be UB, so the wrap is spelled
/// out with unsigned arithmetic: n = 2^32 - 1 gives -2^31.
inline long long naive_closed_form(long long n) {
    const auto un = static_cast<unsigned long long>(n);
    return static_cast<long long>(un * (un + 1)) / 2;
}

/// Exact a+...+b; a > b -> invalid_argument.  Hint: one __int128 multiplication cannot overflow here (prove it).
inline __int128 range_sum_exact(long long, long long) { throw std::logic_error("TODO"); }

/// a..b: Ok if it fits a long long, else Overflow{exact}.  MIN..MAX is Ok(LLONG_MIN).
inline SumResult range_sum(long long, long long) { throw std::logic_error("TODO"); }

// ------------------------------------------------------------------------------------------------ Part 4
/// 128-bit accumulator over __int128 (associative: any chunking, any merge order).
struct Wide {
    __int128 v = 0;
    static Wide zero() { return {}; }
    Wide plus(long long) const { throw std::logic_error("TODO"); }
    Wide merge(const Wide&) const { throw std::logic_error("TODO"); }
    bool fits_long() const { throw std::logic_error("TODO"); }
    __int128 exact() const { return v; }
    SumResult to_result() const { return fits_long() ? SumResult{Ok{static_cast<long long>(v)}} : SumResult{Overflow{v}}; }
    friend bool operator==(const Wide&, const Wide&) = default;
};

/// Sequential baseline: Overflow only if the TRUE total does not fit ({MAX, 1, -1} is Ok(MAX)).
inline SumResult checked_sum(std::span<const long long>) { throw std::logic_error("TODO"); }

/// Divide and conquer: <= threshold sums directly; else left half on another thread (std::async), right half here.
/// threshold < 1 -> invalid_argument.  Careful: a thread per node is 100,000 threads when threshold = 1.
inline SumResult parallel_sum_fork_join(std::span<const long long>, std::size_t) { throw std::logic_error("TODO"); }

/// hardware_concurrency()*4 chunks, one std::async each (the parallel-stream analogue).
inline SumResult parallel_sum_async(std::span<const long long>) { throw std::logic_error("TODO"); }

/// `chunks` pieces, at most hardware_concurrency() threads pulling chunk numbers from a std::atomic counter.
/// chunks < 1 -> invalid_argument.  Why is a thread per chunk wrong in C++ when "a virtual thread per chunk" is fine in Java?
inline SumResult parallel_sum_workers(std::span<const long long>, std::size_t) { throw std::logic_error("TODO"); }

}  // namespace recsum
