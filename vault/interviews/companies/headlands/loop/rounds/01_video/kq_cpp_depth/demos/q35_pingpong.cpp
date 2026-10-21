// Cost of waking a sleeping thread vs spinning on an atomic: round-trip latency between two threads.
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <mutex>
#include <thread>

int main() {
    const int N = 100000;
    using clk = std::chrono::steady_clock;

    // 1) mutex + condition_variable: the kernel puts the thread to sleep and wakes it
    {
        std::mutex m; std::condition_variable cv; int turn = 0;
        std::thread other([&] {
            for (int i = 0; i < N; ++i) {
                std::unique_lock lk(m); cv.wait(lk, [&] { return turn == 1; });
                turn = 0; cv.notify_all();
            }
        });
        auto t0 = clk::now();
        for (int i = 0; i < N; ++i) {
            { std::unique_lock lk(m); turn = 1; cv.notify_all(); cv.wait(lk, [&] { return turn == 0; }); }
        }
        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(clk::now() - t0).count();
        other.join();
        std::printf("condition_variable round trip: %6.0f ns\n", static_cast<double>(ns) / N);
    }
    // 2) spin on an atomic: nobody sleeps, but a core is burned
    {
        std::atomic<int> turn{0};
        std::thread other([&] {
            for (int i = 0; i < N; ++i) { while (turn.load(std::memory_order_acquire) != 1) {} turn.store(0, std::memory_order_release); }
        });
        auto t0 = clk::now();
        for (int i = 0; i < N; ++i) { turn.store(1, std::memory_order_release); while (turn.load(std::memory_order_acquire) != 0) {} }
        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(clk::now() - t0).count();
        other.join();
        std::printf("atomic spin round trip       : %6.0f ns\n", static_cast<double>(ns) / N);
    }
}
