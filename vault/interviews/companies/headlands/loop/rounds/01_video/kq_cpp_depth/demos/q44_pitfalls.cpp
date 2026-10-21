// The small C++ habits that save a live-coding round.
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);                         // faster cin/cout when reading lots of input
    std::cin.tie(nullptr);

    std::vector<int> v;                                       // empty
    std::printf("empty v.size() - 1 = %zu (unsigned wraps: the loop `for (size_t i = v.size()-1; i >= 0; --i)` never ends)\n", v.size() - 1);
    v = {10, 20, 30};
    for (std::size_t i = v.size(); i-- > 0;) std::printf("%d ", v[i]);   // safe reverse loop with an unsigned index
    std::printf("<- reverse\n");

    int a = 2'000'000'000, b = 2'000'000'000;
    long long wide = static_cast<long long>(a) + b;           // widen BEFORE adding
    std::printf("int + int would overflow; as long long: %lld\n", wide);
    int lo = 1'500'000'000, hi = 2'000'000'000;
    std::printf("midpoint: lo + (hi - lo) / 2 = %d\n", lo + (hi - lo) / 2);   // (lo + hi) / 2 overflows

    std::int64_t price_x10000 = 1'902'500;                    // money as integers (190.2500), not floating point
    std::printf("price = %lld.%04lld\n", static_cast<long long>(price_x10000 / 10000), static_cast<long long>(price_x10000 % 10000));

    for (const auto& x : v) std::printf("%d ", x);            // const auto& in range-for: no copies
    std::printf("\n");
}
