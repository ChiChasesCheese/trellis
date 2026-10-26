# hc08 · 解法与原理

这一题考两件事：先用最直接的结构把语义写对，再看到「前缀和加在线修改」就想到树状数组。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep orders in insertion order, with the remaining quantity per id. Before I start: does `delete` remove the whole order or only some units? If an id is deleted completely and put again, does it go to the back? And are the queries strictly before the id, not including it?"

面试官通常会说：可以只删一部分，删光后再放排到最后，查询不含自己。这三个答案决定了数据结构：「保持顺序」要求按插入顺序遍历，「减量不换位」要求改数量不改位置。

## Part 1 · 朴素版

**思路**：`LinkedHashMap<Long, Long>`（id 到剩余数量），迭代顺序就是插入顺序。先写 `put` 和 `delete`，再写一个从头扫到 `id` 的循环，累加订单数或数量。

**原理**：`LinkedHashMap` 在哈希表之外还串了一条按插入顺序的链表，所以按 id 查找是 O(1)，遍历是插入顺序。对已有的 key 调 `put(key, newValue)` 只改值，不改它在链表里的位置，所以「只减量、位置不变」自然成立；先 `remove` 再 `put` 才会排到最后，正好对应「删光再放」。查询要从头扫到 `id`，是 O(n)。

**Java**

```java
private final Map<Long, Long> orders = new LinkedHashMap<>();

public void put(long id, long qty) {
    if (qty <= 0) throw new IllegalArgumentException("invalid quantity");
    if (orders.putIfAbsent(id, qty) != null) throw new IllegalArgumentException("duplicate id");
}

public long delete(long id, long qty) {
    Long have = orders.get(id);
    if (have == null) throw new NoSuchElementException("unknown id");
    if (qty <= 0 || qty > have) throw new IllegalArgumentException("invalid quantity");
    long left = have - qty;
    if (left == 0) orders.remove(id); else orders.put(id, left);
    return left;
}

public int countBefore(long id) { return (int) scan(id, false); }
public long quantityBefore(long id) { return scan(id, true); }

private long scan(long id, boolean sumQty) {
    if (!orders.containsKey(id)) throw new NoSuchElementException("unknown id");
    long result = 0;
    for (var e : orders.entrySet()) {
        if (e.getKey() == id) break;
        result += sumQty ? e.getValue() : 1;
    }
    return result;
}
```

**C++**（用 `vector<pair>` 线性查找，面试里写得快；数据多时换成 `std::list` 加 `unordered_map`）

```cpp
std::vector<std::pair<long long, long long>> orders_;  // (id, remaining), insertion order

std::size_t index_of(long long id) const {
    for (std::size_t i = 0; i < orders_.size(); ++i)
        if (orders_[i].first == id) return i;
    throw std::out_of_range("unknown id");
}

void put(long long id, long long qty) {
    if (qty <= 0) throw std::invalid_argument("invalid quantity");
    for (auto& o : orders_) if (o.first == id) throw std::invalid_argument("duplicate id");
    orders_.emplace_back(id, qty);
}

long long del(long long id, long long qty) {
    const std::size_t i = index_of(id);
    if (qty <= 0 || qty > orders_[i].second) throw std::invalid_argument("invalid quantity");
    const long long left = orders_[i].second -= qty;
    if (left == 0) orders_.erase(orders_.begin() + static_cast<std::ptrdiff_t>(i));
    return left;
}

int count_before(long long id) const { return static_cast<int>(index_of(id)); }

long long quantity_before(long long id) const {
    const std::size_t end = index_of(id);  // find once, not once per step
    long long sum = 0;
    for (std::size_t i = 0; i < end; ++i) sum += orders_[i].second;
    return sum;
}
```

复杂度：`put`、`delete` 在 Java 版是 O(1)，C++ 的 vector 版是 O(n)（线性查找，删除还要挪元素）；两种语言的两个查询都是 O(n)。

## Part 2 · 树状数组

**思路**：给每次 `put` 分配一个递增的位置 1, 2, 3, …，订单的先后顺序就是位置的大小顺序。用两棵树状数组按位置存数据：一棵存订单数（活跃的位置上是 1），一棵存剩余数量。`countBefore(id)` 就是位置 `pos(id) - 1` 的前缀和。

