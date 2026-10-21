// SAN: none
// ASM: yes
// C12: zero-cost abstractions: the std algorithm + lambda compiles to the same loop as hand-written code; std::sort beats qsort.
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

// [[snip:three]]
[[gnu::noinline]] long sum_raw(const int* p, std::size_t n) { long t = 0; for (std::size_t i = 0; i < n; ++i) t += p[i]; return t; }
[[gnu::noinline]] long sum_accumulate(const std::vector<int>& v) { return std::accumulate(v.begin(), v.end(), 0L); }
[[gnu::noinline]] long sum_rangefor(const std::vector<int>& v) { long t = 0; for (int x : v) t += x; return t; }
// [[/snip]]

static int cmp_int(const void* a, const void* b) { int x = *static_cast<const int*>(a), y = *static_cast<const int*>(b); return (x > y) - (x < y); }

int main() {
    const std::size_t N = std::getenv("QUICK") ? 100'000 : 5'000'000;
    std::mt19937 rng(11);
    std::vector<int> base(N);
    for (auto& x : base) x = static_cast<int>(rng() % 1'000'000);

    std::cout << "sums agree: " << (sum_raw(base.data(), N) == sum_accumulate(base) && sum_accumulate(base) == sum_rangefor(base)) << "\n";

    auto time_ms = [](auto&& f) {
        auto t0 = std::chrono::steady_clock::now();
        f();
        return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
    };
    auto a = base, b = base, c = base;
    double t_std = time_ms([&] { std::sort(a.begin(), a.end()); });
    double t_lambda = time_ms([&] { std::sort(b.begin(), b.end(), [](int x, int y) { return x < y; }); });
    double t_qsort = time_ms([&] { std::qsort(c.data(), c.size(), sizeof(int), cmp_int); });
    std::cout << "sort " << N << " ints:  std::sort " << t_std << " ms,  std::sort + lambda " << t_lambda << " ms,  qsort " << t_qsort
              << " ms (qsort/std::sort = " << t_qsort / t_std << "x)\n";
    std::cout << "identical results: " << (a == b && b == c) << "\n";
}
