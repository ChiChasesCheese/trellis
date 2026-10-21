// A comparator that ignores ties makes top-k depend on the order the data arrives in.  A full order does not.
#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct Event { int index; std::string ticker; long long notional; };

// Keep the 2 best by notional only (larger is better): the heap top is the worst kept event.
std::vector<int> top2_notional_only(const std::vector<Event>& events) {
    auto better = [](const Event* a, const Event* b) { return a->notional > b->notional; };
    std::priority_queue<const Event*, std::vector<const Event*>, decltype(better)> heap(better);
    for (const Event& e : events) {
        if (heap.size() < 2) heap.push(&e);
        else if (better(&e, heap.top())) { heap.pop(); heap.push(&e); }
    }
    std::vector<int> out;
    while (!heap.empty()) { out.push_back(heap.top()->index); heap.pop(); }
    std::sort(out.begin(), out.end());
    return out;
}

// Same, with the full order: notional descending, then ticker ascending, then index ascending.
std::vector<int> top2_full_order(const std::vector<Event>& events) {
    auto better = [](const Event* a, const Event* b) {
        if (a->notional != b->notional) return a->notional > b->notional;
        if (a->ticker != b->ticker) return a->ticker < b->ticker;
        return a->index < b->index;
    };
    std::priority_queue<const Event*, std::vector<const Event*>, decltype(better)> heap(better);
    for (const Event& e : events) {
        if (heap.size() < 2) heap.push(&e);
        else if (better(&e, heap.top())) { heap.pop(); heap.push(&e); }
    }
    std::vector<int> out;
    while (!heap.empty()) { out.push_back(heap.top()->index); heap.pop(); }
    std::sort(out.begin(), out.end());
    return out;
}

void show(const char* label, const std::vector<int>& v) {
    std::cout << label;
    for (int i : v) std::cout << " " << i;
    std::cout << "\n";
}

int main() {
    // Three events tie at notional 100; only two can stay.
    std::vector<Event> forward = {{0, "AAA", 100}, {1, "BBB", 100}, {2, "CCC", 100}};
    std::vector<Event> reversed = {{2, "CCC", 100}, {1, "BBB", 100}, {0, "AAA", 100}};
    show("notional only, forward :", top2_notional_only(forward));
    show("notional only, reversed:", top2_notional_only(reversed));
    show("full order,    forward :", top2_full_order(forward));
    show("full order,    reversed:", top2_full_order(reversed));
}
