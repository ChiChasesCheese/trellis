# hc05 · 解法与原理

订单簿题的核心是选对数据结构：价位要有序（取最优价），同价位要保持先后顺序，撤单要能按 id 直接找到。选对之后，撮合只是一个两层循环。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep two sorted maps from price to a FIFO queue, one for bids and one for asks, plus a hash map from order id to its location for cancels. Before I start: are prices integer ticks, are ids unique, and should `add` match or just rest?"

面试官通常会说：价格是整数 tick，id 唯一，`add` 只挂单不撮合，撮合是下一步。

## Part 1 · 订单簿

**思路**：买盘和卖盘各一个有序 map，键是价格，值是该价位的先进先出队列。再加一个 `id → 位置（方向、价格）` 的哈希表，撤单时直接定位。

**原理：为什么这样选**

- 取最优价要有序结构：红黑树（`TreeMap` / `std::map`）取最小或最大键是 O(log n)。买盘要最高价，所以买盘的 map 用反向比较（Java `Comparator.reverseOrder()`，C++ `std::greater`），这样两边的最优价都在 `firstKey()` / `begin()`。
- 同价位要 FIFO，撤单又不能是 O(队长)：Java 用 `LinkedHashMap<id, 剩余量>`，保持插入顺序且按 id 删除是 O(1)；C++ 用 `std::list`，哈希表里存它的迭代器，删除一个元素不会让其他迭代器失效。
- 价位空了必须删。否则 `bestBid` 会返回一个没有任何订单的价位。

**Java**

```java
private final TreeMap<Long, LinkedHashMap<Long, Long>> bids = new TreeMap<>(Comparator.reverseOrder());
private final TreeMap<Long, LinkedHashMap<Long, Long>> asks = new TreeMap<>();
private final Map<Long, Loc> index = new HashMap<>();   // record Loc(Side side, long price)

public void add(long id, Side side, long price, long qty) {
    check(id, price, qty);
    book(side).computeIfAbsent(price, p -> new LinkedHashMap<>()).put(id, qty);
    index.put(id, new Loc(side, price));
}

public boolean cancel(long id) {
    Loc loc = index.remove(id);
    if (loc == null) return false;
    TreeMap<Long, LinkedHashMap<Long, Long>> b = book(loc.side());
    LinkedHashMap<Long, Long> level = b.get(loc.price());
    level.remove(id);
    if (level.isEmpty()) b.remove(loc.price());
    return true;
}

public OptionalLong bestBid() { return bids.isEmpty() ? OptionalLong.empty() : OptionalLong.of(bids.firstKey()); }
```

`check` 检查 `price <= 0 || qty <= 0` 和 id 重复，抛 `IllegalArgumentException`；`book(side)` 返回对应方向的 map；`bestAsk` 和 `size()`（`index.size()`）同理。

**C++**

```cpp
using Level = std::list<Resting>;                    // struct Resting { long long id, qty; }
struct Loc { Side side; long long price; Level::iterator pos; };
std::map<long long, Level, std::greater<>> bids_;
std::map<long long, Level> asks_;
std::unordered_map<long long, Loc> index_;

void add(long long id, Side side, long long price, long long qty) {
    check(id, price, qty);
    Level& level = side == Side::Buy ? bids_[price] : asks_[price];
    level.push_back({id, qty});
    index_[id] = {side, price, std::prev(level.end())};
}

bool cancel(long long id) {
    auto it = index_.find(id);
    if (it == index_.end()) return false;
    const Loc loc = it->second;
    index_.erase(it);
    if (loc.side == Side::Buy) erase(bids_, loc); else erase(asks_, loc);
    return true;
}

std::optional<long long> best_bid() const { return bids_.empty() ? std::nullopt : std::optional(bids_.begin()->first); }
```

`erase` 找到价位、删掉这个迭代器指向的元素，价位空了就连价位一起删。

复杂度：`add` O(log P)（P 是价位数），`cancel` O(log P)（要在 map 里找价位），`bestBid` / `bestAsk` O(1) 到 O(log P)。

## Part 2 · 限价撮合

**思路**：新单先检查参数，然后当对手盘最好价位和新单的限价交叉时一直吃：在最好价位里从队头开始，每次取 `min(剩余量, 被动单剩余量)` 成交；被动单吃完就删，价位吃空也删。吃不动了（不交叉，或者对手盘空了），剩余量按 Part 1 的 `add` 挂簿。

**原理**

- 价格优先来自有序 map 的顺序，时间优先来自 FIFO 队列，两者合起来就是价格-时间优先（price-time priority）。
- 成交价取被动方的价：被动单先挂出来，它承诺了「这个价我愿意成交」，新单给的只是上限（买）或下限（卖）。所以买 105 的单碰到卖 101 的单，按 101 成交，新单还得到了价格改善。
- 参数检查（包括 id 重复）必须在第一笔成交之前，否则抛异常时簿已经被改了一半。
- 吃完一张被动单时要同时从 `index` 里删掉，否则以后它还能被 `cancel` 找到，簿里却已经没有这张单。

**Java**

