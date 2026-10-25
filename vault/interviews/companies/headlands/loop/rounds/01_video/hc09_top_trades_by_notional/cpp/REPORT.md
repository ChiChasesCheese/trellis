# hc09 · 思路与追问（C++20 版）

这是 top-k 的标准题：Part 1 十分钟能写完，分数在追问里，包括 tie-break 写没写全、`price * volume` 会不会溢出、堆为什么改不了中间的元素、多核结果为什么一致。C++ 版再加一层：输入是借来的 `string_view`，结果必须自己拥有字符串；`set` 里存视图时，删除的先后顺序决定会不会悬空。下面按 Part 写怎么写、面试官在探什么、该说出口的话。详细推导和可运行的示例在讲义 [[hc09_top_trades_by_notional_cpp]]。

## 30 秒版本

- **Part 1**：大小为 k 的堆，堆顶是保留集合里最差的事件；堆满后先用一次 `long long` 比较快速拒绝；比较器是全序（notional 降序、ticker 升序、index 升序）。
- **溢出**：每个事件都用 `__builtin_mul_overflow` 检查，包括进不了 top-k 的；不要 `reserve(k)`，`k` 可以是 `INT_MAX`。
- **Part 2**：哈希表聚合 O(n)，再对 m 个 ticker 取堆 O(m log k)；`find` 用 `string_view`，命中时不造临时字符串。
- **Part 3**：`deque` 管过期，`unordered_map` 管总额，`set` 管排名；改键用 `extract` + `insert(node)`，不要「先插后删」。
- **Part 4**：每块一张私有表，最后合并；整数加法的结合律保证结果与分块无关；异常绝不能逃出线程函数体。

## Part 1 · top-k 事件

**写法**

```cpp
auto better = [&](const Key& a, const Key& b) {          // "a 比 b 好"
    if (a.notional != b.notional) return a.notional > b.notional;
    if (int c = tickers[a.index].compare(tickers[b.index]); c != 0) return c < 0;
    return a.index < b.index;
};
std::priority_queue<Key, std::vector<Key>, decltype(better)> heap(better);   // top() = 最差的保留者
```

`priority_queue` 的 `top()` 是比较器下「最大」的元素，而 `better` 下最大的就是排在最后的，也就是最差的保留者。堆里只放 16 字节的 `Key{notional, index}`，不复制字符串；最后才用下标构造 `Trade`。循环里先 `notional_at`（校验加乘法检查），堆满后 `notional < heap.top().notional` 就 `continue`，之后才建 `Key`。弹出的顺序是最差在前，`std::reverse` 一次。

**面试官在探什么**

1. **为什么取最大的 k 个用最差者在顶的堆**：新元素只需要和当前最差的保留者比，比它差就不可能进 top-k；最大堆要扫完才知道谁最差。
2. **比较器为什么要全序**：notional 相同的事件进哪个集合，否则取决于到达顺序或算法内部细节，结果没法复现，也没法测试。`nth_element` 和 `partial_sort` 尤其如此。
3. **快速拒绝为什么用严格小于**：`<=` 会把和堆顶 notional 相同、但 ticker 或下标更靠前的事件挡在门外。notional 相同时要走完整比较。
4. **溢出**：`LLONG_MAX * 2` 在 C++ 里是 UB，不是「回绕成 -2」。用 `__builtin_mul_overflow`，抛 `std::overflow_error`。每个事件都要算，排在末尾的溢出事件也不能漏。`3037000499` 的平方放得下，`3037000500` 的平方放不下。
5. **`reserve(k)`**：`k = INT_MAX` 时要申请几十 GB。容器按 `min(k, n)` 定大小。
6. **结果拥有字符串**：`Trade::ticker` 是 `std::string`。如果存 `string_view`，输入存储一释放，结果就悬空（ASan 会抓）。
7. **什么时候不用堆**：我在 `-O2` 下用 reference 测了 100 万个事件、5000 个 ticker：`k = 100` 时堆约 2 ms、`partial_sort` 约 3 ms、`nth_element` 约 9 ms、整体 `sort` 约 67 ms；`k = 100000` 时堆约 31 ms、`partial_sort` 约 43 ms、`nth_element` 约 16 ms、`sort` 约 64 ms。读法：k 小或数据流式用堆；数据在内存里且 k 很大用 `nth_element`（平均 O(n)，不关心 k），再排前缀；`sort` 最简单，用来对拍。
8. **ticker 的字节序**：比较要按无符号字节，`"\xC3\xA9"` 排在 `"Z"` 之后；`\0` 是名字的一部分，所以用带长度的 `string_view`，不用 `strcmp`。

