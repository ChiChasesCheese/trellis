// std::hash<long long> is the identity.  With a power-of-two bucket array (libc++ keeps one when you ask for one) the bucket is
// hash & mask, so keys that differ only in their high bits all land in bucket 0.
#include <cstdint>
#include <functional>
#include <iostream>
#include <unordered_map>

struct Mixed {  // splitmix64 finaliser
    std::size_t operator()(long long id) const noexcept {
        auto x = static_cast<std::uint64_t>(id);
        x ^= x >> 30; x *= 0xBF58476D1CE4E5B9ull;
        x ^= x >> 27; x *= 0x94D049BB133111EBull;
        x ^= x >> 31;
        return static_cast<std::size_t>(x);
    }
};

template <class Map> std::size_t longest_chain(Map& m) {
    std::size_t worst = 0;
    for (std::size_t b = 0; b < m.bucket_count(); ++b) worst = std::max(worst, m.bucket_size(b));
    return worst;
}

int main() {
    std::cout << "std::hash<long long>(42) = " << std::hash<long long>{}(42) << "\n";
    std::unordered_map<long long, int> plain;
    std::unordered_map<long long, int, Mixed> mixed;
    plain.rehash(4096);   // a power of two, as the order sequence asks for min_capacity buckets
    mixed.rehash(4096);
    for (long long i = 0; i < 2000; ++i) { plain[i << 32] = 1; mixed[i << 32] = 1; }
    std::cout << "2000 keys of the form i<<32, longest bucket chain:  identity hash = " << longest_chain(plain)
              << ",  mixed hash = " << longest_chain(mixed) << "\n";
}
