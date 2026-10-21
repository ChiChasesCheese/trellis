// Part 1 in the simplest possible way: a vector scanned linearly.  Correct, but every query is O(n).
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

struct Naive {
    std::vector<std::pair<long long, long long>> orders;  // {id, qty} in insertion order
    std::size_t find(long long id) const {
        for (std::size_t i = 0; i < orders.size(); ++i)
            if (orders[i].first == id) return i;
        throw std::runtime_error("unknown id");
    }
    void put(long long id, long long qty) { orders.emplace_back(id, qty); }
    long long count_up_to(long long id) const { return static_cast<long long>(find(id)) + 1; }
    long long qty_up_to(long long id) const {
        long long s = 0;
        for (std::size_t i = 0, at = find(id); i <= at; ++i) s += orders[i].second;
        return s;
    }
};

int main() {
    Naive s;
    s.put(10, 5); s.put(20, 3); s.put(30, 7);
    std::cout << "COUNT 30 = " << s.count_up_to(30) << ", QTY 20 = " << s.qty_up_to(20) << "\n";
}
