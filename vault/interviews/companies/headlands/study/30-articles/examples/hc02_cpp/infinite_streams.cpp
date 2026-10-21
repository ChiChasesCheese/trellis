// The finished lazy merger on two infinite ranges.  `reference.hpp` is the code of the lecture.
#include <iostream>
#include <ranges>
#include <vector>

#include "../../../../loop/rounds/01_video/hc02_merge_k_streams/cpp/reference.hpp"

int main() {
    using namespace mergek;
    auto evens = from_range(std::views::iota(0) | std::views::transform([](int x) { return 2 * x; }));
    auto threes = from_range(std::views::iota(0) | std::views::transform([](int x) { return 3 * x; }));

    std::vector<Source<int>> sources;
    sources.push_back(std::move(evens));
    sources.push_back(std::move(threes));
    Merger<int> merged(std::move(sources));  // nothing is pulled yet; Merger is an input range

    for (int x : merged | std::views::take(10)) std::cout << x << ' ';
    std::cout << "\n";
}
