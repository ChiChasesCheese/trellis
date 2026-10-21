// C++20: concepts, ranges, coroutines, <=>, designated initialisers, span, format, jthread, bit ops, constexpr containers.
#include <algorithm>
#include <bit>
#include <compare>
#include <concepts>
#include <coroutine>
#include <format>
#include <iostream>
#include <latch>
#include <numeric>
#include <ranges>
#include <span>
#include <string>
#include <thread>
#include <utility>
#include <vector>

// [[snip:spaceship]]
struct Version {
    int major, minor, patch;
    auto operator<=>(const Version&) const = default;      // one line generates <, <=, >, >=, ==, != (lexicographic)
};
// [[/snip]]

// [[snip:designated]]
struct Config { int threads = 1; bool verbose = false; double timeout = 1.5; };
// [[/snip]]

// [[snip:coro]]
// A minimal generator (C++20 gives you the machinery, not the library type; C++23 adds std::generator).
template <typename T>
struct Generator {
    struct promise_type {
        T current{};
        Generator get_return_object() { return Generator{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) noexcept { current = v; return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    std::coroutine_handle<promise_type> h;
    explicit Generator(std::coroutine_handle<promise_type> hh) : h(hh) {}
    Generator(Generator&& o) noexcept : h(std::exchange(o.h, {})) {}
    ~Generator() { if (h) h.destroy(); }
    bool next() { h.resume(); return !h.done(); }
    T value() const { return h.promise().current; }
};

Generator<int> fibs() {
    int a = 0, b = 1;
    for (;;) { co_yield a; int t = a + b; a = b; b = t; }     // suspends here; resumes on the next next()
}
// [[/snip]]

// [[snip:constexpr_vec]]
constexpr int sum_squares(int n) {
    std::vector<int> v;                                       // std::vector / std::string usable at compile time (C++20)
    for (int i = 1; i <= n; ++i) v.push_back(i * i);
    return std::accumulate(v.begin(), v.end(), 0);
}
static_assert(sum_squares(10) == 385);
// [[/snip]]

template <typename T> concept Small = sizeof(T) <= 8;

int main() {
    Version a{1, 2, 3}, b{1, 10, 0};
    std::cout << "  1.2.3 < 1.10.0: " << (a < b) << ", equal: " << (a == b) << "\n";

    Config c{.threads = 8, .timeout = 0.25};                  // designated initialisers (order must match declaration)
    std::cout << "  " << std::format("threads={} verbose={} timeout={}", c.threads, c.verbose, c.timeout) << "\n";

    std::vector<int> v{5, 3, 9, 1, 7};
    std::span<int> window(v.data() + 1, 3);                   // span: non-owning (pointer, length) view
    std::ranges::sort(window);
    auto evens = v | std::views::filter([](int x) { return x % 2 == 0; });
    std::cout << "  window sorted -> ";
    for (int x : v) std::cout << x << " ";
    std::cout << "(evens: " << std::ranges::distance(evens) << ")\n";

    auto g = fibs();
    std::cout << "  coroutine fibs:";
    for (int i = 0; i < 10 && g.next(); ++i) std::cout << " " << g.value();
    std::cout << "\n";

    std::cout << "  popcount(0b1011)=" << std::popcount(0b1011u) << " bit_width(255)=" << std::bit_width(255u)
              << " countl_zero(1u)=" << std::countl_zero(1u) << " bit_ceil(100)=" << std::bit_ceil(100u) << "\n";
    std::cout << "  constexpr vector: sum of squares 1..10 = " << sum_squares(10) << ", Small<int>=" << Small<int> << "\n";

    std::latch done(2);                                       // latch / barrier / semaphore
    {
        std::jthread t1([&] { done.count_down(); });          // jthread joins in its destructor
        std::jthread t2([&] { done.count_down(); });
        done.wait();
    }
    std::vector<int> w{1, 2, 3, 4, 5};
    std::erase_if(w, [](int x) { return x % 2; });            // uniform erase for all containers
    std::cout << "  ssize=" << std::ssize(w) << " after erase_if(odd), ranges::find(4) found: " << (std::ranges::find(w, 4) != w.end()) << "\n";
}
