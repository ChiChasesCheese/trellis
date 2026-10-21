// Per-thread partial sums.  Adjacent slots share a cache line: every write by one thread invalidates the line in the
// others' caches ("false sharing").  Pad each slot to a full line (128 bytes covers Apple silicon and x86), or keep the
// partial sum in a local variable and write the slot once at the end.
#include <iostream>
#include <numeric>
#include <thread>
#include <vector>

struct alignas(128) Slot {
    long long value = 0;
};
static_assert(sizeof(Slot) == 128, "one slot per cache line");

int main() {
    std::vector<long long> data(4'000'000);
    std::iota(data.begin(), data.end(), 1);

    constexpr int threads = 4;
    std::vector<Slot> slots(threads);                       // padded: no two threads touch the same line
    std::vector<std::thread> pool;
    const std::size_t part = data.size() / threads;
    for (int t = 0; t < threads; ++t)
        pool.emplace_back([&, t] {
            long long local = 0;                            // the hot loop touches only a register ...
            for (std::size_t i = t * part; i < (t + 1) * part; ++i) local += data[i];
            slots[t].value = local;                         // ... and the shared slot is written once
        });
    for (auto& th : pool) th.join();                        // join makes the slots visible to this thread

    long long total = 0;
    for (const Slot& s : slots) total += s.value;
    std::cout << total << "\n";                             // 8000002000000
}
