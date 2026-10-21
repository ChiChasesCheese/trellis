// Same job, two APIs: std::sort (comparator inlined) vs qsort (function pointer).
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

static int cmp_int(const void* a, const void* b) {
    int x = *static_cast<const int*>(a), y = *static_cast<const int*>(b);
    return (x > y) - (x < y);
}

template <class F>
static double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    std::mt19937 rng(42);
    std::vector<int> base(5'000'000);
    for (int& x : base) x = static_cast<int>(rng());
    auto a = base, b = base;
    double t_std = ms([&] { std::sort(a.begin(), a.end()); });
    double t_qs = ms([&] { std::qsort(b.data(), b.size(), sizeof(int), cmp_int); });
    std::printf("same result: %s\n", a == b ? "yes" : "no");
    std::printf("std::sort : %6.1f ms\n", t_std);
    std::printf("qsort     : %6.1f ms\n", t_qs);
}
