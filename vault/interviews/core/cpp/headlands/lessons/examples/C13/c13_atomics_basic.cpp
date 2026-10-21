// C13: std::atomic basics: fetch_add, compare_exchange, flags; and what "lock-free" means on this CPU.
#include <atomic>
#include <cstdint>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

// [[snip:counter]]
std::atomic<long> hits{0};
long locked_hits = 0;
std::mutex mu;

void work(int n) {
    for (int i = 0; i < n; ++i) {
        hits.fetch_add(1, std::memory_order_relaxed);   // atomic read-modify-write: no lost updates
        std::lock_guard<std::mutex> g(mu);              // the mutex version of the same counter
        ++locked_hits;
    }
}
// [[/snip]]

// [[snip:cas]]
// Lock-free "update the max": retry until our compare_exchange wins or someone stored a bigger value.
void update_max(std::atomic<long>& m, long v) {
    long cur = m.load(std::memory_order_relaxed);
    while (cur < v && !m.compare_exchange_weak(cur, v, std::memory_order_relaxed)) {
        // on failure, cur was refreshed with the current value; loop re-checks cur < v
    }
}
// [[/snip]]

int main() {
    std::vector<std::thread> ts;
    for (int t = 0; t < 4; ++t) ts.emplace_back(work, 100000);
    for (auto& t : ts) t.join();
    std::cout << "atomic counter " << hits.load() << ", mutex counter " << locked_hits << " (both exact)\n";

    std::atomic<long> mx{0};
    std::vector<std::thread> us;
    for (int t = 0; t < 4; ++t) us.emplace_back([&, t] { for (int i = 0; i < 1000; ++i) update_max(mx, t * 1000 + i); });
    for (auto& t : us) t.join();
    std::cout << "max via CAS loop: " << mx.load() << "\n";

    std::atomic<bool> flag{false};
    std::atomic<std::uint64_t> u64{0};
    struct Big { char bytes[64]; };
    std::atomic<Big> big{};
    std::cout << std::boolalpha << "is_lock_free: atomic<bool> " << flag.is_lock_free() << ", atomic<uint64_t> " << u64.is_lock_free()
              << ", atomic<64-byte struct> " << big.is_lock_free() << " (falls back to a hidden lock)\n";
    std::cout << "sizeof(atomic<long>)=" << sizeof(std::atomic<long>) << "\n";
}
