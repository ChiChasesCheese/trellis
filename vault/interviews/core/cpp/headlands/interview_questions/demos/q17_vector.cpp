// vector growth, reserve, and what invalidates pointers/iterators.
#include <cstdio>
#include <cstdint>
#include <vector>

int main() {
    std::vector<int> v;
    std::size_t last_cap = 0;
    std::printf("capacity as push_back grows: ");
    for (int i = 0; i < 100; ++i) {
        v.push_back(i);
        if (v.capacity() != last_cap) { std::printf("%zu ", v.capacity()); last_cap = v.capacity(); }
    }
    std::printf("\n");

    std::vector<int> w{1, 2, 3};
    const int* before = w.data();
    w.reserve(1000);
    std::printf("reserve moved the buffer: %s\n", w.data() != before ? "yes (old pointers dangle)" : "no");
    const int* stable = w.data();
    for (int i = 0; i < 500; ++i) w.push_back(i);           // within reserved capacity
    std::printf("push_back within reserve kept the buffer: %s\n", w.data() == stable ? "yes" : "no");

    std::vector<int> x{10, 20, 30, 40};
    auto it = x.begin() + 1;
    it = x.erase(it);                                        // returns the next valid iterator
    std::printf("erase returned iterator to %d, size=%zu capacity>=size: %d\n", *it, x.size(), x.capacity() >= x.size());
    x.clear();
    std::printf("clear: size=%zu capacity=%zu (memory kept)\n", x.size(), x.capacity());
    x.shrink_to_fit();
    std::printf("shrink_to_fit: capacity=%zu\n", x.capacity());

    std::vector<bool> flags(4);                              // not a real container of bool
    std::printf("sizeof(vector<bool>::reference) = %zu\n", sizeof(flags[0]));
}
