// Removing elements: erase-remove, erase in a loop, std::erase_if.
#include <algorithm>
#include <cstdio>
#include <map>
#include <vector>

static void show(const char* tag, const std::vector<int>& v) {
    std::printf("%-22s [", tag);
    for (int x : v) std::printf(" %d", x);
    std::printf(" ]  size=%zu\n", v.size());
}
int main() {
    const std::vector<int> base{1, 2, 3, 4, 5, 6};

    auto a = base;
    auto new_end = std::remove_if(a.begin(), a.end(), [](int x) { return x % 2 == 0; });
    show("after remove_if only:", a);                        // size unchanged; tail is moved-from garbage
    a.erase(new_end, a.end());
    show("after erase:", a);

    auto b = base;
    for (auto it = b.begin(); it != b.end();) {
        if (*it % 2 == 0) it = b.erase(it); else ++it;       // use the returned iterator; never ++ after erase
    }
    show("erase loop:", b);

    auto c = base;
    auto n = std::erase_if(c, [](int x) { return x % 2 == 0; });   // C++20
    show("std::erase_if:", c);
    std::printf("erase_if removed %zu\n", n);

    std::map<int, int> m{{1, 1}, {2, 2}, {3, 3}, {4, 4}};
    for (auto it = m.begin(); it != m.end();) {
        if (it->first % 2 == 0) it = m.erase(it); else ++it;   // node containers: only the erased iterator dies
    }
    std::printf("map after erase loop: %zu entries\n", m.size());
}
