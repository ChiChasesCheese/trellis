// Three spellings of "sum an array". At -O2 they compile to the same code.
#include <cstddef>
#include <numeric>
#include <cstdio>

long sum_loop(const int* p, std::size_t n) {
    long s = 0;
    for (std::size_t i = 0; i < n; ++i) s += p[i];
    return s;
}
long sum_acc(const int* p, std::size_t n) { return std::accumulate(p, p + n, 0L); }
long sum_lambda(const int* p, std::size_t n) {
    return std::accumulate(p, p + n, 0L, [](long a, int b) { return a + b; });
}
// A loop with a known trip count folds to a closed form.
long gauss(long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += i;
    return s;
}
int main() {
    int a[5] = {1, 2, 3, 4, 5};
    std::printf("%ld %ld %ld %ld\n", sum_loop(a, 5), sum_acc(a, 5), sum_lambda(a, 5), gauss(10));
}
