// Traversal cost depends on memory layout, not just Big-O.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <list>
#include <numeric>
#include <random>
#include <vector>

struct AoS { int id; int qty; double px; double pad[5]; };            // 64 bytes per element
struct SoA { std::vector<int> qty; };                                // quantities only

template <class F> double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now(); f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}
int main() {
    const int N = 4'000'000;
    std::vector<int> v(N);
    std::iota(v.begin(), v.end(), 0);
    std::list<int> l(v.begin(), v.end());
    // Linked list whose nodes are in shuffled memory order: the realistic case after many inserts/erases.
    std::vector<int> order(N);
    std::iota(order.begin(), order.end(), 0);
    std::shuffle(order.begin(), order.end(), std::mt19937(7));
    std::vector<int> next(N);
    for (int i = 0; i + 1 < N; ++i) next[order[i]] = order[i + 1];
    next[order[N - 1]] = -1;

    long s1 = 0, s2 = 0, s3 = 0;
    double t_vec = ms([&] { s1 = std::accumulate(v.begin(), v.end(), 0L); });
    double t_list = ms([&] { s2 = std::accumulate(l.begin(), l.end(), 0L); });
    double t_chase = ms([&] { for (int i = order[0]; i != -1; i = next[i]) s3 += i; });
    std::printf("sums equal: %s\n", (s1 == s2 && s2 == s3) ? "yes" : "no");
    std::printf("vector<int> scan            : %6.1f ms\n", t_vec);
    std::printf("std::list<int> scan         : %6.1f ms\n", t_list);
    std::printf("shuffled pointer chase      : %6.1f ms\n", t_chase);

    std::vector<AoS> aos(N / 2);
    SoA soa; soa.qty.assign(N / 2, 1);
    for (auto& a : aos) a.qty = 1;
    long r1 = 0, r2 = 0;
    double t_aos = ms([&] { for (auto& a : aos) r1 += a.qty; });
    double t_soa = ms([&] { for (int q : soa.qty) r2 += q; });
    std::printf("sum one field, array of structs (64 B/elem): %6.1f ms\n", t_aos);
    std::printf("sum one field, struct of arrays (4 B/elem) : %6.1f ms\n", t_soa);
    return (r1 == r2) ? 0 : 1;
}
