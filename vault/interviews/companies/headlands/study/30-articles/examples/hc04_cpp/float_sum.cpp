// Why the running sum is an integer: a double running sum forgets small values next to a big one.
#include <iomanip>
#include <iostream>

int main() {
    double running = 0;
    running += 1e16;
    running += 1;      // 1e16 + 1 is not representable (spacing is 2): rounds back to 1e16
    running += 1;
    running -= 1e16;   // "the big element left the queue"
    std::cout << "double running sum after pop: " << running << "   (exact answer: 2)\n";

    long long exact = 0;
    exact += 10'000'000'000'000'000LL;
    exact += 1;
    exact += 1;
    exact -= 10'000'000'000'000'000LL;
    std::cout << "integer running sum after pop: " << exact << "\n";

    // Converting the final fraction: (2^53 + 1) / 1 is a tie between two doubles; one rounding, half to even.
    long long v = (1LL << 53) + 1;
    std::cout << std::setprecision(17) << "(2^53+1) as double = " << static_cast<double>(v) << "\n";
}
