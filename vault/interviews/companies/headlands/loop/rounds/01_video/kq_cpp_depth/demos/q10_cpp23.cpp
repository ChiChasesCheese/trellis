// C++23 (compile with -std=c++23): expected, print, deducing this, ranges::to, unreachable.
#include <expected>
#include <print>
#include <ranges>
#include <string>
#include <vector>

enum class Err { Empty, TooBig };
std::expected<int, Err> parse_qty(const std::string& s) {
    if (s.empty()) return std::unexpected(Err::Empty);
    int v = std::stoi(s);
    if (v > 1000) return std::unexpected(Err::TooBig);
    return v;
}
struct Counter {
    int n = 0;
    int get(this const Counter& self) { return self.n; }       // explicit object parameter
};
int main() {
    for (const char* s : {"250", "", "5000"}) {
        auto r = parse_qty(s);
        if (r) std::println("ok {}", *r); else std::println("error {}", static_cast<int>(r.error()));
    }
    auto squares = std::views::iota(1, 6) | std::views::transform([](int x) { return x * x; }) | std::ranges::to<std::vector>();
    std::println("squares: {}", squares);
    std::println("counter: {}", Counter{3}.get());
}
