// hc03 · recursive sum 1..n — C++20 reference.  Statement: ../problem.md (Java version: reference/RecursiveSum.java).
// Parts: 1 checked recursion, 2 stack depth (iterative / trampoline), 3 ranges + closed form, 4 parallel sums.
#pragma once

#include <algorithm>
#include <atomic>
#include <bit>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <future>
#include <optional>
#include <pthread.h>
#include <span>
#include <stdexcept>
#include <string>
#include <thread>
#include <unistd.h>
#include <utility>
#include <variant>
#include <vector>

namespace recsum {

// ------------------------------------------------------------------------------------------------ result type
// Why not return a bare long long?  The three bad options are: throw (callers forget), return -1 (a legal sum for ranges
// with negatives) or wrap around (silently wrong).  A variant puts "may overflow" into the type; std::visit with a
// missing branch does not compile.  __int128 plays BigInteger's role: the exact value of every sum here fits (< 2^127).
struct Ok {
    long long value;
    friend bool operator==(const Ok&, const Ok&) = default;
};
struct Overflow {
    __int128 exact;
    friend bool operator==(const Overflow&, const Overflow&) = default;
};
using SumResult = std::variant<Ok, Overflow>;

enum class Width { Int, Long };  // accumulator width; Int makes the overflow happen at n = 65536

/// Checked addition in the given width; std::nullopt means "does not fit".  Operands must already fit the width.
/// Signed overflow is UNDEFINED BEHAVIOUR in C++, so the check has to be done by the builtin, never "after the fact".
inline std::optional<long long> add(Width w, long long a, long long b) {
    long long s;
    if (__builtin_add_overflow(a, b, &s)) return std::nullopt;
    if (w == Width::Int && (s < INT_MIN || s > INT_MAX)) return std::nullopt;
    return s;
}

/// Exact 1+2+...+n.  n*(n+1) < 2^126 for every n <= LLONG_MAX, so it fits __int128.
inline __int128 exact_to(long long n) {
    const __int128 bn = n;
    return bn * (bn + 1) / 2;
}

inline void require_non_negative(long long n) {
    if (n < 0) throw std::invalid_argument("n must be >= 0: " + std::to_string(n));
}

// ------------------------------------------------------------------------------------------------ Part 1
namespace detail {
// The addition happens AFTER the recursive call returns, so every frame must stay alive: this is not a tail call.
inline std::optional<long long> add_up(long long n, Width w) {
    if (n == 0) return 0;
    std::optional<long long> rest = add_up(n - 1, w);
    if (!rest) return std::nullopt;
    return add(w, n, *rest);
}
}  // namespace detail

/// sum(n) = n + sum(n-1).  Stack depth = n.  A stack overflow is a SIGSEGV in C++, not an exception: it cannot be caught.
inline SumResult sum_recursive(long long n, Width w) {
    require_non_negative(n);
    if (auto r = detail::add_up(n, w)) return Ok{*r};
    return Overflow{exact_to(n)};
}

// ------------------------------------------------------------------------------------------------ Part 2
namespace detail {
struct Probe {
    const char* base;
    std::size_t budget;
};
// noinline + the asm barrier after the call keep this a genuine non-tail recursion; otherwise -O2 turns it into a loop.
[[gnu::noinline]] inline int dive(const Probe& p, int depth) {
    const char* here = static_cast<const char*>(__builtin_frame_address(0));
    if (static_cast<std::size_t>(p.base - here) >= p.budget) return depth;
    int deepest = dive(p, depth + 1);
    asm volatile("" ::: "memory");
    return deepest;
}
struct Job {
    std::function<void()> fn;
};
}  // namespace detail

/// Run fn on a new thread whose stack is `bytes` big.  std::thread cannot choose its stack size; pthread attributes can.
inline void run_with_stack(std::size_t bytes, std::function<void()> fn) {
    detail::Job job{std::move(fn)};
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    const auto page = static_cast<std::size_t>(sysconf(_SC_PAGESIZE));
    pthread_attr_setstacksize(&attr, (bytes + page - 1) / page * page);
    pthread_t th;
    int rc = pthread_create(&th, &attr, [](void* p) -> void* { static_cast<detail::Job*>(p)->fn(); return nullptr; }, &job);
    pthread_attr_destroy(&attr);
    if (rc != 0) throw std::runtime_error("pthread_create failed: " + std::to_string(rc));
    pthread_join(th, nullptr);
}

/// How deep can plain recursion go on a thread with `stack_bytes` of stack?  We cannot recurse until the crash (a stack
/// overflow kills the process), so we stop 32 KiB (or half the stack, if smaller) before the end and report the depth.
inline int measure_depth(std::size_t stack_bytes) {
    const std::size_t margin = std::min<std::size_t>(32 * 1024, stack_bytes / 2);
    int depth = 0;
    run_with_stack(stack_bytes, [&] {
        const char* base = static_cast<const char*>(__builtin_frame_address(0));
        depth = detail::dive(detail::Probe{base, stack_bytes - margin}, 0);
    });
    return depth;
}

/// Iterative version: O(1) stack.  One local (acc) is all the "waiting" state the recursion kept in its frames.
inline SumResult sum_iterative(long long n, Width w) {
    require_non_negative(n);
    long long acc = 0;
    for (long long i = 1; i <= n; ++i) {
        auto next = add(w, acc, i);
        if (!next) return Overflow{exact_to(n)};
        acc = *next;
    }
    return Ok{acc};
}

/// Trampoline: either finished (done) or "here is the next step" (more).  Every step returns immediately (its frame is
/// popped) and hands back a small heap-or-inline object; run() loops.  Stack depth is constant.
template <class T>
class Trampoline {
public:
    using Next = std::function<Trampoline()>;  // std::function<R()> may name a still-incomplete R