```java
public List<Trade> match(long id, Side side, long price, long qty) {
    check(id, price, qty);
    TreeMap<Long, LinkedHashMap<Long, Long>> opposite = book(side == Side.BUY ? Side.SELL : Side.BUY);
    List<Trade> trades = new ArrayList<>();
    while (qty > 0 && !opposite.isEmpty()) {
        Map.Entry<Long, LinkedHashMap<Long, Long>> best = opposite.firstEntry();
        long levelPrice = best.getKey();
        if (side == Side.BUY ? levelPrice > price : levelPrice < price) break;
        Iterator<Map.Entry<Long, Long>> queue = best.getValue().entrySet().iterator();
        while (qty > 0 && queue.hasNext()) {
            Map.Entry<Long, Long> maker = queue.next();
            long fill = Math.min(qty, maker.getValue());
            trades.add(new Trade(id, maker.getKey(), levelPrice, fill));
            qty -= fill;
            if (fill == maker.getValue()) { queue.remove(); index.remove(maker.getKey()); }
            else maker.setValue(maker.getValue() - fill);
        }
        if (best.getValue().isEmpty()) opposite.pollFirstEntry();
    }
    if (qty > 0) add(id, side, price, qty);
    return trades;
}
```

**C++**

```cpp
std::vector<Trade> match(long long id, Side side, long long price, long long qty) {
    check(id, price, qty);
    std::vector<Trade> trades;
    if (side == Side::Buy) take(asks_, id, qty, trades, [&](long long p) { return p <= price; });
    else take(bids_, id, qty, trades, [&](long long p) { return p >= price; });
    if (qty > 0) add(id, side, price, qty);
    return trades;
}

template <class Book, class Crosses>
void take(Book& opposite, long long id, long long& qty, std::vector<Trade>& trades, Crosses crosses) {
    while (qty > 0 && !opposite.empty() && crosses(opposite.begin()->first)) {
        auto level = opposite.begin();
        Level& queue = level->second;
        while (qty > 0 && !queue.empty()) {
            Resting& maker = queue.front();
            const long long fill = std::min(qty, maker.qty);
            trades.push_back({id, maker.id, level->first, fill});
            qty -= fill;
            maker.qty -= fill;
            if (maker.qty == 0) { index_.erase(maker.id); queue.pop_front(); }
        }
        if (queue.empty()) opposite.erase(level);
    }
}
```

买盘和卖盘的 map 类型不同（比较器不同），所以 `take` 是模板；「是否交叉」用一个 lambda 传进去。

复杂度：设吃掉了 m 张被动单、t 个价位，时间 O(m + t log P)，每个价位的删除是 O(log P)，每张被动单的删除是哈希表 O(1)。

## Part 3 · 口头追问和回答

**1. 每个操作的复杂度？**

见上：挂单和撤单是 O(log P)，最优价 O(1) 到 O(log P)，撮合是每个吃到的价位 O(log P) 加每张吃到的单 O(1)。撤单之所以不是 O(队长)，是因为 Java 的 `LinkedHashMap` 和 C++ 的 list 迭代器都支持按身份直接删除。如果这里用 `ArrayList` / `std::vector`，撤单要线性查找并移动元素。

**2. 价格范围小而且密集怎么办？**

价格是整数 tick，而且活跃价位集中在最优价附近时，可以用数组按「价格 − 基准价」直接寻址，每个价位一个队列，再记一个「最优价位」下标。挂单和撤单变成 O(1)，找新的最优价时从旧位置向外扫描，多数情况下只走几步。代价是要预先知道价格范围，价格飘出范围时要重新定位。

**3. 热路径零分配？**

Java 的 `TreeMap<Long, …>` 每次都会把 `long` 装箱，每个节点也是一次 new；改成基本类型数组（`long[]`）和预先分配好的订单池（用数组下标代替引用，空闲槽位串成链表）。C++ 同理：`std::list` 每次 `push_back` 都是一次 malloc，可以换成预分配的订单池加侵入式链表（订单自己记 prev / next 下标）。成交结果也不返回新容器，而是写进调用者传入的缓冲区。

**4. 延迟瓶颈在哪里，怎么测？**

热路径上主要是缓存未命中（红黑树和链表的节点分散在堆上）、内存分配、以及哈希表查找。应该先测再改：用有代表性的订单流回放，记录每次调用的耗时分布，看 p99 和 p99.9，而不是平均值。平均值掩盖掉了偶发的分配或 GC 停顿。

**5. 加市价单、改量、止损单要改哪里？**

- 市价单：撮合循环去掉价格交叉判断，吃到对手盘空为止，剩余作废，不挂簿。
- 改量：减量可以原地改，保持队列位置；增量按交易所规则通常要丢掉时间优先，等于撤单后重新挂到队尾。
- 止损单：单独一个按触发价排序的结构，成交价穿过触发价时把它转成市价单或限价单，再走撮合。

**6. 多线程怎么用？**

撮合的结果依赖订单到达顺序，所以一个品种的订单簿通常由一个线程独占，其他线程通过队列把订单送进来，这样不需要锁，顺序也是确定的。要横向扩展就按品种分片，每个品种一个线程。

## 常见错误

1. 价位空了不删：`bestBid` 指向一个没有订单的价位，撮合时拿到空队列。
2. 成交价用了新单的限价：应该用被动单的价。
3. 买盘用升序的 map：`firstKey()` 得到的是最低买价，不是最高买价。
4. 被动单吃完后没有从 id 索引里删：之后 `cancel` 返回 true，簿里却没有这张单。
5. 先成交、后检查 id 重复：抛异常时簿已经被改了。
6. 吃不完的部分直接丢掉：限价单的剩余量要挂簿（市价单才作废）。
