// EXPECTED TO FAIL under ASan: the iterator dangles after push_back reallocates.
#include <cstdio>
#include <vector>
int main() {
    std::vector<int> v{1, 2, 3};
    auto first = v.begin();
    v.push_back(4);          // capacity 3 -> reallocation
    std::printf("%d\n", *first);   // heap-use-after-free
}
