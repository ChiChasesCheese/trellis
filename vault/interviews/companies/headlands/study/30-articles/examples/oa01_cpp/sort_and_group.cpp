#include <algorithm>
#include <iostream>
#include <vector>

struct Chain { int start; long long total; };

int main() {
    std::vector<Chain> v{{9, 10}, {4, 10}, {1, 105}, {5, 200}};
    // Strict weak ordering: total descending, ties by start ascending.  `<=` here would be undefined behaviour.
    std::ranges::sort(v, [](const Chain& a, const Chain& b) {
        return a.total != b.total ? a.total > b.total : a.start < b.start;
    });
    for (auto& c : v) std::cout << c.start << ":" << c.total << " ";
    std::cout << "\n";
}
