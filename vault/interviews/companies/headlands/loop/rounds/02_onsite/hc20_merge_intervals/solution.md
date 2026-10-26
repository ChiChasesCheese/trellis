# hc20 · 解法与原理

合并区间的关键是排序：按起点排好之后，能和当前区间重叠的区间一定紧挨着，只看「上一个合并结果的终点」就够了。后面的追问都是围绕这一点：流式输入时怎么维持有序、相邻怎么算、数据太大怎么办、比较怎么不溢出。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll sort by start, then sweep once, extending the last merged interval while the next start is at most its end. Intervals are closed, so [1,3] and [3,5] overlap, but [1,2] and [3,4] do not merge. May I modify the input? Could start be greater than end?"

面试官通常会说：闭区间，`[1,2]` 和 `[3,4]` 不合并，不要改输入。

## Part 1 · 排序 + 一遍扫描

**思路**：先复制一份数组并按 start 排序；然后从左到右扫，结果列表里放着当前正在扩展的区间，遇到新区间，要么并进去，要么另起一个。

**原理**：

- 排序之后，起点是不下降的。如果下一个区间的起点都超过了当前合并区间的终点，后面所有区间的起点只会更大，也不可能再并进当前区间，所以可以放心封口。
- 并进去的条件是 `cur.start <= last.end`。因为是闭区间，相等也算重叠，这一个 `<=` 就是 `[1,3]` 和 `[3,5]` 合并的原因；如果写成 `<`，端点相碰的区间就合并不了。`[1,2]` 和 `[3,4]` 满足 `3 <= 2` 为假，自然不合并。
- 并进去时终点取 `max(last.end, cur.end)`，因为 `cur` 可能整个被 `last` 包住（`[1,10]` 和 `[2,3]`），不能直接用 `cur.end`。
- 另起一个新区间时要复制一份，否则改结果会改到输入。排序前先 `clone` 外层数组，是为了不改变传入数组的顺序。

**Java**

```java
public static int[][] merge(int[][] intervals) {
    for (int[] iv : intervals) check(iv);
    int[][] sorted = intervals.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> out = new ArrayList<>();
    for (int[] cur : sorted) {
        if (!out.isEmpty() && cur[0] <= out.get(out.size() - 1)[1]) {
            int[] last = out.get(out.size() - 1);
            last[1] = Math.max(last[1], cur[1]);
        } else {
            out.add(new int[] {cur[0], cur[1]});
        }
    }
    return out.toArray(new int[0][]);
}

private static void check(int[] iv) {
    if (iv[0] > iv[1]) throw new IllegalArgumentException("start > end: " + Arrays.toString(iv));
}
```

**C++**

```cpp
inline void check(const Interval& iv) {
    if (iv[0] > iv[1]) throw std::invalid_argument("start > end");
}

inline std::vector<Interval> merge(const std::vector<Interval>& intervals) {
    for (const Interval& iv : intervals) check(iv);
    std::vector<Interval> sorted = intervals;
    std::sort(sorted.begin(), sorted.end(), [](const Interval& a, const Interval& b) { return a[0] < b[0]; });
    std::vector<Interval> out;
    for (const Interval& cur : sorted) {
        if (!out.empty() && cur[0] <= out.back()[1])
            out.back()[1] = std::max(out.back()[1], cur[1]);
        else
            out.push_back(cur);
    }
    return out;
}
```

复杂度：时间 O(n log n)（排序占主要部分，扫描是 O(n)），额外空间 O(n)。

## Part 2 · 插入一个新区间

**思路**：把 `merged` 分成三段，一个下标 `i` 从左扫到右：先把完全在 `added` 左边的区间原样放进结果；再把所有和 `added` 重叠的区间吞进 `added`（扩大它的起点和终点）；吞完后放入 `added`，最后把剩下完全在右边的区间原样放进结果。

**原理**：

- 因为 `merged` 已经有序且互不重叠，区间按 start 和 end 都是递增的。所以「完全在左边」（`end < added.start`）的是一段前缀，「重叠」的是紧接着的一段，其余在右边。三段之间不会交错，一遍扫描足够，不用排序。
- 重叠的判断是 `merged[i].start <= added.end`（已经排除了在左边的，所以只需要看右边界）。同样因为是闭区间，这里要用 `<=`，端点相碰就会合并：`[1,2]`、`[5,6]` 插入 `[2,5]` 得到 `[1,6]`。
- 吞进来的区间会让 `added` 变大，可能碰到更后面的区间，所以循环里用更新后的 `end` 继续判断。

**Java**

