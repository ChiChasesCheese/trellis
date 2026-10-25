# Headlands · 18 题速读

从上往下读，越靠前越可能被问到；每题约 5 分钟：先把「题意」和「核心思路」用自己的话讲一遍，再扫数据结构、两种语言的要点和易错点。
你不需要把每题都写一遍，只要能解释「为什么这样做、哪里会错、被追问时怎么答」；代码只放最关键的几行。
读到哪里卡住了，再打开该题末尾的讲义；Java 和 C++ 两种语言都要能讲。

## 目录

| 题 | 一句话本质 | 难度手感 |
|---|---|---|
| [[#hc05 · 订单簿与限价撮合]] | 有序 Map + 同价 FIFO + id 索引，成交价取被动方 | 难，最可能考 |
| [[#hc14 · 成交日志与滑动窗口 VWAP]] | 定点数解析 + 队列增量维护窗口累计 | 中 |
| [[#hc15 · 流式中位数]] | 大顶堆 + 小顶堆，窗口版用惰性删除 | 中偏难 |
| [[#hc16 · 交易台层级树上的 DP]] | take / skip 两个状态，BFS 序倒扫代替递归 | 中 |
| [[#hc07 · 股票代码哈希表]] | 代码打包进一个 long，开放寻址，完美哈希 | 中偏难 |
| [[#hc02 · 合并 K 路有序流]] | 大小为 k 的最小堆装各序列的队首 | 中 |
| [[#hc04 · 队列均值与快照]] | running sum 用 128 位整数，快照 = 替换状态 | 中 |
| [[#hc09 · 按名义金额取 top-k]] | 大小为 k 的最小堆，窗口版用 TreeSet | 中 |
| [[#oa01 · Job 链报表]] | 把模糊题面变成完整的校验清单 | 易 |
| [[#hc01 · 买卖股票 DP 家族]] | free / hold 状态机 + 滚动数组 | 中 |
| [[#hc03 · 递归求和追问链]] | 溢出、栈深、闭式、并行，一层一层追问 | 中 |
| [[#hc08 · 订单序列 API]] | 两棵树状数组做前缀 count / quantity | 中偏难 |
| [[#hc11 · 订单区间最大重叠]] | 扫描线，同一时刻先结束后开始 | 中 |
| [[#hc06 · CPU 寄存器位运算]] | int 当 32 位无符号用，移位边界 | 易 |
| [[#hc13 · 定长内存池]] | int 数组里的空闲链表 + 版本号 handle + tagged CAS | 中偏难 |
| [[#ld01 · SPSC 共享内存通道]] | 单写者环形缓冲 + release / acquire | 难 |
| [[#ld02 · 交易相关 OOD]] | 状态机、FIFO 仓位、可组合风控、事件溯源 | 中 |
| [[#ld03 · 异步 TCP 消息通道]] | 成帧 + Selector + 背压链 + 重连 | 难 |

## hc05 · 订单簿与限价撮合

- **题意**：订单簿存放所有未成交的买单和卖单：买盘价高优先、卖盘价低优先，同价先到先成交。要支持 add / cancel / modify / 查最优价，再加限价撮合。例：簿上卖 101×5、101×3，来一张买 101×6，先吃 5 再吃 1，成交价是簿上那张单的 101。
- **核心思路**：「最优价」要反复取最小或最大，所以每侧按价格有序；同价位按到达顺序排队；撤单只给 id，所以另建 id 索引。撮合就是循环取对手盘最优价位的队头，价格不再交叉就停。成交价取被动方（maker）的价，因为 maker 报的价是它愿意接受的最差价，taker 的限价只是上限。市价单等于限价设成无穷，复用同一个循环，吃不完的作废。改量：减量保住队列位置，增量丢时间优先（移到队尾）。
- **数据结构**：每侧一个 `TreeMap<价格, 价位>`（买盘用倒序比较器），价位是 `LinkedHashMap<id, 订单>` 加总量缓存，再加 `HashMap<id, 订单>`。取最优 O(log L)（L = 价位数），撤单先查价位再 O(1) 删除。性能追问：价格是 long tick，直接当数组下标，订单放预分配的池，成交走回调不建事件对象，就能稳态零分配。
- **Java 要点**：① Java 21 的 `SequencedMap`：`firstEntry()` / `pollFirstEntry()` 直接取最优价；② 命令和事件用 `sealed interface` + `record`，`switch` 穷尽检查，新增类型编译器会提醒；③ 先 `Math.addExact` 算好再修改，抛异常时簿保持原样。
- **C++ 要点**：① `std::map<价格, 价位>` 升序，best ask 是 `begin()`，best bid 是最后一个；价位里用 `std::list`，id 索引存指向价位和链表节点的迭代器；② map 和 list 在增删其他元素时迭代器不失效，所以存迭代器合法，但拷贝后会悬空，簿设为 move-only；③ 增量改量用 `list::splice` 把节点移到队尾，迭代器仍有效；溢出用 `__builtin_add_overflow`（有符号溢出是未定义行为）。
- **易错点**：① `add` 不撮合（簿可以交叉），只有 `execute(Limit)` 才撮合；② 溢出检查必须在撮合之前，吃掉一半才发现溢出，已发出的成交收不回来；③ 价位被吃空要从 map 里删掉，否则最优价会取到空价位；校验顺序固定为 id → price → quantity → 簿状态。
- **追问**：撤单怎么 O(1)？id 索引直接指到节点，Java 是 `LinkedHashMap.remove(id)`，C++ 是存好的 list 迭代器。同价位怎么先来先成交？队列保序，增量改量才移到队尾。为什么价格用 long 不用 double？tick 是整数，浮点比较会让相等价位错位。
- **链接**：[[hc05_market_order_book|Java 讲义]] · [[hc05_market_order_book_cpp|C++ 讲义]]

```java
long left = qty;                                        // sweep：吃对手盘直到吃完或不再交叉
while (left > 0) {
    var top = opp.firstEntry();                         // 对手盘最优价位
    if (top == null || !(side == BUY ? top.getKey() <= limit : top.getKey() >= limit)) break;
    var level = top.getValue();  var maker = level.fifo.firstEntry().getValue();   // 队头 = 先到先成交
    long fill = Math.min(left, maker.qty);
    out.add(new Trade(takerId, maker.id, side, top.getKey(), fill));   // 成交价 = maker 的价
    left -= fill;  maker.qty -= fill;  level.total -= fill;
    if (maker.qty == 0) { level.fifo.pollFirstEntry(); byId.remove(maker.id);
                          if (level.fifo.isEmpty()) opp.pollFirstEntry(); }
}
```

## hc14 · 成交日志与滑动窗口 VWAP

- **题意**：日志每行 `ts_ms,symbol,price,qty`。按代码算 VWAP（= Σ价×量 / Σ量）和最低 / 最高价，坏行跳过并计数；再改成流式：只看最近 W 毫秒，随时问某代码的 VWAP 和名义金额最大的 k 个代码。例：`187.25` 存成 1_872_500（单位 0.0001）。
- **核心思路**：价格用 long 定点数，全程不碰 double；一行必须恰好 4 个字段，逐字符校验，不做 trim。窗口版用队列加每代码累计 (volume, notional)：新成交入队并累加，队头过期就出队并减掉，每笔成交只进出一次，所以摊还 O(1)。窗口是 (now − W, now]，`now − ts ≥ W` 就过期。top-k 对窗口内的代码做大小为 k 的最小堆。
- **数据结构**：汇总用 `TreeMap<代码, 累计>`（按代码有序输出）；窗口用 `ArrayDeque<Trade>` + `HashMap<代码, 累计>`，某代码的笔数减到 0 就删条目；top-k 用大小为 k 的堆，O(m log k)。百万行追问：一遍扫字节，代码最长 10 个字符、每字符 6 位，打包进一个 long 当键，开放寻址。
- **Java 要点**：① 手写 `indexOf(',')` 解析，不用 `split`、正则、`Double.parseDouble`（都会分配，浮点还丢精度）；② ASCII 数字用 `c >= '0' && c <= '9'`，`Character.isDigit` 会接受 Unicode 数字；③ `record Trade` 的紧凑构造器里 `Math.multiplyExact` 校验，手里有 Trade 就保证 price×qty 装得进 long。
- **C++ 要点**：① 用 `std::string_view` 切片，不拷贝；② `__builtin_mul_overflow` 对应 `multiplyExact`；③ `unordered_map<string, Acc, 透明哈希, equal_to<>>` 允许用 `string_view` 直接查，不必先构造 `std::string`；`char` 是有符号的，查表前转 `unsigned char`。
- **易错点**：① 四舍五入写成 `q = n / v; r = n % v; r >= v − r ? q + 1 : q`，不要写 `2 * r`（会溢出）；② 窗口差一：`ts = now − W` 的成交刚好过期；③ 空行不计入坏行，全空白行是坏行；`410.5` 与 `410.5000` 是同一个价格；乘积溢出的行算坏行。
- **追问**：为什么不用 double？浮点累加有误差、不满足结合律，金额要逐位可验。成交乱序到达怎么办？水位线加允许迟到，缓冲后重排。一亿行怎么并行？分块各算各的再合并，合并是加法和取 min / max，满足结合律。
- **链接**：[[hc14_vwap_trade_log|Java 讲义]] · [[hc14_vwap_trade_log_cpp|C++ 讲义]]

```java
static long vwap(long notional, long volume) {          // 四舍五入，半数向上
    long q = notional / volume, r = notional % volume;
    return r >= volume - r ? q + 1 : q;                 // 不写 2*r
}
private void advance(long t) {                          // 时钟推进，队头过期就减掉
    now = t;
    while (!live.isEmpty() && now - live.getFirst().tsMs() >= window) {
        var old = live.removeFirst();  var a = bySymbol.get(old.symbol());
        a.volume -= old.qty();  a.notional -= old.notional();
        if (--a.count == 0) bySymbol.remove(old.symbol());
    }
}
```

## hc15 · 流式中位数

- **题意**：价格一笔笔到达，随时回答中位数；追加：只看最近 k 笔、任意百分位、价格范围有界。例：依次加入 5, 15, 1, 3，中位数依次是 5, 5, 5, 3（偶数个取下中位数）。
- **核心思路**：大顶堆 `lo` 放较小的一半，小顶堆 `hi` 放较大的一半；不变式是 `lo` 里每个数 ≤ `hi` 里每个数，且 `|lo| = |hi|` 或 `|hi| + 1`，所以 `lo` 堆顶就是下中位数，取 O(1)，加入 O(log n)。滑动窗口时堆不能删任意元素：滑出的旧值记进「待删」表（惰性删除），浮到堆顶才真正弹出，两个堆按有效元素个数平衡。任意百分位 p：p 固定用两个堆，p 查询时才给用顺序统计树，价格有界用树状数组直方图。
- **数据结构**：两堆查询 O(1)，只适合一个固定的 p；顺序统计树（treap）查询 O(log n)，任意 p、值域无界，但实现最复杂；Fenwick 直方图查询 O(log T)，值域有界，构造后零分配。窗口版额外要一个环形缓冲记最近 k 个值，加两张待删计数表。
- **Java 要点**：① 大顶堆是 `new PriorityQueue<>(Collections.reverseOrder())`；② 待删计数用 `delayed.merge(old, 1, Integer::sum)`；③ `doubledMedian()` 返回中位数的两倍，避开「平均数怎么舍入」的约定，和溢出时用 `Math.addExact` 抛异常。
- **C++ 要点**：① `std::priority_queue<long long>` 默认就是大顶堆，小顶堆要写 `priority_queue<ll, vector<ll>, greater<>>`；② 待删表用 `unordered_map`，环形缓冲用 `vector` 加取模；③ 空结构取值抛 `std::out_of_range`，参数非法抛 `std::invalid_argument`，参数检查先于判空。
- **易错点**：① 平衡要按有效元素个数，不是 `heap.size()`；② 每次操作后两个堆顶都必须有效（先清掉失效的），否则 `median()` 会取到已滑出窗口的值；③ 升序流里旧的小值沉在 `lo` 底部永远浮不上来，失效元素多于 2k 时要整体重建，否则堆长到 O(n)。
- **追问**：为什么不排序？每次 O(n log n)，插入有序数组也是 O(n)。旧值在哪个堆里？`old ≤ lo.peek()` 就在 `lo`，因为 `lo` 里每个数都 ≤ `hi` 里每个数。每秒几百万次更新还要 p99？价格有界就用 Fenwick 直方图。
- **链接**：[[hc15_streaming_median|Java 讲义]] · [[hc15_streaming_median_cpp|C++ 讲义]]

```java
void add(long price) {
    if (lo.isEmpty() || price <= lo.peek()) lo.add(price); else hi.add(price);
    if (lo.size() > hi.size() + 1) hi.add(lo.poll());      // lo 太大，挪一个给 hi
    else if (hi.size() > lo.size()) lo.add(hi.poll());     // hi 太大，挪一个给 lo
}
long median() { return lo.peek(); }                        // 下中位数，O(1)
```

## hc16 · 交易台层级树上的 DP

- **题意**：交易台组成一棵树（`parent[i]` 是上级，根是 -1），每台有 PnL（可为负）。选一些台，任何台和它的直接上级不能同时选，求最大总 PnL（树上的打家劫舍）；再还原选了哪些台、求最大路径和；最后一条 10^5 层的链不能爆栈。
- **核心思路**：每个台两个状态：`take[v] = pnl[v] + Σ skip[孩子]`（选 v），`skip[v] = Σ max(take, skip)[孩子]`（不选 v），答案是 `max(take[根], skip[根])`。必须先算孩子再算父亲：建树时 BFS 得到「父亲排在孩子前面」的顺序，倒着扫就是后序，不需要递归。还原方案自顶向下：v 被选当且仅当上级没选且 `take > skip`（严格大于，平局不选）。路径和：每个点记最好的两条向下支（负的当 0），在该点拐弯 = 左支 + 自己 + 右支。
- **数据结构**：`parent[]`、`pnl[]`、孩子表（CSR：`childStart` + `childList` 两个 int 数组）、BFS 顺序 `order[]`、两个 `long[]`。O(n) 时间，O(n) 空间。
- **Java 要点**：① 全用原始数组，不建 `Node` 对象，10^6 个台 < 2 s；② 入参数组 `clone()` 防御性拷贝；③ 范围检查写 `p > MAX || p < -MAX`，因为 `Math.abs(Long.MIN_VALUE)` 仍是负数。`|pnl| ≤ 10^12`、`n ≤ 10^6` 保证所有和 ≤ 10^18 < Long.MAX_VALUE，不需要 `addExact`。
- **C++ 要点**：① 同样的 `vector<int>` / `vector<long long>` 布局；② 递归版在 10^5 层链上会栈溢出，C++ 是直接段错误，不像 Java 的 `StackOverflowError` 可以捕获；③ 下标用 `int`，和 `size()`（无符号）比较时小心 `-1` 回绕。
- **易错点**：① 不保证 `parent[i] < i`，根也不一定是 0，不能把下标顺序当拓扑序；② 建树校验顺序固定：长度 → 台数上限 → pnl 范围 → parent 范围 → 根的个数 → 从根到不了所有台（环）；③ 选台允许一个都不选，所以全负的树答案是 0；但路径必须非空，全负时 `maxPathSum` 是最不坏的单个台。
- **追问**：为什么不用递归？链 10^5 层栈溢出，BFS 序倒扫栈深是 O(1)。输入是边列表怎么办？从指定根 BFS 定向得到 parent，再同样处理。换根答案会变吗？最大独立集和最大路径和是无向树的性质，不变；`plan()` 的平局和 `bestSubtree()` 依赖根，会变。
- **链接**：[[hc16_tree_dp|Java 讲义]] · [[hc16_tree_dp_cpp|C++ 讲义]]

```java
long[] in = new long[n], out = new long[n];             // in = 选 v，out = 不选 v
for (int v = 0; v < n; v++) in[v] = pnl[v];
for (int i = n - 1; i >= 0; i--) {                      // order 是 BFS 序：倒着扫 = 先孩子后父亲
    int v = order[i], p = parent[v];
    if (p >= 0) {
        in[p]  += out[v];                               // 选父亲，孩子不能选
        out[p] += Math.max(in[v], out[v]);              // 不选父亲，孩子随意
    }
}
return n == 0 ? 0 : Math.max(in[root], out[root]);
```

## hc07 · 股票代码哈希表

- **题意**：股票代码（至多 8 个大写字母）做 key 的查表，比如累加每个代码的成交量。从 `HashMap<String, Long>` 出发，一步步优化：手写开放寻址表、把代码打包进一个 long、完美哈希、堆外定长表，并说出你怎么测量。
- **核心思路**：通用 `HashMap` 慢在每个条目有多个对象、要装箱、要追指针（缓存未命中）。突破口是 key 的结构：至多 8 个 A–Z，每字符 5 位共 40 位，正好装进一个 long，比较就是 `==`，没有 `hashCode` / `equals` 的调用。开盘前代码全集已知时，用最小完美哈希（集合内零冲突，value 数组长度恰好 n）；订阅时把代码解析成下标缓存起来，之后每条消息直接用下标。
- **数据结构**：线性探测的开放寻址：删除留墓碑（探测链不能在删除处断），（占用 + 墓碑）/ 容量 ≤ 3/4，超了就 rehash 并清墓碑；key 和 value 交错放在同一个 `long[]`，一个缓存行拿到两样；哈希函数用乘黄金比例取高位。完美哈希用 hash-and-displace。堆外版用 FFM `Arena`，64 字节对齐，每槽 16 字节。
- **Java 要点**：① `slots[2i] = key`、`slots[2i + 1] = value` 的交错布局；② `sealed Parsed permits Ticker, Invalid` + 模式匹配，合法与非法在类型里区分；③ 用 `ThreadMXBean.getThreadAllocatedBytes` 量稳态分配，用 `Arena.ofShared()` 的 `MemorySegment` 做堆外。
- **C++ 要点**：① 对应 `std::vector<Slot>` 加 `uint64_t` 键；`std::unordered_map` 是链地址法，每个节点单独分配，这正是要优化掉的；② `string_view` 配透明哈希，查找时不建 `std::string`；`std::bit_ceil` 取 2 的幂容量；③ 堆外对应一块 `aligned_alloc` 的对齐内存，容量固定、不扩容。
- **易错点**：① 哈希写成 `key & mask`：打包后短代码的低位全是补的 0，几乎所有 key 落到同一格，要乘常数后取高位；② 删除不留墓碑会切断探测链，后面的 key 查不到；反复「插新删旧」要靠 rehash 清墓碑，否则表里没有空格会死循环；③ 完美哈希只保证集合内不冲突，`indexOf` 里必须比较 `keys[slot] == key`，否则集合外的 key 会被误认。
- **追问**：怎么证明更快？测 ns/op、每条记录的字节数、最长探测距离，用真实的偏斜数据，并说清哪些结论没测。key 不止 8 个字符？用两个 long 的 128 位 key，或字符串哈希加字节比较。多线程更新？每线程一张表最后合并，或 `LongAdder`、CAS。
- **链接**：[[hc07_ticker_hash_map|Java 讲义]] · [[hc07_ticker_hash_map_cpp|C++ 讲义]]

```java
static long pack(CharSequence s) {                      // 'A'..'Z' -> 1..26，每字符 5 位，共 40 位
    long key = 0;
    for (int i = 0; i < s.length(); i++)
        key |= (long) (s.charAt(i) - 'A' + 1) << (5 * (7 - i));   // 第 0 个字符在最高 5 位
    return key;                                         // 短代码尾部补 0，所以 key > 0
}
private int home(long key) {                            // 乘黄金比例，取高位
    return (int) ((key * GOLDEN) >>> shift);            // shift = 64 - log2(capacity)
}
```

## hc02 · 合并 K 路有序流

- **题意**：k 个各自升序的序列合并成一个升序序列，相等元素按序列编号小的在前（稳定）。例：`[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]`。追问：惰性和无限流、每个源是会阻塞的 client 的多线程版、结构化并发。
- **核心思路**：每个序列只有队首有资格输出，k 个队首里最小的就是下一个输出，所以用大小为 k 的最小堆装队首；弹出一个，再把它所在序列的下一个元素补进堆，总共 O(N log k)。惰性版：构造时不碰任何源，输出一个元素后，它所在序列的下一个推迟到下一次调用才取（源可能很慢或无限）。多线程版：每个源一个虚拟线程生产者加一条有界队列，合并线程只看各队首；某条流的队首还没到时无法安全决定输出，返回 `Pending`，它的意思是「现在不能决定」，不是「没数据」。
- **数据结构**：`PriorityQueue<Head(value, stream)>`，比较器先比值、再比序列编号（保证稳定）；并发版每源一个 `ArrayBlockingQueue(capacity)`，满了生产者阻塞（背压）；队列里的消息是 `sealed` 的 `Item` / `End` / `Failed`，生产者结束时一定留下 `End` 或 `Failed`，合并器不会永远等一个已经死掉的生产者。
- **Java 要点**：① 比较用 `compareTo`，不要 `a - b`（`Long.MIN_VALUE` 与 `Long.MAX_VALUE` 会溢出）；② 实现 `Iterator<T>` 的 `hasNext` / `next`；`Thread.ofVirtual().start(...)` 起生产者；③ `StructuredTaskScope.ShutdownOnFailure`：一个源失败，其余被中断，走出方法时没有线程泄漏。
- **C++ 要点**：① `std::priority_queue` 弹出的是「最大」，比较器要写成「a 排在 b 之后」，而且它不稳定，平局要自己比较序列编号；② 惰性版做成 input iterator；③ 线程用 `std::jthread` 加 `std::stop_token`（析构自动 join，stop 能唤醒阻塞的等待），队列用 `condition_variable_any` 才能同时等 stop_token。
- **易错点**：① 乱序检查发生在读到那个元素的时候（惰性），不是一开始；元素为 `null` 抛 NPE；② 生产者抛异常也必须放一条 `Failed`，否则合并器永远等它；③ `close()` 时生产者可能阻塞在 `put` 或源里，要靠中断唤醒并等它们退出。
- **追问**：为什么用堆不是每次扫 k 个队首？O(log k) 对 O(k)。慢源拖住整体怎么办？`tryNext()` 非阻塞，返回 `Pending`，调用方可以先做别的。某个源抛异常？读到 `Failed` 时先输出它失败前已入队的元素，再抛 `MergeException` 并关闭其余。
- **链接**：[[hc02_merge_k_streams|Java 讲义]] · [[hc02_merge_k_streams_cpp|C++ 讲义]]

```java
var heap = new PriorityQueue<Head<T>>(Comparator
        .<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream));  // 先值，后序列号 = 稳定
for (int i = 0; i < k; i++) if (advance(heads[i])) heap.add(heads[i]);          // 每个序列放进队首
while (!heap.isEmpty()) {
    Head<T> h = heap.poll();                            // 最小的队首
    out.add(h.value);
    if (advance(h)) heap.add(h);                        // 补进同一个序列的下一个
}
```

## hc04 · 队列均值与快照

- **题意**：实现 FIFO 队列的 `push` / `pop` / `getMean`，均值要 O(1)。追问：快照事件修正历史、保留每个历史版本、单写者多读者。例：push 1, 2, 3 均值 2.0；push 4 均值 2.5；pop 返回 1，均值 3.0。
- **核心思路**：维护 running sum 和个数，均值 = sum / size，每个操作 O(1)。真正考的是三个坑：sum 用 double 会丢精度（`1e16 + 1 + 1 − 1e16` 得 0），用 long 会溢出，所以用 128 位整数；均值返回约分后的分数，或最接近的 double。快照 `Correct(list)` 的意思是丢掉整段历史，用快照内容替换队列和 sum。版本化队列：所有 push 过的元素组成一棵树，一个版本 = (尾节点, 已弹出个数, 窗口和)；push 新建子节点，pop 要找路径上某深度的祖先，用跳表式指针 O(log n)，绝不能每个版本复制一份内容。单写多读：写者每次改完发布一个不可变快照 `(seq, size, sum)`，读者 acquire 读一次引用，不会读到「新 sum 配旧 size」。
- **数据结构**：环形缓冲区（容量 2 的幂，下标用 `& (len − 1)` 代替取模，满了翻倍）+ 128 位累加器 + 个数。
- **Java 要点**：① Java 没有 128 位整数，自己写 `record I128(long hi, long lo)`，进位靠 `Long.compareUnsigned`，符号扩展靠 `x >> 63`；② 转 `BigInteger` 后约分；③ `VarHandle` 的 `setRelease` / `getAcquire` 发布快照 record；`-x` 对 `Long.MIN_VALUE` 会溢出。
- **C++ 要点**：① 有现成的 `__int128`，不用自己写进位；② 环形缓冲用 `vector<long long>` 加 mask，比 `std::deque` 紧凑；③ 128 位和转 double 要正确舍入：和在 ±2^53 以内时一次除法就是正确舍入，否则用长除法；无锁读者的字段必须是 `std::atomic`（或 seqlock），裸变量的并发读写是数据竞争，属于未定义行为。
- **易错点**：① 用 double 累加；② 和超过 `Long.MAX_VALUE` 之后再弹回小数，累加器不能「卡」在大数上（128 位不会有这个问题）；③ 环形缓冲扩容时 `head` 不在 0，要分两段拷贝；均值 3/2 要约分，符号只放分子。
- **追问**：snapshot 是拷贝还是共享？`Correct` 事件必须拷贝传入的列表。为什么不每次重新求和？每次 O(n)。滑动窗口均值呢？同一思路，滚动统计，注意数值稳定性和 NaN / Inf。
- **链接**：[[hc04_queue_mean_snapshot|Java 讲义]] · [[hc04_queue_mean_snapshot_cpp|C++ 讲义]]

```java
record I128(long hi, long lo) {                         // 128 位补码：hi 有符号，lo 按无符号用
    I128 plus(long x) {
        long l = lo + x;
        long carry = Long.compareUnsigned(l, lo) < 0 ? 1 : 0;   // lo 回绕了一次，就进位
        return new I128(hi + (x >> 63) + carry, l);             // x >> 63：非负为 0，负数为 -1
    }
    I128 minus(long x) {
        long l = lo - x;
        long borrow = Long.compareUnsigned(lo, x) < 0 ? 1 : 0;
        return new I128(hi - (x >> 63) - borrow, l);
    }
}
```

## hc09 · 按名义金额取 top-k

- **题意**：三个平行数组 `tickers` / `prices` / `volumes`，事件的名义金额 = price × volume。取名义金额最大的 k 个事件；再扩展到按 ticker 汇总、滑动窗口内的 top-k、多线程分块聚合。例：TSLA 25000×8 = 200000 是最大的事件，但按 ticker 汇总是 AAPL 270500 最大，最大事件不属于最大 ticker。
- **核心思路**：取最大的 k 个用大小为 k 的最小堆：堆顶是保留集合里最差的，新事件比堆顶好才顶替，O(n log k)；随机顺序下绝大多数事件比堆顶还小，一次 long 比较就拒绝，连对象都不用建。排序规则要成为全序：名义金额降序 → ticker 升序 → 下标升序，结果才唯一。窗口版：旧成交过期会让某个 ticker 的总额变小，等于改任意元素的键，堆找不到任意元素，所以用 `TreeSet` 按（总额降序, ticker 升序）排名，删旧键、插新键，O(log m)。并行：切块各自聚合，最后合并，整数加法满足结合律，所以结果与分块方式无关。
- **数据结构**：事件 top-k 用 `PriorityQueue`（容量 k）；ticker 汇总用 `HashMap.merge` 再接堆；窗口版用 `ArrayDeque`（活跃成交，队头最老）+ `HashMap`（总额）+ `TreeSet`（排名）；并行版是每块一个 Map 再合并。
- **Java 要点**：① 每个事件都要算 `Math.multiplyExact`，即使进不了 top-k，这样溢出一定被发现；② 比较器 `Comparator.comparingLong(...).reversed().thenComparing(...)`；`List.reversed()` 是 Java 21 的 Sequenced Collections；③ `Collectors.groupingBy` 和 `teeing` 做汇总，`StructuredTaskScope.ShutdownOnFailure` 做分块。
- **C++ 要点**：① top-k 可用 `std::partial_sort` 或 `std::nth_element`；② `std::set` 对应 `TreeSet`，比较器里放全部 tie-break；`unordered_map` 用 `string_view` 查要配透明哈希；③ 输入用 `std::span` 视图，不拥有数据；并行用 `std::jthread`，每块一个局部 map 最后合并；溢出用 `__builtin_mul_overflow`。
- **易错点**：① 比较器少一级 tie-break，结果不唯一，测试无法复现；② 窗口边界：`now − time ≥ window` 就过期，恰好差 window 也算过期；③ 溢出要在三处都报：单个事件、某一块的部分和、合并两块时；总额恰好等于 `Long.MAX_VALUE` 必须通过，多 1 必须报，与分块无关。
- **追问**：滑动窗口为什么只用 `PriorityQueue` 不行？不能改任意元素的键，`remove(Object)` 是 O(m)。并行合并为什么对？整数加法满足结合律和交换律，double 不行。为什么 top-k 用最小堆而不是最大堆？堆顶放最差的，才能 O(1) 判断新事件值不值得顶替。
- **链接**：[[hc09_top_trades_by_notional|Java 讲义]] · [[hc09_top_trades_by_notional_cpp|C++ 讲义]]

```java
var heap = new PriorityQueue<Trade>(Math.max(1, Math.min(k, n)), BEST_FIRST.reversed()); // 堆顶 = 保留的里最差的
for (int i = 0; i < n; i++) {
    long notional = Math.multiplyExact(prices[i], volumes[i]);   // 每个事件都算，溢出一定被发现
    if (k == 0) continue;
    if (heap.size() == k && notional < heap.peek().notional()) continue;  // 快速拒绝，零分配
    var t = new Trade(i, tickers[i], prices[i], volumes[i]);
    if (heap.size() < k) heap.add(t);
    else if (BEST_FIRST.compare(t, heap.peek()) < 0) { heap.poll(); heap.add(t); }  // 比堆顶好才顶替
}
```

## oa01 · Job 链报表

- **题意**：CSV 每行 `job_id,runtime,next_job_id`（`next = 0` 表示链尾），job 首尾相接成若干条链。每条链输出起点、终点、job 数、总时长、平均时长（`hh:mm:ss`），按总时长降序（相同按 start 升序）；输入有任何问题就只输出 `Malformed Input`。例：1 → 23 → 3，运行时间 60 + 30 + 15 = 105 秒，输出 `00:01:45`，平均 35 秒。
- **核心思路**：算法只是 O(n) 的哈希，难点是把模糊题面变成完整的校验清单。单行内：恰好 3 个整数、`id > 0`、`runtime ≥ 0`、`next ≥ 0`、不是自环。跨行：重复 id、悬空 next、多前驱（两个 job 指向同一个）、环。拼链：没有前驱的 job 是链头，沿 `next` 走到 0；走完后没被访问到的 job 只能在环上（每个节点入度 ≤ 1）。平均时长整秒截断，小时至少两位、不截断。
- **数据结构**：`LinkedHashMap<id, Job>`（按输入顺序遍历）+ `HashSet` 记有前驱的 id + 已访问集合；总时长用 long。
- **Java 要点**：① `record Job` 的紧凑构造器做单行校验；② `sealed Outcome permits Ok, Malformed` 加 `switch` 渲染，编译器保证两种情况都处理；③ `"%02d:%02d:%02d".formatted(...)` 格式化，`Comparator.comparingLong(...).reversed().thenComparingInt(...)` 排序；`Integer.parseInt` 超范围会抛 `NumberFormatException`，要转成 Malformed，且进程退出码仍为 0。
- **C++ 要点**：① 用 `std::from_chars` 解析整数，并检查整段 token 都被消耗（它不跳过空白、不接受 `+`）；② `unordered_map<int, Job>` 加 `unordered_set`；③ `getline` 读行，行尾的 `\r` 要处理；总时长用 `long long`。
- **易错点**：① 漏掉「好链加一个独立的环」：环上没有链头，只能靠已访问数 ≠ 总数发现；② 多前驱和悬空 `next` 容易漏；③ 平均数是截断不是四舍五入（35 秒 / 2 = 17.5 → `00:00:17`），排序第一键是总时长降序。
- **追问**：为什么不用 DFS 找环？入度 ≤ 1 之后每个节点只属于一条链或一个环，数访问个数就够了。并列怎么排？start 升序做第二键。数据量很大呢？O(n) 时间、O(n) 空间，一遍流式读入即可。
- **链接**：[[oa01_job_chain|Java 讲义]] · [[oa01_job_chain_cpp|C++ 讲义]]

```java
var byId = new LinkedHashMap<Integer, Job>();
for (var j : jobs) if (byId.putIfAbsent(j.id(), j) != null) throw malformed("duplicate id");
var hasPred = new HashSet<Integer>();
for (var j : jobs) {
    if (j.nextId() == 0) continue;
    if (!byId.containsKey(j.nextId())) throw malformed("dangling next");
    if (!hasPred.add(j.nextId())) throw malformed("two jobs point at one");
}
// 没有前驱的是链头：沿 next 走到 0，统计 count / total，并记 visited
if (visited.size() != byId.size()) throw malformed("cycle");   // 没走到的只能在环上
```

## hc01 · 买卖股票 DP 家族

- **题意**：给 n 天价格，每次只能持一股、同一天只做一个动作，问最多赚多少。逐步放宽：一次交易 → 次数不限 → 最多 k 笔 → 加冷却期和手续费 → 还原具体的买卖日。例：`[7,1,5,3,6,4]` 一次交易赚 5，不限次数赚 7。
- **核心思路**：把每天画成状态机，只有「不持股 free」和「持股 hold」两个状态，记每个状态下的最优现金。一次交易：边扫边记最低价，答案是今天价格减最低价的最大值（最低点必须在最高点之前）。不限次数：所有上涨日的差价之和。最多 k 笔：`hold[j] = max(hold[j], free[j−1] − p)`，`free[j] = max(free[j], hold[j] + p)`，j 从大到小更新，保证用的都是「昨天的值」；k ≥ n/2 时退化成不限次数。冷却期多一个 COOL 状态（卖出当天），手续费在卖出时扣。
- **数据结构**：长度 k+1 的滚动数组 `free` / `hold`，时间 O(n·min(k, n/2))，空间 O(min(k, n/2))。还原交易时每格多记一个决定位，再回溯，格子数太大就拒绝。
- **Java 要点**：① 负无穷用 `Long.MIN_VALUE / 4`，留出余量，之后再减价格或手续费也不会溢出；② `enum State { FREE, HOLD, COOL }` 加 `afterRest / afterBuy / afterSell`，`sealed Move`（Buy / Sell）配合 `switch` 逐天回放检查方案；③ 输入上界（价格 ≤ 2^40，天数 ≤ 2^22）保证利润装得进 long，内循环不需要 `addExact`。
- **C++ 要点**：① `vector<long long>`，负无穷用 `LLONG_MIN / 4`，有符号溢出是未定义行为；② k 可以到 `INT_MAX`，先和 n/2 取小，千万别 `vector(k + 1)`；③ 状态用 `enum class State`，动作用 `std::variant<Buy, Sell>`。
- **易错点**：① k 很大时 `new long[k + 1]` 内存爆炸；② 冷却期下 `[1,2,1,2]` 不能第 1 天卖、第 2 天买；③ 手续费等于价差时净利润为 0，平局选「休息」，`plan` 里不出现零利润的交易；一次交易别写成全局最大减全局最小。
- **追问**：为什么 j 要倒序更新？正序会用到今天刚更新的 `free[j−1]`，等于同一天卖了又买。怎么还原交易？记下每格是买、卖还是休息，再回溯。空间还能省吗？滚动数组已经是 O(k)。
- **链接**：[[hc01_stock_trading_dp|Java 讲义]] · [[hc01_stock_trading_dp_cpp|C++ 讲义]]

```java
long[] free = new long[k + 1];                          // free[j]：不持股、已用 j 笔时的最大现金
long[] hold = new long[k + 1];                          // hold[j]：持股、买入算在 j 笔内
Arrays.fill(hold, NEG);                                 // 还没买过：不可达，NEG = Long.MIN_VALUE / 4
for (long p : prices)
    for (int j = k; j >= 1; j--) {                      // 倒序：用的都是「昨天」的值
        free[j] = Math.max(free[j], hold[j] + p);       // 休息，或今天卖
        hold[j] = Math.max(hold[j], free[j - 1] - p);   // 休息，或今天买
    }
return free[k];
```

## hc03 · 递归求和追问链

- **题意**：「写个函数递归求 1 到 n 的和」只是脚手架，面试官每问一句就考一个层面：溢出、栈深、区间含负数、并行。例：用 int 位宽时，n = 65535 得 2147450880，n = 65536 溢出，精确值是 2147516416。
- **核心思路**：① 返回类型：`sealed SumResult = Ok(value) | Overflow(exact)`，溢出时带精确值，不返回回绕的错数；加法用 `addExact`。② JVM 没有尾调用优化，递归深度受栈大小限制（默认 1 MiB 约几万层），所以栈比 int 先「溢出」；改成循环，或用 trampoline：尾递归写法返回 `More(下一步)`，由一个 `while` 循环反复执行，把栈换成堆。③ 区间 [a, b]：`(a+b)` 与 `(b−a+1)` 奇偶相反，偶的那个先除 2 再乘；中间量溢出不等于结果溢出，快路径失败就退到 `BigInteger` 再判。④ 并行：逐步 `addExact` 的结果取决于顺序（`[MAX, 1, −1]`），所以每块用满足结合律的 128 位累加器，最后只判一次放不放得进 long。
- **数据结构**：`sealed` 结果类型；`Trampoline = Done | More`；128 位累加器 `Wide(hi, lo)`；ForkJoin 的 `RecursiveTask` / parallel stream / 虚拟线程分块。
- **Java 要点**：① `Math.addExact` / `multiplyExact` / `toIntExact`；② `StackOverflowError` 是 `Error`，不要吞掉；用 `new Thread(null, r, name, stackBytes)` 指定栈大小来量深度；③ `RecursiveTask` 的 `fork` / `join` 配阈值，`StructuredTaskScope` 每块一个虚拟线程。
- **C++ 要点**：① `-O2` 常把尾递归编译成循环（Java 不会），但不能依赖；② 栈溢出是段错误，捕获不了；有符号溢出是未定义行为，要用 `__builtin_add_overflow`；③ 128 位累加直接用 `__int128`，并行用 `std::jthread` 分块。
- **易错点**：① `n * (n + 1) / 2` 的中间量 `n*(n+1)` 先溢出，哪怕结果装得下；② 逐步 `addExact` 的并行版结果不确定，换个切法就可能抛或不抛；③ 测 int 位宽的 n = 65536 时，默认栈上递归先栈溢出，要换大栈线程。
- **追问**：Java 为什么没有尾调用优化？为了保留完整的调用栈轨迹，规范没有要求。区间含负数？公式照样成立，用 `BigInteger` 兜底。double 并行求和为什么结果会抖？浮点加法不满足结合律。
- **链接**：[[hc03_recursive_sum|Java 讲义]] · [[hc03_recursive_sum_cpp|C++ 讲义]]

```java
static SumResult rangeSum(long a, long b) {
    try {
        long s = Math.addExact(a, b);                        // (a+b) 与 (b-a+1) 恰好一奇一偶
        long count = Math.addExact(Math.subtractExact(b, a), 1);
        long v = (count & 1) == 0 ? Math.multiplyExact(count / 2, s)   // 偶的那个先除 2
                                  : Math.multiplyExact(count, s / 2);
        return new Ok(v);
    } catch (ArithmeticException e) {                        // 中间量溢出 != 结果溢出
        var exact = rangeSumExact(a, b);                     // 退到 BigInteger 再判
        return exact.bitLength() <= 63 ? new Ok(exact.longValueExact()) : new Overflow(exact);
    }
}
```

## hc08 · 订单序列 API

- **题意**：维护按到达顺序排列的活跃订单 (id, qty)：`put` 放到末尾，`delete(id, qty)` 减量（减到 0 就移除，位置不变），`countUpTo(id)` / `qtyUpTo(id)` 问「从头到该订单」一共几张、多少量，`idAt(k)` 取第 k 张。例：序列 `[10:5, 20:3, 30:7]`，`COUNT 30` = 3，`QTY 20` = 5 + 3 = 8。
- **核心思路**：查询就是前缀和，每次从头加是 O(n)。订单总是追加在末尾，所以给每张订单一个递增的「插入下标」，删除只把该下标的数清零（留洞）。两棵 Fenwick 树（树状数组）按下标累加：一棵存活跃单数，一棵存剩余量，查询和修改都是 O(log n)；`idAt(k)` 在计数树上做二分下降。留洞会让下标只增不减，所以下标空间写满时要压缩：把活跃订单按序重新编号，让容量跟着活跃数走，而不是跟着历史走。
- **数据结构**：Fenwick `cnt[]`（int）和 `sum[]`（long），容量取 2 的幂；`HashMap<id, 下标>`；`idByIdx[]` / `qtyByIdx[]`；总量一个 long。
- **Java 要点**：① 更新 `for (; i <= cap; i += i & -i)`，查询 `for (; i > 0; i -= i & -i)`；② 所有会抛异常的检查（qty、重复、溢出）都排在修改之前，失败时状态不变；③ 未知 id 抛 `NoSuchElementException`，越界抛 `IndexOutOfBoundsException`，文本接口用 `sealed Op` / `Result`。
- **C++ 要点**：① 树用 `vector<int>` / `vector<long long>`；② 用 `std::bit_ceil` 取 2 的幂容量；`i & -i` 要保证 i > 0；③ 文本命令用 `std::from_chars` 解析，溢出检查用 `__builtin_add_overflow`。
- **易错点**：① Fenwick 下标从 1 开始，从 0 开始会死循环；② 部分删除只减量，不改 `countUpTo`，减到 0 才移除；同一个 id 删光后再 `put`，排到最后；③ 不压缩的话，200 万次 put / delete 循环会让内存一直涨，压缩后容量必须 ≤ 4096。
- **追问**：为什么用 Fenwick 不用线段树？同样 O(log n)，但只要一个数组、循环里只有加法和位运算，常数小、代码短。为什么不用离散化？插入下标天然递增。`idAt` 怎么二分？步长从大到小试，整块的订单数还小于剩余的 k 就整块跳过。
- **链接**：[[hc08_order_sequence_api|Java 讲义]] · [[hc08_order_sequence_api_cpp|C++ 讲义]]

```java
void add(long[] tree, int i, long delta) {              // 点更新：加到所有「管着 i」的结点
    for (; i <= capacity; i += i & -i) tree[i] += delta;   // i & -i = 最低位的 1
}
long prefix(long[] tree, int i) {                       // [1, i] 拆成若干不相交的块
    long r = 0;
    for (; i > 0; i -= i & -i) r += tree[i];
    return r;
}
// idAt(k)：pos = 0；步长从 capacity 减半，tree[pos + step] < k 就整块跳过（pos += step, k -= tree[pos]）
```

## hc11 · 订单区间最大重叠

- **题意**：每张订单活在半开区间 `[start, end)`，问同一时刻最多有多少张订单同时活着（以及最早出现的时刻）。追问：按买 / 卖方向分别算、撤单把区间截短、在线版、坐标高达 10^18 的线段树。例：`[[1,5],[2,6],[4,8]]` → 3，最早在 t = 4；`[[1,3],[3,5]]` → 1，不重叠。
- **核心思路**：扫描线。最大值只会出现在某个 start 上（只有 start 让计数变大），所以把 starts 和 ends 各自排序；处理第 i 个 start 时，先扣掉所有 `end ≤ s` 的结束（同一时刻先结束后开始），活跃数 = (i+1) − 已结束数，严格大于才更新，这样保留最早的时刻。如果区间是闭区间，条件改成 `end < s`。撤单就是把 end 变成 `min(end, time)`，`time ≤ start` 则这张单从没活过。在线版里同一时间戳的事件算一批，最大值要追溯修正。大坐标：坐标压缩加懒标记线段树（区间加、区间最大）。
- **数据结构**：两个各自排好序的 `long[]`（比事件列表省）；买、卖各一条车道；`IntervalIndex` 用排序去重的端点数组加二分，再加线段树；总复杂度 O(n log n)。
- **Java 要点**：① 对坐标只比较、不做 `end − start` 或 `(a+b)/2`，坐标接近 `Long.MAX_VALUE` 会溢出；② `Arrays.sort(long[])`，输入数组不能被修改；③ `sealed OrderEvent`（Place / Cancel）加 `switch` 分派。
- **C++ 要点**：① `std::sort` 两个 `vector<long long>`；② 也可以用 `std::map<long long, int>` 做差分数组，遍历时累加前缀和；③ 查「t 时刻活着几个」用 `upper_bound` 再往前退一格；事件用 `std::variant<Place, Cancel>`；线段树下标是 `size_t`，无符号减法会回绕。
- **易错点**：① 必须先结束再开始，否则 `[1,3)` 与 `[3,5)` 会被数成 2 个；② `start == end` 的空区间要忽略；同一个 id 多次撤单，最早的生效；③ 买方峰值和卖方峰值可以出现在不同时刻，所以 `all.count` 不等于 `buy.count + sell.count`。
- **追问**：end 是包含的呢？闭区间，`ends[j] < s` 才算结束，`[1,3]` 与 `[3,5]` 在 3 重叠。只要全局最大，为什么扫描线更好？排序一遍 O(n log n) 就够，线段树只在要问任意时间段的最大值、或增删顺序任意时才值得。`t > now` 的预测查询为什么贵？未来的撤单还没发生，答案要重算。
- **链接**：[[hc11_order_interval_overlap|Java 讲义]] · [[hc11_order_interval_overlap_cpp|C++ 讲义]]

```java
Arrays.sort(starts, 0, n);  Arrays.sort(ends, 0, n);
int best = 0, j = 0;  long bestTime = 0;                // ends[0..j) 都已结束
for (int i = 0; i < n; i++) {
    long s = starts[i];
    while (j < n && ends[j] <= s) j++;                  // 同一时刻先结束；闭区间改成 ends[j] < s
    int live = (i + 1) - j;                             // 已开始 - 已结束
    if (live > best) { best = live; bestTime = s; }     // 严格 >：保留最早时刻
}
return new Peak(best, bestTime);
```

## hc06 · CPU 寄存器位运算

- **题意**：一个无符号 32 位寄存器，给初值和一串指令（AND / OR / XOR / NOT、SHL / SHR、ROL / ROR、SET / CLEAR / TOGGLE、POPCOUNT 等）依次执行，最后输出终值的十六进制、无符号十进制和 32 位二进制；任何格式或范围问题只输出 `Malformed Input`。例：`0xF0`，`AND 0x3C` 得 `0x30`，`SHL 4` 得 `0x300`，`OR 0x0F` 得 `0x30F`。
- **核心思路**：全部难点来自 Java 的 `int` 是有符号的补码。用 `int` 存 32 位、按位运算，只有需要无符号语义时才转 `long`（`& 0xFFFFFFFFL`）。逻辑右移用 `>>>`，不是算术右移 `>>`；移位位数 ≥ 32 要显式得 0，因为 Java 的 `<<` 只取位数的低 5 位，`x << 32 == x`；解析 `0xFFFFFFFF` 要用 long，`Integer.parseInt("FFFFFFFF", 16)` 会抛异常。指令用 `sealed Instr` 层次加 `record` 表示，`switch` 模式匹配执行；热路径追问：把程序一次解码成 `int[]`，执行循环里不分配。
- **数据结构**：一个 `int` 寄存器；`sealed Instr` 分成 `Update`（改寄存器）和 `Query`（输出一个数）；编译后的 `int[] ops` / `int[] args`；复杂度 O(指令数)。
- **Java 要点**：① `Integer.bitCount` / `numberOfTrailingZeros` / `numberOfLeadingZeros`，对 0 返回 32；② `Integer.rotateLeft` / `rotateRight` 自动对 32 取模；`Integer.compress` / `expand` / `reverse` / `reverseBytes`；③ 输出用 `"%08X".formatted(reg)` 和 `Integer.toUnsignedString(reg)`。
- **C++ 要点**：① 寄存器用 `uint32_t`：无符号回绕有定义，`>>` 就是逻辑右移，不会有符号问题；② 但 `x << 32` 是未定义行为（位数 ≥ 位宽），必须显式判断；③ 用 `std::rotl` / `rotr`、`std::popcount` / `countr_zero` / `countl_zero`（对 0 返回 32，而 `__builtin_ctz(0)` 是未定义行为）。
- **易错点**：① 用 `>>` 代替 `>>>`：寄存器最高位为 1 时 SHR 会补 1；② `1 << 31` 是负数；位号 32 与 -1 要拒绝；③ 十进制 `010` 是 10 不是八进制；`0x` 单独出现、`4294967296`、`-1` 都非法；CTZ / CLZ / POPCOUNT 在 0 和 -1 上要测。
- **追问**：换成 64 位寄存器？用 `long`、`Long.toUnsignedString`、`Long.compareUnsigned`。「找 bug」题常见什么？`>>` 代替 `>>>`、`(int)` 与 `long` 混用。为什么解码一次？热循环里无分支、无分配，移位位数提前限制到 32。
- **链接**：[[hc06_cpu_register_bitwise|Java 讲义]] · [[hc06_cpu_register_bitwise_cpp|C++ 讲义]]

```java
static int apply(int reg, Update u) {
    return switch (u) {
        case And(var m)       -> reg & m;
        case Not _            -> ~reg;
        case Shl(var n)       -> n >= 32 ? 0 : reg << n;    // Java 的 << 只取低 5 位，32 必须显式处理
        case Shr(var n)       -> n >= 32 ? 0 : reg >>> n;   // 逻辑右移用 >>>，补 0
        case Rol(var n)       -> Integer.rotateLeft(reg, n);   // 自动对 32 取模
        case SetBit(var b)    -> reg | (1 << b);
        case ClearBit(var b)  -> reg & ~(1 << b);   // Or / Xor / Ror / ToggleBit 同理
    };
}
```

## hc13 · 定长内存池

- **题意**：启动时一次备好 `capacity` 个等大的块，运行时 `allocate()` 借、`free()` 还，都是 O(1)，热路径不 `new`（分配太快会让 GC 频繁停顿，停顿直接变成延迟毛刺）。池满返回 `NONE`，不抛异常；归还返回 `FREED` / `DOUBLE_FREE` / `INVALID`。后续追加：带版本号的 handle、堆外内存、无锁并发。
- **核心思路**：空闲链表藏在一个 `int[] next` 里：块空闲时 `next[i]` 是下一个空闲块的编号，块在用时 `next[i]` 设成哨兵 `ALLOCATED`（−2），所以不用另开 `boolean[]`，一个 int 同时当「链表指针」和「是否在用」（两种状态互斥）。借 = 摘链头，还 = 插链头，最后归还的最先被再分配（LIFO，缓存友好）。只有块编号防不了「A 还了、B 借走同一块、A 又还一次」，所以 handle = 版本号（高 32 位）+ 槽位（低 32 位），偶数表示空闲、奇数表示在用，allocate 和 free 各加 1，陈旧 handle 的版本对不上。并发版是 Treiber 栈：head 是一个 long，高 32 位 tag、低 32 位栈顶，每次 CAS 成功 tag 加 1，用来对付 ABA。
- **数据结构**：`int[] next` + `head` + `available`；`int[] gens`（版本号）；堆外 `MemorySegment`，32 字节定长记录；`VarHandle` 做 CAS 的带 tag 的 head。所有操作 O(1)。
- **Java 要点**：① `handle = (long) gen << 32 | (index & 0xFFFFFFFFL)`，`& 0xFFFFFFFFL` 防止符号扩展；② 无锁用 `VarHandle.compareAndSet`，数组元素用 `MethodHandles.arrayElementVarHandle(int[].class)`；③ 堆外用 FFM 的 `Arena` / `MemorySegment` / `ValueLayout`，类实现 `AutoCloseable`；归还结果是 `FreeResult` 枚举，`switch` 表达式穷尽检查。
- **C++ 要点**：① 一块 `std::aligned_alloc(64, …)` 的对齐内存加 placement new 构造记录，`unique_ptr` 带自定义 deleter 释放（RAII，对应 `Arena.close`）；② `alignas(32)` 的槽；③ tagged head 是 `std::atomic<uint64_t>` 加 `compare_exchange_weak`，显式写 `memory_order`；next 数组元素也要是 `std::atomic`，不能裸读写；用 `is_always_lock_free` 确认无锁。
- **易错点**：① 重复归还会把同一块插进链表两次，之后一块分给两个人，必须靠哨兵拒绝；② handle 里的下标要 `& 0xFFFFFFFFL`，否则负的 int 符号扩展会污染高 32 位的版本号；③ 没有 tag 的 CAS 会被 ABA 骗过：线程 A 读到 head = X、next = Y 后被切走，B 弹出 X 和 Y 再把 X 压回，A 的 CAS 成功了，但 next 已过期。
- **追问**：为什么版本号用奇偶？并发版可以用一次 CAS 完成「在用 → 空闲」，重复归还只有一个赢家。版本号 32 位回绕怎么办？2^32 是偶数，奇偶性不变，不用特殊处理。为什么用堆外？GC 看不见它，不产生 GC 工作；代价是要手动 `close` 和自己管边界。
- **链接**：[[hc13_fixed_memory_pool|Java 讲义]] · [[hc13_fixed_memory_pool_cpp|C++ 讲义]]

```java
int allocate() {
    int block = head;
    if (block == NONE) return NONE;                     // 池满不是错误
    head = next[block];  next[block] = ALLOCATED;       // 摘链头，打上「在用」哨兵 (-2)
    available--;  return block;
}
FreeResult free(int block) {
    if (block < 0 || block >= next.length) return INVALID;
    if (next[block] != ALLOCATED) return DOUBLE_FREE;   // 不在用，说明已经还过
    next[block] = head;  head = block;  available++;    // 插链头 (LIFO)
    return FREED;
}
```

## ld01 · SPSC 共享内存通道

- **题意**：行情进程把消息交给策略进程，两个进程直接读写同一块共享内存：恰好一个写者、一个读者，有界（满了告诉写者）、不丢不重不乱序，热路径上没有锁和系统调用。写者 `finish()` 之后，读者要能区分「暂时没有」（`poll` 返回 null）和「永远没有了」（`isDrained`）。例：容量 4 的环，offer 10, 20, 30, 40 后再 offer 50 返回 false；poll 出 10 之后 offer 50 成功。
- **核心思路**：环形缓冲区，`head`（读计数）和 `tail`（写计数）只增不减，下标 = 计数 `& (cap − 1)`；空 ⇔ `tail − head == 0`，满 ⇔ 差值等于容量，不浪费槽位。每个变量只有一个写者（`tail` 归生产者，`head` 归消费者），所以不需要锁和 CAS，只需要内存序：写者先写数据，再用 release 发布 `tail`；读者 acquire 读 `tail` 之后才读数据，读完再 release 发布 `head`。弱内存序的 CPU（ARM、Apple M）上少了这对屏障，会读到新 `tail` 配旧数据。两个优化：cached index（只有按旧值看是满或空时，才去读对方的真实下标，少一次跨核缓存行传输）和填充（生产者字段与消费者字段隔开至少一条缓存行，防伪共享）。变长消息：记录 = `[len][payload]` 补齐到 8 字节；放不下连续的一整条时，先写一条 PAD 记录占满到末尾，再从头写真记录。
- **数据结构**：`long[]` 或 `MemorySegment` 环加 head / tail 计数和各自缓存的对方下标；共享内存头部是 magic / capacity / version / head / tail / closed；`FileChannel.map` 把文件映射进两个进程；容量是 2 的幂。
- **Java 要点**：① `VarHandle` 的 `setRelease` / `getAcquire`，不用锁、不用 CAS；② `MethodHandles.memorySegmentViewVarHandle(ValueLayout.JAVA_LONG)` 对段做原子访问，堆上的 `byte[]` 段不支持，要用 `Arena.ofShared().allocate(bytes, 128)`；③ `LongQueue.poll()` 空时抛 `NoSuchElementException`，因为每个 long 都可能是合法消息，没有哨兵值可用；`init` 最后才 release 写 magic，别人看到 magic 就一定看到完整头部。
- **C++ 要点**：① `std::atomic<uint64_t>` 的 `store(release)` / `load(acquire)`；② `alignas(64)` 或 128 把 head 和 tail 隔开（对应 Java 的继承加填充）；原子对象不可拷贝不可移动，所以环也不可拷贝；③ 共享内存里的字节用 C++20 的 `std::atomic_ref`，内存保持普通字节，每次访问再指定内存序；生产者保留一份私有的 tail 副本，不去读自己的原子变量。
- **易错点**：① 把 `setRelease` 改成普通写：x86 上看不出问题，ARM 上立刻读到旧数据；② PAD 没有单独发布会死锁；因此 `offer` 返回 false 时，可能已经悄悄发布了一条 PAD；③ `isDrained` 要先读 `closed` 再读 `tail`，反过来可能漏掉 close 前最后一批消息；永远放不下的消息（超过 `maxPayload`）抛 `IllegalArgumentException`，不是返回 false。
- **追问**：为什么不用锁或 CAS？每个变量只有一个写者，没有写写竞争。怎么证明伪共享存在？单独量两个线程各自自增相邻的、和相隔一条缓存行的计数器。为什么容量要 2 的幂？用 `& mask` 代替取模，更快。
- **链接**：[[ld01_spsc_channel|Java 讲义]] · [[ld01_spsc_channel_cpp|C++ 讲义]]

```java
boolean offer(long v) {                                 // 仅生产者线程
    long t = tail;                                      // 自己独占写，普通读
    if (t - cachedHead == buf.length) {                 // 按旧快照是满的，才去读真实的 head
        cachedHead = (long) HEAD.getAcquire(this);
        if (t - cachedHead == buf.length) return false;
    }
    buf[(int) (t & mask)] = v;                          // 1. 先写数据
    TAIL.setRelease(this, t + 1);                       // 2. release 发布
    return true;                                        // poll 对称：getAcquire(tail) 再读数据，最后 setRelease(head)
}
```

## ld02 · 交易相关 OOD

- **题意**：交易系统最基础的三个对象加一个装配：订单状态机（`PENDING → WORKING → PARTIALLY_FILLED → FILLED`，另有 `CANCELED`、`REJECTED`）、仓位与盈亏、交易前风控、事件溯源的 `TradingDesk`。例：买 10@100、买 10@110、卖 15@120，先平 10@100（+200）再平 5@110（+50），剩 5 手，已实现盈亏 250。
- **核心思路**：① 状态机：非法转移抛 `IllegalTransitionException` 且状态不变；`Fill` 的去重在状态检查之前（重复回报是幂等的，即使订单已 FILLED）；超量成交不能记下 `execId`，之后用合法数量重发应当成功；`openCount` / `openLeaves` 增量维护成 O(1)，因为风控每单都要调。② 仓位：队内 lot 方向相同，反向成交从队首开始平仓，每平 c 手实现 `方向 × (成交价 − lot 价) × c`；平完还有剩余就翻转，剩余部分以成交价作为新方向的第一个 lot；先只读地算出盈亏，再一次提交，溢出时仓位保持原样。③ 风控：检查顺序固定（等于 `RiskReason` 的声明顺序），同时违反多条时原因才确定；没有参考价就拒绝（fail closed）；价格带用整数交叉相乘；仓位检查看最坏情况，即所有未完成单加本单全部成交。④ 事件溯源：每个变更方法先把输入写进 journal 再处理，抛异常的输入也在 journal 里，重放时同样抛、同样被吞，状态因此逐项相同；风控拒单产生的内部 Reject 是输出，不进 journal。
- **数据结构**：`HashMap<id, 订单状态>` 加聚合计数；每个标的一个 `Deque<Lot>`；`TreeMap<symbol, Position>`（输出按字典序）；`List<DeskEvent>` journal；`sealed ExecEvent` / `DeskEvent`。
- **Java 要点**：① `record` 紧凑构造器做校验（`Order` 保证 `id`、`qty`、`px` 都大于 0）；② `sealed` 事件加穷尽 `switch`，新增事件类型时编译器会提醒漏处理；③ 价格和数量全用整数（tick、股），PnL 逐位可验，乘法用 `Math.multiplyExact`；`List.copyOf` 给出 journal 的快照。
- **C++ 要点**：① `std::variant` 加 `std::visit` 对应 sealed 加 switch；② 用 `std::deque<Lot>` 做 FIFO，`std::map` 保证输出按字典序；③ 「先验证、后修改」写成两阶段：先在局部变量里算好结果，最后一次赋值提交（强异常保证）；溢出检查用 `__builtin_mul_overflow`。
- **易错点**：① 风控检查必须在登记订单之前，否则这张单会把自己算进未完成数量；② 价格带用 `|px − ref| × 10000 ≤ ref × bps`（等于时通过）；乘积溢出算 `NOTIONAL_LIMIT`，不能回绕后放行；③ 翻转要在一笔成交里同时完成平仓和开反向仓；`PENDING` 状态收到 `Cancel` 非法；熔断时连减仓单也拒绝。
- **追问**：价格带为什么不用除法？除法有舍入，边界值会误判，交叉相乘是精确的。为什么重放得到同一个状态？状态只由输入事件决定性地推出，没有时钟和随机数。「最坏情况仓位」是什么？假设某标的所有未完成买单（或卖单）都成交后的净仓。
- **链接**：[[ld02_trading_ood|Java 讲义]] · [[ld02_trading_ood_cpp|C++ 讲义]]

```java
long dev = Math.multiplyExact(Math.abs(o.px() - ref), 10_000L);   // |px - ref| / ref <= bps / 10000
if (dev > Math.multiplyExact(ref, limits.priceBandBps()))         // 交叉相乘：没有除法，没有舍入
    return reject(RiskReason.PRICE_BAND);
// 以上在 try 里：ArithmeticException -> NOTIONAL_LIMIT，不能回绕放行
long buyLeaves  = orders.openLeaves(sym, Side.BUY)  + (o.side() == Side.BUY  ? o.qty() : 0);
long sellLeaves = orders.openLeaves(sym, Side.SELL) + (o.side() == Side.SELL ? o.qty() : 0);
long net = positions.netQty(sym);
if (net + buyLeaves > limits.maxPosition() || net - sellLeaves < -limits.maxPosition())
    return reject(RiskReason.POSITION_LIMIT);           // 最坏情况：未完成的单全部成交
```

## ld03 · 异步 TCP 消息通道

- **题意**：TCP 是可靠有序的字节流，不是消息流：两条 10 字节的消息可能合并成 20 字节被读到，也可能在消息中间被切开；`write` 可能只写进一部分；对端读得慢会产生背压；连接还会断。要在字节流上做一个有界的消息通道：`offer(msg)` 发（满了返回 false）、`poll()` 收，再加断线重连。
- **核心思路**：① 成帧：`[len:int32 大端][payload]`，增量解码器接收任意切分的字节块，凑齐一整帧才返回；非法帧头（`len < 0` 或 `> maxFrame`）在只看到 4 字节头时就报错，不等凑齐，并且粘性失败，因为流已经失去同步。② 一个 I/O 线程加一个 `Selector`：应用线程只碰两个有界缓冲区，系统调用都在 I/O 线程里；每轮按状态重新设置兴趣集，入站环有空位才监听 `OP_READ`，出站有数据才监听 `OP_WRITE`，部分写剩下的数据留在缓冲里等下次可写。③ 背压链：对端不读 → 内核发送缓冲满 → `write` 返回 0 → 出站环满 → `offer` 返回 false；应用不 `poll` → 入站环满 → 停止监听 `OP_READ` → 内核接收缓冲满 → TCP 窗口为 0 → 对端写不出去。`poll` 腾出空间后必须唤醒 I/O 线程。④ 重连：指数退避加抖动，断线期间的 pending 队列有界；已交给旧连接的消息连接断了可能丢，TCP 不保证对端应用处理了。
- **数据结构**：`ByteRing`（任意正容量，写到末尾回绕时分两段拷贝）、出站环、入站 `FrameDecoder`；`Selector`；`Backoff(initial, max, multiplier)` 封顶且不溢出；`ReconnectingClient` 的有界 pending 队列。两个环的容量都必须 ≥ `maxFrame + 4`，否则最大的消息永远放不下。
- **Java 要点**：① 非阻塞 `SocketChannel`，`Selector.select()` 睡眠、`wakeup()` 唤醒，`key.interestOps(ops)` 设置兴趣集；② `ByteBuffer` 写完要 `flip()` 才能读；`TCP_NODELAY` 必须开，关闭 Nagle，小消息不被攒着；③ `shutdownOutput()` 发 FIN 实现半关闭；备选写法是虚拟线程加阻塞 I/O。
- **C++ 要点**：① Java 的 `Selector` 对应 `poll(2)` 事件循环；② `selector.wakeup()` 对应 self-pipe（往管道写 1 字节让 `poll` 返回；macOS 没有 eventfd，所以用 pipe）；fd 包在 move-only 的 RAII 类里，析构时 `close`；③ 对已断开的连接写数据要用 `MSG_NOSIGNAL`（macOS 用 `SO_NOSIGPIPE`），否则 SIGPIPE 会杀掉进程；大端长度用移位逐字节拼，不用 `reinterpret_cast`。
- **易错点**：① `poll` 之后忘了唤醒 I/O 线程，入站读恢复不了，通道卡死；② EOF 恰好落在一帧中间说明流被截断（`EOFException`）；EOF 不等于本端关闭，之前收齐的完整帧仍可取；③ 容量恰好等于 `maxFrame + 4` 时仍要正常工作（每条消息都在环的回绕边界上被切开）；`writeAll` 全有或全无，不能留下半个帧头。
- **追问**：为什么开 `TCP_NODELAY`？Nagle 会把小包攒起来再发，增加延迟。为什么重连只能做到 at-most-once？进了旧连接缓冲的消息，连接断了就丢；要 at-least-once 得有应用层序号、确认、重传和去重。为什么退避要加抖动？避免大量客户端同时重连造成惊群。
- **链接**：[[ld03_async_tcp_channel|Java 讲义]] · [[ld03_async_tcp_channel_cpp|C++ 讲义]]

```java
int ops = 0;                                            // 每轮按状态重新声明关心的事件
if (!peerClosed && in.free() > 0) ops |= SelectionKey.OP_READ;   // 入站环满了就不读：这就是背压
if (!finSent && (wbuf.hasRemaining() || !out.isEmpty())) ops |= SelectionKey.OP_WRITE;
key.interestOps(ops);
selector.select();                                      // 睡到 socket 就绪，或有人 selector.wakeup()
// 应用线程的 offer() / poll() 改了状态之后要 wakeup()，I/O 线程才会重新计算 ops
```
