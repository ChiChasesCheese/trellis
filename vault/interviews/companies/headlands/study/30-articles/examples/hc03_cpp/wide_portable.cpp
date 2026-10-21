// A 128-bit accumulator from two 64-bit halves: what to write when __int128 does not exist (MSVC).
#include <cassert>
#include <climits>
#include <cstdint>
#include <iostream>
#include <random>

struct Wide {
    std::int64_t hi = 0;       // signed high half
    std::uint64_t lo = 0;      // unsigned low half

    Wide plus(std::int64_t x) const {
        std::uint64_t nlo = lo + static_cast<std::uint64_t>(x);            // unsigned: wraps, well defined
        std::uint64_t carry = nlo < lo ? 1 : 0;                           // wrapped => carry into hi
        std::uint64_t sign_ext = x < 0 ? ~std::uint64_t{0} : 0;           // high half of the sign-extended x
        return {static_cast<std::int64_t>(static_cast<std::uint64_t>(hi) + sign_ext + carry), nlo};
    }
    Wide merge(const Wide& o) const {
        std::uint64_t nlo = lo + o.lo;
        std::uint64_t carry = nlo < lo ? 1 : 0;
        return {static_cast<std::int64_t>(static_cast<std::uint64_t>(hi) + static_cast<std::uint64_t>(o.hi) + carry), nlo};
    }
    bool fits_long() const {                       // hi must be the sign extension of lo
        return hi == (static_cast<std::int64_t>(lo) < 0 ? -1 : 0);
    }
    __int128 to_i128() const { return (static_cast<__int128>(hi) << 64) | lo; }   // only for checking here
};

int main() {
    std::mt19937_64 rnd(1);
    Wide w;
    __int128 ref = 0;
    for (int i = 0; i < 1'000'000; ++i) {
        std::int64_t x = rnd() % 3 == 0 ? static_cast<std::int64_t>(rnd()) : (rnd() % 2 ? LLONG_MAX : LLONG_MIN);
        w = w.plus(x);
        ref += x;
        assert(w.to_i128() == ref);
        assert(w.fits_long() == (ref >= LLONG_MIN && ref <= LLONG_MAX));
    }
    Wide a = Wide{}.plus(LLONG_MAX).plus(LLONG_MAX), b = Wide{}.plus(LLONG_MIN);
    assert(a.merge(b).to_i128() == static_cast<__int128>(LLONG_MAX) * 2 + LLONG_MIN);
    std::cout << "portable Wide agrees with __int128 on 1,000,000 random adds\n";
}
