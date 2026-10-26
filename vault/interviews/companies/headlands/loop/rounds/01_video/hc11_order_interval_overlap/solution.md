# hc11 · 解法与原理

最大重叠的核心是扫描线：活跃数只在区间的端点处变化，所以只要把端点排好序，扫一遍就能数出每个时刻的活跃数。难点是同一时刻先处理结束还是先处理开始；后面的撤单和买卖方向，都只是在扫描线之前先把订单换成正确的区间。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll turn each interval into a +1 event at its start and a -1 event at its end, sort the events, and keep a running count. Before I start: is the end inclusive, so do `[1,3]` and `[3,5]` overlap? Can the input be unsorted? Can the timestamps be very large?"

面试官通常会说：先按左闭右开，输入可能乱序，时间可能很大。问出这三点，说明你知道坑在端点上。

## Part 1 · 最大重叠

**思路**：每个区间产生两个事件：`(start, +1)` 和 `(end, -1)`。把所有事件按（时间，增量）排序，同一时刻 `-1` 排在 `+1` 前面。然后扫一遍，累加增量，记录累加值出现过的最大值。

**原理：为什么同一时刻要先结束再开始**

区间是 `[start, end)`：在 `end` 那一刻，旧订单已经不活了；在 `start` 那一刻，新订单已经活了。如果 `[1,3)` 和 `[3,5)` 在 t=3 先处理开始，计数会短暂变成 2，答案就错了。所以 t=3 这一刻必须先 `-1` 再 `+1`。把增量作为排序的第二个关键字，`-1 < +1`，天然满足这一条。

如果面试官说 end 是包含的（`[1,3]` 和 `[3,5]` 重叠），把顺序反过来：同一时刻先 `+1` 再 `-1`，也就是第二关键字降序。

**原理：为什么时间只比较、不做减法**

时间可以接近 `Long.MAX_VALUE`，`end - start` 之类的运算会溢出。排序只需要比较，Java 里用 `comparingLong`，不要写 `(int)(a - b)` 这种比较器。

**Java**

```java
public static int maxOverlap(long[][] intervals) {
    List<long[]> events = new ArrayList<>();  // {时间, +1 开始 / -1 结束}
    for (long[] iv : intervals) {
        if (iv[1] < iv[0]) throw new IllegalArgumentException("end < start");
        if (iv[0] == iv[1]) continue;
        events.add(new long[] {iv[0], +1});
        events.add(new long[] {iv[1], -1});
    }
    // 同一时刻 -1 排在 +1 前面：先结束再开始，[1,3) 和 [3,5) 不重叠
    events.sort(Comparator.<long[]>comparingLong(e -> e[0]).thenComparingLong(e -> e[1]));
    int cur = 0, best = 0;
    for (long[] e : events) {
        cur += (int) e[1];
        best = Math.max(best, cur);
    }
    return best;
}
```

**C++**

```cpp
inline int max_overlap(const std::vector<std::pair<long long, long long>>& intervals) {
    std::vector<std::pair<long long, int>> events;  // (时间, +1 开始 / -1 结束)
    for (const auto& [s, e] : intervals) {
        if (e < s) throw std::invalid_argument("end < start");
        if (s == e) continue;
        events.push_back({s, +1});
        events.push_back({e, -1});
    }
    std::sort(events.begin(), events.end());  // 同一时刻 -1 排在 +1 前面
    int cur = 0, best = 0;
    for (const auto& ev : events) {
        cur += ev.second;
        best = std::max(best, cur);
    }
    return best;
}
```

C++ 的 `pair` 默认先比第一个元素再比第二个，`-1 < +1`，所以直接 `sort` 就是想要的顺序。

复杂度：排序 O(n log n)，扫描 O(n)，额外空间 O(n)。

## Part 2 · 买 / 卖方向 + 撤单

**思路**：撤单是一个业务词，翻译成区间就是「把 `end` 改小」：有效区间是 `[start, min(end, 撤单时间))`。先对每张订单算出有效区间，如果它不是空的（`有效 end > start`），就按方向放进买或卖的列表。最后对两个列表分别调用 Part 1。

**原理：为什么不用重新写一遍扫描线**

两个方向互不影响：买方的重叠只数买单，卖方的只数卖单。所以「分组 + 调用 Part 1」和「扫描线里按方向各记一个计数」等价，而且代码更短，Part 1 的正确性也直接继承下来。买方峰值和卖方峰值可以出现在不同的时刻，所以两个数不能相加当作总重叠。

**原理：撤单的边界**

- 撤单时间 `<= start`：有效区间为空，订单从没活过，不进任何一组。
- 撤单时间 `>= end`：`min(end, 撤单时间)` 还是 `end`，没有影响。
- 撤单的下标不存在，是调用方的错，要报错，不能悄悄忽略。

**Java**

