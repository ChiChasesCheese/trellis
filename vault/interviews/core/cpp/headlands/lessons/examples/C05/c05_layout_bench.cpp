// SAN: none
// C05: the same sum over six containers. Complexity is identical (O(n)); memory layout is not.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <deque>
#include <iostream>
#include <list>
#include <map>
#include <numeric>
#include <random>
#include <set>
#include <unordered_map>
#include <vector>

template <class F>
void bench(const char* name, std::size_t n, F&& f) {
    f();                                                   // warm
    auto t0 = std::chrono::steady_clock::now();
    long r = 0;
    for (int rep = 0; rep < 5; ++rep) r += f();
    auto t1 = std::chrono::steady_clock::now();
    double ns = std::chrono::duration<double, std::nano>(t1 - t0).count() / 5.0 / static_cast<double>(n);
    std::cout << "  " << name << ": " << ns << " ns/element (checksum " << r << ")\n";
}

int main() {
    const std::size_t N = std::getenv("QUICK") ? 200'000 : 2'000'000;
    std::vector<int> v(N);
    std::iota(v.begin(), v.end(), 0);
    std::deque<int> d(v.begin(), v.end());
    // The list/map nodes are allocated in a SHUFFLED order so neighbours in the list are not neighbours in memory,
    // like a long-lived container whose nodes were allocated and freed over time.
    std::vector<int> order(v);
    std::mt19937 rng(1);
    std::shuffle(order.begin(), order.end(), rng);
    // [[snip:shuffled]]
    std::list<int> l_shuffled;                             // nodes allocated in shuffled value order ...
    for (int x : order) l_shuffled.push_back(x);
    l_shuffled.sort();                                     // ... then RELINKED in value order: traversal jumps around memory
    // [[/snip]]
    std::list<int> l_seq(v.begin(), v.end());
    std::set<int> s(v.begin(), v.end());
    std::unordered_map<int, int> um;
    um.reserve(N);
    for (int x : v) um[x] = x;

    std::cout << "sum over " << N << " ints, ns per element\n";
    bench("vector           ", N, [&] { return std::accumulate(v.begin(), v.end(), 0L); });
    bench("deque            ", N, [&] { return std::accumulate(d.begin(), d.end(), 0L); });
    bench("list (alloc seq.)", N, [&] { return std::accumulate(l_seq.begin(), l_seq.end(), 0L); });
    bench("list (shuffled)  ", N, [&] { return std::accumulate(l_shuffled.begin(), l_shuffled.end(), 0L); });
    bench("set (RB-tree)    ", N, [&] { return std::accumulate(s.begin(), s.end(), 0L); });
    bench("unordered_map    ", N, [&] { long t = 0; for (auto& kv : um) t += kv.second; return t; });
}
