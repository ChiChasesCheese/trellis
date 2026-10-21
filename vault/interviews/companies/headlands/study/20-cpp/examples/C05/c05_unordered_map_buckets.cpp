// C05: unordered_map internals you can observe: buckets, load factor, rehash, collisions, custom hash.
#include <cstdint>
#include <functional>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>

// [[snip:rehash]]
void rehash_trace() {
    std::unordered_map<int, int> m;
    std::size_t last = m.bucket_count();
    std::cout << "  initial bucket_count=" << last << " max_load_factor=" << m.max_load_factor() << "\n  rehash points:";
    for (int i = 0; i < 100000; ++i) {
        m[i] = i;
        if (m.bucket_count() != last) { last = m.bucket_count(); std::cout << " " << m.size() << "->" << last; }
    }
    std::cout << "\n  final size=" << m.size() << " buckets=" << m.bucket_count() << " load_factor=" << m.load_factor() << "\n";
    std::unordered_map<int, int> r;
    r.reserve(100000);                                    // pre-size: zero rehashes during the fill
    std::size_t b = r.bucket_count();
    for (int i = 0; i < 100000; ++i) r[i] = i;
    std::cout << "  with reserve(100000): buckets " << b << " before and " << r.bucket_count() << " after the fill\n";
}
// [[/snip]]

// [[snip:custom]]
struct Key {
    std::uint32_t exch;
    std::string sym;
    bool operator==(const Key& o) const { return exch == o.exch && sym == o.sym; }
};
struct KeyHash {
    std::size_t operator()(const Key& k) const {
        std::size_t h = std::hash<std::string>{}(k.sym);
        return h ^ (std::hash<std::uint32_t>{}(k.exch) + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2));   // boost-style combine
    }
};
// [[/snip]]

// [[snip:bad_hash]]
struct BadHash { std::size_t operator()(int) const { return 42; } };    // every key collides: O(n) per operation
// [[/snip]]

int main() {
    std::cout << "[rehash]\n"; rehash_trace();

    std::cout << "[buckets and collisions]\n";
    std::unordered_map<int, int> m;
    for (int i = 0; i < 20; ++i) m[i * 1000] = i;
    std::size_t longest = 0;
    for (std::size_t b = 0; b < m.bucket_count(); ++b) longest = std::max(longest, m.bucket_size(b));
    std::cout << "  " << m.size() << " keys in " << m.bucket_count() << " buckets, longest chain " << longest << "\n";

    std::cout << "[custom key]\n";
    std::unordered_map<Key, int, KeyHash> pos;
    pos[{1, "AAPL"}] = 100;
    pos[{2, "AAPL"}] += 50;
    pos[{1, "AAPL"}] += 25;
    std::cout << "  (1,AAPL)=" << pos[{1, "AAPL"}] << " (2,AAPL)=" << pos[{2, "AAPL"}] << " entries=" << pos.size() << "\n";

    std::cout << "[all keys collide]\n";
    std::unordered_set<int, BadHash> bad;
    for (int i = 0; i < 1000; ++i) bad.insert(i);
    std::size_t worst = 0;
    for (std::size_t b = 0; b < bad.bucket_count(); ++b) worst = std::max(worst, bad.bucket_size(b));
    std::cout << "  1000 ints with a constant hash: longest chain " << worst << " (lookups degrade to a linear scan)\n";
    std::cout << "[operator[] inserts]\n";
    std::unordered_map<std::string, int> wc;
    int miss = wc["absent"];                     // operator[] default-constructs a missing value and INSERTS it
    std::cout << "  value " << miss << ", size now " << wc.size() << "; find() leaves it alone: "
              << (wc.find("other") == wc.end()) << ", size " << wc.size() << "\n";
}
