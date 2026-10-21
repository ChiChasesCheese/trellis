// constexpr / consteval / static_assert and CRTP.
#include <array>
#include <cstdio>

constexpr std::array<int, 16> make_popcount_table() {
    std::array<int, 16> t{};
    for (int i = 0; i < 16; ++i) { int c = 0; for (int b = i; b; b >>= 1) c += b & 1; t[i] = c; }
    return t;
}
constexpr auto kTable = make_popcount_table();                 // built by the compiler, lives in .rodata
static_assert(kTable[15] == 4 && kTable[8] == 1);

constexpr unsigned long long fib(int n) {
    unsigned long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) { auto t = a + b; a = b; b = t; }
    return a;
}
constexpr auto kFib50 = fib(50);                               // 12586269025, no work at run time

template <class D> struct Base { int run() { return static_cast<D*>(this)->step() + 1; } };
struct Impl : Base<Impl> { int step() { return 41; } };

int popcount32(unsigned x) { return kTable[x & 15] + kTable[(x >> 4) & 15] + kTable[(x >> 8) & 15] + kTable[(x >> 12) & 15]
                                  + kTable[(x >> 16) & 15] + kTable[(x >> 20) & 15] + kTable[(x >> 24) & 15] + kTable[x >> 28]; }
int main() {
    std::printf("fib(50) = %llu (computed at compile time)\n", kFib50);
    std::printf("popcount32(0xF0F0F0F1) = %d\n", popcount32(0xF0F0F0F1u));
    Impl i;
    std::printf("CRTP run() = %d\n", i.run());
}
