// Signed overflow is undefined behaviour; unsigned wraps.  __builtin_mul_overflow reports the overflow without invoking UB.
#include <climits>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error(std::to_string(a) + " * " + std::to_string(b));
    return r;
}

int main() {
    const long long a = LLONG_MAX, b = 2;
    // The wrong way, made visible without UB: do the product in unsigned 64-bit arithmetic and reinterpret.
    const auto wrapped = static_cast<long long>(static_cast<unsigned long long>(a) * static_cast<unsigned long long>(b));
    std::cout << "LLONG_MAX * 2 wrapped to " << wrapped << " (a negative notional)\n";
    // The right way.
    try {
        (void)mul_exact(a, b);
    } catch (const std::overflow_error& e) {
        std::cout << "mul_exact threw overflow_error: " << e.what() << "\n";
    }
    std::cout << "3037000499^2 = " << mul_exact(3037000499LL, 3037000499LL) << "\n";
    try {
        (void)mul_exact(3037000500LL, 3037000500LL);
    } catch (const std::overflow_error&) {
        std::cout << "3037000500^2 overflows\n";
    }
    // int * int is also signed: price (int) * volume (int) overflows at 46341 * 46341, even if the result is stored in a long long.
    const int p = 46341, v = 46341;
    int as_int;
    std::cout << "46341 * 46341 overflows int: " << (__builtin_mul_overflow(p, v, &as_int) ? "yes" : "no") << "\n";
    std::cout << "as long long: " << static_cast<long long>(p) * v << "\n";
}
