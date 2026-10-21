// Turning a closed [s, e] into a half-open [s, e + 1) breaks at e = LLONG_MAX: e + 1 is signed overflow (undefined behaviour).
// Compare instead of converting: a closed end happened only if it is strictly before the start being considered.
#include <climits>
#include <iostream>

int main() {
    const long long e = LLONG_MAX;
    long long plus_one;
    const bool overflow = __builtin_add_overflow(e, 1LL, &plus_one);
    std::cout << "LLONG_MAX + 1 overflows: " << (overflow ? "yes" : "no") << " (wrapped value would be " << plus_one << ")\n";

    // closed: has the interval [?, e] ended before time s?   e < s   (no arithmetic)
    // half-open: has [?, e) ended by time s?                 e <= s
    const long long s = LLONG_MAX;
    std::cout << "closed end LLONG_MAX happened before s = LLONG_MAX: " << (e < s ? "yes" : "no") << "\n";
    std::cout << "half-open end LLONG_MAX happened by s = LLONG_MAX: " << (e <= s ? "yes" : "no") << "\n";
}