```java
public static int[] maxOverlapBySide(List<Order> orders, Map<Integer, Long> cancelAt) {
    for (int id : cancelAt.keySet())
        if (id < 0 || id >= orders.size()) throw new IllegalArgumentException("unknown order " + id);
    List<List<long[]>> bySide = List.of(new ArrayList<>(), new ArrayList<>());
    for (int i = 0; i < orders.size(); i++) {
        Order o = orders.get(i);
        if (o.end() < o.start()) throw new IllegalArgumentException("end < start");
        long end = Math.min(o.end(), cancelAt.getOrDefault(i, Long.MAX_VALUE));  // 撤单把区间截短
        if (end > o.start()) bySide.get(o.side().ordinal()).add(new long[] {o.start(), end});
    }
    return new int[] {maxOverlap(bySide.get(0).toArray(new long[0][])), maxOverlap(bySide.get(1).toArray(new long[0][]))};
}
```

**C++**

```cpp
inline std::pair<int, int> max_overlap_by_side(const std::vector<Order>& orders, const std::map<int, long long>& cancel_at) {
    for (const auto& kv : cancel_at)
        if (kv.first < 0 || kv.first >= static_cast<int>(orders.size())) throw std::invalid_argument("unknown order");
    std::vector<std::pair<long long, long long>> by_side[2];
    for (int i = 0; i < static_cast<int>(orders.size()); ++i) {
        const Order& o = orders[i];
        if (o.end < o.start) throw std::invalid_argument("end < start");
        auto it = cancel_at.find(i);
        const long long end = it == cancel_at.end() ? o.end : std::min(o.end, it->second);  // 撤单把区间截短
        if (end > o.start) by_side[static_cast<int>(o.side)].push_back({o.start, end});
    }
    return {max_overlap(by_side[0]), max_overlap(by_side[1])};
}
```

复杂度：O(n log n) 时间，O(n) 额外空间。

## Part 3 · 口头追问和回答

**1. 如果 end 是包含的，怎么改？**

`[1,3]` 和 `[3,5]` 在 t=3 都活着，所以同一时刻要先处理开始、再处理结束。做法是把排序的第二关键字反过来（`+1` 在前），或者把每个 `end` 改成 `end + 1` 后仍按半开区间处理。后一种做法在 `end` 接近 `Long.MAX_VALUE` 时 `end + 1` 会溢出，所以前一种更稳。

**2. 同一时刻 `+1` 和 `-1` 的先后不管，会出什么错？**

结果取决于排序的实现细节。如果 `+1` 排在前面，`[1,3)` 和 `[3,5)` 会被数成重叠 2，答案偏大；对包含端点的约定，顺序反过来才错。这种错只出现在首尾相接的数据上，普通例子都能过，所以面试官爱考。

**3. 订单和撤单实时到达，随时回答「到现在为止最大重叠」，怎么做？**

维护当前活跃数和历史最大值。新订单到达，活跃数加一；订单自然结束，需要一个按 `end` 排序的最小堆，时间推进时把已经结束的弹出并减一；撤单时把这张订单的 `end` 提前（先从堆里删掉旧的，用有序集合比较方便）。难点是同一时间戳内的事件：先 `place` 再 `cancel` 同一张订单，这张订单的区间是空的，历史最大值不能被那一瞬间的计数污染，所以最大值要等这个时间戳处理完才算数。

**4. 时间戳高达 10^18，还要任意顺序加入、撤销区间，并查询某个时间段内的最大重叠，怎么做？**

用坐标压缩（coordinate compression）加线段树（segment tree）。活跃数只在端点处变化，把所有出现过的端点排序去重，相邻端点之间是一个「基本段」，段内活跃数是常数。区间 `[s, e)` 对应一段连续的基本段，于是问题变成：对下标区间加 1 或减 1，查下标区间的最大值。带懒标记（lazy propagation）的线段树每次操作 O(log m)，m 是不同端点数。需要事先知道所有端点；端点事先不知道的话要用动态开点或平衡树。

**5. 每张订单有数量，求同一时刻在簿的最大总量，怎么改？**

把 `+1` 和 `-1` 换成 `+数量` 和 `-数量`，其余不变。累加值用 `long`，并且要考虑数量之和溢出（用 `Math.addExact`）。

**6. 只要全局最大重叠，为什么扫描线比线段树好？**

扫描线 O(n log n)，只是一次排序加一次扫描，代码十来行，没有额外结构。线段树也是 O(n log n)，但要先压缩坐标，代码多很多，常数也大。线段树的价值在于**需要在线更新**和**查询任意时间段的最大值**，这两件事扫描线做不到。

## 常见错误

1. 排序只按时间，不管同一时刻的先后：首尾相接的区间被数成重叠。
2. 用 `Integer` 或 `int` 存时间，或者用 `a - b` 比较：时间大了溢出，排序顺序错乱。
3. 不过滤 `start == end` 的空区间，也不处理撤单时间 `<= start`：数出从没活过的订单。
4. 撤单当成「删掉这张订单」：撤单时间之前它是活着的，应该是把 `end` 改小。
5. 把买方峰值和卖方峰值相加当作总重叠：两个峰值可能出现在不同的时刻。
