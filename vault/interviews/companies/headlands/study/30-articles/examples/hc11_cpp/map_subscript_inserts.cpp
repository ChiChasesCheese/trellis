// std::map::operator[] INSERTS a default-constructed value for a missing key.  A "read" written with it grows the map.
#include <iostream>
#include <iterator>
#include <map>

int live_at_wrong(std::map<long long, int>& history, long long t) { return history[t]; }  // inserts (t, 0) when t is missing

int live_at_right(const std::map<long long, int>& history, long long t) {
    auto it = history.upper_bound(t);  // first step strictly after t
    return it == history.begin() ? 0 : std::prev(it)->second;  // the step at or before t; before the first step: 0
}

int main() {
    std::map<long long, int> history = {{5, 1}, {9, 0}};
    std::cout << "size before: " << history.size() << "\n";
    for (long long t = 0; t < 12; ++t) (void)live_at_right(history, t);
    std::cout << "after 12 correct reads: " << history.size() << "\n";
    for (long long t = 0; t < 12; ++t) (void)live_at_wrong(history, t);
    std::cout << "after 12 reads through operator[]: " << history.size() << "  (each inserted step claims the count dropped to 0)\n";
}
