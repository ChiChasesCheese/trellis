// A small "framework" function with a classic bug: average of the last k prices, off by one at the start.
#include <cassert>
#include <cstdio>
#include <vector>

double avg_last(const std::vector<double>& px, std::size_t k) {
    assert(k > 0 && k <= px.size());           // contract: trap bad input in debug builds
    double sum = 0;
    for (std::size_t i = px.size() - k + 1; i < px.size(); ++i)   // BUG: should start at px.size() - k
        sum += px[i];
    return sum / static_cast<double>(k);
}

int main() {
    std::vector<double> px{10, 20, 30, 40};
    std::printf("avg of last 2 = %.2f (expected 35.00)\n", avg_last(px, 2));
}
