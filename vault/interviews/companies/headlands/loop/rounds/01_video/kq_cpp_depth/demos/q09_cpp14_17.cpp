// C++14 and C++17 additions that show up in everyday code.
#include <cstdio>
#include <map>
#include <memory>
#include <optional>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <variant>
#include <vector>

// ---- C++14
auto add = [](auto a, auto b) { return a + b; };            // generic lambda
auto twice(int x) { return 2 * x; }                          // return type deduction
constexpr int fact(int n) { int r = 1; for (int i = 2; i <= n; ++i) r *= i; return r; }  // loops in constexpr
template <class T> constexpr T pi_v = T(3.14159265358979L);  // variable template

// ---- C++17
template <class T>
auto describe(const T& x) {
    if constexpr (std::is_integral_v<T>) return std::string("integer ") + std::to_string(x);   // compile-time branch
    else return std::string("other");
}
std::optional<int> parse(std::string_view s) {              // no allocation, no copy of the text
    if (s.empty()) return std::nullopt;
    return static_cast<int>(s.size());
}
struct Print {
    void operator()(int i) const { std::printf("int %d\n", i); }
    void operator()(const std::string& s) const { std::printf("string %s\n", s.c_str()); }
};

int main() {
    std::printf("%d %.1f %d %d\n", add(1, 2), add(1.5, 2.0), twice(4), fact(5));
    auto u = std::make_unique<int>(7);                        // C++14
    std::printf("make_unique -> %d, pi_v<float> = %.3f\n", *u, pi_v<float>);

    std::map<std::string, int> m{{"AAPL", 190}, {"MSFT", 410}};
    for (const auto& [sym, px] : m) std::printf("%s=%d ", sym.c_str(), px);   // structured bindings
    std::printf("\n");
    if (auto it = m.find("AAPL"); it != m.end()) std::printf("found %d\n", it->second);   // init-statement
    std::printf("%s | %s\n", describe(7).c_str(), describe(2.5).c_str());
    auto r = parse("hello");
    std::printf("optional has_value=%d value=%d, empty -> %d\n", r.has_value(), *r, parse("").has_value());
    std::variant<int, std::string> var = std::string("hi");
    std::visit(Print{}, var);
    std::pair p(1, 2.5);                                      // class template argument deduction
    std::vector w{1, 2, 3};                                   // deduces vector<int>
    auto sum_all = [](auto... xs) { return (xs + ...); };    // fold expression
    std::printf("CTAD pair.second=%.1f vector size=%zu fold=%d\n", p.second, w.size(), sum_all(1, 2, 3, 4));
}
