// A tour of common undefined behaviour. Under UBSan each line prints a "runtime error" and the program continues.
#include <climits>
#include <cstdio>

int main(int argc, char**) {
    volatile int n = argc;                  // n == 1, opaque to the optimizer
    int a = INT_MAX + n;                    // signed overflow
    int s = 1 << (31 + n);                  // shift exponent 32 is too large for int
    int m1 = -n;
    int q = INT_MIN / m1;                   // INT_MIN / -1: not representable
    alignas(int) char buf[16] = {};
    int mis = *reinterpret_cast<int*>(buf + n);   // load through a misaligned int*
    unsigned sh = 1u << (n + 40);           // another bad shift
    std::printf("results (meaningless): %d %d %d %d %u\n", a, s, q, mis, sh);
}
