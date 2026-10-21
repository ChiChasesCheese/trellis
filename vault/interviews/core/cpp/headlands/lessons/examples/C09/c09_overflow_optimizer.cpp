// SAN: none
// ASM: yes
// C09: "UB is a promise to the compiler". The overflow check below is deleted at -O2 because x + 1 < x "cannot happen".
#include <climits>
#include <cstdint>
#include <iostream>

// [[snip:checks]]
[[gnu::noinline]] bool overflows_signed_naive(int x) { return x + 1 < x; }                  // compiler: always false
[[gnu::noinline]] bool overflows_signed_safe(int x) { return x == INT_MAX; }                // test the BOUNDARY instead
[[gnu::noinline]] bool overflows_unsigned(std::uint32_t x) { return x + 1u < x; }           // defined wrap: check is real
[[gnu::noinline]] bool add_checked(int a, int b, int& out) { return __builtin_add_overflow(a, b, &out); }   // GCC/Clang builtin
// [[/snip]]

int main(int argc, char**) {
    int big = INT_MAX - 1 + argc;                       // INT_MAX at run time
    std::cout << std::boolalpha;
    std::cout << "naive signed check on INT_MAX : " << overflows_signed_naive(big) << "   (the overflow happened, the check says no)\n";
    std::cout << "boundary check on INT_MAX     : " << overflows_signed_safe(big) << "\n";
    std::cout << "unsigned check on UINT32_MAX  : " << overflows_unsigned(UINT32_MAX - 1 + argc) << "\n";
    int out = 0;
    std::cout << "__builtin_add_overflow(INT_MAX,1): " << add_checked(big, 1, out) << " (wrapped result " << out << ")\n";
}
