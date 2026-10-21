// EXPECTED TO ABORT with libc++ hardening enabled: vector::operator[] out of range.
#include <cstdio>
#include <vector>
int main(int argc, char**) {
    std::vector<int> v{1, 2, 3};
    std::printf("%d\n", v[static_cast<std::size_t>(argc) + 2]);
}
