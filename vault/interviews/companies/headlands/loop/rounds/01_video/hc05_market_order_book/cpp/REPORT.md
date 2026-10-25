# hc05 · 思路与追问（C++20 版）

订单簿不难，面试官看的是三件事：数据结构选得对不对（有序 map + 带序队列 + id 索引）、规则说得清不清楚（价格-时间优先、成交价取谁的、减量保优先级）、一路追问下去你还稳不稳（性能、溢出、测试、迭代器）。下面按 Part 写清怎么写、面试官在探什么、该说出口的话。详细推导和可运行的示例在讲义 [[hc05_market_order_book_cpp]]。

## 30 秒版本

- **结构**：买卖各一个 `std::map<价格, 价位>`；价位 = `std::list<订单>`（到达顺序）加缓存的总量；`unordered_map<id, Locator>` 里存**迭代器**（价位迭代器 + 订单迭代器），撤单不用搜索。
- **为什么迭代器合法**：`map` / `list` 是节点式容器，增删别的元素不会让已有迭代器失效。代价：迭代器指向自己的节点，所以簿**不能拷贝**，只能移动。
- **撮合**：循环取对面最优档的队头，成交 `min(剩余, maker 量)`，成交价取 maker 价；maker 吃光就从 `list` 和 id 表里删，价位空了连价位一起从 `map` 删。
- **原子性**：所有会失败的检查（含溢出）放在修改和成交**之前**；溢出用 `__builtin_add_overflow`，不能加完再看。
- **增量改量**：用 `list::splice` 把节点挪到队尾，节点和迭代器都不变。
- **热路径**：价格是有界整数 tick → 价位用数组下标；订单池 + 侵入式链表 + free list；id 表开放寻址；最优价靠位图；成交走模板回调。构造时一次分配完，之后零分配。

## Part 1 · 维护（不撮合）

**写法**

```cpp
struct Locator { Side side; Ladder::iterator level; Fifo::iterator node; };
std::map<long long, PriceLevel> bids_, asks_;       // PriceLevel { std::list<Node> fifo; long long total; }
std::unordered_map<long long, Locator> by_id_;
```

`add` 按 `id → price → qty → 重复 id → 溢出` 的顺序检查，全部通过之后才 `try_emplace` 价位、`push_back` 到队尾、记下 `Locator`。`cancel`：查 `by_id_`，从价位里 `erase` 节点，扣掉总量，价位空了就从 `map` 里删。`best_ask` 是 `asks_.begin()`，`best_bid` 是 `bids_.rbegin()`，都是 O(log L)（L 是价位数）。

**面试官在探什么**

1. **撤单怎么做到 O(1)**：id 表直接给出订单节点和价位的迭代器，`list::erase(iterator)` 是 O(1)；只有价位变空才有一次 `map::erase`，O(log L)。
2. **为什么能存迭代器**：节点式容器增删别的元素不会让它们失效；`vector` 增长会搬走所有元素，迭代器和引用全部悬空。
3. **拷贝一个簿会怎样**：拷贝出来的 id 表里的迭代器还指向**原对象**的节点，原对象销毁后全部悬空，对拷贝撤单会改坏别人的数据。所以拷贝构造 `= delete`，保留 `noexcept` 的移动：节点式容器移动时节点不动，迭代器跟着节点进了新对象。
4. **增量改量为什么 `splice` 而不是删了再插**：删除再插入要一次释放加一次分配，还会让 `Locator` 里的迭代器失效；`splice` 只改指针，O(1)，节点和迭代器都不变。减量原地改数量和总量，不动位置。
5. **溢出**：先判断 `total + qty` 会不会超过 `LLONG_MAX`（`__builtin_add_overflow`），会就抛 `overflow_error`，此时还什么都没改，簿保持原样。`total += qty` 加完再看是有符号溢出，UB。
6. **参数检查的顺序**：`id → price → qty → 重复 id`；`modify` 先看 `new_qty <= 0`，再看 id 存不存在。
7. **`depth(side, n)` 里 `n` 的类型**：`out.size()` 是无符号、`n` 是 `int`，直接比较时负数会变成巨大的无符号数；先检查 `n < 0`，比较用 `std::cmp_less`。
8. **为什么价格是整数**：`0.1 + 0.2 != 0.3`，浮点数做 `map` 的 key 会出现看起来一样却分进两个价位；交易所本来就以 tick 报价。

**该说出口的话**：「按价格排序的 map 加按到达顺序的 list，id 表里存迭代器，所以撤单是 O(1)；节点式容器不会因别的元素增删而失效，所以迭代器是安全的，代价是簿只能移动、不能拷贝。」

## Part 2 · 撮合 + 事件

