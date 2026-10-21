// C06: <algorithm> and <numeric>: the C++ answer to Java's Collections.sort / streams, with iterator pairs.
#include <algorithm>
#include <climits>
#include <iostream>
#include <numeric>
#include <queue>
#include <string>
#include <vector>

struct Trade { std::string sym; long qty; double px; };

template <class C>
void show(const char* label, const C& c) {
    std::cout << "  " << label << ":";
    for (const auto& x : c) std::cout << " " << x;
    std::cout << "\n";
}

int main() {
    // [[snip:sort]]
    std::vector<Trade> ts{{"MSFT", 50, 410.0}, {"AAPL", 100, 187.5}, {"NVDA", 10, 900.0}, {"AAPL", 20, 188.0}};
    std::sort(ts.begin(), ts.end(), [](const Trade& a, const Trade& b) {
        if (a.sym != b.sym) return a.sym < b.sym;        // must be a strict weak ordering: never use <=
        return a.qty * a.px > b.qty * b.px;              // then by notional, descending
    });
    for (auto& t : ts) std::cout << "  " << t.sym << " " << t.qty << " @ " << t.px << "\n";
    // [[/snip]]

    // [[snip:search]]
    std::vector<int> v{1, 3, 3, 5, 8, 13, 21};            // sorted
    auto lo = std::lower_bound(v.begin(), v.end(), 3);    // first element >= 3
    auto hi = std::upper_bound(v.begin(), v.end(), 3);    // first element >  3
    std::cout << "  lower_bound(3) index " << lo - v.begin() << ", upper_bound(3) index " << hi - v.begin()
              << ", count " << hi - lo << ", binary_search(8)=" << std::binary_search(v.begin(), v.end(), 8) << "\n";
    // [[/snip]]

    // [[snip:accumulate]]
    std::vector<int> big(10, 1'000'000'000);
    // std::accumulate(big.begin(), big.end(), 0) would sum in INT (init's type) and overflow: see c06_accumulate_ub.cpp
    long long right = std::accumulate(big.begin(), big.end(), 0LL);     // init type decides the accumulator type
    std::cout << "  sum with 0LL init: " << right << "\n";
    // [[/snip]]

    // [[snip:partition]]
    std::vector<int> w{9, 4, 7, 1, 8, 2, 6};
    std::nth_element(w.begin(), w.begin() + 3, w.end());                 // O(n): w[3] is the 4th smallest, rest partitioned
    std::cout << "  4th smallest via nth_element: " << w[3] << "\n";
    std::partial_sort(w.begin(), w.begin() + 3, w.end());                // smallest 3, sorted
    show("first three sorted", std::vector<int>(w.begin(), w.begin() + 3));
    auto mid = std::stable_partition(w.begin(), w.end(), [](int x) { return x % 2 == 0; });
    std::cout << "  evens before odds, " << mid - w.begin() << " evens\n";
    // [[/snip]]

    // [[snip:misc]]
    std::vector<int> u{1, 1, 2, 2, 2, 3, 1};
    u.erase(std::unique(u.begin(), u.end()), u.end());                   // removes CONSECUTIVE duplicates only
    show("unique", u);
    std::vector<int> seq(5);
    std::iota(seq.begin(), seq.end(), 10);
    std::vector<int> prefix(seq.size());
    std::partial_sum(seq.begin(), seq.end(), prefix.begin());
    show("iota", seq); show("prefix sums", prefix);
    auto [mn, mx] = std::minmax_element(seq.begin(), seq.end());
    std::cout << "  min " << *mn << " max " << *mx << "\n";
    std::string perm = "abc";
    std::cout << "  permutations:";
    do { std::cout << " " << perm; } while (std::next_permutation(perm.begin(), perm.end()));
    std::cout << "\n";
    // [[/snip]]

    // [[snip:pq]]
    std::priority_queue<int> maxheap;                                      // C++ default is a MAX-heap (Java's is a min-heap)
    for (int x : {5, 1, 9, 3}) maxheap.push(x);
    std::cout << "  maxheap top " << maxheap.top();
    std::priority_queue<int, std::vector<int>, std::greater<int>> minheap;  // Java's PriorityQueue default
    for (int x : {5, 1, 9, 3}) minheap.push(x);
    std::cout << ", minheap top " << minheap.top() << "\n";
    auto cmp = [](const Trade& a, const Trade& b) { return a.qty * a.px > b.qty * b.px; };   // "greater" => min-heap by notional
    std::priority_queue<Trade, std::vector<Trade>, decltype(cmp)> top3(cmp);
    for (auto& t : ts) { top3.push(t); if (top3.size() > 3) top3.pop(); }  // keep the 3 largest notionals
    std::cout << "  top-3 notional kept, smallest of them: " << top3.top().sym << " " << top3.top().qty * top3.top().px << "\n";
    // [[/snip]]
}