**该说出口的话**：「大小为 k 的堆，堆顶是最差的保留者，堆满后一次 notional 比较就能拒绝绝大多数事件；比较器是全序，每个事件都用 builtin 检查乘法。」

## Part 2 · top-k ticker

**写法**

```cpp
void add_to(Totals& t, std::string_view k, long long amount) {
    if (auto it = t.find(k); it != t.end()) it->second = add_exact(it->second, amount);   // 先检查，再写
    else t.emplace(std::string(k), amount);
}
```

`Totals` 的哈希是透明的（`is_transparent`），`find(string_view)` 不构造临时 `std::string`，只有新键才拷贝一份。`add_exact` 抛异常时还没写表，所以表保持原样。`top_of` 的堆里放指向表节点的指针，最后才拷贝字符串到 `TickerTotal`。

**面试官在探什么**

1. **聚合和选择是两步**：聚合 O(n)，选择 O(m log k)；先全排序是 O(m log m)，多余。
2. **最大的事件不属于最大的 ticker**：样例里前者是 TSLA（200000），后者是 AAPL（270500）。
3. **每个事件都不溢出，合起来也可能溢出**：同一个 ticker 的两个 2^62 相加是 2^63，放不下；总额恰好等于 `LLONG_MAX` 要通过。
4. **零总额的 ticker 存在**：只要出现过，就要在结果里排在最后，不能因为 `if (total)` 丢掉。
5. **`summarize` 一趟算两个聚合**：总额和最大事件互不依赖；notional 和 ticker 都相同时，用严格大于，保留先出现的（下标小的）。
6. **指针堆的生命周期**：堆里的指针指向表的节点，`unordered_map` 的节点不会因 rehash 而移动，但表销毁后就悬空；所以返回前一定要拷贝成 `TickerTotal`。

**该说出口的话**：「先用哈希表聚合，再对不同 ticker 的个数 m 做大小为 k 的堆；溢出在每次累加时检查，表在抛出前不动。」

## Part 3 · 流式滑动窗口 top-k

**写法**：三个结构分工明确。

| 结构 | 作用 |
|---|---|
| `std::deque<Fill>` | 活跃成交，按到达顺序；只有队头会过期 |
| `unordered_map<string, {total, count}>` | 每个 ticker 的窗口总额和活跃笔数 |
| `std::set<Rank, RankOrder>` | 按（总额降序、ticker 升序）排好的活跃 ticker |

`add` 的顺序：先 `advance_to(f.time)`，再算 `add_exact(old, notional)`，这一步抛了什么都没动；然后才 `push_back` 和改排名。改键用 node handle：

```cpp
auto node = ranking_.extract(Rank{from, ticker});   // 摘下节点，不分配
node.value().total = to;
ranking_.insert(std::move(node));
```

过期是 `while (!live_.empty() && now - live_.front().time >= window)`：该 ticker 的活跃笔数为 1 就先从 `ranking_` 删条目、再删 map 节点；否则只改总额和笔数。

**面试官在探什么**

1. **为什么只用 `priority_queue` 不行**：ticker 的总额会变大也会变小，等于「改任意元素的键」，`priority_queue` 只能看堆顶、弹堆顶。替代方案有懒删除（旧条目留在堆里，弹出时发现不一致再丢，空间随更新数增长）和有序集合（删旧键、插新键，各 O(log m)，空间 O(m)）。
2. **窗口边界**：`now - time >= window` 过期，恰好差 `window` 就过期；写成 `>` 就差一。
3. **相等键陷阱**：零 notional 的成交打到已有 ticker 上，总额不变，新旧键相等。「先 `insert` 新键、再 `erase` 旧键」时 `insert` 什么也没做，`erase` 把唯一的条目删了，这个 ticker 从排名里消失。`extract` 加 `insert(node)` 无论键变没变都对，而且中间不会因分配失败而留下半截状态。
4. **`string_view` 指向 map 的键**：`Rank` 里的视图指向 `acc_` 节点里的 key，省掉一份字符串拷贝。代价是三条纪律：节点不会移动（`unordered_map` 保证）；先删排名条目、再删 map 节点；类不能拷贝也不能移动（拷贝出来的 `ranking_` 会指向旧对象的节点）。
5. **原子性**：溢出必须在改任何结构之前抛出；之后唯一可能抛的是分配失败，新 ticker 的路径用 `try/catch` 回滚。
6. **`std::visit`**：`replay` 用 `overloaded{...}` 处理 `Fill` / `Tick` / `Ask`，漏一个分支是编译错误，不是运行时 bug。
7. **复杂度**：每个成交最多进出各一次，摊还 O(log m)；查询是 O(log m + k)（取 `set` 的前 k 个）。
8. **能不能更快**：m 很小时每次查询直接扫 `unordered_map`；要精确且空间有界，就用 `set`。

