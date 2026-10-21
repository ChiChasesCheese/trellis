# hc05 · Market Order Book（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。下面所有代码块按顺序拼起来就是一份能编译、能通过全部测试的完整实现。

## 1. 题目

### 1.1 订单簿是什么

交易所对每个品种维护一本**订单簿**（order book）：想买的人挂**买单**（bid），想卖的人挂**卖单**（ask），每张单有 `id`、价格、数量。

* 价格用整数 **tick**（最小报价单位）表示，不用浮点数。数量是整数。
* 买盘里出价最高的叫 **best bid**，卖盘里要价最低的叫 **best ask**。
* 同一个价格上的所有单合在一起叫一个**价位**（price level）。
* 新来一张单，如果「买价 ≥ 当前最低卖价」（或「卖价 ≤ 当前最高买价」），就和簿上的单**成交**（match）；剩下没成交的挂在簿上等人来吃。
* **价格-时间优先**（price-time priority）：先吃价格最好的价位；同一价位按到达顺序，先来的先成交。
* 成交价取**被动方**（簿上先挂的那张，maker）的价格，主动方（taker）拿到价格改善。

### 1.2 四个 Part

| Part | 内容 |
|---|---|
| 1 | 只维护，**不撮合**：`add`、`cancel`、`modify`、`best_bid`/`best_ask`、`depth`、同价位 FIFO。减量保持排队位置，增量排到队尾；价位总量溢出要报错且簿不变 |
| 2 | `execute(Command)` → 事件：限价单、市价单、撤单、改量；用 `std::variant` 表示命令和事件；文本接口 `parse` / `render` / `replay` |
| 3 | 批量限价撮合（`run_batch`）：一批 `[side, price, qty]` 按到达顺序撮合，汇总成交、成交量、名义金额、剩余盘口 |
| 4 | 性能追问「每秒几百万条命令，GC/分配器很忙」：`TickBook`——整数 tick、数组代替树、预分配池、O(1) 撤单、热路径零分配 |

样例（先手算再看代码）：

```
LIMIT 1 SELL 101 5          REST id=1 side=SELL px=101 qty=5
LIMIT 2 SELL 101 3          REST id=2 side=SELL px=101 qty=3
LIMIT 3 SELL 102 4          REST id=3 side=SELL px=102 qty=4
LIMIT 4 BUY 101 6           TRADE taker=4 maker=1 side=BUY px=101 qty=5     ← 先吃 1 号（先到）
                            TRADE taker=4 maker=2 side=BUY px=101 qty=1     ← 再吃 2 号的 1 张
limit 5 buy 103 10          TRADE taker=5 maker=2 side=BUY px=101 qty=2     ← 2 号剩 2 张
                            TRADE taker=5 maker=3 side=BUY px=102 qty=4     ← 价格更高的 102 档
                            REST id=5 side=BUY px=103 qty=4                 ← 10 − 2 − 4 = 4 张挂簿
MARKET 6 SELL 5             TRADE taker=6 maker=5 side=SELL px=103 qty=4    ← 成交价取 maker 的 103
                            CANCEL id=6 remaining=1                         ← 市价单吃不完的部分作废
CANCEL 3                    REJECT id=3 reason=unknown id                   ← 3 号早被吃光了
MODIFY 9 1                  REJECT id=9 reason=unknown id
```

## 2. 数据结构选型

三个需求，三个结构：

| 需求 | 结构 | 复杂度 |
|---|---|---|
| 反复取「最好的价位」，成交会把最好的价位吃光，价位要按价格有序 | **`std::map<价格, 价位>`**（红黑树） | 最优价：`begin()` 是 O(1)，`rbegin()` 是 O(log L)；插入删除 O(log L)；L = 价位数（很小） |
| 同价位按到达顺序排队，撤单要从**队伍中间**拿掉，还要 O(1) | **`std::list<订单>`** + 保存的迭代器 | 队尾插入、任意位置删除、移到队尾，都是 O(1) |
| 撤单 / 改量只给 `id`，不给价格 | **`std::unordered_map<id, Locator>`** | O(1) 平均；`Locator` 里存着价位和订单节点的迭代器 |

```
asks_ (map, 价格升序)         bids_ (map, 价格升序；最优 = 最后一个)
  101 ─▶ [#1(5)] ─ [#2(3)]      99 ─▶ [#7(2)]
  102 ─▶ [#3(4)]               100 ─▶ [#6(1)] ─ [#9(8)]
                              by_id_:  1 ─▶ {Sell, 指向 101 价位, 指向 #1 节点}  …
```

**为什么可以保存迭代器**：`std::map` 和 `std::list` 是**节点式**容器，插入或删除**别的**元素不会使已有元素的迭代器失效（只有被删的元素本身的迭代器失效）；`std::list::splice` 能把节点原地接到另一个位置，迭代器依然有效。`std::vector` 做不到：增长时可能把所有元素搬走。

```cpp
// Which containers keep an iterator valid while OTHER elements come and go -- the property the id index relies on.
#include <iostream>
#include <list>
#include <map>
#include <vector>

int main() {
    // std::list: an iterator stays valid until its own element is erased.  splice moves the node without invalidating it.
    std::list<int> queue{10, 20, 30};
    auto second = std::next(queue.begin());                 // points at 20
    queue.push_back(40);
    queue.erase(queue.begin());                             // erase 10
    queue.splice(queue.end(), queue, second);               // move 20 to the back: same node, same iterator
    std::cout << "list after splice:";
    for (int x : queue) std::cout << ' ' << x;
    std::cout << "   *second = " << *second << "\n";

    // std::map: same guarantee for its nodes.
    std::map<long long, int> ladder{{100, 1}, {101, 2}, {102, 3}};
    auto level = ladder.find(101);
    ladder.erase(100);
    ladder.emplace(99, 0);
    std::cout << "map iterator still sees " << level->first << " -> " << level->second << "\n";

    // std::vector: any growth may move every element, so iterators and references become dangling.
    std::vector<int> v{1, 2, 3};
    const int* before = &v[0];
    v.reserve(1000);                                        // reallocates
    std::cout << "vector element moved: " << std::boolalpha << (before != &v[0]) << "\n";

    // A copy of a structure that stores iterators still holds iterators into the ORIGINAL.
    struct Indexed {
        std::list<int> items;
        std::list<int>::iterator first;
    };
    Indexed a{{1, 2, 3}, {}};
    a.first = a.items.begin();
    Indexed b = a;                                          // copies the list, copies the iterator value
    std::cout << "copy's iterator points into the copy's list: " << (&*b.first == &*b.items.begin()) << "\n";
}
```

最后一行说明了另一件事：**包含迭代器的结构不能直接拷贝**——拷贝出来的迭代器仍然指着原对象的节点。所以 `OrderBook` 删除拷贝构造 / 拷贝赋值，只能移动；节点式容器被移动时节点不动，保存的迭代器仍然有效（测试里先移动、再撤单，由 AddressSanitizer 把关）。

## 3. 类型

```cpp
#include <algorithm>
#include <array>
#include <bit>
#include <cctype>
#include <charconv>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <format>
#include <iterator>
#include <list>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>
namespace book {
```

