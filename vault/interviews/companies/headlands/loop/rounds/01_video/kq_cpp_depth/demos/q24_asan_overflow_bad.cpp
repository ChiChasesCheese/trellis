// EXPECTED TO FAIL under ASan: heap buffer overflow.
#include <cstdio>
#include <cstdlib>
int main() {
    int* a = static_cast<int*>(std::malloc(4 * sizeof(int)));
    for (int i = 0; i <= 4; ++i) a[i] = i;      // off-by-one: i == 4 writes past the end
    std::printf("%d\n", a[0]);
    std::free(a);
}
