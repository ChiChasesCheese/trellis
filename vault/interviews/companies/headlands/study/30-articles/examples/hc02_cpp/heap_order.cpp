// std::priority_queue pops the LARGEST element under its comparator, and it is not stable.
#include <iostream>
#include <queue>
#include <vector>

struct Head {
    int value;
    int stream;
};

template <class Cmp>
void drain(const char* label, Cmp cmp) {
    std::priority_queue<Head, std::vector<Head>, Cmp> pq(cmp);
    for (int s = 0; s < 6; ++s) pq.push({1, s});  // six equal values from streams 0..5
    for (int s = 0; s < 3; ++s) pq.push({0, s});  // three smaller ones
    std::cout << label;
    while (!pq.empty()) {
        std::cout << pq.top().value << ':' << pq.top().stream << ' ';
        pq.pop();
    }
    std::cout << '\n';
}

int main() {
    std::priority_queue<int> by_default;  // default comparator std::less: a MAX-heap
    for (int x : {1, 5, 3}) by_default.push(x);
    std::cout << "default top: " << by_default.top() << "   (largest first)\n";

    // "a comes later than b" -> the smallest value comes out first.  Ties: whatever the heap internals give.
    drain("value only        : ", [](const Head& a, const Head& b) { return a.value > b.value; });
    // Add the stream index to the comparator and the order is fully determined: lower stream first.
    drain("value, then stream: ", [](const Head& a, const Head& b) {
        if (a.value != b.value) return a.value > b.value;
        return a.stream > b.stream;
    });
}
