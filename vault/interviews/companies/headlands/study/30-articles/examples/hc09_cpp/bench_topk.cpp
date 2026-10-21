// Four ways to take the k best of n events: bounded heap, partial_sort, nth_element + sort of the prefix, full sort.
// Every variant uses the same strict total order (notional descending, then index ascending), so the answers are identical.
// Build with -O2 and no sanitizers for meaningful timings.
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <vector>

struct Key { long long notional; int index; };
inline bool better(const Key& a, const Key& b) { return a.notional != b.notional ? a.notional > b.notional : a.index < b.index; }

template <class F> double ms(F&& f) {
    const auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

std::vector<Key> heap_topk(const std::vector<Key>& all, std::size_t k) {
    std::priority_queue<Key, std::vector<Key>, decltype(&better)> heap(&better);
    for (const Key& e : all) {
        if (heap.size() == k && e.notional < heap.top().notional) continue;  // fast reject
        if (heap.size() < k) heap.push(e);
        else if (better(e, heap.top())) { heap.pop(); heap.push(e); }
    }
    std::vector<Key> out;
    while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }
    std::reverse(out.begin(), out.end());
    return out;
}
std::vector<Key> partial_sort_topk(std::vector<Key> v, std::size_t k) {
    std::partial_sort(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(k), v.end(), better);
    v.resize(k);
    return v;
}
std::vector<Key> nth_element_topk(std::vector<Key> v, std::size_t k) {
    std::nth_element(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(k - 1), v.end(), better);
    std::sort(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(k), better);
    v.resize(k);
    return v;
}
std::vector<Key> sort_topk(std::vector<Key> v, std::size_t k) {
    std::sort(v.begin(), v.end(), better);
    v.resize(k);
    return v;
}

int main() {
    const int n = 2'000'000;
    std::mt19937_64 rnd(1);
    std::vector<Key> events(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) events[static_cast<std::size_t>(i)] = {static_cast<long long>(rnd() % 1'000'000'000), i};
    std::cout << "n = " << n << ", milliseconds\n";
    std::cout << "      k    heap  partial_sort  nth_element    sort\n";
    for (std::size_t k : {std::size_t{10}, std::size_t{1000}, std::size_t{100000}, std::size_t{1000000}}) {
        std::vector<Key> a, b, c, d;
        const double th = ms([&] { a = heap_topk(events, k); });
        const double tp = ms([&] { b = partial_sort_topk(events, k); });
        const double tn = ms([&] { c = nth_element_topk(events, k); });
        const double ts = ms([&] { d = sort_topk(events, k); });
        const bool same = std::equal(a.begin(), a.end(), b.begin(), [](const Key& x, const Key& y) { return x.index == y.index; }) &&
                          std::equal(a.begin(), a.end(), c.begin(), [](const Key& x, const Key& y) { return x.index == y.index; }) &&
                          std::equal(a.begin(), a.end(), d.begin(), [](const Key& x, const Key& y) { return x.index == y.index; });
        std::cout << std::fixed << std::setprecision(1) << std::setw(7) << k << std::setw(8) << th << std::setw(14) << tp << std::setw(13) << tn
                  << std::setw(8) << ts << (same ? "" : "  MISMATCH") << "\n";
    }
}
