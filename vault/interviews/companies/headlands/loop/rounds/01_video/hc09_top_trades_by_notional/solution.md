# hc09 · 解法与原理

两问都是「从很多个候选里选最大的 k 个」，工具只有一个：大小为 k 的最小堆。写代码之前把并列规则和溢出说清楚，这两处是面试官真正看的地方。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep a min-heap of size k, so each event costs O(log k). Before I start: if two events have the same notional, which comes first? Do I return indices or the events themselves? And can price times volume overflow a long?"

面试官通常会说：并列时下标小的在前，返回下标，溢出要报错。问出这三点，说明你知道堆只负责「选谁」，顺序要靠你自己定义。

## Part 1 · top-k 事件

**思路**：先定义「谁更好」：notional 大的更好，相同则下标小的更好。堆顶放最差的那个。遍历每个事件：算 notional（用会检查溢出的乘法），入堆，堆比 k 大就弹出堆顶。遍历完，堆里剩的就是最好的 k 个。

**原理：为什么是最小堆**

要留下最大的 k 个，每来一个新元素，要踢掉的是「目前这 k 个里最差的」。最小堆的堆顶正是最差的，O(1) 看到，O(log k) 踢掉。用最大堆就得把全部 n 个都放进去再弹 k 次，空间 O(n)。

**原理：并列规则为什么要写进比较器**

堆里的比较器必须是全序（任意两个元素都分得出先后），否则 notional 相同的元素谁被踢掉由实现决定，结果不可复现。比较器里把「notional 小的更差；notional 相同时下标大的更差」写全，堆顶就总是确定的那一个。弹出的顺序是从差到好，最后反转一次。

**原理：溢出**

Java 的 `long` 乘法溢出时静默回绕成别的数，`Math.multiplyExact` 溢出时抛 `ArithmeticException`。C++ 有符号溢出是未定义行为（undefined behavior），要用 `__builtin_mul_overflow`，它边乘边告诉你有没有溢出。notional 要对每个事件都算，不能只对进堆的事件算，否则一个很大的事件刚好没进 top-k，错误就被漏掉了。

**Java**

```java
public static List<Integer> topEvents(String[] tickers, long[] prices, long[] volumes, int k) {
    int n = tickers.length;
    if (k < 0 || prices.length != n || volumes.length != n) throw new IllegalArgumentException();
    long[] notional = new long[n];
    // 堆顶 = 当前最差的：notional 最小；notional 相同则下标最大
    PriorityQueue<Integer> heap = new PriorityQueue<>(
            Comparator.<Integer>comparingLong(i -> notional[i]).thenComparing(Comparator.reverseOrder()));
    for (int i = 0; i < n; i++) {
        notional[i] = Math.multiplyExact(prices[i], volumes[i]);
        heap.offer(i);
        if (heap.size() > k) heap.poll();
    }
    List<Integer> result = new ArrayList<>();
    while (!heap.isEmpty()) result.add(heap.poll());
    Collections.reverse(result);  // 弹出顺序是从差到好
    return result;
}
```

**C++**

```cpp
inline std::vector<int> top_events(const std::vector<std::string>& tickers, const std::vector<long long>& prices,
                                   const std::vector<long long>& volumes, int k) {
    const int n = static_cast<int>(tickers.size());
    if (k < 0 || prices.size() != tickers.size() || volumes.size() != tickers.size()) throw std::invalid_argument("bad input");
    std::vector<long long> notional(n);
    // 堆顶 = 最差的：notional 最小；notional 相同则下标最大
    auto better = [&](int a, int b) { return notional[a] != notional[b] ? notional[a] > notional[b] : a < b; };
    std::priority_queue<int, std::vector<int>, decltype(better)> heap(better);
    for (int i = 0; i < n; ++i) {
        if (__builtin_mul_overflow(prices[i], volumes[i], &notional[i])) throw std::overflow_error("notional overflow");
        heap.push(i);
        if (static_cast<int>(heap.size()) > k) heap.pop();
    }
    std::vector<int> result;
    while (!heap.empty()) { result.push_back(heap.top()); heap.pop(); }
    std::reverse(result.begin(), result.end());
    return result;
}
```

C++ 的 `priority_queue` 把比较器认为「最大」的放在堆顶，所以比较器写成「a 比 b 更好」，堆顶就是最差的。

复杂度：时间 O(n log k)；堆里最多 k + 1 个元素，再加上存 notional 的数组，额外空间 O(n + k)。

## Part 2 · top-k ticker

**思路**：先遍历一次，用哈希表把每个 ticker 的 notional 累加起来（Java 用 `merge`，C++ 用 `operator[]`）。然后对哈希表里的 m 个不同 ticker，用 Part 1 完全相同的堆选出 k 个：比较器换成「总额大的更好，总额相同则 ticker 字典序小的更好」。

**原理：为什么要分两步**

「汇总」和「选择」是两个问题：汇总要求同一个 ticker 的所有事件都看完，总额才确定；选择要求每个候选都有最终的值。堆只能对最终值排序，所以必须先汇总完再入堆。

**原理：溢出要检查两次**

单个事件的乘法要查，累加也要查。每个事件都不溢出，同一个 ticker 的总额也可能溢出：两个 `Long.MAX_VALUE / 2 + 1` 各自放得下，加起来就放不下。Java 里 `merge(key, value, Math::addExact)` 一行解决，C++ 用 `__builtin_add_overflow`。

**Java**

