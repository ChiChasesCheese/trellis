// Amortised cost of compaction: a compaction costs O(capacity) but frees about m/2 slots, so each put pays O(1) on average.
#include <algorithm>
#include <bit>
#include <iostream>

int main() {
    const int live = 1000, min_capacity = 16;
    long long moved = 0, puts = 0;
    int capacity = static_cast<int>(std::bit_ceil(static_cast<unsigned>(std::max(min_capacity, live + live / 2 + 1))));
    int next = live + 1;                       // 1000 live orders were just compacted into the front
    for (int cycle = 0; cycle < 1000; ++cycle) {
        while (next <= capacity) { ++next; ++puts; }   // each put also removes the oldest: live stays 1000
        moved += live;                                  // compaction moves the live orders
        capacity = static_cast<int>(std::bit_ceil(static_cast<unsigned>(std::max(min_capacity, live + live / 2 + 1))));
        next = live + 1;
    }
    std::cout << "capacity " << capacity << ", puts per compaction ~" << puts / 1000 << ", moves per put = " << static_cast<double>(moved) / static_cast<double>(puts) << "\n";
}
