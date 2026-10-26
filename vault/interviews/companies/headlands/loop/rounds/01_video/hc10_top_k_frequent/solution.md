# hc10 · 解法与原理

核心是「先数，再选」：数次数用哈希表，选前 k 个有三种办法，堆、分桶、快速选择。面试官看的是你能不能说清为什么选这一种，以及数据变大之后怎么办。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll count occurrences with a hash map, then keep the best k in a min-heap of size k so the worst of them is always on top. That's O(n + d log k) where d is the number of distinct values. Before I start: is k always valid, and how should I order the result when two values have the same count?"

面试官通常会说：k 合法，先按次数从多到少，次数相同的随意或者值小的在前。你主动把次数相同时的顺序定下来，测试就是确定的。

## Part 1 · 哈希表 + 大小为 k 的最小堆

**思路**：第一步，遍历数组，用哈希表记下每个值的次数。第二步，遍历哈希表，把（值，次数）放进堆；堆超过 k 个就弹出堆顶。最后堆里剩下的就是前 k 名。

**原理：为什么是最小堆，而不是最大堆**

我们要留下最好的 k 个，所以每次要踢掉的是当前 k+1 个里最差的那个，最差的放在堆顶才能 O(log k) 弹出。如果用最大堆，要先把全部 d 个不同值放进去再弹 k 次，是 O(d log d)。大小为 k 的最小堆让每次操作只有 O(log k)，总共 O(n + d log k)；k 比 d 小很多时，这比排序整个哈希表快。

「最差」要和输出顺序一致：次数少的更差；次数相同时，值大的更差（因为值小的要排前面）。最后弹出堆的顺序是从最差到最好，所以结果数组从末尾往前填。

**Java**

```java
public static int[] topKHeap(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    for (int x : nums) cnt.merge(x, 1, Integer::sum);
    if (k < 1 || k > cnt.size()) throw new IllegalArgumentException("k out of range: " + k);
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[1] != b[1] ? Integer.compare(a[1], b[1]) : Integer.compare(b[0], a[0]));
    for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
        heap.add(new int[] {e.getKey(), e.getValue()});
        if (heap.size() > k) heap.poll();
    }
    int[] result = new int[k];
    for (int i = k - 1; i >= 0; i--) result[i] = heap.poll()[0];
    return result;
}
```

**C++**

```cpp
inline std::vector<int> top_k_heap(const std::vector<int>& nums, int k) {
    std::unordered_map<int, int> cnt;
    for (int x : nums) ++cnt[x];
    if (k < 1 || k > static_cast<int>(cnt.size())) throw std::invalid_argument("k out of range");
    using Item = std::pair<int, int>;  // (count, value)
    auto better = [](const Item& a, const Item& b) { return a.first != b.first ? a.first > b.first : a.second < b.second; };
    std::priority_queue<Item, std::vector<Item>, decltype(better)> heap(better);
    for (const auto& [value, c] : cnt) {
        heap.push({c, value});
        if (static_cast<int>(heap.size()) > k) heap.pop();
    }
    std::vector<int> result(k);
    for (int i = k - 1; i >= 0; --i) { result[i] = heap.top().second; heap.pop(); }
    return result;
}
```

C++ 的 `priority_queue` 默认把「最大」的放在堆顶；`better(a, b)` 表示 a 排在 b 前面，把它当作「小于」传进去，堆顶就是排名最靠后的，也就是最差的。

复杂度：时间 O(n + d log k)，空间 O(d)。

## Part 2 · 按出现次数分桶

**思路**：次数最多是 n，所以开 n + 1 个桶，桶 f 放所有恰好出现 f 次的值。从 f = n 往下走，把桶里的值依次放进结果，放满 k 个就停。

**原理：为什么能到 O(n)**

堆做的是比较排序，每个元素 O(log k)。但这里要排序的键是「次数」，取值范围只有 1 到 n，是小整数，可以直接当数组下标：计数完成后，把值放进对应的桶，遍历所有桶只要 O(n)，不需要比较。

一个要诚实说明的细节：题目要求「次数相同时值小的在前」，桶内要排序。最坏情况是 d 个不同值次数都相同，这时所有值挤在一个桶里，排序是 O(d log d)。如果题目允许次数相同时任意顺序，桶内不用排，整体才是严格的 O(n)。另外分桶需要 O(n) 的额外空间，堆只需要 O(d + k)。

**Java**

```java
public static int[] topKBucket(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    for (int x : nums) cnt.merge(x, 1, Integer::sum);
    if (k < 1 || k > cnt.size()) throw new IllegalArgumentException("k out of range: " + k);
    List<List<Integer>> bucket = new ArrayList<>();
    for (int f = 0; f <= nums.length; f++) bucket.add(new ArrayList<>());
    for (Map.Entry<Integer, Integer> e : cnt.entrySet()) bucket.get(e.getValue()).add(e.getKey());
    int[] result = new int[k];
    int n = 0;
    for (int f = nums.length; f >= 1 && n < k; f--) {
        Collections.sort(bucket.get(f));
        for (int v : bucket.get(f)) if (n < k) result[n++] = v;
    }
    return result;
}
```

