// False sharing: independent counters on one cache line slow each other down.
#include <atomic>
#include <chrono>
#include <cstdio>
#include <new>
#include <thread>
#include <vector>

template <std::size_t Pad> struct Slot { alignas(Pad) std::atomic<long> v{0}; };

template <std::size_t Pad>
double run() {
    Slot<Pad> slots[4];
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t)
        ts.emplace_back([&slots, t] { for (int i = 0; i < 20'000'000; ++i) slots[t].v.fetch_add(1, std::memory_order_relaxed); });
    for (auto& t : ts) t.join();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}
int main() {
    std::printf("sizeof(atomic<long>) = %zu; hardware_destructive_interference_size = %zu\n",
                sizeof(std::atomic<long>), std::hardware_destructive_interference_size);
    std::printf("4 threads, adjacent counters (8 B apart)  : %6.0f ms\n", run<8>());
    std::printf("4 threads, 64 B apart                      : %6.0f ms\n", run<64>());
    std::printf("4 threads, 128 B apart                     : %6.0f ms\n", run<128>());
}
