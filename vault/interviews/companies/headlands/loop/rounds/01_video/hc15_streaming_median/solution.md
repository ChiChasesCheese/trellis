# hc15 · 解法与原理

两个堆是教科书做法，几分钟能写完；难点在 Part 2，要想到「堆删不了旧数据」并换成有序容器。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep the smaller half in a max-heap and the larger half in a min-heap, so the median is always at a heap top. For an even count, do you want the lower median, the upper one, or the average? Prices are integer ticks, right? And what should `median()` do when there is no data?"

面试官通常会说：偶数个取下中位数，价格是整数，没数据抛异常。

## Part 1 · 两个堆

**思路**：`lo` 是大顶堆，存较小的一半；`hi` 是小顶堆，存较大的一半。新价格不大于 `lo` 的堆顶就进 `lo`，否则进 `hi`；然后调整个数，使 `lo` 的个数等于 `hi` 的个数，或者比它多一个。

**原理：为什么中位数在 `lo` 的堆顶**

`lo` 里所有数都不大于 `hi` 里所有数，所以把两个堆接起来就是有序序列，分界线在中间。`lo` 的个数是 `⌈n/2⌉`，它的最大值正好是排序后第 `⌈n/2⌉` 小的数，也就是下中位数。取堆顶 O(1)；加入一个数最多做一次入堆、一次出堆再入堆，O(log n)。

**Java**

```java
private final PriorityQueue<Long> lo = new PriorityQueue<>(Collections.reverseOrder());
private final PriorityQueue<Long> hi = new PriorityQueue<>();

public void add(long price) {
    if (lo.isEmpty() || price <= lo.peek()) lo.add(price); else hi.add(price);
    if (lo.size() > hi.size() + 1) hi.add(lo.poll());
    else if (hi.size() > lo.size()) lo.add(hi.poll());
}

public long median() {
    if (lo.isEmpty()) throw new NoSuchElementException("no data");
    return lo.peek();
}
```

**C++**

```cpp
std::priority_queue<long long> lo_;
std::priority_queue<long long, std::vector<long long>, std::greater<>> hi_;

void add(long long price) {
    if (lo_.empty() || price <= lo_.top()) lo_.push(price); else hi_.push(price);
    if (lo_.size() > hi_.size() + 1) { hi_.push(lo_.top()); lo_.pop(); }
    else if (hi_.size() > lo_.size()) { lo_.push(hi_.top()); hi_.pop(); }
}

long long median() const {
    if (lo_.empty()) throw std::out_of_range("no data");
    return lo_.top();
}
```

复杂度：`add` O(log n)，`median` O(1)，空间 O(n)。

## Part 2 · 最近 k 笔的中位数

**思路**：同样分成「较小的一半」和「较大的一半」，但这次两半都用有序容器（能找到并删除任意一个元素）。另有一个队列按到达顺序记着窗口里的价格。每次加入：先放进合适的一半；窗口超过 k 笔就从队头取出最老的价格，从它所在的那一半里删一个；最后把两半重新平衡。

**原理：为什么要换结构**

堆只能高效地删堆顶，删中间的元素是 O(n)。有序容器（红黑树）删任意元素是 O(log k)。所以 Part 2 用 `multiset`（C++）或带计数的 `TreeMap`（Java，价格 → 出现次数）。

**原理：删的时候该看哪一半**

不变量是 `lo` 里的最大值不大于 `hi` 里的最小值。离开的价格 `old`：如果 `old <= lo` 的最大值，它在 `lo` 里（`old` 等于分界值时 `lo` 里一定有一份，因为分界值就是 `lo` 里的最大值）；否则它在 `hi` 里。

**坑：重复价格**

C++ 里 `multiset::erase(value)` 会把所有相等的元素全删掉，必须 `erase(find(value))` 只删一个。Java 里把计数减一，减到 0 时要把 key 删掉，否则 `lastKey()` 会返回一个已经不存在的价格。`loN` / `hiN` 要记元素个数，而不是 key 的个数，用 `size()` 会在有重复时算错。

**Java**

```java
private final int k;
private final Deque<Long> window = new ArrayDeque<>();
private final TreeMap<Long, Integer> lo = new TreeMap<>(), hi = new TreeMap<>();
private int loN, hiN;  // 元素个数（含重复）

private static void put(TreeMap<Long, Integer> m, long x) { m.merge(x, 1, Integer::sum); }
private static void take(TreeMap<Long, Integer> m, long x) { m.merge(x, -1, (a, b) -> a + b == 0 ? null : a + b); }

public void add(long price) {
    window.addLast(price);
    if (loN == 0 || price <= lo.lastKey()) { put(lo, price); loN++; } else { put(hi, price); hiN++; }
    if (window.size() > k) {
        long old = window.pollFirst();
        if (old <= lo.lastKey()) { take(lo, old); loN--; } else { take(hi, old); hiN--; }
    }
    while (loN > hiN + 1) { long m = lo.lastKey(); take(lo, m); loN--; put(hi, m); hiN++; }
    while (hiN > loN)     { long m = hi.firstKey(); take(hi, m); hiN--; put(lo, m); loN++; }
}

public long median() {
    if (loN == 0) throw new NoSuchElementException("no data");
    return lo.lastKey();
}
```

