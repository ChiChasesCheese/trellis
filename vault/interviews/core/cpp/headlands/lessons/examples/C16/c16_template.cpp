// C16: a CoderPad-ready single-file skeleton: includes, solution, assert-style tests, main.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <optional>
#include <queue>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

// [[snip:check]]
#define CHECK(cond) do { if (!(cond)) { std::cerr << "FAILED line " << __LINE__ << ": " #cond "\n"; std::exit(1); } } while (0)
#define CHECK_EQ(a, b) do { auto va = (a); auto vb = (b); if (!(va == vb)) { std::cerr << "FAILED line " << __LINE__ << ": " #a " == " #b "  (" << va << " vs " << vb << ")\n"; std::exit(1); } } while (0)
// [[/snip]]

// ---- Problem 1: two sum (hash map, O(n)) ----
// [[snip:twosum]]
std::optional<std::pair<int, int>> two_sum(const std::vector<int>& a, int target) {
    std::unordered_map<int, int> seen;                    // value -> index
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
        if (auto it = seen.find(target - a[i]); it != seen.end()) return std::pair{it->second, i};
        seen.emplace(a[i], i);
    }
    return std::nullopt;
}
// [[/snip]]

// ---- Problem 2: top-k trades by notional (min-heap of size k, O(n log k)) ----
// [[snip:topk]]
struct Trade { std::string sym; long qty; long px_cents; };

std::vector<Trade> top_k(const std::vector<Trade>& trades, std::size_t k) {
    auto notional = [](const Trade& t) { return t.qty * t.px_cents; };
    auto worse = [&](const Trade& a, const Trade& b) { return notional(a) > notional(b); };   // "greater" => smallest on top
    std::priority_queue<Trade, std::vector<Trade>, decltype(worse)> heap(worse);
    for (const auto& t : trades) {
        heap.push(t);
        if (heap.size() > k) heap.pop();                  // drop the smallest of the k+1
    }
    std::vector<Trade> out;
    while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }
    std::reverse(out.begin(), out.end());                 // largest first
    return out;
}
// [[/snip]]

// ---- Problem 3: order book best bid/ask with std::map ----
// [[snip:book]]
class Book {
    std::map<long, long, std::greater<long>> bids_;       // price -> qty, best (highest) first
    std::map<long, long> asks_;                           // best (lowest) first
public:
    void add(bool buy, long px, long qty) { (buy ? bids_[px] : asks_[px]) += qty; }
    void cancel(bool buy, long px, long qty) {
        auto erase_from = [&](auto& m) {
            auto it = m.find(px);
            if (it == m.end()) return;
            it->second -= qty;
            if (it->second <= 0) m.erase(it);             // never leave empty levels behind
        };
        if (buy) erase_from(bids_); else erase_from(asks_);
    }
    std::optional<long> best_bid() const { return bids_.empty() ? std::nullopt : std::optional(bids_.begin()->first); }
    std::optional<long> best_ask() const { return asks_.empty() ? std::nullopt : std::optional(asks_.begin()->first); }
};
// [[/snip]]

// [[snip:tests]]
void run_tests() {
    auto r = two_sum({2, 7, 11, 15}, 9);
    CHECK(r.has_value());
    CHECK_EQ(r->first, 0);
    CHECK_EQ(r->second, 1);
    CHECK(!two_sum({1, 2}, 100).has_value());
    CHECK(!two_sum({}, 0).has_value());                   // edge: empty input

    std::vector<Trade> ts{{"A", 10, 100}, {"B", 5, 1000}, {"C", 1, 50}, {"D", 20, 100}};
    auto top = top_k(ts, 2);
    CHECK_EQ(top.size(), 2u);
    CHECK_EQ(top[0].sym, "B");                            // 5000
    CHECK_EQ(top[1].sym, "D");                            // 2000
    CHECK_EQ(top_k(ts, 0).size(), 0u);                    // edge: k == 0
    CHECK_EQ(top_k(ts, 99).size(), 4u);                   // edge: k > n

    Book b;
    CHECK(!b.best_bid().has_value());
    b.add(true, 100, 5); b.add(true, 101, 3); b.add(false, 103, 4); b.add(false, 102, 1);
    CHECK_EQ(*b.best_bid(), 101L);
    CHECK_EQ(*b.best_ask(), 102L);
    b.cancel(true, 101, 3);
    CHECK_EQ(*b.best_bid(), 100L);
}
// [[/snip]]

int main() {
    run_tests();
    std::cout << "all tests passed\n";
}
