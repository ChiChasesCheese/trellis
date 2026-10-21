// C07: constexpr / consteval / constinit: move work from run time to compile time.
#include <array>
#include <cstdint>
#include <iostream>

// [[snip:fn]]
constexpr std::uint64_t fib(int n) {                   // an ordinary function that MAY run at compile time
    std::uint64_t a = 0, b = 1;
    for (int i = 0; i < n; ++i) { auto t = a + b; a = b; b = t; }
    return a;
}
static_assert(fib(50) == 12586269025ULL, "checked by the compiler, costs nothing at run time");
// [[/snip]]

// [[snip:table]]
constexpr std::array<std::uint32_t, 16> make_squares() {     // a lookup table baked into the binary
    std::array<std::uint32_t, 16> t{};
    for (std::uint32_t i = 0; i < t.size(); ++i) t[i] = i * i;
    return t;
}
constexpr auto kSquares = make_squares();
static_assert(kSquares[15] == 225);

constexpr bool is_prime(int n) {
    if (n < 2) return false;
    for (int d = 2; d * d <= n; ++d) if (n % d == 0) return false;
    return true;
}
constexpr int count_primes_below(int n) { int c = 0; for (int i = 2; i < n; ++i) c += is_prime(i); return c; }
constexpr int kPrimesBelow1000 = count_primes_below(1000);     // evaluated by the compiler
// [[/snip]]

// [[snip:consteval]]
consteval int must_be_compile_time(int x) { return x * 2; }    // C++20: calling at run time is a compile error
constinit int g_counter = 100;                                  // C++20: constant-initialised, but mutable (no init-order fiasco)
// [[/snip]]

int main() {
    std::cout << "fib(50)=" << fib(50) << " (also usable with run-time n: fib(10)=" << fib(10) << ")\n";
    std::cout << "squares[7]=" << kSquares[7] << " primes below 1000: " << kPrimesBelow1000 << "\n";
    constexpr int k = must_be_compile_time(21);
    std::cout << "consteval gave " << k << ", constinit counter " << ++g_counter << "\n";
    int runtime_n = 0;
    std::cin >> runtime_n;                                       // stdin is empty in the build script -> stays 0
    // must_be_compile_time(runtime_n);                          // error: not a constant expression
    std::cout << "runtime_n=" << runtime_n << " fib=" << fib(runtime_n) << "\n";
}
