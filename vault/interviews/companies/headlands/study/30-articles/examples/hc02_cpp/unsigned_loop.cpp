// Counting down with an unsigned index: `i >= 0` is always true, and n / 2 - 1 wraps when n == 0.
#include <cstddef>
#include <iostream>

int main() {
    const std::size_t n = 7;
    // for (std::size_t i = n / 2 - 1; i >= 0; --i) { ... }   // never ends: after 0 comes 18446744073709551615
    std::cout << "indices n/2-1 .. 0:";
    for (std::size_t i = n / 2; i-- > 0;) std::cout << ' ' << i;  // test, THEN decrement
    std::cout << "\n";

    const std::size_t empty = 0;
    std::cout << "empty / 2 - 1 = " << (empty / 2 - 1) << "   (wrapped)\n";
    std::size_t visited = 0;
    for (std::size_t i = empty / 2; i-- > 0;) ++visited;  // n == 0 is handled without a special case
    std::cout << "visited " << visited << "\n";
}
