# hc02 · 解法与原理

合并 k 个有序序列的做法只有一个：用最小堆（min-heap）维护「每个序列当前的队首」。Part 2 把同样的堆搬进迭代器，口头追问再把它放到阻塞和多线程的场景里。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep one head element per list in a min-heap, pop the smallest, and push the next element from the same list. Before I start: can k be zero, can lists be empty, and what's the element type?"

面试官通常会说：k 可以为 0，序列可以为空，元素先当 `int`。顺便确认输入允许相等，输出是否要求稳定。

## Part 1 · 最小堆合并

**思路**：先把每个非空序列的第一个元素放进堆，堆元素记三样东西：值、来自第几个序列、在序列里的下标。循环：弹出堆顶，写进结果，再把同一序列的下一个元素放进堆。

**原理：为什么堆里只要 k 个元素就够**

每个序列是升序的，所以全局最小的未输出元素，一定是某个序列的队首。堆里始终放着每个序列的队首，堆顶就是全局最小。弹出之后，这个序列的新队首补进去，不变式保持。

**Java**

```java
public static List<Integer> merge(List<List<Integer>> lists) {
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    for (int i = 0; i < lists.size(); i++)
        if (!lists.get(i).isEmpty()) heap.add(new int[]{lists.get(i).get(0), i, 0});
    List<Integer> out = new ArrayList<>();
    while (!heap.isEmpty()) {
        int[] top = heap.poll();
        out.add(top[0]);
        List<Integer> src = lists.get(top[1]);
        if (top[2] + 1 < src.size()) heap.add(new int[]{src.get(top[2] + 1), top[1], top[2] + 1});
    }
    return out;
}
```

**C++**

```cpp
using Head = std::tuple<long long, std::size_t, std::size_t>;  // 值, 序列号, 下标
using MinHeap = std::priority_queue<Head, std::vector<Head>, std::greater<Head>>;

inline std::vector<long long> merge(const std::vector<std::vector<long long>>& lists) {
    MinHeap heap;
    for (std::size_t i = 0; i < lists.size(); ++i)
        if (!lists[i].empty()) heap.emplace(lists[i][0], i, 0);
    std::vector<long long> out;
    while (!heap.empty()) {
        auto [value, list, pos] = heap.top();
        heap.pop();
        out.push_back(value);
        if (pos + 1 < lists[list].size()) heap.emplace(lists[list][pos + 1], list, pos + 1);
    }
    return out;
}
```

C++ 的 `priority_queue` 默认是最大堆，要加 `std::greater` 才是最小堆。用 tuple 比较时，值相等会继续比序列号，所以序号小的序列自然排在前面。

复杂度：N 是元素总数，每个元素进堆、出堆各一次，堆大小不超过 k，时间 O(N log k)，额外空间 O(k)（不算输出）。

## Part 2 · 惰性迭代器

**思路**：把 Part 1 的循环拆开，每次 `next()` 只做一轮。关键是「补下一个」要放在下一次调用里：`next()` 弹出堆顶后，只记住它来自哪个 source，真正取那个 source 的下一个元素在下一次 `hasNext` / `next` 里做。

**原理：为什么要推迟**

如果弹出之后立刻去取同一个 source 的下一个元素，那么对一个很慢或者无限的 source，你会在用户还没要下一个结果时就先等它。推迟之后，消费 n 个元素，source 被读取的次数是初始的 k 次加上之后 n − 1 次，即 k + n − 1。构造时也不读，这样构造一个迭代器没有副作用。

**Java**

```java
private record Head(int value, Iterator<Integer> source) {}

public static Iterator<Integer> mergeIterators(List<Iterator<Integer>> sources) {
    PriorityQueue<Head> heap = new PriorityQueue<>((a, b) -> Integer.compare(a.value(), b.value()));
    return new Iterator<>() {
        boolean started = false;
        Iterator<Integer> last = null;  // 上一次输出来自哪个 source

        private void fill() {
            if (!started) {
                started = true;
                for (Iterator<Integer> s : sources) if (s.hasNext()) heap.add(new Head(s.next(), s));
            }
            if (last != null) {
                if (last.hasNext()) heap.add(new Head(last.next(), last));
                last = null;
            }
        }

        @Override public boolean hasNext() { fill(); return !heap.isEmpty(); }

        @Override public Integer next() {
            fill();
            if (heap.isEmpty()) throw new NoSuchElementException();
            Head top = heap.poll();
            last = top.source();
            return top.value();
        }
    };
}
```

