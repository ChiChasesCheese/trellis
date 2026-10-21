// Two 64-bit halves written separately are NOT one 128-bit value for a concurrent reader.
// (Relaxed atomics keep this program free of data races; the tearing is a logic bug, not UB.)
#include <atomic>
#include <iostream>
#include <thread>

int main() {
    std::atomic<unsigned long long> hi{0}, lo{0};
    std::atomic<bool> stop{false};
    std::thread writer([&] {
        for (unsigned long long i = 1; i <= 2'000'000; ++i) {
            hi.store(i, std::memory_order_relaxed);   // the pair (hi, lo) should always be (i, i)
            lo.store(i, std::memory_order_relaxed);
        }
        stop.store(true);
    });
    long long torn = 0, reads = 0;
    while (!stop.load()) {
        auto h = hi.load(std::memory_order_relaxed);
        auto l = lo.load(std::memory_order_relaxed);
        ++reads;
        if (h != l) ++torn;                           // saw hi from one update and lo from another
    }
    writer.join();
    std::cout << "torn reads observed: " << (torn > 0 ? "yes" : "none this run") << " (out of " << (reads > 0 ? "many" : "0") << ")\n";
}
