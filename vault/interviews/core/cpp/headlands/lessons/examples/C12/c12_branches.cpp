// SAN: none
// C12: the CPU is part of "why C++ is fast": same loop, sorted vs random data -> branch predictor.
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

// [[snip:loop]]
[[gnu::noinline]] long sum_if_big(const std::vector<int>& v, std::vector<int>& out) {
    long t = 0;
    out.clear();
    for (int x : v) { if (x >= 128) { t += x; out.push_back(x); } }       // data-dependent branch with a side effect
    return t;
}
// [[/snip]]

int main() {
    const std::size_t N = std::getenv("QUICK") ? 100'000 : 20'000'000;
    std::mt19937 rng(5);
    std::vector<int> v(N);
    for (auto& x : v) x = static_cast<int>(rng() % 256);
    std::vector<int> tmp;
    tmp.reserve(N);
    auto time = [&](const char* name) {
        auto t0 = std::chrono::steady_clock::now();
        long s = 0;
        for (int r = 0; r < 3; ++r) s += sum_if_big(v, tmp);
        std::cout << "  " << name << ": " << std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / 3.0 / static_cast<double>(N)
                  << " ns/element (sum " << s % 10 << ")\n";
    };
    time("random data");
    std::sort(v.begin(), v.end());
    time("sorted data");
}
