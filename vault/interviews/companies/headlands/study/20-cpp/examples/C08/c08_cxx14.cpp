// STD: c++14
// C++14: a small "bug-fix and polish" release on top of C++11.
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

// [[snip:deduce]]
auto add(int a, int b) { return a + b; }                      // return type deduction for ordinary functions

constexpr int factorial(int n) {                              // relaxed constexpr: loops and locals allowed (C++11: single return)
    int r = 1;
    for (int i = 2; i <= n; ++i) r *= i;
    return r;
}
static_assert(factorial(5) == 120, "");

template <typename T> constexpr T kPi = T(3.1415926535897932385L);   // variable templates
// [[/snip]]

[[deprecated("use add()")]] inline int old_add(int a, int b) { return a + b; }   // using it would warn

int main() {
    // [[snip:lambda]]
    auto gen = [](auto a, auto b) { return a * b; };          // generic lambda: auto parameters
    auto owned = std::make_unique<int>(9);                     // std::make_unique (C++11 had make_shared only)
    auto use = [p = std::move(owned)] { return *p + 1; };      // init-capture: move into a lambda
    std::cout << "  gen " << gen(3, 4) << " " << gen(1.5, 2) << ", init-capture " << use() << "\n";
    // [[/snip]]

    // [[snip:lit]]
    int mask = 0b1010'1010;                                    // binary literals and digit separators
    long big = 1'000'000'000L;
    using namespace std::string_literals;                      // "text"s : std::string literals
    auto s = "abc"s + "def";
    std::cout << "  mask=" << mask << " big=" << big << " s=" << s << " kPi<float>=" << kPi<float> << "\n";
    // [[/snip]]

    // [[snip:exchange]]
    std::vector<int> v{1, 2, 3};
    auto old = std::exchange(v, std::vector<int>{9});          // std::exchange: set a new value, get the old one
    std::cout << "  exchange: old size " << old.size() << ", new size " << v.size() << ", add " << add(2, 3) << "\n";
    // [[/snip]]
}