**C++**

```cpp
class MergeIterator {
public:
    explicit MergeIterator(std::vector<std::vector<long long>> lists) : lists_(std::move(lists)), pos_(lists_.size(), 0) {}

    bool has_next() { fill(); return !heap_.empty(); }

    long long next() {
        fill();
        if (heap_.empty()) throw std::out_of_range("merge exhausted");
        auto [value, list, p] = heap_.top();
        heap_.pop();
        last_ = static_cast<long>(list);  // 它的下一个元素推迟到下一次调用才取
        return value;
    }

private:
    void pull(std::size_t i) {
        if (pos_[i] < lists_[i].size()) heap_.emplace(lists_[i][pos_[i]], i, pos_[i]), ++pos_[i];
    }
    void fill() {
        if (!started_) {
            started_ = true;
            for (std::size_t i = 0; i < lists_.size(); ++i) pull(i);
        }
        if (last_ >= 0) { pull(static_cast<std::size_t>(last_)); last_ = -1; }
    }

    std::vector<std::vector<long long>> lists_;
    std::vector<std::size_t> pos_;
    MinHeap heap_;
    bool started_ = false;
    long last_ = -1;
};
```

复杂度：每次 `next` O(log k)，额外空间 O(k)。`hasNext` 可以反复调用，因为 `fill` 做完一次就清掉 `last`，不会重复取。

## Part 3 · 口头追问和回答

**1. 复杂度是多少？k 和序列长度有区别吗？**

O(N log k)，N 是元素总数。k 很大时每次堆操作更贵，但总比把所有元素排序的 O(N log N) 小。k = 1 时堆里只有一个元素，基本是线性。若 k 很大而序列很短，也可以两两归并，分治地合并，复杂度同样是 O(N log k)。

**2. 为什么不能先拼起来再排序？**

排序是 O(N log N)，而且要把全部 N 个元素同时放进内存。堆版本的额外空间只有 O(k)，而且输入已经有序这个信息被用上了。对流式输入，拼起来再排更是不可能，因为流可能无限。

**3. 怎么保证相等元素稳定？**

让堆的比较键是（值，序列号），值相等时序列号小的先出。序列内部本来就是顺序读取的，所以同一序列里的相等元素也保持原来的顺序。C++ 的 tuple 比较天然这样；Java 里要把比较器写成先比值、再比序列号。

**4. 每个 source 是会阻塞的网络连接，怎么办？**

单线程里调 `source.next()` 会卡住整个合并。做法是每个 source 一个生产者线程，把元素放进自己的有界队列；合并线程只从队列里取。因为要输出全局最小，合并线程必须拿到每个活着的 source 的队首才能决定输出谁，慢的 source 仍然会拖慢输出，但不会拖慢其他生产者的读取。

**5. 非阻塞接口应该长什么样？**

`tryNext()` 立刻返回三种结果之一：`Ready(value)`、`Pending`、`Done`。`Pending` 的意思是「还有 source 没给出队首，现在无法安全判断下一个该输出谁」，而不是「没有数据」。因为那个慢 source 的下一个元素可能比其他所有队首都小，所以合并器不能跳过它输出别人。

**6. 有界缓冲区和背压是什么？**

每个队列有容量上限，队列满了生产者阻塞在 `put` 上，消费者不取，生产者就停下。这样快的 source 不会无限占用内存，慢的消费者也不会被淹没。每个 source 最多被读取「容量 + 正在手里的那一个」个元素。还要保证生产者结束或出错时一定放一个结束标记（End / Failed）进队列，否则合并线程会永远等一个已经死掉的生产者。

## 常见错误

1. 比较写成 `a - b`：极端值相减溢出，顺序错乱。
2. 把 k 个序列全部放进堆，而不是只放队首：堆变成 O(N)，复杂度退化成 O(N log N)。
3. 忘了处理空序列：对空序列取第 0 个元素越界。
4. 迭代器的 `next` 弹出后立刻补下一个：对慢 source 或无限 source 会提前阻塞，也违反 k + n − 1 的取数约束。
5. `hasNext` 每次都重新补一个元素：连续调两次 `hasNext` 会多取。
