// A tour of common undefined behaviour. Under UBSan each line prints a "runtime error" and the program continues.
#include <climits>
#include <cstdio>

int main(int argc, char**) {
    volatile int n = argc;                  // n == 1, opaque to the optimizer
    int big = INT_MAX;
    int a = big + n;                        // signed overflow
    int s = 1 << (31 + n);                  // shift exponent 32 is too large for int
    int arr[4] = {1, 2, 3, 4};
    int idx = 3 + n;                        // 4
    int oob = arr[idx];                     // out of bounds of a fixed array
    unsigned sh = 1u << (n + 40);           // another bad shift
    std::printf("results (meaningless): %d %d %d %u\n", a, s, oob, sh);
}
