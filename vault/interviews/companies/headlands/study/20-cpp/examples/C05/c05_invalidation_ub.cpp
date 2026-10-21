// EXPECT: run-fail
// C05: iterator/reference invalidation. push_back may reallocate; every iterator, pointer and reference into the old block dangles.
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    int& first = v[0];              // reference into the current buffer
    auto it = v.begin();            // iterator into the same buffer
    v.push_back(4);                 // capacity was 3: reallocation, old buffer freed
    std::cout << "size=" << v.size() << "\n";
    std::cout << first << "\n";     // use-after-free (ASan: heap-use-after-free)
    std::cout << *it << "\n";
}