```java
public static List<String> topTickers(String[] tickers, long[] prices, long[] volumes, int k) {
    int n = tickers.length;
    if (k < 0 || prices.length != n || volumes.length != n) throw new IllegalArgumentException();
    Map<String, Long> total = new HashMap<>();
    for (int i = 0; i < n; i++) total.merge(tickers[i], Math.multiplyExact(prices[i], volumes[i]), Math::addExact);
    // 堆顶 = 最差的：总额最小；总额相同则 ticker 最大
    PriorityQueue<String> heap = new PriorityQueue<>(
            Comparator.<String>comparingLong(t -> total.get(t)).thenComparing(Comparator.reverseOrder()));
    for (String t : total.keySet()) {
        heap.offer(t);
        if (heap.size() > k) heap.poll();
    }
    List<String> result = new ArrayList<>();
    while (!heap.isEmpty()) result.add(heap.poll());
    Collections.reverse(result);
    return result;
}
```

**C++**

```cpp
inline std::vector<std::string> top_tickers(const std::vector<std::string>& tickers, const std::vector<long long>& prices,
                                            const std::vector<long long>& volumes, int k) {
    if (k < 0 || prices.size() != tickers.size() || volumes.size() != tickers.size()) throw std::invalid_argument("bad input");
    std::unordered_map<std::string, long long> total;
    for (std::size_t i = 0; i < tickers.size(); ++i) {
        long long notional;
        if (__builtin_mul_overflow(prices[i], volumes[i], &notional)) throw std::overflow_error("notional overflow");
        if (__builtin_add_overflow(total[tickers[i]], notional, &total[tickers[i]])) throw std::overflow_error("total overflow");
    }
    using Entry = std::pair<long long, std::string>;  // (总额, ticker)
    auto better = [](const Entry& a, const Entry& b) { return a.first != b.first ? a.first > b.first : a.second < b.second; };
    std::priority_queue<Entry, std::vector<Entry>, decltype(better)> heap(better);
    for (const auto& [ticker, sum] : total) {
        heap.push({sum, ticker});
        if (static_cast<int>(heap.size()) > k) heap.pop();
    }
    std::vector<std::string> result;
    while (!heap.empty()) { result.push_back(heap.top().second); heap.pop(); }
    std::reverse(result.begin(), result.end());
    return result;
}
```

复杂度：汇总 O(n)，选择 O(m log k)，m 是不同 ticker 的个数；额外空间 O(m + k)。哈希表的遍历顺序是任意的，所以并列规则必须写进比较器，不能靠遍历顺序。

## Part 3 · 口头追问和回答

**1. 为什么取最大的 k 个要用最小堆？**

堆里始终保存「目前最好的 k 个」。新元素来了，要和其中最差的那个比，如果新元素更好，就踢掉最差的。最小堆的堆顶就是最差的，O(1) 取、O(log k) 删，空间只要 O(k)。最大堆的堆顶是最好的，对这个任务没用。

**2. 排序、堆、quickselect 怎么比？**

- 排序：O(n log n) 时间，要把全部数据放进内存，代码最短。n 小或者 k 接近 n 时合适。
- 堆：O(n log k) 时间，额外空间 O(k)，可以一边读一边做，适合 k 远小于 n 和数据流。
- quickselect：平均 O(n)，最坏 O(n²)，要改动数组（或复制一份），也不适合数据流。
- 面试里默认写堆；说出另外两个和它们的取舍就够了。

**3. `price × volume` 溢出怎么处理？价格是 `double` 呢？**

整数价格（以最小报价单位 tick 计）下，用 `Math.multiplyExact` / `__builtin_mul_overflow`，溢出就报错，绝不静默回绕。想要不报错可以改用 128 位整数或 `BigInteger`，代价是慢。价格是 `double` 时，乘法不会溢出成负数，但累加会丢精度，而且累加的顺序不同结果不同；金额一般先转成整数 tick，或者用 `BigDecimal`。

**4. 事件是实时流，怎么做？**

- 只要 top-k **事件**：堆原样可用，来一个事件处理一次，O(log k)，内存 O(k)。
- top-k **ticker**：同一个 ticker 的总额会变，而堆不能删除或修改中间的元素。办法是哈希表存总额，再配一个按（总额，ticker）排序的有序集合（Java 的 `TreeSet`，C++ 的 `std::set`）：更新时先删旧键再插新键，每次 O(log m)。
- 只关心最近一段时间：窗口外的旧成交要「扣掉」，总额会变小，更需要有序集合；另外要一个按时间排队的队列，知道哪些成交该过期。

**5. 数据有两千万条，怎么用多核？**

把数组切成几块，每块各自算一个「ticker → 总额」的哈希表，最后把各块的表合并（同一个 ticker 的总额相加），再对合并后的表选 top-k。各块之间没有共享的可变状态，不需要锁。整数加法满足结合律，所以怎么切块结果都一样；`double` 不满足，结果会随切法变。所有价格和数量都非负时，部分和只增不减，因此「最终总额是否溢出」与怎么切块无关，各块里查、合并时也查就能得到同样的结果。

**6. 并列规则不写清楚会出什么问题？**

结果不唯一：同样的输入，换一种遍历顺序或者换一种实现，返回的第 k 名可能不同，测试和下游都无法复现。堆本身不保证稳定，所以并列规则要写在比较器里，让比较器成为全序。

## 常见错误

1. 用最大堆，把全部事件放进去再弹 k 个：空间变成 O(n)，也说明没有想清楚「踢掉谁」。
2. 比较器只比 notional：并列时谁被踢掉由实现决定，答案不稳定。
3. 只对进堆的事件算 notional：没进 top-k 的事件溢出被漏掉。
4. Part 2 只检查单个事件的乘法，不检查累加：同一个 ticker 的总额静默回绕成负数，排到最后。
5. 弹出堆之后忘了反转：返回的是从差到好的顺序。
6. 用 `i < k` 之类的条件在堆没满时特殊处理，却忘了 `k == 0`：对空堆调用 `peek` 或 `top`。上面的写法先入堆再弹出，`k == 0` 自然得到空结果。
