# oa03 · 解法与原理

时间点连接本质上是「归并两个有序序列」：左右两张表都按时间升序，那么一个只往前走的指针就够了，不需要回头。多品种的差别只是「最新值」从一个变量变成一张哈希表。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "For each left row I'll return the price of the latest right row whose timestamp is less than or equal to the left timestamp. Two questions: does an equal timestamp count as a match, and if there is no right row yet, should I return null or skip the row?"

面试官通常会说：相等算匹配，没有匹配就返回空值，结果和左表一一对应。再补一问：同一时刻有多条右行时取最后一条，是否可以？

## Part 1 · 单一品种，双指针

**思路**：对左表逐行处理，右表的指针 `j` 只增不减。每处理一个左行，先把所有 `ts <= left.ts` 的右行吃掉，每吃一行就更新「目前最新的 price」，然后把这个值作为这一行的结果。

**原理**：左表升序，所以下一个左行的时间不会比当前更早。已经吃掉的右行对下一个左行同样满足 `right.ts <= left.ts`，不需要重看；还没吃的右行，对当前左行来说太晚了。因此每个右行只被访问一次，每个左行只被访问一次。

**Java**

```java
public static List<OptionalLong> joinSingle(List<Left> left, List<Right> right) {
    List<OptionalLong> out = new ArrayList<>();
    OptionalLong last = OptionalLong.empty();
    int j = 0;
    for (Left l : left) {
        while (j < right.size() && right.get(j).ts() <= l.ts()) last = OptionalLong.of(right.get(j++).price());
        out.add(last);
    }
    return out;
}
```

**C++**

```cpp
inline std::vector<std::optional<long long>> join_single(const std::vector<Left>& left, const std::vector<Right>& right) {
    std::vector<std::optional<long long>> out;
    std::optional<long long> last;
    std::size_t j = 0;
    for (const Left& l : left) {
        while (j < right.size() && right[j].ts <= l.ts) last = right[j++].price;
        out.push_back(last);
    }
    return out;
}
```

复杂度：时间 O(n + m)，额外空间 O(1)（不算输出）。

## Part 2 · 多个品种，哈希表

**思路**：循环结构不变，只把「一个最新价」换成哈希表 `symbol → 最新 price`。吃右行时写入表；回答左行时，只查它自己品种的那一项，查不到就是无匹配。

**原理**：右表整体按 ts 升序，所以每个品种自己的子序列也是升序的。扫描到某一时刻，表里每个品种存的正是「该品种 ts 不晚于当前时刻的最新一行」。写入时后来的覆盖先来的，所以同一时刻有多条右行时，表里靠后的那条胜出。`<=` 保证同一时刻的右行也被吃进来，这是「at or before」里 at 的部分。

**Java**

```java
public static List<OptionalLong> join(List<Left> left, List<Right> right) {
    List<OptionalLong> out = new ArrayList<>();
    Map<String, Long> latest = new HashMap<>();
    int j = 0;
    for (Left l : left) {
        while (j < right.size() && right.get(j).ts() <= l.ts()) {
            Right r = right.get(j++);
            latest.put(r.symbol(), r.price());
        }
        Long p = latest.get(l.symbol());
        out.add(p == null ? OptionalLong.empty() : OptionalLong.of(p));
    }
    return out;
}
```

**C++**

```cpp
inline std::vector<std::optional<long long>> join(const std::vector<Left>& left, const std::vector<Right>& right) {
    std::vector<std::optional<long long>> out;
    std::unordered_map<std::string, long long> latest;
    std::size_t j = 0;
    for (const Left& l : left) {
        while (j < right.size() && right[j].ts <= l.ts) { latest[right[j].symbol] = right[j].price; ++j; }
        auto it = latest.find(l.symbol);
        out.push_back(it == latest.end() ? std::nullopt : std::optional<long long>(it->second));
    }
    return out;
}
```

复杂度：时间 O(n + m)（哈希表操作按平均 O(1) 计），空间 O(k)，k 是右表里出现过的品种数。

## Part 3 · 口头追问和回答

**1. 只接受时间差不超过 T 的匹配，怎么改？**

哈希表里不能只存 price，要连 ts 一起存：`symbol → (ts, price)`。回答左行时先查到最新右行，再判断 `left.ts - right.ts <= T`，不满足就返回无匹配。注意只检查「最新的那一条」就够了：最新的一条都太旧，更早的只会更旧。复杂度不变。

**2. 输入没有排序怎么办？**

两个办法。一是先把两张表各自按 ts 排序，再用上面的双指针，总时间 O(n log n + m log m)。二是只排序右表（并按品种分组），对每个左行在对应品种的 ts 数组里二分，找「最后一个 `ts <= left.ts` 的位置」（C++ 里是 `upper_bound` 再退一位），总时间 O(m log m + n log m)，而且左表可以保持原来的顺序，不用再还原。

**3. 流式数据，右表可能乱序到达，怎么处理？**

只维护「最新值」的哈希表在乱序时会出错：一条迟到的旧报价会覆盖更新的报价。有两种处理方式。一是写入时比较 ts，只有比表里已有的 ts 更大（或相等）才覆盖。二是引入水位线（watermark）：约定「ts 小于 W 的右行不会再来」，左行要等水位线越过它的 ts 之后才能输出，否则后到的右行可能改变它的答案。乱序容忍越大，左行等待越久、缓冲越多，这是延迟和正确性之间的取舍；水位线之后才到的数据只能丢弃，或者走单独的修正通道。

**4. pandas 的 `merge_asof`、kdb 的 `aj` 和这题是什么关系？**

是同一个操作。`pandas.merge_asof(left, right, on="ts", by="symbol")` 对左表每行取右表里 `ts` 不大于它的最近一行，`by` 就是品种分组，`tolerance` 参数就是第 1 问的时间窗口，`direction` 可选 `backward`（默认，也就是这里要的「不晚于」）、`forward` 或 `nearest`。kdb 的 `aj` 同样按若干列精确匹配、最后一列做「不晚于」匹配。两者都要求按时间排序的输入，所以可以用同样的双指针或二分实现。

**5. 为什么不直接对每个左行扫一遍右表？**

嵌套循环是 O(n × m)。行情数据动辄每张表几百万行，乘起来是万亿级，跑不完。利用「两张表都有序」这个条件，可以降到 O(n + m)；这也是面试官在看的点：你有没有用上题目给的有序性。

## 常见错误

1. 比较写成 `<`：同一时刻的右行被漏掉 → 成交和同一毫秒的报价对不上，结果偏旧。
2. 每个左行都从头扫右表，或者双指针每次回退 → 退化成 O(n × m)。
3. 多品种时只用一个「最新价」变量 → 别的品种的价格串进来。
4. 没有匹配时返回 0 → 和真实价格 0 混淆；应该返回空值（`OptionalLong` / `std::optional`）。
5. 流式场景直接用「后到者覆盖」 → 迟到的旧报价盖掉新报价。
