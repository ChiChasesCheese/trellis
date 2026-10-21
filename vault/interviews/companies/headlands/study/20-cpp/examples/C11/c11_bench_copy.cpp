// SAN: none
// C11: speed. For trivially copyable data, std::copy, memcpy and memmove hit the same library routine; a naive loop is optimised to it.
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>

template <class F>
double gb_per_s(std::size_t bytes, int reps, F&& f) {
    f();
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < reps; ++i) f();
    auto t1 = std::chrono::steady_clock::now();
    double s = std::chrono::duration<double>(t1 - t0).count();
    return static_cast<double>(bytes) * reps / s / 1e9;
}

int main() {
    const std::size_t N = std::getenv("QUICK") ? (1u << 16) : (16u << 20);          // 16M ints = 64 MiB
    const int reps = std::getenv("QUICK") ? 4 : 20;
    std::vector<int> src(N, 1), dst(N, 0);
    std::size_t bytes = N * sizeof(int);
    std::cout << "copy " << bytes / (1 << 20) << " MiB of int, GB/s (higher is better)\n";
    std::cout << "  std::copy : " << gb_per_s(bytes, reps, [&] { std::copy(src.begin(), src.end(), dst.begin()); }) << "\n";
    std::cout << "  memcpy    : " << gb_per_s(bytes, reps, [&] { std::memcpy(dst.data(), src.data(), bytes); }) << "\n";
    std::cout << "  memmove   : " << gb_per_s(bytes, reps, [&] { std::memmove(dst.data(), src.data(), bytes); }) << "\n";
    std::cout << "  for loop  : " << gb_per_s(bytes, reps, [&] { int* __restrict d = dst.data(); const int* s = src.data(); for (std::size_t i = 0; i < N; ++i) d[i] = s[i]; }) << "\n";
    std::cout << "  vector=   : " << gb_per_s(bytes, reps, [&] { dst = src; }) << "\n";
    std::vector<int> small_src(16, 1), small_dst(16);
    long long total = 0;
    auto t0 = std::chrono::steady_clock::now();
    const long iters = std::getenv("QUICK") ? 100000 : 50'000'000;
    for (long i = 0; i < iters; ++i) { std::memcpy(small_dst.data(), small_src.data(), 64); small_src[i & 15] = static_cast<int>(i); total += small_dst[3]; }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "  64-byte memcpy: " << std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(iters) << " ns each (total " << (total & 1) << ")\n";
}