**原理：树状数组怎么工作**

数组 `tree[i]` 存的是位置区间 `(i - lowbit(i), i]` 的和，其中 `lowbit(i) = i & -i` 是 `i` 二进制里最低的那个 1（例如 `lowbit(12) = 4`，`tree[12]` 管位置 9 到 12）。

- **查询前缀 `[1, i]`**：把区间拆成几块不相交的区间。`i -= i & -i` 去掉最低位，跳到前一块，每次少一个 1，最多 log2(n) 步。
- **修改位置 `i`**：把变化加到所有管着 `i` 的节点上。`i += i & -i` 跳到下一个管着它的节点，最多 log2(n) 步。
- 位置必须从 1 开始：`0 & -0 = 0`，循环会永远停在原地。

「只留洞、不回收位置」是关键：回收位置会打乱插入顺序。删光订单时只需要把它位置上的 1 减掉、数量减去剩余值，其它位置的相对顺序不变。再次 `put` 同一个 id 时拿到一个全新的、更大的位置，所以自然排到最后。代价是位置只增不减，`capacity` 要预先给定（怎么回收见 Part 3）。

查询 `pos - 1` 而不是 `pos`：题目要的是不含自己。

**Java**

```java
private final long[] cnt, sum, qty;                   // 下标 1..capacity
private final Map<Long, Integer> pos = new HashMap<>(); // 活跃订单 id -> 位置
private int next = 1;

public FastOrderSequence(int capacity) {
    cnt = new long[capacity + 1]; sum = new long[capacity + 1]; qty = new long[capacity + 1];
}

public void put(long id, long q) {
    if (q <= 0) throw new IllegalArgumentException("invalid quantity");
    if (pos.containsKey(id)) throw new IllegalArgumentException("duplicate id");
    if (next >= cnt.length) throw new IllegalStateException("out of positions");
    int i = next++;
    pos.put(id, i);
    qty[i] = q;
    add(cnt, i, 1);
    add(sum, i, q);
}

public long delete(long id, long q) {
    int i = position(id);
    if (q <= 0 || q > qty[i]) throw new IllegalArgumentException("invalid quantity");
    qty[i] -= q;
    add(sum, i, -q);
    if (qty[i] == 0) { add(cnt, i, -1); pos.remove(id); }
    return qty[i];
}

public int countBefore(long id) { return (int) prefix(cnt, position(id) - 1); }
public long quantityBefore(long id) { return prefix(sum, position(id) - 1); }

private int position(long id) {
    Integer i = pos.get(id);
    if (i == null) throw new NoSuchElementException("unknown id");
    return i;
}
private void add(long[] tree, int i, long delta) {
    for (; i < tree.length; i += i & -i) tree[i] += delta;
}
private long prefix(long[] tree, int i) {
    long r = 0;
    for (; i > 0; i -= i & -i) r += tree[i];
    return r;
}
```

**C++**

```cpp
std::vector<long long> cnt_, sum_, qty_;        // positions 1..capacity
std::unordered_map<long long, int> pos_;        // active id -> position
int next_ = 1;

explicit FastOrderSequence(int capacity) : cnt_(capacity + 1), sum_(capacity + 1), qty_(capacity + 1) {}

void put(long long id, long long qty) {
    if (qty <= 0) throw std::invalid_argument("invalid quantity");
    if (pos_.count(id)) throw std::invalid_argument("duplicate id");
    if (next_ >= static_cast<int>(cnt_.size())) throw std::logic_error("out of positions");
    int i = next_++;
    pos_[id] = i;
    qty_[i] = qty;
    add(cnt_, i, 1);
    add(sum_, i, qty);
}

long long del(long long id, long long qty) {
    int i = position(id);
    if (qty <= 0 || qty > qty_[i]) throw std::invalid_argument("invalid quantity");
    qty_[i] -= qty;
    add(sum_, i, -qty);
    if (qty_[i] == 0) { add(cnt_, i, -1); pos_.erase(id); }
    return qty_[i];
}

int count_before(long long id) const { return static_cast<int>(prefix(cnt_, position(id) - 1)); }
long long quantity_before(long long id) const { return prefix(sum_, position(id) - 1); }

// add / prefix 与 Java 版的循环相同；position 在 pos_ 里找不到时抛 std::out_of_range
```

