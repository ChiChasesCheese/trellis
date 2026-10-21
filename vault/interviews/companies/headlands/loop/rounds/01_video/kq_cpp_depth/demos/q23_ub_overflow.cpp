// Signed overflow is undefined, so the optimizer may assume it never happens.
#include <climits>
#include <cstdio>

bool always_bigger(int x) { return x + 1 > x; }               // with UB: always true
bool wrap_check(unsigned x) { return x + 1 > x; }             // unsigned wraps: false for UINT_MAX

int main(int argc, char**) {
    int big = INT_MAX - 1 + argc;                              // INT_MAX at run time (argc == 1)
    std::printf("always_bigger(INT_MAX) = %d\n", always_bigger(big));
    std::printf("wrap_check(UINT_MAX)   = %d\n", wrap_check(UINT_MAX));
    unsigned u = 0xFFFFFFFFu;
    std::printf("UINT_MAX + 1 = %u (defined: wraps)\n", u + 1);
}