```java
public static int[][] insert(int[][] merged, int[] added) {
    check(added);
    List<int[]> out = new ArrayList<>();
    int i = 0, n = merged.length, start = added[0], end = added[1];
    while (i < n && merged[i][1] < start) out.add(merged[i++].clone());
    while (i < n && merged[i][0] <= end) {
        start = Math.min(start, merged[i][0]);
        end = Math.max(end, merged[i][1]);
        i++;
    }
    out.add(new int[] {start, end});
    while (i < n) out.add(merged[i++].clone());
    return out.toArray(new int[0][]);
}
```

**C++**

```cpp
inline std::vector<Interval> insert(const std::vector<Interval>& merged, const Interval& added) {
    check(added);
    std::vector<Interval> out;
    std::size_t i = 0, n = merged.size();
    int start = added[0], end = added[1];
    while (i < n && merged[i][1] < start) out.push_back(merged[i++]);
    while (i < n && merged[i][0] <= end) {
        start = std::min(start, merged[i][0]);
        end = std::max(end, merged[i][1]);
        ++i;
    }
    out.push_back({start, end});
    while (i < n) out.push_back(merged[i++]);
    return out;
}
```

复杂度：时间 O(n)，空间 O(n)（结果列表）。

## Part 3 · 口头追问和回答

**1. 区间一个一个流进来怎么办？**

用一棵有序映射（Java 的 `TreeMap`，C++ 的 `std::map`），键是 start，值是 end，里面始终存放互不重叠的合并结果。插入 `[s, e]` 时：先找起点不超过 `s` 的最后一个区间（`floorEntry`），如果它的终点 `>= s`，就把它并进来，新起点取它的起点；然后反复取起点不超过 `e` 的下一个区间（从 `s` 之后开始），并进来、从映射里删掉；最后把合并后的区间放回去。每个区间最多被插入一次、删除一次，所以平均每次插入 O(log n)；查询当前合并结果，按键遍历即可。

**2. 整数区间 `[1,2]` 和 `[3,4]` 要不要合并？**

看题目怎么定义。按「共用的点」来算，它们不重叠，不合并，开头约定的就是这样；按「覆盖的整数」来算，合起来覆盖 1、2、3、4，可以合并成 `[1,4]`，这时条件改成 `cur.start <= last.end + 1`。但是 `last.end` 等于 `Integer.MAX_VALUE` 时 `+ 1` 会溢出，所以先转成 `long` 再比较：`(long) cur.start <= (long) last.end + 1`。开场就要问清楚用哪种。

**3. 数据大到内存放不下怎么办？**

做外部排序（external sort）：把输入切成内存放得下的块，每块在内存里排序后写成一个有序的文件（run）；然后对这些文件做多路归并（k-way merge），用一个小顶堆每次取出起点最小的区间。归并输出本身就是按起点有序的，所以可以边归并边做 Part 1 的扫描：只需要记住「当前正在扩展的那一个区间」，合并结果直接写出去，不必把所有区间同时放在内存里。

**4. 为什么不能写 `a[0] - b[0]` 做比较？**

两个 `int` 相减可能溢出。比如 `a[0] = Integer.MAX_VALUE`、`b[0] = Integer.MIN_VALUE`，差值放不进 `int`，回绕成负数，排序顺序就错了，而且结果不稳定，有时甚至让排序抛异常。用 `Integer.compare(a[0], b[0])`（Java）或 `a[0] < b[0]`（C++）就没有这个问题。测试里专门放了端点是最小值和最大值的用例。

**5. 为什么 Part 2 不需要排序？**

因为输入已经有序且互不重叠，区间的起点和终点都是单调递增的，所以和 `added` 重叠的区间必然是连续的一段，一遍扫描就能找到。排序是 O(n log n)，一遍扫描是 O(n)。如果想更快地定位，可以用二分在 `merged` 里找这一段的两端，查找 O(log n)，但是生成新列表仍然要复制，整体还是 O(n)；只有在可以原地修改一个平衡树（见追问 1）时，插入才能做到 O(log n)。

## 常见错误

1. 用 `<` 判断重叠：端点相碰的区间（`[1,3]`、`[3,5]`）没有合并。
2. 并进去时直接令 `last.end = cur.end`：`cur` 被包住时终点反而变小，`[1,10]`、`[2,3]` 变成 `[1,3]`。
3. 没有复制就修改：直接改传入的区间，调用者的数据被悄悄改掉。
4. 排序比较器写成 `a[0] - b[0]`：端点接近 `int` 的上下限时溢出，排序出错。
5. Part 2 里把「完全在左边」写成 `merged[i][0] < start`（比较起点）：起点在 `added` 之前、终点却伸进 `added` 的区间被当成左边的，没有合并。应该比较终点：`merged[i][1] < start`。
