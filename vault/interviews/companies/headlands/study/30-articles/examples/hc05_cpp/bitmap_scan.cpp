// Finding the next non-empty price level among 100000 ticks: scan 64 levels per step with one count-zeros instruction.
#include <bit>
#include <cstdint>
#include <iostream>
#include <vector>

// first set bit at position >= from, or -1
int at_or_above(const std::vector<std::uint64_t>& bits, int from) {
    std::size_t w = static_cast<std::size_t>(from) >> 6;
    std::uint64_t word = bits[w] & (~0ull << (from & 63));  // clear the bits below `from`
    for (;;) {
        if (word != 0) return static_cast<int>(w * 64) + std::countr_zero(word);
        if (++w >= bits.size()) return -1;
        word = bits[w];
    }
}

// last set bit at position <= from, or -1
int at_or_below(const std::vector<std::uint64_t>& bits, int from) {
    std::size_t w = static_cast<std::size_t>(from) >> 6;
    std::uint64_t word = bits[w] & (~0ull >> (63 - (from & 63)));  // clear the bits above `from`
    for (;;) {
        if (word != 0) return static_cast<int>(w * 64) + 63 - std::countl_zero(word);
        if (w == 0) return -1;
        word = bits[--w];
    }
}

int main() {
    constexpr int ticks = 100000;
    std::vector<std::uint64_t> bits((ticks + 63) / 64, 0);
    for (int p : {10, 90000, 99999}) bits[static_cast<std::size_t>(p) >> 6] |= 1ull << (p & 63);

    std::cout << "first level at or above 11    : " << at_or_above(bits, 11) << "   (skipped " << (90000 - 11) / 64 << " empty words)\n";
    std::cout << "last level at or below 89999  : " << at_or_below(bits, 89999) << "\n";
    std::cout << "first level at or above 99999 : " << at_or_above(bits, 99999) << "\n";
    std::cout << "last level at or below 9      : " << at_or_below(bits, 9) << "   (none)\n";
}
