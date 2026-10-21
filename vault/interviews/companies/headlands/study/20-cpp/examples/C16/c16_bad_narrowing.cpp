// EXPECT: compile-fail
#include <cstdint>
int main() {
    long big = 5'000'000'000L;
    int x{big};                                        // brace initialisation forbids narrowing conversions
    int y = big;                                       // parenthesis/assignment form silently truncates
    return x + y;
}
