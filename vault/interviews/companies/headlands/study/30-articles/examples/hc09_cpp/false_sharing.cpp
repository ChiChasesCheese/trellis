// Two counters updated by two threads: in the same cache line they fight over it ("false sharing"); on separate lines they do not.
// Build with -O2 and no sanitizers.  The numbers depend on the machine; the gap is what matters.
#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>

struct Shared { std::atomic<long long> a{0}, b{0}; };                     // a and b in one 16-byte neighbourhood
struct Padded { alignas(64) std::atomic<long long> a{0}; alignas(64) std::atomic<long long> b{0}; };  // 64 bytes apart

template <class T> double run(T& counters) {
    constexpr int iterations = 20'000'000;
    const auto t0 = std::chrono::steady_clock::now();
    {
        std::jthread x([&] { for (int i = 0; i < iterations; ++i) counters.a.fetch_add(1, std::memory_order_relaxed); });
        std::jthread y([&] { for (int i = 0; i < iterations; ++i) counters.b.fetch_add(1, std::memory_order_relaxed); });
    }
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    Shared s;
    Padded p;
    std::cout << "same cache line:      " << run(s) << " ms\n";
    std::cout << "separate cache lines: " << run(p) << " ms\n";
}
