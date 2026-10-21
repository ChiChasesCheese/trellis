// Branch prediction: the same loop on random vs sorted data; and a branchless rewrite.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>

template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

// Written so the branch survives: each hit pushes into a vector (a side effect the compiler cannot turn into a select).
__attribute__((noinline)) std::size_t collect_big(const std::vector<int>& v, std::vector<int>& out) {
    out.clear();
    for (int x : v) if (x >= 128) out.push_back(x);
    return out.size();
}
// Branchless: always write, advance the cursor by 0 or 1.
__attribute__((noinline)) std::size_t collect_big_branchless(const std::vector<int>& v, std::vector<int>& out) {
    out.resize(v.size());
    std::size_t k = 0;
    for (int x : v) { out[k] = x; k += (x >= 128); }
    return k;
}

int main() {
    std::mt19937 rng(5);
    std::vector<int> data(20'000'000);
    for (int& x : data) x = static_cast<int>(rng() % 256);
    auto sorted = data;
    std::sort(sorted.begin(), sorted.end());
    std::vector<int> out; out.reserve(data.size());
    std::size_t n1 = 0, n2 = 0, n3 = 0;
    double t_rand = ms([&] { n1 = collect_big(data, out); });
    double t_sorted = ms([&] { n2 = collect_big(sorted, out); });
    double t_bl = ms([&] { n3 = collect_big_branchless(data, out); });
    std::printf("same count of hits: %s\n", (n1 == n3 && n1 == n2) ? "yes" : "no");
    std::printf("branchy, random data  : %6.1f ms\n", t_rand);
    std::printf("branchy, sorted data  : %6.1f ms\n", t_sorted);
    std::printf("branchless, random    : %6.1f ms\n", t_bl);
}
