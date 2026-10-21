// "Not reachable yet" needs a sentinel that survives `+ price - fee` without overflowing.
#include <climits>
#include <iostream>

int main() {
    constexpr long long price = 1LL << 40, fee = 1LL << 40;
    for (long long neg : {LLONG_MIN, LLONG_MIN / 4}) {
        long long a, b;
        const bool o1 = __builtin_add_overflow(neg, price, &a);   // NEG + price
        const bool o2 = __builtin_sub_overflow(a, fee, &b);        // ... - fee
        const bool o3 = __builtin_sub_overflow(neg, price, &a);   // NEG - price (a buy from an unreachable state)
        std::cout << (neg == LLONG_MIN ? "LLONG_MIN     " : "LLONG_MIN / 4 ") << "  NEG+price: " << (o1 ? "overflow" : "ok")
                  << "   -fee: " << (o2 ? "overflow" : "ok") << "   NEG-price: " << (o3 ? "overflow" : "ok") << "\n";
    }
}
