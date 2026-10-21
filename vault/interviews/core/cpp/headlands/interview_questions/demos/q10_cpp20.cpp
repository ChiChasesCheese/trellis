// C++20 highlights: concepts, ranges, span, <=>, designated initializers, consteval, erase_if, jthread, <bit>.
#include <algorithm>
#include <bit>
#include <compare>
#include <format>
#include <concepts>
#include <cstdio>
#include <ranges>
#include <span>
#include <thread>
#include <vector>

template <std::integral T>                                    // concept constrains T
T gcd_of(T a, T b) { return b == 0 ? a : gcd_of(b, a % b); }

struct Version {
    int major, minor;
    auto operator<=>(const Version&) const = default;         // generates <, >, ==, ... from members
};
struct Params { int depth = 1; double tick = 0.01; };

consteval int cube(int x) { return x * x * x; }               // must run at compile time
int sum(std::span<const int> s) { int t = 0; for (int x : s) t += x; return t; }   // pointer + length view

int main() {
    std::printf("gcd = %d\n", gcd_of(48, 18));
    std::printf("Version{1,2} < Version{1,10}: %d\n", Version{1, 2} < Version{1, 10});
    Params p{.depth = 5};                                     // designated initializer
    std::printf("depth=%d tick=%.2f cube=%d\n", p.depth, p.tick, cube(3));

    std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8};
    auto evens_squared = v | std::views::filter([](int x) { return x % 2 == 0; })
                           | std::views::transform([](int x) { return x * x; });   // lazy pipeline
    for (int x : evens_squared) std::printf("%d ", x);
    std::printf("\n");
    std::printf("span sum = %d (array and vector both bind)\n", sum(v) + sum(std::vector<int>{1}));
    std::erase_if(v, [](int x) { return x % 3 == 0; });
    std::printf("after erase_if: %zu elements\n", v.size());
    std::printf("popcount(255)=%d countl_zero(1u)=%d bit_ceil(100)=%u rotl(0x80000001u,1)=0x%x\n",
                std::popcount(255u), std::countl_zero(1u), std::bit_ceil(100u), std::rotl(0x80000001u, 1));
    std::printf("%s\n", std::format("format: {:>6} | {:08b} | {:.2f}", "px", 37u, 3.14159).c_str());
    std::jthread t([] { std::printf("jthread joins automatically\n"); });
}
