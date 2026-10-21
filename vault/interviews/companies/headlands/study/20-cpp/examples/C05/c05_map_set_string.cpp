// C05: std::map (red-black tree), ordered queries, and std::string small-string optimisation (SSO).
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <string>

// [[snip:book]]
// Order book side: price -> total quantity. std::map is sorted, so best bid/ask are O(1) at the ends, lookups O(log n).
void order_book() {
    std::map<long, long, std::greater<long>> bids;     // descending: begin() is the best (highest) bid
    std::map<long, long> asks;                         // ascending : begin() is the best (lowest) ask
    bids[10010] += 100; bids[10005] += 50; bids[10010] += 25; bids[9990] += 300;
    asks[10020] += 40;  asks[10030] += 10; asks[10025] += 75;
    std::cout << "  best bid " << bids.begin()->first << " x " << bids.begin()->second
              << ", best ask " << asks.begin()->first << " x " << asks.begin()->second << "\n";
    auto it = bids.lower_bound(10006);                 // first key NOT BEFORE 10006 in this ordering (<= 10006 here)
    std::cout << "  first bid at or below 10006: " << it->first << "\n";
    std::cout << "  asks in [10020,10026]:";
    for (auto i = asks.lower_bound(10020); i != asks.upper_bound(10026); ++i) std::cout << " " << i->first;
    std::cout << "\n";
    if (auto f = asks.find(10025); f != asks.end()) asks.erase(f);     // erase by iterator: O(1) amortised
    std::cout << "  asks left: " << asks.size() << "\n";
}
// [[/snip]]

// [[snip:sso]]
bool is_inline(const std::string& s) {             // does the character buffer live inside the string object itself?
    auto b = reinterpret_cast<std::uintptr_t>(&s);
    auto d = reinterpret_cast<std::uintptr_t>(s.data());
    return d >= b && d < b + sizeof(std::string);
}

void sso() {
    std::cout << "  sizeof(std::string)=" << sizeof(std::string) << ", capacity of an empty string=" << std::string().capacity() << "\n";
    for (std::size_t n : {5, 22, 23, 40}) {
        std::string s(n, 'x');
        std::cout << "  length " << n << ": characters " << (is_inline(s) ? "INSIDE the object (no allocation)" : "on the HEAP") << "\n";
    }
}
// [[/snip]]

// [[snip:node]]
// Node-based containers pay one allocation per element plus bookkeeping pointers.
void node_cost() {
    std::cout << "  sizeof(std::pair<long,long>)=" << sizeof(std::pair<long, long>)
              << " but each std::map<long,long> node is a separate heap block: payload + parent/left/right pointers + colour\n";
}
// [[/snip]]

int main() {
    std::cout << "[order book]\n"; order_book();
    std::cout << "[string SSO]\n"; sso();
    std::cout << "[node cost]\n"; node_cost();
    std::set<int> s{5, 1, 9, 3};
    std::cout << "[set] sorted unique:";
    for (int x : s) std::cout << " " << x;
    std::cout << "; count(3)=" << s.count(3) << " contains(4)=" << s.contains(4) << "\n";
    std::map<std::string, int> m;
    std::cout << "[map] m[\"x\"] on a missing key inserts: " << m["x"] << ", size " << m.size() << "\n";
}
