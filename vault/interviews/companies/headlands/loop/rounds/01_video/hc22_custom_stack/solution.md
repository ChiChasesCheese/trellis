# hc22 · 解法与原理

主体只有两个想法：栈用数组存；批量加法不要立刻做，记在一个「待加」数组里，等元素真正出栈时再结算。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep the elements in an array with a size counter. Before I start: is 'bottom k' the k oldest elements? What if k is larger than the current size — add to everything? And how big can the values get — is `int` enough?"

面试官通常会说：栈底就是最先进栈的，k 太大就全加，值先当作 `int` 范围。你可以顺手说一句「我会用 `long` 存，之后再解释为什么」。

## Part 1 · 数组版

**思路**：先写 `a[]` 和 `size`。`push` 在 `size < 容量` 时写入；`pop` 在 `size == 0` 时返回 -1；`increment` 对下标 `0 .. min(k, size) - 1` 循环加。

**原理**：「栈底的 k 个」是下标最小的 k 个，所以 `increment` 只改栈内靠下的部分，pop 取走的栈顶不受影响，除非 k 覆盖到栈顶。`min(k, size)` 是为了不碰还没有元素的格子。

**Java**

```java
private final long[] a;
private int size;

public CustomStack(int maxSize) { a = new long[maxSize]; }
public void push(long x) { if (size < a.length) a[size++] = x; }
public long pop() { return size == 0 ? -1 : a[--size]; }
public void increment(int k, long val) {
    for (int i = 0; i < Math.min(k, size); i++) a[i] += val;
}
```

**C++**

```cpp
explicit CustomStack(int max_size) : a_(max_size) {}
void push(long long x) { if (size_ < a_.size()) a_[size_++] = x; }
long long pop() { return size_ == 0 ? -1 : a_[--size_]; }
void increment(int k, long long val) {
    for (std::size_t i = 0; i < std::min<std::size_t>(k, size_); ++i) a_[i] += val;
}
// members: std::vector<long long> a_; std::size_t size_ = 0;
```

复杂度：`push`、`pop` 是 O(1)，`increment` 是 O(min(k, size))。

## Part 2 · increment 改成 O(1)

**思路**：再加一个数组 `inc`，`increment(k, val)` 只把 `val` 加到 `inc[min(k, size) - 1]` 上，不碰 `a`。`pop` 时算出真实值 `a[i] + inc[i]`，再把 `inc[i]` 下推给 `inc[i - 1]`，最后把 `inc[i]` 清零。

**原理：为什么懒标记是对的**

约定：`inc[i]` 的含义是「下标 0 到 i 的每个元素，都还欠着 `inc[i]`」。这样 `increment` 要加给 0 到 i 的元素，只需要在 `inc[i]` 上记一笔。

栈只有从顶部才能取走元素，所以结算的顺序是固定的：第 i 个元素出栈时，所有欠在它身上的增量，就是 `inc[i]` 加上上面已经出栈的那些位置下推下来的部分。它自己拿走 `inc[i]`；剩下的 0 到 i-1 也欠着同一笔，所以下推给 `inc[i - 1]`。下推之后，`inc[i - 1]` 同时包含「原来记在 i-1 上的」和「从 i 下推来的」，含义不变。

**为什么必须清零**：出栈后这个位置变成空格子，下一次 `push` 会再用它。如果 `inc[i]` 不清零，新元素会带着旧增量出栈。

**Java**

```java
private final long[] a, inc;
private int size;

public CustomStack(int maxSize) { a = new long[maxSize]; inc = new long[maxSize]; }
public void push(long x) { if (size < a.length) a[size++] = x; }

public long pop() {
    if (size == 0) return -1;
    int i = --size;
    long result = a[i] + inc[i];
    if (i > 0) inc[i - 1] += inc[i];
    inc[i] = 0;
    return result;
}

public void increment(int k, long val) {
    int i = Math.min(k, size) - 1;
    if (i >= 0) inc[i] += val;
}
```

**C++**

