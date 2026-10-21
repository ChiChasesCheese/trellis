// Signed overflow is undefined behaviour in C++.  Three correct ways to add with a check.
#include <climits>
#include <iostream>
#include <optional>

// 1. The compiler builtin (clang, gcc): the best answer.
std::optional<long long> add_builtin(long long a, long long b) {
    long long s;
    if (__builtin_add_overflow(a, b, &s)) return std::nullopt;
    return s;
}

// 2. Test BEFORE adding, using only operations that cannot overflow.
std::optional<long long> add_precheck(long long a, long long b) {
    if (b > 0 && a > LLONG_MAX - b) return std::nullopt;
    if (b < 0 && a < LLONG_MIN - b) return std::nullopt;
    return a + b;
}

// 3. Widen: the exact sum of two long longs always fits __int128.
std::optional<long long> add_wide(long long a, long long b) {
    __int128 s = static_cast<__int128>(a) + b;
    if (s < LLONG_MIN || s > LLONG_MAX) return std::nullopt;
    return static_cast<long long>(s);
}

int main() {
    for (auto f : {add_builtin, add_precheck, add_wide}) {
        auto r1 = f(LLONG_MAX, 1), r2 = f(LLONG_MIN, -1), r3 = f(LLONG_MAX, LLONG_MIN);
        std::cout << r1.has_value() << r2.has_value() << (r3 ? *r3 : 0) << "\n";   // 0 0 -1
    }
}