**该说出口的话**：「堆改不了中间的元素，所以用有序集合：总额变了就摘下节点、改键、再插回去，窗口过期只看 `deque` 的队头。」

## Part 4 · 并行分块聚合

**写法**：`run_chunks` 为每块起一个 `std::jthread`，每个线程体包在 `try/catch` 里。

```cpp
try { body(c, from, to, stop.get_token()); }
catch (const Cancelled&) {}                                        // 被取消，不是错误
catch (...) { errors[c] = std::current_exception(); stop.request_stop(); }
```

所有 `jthread` 在作用域结束时 join，之后按块号从小到大重抛第一个记录的异常。每块的循环里每 4096 个事件看一次 `stop.stop_requested()`。三种实现：

| 实现 | 结构 | 要点 |
|---|---|---|
| `totals_chunked` | 每块一个 `jthread` + 一张私有表，最后合并 | 无共享、无锁；推荐 |
| `totals_recursive` | 左半 `std::async`，右半自己算 | 标准库没有线程池，`threshold = 1` 会起 n 个线程，所以 `threshold` 不能小 |
| `totals_sharded` | 16 片，每片一把 `std::mutex` | 对照组；热点 ticker 上线程排队。`alignas(64)` 让每片占自己的缓存行，避免伪共享 |

**面试官在探什么**

1. **合并为什么对**：整数加法满足结合律和交换律，怎么切、怎么合并都一样；每张表只被一个线程写，没有共享可变状态；所以不需要锁。
2. **溢出为什么与分块无关**：notional 非负，部分和单调不减，只要任何一块或任何一次合并溢出，真实总和就一定超过 `LLONG_MAX`，顺序版也会溢出；反过来，总和不超过 `LLONG_MAX` 时，所有部分和都不超过。所以单个事件、块内、合并三处都要检查。
3. **为什么价格用整数**：`double` 加法不满足结合律，并行结果会随分块抖动。
4. **异常逃出线程体**：直接 `std::terminate`。要 catch、存 `std::current_exception()`、join 之后再 `rethrow_exception`。
5. **取消是协作式的**：一块失败后 `request_stop()`，其他块在下一个检查点退出；测试要求失败调用的耗时小于完整运行的一半加 5 毫秒。
6. **`jthread` 和 `thread`**：`jthread` 析构时自动 `request_stop` 加 `join`；可 join 的 `std::thread` 被析构会 `std::terminate`。线程启动本身也可能抛异常（`emplace_back`），所以起线程的循环要 `catch`，先请求停止，再让 vector 析构去 join 已经起来的线程。
7. **块边界**：`n * c / chunks` 用 64 位无符号算，`n = 2'000'000'000`、`c = 3`、`chunks = 4` 得 1'500'000'000；用 `int` 乘会溢出。
8. **共享表为什么没有收益**：标准库没有并发哈希表，要自己分片加锁；热点 ticker 上所有线程排队，扩展性差。

**该说出口的话**：「每块算自己的表，最后合并，正确性靠整数加法的结合律；异常在线程里 catch 住带回主线程，失败时用 stop token 通知其他块。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 溢出 | `Math.multiplyExact` 抛 `ArithmeticException` | 有符号溢出是 UB，用 `__builtin_mul_overflow`，抛 `std::overflow_error` |
| 输入 | `String[]`，`null` 抛 NPE | `span<const string_view>`，没有 null；视图是借来的，结果要拥有 `std::string` |
| 堆里放什么 | `PriorityQueue<Trade>` | `priority_queue<Key>`，16 字节，需要时再查数组 |
| 改排名的键 | `TreeSet.remove` 加 `add` | `set::extract` 加 `insert(node)`：相等键陷阱、不分配 |
| 对哈希表的键取视图 | 不存在 | `string_view` 指向 map 节点；删除顺序和不可拷贝是你的责任 |
| 并发工具 | parallel 流、`RecursiveTask`、`StructuredTaskScope`、`ConcurrentHashMap` | `jthread` 加 `stop_source`、`std::async`、手写分片加 `mutex`；没有线程池和并发 map |
| 取消 | `Thread.interrupt` 加检查标志 | `std::stop_token`，同样是协作式 |
| 字符串顺序 | UTF-16 码元 | 无符号字节 |
