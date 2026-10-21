// C14: C++20 jthread (joins automatically), cooperative cancellation with stop_token, latch/barrier/semaphore.
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <latch>
#include <mutex>
#include <semaphore>
#include <stop_token>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

// [[snip:worker]]
void worker(std::stop_token st, std::atomic<int>& ticks) {
    while (!st.stop_requested()) {                  // cooperative cancellation: the thread checks, nobody kills it
        ++ticks;
        std::this_thread::sleep_for(1ms);
    }
}
// [[/snip]]

// [[snip:cvstop]]
struct Mailbox {
    std::mutex m;
    std::condition_variable_any cv;                 // _any: wait() can take a stop_token
    int pending = 0;
};
void waiter(std::stop_token st, Mailbox& mb, bool& woke_by_stop) {
    std::unique_lock lk(mb.m);
    bool got = mb.cv.wait(lk, st, [&] { return mb.pending > 0; });   // returns false if stop was requested first
    woke_by_stop = !got;
}
// [[/snip]]

int main() {
    std::atomic<int> ticks{0};
    {
        std::jthread t(worker, std::ref(ticks));    // stop_token is passed automatically as the first argument
        std::this_thread::sleep_for(20ms);
        t.request_stop();
    }                                               // ~jthread: request_stop() then join(): no terminate, no leak
    std::cout << "worker stopped cleanly, ticked at least once: " << (ticks.load() > 0) << "\n";

    Mailbox mb;
    bool by_stop = false;
    {
        std::jthread w(waiter, std::ref(mb), std::ref(by_stop));
        std::this_thread::sleep_for(10ms);          // the waiter is blocked on the condition variable
    }                                               // destructor requests stop -> cv.wait returns -> join completes
    std::cout << "blocked waiter released by stop request: " << by_stop << "\n";

    // [[snip:latch]]
    std::latch ready(3);                            // one-shot countdown
    std::counting_semaphore<2> slots(2);            // at most 2 workers inside the section at once
    std::atomic<int> inside{0}, max_inside{0};
    std::vector<std::jthread> ts;
    for (int i = 0; i < 3; ++i)
        ts.emplace_back([&] {
            slots.acquire();
            int n = ++inside;
            int m = max_inside.load();
            while (m < n && !max_inside.compare_exchange_weak(m, n)) { }
            std::this_thread::sleep_for(5ms);
            --inside;
            slots.release();
            ready.count_down();
        });
    ready.wait();
    // [[/snip]]
    std::cout << "latch released; max concurrent inside semaphore section: " << max_inside.load() << " (limit 2)\n";
}