**写法**：`Command` 和 `Event` 都是 `std::variant`，`execute` 用 `std::visit` 加 `overloaded{...}`，漏一种命令就编译不过。先 `validate`（只读，返回失败原因或空），失败就返回单个 `Rejected`；通过之后：

```cpp
while (left > 0 && !opp.empty()) {
    auto top = (side == Buy) ? opp.begin() : std::prev(opp.end());   // 对面最优档
    if (side == Buy ? top->first > limit : top->first < limit) break;
    Node& maker = top->second.fifo.front();
    long long fill = std::min(left, maker.qty);
    out.push_back(Trade{taker, maker.id, side, top->first, fill});   // 成交价 = maker 价
    ...                                                              // 扣量；maker 吃光就 pop_front 并删 id、空价位删档
}
```

限价单：先查自己那一侧价位会不会溢出，再扫单，剩余的挂簿并发 `Rested`。市价单：限价设成 `LLONG_MAX`（买）或 0（卖），复用同一个循环；有剩余发 `Cancelled`。

**面试官在探什么**

1. **成交价取谁的**：被动方（簿上那张）的价。卖 90 的单撞上买 100 的单，成交价是 100，对主动方有利，这是规则不是 bug。
2. **同价位谁先成交**：队头（`list` 的 `front`）；部分成交的 maker 留在队头，只是量变小。
3. **溢出检查为什么在撮合之前**：成交事件发出去就收不回来。先吃了对手盘，再发现自己挂不上簿，会得到「成交了一半却报溢出」的非原子结果。所以先检查，要么整单拒绝，要么整单完成。
4. **悬空引用**：`lvl.fifo.pop_front()` 之后不能再用 `maker` 引用；先把 `maker.id` 拷出来，再 pop，再从 id 表里删。
5. **`Rejected.reason` 为什么是 `string_view`**：它总是指向那几个 `inline constexpr` 常量，在静态存储里，不分配，簿销毁以后事件也还能渲染。
6. **严格解析**：`std::stoll("5x")` 返回 5，不报错；`strtoll` 接受 `+` 和十六进制。用 `std::from_chars`，同时检查 `ec` 和 `end == 末尾`：`"1.5"` 会成功读出 1 然后停在 `.`，超范围由 `ec` 报告。
7. **`toupper` 的陷阱**：`char` 可能是有符号的，传负值给 `toupper` 是 UB；比较大小写不敏感命令名时先转成 `unsigned char`。
8. **怎么证明实现对了**：手算样例 + 不变量（不交叉；提交量 = 2 × 成交量 + 簿上剩余 + 作废量）+ 对拍（同一串随机命令喂给快实现和一个线性扫描的暴力模型，逐事件比较）。id 取得很少，让重复、未知、复用频繁出现。
9. **异常安全**：先检查后修改，失败时簿没动，这是强保证；热路径上完全不分配（Part 4）才能连 `bad_alloc` 也排除。

**该说出口的话**：「先校验，再检查溢出，最后才扫单，所以失败的命令什么都不改；成交价取 maker 价，同价按队头先后；事件用 `variant`，漏处理编译就报错。」

## Part 3 · 批量撮合

**写法**：先遍历所有行校验（长度、`side`、`price`、`qty`，消息带 `row i`），再按行序生成 `Limit{i + 1, side, price, qty}` 调 `execute`，从事件里挑出 `Trade`（`std::get_if`）；某一行被 `Rejected`（溢出）就抛 `overflow_error`。名义金额：每笔用 `__builtin_mul_overflow(price, qty)`，累加用 `__builtin_add_overflow`，成交总量同理。最后 `depth(Buy, INT_MAX)` 和 `depth(Sell, INT_MAX)` 取全部档位。

**面试官在探什么**

1. **为什么先整体校验再处理**：校验失败时不能留下处理了一半的结果，也不要让第 1000 行的错误在第 1 行就产生副作用。
2. **名义金额溢出**：`4e9 × 3e9 = 1.2e19`，超过 `LLONG_MAX`（约 9.22e18）；两笔各 9e18 的累加也会溢出。要用带溢出检查的乘法和加法，不能乘完再看。
3. **复用 Part 2**：批量撮合不要另写一套撮合；同一份规则只实现一次。

**该说出口的话**：「批量撮合就是把每一行当限价单交给 `execute`，金额用 builtin 乘法和加法，溢出就抛异常，不返回回绕后的数。」

## Part 4 · `TickBook`

**写法**

