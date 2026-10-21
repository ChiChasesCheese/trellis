// EXPECT: run-fail
// C09: signed integer overflow is undefined behaviour; unsigned overflow wraps (defined). UBSan names the line.
#include <climits>
#include <cstdint>
#include <iostream>

int main(int argc, char**) {
    int x = INT_MAX - 1 + argc;                  // argc == 1 at run time, so x == INT_MAX
    std::uint32_t u = UINT32_MAX - 1 + static_cast<std::uint32_t>(argc);
    std::cout << "unsigned UINT32_MAX + 1 = " << u + 1u << " (defined: wraps to 0)\n";
    int y = x + 1;                               // UB: UBSan reports "signed integer overflow"
    std::cout << "signed INT_MAX + 1 = " << y << " (whatever the compiler happened to emit)\n";
}