```cpp
enum class Side { Buy, Sell };
constexpr Side opposite(Side s) noexcept { return s == Side::Buy ? Side::Sell : Side::Buy; }
constexpr std::string_view name(Side s) noexcept { return s == Side::Buy ? "BUY" : "SELL"; }

/// One price level of the ladder: price in ticks, total resting quantity, number of orders.
struct Level {
    long long price;
    long long total_qty;
    int order_count;
    friend bool operator==(const Level&, const Level&) = default;
};
/// A resting order as seen from outside (qty = what is left).
struct Order {
    long long id;
    Side side;
    long long price;
    long long qty;
    friend bool operator==(const Order&, const Order&) = default;
};

inline constexpr std::string_view INVALID_ID = "invalid id";
inline constexpr std::string_view INVALID_PRICE = "invalid price";
inline constexpr std::string_view INVALID_QTY = "invalid quantity";
inline constexpr std::string_view DUPLICATE_ID = "duplicate id";
inline constexpr std::string_view UNKNOWN_ID = "unknown id";
inline constexpr std::string_view OVERFLOW_REASON = "overflow";
```

* `Side` 是 `enum class`：不会隐式转成整数；`opposite`、`name` 是 `constexpr` 函数。
* `Level` / `Order` 用 `friend bool operator==(...) = default;`：C++20 的默认比较，测试直接 `==`。
* 失败原因是 `std::string_view` 常量，指向静态存储，`Rejected` 里存它不分配、不悬空。

```cpp
struct Limit {
    long long id;
    Side side;
    long long price;
    long long qty;
    friend bool operator==(const Limit&, const Limit&) = default;
};
struct Market {
    long long id;
    Side side;
    long long qty;
    friend bool operator==(const Market&, const Market&) = default;
};
struct Cancel {
    long long id;
    friend bool operator==(const Cancel&, const Cancel&) = default;
};
struct Modify {
    long long id;
    long long new_qty;
    friend bool operator==(const Modify&, const Modify&) = default;
};
using Command = std::variant<Limit, Market, Cancel, Modify>;

/// price = the price of the passive (resting) order.
struct Trade {
    long long taker_id;
    long long maker_id;
    Side taker_side;
    long long price;
    long long qty;
    friend bool operator==(const Trade&, const Trade&) = default;
};
struct Rested {
    long long id;
    Side side;
    long long price;
    long long qty;
    friend bool operator==(const Rested&, const Rested&) = default;
};
struct Cancelled {
    long long id;
    long long remaining;
    friend bool operator==(const Cancelled&, const Cancelled&) = default;
};
struct Modified {
    long long id;
    long long old_qty;
    long long new_qty;
    friend bool operator==(const Modified&, const Modified&) = default;
};
struct Rejected {
    long long id;
    std::string_view reason;  // always one of the constants above: static storage, no allocation
    friend bool operator==(const Rejected&, const Rejected&) = default;
};
using Event = std::variant<Trade, Rested, Cancelled, Modified, Rejected>;

namespace detail {
template <class... Ts>
struct overloaded : Ts... {
    using Ts::operator()...;
};
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

/// a + b into `out`; false on overflow (never relies on signed overflow, which is undefined behaviour).
inline bool add_ok(long long a, long long b, long long& out) { return !__builtin_add_overflow(a, b, &out); }
}  // namespace detail
```

* `Command` 和 `Event` 是 **`std::variant`**：一个封闭的类型集合，值要么是 `Limit`，要么是 `Market`……处理它们用 `std::visit`，**漏掉任何一种情况都编译不过**（对比虚函数：新增子类时不会提醒你更新所有 switch）。
* `overloaded` 把几个 lambda 合成一个访问者：

```cpp
// std::variant + std::visit: a closed set of event types and a visitor the compiler checks for completeness.
#include <iostream>
#include <string>
#include <variant>

struct Trade { long long px; long long qty; };
struct Rested { long long px; long long qty; };
struct Cancelled { long long remaining; };
using Event = std::variant<Trade, Rested, Cancelled>;

template <class... Ts>
struct overloaded : Ts... { using Ts::operator()...; };
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

std::string render(const Event& e) {
    return std::visit(overloaded{
                          [](const Trade& t) { return "TRADE " + std::to_string(t.qty) + " @ " + std::to_string(t.px); },
                          [](const Rested& r) { return "REST " + std::to_string(r.qty) + " @ " + std::to_string(r.px); },
                          [](const Cancelled& c) { return "CANCEL " + std::to_string(c.remaining); },
                          // Add a fourth alternative to Event and delete nothing here: this call stops compiling,
                          // because std::visit requires the visitor to accept EVERY alternative.
                      },
                      e);
}

int main() {
    for (const Event& e : {Event{Trade{101, 5}}, Event{Rested{99, 3}}, Event{Cancelled{2}}}) std::cout << render(e) << "\n";
    const Event e = Trade{1, 2};
    if (const auto* t = std::get_if<Trade>(&e)) std::cout << "get_if: trade of " << t->qty << "\n";  // one alternative, no visitor
}
```

## 4. Part 1：维护（不撮合）

```cpp
/// Single-instrument limit order book.  Both sides are std::map<price, PriceLevel> in ascending price order (best bid =
/// the last element, best ask = the first); a level is a std::list of orders in arrival order plus a cached total.  The id
/// index stores iterators straight to the order's list node and its level, so cancel needs no search.
/// std::map and std::list never invalidate iterators on insert/erase of OTHER elements -- that is what makes the stored
/// iterators legal.  They would dangle in a copy, so the book is move-only.
class OrderBook {
public:
    OrderBook() = default;
    OrderBook(const OrderBook&) = delete;
    OrderBook& operator=(const OrderBook&) = delete;
    OrderBook(OrderBook&&) noexcept = default;  // node-based containers keep their nodes (and iterators) when moved
    OrderBook& operator=(OrderBook&&) noexcept = default;
```

