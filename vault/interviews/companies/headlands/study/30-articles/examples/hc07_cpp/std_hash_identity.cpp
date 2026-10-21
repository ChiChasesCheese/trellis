// std::hash<integer> is (in libc++ and libstdc++) the identity, so `hash & mask` keeps only the low bits of the key.
// A packed ticker has zeros there.  Simulate linear probing for the 17576 three-letter codes.
#include <cstdint>
#include <functional>
#include <iostream>
#include <vector>

using Key = std::uint64_t;

Key pack3(char a, char b, char c) {  // 5 bits per letter, first letter in bits 35..39: the low 25 bits stay 0
    auto code = [](char ch) { return static_cast<Key>(ch - 'A' + 1); };
    return (code(a) << 35) | (code(b) << 30) | (code(c) << 25);
}

template <class Index>
std::size_t longest_probe(const std::vector<Key>& keys, std::size_t capacity, Index index) {
    std::vector<std::uint8_t> used(capacity, 0);
    std::size_t worst = 0;
    for (Key k : keys) {
        const std::size_t home = index(k);
        std::size_t i = home;
        while (used[i]) i = (i + 1) & (capacity - 1);
        used[i] = 1;
        worst = std::max(worst, (i - home) & (capacity - 1));
    }
    return worst;
}

int main() {
    std::vector<Key> keys;
    for (char a = 'A'; a <= 'Z'; ++a)
        for (char b = 'A'; b <= 'Z'; ++b)
            for (char c = 'A'; c <= 'Z'; ++c) keys.push_back(pack3(a, b, c));

    constexpr std::size_t capacity = 1 << 16;
    constexpr int shift = 64 - 16;
    std::cout << "std::hash<uint64_t>(42) = " << std::hash<std::uint64_t>{}(42) << "   (the identity)\n";
    std::cout << "17576 codes, capacity " << capacity << ", longest probe:\n";
    std::cout << "  std::hash & mask     : " << longest_probe(keys, capacity, [](Key k) { return std::hash<Key>{}(k) & (capacity - 1); }) << "\n";
    std::cout << "  (key * golden) >> 48 : " << longest_probe(keys, capacity, [](Key k) { return static_cast<std::size_t>((k * 0x9E3779B97F4A7C15ull) >> shift); }) << "\n";
}
