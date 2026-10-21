// ALSO: thread
// C13: a lock-free single-producer/single-consumer ring buffer: the canonical low-latency queue.
#include <atomic>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <thread>
#include <vector>

// [[snip:ring]]
template <class T, std::size_t N>                       // N must be a power of two: index = counter & (N-1), no modulo
class SpscRing {
    static_assert((N & (N - 1)) == 0, "capacity must be a power of two");
    alignas(64) std::atomic<std::size_t> head_{0};      // written only by the consumer
    alignas(64) std::atomic<std::size_t> tail_{0};      // written only by the producer; own cache line (no false sharing)
    alignas(64) T buf_[N];
public:
    bool push(const T& v) {                             // producer thread only
        std::size_t t = tail_.load(std::memory_order_relaxed);            // our own variable: relaxed is enough
        if (t - head_.load(std::memory_order_acquire) == N) return false; // full (acquire: see the consumer's frees)
        buf_[t & (N - 1)] = v;
        tail_.store(t + 1, std::memory_order_release);                    // publish the slot
        return true;
    }
    bool pop(T& out) {                                  // consumer thread only
        std::size_t h = head_.load(std::memory_order_relaxed);
        if (h == tail_.load(std::memory_order_acquire)) return false;     // empty
        out = buf_[h & (N - 1)];
        head_.store(h + 1, std::memory_order_release);                    // hand the slot back
        return true;
    }
};
// [[/snip]]

int main() {
    constexpr std::size_t COUNT = 2'000'000;
    static SpscRing<std::uint64_t, 1024> ring;
    std::uint64_t sum = 0;
    std::thread consumer([&] {
        std::uint64_t v, expect = 0;
        for (std::size_t got = 0; got < COUNT;) {
            if (ring.pop(v)) { if (v != expect++) { std::cout << "ORDER VIOLATION\n"; std::abort(); } sum += v; ++got; }
        }
    });
    for (std::uint64_t i = 0; i < COUNT; ++i) while (!ring.push(i)) { }
    consumer.join();
    std::cout << "transferred " << COUNT << " items in order, sum " << sum << " (expected " << (COUNT * (COUNT - 1)) / 2 << ")\n";
}