| 部件 | 做法 | 为什么 |
|---|---|---|
| 价位 | 每侧一个 `{head, tail, qty}` 数组，下标 = tick | 价格有界，O(1) 取价位，没有 `map` 节点 |
| 订单 | 预分配的记录池，用 `int` 下标串成每个价位的双向链表，另有 free list | 撤单只改前后两个下标，O(1)；不分配 |
| id 表 | 开放寻址，容量取不小于 2 × `capacity` 的 2 的幂；乘一个奇常数再折叠高位做哈希；回移删除 | id 常常连续，直接取模会聚簇；回移删除不留墓碑 |
| 最优价 | 位图（每价位 1 位）+ `std::countr_zero` / `std::countl_zero` | 价位空了就在位图里找下一个非空价位，每字一条指令 |
| 成交 | 模板参数 `Sink&&`，直接调用 `sink(taker, maker, price, qty)` | 不建事件对象，可以内联 |

`limit` 先在 **64 位**上检查所有参数，再转成 `int` 下标；池满（free list 为空）立刻返回 `FULL`，此时还没撮合。

**面试官在探什么**

1. **为什么 `std::map` + `std::list` 慢**：每个挂单至少两次分配（`list` 节点、`unordered_map` 节点），节点散落在堆上，遍历是指针追逐，缓存不友好。数组和链表下标让订单记录紧凑，不分配。
2. **先检查再收窄**：`static_cast<int>((1LL << 32) + 5)` 是 5，一个本该被拒绝的价格会变成合法价格，还会读到别人的价位。范围检查在 64 位上做，通过之后再收窄；`qty_at` 同理。
3. **回移删除 vs 墓碑**：直接把槽置空会截断后面键的探测链，之后查找失败；墓碑能解决，但会堆积，需要定期 rehash，装载因子要把墓碑算进去。回移删除删除时把后面的键搬回来，探测链不会越来越长，代价是删除代码更复杂。
4. **`MAX_QTY = 2^40`**：2^22 张 × 2^40 = 2^62 < 2^63，价位总量从源头不可能溢出，热路径上就不用溢出检查。
5. **位图扫描的最坏代价**：最优价被吃光后要找下一个非空价位，最坏扫 `max_ticks / 64` 个字（`max_ticks = 100000` 时是 1563 个字）。要做到更快可以再加一层汇总位图。
6. **`std::function` 作回调**：捕获较大时会堆分配，违背零分配。模板参数 `Sink&&` 接受 lambda、函数对象、函数指针，没有类型擦除。
7. **证明零分配**：测试重载全局 `operator new` 计数：预热之后 100 万次操作次数必须是 0；同样的操作在 `OrderBook` 上每个挂单至少一次。
8. **价格范围很大怎么办**：数组只覆盖中间价附近的一段，远处价位放一棵 `map`；价位很稀疏时用有序数组加二分。
9. **多线程**：撮合引擎通常单线程（确定性、无锁、延迟可预测）；按品种分片；线程之间用单生产者单消费者的环形队列传命令和事件。不要给每个方法加锁。

**该说出口的话**：「价格是有界整数，价位就是数组下标；订单放预分配的池里用下标串成链，id 表开放寻址，最优价靠位图加 `countr_zero`；构造时一次分配完，之后每个操作都不分配。」

## C++ 专属坑速查

- 存迭代器的簿被拷贝：迭代器指向原对象；`= delete` 拷贝，保留 `noexcept` 移动。
- `pop_front()` 之后继续用 `maker` 引用。
- `total += qty` 先加后查（有符号溢出 UB）；用 `__builtin_add_overflow` 先判断。
- `std::stoll` / `strtoll` 解析不严格；`from_chars` 要检查消费到末尾。
- `toupper` / `tolower` 传负的 `char`；先转 `unsigned char`。
- `size_t` 和 `int` 比较，负数变成巨大无符号数；用 `std::cmp_less` 或先判负。
- `long long` 价格直接 `static_cast<int>`。
- 热路径上用 `std::function` 作回调。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 有序价位 | `TreeMap`（红黑树） | `std::map`（红黑树）；热路径用数组 + 位图 |
| 价位内队列 | `LinkedHashMap<id, Node>`，O(1) 摘除 | `std::list` + id 表存迭代器；`splice` 挪到队尾 |
| 命令 / 事件 | `sealed interface` + record + 模式匹配 `switch` | `std::variant` + `std::visit` + `overloaded` |
| 整数溢出 | `Math.addExact` 抛异常；回绕有定义 | 有符号溢出是 UB，用 `__builtin_add_overflow` |
| 失败原因 | 字符串 | `string_view` 指向静态常量，不分配 |
| 拷贝簿 | 引用语义，没有这个问题 | 存着迭代器，拷贝会悬空，所以只能移动 |
| 热路径分配 | 靠 JIT/GC 调优；数组代替对象图 | 预分配池 + 零分配，可以用重载 `operator new` 在测试里计数验证 |
| 回调 | `TradeSink` 接口 | 模板参数 `Sink&&`，不用 `std::function` |
| 解析整数 | `Long.parseLong` | `std::from_chars` + 检查消费完整 |
