# hc04 · 解法与原理

队列加均值的核心只有一句话：别每次重新求和，边进边出的时候顺手维护「和」与「个数」。快照修正是在这个基础上多一个「整体替换」的操作。下面先说开场 3 分钟怎么做，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep a queue, a running sum and the size, so `mean` is just `sum / size` in O(1). Questions: what should `pop` and `mean` do on an empty queue — throw? Is `double` fine as the return type? Can the values be large enough that the sum overflows `long`?"

面试官通常会说：空队列抛异常，返回 `double`，先不考虑溢出，但可能会追问。

## Part 1 · 队列 + O(1) 均值

**思路**：先选容器（Java 用 `ArrayDeque<Long>`，C++ 用 `std::deque<long long>`），再加一个 `long` 型的和。`push` 时和加上新值，`pop` 时和减去弹出的值，`mean` 用和除以队列长度。

**原理：为什么和用 `long` 不用 `double`**

`double` 只有 53 位有效数字。1e16 已经超过 2^53，相邻两个 `double` 间隔是 2，所以 `1e16 + 1` 会被舍入回 `1e16`。加了又减之后，`1e16 + 1 + 1 - 1e16` 在 `double` 里算出来是 0，真实答案是 2。队列会反复加减，误差一直累积。`long` 的加减是精确的，只要不溢出，每次都是对的。只有最后一步 `sum / size` 转成 `double` 时才有一次舍入。

**原理：为什么每次重新求和不行**

重新遍历队列是 O(n)，调用 n 次就是 O(n²)。维护和之后，每个操作只改一两个变量，是 O(1)。

**Java**

```java
private final ArrayDeque<Long> queue = new ArrayDeque<>();
private long sum = 0;

public void push(long x) {
    queue.addLast(x);
    sum += x;
}

public long pop() {
    long x = queue.removeFirst();  // 空队列时自己抛 NoSuchElementException
    sum -= x;
    return x;
}

public double mean() {
    if (queue.isEmpty()) throw new NoSuchElementException("empty queue");
    return (double) sum / queue.size();
}
```

**C++**

```cpp
void push(long long x) { q_.push_back(x); sum_ += x; }

long long pop() {
    if (q_.empty()) throw std::out_of_range("empty queue");
    long long x = q_.front();
    q_.pop_front();
    sum_ -= x;
    return x;
}

double mean() const {
    if (q_.empty()) throw std::out_of_range("empty queue");
    return static_cast<double>(sum_) / static_cast<double>(q_.size());
}
// 成员：std::deque<long long> q_;  long long sum_ = 0;
```

复杂度：三个操作都是 O(1)，空间 O(n)。

## Part 2 · 快照修正

**思路**：`snapshot` 先清空队列，把和归零，再把新内容逐个 `push` 进去。这样和始终等于队列里的元素之和，不用另写一套求和逻辑。`run` 把每行事件按空格拆开，按第一个词分派到对应方法，遇到 `mean` 就把结果记下来。

**原理：为什么快照要复制，而不是直接保存传入的列表**

如果队列直接引用调用方的列表，调用方之后往列表里加元素，队列的内容就变了，而和没有跟着变，`mean` 立刻算错。逐个 `push` 进自己的容器，既复制了数据，又让和天然正确。

**原理：为什么清空时和要归零**

只清空队列不重置和，旧的和会留在里面，后面所有均值都是错的。这是这个 Part 最常见的错误。

**Java**

```java
public void snapshot(List<Long> contents) {
    queue.clear();
    sum = 0;
    for (long x : contents) push(x);
}

public static List<Double> run(List<String> events) {
    QueueMean q = new QueueMean();
    List<Double> means = new ArrayList<>();
    for (String event : events) {
        String[] w = event.trim().split("\\s+");
        switch (w[0]) {
            case "push" -> q.push(Long.parseLong(w[1]));
            case "pop" -> q.pop();
            case "mean" -> means.add(q.mean());
            case "snapshot" -> {
                List<Long> contents = new ArrayList<>();
                for (int i = 1; i < w.length; i++) contents.add(Long.parseLong(w[i]));
                q.snapshot(contents);
            }
            default -> throw new IllegalArgumentException("unknown event: " + event);
        }
    }
    return means;
}
```

**C++**

