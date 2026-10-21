// Rolling DP with a cooldown: every transition must read YESTERDAY's values.  Reading today's already-updated `idle` lets
// a buy happen the day the cooldown ends... or, here, the day after the sale.
#include <algorithm>
#include <array>
#include <climits>
#include <iostream>
#include <vector>

constexpr long long NEG = LLONG_MIN / 4;

long long with_cooldown(const std::vector<long long>& prices, bool read_todays_idle) {
    std::array<long long, 3> s{0, NEG, NEG};  // {idle, held, cool}
    for (long long p : prices) {
        const auto yesterday = s;
        s[2] = yesterday[1] + p;                                   // sold today
        s[0] = std::max(yesterday[0], yesterday[2]);               // rest, or the cooldown ended
        s[1] = std::max(yesterday[1], (read_todays_idle ? s[0] : yesterday[0]) - p);  // buy
    }
    return std::max(s[0], s[2]);
}

int main() {
    const std::vector<long long> prices{1, 2, 3, 0, 2};
    std::cout << "buy from yesterday's idle: " << with_cooldown(prices, false) << "   (correct: 3)\n";
    std::cout << "buy from today's idle:     " << with_cooldown(prices, true) << "   (wrong: sells on day 1 and buys again on day 2, the cooldown day)\n";
}
