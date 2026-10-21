// EXPECT: run-fail
// C06: std::accumulate's accumulator type is the TYPE OF THE INIT VALUE, not the element type or the destination.
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> big(10, 1'000'000'000);
    long long wrong = std::accumulate(big.begin(), big.end(), 0);      // 0 is an int: every partial sum is an int
    std::cout << "sum with int init: " << wrong << "  (signed overflow = undefined behaviour)\n";
}