`take` 里 `merge` 的函数返回 `null` 表示删掉这个 key。构造函数里检查 `k < 1`。

**C++**

```cpp
size_t k_;
std::deque<long long> window_;
std::multiset<long long> lo_, hi_;

void add(long long price) {
    window_.push_back(price);
    if (lo_.empty() || price <= *lo_.rbegin()) lo_.insert(price); else hi_.insert(price);
    if (window_.size() > k_) {
        long long old = window_.front();
        window_.pop_front();
        if (old <= *lo_.rbegin()) lo_.erase(lo_.find(old)); else hi_.erase(hi_.find(old));  // 只删一个
    }
    while (lo_.size() > hi_.size() + 1) { auto it = std::prev(lo_.end()); hi_.insert(*it); lo_.erase(it); }
    while (hi_.size() > lo_.size()) { auto it = hi_.begin(); lo_.insert(*it); hi_.erase(it); }
}

long long median() const {
    if (lo_.empty()) throw std::out_of_range("no data");
    return *lo_.rbegin();
}
```

复杂度：`add` O(log k)，`median` O(1)，空间 O(k)。

## Part 3 · 口头追问和回答

**1. 为什么中位数能用「一个大顶堆 + 一个小顶堆」？**

见 Part 1 的原理：两个堆接起来就是有序序列，大顶堆的堆顶是前一半的最大值，正好卡在中间。每次加入后用一次堆间搬运恢复个数关系。

**2. 滑动窗口为什么不继续用堆？惰性删除是什么？**

堆不能快速删除任意元素。惰性删除的做法：离开窗口的价格先不删，只在一个「待删」计数表里记一笔；等它浮到堆顶时再弹出。这样可以只用堆，但要同时维护两个堆的「有效个数」，还要在每次取堆顶前先清理，代码比有序容器长，而且堆里会暂时留着已经离开窗口的数。面试里写 `multiset` 或 `TreeMap` 更短，也更不容易错。

**3. 任意百分位（比如 P95）怎么做？**

用最近秩法：n 个数的 p% 分位是排序后第 `⌈p·n/100⌉` 小的数。p 固定时，仍然是两个堆，只是两个堆的个数比例不是 1:1 而是 p:(100-p)，每次加入后调整。p 在查询时才给，就需要能回答「第 r 小」的结构：顺序统计树（order-statistic tree，每个结点记子树大小）或树状数组（Fenwick tree，见下一问）。标准库的 `std::multiset` 和 `TreeMap` 不能按下标取第 r 个，需要自己实现或换结构。

**4. 价格在一个已知的小范围里时，有没有更简单的做法？**

有。价格是 `0..T` 的整数 tick 时，开一个长度 T+1 的计数数组：`add` 是 `count[p]++`。要找第 r 小，从小到大累加计数，累加到 r 时的下标就是答案，单次 O(T)；T 较大时在计数数组上建树状数组，加入和查第 r 小都是 O(log T)，内存固定、没有分配。限制是价格必须有界，而且 T 不能大到数组放不下。

**5. 一百万次操作要多久？**

Part 1 每次 O(log n)，一百万次加入总共 O(10^6 × log n)，n 最大一百万，log 约 20，是一两千万次比较的量级，Java 和 C++ 都跑得很快。Part 2 的 `TreeMap` / `multiset` 每次插入分配一个结点，常数更大，但复杂度是 O(log k)，同一个量级。如果需要更快，价格有界时用第 4 问的数组。面试里说出复杂度和常数的来源即可，不要凭印象报具体的秒数。

**6. 偶数个时想要真正的平均数怎么办？会不会溢出？**

返回两个中间值的和（即中位数的两倍），让调用方决定怎么除，这样没有舍入问题。两个 `long` 相加可能溢出：Java 用 `Math.addExact`，C++ 用 `__builtin_add_overflow`。不要先除以 2 再相加：负数的整数除法向零取整，容易差 1。

## 常见错误

1. 没数据时直接取堆顶：Java 的 `peek()` 返回 `null`，拆箱成 `long` 时 `NullPointerException`。
2. C++ 用 `multiset::erase(value)`：把窗口里所有相等的价格一起删了，中位数错。
3. Java 的 `TreeMap` 计数减到 0 不删 key：`lastKey()` 返回已经离开窗口的价格。
4. 用 `lo.size()` 而不是元素个数来平衡：有重复价格时两半个数不对。
5. 平衡只做一次 `if` 而不是循环（Part 2）：加入和删除各让一半多出一个，一次搬运不够。
6. 偶数个时返回两个中间值的 `(a + b) / 2`：整数除法丢掉小数，大数相加还会溢出。