```cpp
    /// Rest an order without matching (the book may end up crossed).  Invalid arguments / duplicate id: std::invalid_argument
    /// (checked in the order id, price, quantity, duplicate); level total overflow: std::overflow_error, book unchanged.
    void add(long long id, Side side, long long price, long long qty) {
        if (id <= 0) throw std::invalid_argument(std::string(INVALID_ID));
        if (price <= 0) throw std::invalid_argument(std::string(INVALID_PRICE));
        if (qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        if (by_id_.contains(id)) throw std::invalid_argument(std::string(DUPLICATE_ID));
        if (level_would_overflow(side, price, qty)) throw std::overflow_error("level total overflows");
        rest(id, side, price, qty);
    }

    bool cancel(long long id) {
        const auto it = by_id_.find(id);
        if (it == by_id_.end()) return false;
        unlink(it->second);
        by_id_.erase(it);
        return true;
    }

    /// Only the quantity changes.  Smaller: keeps its place in the queue.  Equal: nothing.  Larger: goes to the back of the
    /// queue (time priority is lost).  new_qty <= 0 -> std::invalid_argument even for an unknown id; unknown id -> false;
    /// level total overflow -> std::overflow_error (book unchanged).
    bool modify(long long id, long long new_qty) {
        if (new_qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        switch (try_modify(id, new_qty)) {
            case ModifyResult::Ok: return true;
            case ModifyResult::Unknown: return false;
            case ModifyResult::Overflow: break;
        }
        throw std::overflow_error("level total overflows");
    }

    std::optional<long long> best_bid() const {
        if (bids_.empty()) return std::nullopt;
        return bids_.rbegin()->first;
    }
    std::optional<long long> best_ask() const {
        if (asks_.empty()) return std::nullopt;
        return asks_.begin()->first;
    }

    /// The best n levels: bids from the highest price down, asks from the lowest up.  n < 0 -> std::invalid_argument.
    std::vector<Level> depth(Side side, int n) const {
        if (n < 0) throw std::invalid_argument("n < 0");
        std::vector<Level> out;
        const auto push = [&](const auto& entry) {
            out.push_back({entry.first, entry.second.total, static_cast<int>(entry.second.fifo.size())});
        };
        if (side == Side::Buy) {
            for (auto it = bids_.rbegin(); it != bids_.rend() && std::cmp_less(out.size(), n); ++it) push(*it);
        } else {
            for (auto it = asks_.begin(); it != asks_.end() && std::cmp_less(out.size(), n); ++it) push(*it);
        }
        return out;
    }

    std::optional<Order> find(long long id) const {
        const auto it = by_id_.find(id);
        if (it == by_id_.end()) return std::nullopt;
        const Locator& loc = it->second;
        return Order{id, loc.side, loc.level->first, loc.node->qty};
    }

    /// Order ids at one price level, front of the queue first (empty if there is no such level).
    std::vector<long long> queue(Side side, long long price) const {
        const Ladder& lad = ladder(side);
        const auto it = lad.find(price);
        std::vector<long long> ids;
        if (it != lad.end())
            for (const Node& n : it->second.fifo) ids.push_back(n.id);
        return ids;
    }

    std::size_t size() const noexcept { return by_id_.size(); }
```

要点：

* **所有会失败的检查都在修改之前**：参数校验、重复 id、价位总量溢出（`__builtin_add_overflow`——**有符号溢出在 C++ 里是 UB**，不能先加后比较）。失败时簿保持原样。唯一还可能抛的是内存耗尽（`bad_alloc`），那不在契约内。
* `modify`：减量只改数量；**增量**检查价位总量不溢出后，用 `lvl.fifo.splice(lvl.fifo.end(), lvl.fifo, node)` 把节点移到队尾——O(1)，`Locator` 里存的迭代器继续有效（见 `try_modify`）。等量什么也不变。`new_qty <= 0` 先报参数错，即使 id 未知。
* `best_bid` 是 `bids_.rbegin()`，`best_ask` 是 `asks_.begin()`：两边都用升序的 `map`，不需要两种比较器、两种迭代器类型，`Locator` 也只要一种。
* `depth` 的 `n` 是 `int`，和 `out.size()`（`size_t`）比较时用 `std::cmp_less`——普通 `<` 会把 `-1` 转成巨大的无符号数（编译器警告，也是真 bug）。

```cpp
private:
    struct Node {
        long long id;
        long long qty;
    };
    using Fifo = std::list<Node>;
    struct PriceLevel {
        Fifo fifo;
        long long total = 0;  // cached sum of the quantities in fifo
    };
    using Ladder = std::map<long long, PriceLevel>;
    struct Locator {
        Side side;
        Ladder::iterator level;
        Fifo::iterator node;
    };
    enum class ModifyResult { Ok, Unknown, Overflow };

    Ladder& ladder(Side s) { return s == Side::Buy ? bids_ : asks_; }
    const Ladder& ladder(Side s) const { return s == Side::Buy ? bids_ : asks_; }

    static long long id_of(const Command& c) {
        return std::visit([](const auto& x) { return x.id; }, c);
    }

    bool level_would_overflow(Side side, long long price, long long qty) const {
        const Ladder& lad = ladder(side);
        const auto it = lad.find(price);
        long long ignored;
        return it != lad.end() && !detail::add_ok(it->second.total, qty, ignored);
    }

    /// Precondition: the id is free and the level total cannot overflow.
    void rest(long long id, Side side, long long price, long long qty) {
        const auto [level, created] = ladder(side).try_emplace(price);
        (void)created;
        PriceLevel& lvl = level->second;
        lvl.fifo.push_back({id, qty});
        lvl.total += qty;
        by_id_.emplace(id, Locator{side, level, std::prev(lvl.fifo.end())});
    }

    /// Remove the order from its queue and level (the caller erases the id index entry).
    void unlink(const Locator& loc) {
        PriceLevel& lvl = loc.level->second;
        lvl.total -= loc.node->qty;
        lvl.fifo.erase(loc.node);
        if (lvl.fifo.empty()) ladder(loc.side).erase(loc.level);
    }

    ModifyResult try_modify(long long id, long long new_qty) {
        const auto it = by_id_.find(id);
        if (it == by_id_.end()) return ModifyResult::Unknown;
        Locator& loc = it->second;
        PriceLevel& lvl = loc.level->second;
        const long long old = loc.node->qty;
        if (new_qty > old) {
            long long total;
            if (!detail::add_ok(lvl.total, new_qty - old, total)) return ModifyResult::Overflow;  // nothing modified yet
            lvl.total = total;
            loc.node->qty = new_qty;
            lvl.fifo.splice(lvl.fifo.end(), lvl.fifo, loc.node);  // to the back; the node (and our iterator) stay valid
        } else {
            lvl.total -= old - new_qty;
            loc.node->qty = new_qty;
        }
        return ModifyResult::Ok;
    }
```

* `rest`：`try_emplace(price)` 找到或创建价位；`push_back` 之后 `std::prev(end())` 就是新节点的迭代器；存进 `by_id_`。
* `unlink`：减总量、从 `list` 里 `erase(node)`、价位空了就 `erase(level)`——**不需要任何查找**，这就是 O(1) 撤单。
* `ModifyResult` 是内部枚举：撮合路径上不用异常做控制流（`modify` 对外再转成异常）。

## 5. Part 2：撮合

规则：

1. 校验顺序：`id → price → quantity → 簿状态`。失败返回**一个** `Rejected`，簿不变。
2. 限价单：只要对手盘最优价「不比我的限价差」（买：`ask <= price`；卖：`bid >= price`）就吃；吃不完的挂簿（`Rested`）。
3. 市价单 = 限价设成无穷（买 `LLONG_MAX`，卖 `0`），复用同一个循环；吃不完的部分**作废**（`Cancelled`，immediate-or-cancel）。
4. **溢出检查在撮合之前**：限价单挂簿后会让自己那一侧同价位的总量溢出 → 整单拒绝，**且不先去吃对手盘**。否则先成交了一半、挂剩余部分时才发现溢出，已经发出去的成交收不回来。