    static Trampoline done(T value) { return Trampoline(std::in_place_index<0>, std::move(value)); }
    static Trampoline more(Next next) { return Trampoline(std::in_place_index<1>, std::move(next)); }

    bool is_done() const { return state_.index() == 0; }
    T take() && { return std::move(std::get<0>(state_)); }
    Trampoline step() const { return std::get<1>(state_)(); }

private:
    // Not a variadic `Trampoline(A&&...)`: that would out-compete the copy constructor for non-const lvalues.
    template <std::size_t I, class A>
    Trampoline(std::in_place_index_t<I> tag, A&& a) : state_(tag, std::forward<A>(a)) {}
    std::variant<T, Next> state_;
};

/// Run a trampoline: a loop, no recursion.  `cur = cur.step()` is safe: step() has returned before the assignment
/// destroys the std::function it was called through.
template <class T>
T run(Trampoline<T> cur) {
    while (!cur.is_done()) cur = cur.step();
    return std::move(cur).take();
}

namespace detail {
using SumTramp = Trampoline<std::optional<long long>>;
// Tail-recursive form: `acc` carries the sum so far, the recursive call is the last thing that happens.
inline SumTramp step(long long n, long long acc, Width w) {
    if (n == 0) return SumTramp::done(acc);
    auto next = add(w, acc, n);
    if (!next) return SumTramp::done(std::nullopt);
    return SumTramp::more([n, w, a = *next] { return step(n - 1, a, w); });
}
inline Trampoline<bool> odd(long long n);
inline Trampoline<bool> even(long long n) {
    return n == 0 ? Trampoline<bool>::done(true) : Trampoline<bool>::more([n] { return odd(n - 1); });
}
inline Trampoline<bool> odd(long long n) {
    return n == 0 ? Trampoline<bool>::done(false) : Trampoline<bool>::more([n] { return even(n - 1); });
}
// Plain tail recursion.  Clang/GCC at -O1+ usually turn this into a loop; the standard does not promise it.
inline std::optional<long long> tail(long long n, long long acc, Width w) {
    if (n == 0) return acc;
    auto next = add(w, acc, n);
    if (!next) return std::nullopt;
    return tail(n - 1, *next, w);
}
}  // namespace detail

inline SumResult sum_trampoline(long long n, Width w) {
    require_non_negative(n);
    if (auto r = run(detail::step(n, 0, w))) return Ok{*r};
    return Overflow{exact_to(n)};
}

/// Mutual recursion is_even/is_odd: not even a self tail call, a trampoline handles it all the same.
inline bool is_even(long long n) {
    require_non_negative(n);
    return run(detail::even(n));
}

/// Tail-recursive source form, left to the optimiser.  Correct everywhere; stack-safe only if the compiler says so.
inline SumResult sum_tail_recursive(long long n, Width w) {
    require_non_negative(n);
    if (auto r = detail::tail(n, 0, w)) return Ok{*r};
    return Overflow{exact_to(n)};
}

// ------------------------------------------------------------------------------------------------ Part 3
/// The classic wrong answer, made well-defined: in Java `n * (n + 1) / 2` wraps; in C++ the same signed expression is
/// UB, so the wrap is spelled out with unsigned arithmetic (modular since forever) and a conversion that is modular
/// since C++20.  n = 2^32 - 1: n*(n+1) = 2^64 - 2^32 wraps to a negative long long, and the result is -2^31.
inline long long naive_closed_form(long long n) {
    const auto un = static_cast<unsigned long long>(n);
    const auto wrapped = static_cast<long long>(un * (un + 1));
    return wrapped / 2;
}

/// Exact a+(a+1)+...+b.  |(a+b)*(b-a+1)| <= 2^126 + 2^63 < 2^127, so one __int128 multiplication cannot overflow, and the
/// product is always even (one factor is even), so the division by 2 is exact.
inline __int128 range_sum_exact(long long a, long long b) {
    if (a > b) throw std::invalid_argument("a > b: " + std::to_string(a) + " > " + std::to_string(b));
    return (static_cast<__int128>(a) + b) * (static_cast<__int128>(b) - a + 1) / 2;
}

inline SumResult range_sum(long long a, long long b) {
    const __int128 exact = range_sum_exact(a, b);
    if (exact >= LLONG_MIN && exact <= LLONG_MAX) return Ok{static_cast<long long>(exact)};
    return Overflow{exact};
}

// ------------------------------------------------------------------------------------------------ Part 4
/// 128-bit accumulator.  Addition is associative, so any chunking and any merge order give the same answer; the
/// overflow decision is taken once, at the end.  (Per-step checked adds depend on the order: {MAX, 1, -1}.)
struct Wide {
    __int128 v = 0;
    static Wide zero() { return {}; }
    Wide plus(long long x) const { return Wide{v + x}; }
    Wide merge(const Wide& o) const { return Wide{v + o.v}; }
    bool fits_long() const { return v >= LLONG_MIN && v <= LLONG_MAX; }
    __int128 exact() const { return v; }
    SumResult to_result() const { return fits_long() ? SumResult{Ok{static_cast<long long>(v)}} : SumResult{Overflow{v}}; }
    friend bool operator==(const Wide&, const Wide&) = default;
};

/// Hot loop: a local __int128 lives in two registers; no objects, no calls.
inline Wide sum_chunk(std::span<const long long> data) {
    __int128 acc = 0;
    for (long long x : data) acc += x;
    return Wide{acc};
}

inline SumResult checked_sum(std::span<const long long> data) { return sum_chunk(data).to_result(); }

namespace detail {
inline Wide fork_join(std::span<const long long> d, std::size_t threshold, int spawn_levels) {
    if (d.size() <= threshold) return sum_chunk(d);
    const std::size_t mid = d.size() / 2;  // size_t cannot go negative; with `int` indices (lo + hi) / 2 overflows on big arrays
    const auto left = d.first(mid), right = d.subspan(mid);
    if (spawn_levels <= 0) return fork_join(left, threshold, 0).merge(fork_join(right, threshold, 0));
    // No work-stealing pool in the standard library: a thread per node would be 100,000 threads for threshold = 1,
    // so only the top levels get a thread (about 2 * cores tasks); below that it is plain recursion.
    auto spawned = std::async(std::launch::async, [=] { return fork_join(left, threshold, spawn_levels - 1); });
    const Wide mine = fork_join(right, threshold, spawn_levels - 1);
    return spawned.get().merge(mine);  // get() rethrows a worker's exception here
}
}  // namespace detail

inline std::size_t hardware_threads() { return std::max(1u, std::thread::hardware_concurrency()); }

inline SumResult parallel_sum_fork_join(std::span<const long long> data, std::size_t threshold) {
    if (threshold < 1) throw std::invalid_argument("threshold < 1");
    const int levels = std::bit_width(hardware_threads());
    return detail::fork_join(data, threshold, levels).to_result();
}

namespace detail {
inline std::span<const long long> chunk_of(std::span<const long long> d, std::size_t chunk, std::size_t size) {
    const std::size_t from = std::min(d.size(), chunk * size), to = std::min(d.size(), (chunk + 1) * size);
    return d.subspan(from, to - from);
}
inline std::size_t ceil_div(std::size_t a, std::size_t b) { return a / b + (a % b != 0); }
}  // namespace detail

/// One std::async per chunk, hardware_threads()*4 chunks (the parallel-stream analogue).
inline SumResult parallel_sum_async(std::span<const long long> data) {
    const std::size_t chunks = hardware_threads() * 4;
    const std::size_t size = detail::ceil_div(data.size(), chunks);
    std::vector<std::future<Wide>> parts;
    parts.reserve(chunks);
    for (std::size_t i = 0; i < chunks; ++i)
        parts.push_back(std::async(std::launch::async, [=] { return sum_chunk(detail::chunk_of(data, i, size)); }));
    Wide total = Wide::zero();
    for (auto& p : parts) total = total.merge(p.get());
    return total.to_result();
}

namespace detail {
struct JoinAll {  // a joinable std::thread destroyed without join() calls std::terminate: join on every exit path
    std::vector<std::thread> threads;
    ~JoinAll() { for (auto& t : threads) if (t.joinable()) t.join(); }
};
}  // namespace detail

/// `chunks` pieces of work, at most hardware_threads() OS threads pulling chunk numbers from an atomic counter.
/// This is what "a virtual thread per chunk" becomes in C++: there are no cheap threads, so you size the pool yourself.
inline SumResult parallel_sum_workers(std::span<const long long> data, std::size_t chunks) {
    if (chunks < 1) throw std::invalid_argument("chunks < 1");
    const std::size_t size = detail::ceil_div(data.size(), chunks);
    std::vector<Wide> parts(chunks);  // slot i is written by exactly one worker: no data race, no lock
    std::atomic<std::size_t> next{0};
    {
        detail::JoinAll pool;
        const std::size_t workers = std::min(chunks, hardware_threads());
        for (std::size_t w = 0; w < workers; ++w)
            pool.threads.emplace_back([&] {
                for (std::size_t i; (i = next.fetch_add(1, std::memory_order_relaxed)) < chunks;)
                    parts[i] = sum_chunk(detail::chunk_of(data, i, size));
            });
    }  // ~JoinAll joins; thread join() is the synchronisation that makes `parts` visible to us
    Wide total = Wide::zero();
    for (const Wide& p : parts) total = total.merge(p);
    return total.to_result();
}

}  // namespace recsum
