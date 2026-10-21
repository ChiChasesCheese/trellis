#include <vector>
int main() {
    long big = 5'000'000'000L;
    int x{big};                       // braces forbid narrowing
    std::vector<int> v{1, 2.5};       // double -> int in a braced list
    return x + v[0];
}