```cpp
    /// Execute one command and return the events it caused, in order.  Failure = one Rejected event and the book is
    /// untouched.  Checks in the order id, price, quantity, book state.
    std::vector<Event> execute(const Command& cmd) {
        if (const auto bad = validate(cmd)) return {Rejected{id_of(cmd), *bad}};
        return std::visit(
            detail::overloaded{
                [&](const Limit& c) -> std::vector<Event> {
                    if (level_would_overflow(c.side, c.price, c.qty)) return {Rejected{c.id, OVERFLOW_REASON}};  // BEFORE matching: all or nothing
                    std::vector<Event> events;
                    const long long left = sweep(c.id, c.side, c.price, c.qty, events);
                    if (left > 0) {
                        rest(c.id, c.side, c.price, left);
                        events.push_back(Rested{c.id, c.side, c.price, left});
                    }
                    return events;
                },
                [&](const Market& c) -> std::vector<Event> {
                    std::vector<Event> events;
                    const long long left = sweep(c.id, c.side, c.side == Side::Buy ? LLONG_MAX : 0, c.qty, events);
                    if (left > 0) events.push_back(Cancelled{c.id, left});  // immediate-or-cancel: the rest is void
                    return events;
                },
                [&](const Cancel& c) -> std::vector<Event> {
                    const auto it = by_id_.find(c.id);
                    const long long left = it->second.node->qty;
                    unlink(it->second);
                    by_id_.erase(it);
                    return {Cancelled{c.id, left}};
                },
                [&](const Modify& c) -> std::vector<Event> {
                    const long long old = by_id_.find(c.id)->second.node->qty;
                    if (try_modify(c.id, c.new_qty) == ModifyResult::Overflow) return {Rejected{c.id, OVERFLOW_REASON}};
                    return {Modified{c.id, old, c.new_qty}};
                },
            },
            cmd);
    }

    std::vector<Event> execute_all(const std::vector<Command>& cmds) {
        std::vector<Event> out;
        for (const Command& c : cmds) {
            std::vector<Event> evs = execute(c);
            out.insert(out.end(), evs.begin(), evs.end());
        }
        return out;
    }
```

* `std::visit(overloaded{...}, cmd)`：四个 lambda 对应四种命令，每个都 `-> std::vector<Event>`。少写一个就编译失败。
* `Cancel` / `Modify` 分支直接用 `by_id_.find(c.id)->...`：`validate` 已经保证 id 存在。

```cpp
    std::optional<std::string_view> validate(const Command& cmd) const {
        using R = std::optional<std::string_view>;
        return std::visit(
            detail::overloaded{
                [&](const Limit& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    if (c.price <= 0) return INVALID_PRICE;
                    if (c.qty <= 0) return INVALID_QTY;
                    return by_id_.contains(c.id) ? R(DUPLICATE_ID) : std::nullopt;
                },
                [&](const Market& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    if (c.qty <= 0) return INVALID_QTY;
                    return by_id_.contains(c.id) ? R(DUPLICATE_ID) : std::nullopt;
                },
                [&](const Cancel& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    return by_id_.contains(c.id) ? std::nullopt : R(UNKNOWN_ID);
                },
                [&](const Modify& c) -> R {
                    if (c.id <= 0) return INVALID_ID;
                    if (c.new_qty <= 0) return INVALID_QTY;
                    return by_id_.contains(c.id) ? std::nullopt : R(UNKNOWN_ID);
                },
            },
            cmd);
    }
```

```cpp
    /// Eat the opposite side while it crosses `limit`; returns the unfilled quantity.  The trade price is the maker's price.
    long long sweep(long long taker_id, Side side, long long limit, long long qty, std::vector<Event>& out) {
        Ladder& opp = ladder(opposite(side));
        long long left = qty;
        while (left > 0 && !opp.empty()) {
            const auto top = side == Side::Buy ? opp.begin() : std::prev(opp.end());  // best opposite level
            const long long px = top->first;
            if (side == Side::Buy ? px > limit : px < limit) break;
            PriceLevel& lvl = top->second;
            Node& maker = lvl.fifo.front();
            const long long fill = std::min(left, maker.qty);
            out.push_back(Trade{taker_id, maker.id, side, px, fill});
            left -= fill;
            maker.qty -= fill;
            lvl.total -= fill;
            if (maker.qty == 0) {
                const long long maker_id = maker.id;
                lvl.fifo.pop_front();
                by_id_.erase(maker_id);
                if (lvl.fifo.empty()) opp.erase(top);
            }
        }
        return left;
    }

    Ladder bids_, asks_;
    std::unordered_map<long long, Locator> by_id_;
};
```

* `sweep` 取最优对手价位：买单看 `opp.begin()`（最低卖价），卖单看 `std::prev(opp.end())`（最高买价）。
* `maker.qty == 0` 时：**先**记下 `maker_id`，`pop_front()`，再 `by_id_.erase(maker_id)`——`maker` 是 `list` 节点里的引用，`pop_front` 之后它就悬空了。价位空了才 `opp.erase(top)`。
* 成交价取 `px`（maker 的价位）。

### 5.1 文本接口

`LIMIT id BUY|SELL price qty`、`MARKET id BUY|SELL qty`、`CANCEL id`、`MODIFY id new_qty`；大小写不敏感，空白任意。

```cpp
namespace detail {
inline bool iequals(std::string_view a, std::string_view b) {
    return std::ranges::equal(a, b, [](unsigned char x, unsigned char y) { return std::toupper(x) == std::toupper(y); });
}
inline bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }
inline std::vector<std::string_view> split_words(std::string_view s) {
    std::vector<std::string_view> words;
    std::size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && is_space(s[i])) ++i;
        const std::size_t start = i;
        while (i < s.size() && !is_space(s[i])) ++i;
        if (i > start) words.push_back(s.substr(start, i - start));
    }
    return words;
}
/// The whole token must be one base-10 integer that fits in long long: from_chars stops at the first bad character
/// ("1.5" -> 1) and reports range errors, so check both.  (std::stoll would accept "12abc" and a leading '+'/space.)
inline long long parse_ll(std::string_view tok) {
    long long v = 0;
    const auto [end, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), v);
    if (ec != std::errc{} || end != tok.data() + tok.size()) throw std::invalid_argument("bad number: " + std::string(tok));
    return v;
}
inline Side parse_side(std::string_view tok) {
    if (iequals(tok, "BUY")) return Side::Buy;
    if (iequals(tok, "SELL")) return Side::Sell;
    throw std::invalid_argument("bad side: " + std::string(tok));
}
inline void need_args(const std::vector<std::string_view>& w, std::size_t n) {
    if (w.size() != n) throw std::invalid_argument(std::string(w[0]) + " expects " + std::to_string(n - 1) + " arguments");
}
}  // namespace detail

/// LIMIT id BUY|SELL price qty | MARKET id BUY|SELL qty | CANCEL id | MODIFY id new_qty  (case-insensitive, any whitespace).
inline Command parse(std::string_view line) {
    const auto w = detail::split_words(line);
    if (w.empty()) throw std::invalid_argument("empty command");
    using detail::iequals;
    using detail::parse_ll;
    if (iequals(w[0], "LIMIT")) {
        detail::need_args(w, 5);
        return Limit{parse_ll(w[1]), detail::parse_side(w[2]), parse_ll(w[3]), parse_ll(w[4])};
    }
    if (iequals(w[0], "MARKET")) {
        detail::need_args(w, 4);
        return Market{parse_ll(w[1]), detail::parse_side(w[2]), parse_ll(w[3])};
    }
    if (iequals(w[0], "CANCEL")) {
        detail::need_args(w, 2);
        return Cancel{parse_ll(w[1])};
    }
    if (iequals(w[0], "MODIFY")) {
        detail::need_args(w, 3);
        return Modify{parse_ll(w[1]), parse_ll(w[2])};
    }
    throw std::invalid_argument("unknown command: " + std::string(w[0]));
}
```

