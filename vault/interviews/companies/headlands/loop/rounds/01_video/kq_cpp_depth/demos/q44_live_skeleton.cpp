// A realistic CoderPad skeleton: parse commands, keep an order book, print the best prices.
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <optional>
#include <sstream>
#include <string>
#include <unordered_map>

enum class Side { Buy, Sell };

class OrderBook {
public:
    void add(std::uint64_t id, Side side, int price, int qty) {
        if (qty <= 0 || orders_.contains(id)) return;                 // reject bad input quietly
        orders_[id] = {side, price, qty};
        adjust(side, price, qty);
    }
    bool cancel(std::uint64_t id) {
        auto it = orders_.find(id);
        if (it == orders_.end()) return false;
        adjust(it->second.side, it->second.price, -it->second.qty);
        orders_.erase(it);
        return true;
    }
    std::optional<int> best_bid() const { return bids_.empty() ? std::nullopt : std::optional<int>(bids_.begin()->first); }
    std::optional<int> best_ask() const { return asks_.empty() ? std::nullopt : std::optional<int>(asks_.begin()->first); }
private:
    struct Order { Side side; int price; int qty; };
    void adjust(Side s, int price, int delta) {                     // works on both map types (generic lambda)
        auto apply = [&](auto& levels) { if ((levels[price] += delta) == 0) levels.erase(price); };
        if (s == Side::Buy) apply(bids_); else apply(asks_);
    }
    std::unordered_map<std::uint64_t, Order> orders_;
    std::map<int, int, std::greater<int>> bids_;       // highest price first
    std::map<int, int> asks_;                          // lowest price first
};

int main() {
    OrderBook ob;
    std::istringstream in("ADD 1 B 100 10\nADD 2 B 101 5\nADD 3 S 105 7\nCANCEL 2\nADD 4 S 103 1\nBEST\n");
    std::string cmd;
    while (in >> cmd) {
        if (cmd == "ADD") {
            std::uint64_t id; char side; int px, qty;
            in >> id >> side >> px >> qty;
            ob.add(id, side == 'B' ? Side::Buy : Side::Sell, px, qty);
        } else if (cmd == "CANCEL") {
            std::uint64_t id; in >> id;
            std::cout << "cancel " << id << (ob.cancel(id) ? " ok\n" : " unknown\n");
        } else if (cmd == "BEST") {
            auto b = ob.best_bid(), a = ob.best_ask();
            std::cout << "best bid " << (b ? std::to_string(*b) : "-") << ", best ask " << (a ? std::to_string(*a) : "-") << "\n";
        }
    }
}