```cpp
explicit CustomStack(int max_size) : a_(max_size), inc_(max_size) {}
void push(long long x) { if (size_ < a_.size()) a_[size_++] = x; }

long long pop() {
    if (size_ == 0) return -1;
    const std::size_t i = --size_;
    const long long result = a_[i] + inc_[i];
    if (i > 0) inc_[i - 1] += inc_[i];
    inc_[i] = 0;
    return result;
}

void increment(int k, long long val) {
    const long long i = std::min<long long>(k, static_cast<long long>(size_)) - 1;
    if (i >= 0) inc_[static_cast<std::size_t>(i)] += val;
}
// members: std::vector<long long> a_, inc_; std::size_t size_ = 0;
```

复杂度：三个操作都是 O(1)，额外空间 O(maxSize)。

## Part 3 · 口头追问和回答

**1. 懒标记为什么是对的？pop 的时候为什么要把增量下推？**

增量记在 `inc[i]` 上，表示 0 到 i 的所有元素都欠这一笔。第 i 个元素出栈时，它自己结算掉 `inc[i]`；但 0 到 i-1 的元素还欠着，所以要把 `inc[i]` 加到 `inc[i - 1]` 上，让账继续留在栈里。不下推的话，`increment(3, 10)` 之后只有栈顶元素拿到 10，下面两个就丢了。

**2. 为什么 pop 之后要把 `inc[i]` 清零？**

下标 i 之后还会被 `push` 重新使用。旧增量留着，新元素就会在出栈时多拿一笔。测试里「pop 后在同一位置 push 再 pop」专门查这个。

**3. 值会溢出怎么办？为什么用 `long`？「栈空返回 -1」会有什么问题？**

一个元素可能被加很多次，比如原值 0 加三次 2000000000 是 6000000000，超过 `int` 最大值 2147483647。Java 的 `int` 溢出会静默回绕成负数；C++ 的有符号溢出是未定义行为（UB）。所以内部用 64 位存，`long` 能放下 9.2×10^18，通常够用。如果连 64 位也不够，要么限制 `increment` 的次数和大小，要么换大整数，要么检查溢出后报错（Java 用 `Math.addExact`，C++ 用 `__builtin_add_overflow`）。另外，如果元素本身可以是 -1，那 `pop()` 返回 -1 就分不清是「栈空」还是「弹出了 -1」；更干净的接口是返回 `Optional` / 抛异常 / 用 `bool` 加输出参数。

**4. 如果要给任意区间 [l, r] 加一个数，怎么做？**

栈的特殊性在于只从顶部取，所以每次加的区间都是一个前缀（0 到 i），一个懒标记数组就够。任意区间加法有两种常见做法：

- **差分数组**（difference array）：加 [l, r] 等价于 `d[l] += val; d[r + 1] -= val`，查某个位置的值是 `d` 的前缀和。如果只在最后一次性查所有位置，这样最简单；但每次单点查询是 O(n)。
- **线段树 / 树状数组**（segment tree / Fenwick tree）：区间加 + 单点查询用树状数组存差分，两个操作都是 O(log n)；区间加 + 区间查询用带懒标记的线段树，也是 O(log n)。

**5. 多线程同时调用，要怎么保证正确？**

`push`、`pop`、`increment` 都要读写 `size` 和数组，没有同步就会出现数据竞争。最简单的做法是给整个对象加一把互斥锁（Java 用 `synchronized` 或 `ReentrantLock`，C++ 用 `std::mutex` 加 `std::lock_guard`），三个操作都在锁里做。这样每个操作都是原子的，操作的整体顺序是某个串行顺序，已经满足栈的语义。因为每个操作只有 O(1)，锁的持有时间极短，不值得上无锁（lock-free）结构；无锁版要同时原子地更新 `size` 和 `inc`，实现复杂得多。

## 常见错误

1. `increment` 写成 `for (i < k)`：k 大于栈内元素数时，改到了还没有元素的格子，之后 push 的新元素会带着这笔增量。
2. pop 不下推增量：下面的元素丢掉加法。
3. pop 不把 `inc[i]` 清零：同一位置再次 push 的元素多拿一笔旧增量。
4. `increment` 里忘了 `k == 0` 或空栈：`min(k, size) - 1` 变成 -1，数组越界。
5. 用 `int` 存增量：多次加法后回绕成负数（Java）或触发未定义行为（C++）。
