// SAN: none
// C13: false sharing: two threads write DIFFERENT variables that live on the SAME cache line, and slow each other down.
#include <atomic>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <thread>

// [[snip:layouts]]
struct Adjacent { std::atomic<long> a{0}; std::atomic<long> b{0}; };                     // same cache line
struct Padded64 { alignas(64) std::atomic<long> a{0}; alignas(64) std::atomic<long> b{0}; };
struct Padded128 { alignas(128) std::atomic<long> a{0}; alignas(128) std::atomic<long> b{0}; };
// [[/snip]]

template <class S>
double run_ms(long iters) {
    S s;
    auto t0 = std::chrono::steady_clock::now();
    std::thread t1([&] { for (long i = 0; i < iters; ++i) s.a.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (long i = 0; i < iters; ++i) s.b.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    const long iters = std::getenv("QUICK") ? 100'000 : 50'000'000;
    std::cout << "sizeof: Adjacent=" << sizeof(Adjacent) << " Padded64=" << sizeof(Padded64) << " Padded128=" << sizeof(Padded128) << "\n";
    std::cout << "2 threads x " << iters << " increments of their own counter:\n";
    std::cout << "  adjacent (same line) : " << run_ms<Adjacent>(iters) << " ms\n";
    std::cout << "  alignas(64) padding  : " << run_ms<Padded64>(iters) << " ms\n";
    std::cout << "  alignas(128) padding : " << run_ms<Padded128>(iters) << " ms\n";
}