解析整数是这类题的陷阱集中营：

```cpp
// Parsing integers: std::from_chars is the strict one, but you still have to check how much it consumed.
#include <charconv>
#include <cstdlib>
#include <iostream>
#include <string>
#include <string_view>

void show(std::string_view text) {
    long long v = 0;
    const auto [end, ec] = std::from_chars(text.data(), text.data() + text.size(), v);
    const bool whole = ec == std::errc{} && end == text.data() + text.size();
    std::cout << '"' << text << "\"  from_chars: " << (ec == std::errc::result_out_of_range ? "out of range" : ec == std::errc{} ? "ok" : "no digits")
              << ", consumed " << (end - text.data()) << "/" << text.size() << " -> " << (whole ? "ACCEPT" : "reject");
    std::string stoll_result;
    try {
        stoll_result = std::to_string(std::stoll(std::string(text)));
    } catch (const std::exception&) {
        stoll_result = "throws";
    }
    std::cout << "   |   stoll: " << stoll_result << "\n";
}

int main() {
    show("100");
    show("1.5");                    // from_chars stops at '.', so check the end pointer
    show("12abc");                  // stoll happily returns 12
    show("+5");                     // from_chars: no leading '+'; stoll accepts it
    show(" 7");                     // from_chars: no leading space; stoll skips it
    show("99999999999999999999");  // from_chars reports out of range
    show("-0");
}
```

* `std::from_chars` 不跳空白、不认 `+`、不抛异常、不分配；但它遇到非法字符就**停下**，只返回「读到哪里」——必须检查 `end == 末尾`，否则 `"1.5"` 被读成 `1`，`"12abc"` 被读成 `12`。溢出由 `errc::result_out_of_range` 报告。
* `std::stoll` 会接受前导空格、`+`、尾部垃圾（`"12abc"` → 12），而且用异常报错。
* 大小写不敏感比较要先把 `char` 转成 `unsigned char` 再调 `std::toupper`——对负数的 `char`（UTF-8 字节）调用是 UB。
* `render` 用 `std::format`（C++20）。

```cpp
/// One line per event.  std::visit with a visitor that handles every alternative: a new Event type would not compile.
inline std::string render(const Event& e) {
    return std::visit(
        detail::overloaded{
            [](const Trade& t) { return std::format("TRADE taker={} maker={} side={} px={} qty={}", t.taker_id, t.maker_id, name(t.taker_side), t.price, t.qty); },
            [](const Rested& r) { return std::format("REST id={} side={} px={} qty={}", r.id, name(r.side), r.price, r.qty); },
            [](const Cancelled& c) { return std::format("CANCEL id={} remaining={}", c.id, c.remaining); },
            [](const Modified& m) { return std::format("MODIFY id={} old={} new={}", m.id, m.old_qty, m.new_qty); },
            [](const Rejected& r) { return std::format("REJECT id={} reason={}", r.id, r.reason); },
        },
        e);
}

/// Run a script (blank lines and '#' lines are skipped).  A malformed line -> std::invalid_argument("line N: ..."), N from 1.
inline std::vector<std::string> replay(const std::vector<std::string>& lines) {
    OrderBook b;
    std::vector<std::string> out;
    for (std::size_t i = 0; i < lines.size(); ++i) {
        const auto w = detail::split_words(lines[i]);
        if (w.empty() || w[0].front() == '#') continue;
        Command cmd;
        try {
            cmd = parse(lines[i]);
        } catch (const std::invalid_argument& e) {
            throw std::invalid_argument("line " + std::to_string(i + 1) + ": " + e.what());
        }
        for (const Event& ev : b.execute(cmd)) out.push_back(render(ev));
    }
    return out;
}
```

## 6. Part 3：批量撮合

```cpp
struct Summary {
    std::vector<Trade> trades;
    long long filled_qty;
    long long notional;  // sum of price * qty over all trades
    std::vector<Level> bids, asks;
    friend bool operator==(const Summary&, const Summary&) = default;
};

/// rows[i] = {side, price, qty}, side 0 = BUY, 1 = SELL; order id = i + 1; processed as limit orders in order.
/// Every row is validated first (std::invalid_argument "row i: ..."); notional overflow -> std::overflow_error.
inline Summary run_batch(const std::vector<std::vector<long long>>& rows) {
    for (std::size_t i = 0; i < rows.size(); ++i) {
        const auto& r = rows[i];
        const std::string at = "row " + std::to_string(i) + ": ";
        if (r.size() != 3) throw std::invalid_argument(at + "expected [side, price, quantity]");
        if (r[0] != 0 && r[0] != 1) throw std::invalid_argument(at + "bad side");
        if (r[1] <= 0) throw std::invalid_argument(at + std::string(INVALID_PRICE));
        if (r[2] <= 0) throw std::invalid_argument(at + std::string(INVALID_QTY));
    }
    OrderBook b;
    std::vector<Trade> trades;
    for (std::size_t i = 0; i < rows.size(); ++i) {
        const Side side = rows[i][0] == 0 ? Side::Buy : Side::Sell;
        for (const Event& e : b.execute(Limit{static_cast<long long>(i) + 1, side, rows[i][1], rows[i][2]})) {
            if (const auto* t = std::get_if<Trade>(&e)) trades.push_back(*t);
            else if (const auto* rej = std::get_if<Rejected>(&e)) throw std::overflow_error("row " + std::to_string(i) + ": " + std::string(rej->reason));
        }
    }
    long long filled = 0, notional = 0;
    for (const Trade& t : trades) {
        long long value;
        if (__builtin_mul_overflow(t.price, t.qty, &value) || __builtin_add_overflow(notional, value, &notional) ||
            __builtin_add_overflow(filled, t.qty, &filled))
            throw std::overflow_error("notional overflows long long");
    }
    return {std::move(trades), filled, notional, b.depth(Side::Buy, INT_MAX), b.depth(Side::Sell, INT_MAX)};
}
```

* **先整体校验再处理**：半途发现第 9999 行非法时，前面的行已经改了簿；调用者要么拿到完整结果，要么拿到异常，不要半个状态。
* Java 版的 `long[][]` 要检查每行长度是不是 3；C++ 里同样的输入是 `vector<vector<long long>>`，所以也要检查。如果你自己设计接口，用 `struct Row { int side; long long price, qty; }`，行长度错误在类型上就不可能发生。
* 名义金额 = Σ 价格 × 数量。两个 `long long` 相乘很容易超过 9.2e18（`4e9 × 3e9` 就超），`__builtin_mul_overflow` / `__builtin_add_overflow` 遇到溢出就抛异常，而不是静默回绕。

## 7. Part 4：`TickBook`——热路径

面试官：「你的 `OrderBook` 每秒要处理几百万条命令，profile 显示分配器很忙。怎么办？」先量一下问题：

