---
id: hl-c16-book
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 6
---
## Q
用 C++ 写出订单簿最简版 `Book`：`add`、`cancel`、`best_bid`、`best_ask`。取消后数量归零要怎么处理？

## A
```cpp
class Book {
    std::map<long, long, std::greater<long>> bids_;   // 价格 -> 数量，最高价在前
    std::map<long, long> asks_;                       // 最低价在前
public:
    void add(bool buy, long px, long qty) { (buy ? bids_[px] : asks_[px]) += qty; }
    void cancel(bool buy, long px, long qty) {
        auto erase_from = [&](auto& m) {
            auto it = m.find(px);
            if (it == m.end()) return;
            it->second -= qty;
            if (it->second <= 0) m.erase(it);         // 不留空档位
        };
        if (buy) erase_from(bids_); else erase_from(asks_);
    }
    std::optional<long> best_bid() const {
        return bids_.empty() ? std::nullopt : std::optional(bids_.begin()->first); }
    std::optional<long> best_ask() const {
        return asks_.empty() ? std::nullopt : std::optional(asks_.begin()->first); }
};
```
- 数量 ≤ 0 就 `erase` 档位，**绝不留下空档位**，否则最优价会错。
