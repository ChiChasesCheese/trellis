// SAN: none
// C12: value types and cache locality. Same data, same O(n) sum; the difference is what the cache sees.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <numeric>
#include <random>
#include <vector>

// [[snip:structs]]
struct Order { std::uint64_t id; std::int64_t px; std::int64_t qty; std::uint8_t side; };            // 32 bytes with padding
struct OrderBad { std::uint8_t side; std::uint64_t id; std::uint8_t flag; std::int64_t px; std::int64_t qty; };   // padding between fields
struct OrderPacked { std::uint64_t id; std::int64_t px; std::int64_t qty; std::uint8_t side; std::uint8_t flag; };
// [[/snip]]

// [[snip:soa]]
struct Soa { std::vector<std::uint64_t> id; std::vector<std::int64_t> px; std::vector<std::int64_t> qty; };
// [[/snip]]

template <class F>
double ns_per(std::size_t n, int reps, F&& f, long& sink) {
    sink += f();
    auto t0 = std::chrono::steady_clock::now();
    for (int r = 0; r < reps; ++r) sink += f();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::nano>(t1 - t0).count() / reps / static_cast<double>(n);
}

int main() {
    const std::size_t N = std::getenv("QUICK") ? 50'000 : 4'000'000;
    const int reps = std::getenv("QUICK") ? 2 : 5;
    long sink = 0;
    std::cout << "sizeof: Order=" << sizeof(Order) << " OrderBad=" << sizeof(OrderBad) << " OrderPacked=" << sizeof(OrderPacked)
              << " (field order changes padding)\n";

    std::vector<Order> values(N);
    for (std::size_t i = 0; i < N; ++i) values[i] = Order{i, 100 + static_cast<std::int64_t>(i % 50), static_cast<std::int64_t>(i % 7), 0};
    // pointer version: Java-style "array of references"; allocate in order, then SHUFFLE the pointers (what a long-lived heap looks like)
    std::vector<std::unique_ptr<Order>> ptrs;
    ptrs.reserve(N);
    for (std::size_t i = 0; i < N; ++i) ptrs.push_back(std::make_unique<Order>(values[i]));
    std::mt19937 rng(7);
    std::shuffle(ptrs.begin(), ptrs.end(), rng);
    Soa soa;
    for (auto& o : values) { soa.id.push_back(o.id); soa.px.push_back(o.px); soa.qty.push_back(o.qty); }

    std::cout << "notional sum (px*qty) over " << N << " orders, ns per order:\n";
    std::cout << "  vector<Order>                 : " << ns_per(N, reps, [&] { long t = 0; for (auto& o : values) t += o.px * o.qty; return t; }, sink) << "\n";
    std::cout << "  vector<unique_ptr<Order>> shuf: " << ns_per(N, reps, [&] { long t = 0; for (auto& p : ptrs) t += p->px * p->qty; return t; }, sink) << "\n";
    std::cout << "  struct of arrays (px, qty)    : " << ns_per(N, reps, [&] { long t = 0; for (std::size_t i = 0; i < N; ++i) t += soa.px[i] * soa.qty[i]; return t; }, sink) << "\n";
    std::cout << "  sum of qty only, vector<Order>: " << ns_per(N, reps, [&] { long t = 0; for (auto& o : values) t += o.qty; return t; }, sink) << "\n";
    std::cout << "  sum of qty only, SoA          : " << ns_per(N, reps, [&] { return std::accumulate(soa.qty.begin(), soa.qty.end(), 0L); }, sink) << "\n";
    std::cout << "(sink " << (sink & 1) << ")\n";
}