```cpp
// Allocation count: node-based containers allocate per element; preallocated arrays do not allocate at all.
#include <cstdlib>
#include <iostream>
#include <list>
#include <map>
#include <new>
#include <vector>

static std::size_t g_news = 0;
void* operator new(std::size_t n) {
    ++g_news;
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

int main() {
    constexpr int orders = 1000;

    std::size_t before = g_news;
    std::map<long long, std::list<long long>> tree;
    for (int i = 0; i < orders; ++i) tree[1 + i % 50].push_back(i);  // 50 map nodes + 1000 list nodes
    std::cout << "map<price, list<order>>: " << g_news - before << " allocations for " << orders << " orders\n";

    struct Rec { long long id, qty; int prev, next; };
    std::vector<Rec> pool(orders);                                   // one allocation, made up front
    std::vector<int> head(51, -1), tail(51, -1);                     // one record per price level
    before = g_news;
    for (int i = 0; i < orders; ++i) {
        const int p = 1 + i % 50;
        pool[i] = {i, 1, tail[p], -1};
        if (tail[p] >= 0) pool[tail[p]].next = i; else head[p] = i;
        tail[p] = i;
    }
    std::cout << "preallocated arrays    : " << g_news - before << " allocations for " << orders << " orders\n";
}
```

每个订单一个 `list` 节点（外加 `map` 的价位节点、`unordered_map` 的节点、每条命令返回的 `vector<Event>`）：分配次数和命令数成正比，尾延迟被分配器抖动拖累。低延迟系统要的是**稳态零分配**。办法是利用「价格是有界整数」这个事实：

1. **价位 = 数组下标。** 价格是 tick `1..max_ticks-1`，价位不需要树：`levels[side][tick]` 存 `{head, tail, qty}`。
2. **订单放进预分配的池。** `std::vector<Rec>` 在构造函数里一次分配，用 `int` 下标（而不是指针）互相链接成**侵入式双向链表**；空闲记录用 free list 串起来。`Rec` 32 字节，id、qty、价格、前后指针放在一起（AoS：撮合时这些字段一起用）。
3. **最优价被吃光 / 撤光后找下一档**：非空价位位图，一个 `uint64_t` 管 64 个价位，用 `std::countr_zero` / `std::countl_zero` 一条指令定位：

```cpp
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
```

4. **id → 记录** 用开放寻址的整数哈希表（`vector<IdSlot>`），`0` 表示空槽（id 恒 > 0）。删除用**回移删除**（backward shift）：不留墓碑，探测链不会越来越长。
5. **成交走回调**，不创建事件对象。`limit` 是一个**模板**：`Sink` 可以是 lambda、函数对象、函数指针，调用被内联，不像 `std::function` 可能为较大的捕获分配内存。
6. 代价：价格带和同时挂单数是构造时固定的上限，超过就拒绝（`REJECTED` / `FULL`）——这正是低延迟系统的取舍。

```cpp
/// Hot-path order book: prices are integer ticks 1..max_ticks-1, so a price level is an array index, not a tree node.
/// Everything is allocated in the constructor: a pool of order records linked by 32-bit indices (intrusive doubly linked
/// list per level, free list for spare records), one {head, tail, qty} record per tick and side, a bitmap of non-empty
/// levels to find the next best price, and an open-addressing id -> record table with backward-shift deletion.
/// limit()/cancel() never allocate.  Trades go to a callable: no event objects.
class TickBook {
public:
    static constexpr long long NONE = -1;
    static constexpr long long REJECTED = -1;
    static constexpr long long FULL = -2;
    /// 2^22 live orders * 2^40 = 2^62 < 2^63: a level total can never overflow.
    static constexpr long long MAX_QTY = 1LL << 40;

    /// max_ticks >= 2; 1 <= capacity <= 2^22 (maximum number of live orders), else std::invalid_argument.
    TickBook(int max_ticks, int capacity)
        : max_ticks_(check_ticks(max_ticks)), capacity_(check_capacity(capacity)), pool_(static_cast<std::size_t>(capacity)),
          ids_(std::bit_ceil(std::max<std::size_t>(16, static_cast<std::size_t>(capacity) * 2))), bid_best_(0), ask_best_(max_ticks) {
        id_mask_ = ids_.size() - 1;
        for (int i = 0; i < capacity_; ++i) pool_[static_cast<std::size_t>(i)].next = i + 1 < capacity_ ? i + 1 : -1;
        free_head_ = 0;
        for (auto& s : side_) {
            s.levels.assign(static_cast<std::size_t>(max_ticks_), LevelRec{});
            s.bits.assign((static_cast<std::size_t>(max_ticks_) + 63) / 64, 0);
        }
    }

    /// Match against the opposite side (price-time priority, trade price = maker's price), call
    /// `sink(taker_id, maker_id, price, qty)` per trade, rest the remainder.  Returns the rested quantity (0 = fully filled),
    /// REJECTED for an invalid argument (id <= 0, id already live, price outside 1..max_ticks-1, qty outside 1..MAX_QTY), or
    /// FULL when the pool has no free record (nothing is matched in that case).
    template <class Sink>
    long long limit(long long id, Side side, long long price, long long qty, Sink&& sink) {
        // range-check the 64-bit values BEFORE narrowing to int: (1<<32) + 5 would otherwise become price 5
        if (id <= 0 || price <= 0 || price >= max_ticks_ || qty <= 0 || qty > MAX_QTY) return REJECTED;
        if (find_id(id) >= 0) return REJECTED;
        if (free_head_ < 0) return FULL;
        const int p = static_cast<int>(price);
        const bool buy = side == Side::Buy;
        const int me = buy ? 0 : 1, other = 1 - me;
        long long left = qty;
        while (left > 0 && (buy ? ask_best_ <= p : bid_best_ >= p)) {
            const int bp = buy ? ask_best_ : bid_best_;
            const int slot = side_[other].levels[static_cast<std::size_t>(bp)].head;
            Rec& maker = pool_[static_cast<std::size_t>(slot)];
            const long long fill = std::min(left, maker.qty);
            sink(id, maker.id, static_cast<long long>(bp), fill);
            left -= fill;
            maker.qty -= fill;
            side_[other].levels[static_cast<std::size_t>(bp)].qty -= fill;
            if (maker.qty == 0) unlink(slot);
        }
        if (left > 0) rest(id, me, p, left);
        return left;
    }

    /// O(1): the id table gives the record, the record knows its neighbours.
    bool cancel(long long id) {
        const int slot = find_id(id);
        if (slot < 0) return false;
        unlink(slot);
        return true;
    }

    long long best_bid() const noexcept { return bid_best_ == 0 ? NONE : bid_best_; }
    long long best_ask() const noexcept { return ask_best_ == max_ticks_ ? NONE : ask_best_; }
    int live_orders() const noexcept { return live_; }

    /// Total quantity at a price; 0 for a price outside the band (no out-of-bounds read, no truncation).
    long long qty_at(Side side, long long price) const noexcept {
        if (price <= 0 || price >= max_ticks_) return 0;
        return side_[side == Side::Buy ? 0 : 1].levels[static_cast<std::size_t>(price)].qty;
    }
```

要点：

