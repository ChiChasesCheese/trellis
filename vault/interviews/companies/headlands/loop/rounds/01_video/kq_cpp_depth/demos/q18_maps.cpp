// map vs unordered_map vs sorted vector; operator[] side effects; rehash and invalidation.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <map>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}
int main() {
    std::map<std::string, int> m;
    int q = m["missing"];                                    // operator[] INSERTS a default value
    std::printf("after reading m[\"missing\"]: size=%zu value=%d\n", m.size(), q);
    auto found = m.find("other");                            // find does not insert
    std::printf("find(\"other\") -> %s, size still %zu\n", found == m.end() ? "end" : "found", m.size());
    m.try_emplace("k", 1); m.try_emplace("k", 2);            // second call: key exists, value untouched
    std::printf("try_emplace twice keeps first value: %d\n", m["k"]);
    for (auto& [k, v] : m) std::printf("%s ", k.c_str());    // sorted by key
    std::printf("<- map iterates in key order\n");

    std::unordered_map<int, int> um;
    um[1] = 100;
    int& ref = um[1];
    auto it = um.find(1);
    std::size_t buckets = um.bucket_count();
    for (int i = 2; i < 1000; ++i) um[i] = i;                // forces rehash
    std::printf("rehash happened: buckets %zu -> %zu; reference still valid: %d\n", buckets, um.bucket_count(), ref);
    (void)it;                                                // `it` is invalid now; references/pointers to elements are not

    const int N = 1'000'000;
    std::mt19937 rng(3);
    std::vector<int> keys(N);
    for (int& k : keys) k = static_cast<int>(rng() % 5'000'000);
    std::map<int, int> om; std::unordered_map<int, int> hm;
    std::vector<std::pair<int, int>> sv;
    double t_om = ms([&] { for (int k : keys) om[k] = k; });
    double t_hm = ms([&] { hm.reserve(N); for (int k : keys) hm[k] = k; });
    double t_sv = ms([&] { for (int k : keys) sv.emplace_back(k, k); std::sort(sv.begin(), sv.end()); });
    long hit = 0;
    double l_om = ms([&] { for (int k : keys) hit += om.count(k); });
    double l_hm = ms([&] { for (int k : keys) hit += hm.count(k); });
    double l_sv = ms([&] { for (int k : keys) hit += std::binary_search(sv.begin(), sv.end(), std::pair{k, k}); });
    std::printf("build  1M: std::map %.0f ms | unordered_map %.0f ms | sorted vector %.0f ms\n", t_om, t_hm, t_sv);
    std::printf("lookup 1M: std::map %.0f ms | unordered_map %.0f ms | sorted vector %.0f ms (hits %ld)\n", l_om, l_hm, l_sv, hit);
}
