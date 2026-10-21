// STD: c++17
// C++17: the big usability release. Library vocabulary types and compile-time branching.
#include <algorithm>
#include <charconv>
#include <iostream>
#include <map>
#include <numeric>
#include <optional>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <variant>
#include <vector>

namespace trading::risk { inline constexpr int kMaxQty = 1000; }      // nested namespaces, inline variables

// [[snip:vocab]]
std::optional<int> parse_int(std::string_view s) {                    // optional: "maybe a value" without null or sentinel
    int v = 0;
    auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), v);   // structured binding of a struct
    if (ec != std::errc{} || ptr != s.data() + s.size()) return std::nullopt;
    return v;
}

using Msg = std::variant<int, double, std::string>;                   // variant: a type-safe union (Java: sealed interface)
struct Visitor {
    std::string operator()(int i) const { return "int " + std::to_string(i); }
    std::string operator()(double d) const { return "double " + std::to_string(d); }
    std::string operator()(const std::string& s) const { return "string " + s; }
};
// [[/snip]]

// [[snip:constexpr_if]]
template <typename T>
auto to_text(const T& v) {
    if constexpr (std::is_arithmetic_v<T>) return std::to_string(v);  // compile-time branch, replaces SFINAE tricks
    else return std::string(v);
}
// [[/snip]]

[[nodiscard]] int must_use() { return 1; }

int main() {
    // [[snip:init]]
    std::map<std::string, int> m;
    if (auto [it, inserted] = m.try_emplace("AAPL", 100); inserted)    // if-with-initializer + structured bindings
        std::cout << "  inserted " << it->first << "=" << it->second << "\n";
    m.insert_or_assign("AAPL", 150);
    for (const auto& [sym, qty] : m) std::cout << "  " << sym << " -> " << qty << "\n";
    // [[/snip]]

    std::cout << "  parse 42: " << parse_int("42").value_or(-1) << ", parse x: " << parse_int("x").value_or(-1) << "\n";
    std::vector<Msg> msgs{1, 2.5, std::string("hi")};
    for (const auto& mm : msgs) std::cout << "  " << std::visit(Visitor{}, mm) << "\n";
    std::cout << "  " << to_text(12) << " " << to_text("txt") << "\n";

    // [[snip:ctad]]
    std::pair p(1, 2.5);                                              // CTAD: no need to write pair<int,double>
    std::tuple t(1, 'c', std::string("s"));
    std::vector<int> nums{1, 2, 3};
    auto total = std::reduce(nums.begin(), nums.end());               // <numeric>: reduce (also has parallel overloads)
    // [[/snip]]
    std::cout << "  " << p.first << " " << std::get<1>(t) << " " << total << "\n";
    std::cout << "  gcd " << std::gcd(12, 18) << " lcm " << std::lcm(4, 6) << " clamp " << std::clamp(15, 0, 10) << " max qty " << trading::risk::kMaxQty << "\n";
    (void)must_use();                                                 // [[nodiscard]]: ignoring the result would warn
}
