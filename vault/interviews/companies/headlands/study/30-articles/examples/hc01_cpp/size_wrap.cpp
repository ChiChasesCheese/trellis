// Unsigned and signed arithmetic traps around sizes and k.
#include <climits>
#include <iostream>
#include <vector>

int main() {
    const std::vector<long long> empty;
    std::cout << "empty.size() - 1 = " << empty.size() - 1 << "   <- loop `i < size() - 1` would run ~2^64 times\n";

    int k = INT_MAX, k_plus_one = 0;
    const bool overflowed = __builtin_add_overflow(k, 1, &k_plus_one);
    std::cout << "INT_MAX + 1 overflows: " << std::boolalpha << overflowed << "   <- `vector(k + 1)` is signed overflow (UB) for k = INT_MAX\n";

    const long long cells_wrong_if_int = static_cast<long long>(100'001) * 50'000;
    std::cout << "(n + 1) * (k + 1) = " << cells_wrong_if_int << " does not fit in int (max " << INT_MAX << "): form the product in long long\n";
}
