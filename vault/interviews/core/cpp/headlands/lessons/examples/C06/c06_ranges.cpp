// C06: C++20 ranges: lazy views composed with |, projections in algorithms. Java Streams, minus allocation and boxing.
#include <algorithm>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

namespace rv = std::views;
namespace rg = std::ranges;

struct Fill { std::string sym; long qty; };

int main() {
    // [[snip:pipeline]]
    std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto pipeline = v | rv::filter([](int x) { return x % 2 == 0; })
                      | rv::transform([](int x) { return x * x; })
                      | rv::take(3);                          // NOTHING has run yet: views are lazy descriptions
    std::cout << "  squares of the first three evens:";
    for (int x : pipeline) std::cout << " " << x;             // the work happens here, element by element, no temp vectors
    std::cout << "\n";
    // [[/snip]]

    // [[snip:iota]]
    long total = 0;
    for (long i : rv::iota(1, 1'000'001) | rv::filter([](long i) { return i % 3 == 0; })) total += i;   // no vector of 1M ints
    std::cout << "  sum of multiples of 3 up to 1,000,000: " << total << "\n";
    // [[/snip]]

    // [[snip:projection]]
    std::vector<Fill> fills{{"MSFT", 50}, {"AAPL", 100}, {"NVDA", 10}};
    rg::sort(fills, {}, &Fill::qty);                          // sort by a member: comparator-free projection
    std::cout << "  by qty:";
    for (auto& f : fills) std::cout << " " << f.sym;
    auto it = rg::find(fills, "AAPL", &Fill::sym);
    std::cout << "; AAPL at index " << it - fills.begin() << "\n";
    auto mx = rg::max_element(fills, {}, &Fill::qty);
    std::cout << "  max qty: " << mx->sym << "\n";
    // [[/snip]]

    // [[snip:dangling]]
    auto bad = rg::find(std::vector<int>{1, 2, 3}, 2);        // temporary container: result is rg::dangling, not an iterator
    static_assert(std::is_same_v<decltype(bad), rg::dangling>);
    std::cout << "  find on a temporary returns ranges::dangling (use of it will not compile)\n";
    // [[/snip]]

    // [[snip:strings]]
    std::string csv = "AAPL,MSFT,NVDA";
    std::cout << "  split:";
    for (auto part : csv | rv::split(',')) std::cout << " [" << std::string(part.begin(), part.end()) << "]";
    std::cout << "\n  reversed keys:";
    for (int x : v | rv::reverse | rv::take(3)) std::cout << " " << x;
    std::cout << "\n";
    // [[/snip]]
}
