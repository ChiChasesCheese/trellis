// SAN: none
// C13: why memory_order matters. Store-buffering litmus test: can both threads read 0?
//   T1: x = 1; r1 = y;      T2: y = 1; r2 = x;
// Sequential consistency forbids r1 == r2 == 0. Relaxed ordering allows it (each store may be delayed past the other thread's load).
#include <atomic>
#include <cstdlib>
#include <iostream>
#include <thread>

std::atomic<int> x, y;
std::atomic<int> start{0}, done1{0}, done2{0};
int r1, r2;

template <std::memory_order MO>
long trial(long rounds) {
    long both_zero = 0;
    std::thread t1([&] {
        for (long i = 0; i < rounds; ++i) {
            while (start.load(std::memory_order_acquire) != 2 * i + 1) { }       // wait for the round to open
            x.store(1, MO);
            r1 = y.load(MO);
            done1.store(i + 1, std::memory_order_release);
        }
    });
    std::thread t2([&] {
        for (long i = 0; i < rounds; ++i) {
            while (start.load(std::memory_order_acquire) != 2 * i + 1) { }
            y.store(1, MO);
            r2 = x.load(MO);
            done2.store(i + 1, std::memory_order_release);
        }
    });
    for (long i = 0; i < rounds; ++i) {
        x.store(0); y.store(0);
        start.store(2 * i + 1, std::memory_order_release);                       // open round i
        while (done1.load(std::memory_order_acquire) != i + 1 || done2.load(std::memory_order_acquire) != i + 1) { }
        if (r1 == 0 && r2 == 0) ++both_zero;
    }
    t1.join(); t2.join();
    start = 0; done1 = 0; done2 = 0;
    return both_zero;
}

int main() {
    const long rounds = std::getenv("QUICK") ? 2000 : 200000;
    std::cout << "rounds: " << rounds << "\n";
    std::cout << "memory_order_relaxed: r1==0 && r2==0 in " << trial<std::memory_order_relaxed>(rounds) << " rounds\n";
    std::cout << "memory_order_seq_cst: r1==0 && r2==0 in " << trial<std::memory_order_seq_cst>(rounds) << " rounds\n";
}