```cpp
void snapshot(const std::vector<long long>& contents) {
    q_.clear();
    sum_ = 0;
    for (long long x : contents) push(x);
}

inline std::vector<double> run(const std::vector<std::string>& events) {
    QueueMean q;
    std::vector<double> means;
    for (const std::string& event : events) {
        std::istringstream in(event);
        std::string op;
        in >> op;
        if (op == "push") { long long x; in >> x; q.push(x); }
        else if (op == "pop") q.pop();
        else if (op == "mean") means.push_back(q.mean());
        else if (op == "snapshot") {
            std::vector<long long> contents;
            for (long long x; in >> x;) contents.push_back(x);
            q.snapshot(contents);
        } else throw std::invalid_argument("unknown event: " + event);
    }
    return means;
}
```

复杂度：`snapshot` 是 O(新内容长度)，其余事件 O(1)。

## Part 3 · 口头追问和回答

**1. 为什么和要用 `long` 而不是 `double`？**

见 Part 1 的原理。`double` 在 1e16 以上间隔变成 2，小的数加上去会被吞掉，反复加减后误差累积；`long` 的加减精确，最后只在除法那一步舍入一次。

**2. 元素是 `Long.MAX_VALUE` 时，和会溢出，怎么办？**

`Long.MAX_VALUE` 是 9223372036854775807，两个就超过了 `long`。Java 里 `+` 会静默回绕成负数，C++ 里有符号溢出是未定义行为（undefined behavior）。有三种做法：一是用更宽的和，C++ 用 `__int128`，Java 用 `BigInteger`，或者拆成高低两个 `long`；二是用 `Math.addExact` / `__builtin_add_overflow` 在溢出时报错；三是先跟面试官确认元素范围。如果要求「精确」的均值，返回类型也要改：和可能是 128 位，用 `double` 返回就只剩 53 位有效数字，要精确就返回约分后的分数（分子、分母）。

**3. 一个线程写、很多线程读均值，怎么做？**

不要让读者分别读 `sum` 和 `count`：读到「新的和 + 旧的个数」就是撕裂值。办法是把 `(sum, count)` 打包成一个不可变对象，写者每次修改后用一次 volatile 写（Java 用 `volatile` 字段或 `AtomicReference`）发布出去，读者只读一次这个引用，再用里面的两个值算均值。读者不加锁，写者不被阻塞，读到的一定是某个时刻一致的状态。每次修改多分配一个小对象，这是代价；C++ 里可以用 `std::atomic<std::shared_ptr<Stat>>`，或者用序列锁（seqlock，读者发现版本号变了就重读）。多个写者则必须加锁，因为「读队列、改队列」不是原子的。

**4. 保留每个历史版本，快照要复制多少数据？**

最直接的做法是每个版本复制一份内容，N 个版本、每个 n 个元素就是 O(N·n) 的空间，版本一多就撑不住。更好的做法是持久化数据结构（persistent data structure）：新版本和旧版本共享大部分节点，只新建被改动的那一小部分，比如用链表的版本树，每个版本记住自己的和与个数，还有一个指向父版本的指针。这样 `push` 是 O(1) 或 O(log n)，旧版本永远不变，还能从旧版本分叉出新的历史。

**5. 滑动窗口（固定长度 k）的均值怎么做？**

做法和 Part 1 一样：新数进来加到和里，窗口满了就把最老的减掉。容器上，固定长度用环形数组（ring buffer）最合适：一块连续内存，不分配、不释放，对缓存友好。`std::deque` 是分段数组，每段要单独分配，访问慢一点，但长度不固定时它省事。如果数据里可能有 NaN 或无穷，`double` 的和一旦被污染就永远恢复不了，要么用整数，要么每隔一段时间重新求和。

## 常见错误

1. 每次 `mean` 都遍历求和：每次 O(n)，调用多了超时。
2. 用 `double` 维护和：加了又减，大数把小数吞掉，结果错。
3. `pop` 忘记把和减掉，或者先弹出再读队头：均值永远不对，或者在空队列上崩溃。
4. `snapshot` 只清空队列，没把和归零：之后所有均值都带着旧的和。
5. `snapshot` 直接保存调用方的列表引用：调用方之后改列表，队列内容跟着变，和却没变。
6. 空队列上 `mean` 做 `sum / 0`：Java 的 `double` 除法得到 NaN，C++ 同理，不报错但结果没有意义。