复杂度：四个方法都是 O(log n)（哈希表查找平均 O(1)）；空间 O(capacity)。

## Part 3 · 口头追问和回答

**1. 删除只留洞、位置只增不减，内存怎么控制？压缩的摊还代价是多少？**

位置用完时做一次压缩（compaction）：按原来的顺序把活跃订单重新编号为 1, 2, …, m，再换一个新的、更小的数组，线性时间重建树状数组。重建的代价和新容量 C 成正比，是 O(C)。如果让新容量 C = 2m，压缩之后至少有 m 个空位，下一次压缩前至少发生 m 次 `put`，所以每次 `put` 分摊到的代价是 O(C / m) = O(2)，也就是 O(1)。这样内存跟着活跃订单数走，而不是跟着历史订单总数走。压缩只重排位置，不改变顺序，所以所有查询结果都不变。

**2. 为什么用树状数组而不用线段树，或者 `TreeMap`？**

需求只有「单点修改 + 前缀和」。线段树也是 O(log n)，但代码更长、常数更大；树状数组就是一个数组加 `i & -i` 的循环。`TreeMap` 能按 key 排序，但要回答「前面有几个」得是带子树大小的平衡树（order-statistic tree），标准库没有；这里的插入顺序本来就递增，位置天然有序，不需要平衡树。

**3. 总数量加起来可能超过 `long` 的范围，怎么处理？**

`put` 里先算好新的总量，用 `Math.addExact`（C++ 用 `__builtin_add_overflow`）检查，溢出就抛异常，并且在改任何状态之前抛，这样失败的调用不留下半截修改。要保证检查在修改之前，是因为树状数组的更新会改 O(log n) 个节点，改到一半才发现溢出就很难回滚。

**4. 多个线程同时 `put` 和查询，怎么办？**

最简单的是一把读写锁（`ReentrantReadWriteLock`）：查询拿读锁，`put` 和 `delete` 拿写锁，多个查询可以并行。写多的时候读写锁也会成为瓶颈，这时常见的做法是单线程处理全部写入（命令放进队列），读线程读一个不可变的快照。要强调的是：树状数组的更新会同时改很多节点，没有锁的并发读会读到一半新一半旧的和。

**5. 自己写哈希表时，为什么要先用 splitmix 之类的函数把 id 搅一遍？**

订单 id 往往是递增的整数，或者有规律的位模式。如果直接取 `id % 桶数`，规律的 id 会集中落进少数桶，冲突链变长，查找退化到 O(n)。splitmix 是一个几乎不花时间的整数混合函数（几次移位、异或和乘法），能让输出的每一位都依赖输入的所有位，id 的规律就被打散了。标准库的 `HashMap` 和 `unordered_map` 在不同实现里已经做了类似的处理，所以面试里只有被要求自己写哈希表时才需要提。

**6. 如果还要「第 k 张订单是谁」，树状数组能做吗？**

能。订单数那棵树上做「树上二分」：从最高位的步长开始往下试，如果当前位置加上这一步长后，那一块的订单数还小于剩余的 k，就整块跳过并把 k 减掉；否则不跳。把所有步长试完，得到的位置再加 1 就是第 k 张订单所在的位置，再通过「位置到 id」的数组取出 id。时间 O(log n)。要求树的大小是 2 的幂时最好写，这也是平时把 `capacity` 向上取整到 2 的幂的一个理由。

## 常见错误

1. 查询写成 `prefix(pos)` 而不是 `prefix(pos - 1)`：把订单自己也算进去了，所有结果多一个。
2. 树状数组下标从 0 开始：`i & -i` 在 0 上是 0，修改和查询的循环都不会前进。
3. 删光订单后把位置还给后面的 `put` 重用：新订单会插到旧订单的位置上，顺序不对。
4. 删除时只减数量树，忘了在订单数树里减 1：之后 `countBefore` 一直把已删除的订单算进去。
5. Java 里 `delete` 用「先 `remove` 再 `put`」更新数量：订单被排到了最后，而题目要求没删光的订单位置不变。
6. 重复 id 的检查放在状态修改之后：抛异常时对象已经被改了。
