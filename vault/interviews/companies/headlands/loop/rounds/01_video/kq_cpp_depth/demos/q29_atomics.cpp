// std::atomic: counters, compare-exchange, and release/acquire message passing.
#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>
#include <vector>

struct Msg { int a, b; };

template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    std::atomic<long> counter{0};
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t) ts.emplace_back([&] { for (int i = 0; i < 1'000'000; ++i) counter.fetch_add(1, std::memory_order_relaxed); });
    for (auto& t : ts) t.join();
    std::printf("4 threads x 1M fetch_add -> %ld\n", counter.load());

    std::atomic<int> maxv{0};                                       // CAS loop: lock-free "max"
    auto update_max = [&](int v) {
        int cur = maxv.load(std::memory_order_relaxed);
        while (cur < v && !maxv.compare_exchange_weak(cur, v, std::memory_order_relaxed)) {}   // cur refreshed on failure
    };
    std::vector<std::thread> ws;
    for (int t = 0; t < 4; ++t) ws.emplace_back([&, t] { for (int i = 0; i < 100000; ++i) update_max(t * 100000 + i); });
    for (auto& t : ws) t.join();
    std::printf("max via CAS = %d\n", maxv.load());

    // Release/acquire: the consumer that sees ready==true must see the payload written before the store.
    int bad = 0;
    for (int round = 0; round < 20000; ++round) {
        Msg payload{0, 0};
        std::atomic<bool> ready{false};
        std::thread p([&] { payload = {round, round * 2}; ready.store(true, std::memory_order_release); });
        std::thread c([&] {
            while (!ready.load(std::memory_order_acquire)) {}
            if (payload.a != round || payload.b != round * 2) ++bad;
        });
        p.join(); c.join();
    }
    std::printf("release/acquire handoff: %d bad reads in 20000 rounds\n", bad);

    std::atomic<long> seq{0}, rel{0};
    double t_seq = ms([&] { for (int i = 0; i < 20'000'000; ++i) seq.fetch_add(1, std::memory_order_seq_cst); });
    double t_rel = ms([&] { for (int i = 0; i < 20'000'000; ++i) rel.fetch_add(1, std::memory_order_relaxed); });
    std::printf("uncontended fetch_add x20M: seq_cst %.0f ms, relaxed %.0f ms\n", t_seq, t_rel);
    std::printf("atomic<long> lock-free: %d, atomic<Msg> lock-free: %d\n", std::atomic<long>::is_always_lock_free, std::atomic<Msg>::is_always_lock_free);
}