* **先在 64 位上检查范围，再收窄成 `int`。** `price = 2³² + 5` 先 `static_cast<int>` 会变成 5，一个本该被拒绝的价格悄悄变成合法价格（`qty_at` 同理）。
* `MAX_QTY = 2⁴⁰`、容量 ≤ 2²²：价位总量 ≤ 2⁶² < 2⁶³，**从源头消灭溢出**，热路径里就不需要检查。
* `FULL` 时不撮合、不改变簿：先看有没有空闲记录，再动手。
* 池满返回 `FULL` 而不是抛异常：热路径上的失败是常态，用返回值。

```cpp
private:
    struct Rec {  // 32 bytes: id, qty, price, prev, next, side
        long long id = 0;
        long long qty = 0;
        std::int32_t price = 0;
        std::int32_t prev = -1;
        std::int32_t next = -1;  // next in the level's queue; in a free record: next free record
        std::uint8_t side = 0;
    };
    struct LevelRec {
        std::int32_t head = -1, tail = -1;
        long long qty = 0;
    };
    struct SideData {
        std::vector<LevelRec> levels;
        std::vector<std::uint64_t> bits;  // bit p set = level p is not empty
    };
    struct IdSlot {
        long long key = 0;  // 0 = empty (ids are > 0)
        std::int32_t slot = 0;
    };

    static int check_ticks(int t) {
        if (t < 2) throw std::invalid_argument("max_ticks < 2");
        return t;
    }
    static int check_capacity(int c) {
        if (c < 1 || c > (1 << 22)) throw std::invalid_argument("capacity out of range");
        return c;
    }

    void rest(long long id, int s, int p, long long qty) {
        const int slot = free_head_;
        Rec& r = pool_[static_cast<std::size_t>(slot)];
        free_head_ = r.next;
        ++live_;
        r.id = id;
        r.qty = qty;
        r.price = p;
        r.side = static_cast<std::uint8_t>(s);
        LevelRec& lv = side_[s].levels[static_cast<std::size_t>(p)];
        r.prev = lv.tail;
        r.next = -1;
        if (lv.tail >= 0) {
            pool_[static_cast<std::size_t>(lv.tail)].next = slot;
        } else {  // the level was empty
            lv.head = slot;
            side_[s].bits[static_cast<std::size_t>(p) >> 6] |= 1ull << (p & 63);
            if (s == 0) bid_best_ = std::max(bid_best_, p);
            else ask_best_ = std::min(ask_best_, p);
        }
        lv.tail = slot;
        lv.qty += qty;
        put_id(id, slot);
    }

    /// Detach the record from its queue, give it back to the pool, forget its id; if the level became empty, find the next best price.
    void unlink(int slot) {
        Rec& r = pool_[static_cast<std::size_t>(slot)];
        const int s = r.side, p = r.price;
        LevelRec& lv = side_[s].levels[static_cast<std::size_t>(p)];
        if (r.prev >= 0) pool_[static_cast<std::size_t>(r.prev)].next = r.next; else lv.head = r.next;
        if (r.next >= 0) pool_[static_cast<std::size_t>(r.next)].prev = r.prev; else lv.tail = r.prev;
        lv.qty -= r.qty;
        if (lv.head < 0) {
            side_[s].bits[static_cast<std::size_t>(p) >> 6] &= ~(1ull << (p & 63));
            if (s == 0 && p == bid_best_) {
                const int n = p > 0 ? at_or_below(side_[0].bits, p - 1) : -1;
                bid_best_ = n < 0 ? 0 : n;
            } else if (s == 1 && p == ask_best_) {
                const int n = p + 1 < max_ticks_ ? at_or_above(side_[1].bits, p + 1) : -1;
                ask_best_ = n < 0 ? max_ticks_ : n;
            }
        }
        erase_id(r.id);
        r.next = free_head_;
        free_head_ = slot;
        --live_;
    }

    // first non-empty level at or above / below `from`: mask the word, then countr_zero / countl_zero (one instruction each)
    static int at_or_above(const std::vector<std::uint64_t>& b, int from) {
        std::size_t w = static_cast<std::size_t>(from) >> 6;
        std::uint64_t word = b[w] & (~0ull << (from & 63));
        for (;;) {
            if (word != 0) return static_cast<int>(w * 64) + std::countr_zero(word);
            if (++w >= b.size()) return -1;
            word = b[w];
        }
    }
    static int at_or_below(const std::vector<std::uint64_t>& b, int from) {
        std::size_t w = static_cast<std::size_t>(from) >> 6;
        std::uint64_t word = b[w] & (~0ull >> (63 - (from & 63)));
        for (;;) {
            if (word != 0) return static_cast<int>(w * 64) + 63 - std::countl_zero(word);
            if (w == 0) return -1;
            word = b[--w];
        }
    }

    // id table: ids are often consecutive, so multiply by an odd constant and fold the high half into the low half
    std::size_t id_hash(long long id) const noexcept {
        const std::uint64_t h = static_cast<std::uint64_t>(id) * 0x9E3779B97F4A7C15ull;
        return static_cast<std::size_t>(h ^ (h >> 32)) & id_mask_;
    }
    int find_id(long long id) const noexcept {
        for (std::size_t i = id_hash(id); ids_[i].key != 0; i = (i + 1) & id_mask_)
            if (ids_[i].key == id) return ids_[i].slot;
        return -1;
    }
    void put_id(long long id, int slot) noexcept {
        std::size_t i = id_hash(id);
        while (ids_[i].key != 0) i = (i + 1) & id_mask_;
        ids_[i] = {id, slot};
    }
    /// Backward-shift deletion: no tombstones.  Emptying the slot would cut the probe chain of keys pushed past it, so slide
    /// each later key of the cluster back into the hole when its home slot does not lie cyclically in (hole, its position].
    void erase_id(long long id) noexcept {
        std::size_t i = id_hash(id);
        while (ids_[i].key != id) i = (i + 1) & id_mask_;
        std::size_t j = i;
        for (;;) {
            j = (j + 1) & id_mask_;
            if (ids_[j].key == 0) break;
            const std::size_t home = id_hash(ids_[j].key);
            if (((j - home) & id_mask_) >= ((j - i) & id_mask_)) {
                ids_[i] = ids_[j];
                i = j;
            }
        }
        ids_[i].key = 0;
    }

    int max_ticks_;
    int capacity_;
    std::vector<Rec> pool_;
    std::vector<IdSlot> ids_;
    std::size_t id_mask_ = 0;
    std::array<SideData, 2> side_;
    int free_head_ = -1;
    int live_ = 0;
    int bid_best_;  // 0 = no bids
    int ask_best_;  // max_ticks_ = no asks
};
```

回移删除（`erase_id`）：删掉位置 `i` 的 key 之后，往后看同一簇里的每个 key `j`：只有当它的家**不在**环形区间 `(洞, j]` 里时，才能搬进洞（搬过去之后它仍然在「家 → 实际位置」的探测路径上）。例（容量 8）：a、b 的家都是 2，c 的家是 3，依次插入后：

