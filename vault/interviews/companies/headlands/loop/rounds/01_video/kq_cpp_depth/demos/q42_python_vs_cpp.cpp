// Things that differ between Python and C++ in plain arithmetic, plus a timing loop (see q42_loop.py for the Python twin).
#include <chrono>
#include <climits>
#include <cstdint>
#include <cstdio>

long long collatz_total(int limit) {
    long long steps = 0;
    for (int n = 1; n <= limit; ++n) {
        long long x = n;
        while (x != 1) { x = (x & 1) ? 3 * x + 1 : x / 2; ++steps; }
    }
    return steps;
}
int main(int argc, char**) {
    std::printf("7 / 2 = %d (Python: 3.5; // gives 3)\n", 7 / 2);
    std::printf("-7 / 2 = %d, -7 %% 2 = %d (Python: -4 and 1: floors)\n", -7 / 2, -7 % 2);
    std::uint32_t u = 0; --u;
    std::printf("unsigned 0 - 1 = %u (Python has no wraparound)\n", u);
    std::int64_t big = INT64_MAX - 1 + argc;
    std::uint64_t wrapped = static_cast<std::uint64_t>(big) + 1;
    std::printf("INT64_MAX + 1 as unsigned wraps to %llu (Python int never overflows)\n", static_cast<unsigned long long>(wrapped));
    std::printf("0.1 + 0.2 == 0.3 ? %d (same in both languages)\n", 0.1 + 0.2 == 0.3);
    std::printf("sizeof: int=%zu long=%zu long long=%zu float=%zu double=%zu\n", sizeof(int), sizeof(long), sizeof(long long), sizeof(float), sizeof(double));

    auto t0 = std::chrono::steady_clock::now();
    long long total = collatz_total(300000);
    double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
    std::printf("collatz total steps (1..300000) = %lld in %.0f ms\n", total, ms);
}
