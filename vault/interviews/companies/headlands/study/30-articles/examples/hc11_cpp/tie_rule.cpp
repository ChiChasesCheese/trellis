// The tie rule of a sweep line: at the same time, an END must be processed before a START ([1,3) and [3,5) do not overlap).
// With std::pair<time, delta> the default order (-1 < +1) is already right; sorting only by time leaves it to chance.
#include <algorithm>
#include <iostream>
#include <utility>
#include <variant>
#include <vector>

using Event = std::pair<long long, int>;  // (time, +1 start / -1 end)

int sweep(std::vector<Event> events, bool by_time_only) {
    if (by_time_only) {
        // Wrong: events with equal times keep whatever relative order they had (here: all starts were appended before all ends).
        std::stable_sort(events.begin(), events.end(), [](const Event& a, const Event& b) { return a.first < b.first; });
    } else {
        std::sort(events.begin(), events.end());  // (time, delta): -1 sorts before +1
    }
    int live = 0, best = 0;
    for (const auto& [time, delta] : events) {
        (void)time;
        live += delta;
        best = std::max(best, live);
    }
    return best;
}

struct Close { long long time; };
struct Open { long long time; };

int main() {
    // [1,3) and [3,5): the answer must be 1.
    std::vector<Event> events = {{1, +1}, {3, +1}, {3, -1}, {5, -1}};  // starts of both intervals, then their ends
    std::cout << "time only, ties in insertion order: " << sweep(events, true) << "   (wrong: start at 3 came before the end at 3)\n";
    std::cout << "(time, delta) pairs:                " << sweep(events, false) << "\n";

    // The same rule as the ORDER OF A VARIANT's alternatives: Close is alternative 0, Open is alternative 1.
    using SweepEvent = std::variant<Close, Open>;
    std::vector<SweepEvent> ev = {Open{1}, Open{3}, Close{3}, Close{5}};
    auto time_of = [](const SweepEvent& e) { return std::visit([](const auto& x) { return x.time; }, e); };
    std::sort(ev.begin(), ev.end(), [&](const SweepEvent& a, const SweepEvent& b) { return std::pair(time_of(a), a.index()) < std::pair(time_of(b), b.index()); });
    for (const auto& e : ev) std::cout << (e.index() == 0 ? "Close@" : "Open@") << time_of(e) << " ";
    std::cout << "\n";
}