**C++**

```cpp
inline std::vector<int> top_k_bucket(const std::vector<int>& nums, int k) {
    std::unordered_map<int, int> cnt;
    for (int x : nums) ++cnt[x];
    if (k < 1 || k > static_cast<int>(cnt.size())) throw std::invalid_argument("k out of range");
    std::vector<std::vector<int>> bucket(nums.size() + 1);
    for (const auto& [value, c] : cnt) bucket[c].push_back(value);
    std::vector<int> result;
    for (std::size_t f = nums.size(); f >= 1 && static_cast<int>(result.size()) < k; --f) {
        std::sort(bucket[f].begin(), bucket[f].end());
        for (int v : bucket[f]) if (static_cast<int>(result.size()) < k) result.push_back(v);
    }
    return result;
}
```

复杂度：时间 O(n)（不计桶内排序），空间 O(n)。

## Part 3 · 口头追问和回答

**1. 数据流太大，哈希表放不下内存怎么办？**

如果可以接受近似，就只保留一个固定大小的数据结构，不再给每个不同的值存一个计数。常用两种：Count-Min 草图用来估计任意值的次数，Space-Saving 直接维护一份「可能的高频元素」。如果必须精确，就把数据按哈希分成 P 份写到磁盘，同一个值一定落进同一份，每份单独在内存里数，各自留下前 k，再合并。

**2. Count-Min 草图怎么工作？**

它是 d 行 w 列的计数器表，每一行有一个独立的哈希函数。来一个值，每一行都在它哈希到的那一列加 1。查询一个值的次数时，取 d 行里对应计数器的**最小值**。不同的值可能哈希到同一格，所以每个计数器只会比真实次数大，不会小；取最小值是为了挑出被别人污染得最少的那一行。因此估计值永远不小于真实值，只会偏大。标准结论：取 w = ⌈e / ε⌉ 列、d = ⌈ln(1 / δ)⌉ 行，估计值至多比真实值多 ε·N（N 是总元素数），出错的概率不超过 δ。找前 k 时，配一个大小为 k 的堆，每来一个值就更新草图并用估计值更新堆。

**3. Space-Saving 怎么只用 m 个计数器？**

只保留 m 个（值，计数）。来一个值：如果已经被跟踪，计数加 1；如果没被跟踪而且还有空位，加进来，计数为 1；如果没有空位，就替换掉当前计数最小的那个，新值的计数设为「被替换者的计数 + 1」。这样每个计数都不会低估，高估量不会超过 N / m，所以真实次数大于 N / m 的值一定在表里。

**4. 分布式：每台机器算本地前 k 再合并，为什么不对？**

因为一个值可能在每台机器上都不是前 k，但加起来是全局第一。例子：k = 1，机器 1 里 a 出现 10 次、b 出现 9 次；机器 2 里 c 出现 10 次、b 出现 9 次。本地前 1 分别是 a 和 c，b 被丢掉了，但全局 b 出现 18 次，a 和 c 都是 10 次，b 才是第一。正确做法有两种：按值的哈希把数据分发到各台机器（同一个值的所有出现落到同一台），每台算出的次数就是全局次数，再取各自的前 k 合并；或者每台机器先上报所有计数（或者足够多的候选），汇总之后再选。

**5. 堆、分桶、快速选择怎么选？**

- 堆：O(n + d log k)，额外空间 O(d + k)，k 小的时候最合适，也是流式场景里最自然的。
- 分桶：O(n)，额外空间 O(n)；次数天然是小整数，所以可行。次数相同时要排序就不是严格线性。
- 快速选择：对 d 个（值，次数）做 partition，平均 O(d)，最坏 O(d²)；只需要「前 k 个」而不要求有序，并且数据已经全部在内存里时最快；要输出有序还得再对 k 个排序。

面试里先写堆（代码短，不容易错），被问到更快的方法再讲分桶。

## 常见错误

1. 用最大堆放进全部 d 个值再弹 k 次 → 变成 O(d log d)，没有利用 k 小这个条件。
2. 堆里比较器的次数方向写反 → 留下的是出现最少的 k 个。
3. 次数相同时不规定顺序，只对着一个输出去调 → 换一个哈希表实现，输出顺序就变了。
4. 结果数组从前往后填弹出的元素 → 顺序是反的，最好的排在最后。
5. 分布式里直接合并各台机器的本地前 k → 漏掉分散在各处的全局高频值。
