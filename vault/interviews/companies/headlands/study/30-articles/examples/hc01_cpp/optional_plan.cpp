// std::optional for "may not exist": a plan that is too big, or a sell day that has not been seen yet.
#include <iostream>
#include <optional>
#include <string>

std::optional<int> plan_cells(long long n, long long w) {
    const long long cells = (n + 1) * w;               // 64-bit product
    if (cells > (1LL << 28)) return std::nullopt;       // too big: not an error in the caller's input, just "no answer"
    return static_cast<int>(cells);
}

int main() {
    if (const auto c = plan_cells(100'000, 100)) std::cout << "100k days, 100 trades: " << *c << " cells\n";
    if (!plan_cells(100'000, 50'000)) std::cout << "100k days, 50k trades: nullopt\n";

    std::optional<int> pending_sell;   // empty until the walk meets a sell
    try {
        std::cout << pending_sell.value() << "\n";       // throws std::bad_optional_access: a bug becomes a loud failure
    } catch (const std::bad_optional_access& e) {
        std::cout << "value() on an empty optional throws: " << e.what() << "  (`*pending_sell` would be undefined behaviour)\n";
    }
}