```
slot:   2   3   4   5
key:    a   b   c   .

删除 a，洞在 2：
  b 在 3，家 2，不在 (2,3] 里 → b 搬进洞，洞移到 3
  c 在 4，家 3，不在 (3,4] 里 → c 搬进洞，洞移到 4
  slot 5 是空格 → 结束，把洞（4）置空
结果:   b   c   .

如果 c 的家就是 4（本来就在家里）：家 4 在 (3,4] 里 → 不能搬，否则 c 会跑到家的前面，从 4 出发永远找不到它。
```

（直接把 slot 2 置空，`b` 和 `c` 就都查不到了。）

## 8. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| 有序 Map | `TreeMap`（`SequencedMap`，`firstEntry`） | `std::map`，`begin()` / `rbegin()` |
| 队列 | `LinkedHashMap<id, Node>`（哈希 + 链表） | `std::list` + `unordered_map` 里存迭代器；`splice` 移到队尾 |
| 命令 / 事件 | `sealed interface` + `record`，`switch` 模式匹配 | `std::variant` + `std::visit(overloaded{…})` |
| 溢出 | `Math.addExact` | `__builtin_add_overflow` / `__builtin_mul_overflow` |
| 失败原因 | `String` | `std::string_view` 常量（静态存储） |
| 解析 | `Long.parseLong`（抛 `NumberFormatException`） | `std::from_chars` + 检查是否读完 |
| 对象拷贝 | 引用语义，没有这个问题 | 含迭代器的类**不能拷贝**；移动是安全的（节点不动） |
| 成交回调 | `TradeSink` 接口 | 模板参数，任何可调用对象，内联 |
| 位扫描 | `Long.numberOfTrailingZeros` | `std::countr_zero`（`<bit>`） |
| 零分配 | `ThreadMXBean` 测分配字节 | 重载 `operator new` 数次数；预分配 `vector` |
| 收窄 | 类型不允许隐式收窄 | `long long → int` 是静默的，先检查范围 |

## 9. 陷阱

1. `add` 去撮合了（Part 1 只挂不撮）。
2. 成交价取了 taker 的限价；部分成交的 maker 被丢到队尾。
3. 增量 modify 不丢优先级 / 减量反而丢了；`modify(未知 id, 0)` 该先报参数错。
4. 价位空了没从 `map` 删，`best_bid` 返回一个空价位。
5. 总量溢出：`total += qty` 先加后查（UB）；先改后查导致簿被改了一半。
6. 限价单的溢出检查放在撮合之后：成交已经发出，却报 overflow。
7. 保存的迭代器：**拷贝** `OrderBook`；用 `vector` 保存订单再保存迭代器 / 引用。
8. `pop_front()` 之后继续用 `maker` 引用。
9. `std::stoll` 解析（接受 `"12abc"`）；`toupper` 传负数。
10. `size_t` 和 `int` 比较（`n < 0` 转成巨大无符号数）。
11. `long long` 价格直接 `static_cast<int>`。
12. `TickBook`：回移删除写成直接置空；最优价被吃光后没更新（要跨过上万个空价位）；池满时仍然撮合。
13. `std::function` 作为热路径回调：较大的捕获会分配。

## 10. 面试官会追问什么（senior）

**Q1. 撤单怎么做到 O(1)？** `id → {价位迭代器, 订单节点迭代器}`；节点式容器的迭代器不会因别的元素的增删而失效；`list::erase(iterator)` 是 O(1)。

**Q2. 同价位怎么保证先来先成交？** 价位里是按到达顺序的 `list`，队头先成交；增量 modify 视为重新排队（`splice` 到队尾）。

**Q3. 为什么价格用整数不用 `double`？** `0.1 + 0.2 != 0.3`；价格要比较相等、当 map 的 key；浮点数做 key 会出现「看起来一样却是两个价位」。交易所本来就以 tick 报价。

**Q4. `map` 还是数组（按 tick 下标）？** 价格带有界且不太稀疏时数组：O(1)，没有分配，缓存友好；价格范围很大或很稀疏时用 `map`（或 B 树 / 跳表）。数组的最优价靠位图找；位图扫描最坏 `max_ticks / 64` 个字。

**Q5. 怎么证明新版本和旧版本行为一致？** 对拍（differential testing）：同一串随机命令喂给两个实现，逐步比较成交序列、最优价、每档数量；再加一个「显然正确的暴力模型」作为裁判。

**Q6. 多线程怎么办？** 撮合引擎通常**单线程**（确定性、无锁、延迟可预测）；按品种分片（一个品种一个线程）；线程间用单生产者单消费者的环形队列传命令和事件。

**Q7. 异常安全？** 所有会失败的检查放在修改之前（强保证）；`bad_alloc` 之后的一致性要靠先分配后提交，或者在热路径上完全不分配（`TickBook`）。

**Q8. `std::unordered_map` 的 `find` 返回的迭代器，`rehash` 之后还有效吗？** 迭代器失效（rehash 之后），但**指向元素的引用和指针仍然有效**。本题只在 `by_id_` 里存「值」（`Locator`），查完立即使用，不长期保存 `by_id_` 自己的迭代器。

## 11. 自测

1. 为什么 `std::map` 的迭代器可以存进 `by_id_`，而 `std::vector` 的不行？
2. 拷贝一个 `OrderBook` 会发生什么？为什么删除拷贝构造函数而保留移动构造函数是安全的？
3. 增量 `modify` 为什么要用 `splice` 而不是「删除再插入」？
4. 限价单为什么要在撮合**之前**检查自己那一侧价位的溢出？
5. `std::from_chars("1.5")` 返回成功，为什么还要检查 `end`？
6. `TickBook::limit` 里为什么先检查 `price >= max_ticks_` 再 `static_cast<int>`？
7. 回移删除比墓碑好在哪里？

<details><summary>答案</summary>

1. `map` / `list` 是节点式容器：插入、删除别的元素不会移动已有节点，迭代器一直指向同一个节点；`vector` 增长时会把所有元素搬到新内存，迭代器、引用全部悬空。
2. 拷贝出来的 `by_id_` 里的迭代器仍然指向**原对象**的节点；原对象销毁后全部悬空，对拷贝撤单会改坏别人的数据。移动是安全的：节点式容器移动时节点不动，迭代器随节点转到新对象里（被移走的对象为空）。
3. 「删除再插入」要两次分配 / 释放，并让旧迭代器失效（`Locator` 要重新写）；`splice` 只改指针，O(1)，节点和迭代器保持不变。
4. 因为撮合会产生成交事件，而成交已经发生就收不回来。先吃了对手盘、再发现自己挂不上簿，会得到「成交了一半却报溢出」的非原子结果；先检查，要么整单拒绝，要么整单完成。
5. `from_chars` 读到第一个不属于数字的字符就停下，把读到的部分当作成功（`"1.5"` → 1，`end` 指向 `.`）；只有 `end == 末尾` 才说明整个 token 是一个整数。
6. `static_cast<int>(2³² + 5)` 是 5：一个本该被拒绝的价格会变成合法价格。所有范围检查在 64 位上做，通过之后再收窄。
7. 墓碑会占用探测链，需要定期 rehash 清理，装载因子要把墓碑算进去；回移删除在删除时把后面的元素搬回来，不留墓碑，探测链不会越来越长，代价是删除代码更复杂。

</details>
