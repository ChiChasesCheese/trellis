// STD: c++23
// C++23 peek: what the NEXT standard adds. Not asked in the report, worth one sentence if the interviewer pushes.
#include <expected>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

// [[snip:expected]]
std::expected<int, std::string> parse_qty(const std::string& s) {      // result-or-error without exceptions (Java: Result<T,E>)
    try { return std::stoi(s); } catch (...) { return std::unexpected("bad qty: " + s); }
}
// [[/snip]]

// [[snip:deducing]]
struct Counter {
    int n = 0;
    template <class Self> auto&& value(this Self&& self) { return std::forward<Self>(self).n; }   // deducing this
};
// [[/snip]]

int main() {
    for (std::string s : {"100", "abc"}) {
        auto r = parse_qty(s);
        if (r) std::cout << "  ok " << *r << "\n"; else std::cout << "  error: " << r.error() << "\n";
    }
    Counter c; c.value() = 5;
    std::vector<int> v{1, 2, 3, 4};
    auto squares = v | std::views::transform([](int x) { return x * x; }) | std::ranges::to<std::vector>();   // ranges::to
    std::cout << "  deducing this: " << c.value() << ", ranges::to size " << squares.size() << "\n";
    for (auto [a, b] : std::views::zip(v, squares)) std::cout << "  " << a << "^2=" << b;
    std::cout << "\n";
    if consteval { } else { std::cout << "  (if consteval compiles)\n"; }
}
