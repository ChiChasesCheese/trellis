# hc13 · 解法与原理

内存池考的是两件事：怎么 O(1) 找到一个空闲块，以及怎么发现「手里的编号已经不属于你了」。第一件事靠一个整数数组串成链表，第二件事靠给每个槽位加版本号。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep a free list threaded through an int array: `next[i]` is the next free block after `i`. Allocate pops the head, release pushes it back, both O(1). Before I start: what should `allocate` return when the pool is full, and should a double release throw or be ignored?"

面试官通常会说：池满返回 -1，重复归还要报错。再顺口问一句「分配顺序有要求吗」，答案一般是没有，你可以说明你的实现是后进先出。

## Part 1 · 空闲链表

**思路**：先开一个 `int[] next`。空闲的块 `i` 里放「下一个空闲块的编号」，链尾放 `-1`；在用的块里放一个特殊值 `USED = -2`。再用一个变量 `head` 指向链头。

**原理：为什么不另开一个 `boolean[]` 记录是否在用**

空闲块里的 `next[i]` 是链表指针，在用的块里这个位置本来没用，正好拿来放「在用」的标记，所以一个数组同时装下链表和状态。重复归还时，块 `i` 已经在链上，`next[i]` 不是 `USED`，一比较就能发现。如果不检查，同一个块会被插进链表两次，之后两次 `allocate` 会把同一个块给两个人，这是最危险的错误。

**Java**

```java
public final class IndexPool {
    private static final int USED = -2;
    private final int[] next;
    private int head = 0;

    public IndexPool(int capacity) {
        if (capacity < 1) throw new IllegalArgumentException("capacity must be >= 1: " + capacity);
        next = new int[capacity];
        for (int i = 0; i < capacity; i++) next[i] = i + 1 < capacity ? i + 1 : -1;
    }

    public int allocate() {
        int block = head;
        if (block == -1) return -1;
        head = next[block];
        next[block] = USED;
        return block;
    }

    public void release(int block) {
        if (block < 0 || block >= next.length) throw new IllegalArgumentException("no such block: " + block);
        if (next[block] != USED) throw new IllegalStateException("block not in use: " + block);
        next[block] = head;
        head = block;
    }
}
```

**C++**

```cpp
class IndexPool {
public:
    explicit IndexPool(int capacity) {
        if (capacity < 1) throw std::invalid_argument("capacity must be >= 1");
        next_.resize(capacity);
        for (int i = 0; i < capacity; ++i) next_[i] = i + 1 < capacity ? i + 1 : -1;
    }

    int allocate() {
        const int block = head_;
        if (block == -1) return -1;
        head_ = next_[block];
        next_[block] = kUsed;
        return block;
    }

    void release(int block) {
        if (block < 0 || block >= static_cast<int>(next_.size())) throw std::out_of_range("no such block");
        if (next_[block] != kUsed) throw std::logic_error("block not in use");
        next_[block] = head_;
        head_ = block;
    }

private:
    static constexpr int kUsed = -2;
    std::vector<int> next_;
    int head_ = 0;
};
```

复杂度：`allocate` 和 `release` 都是 O(1)；构造是 O(capacity)；空间是 capacity 个 `int`。

## Part 2 · 带版本号的 handle

**思路**：Part 1 的编号发给调用方之后，池就管不住它了。给每个槽位加一个版本号 `generation`，每次归还加 1；发给调用方的不再是裸编号，而是把版本号和下标拼在一起的 64 位 handle。归还时先比较 handle 里的版本号和槽位当前的版本号，不一致就是过期的 handle。

**原理：它解决了什么**

场景：A 借到块 3，还掉；B 借到同一个块 3；A 手里还留着旧编号 3，再还一次。只有编号时，池分不清这是 A 还是 B，会把 B 正在用的块放回链表。有了版本号，A 手里是 `(generation 0, index 3)`，B 手里是 `(generation 1, index 3)`，槽位当前版本是 1，A 的旧 handle 因为版本号不等被拒绝。这种「还掉之后继续用」的错误叫 use-after-free，旧编号还能用的这类问题就是它在池里的版本。

位运算有一个坑：把 `int` 下标放进低 32 位时，Java 里 `(long) index` 对负数会做符号扩展，高 32 位全变成 1，污染版本号，所以要写 `index & 0xFFFFFFFFL`。取回时 `(int) handle` 直接截低 32 位，不会出错。C++ 里把 `uint32_t` 的版本号提升成 `uint64_t` 再左移 32 位，也不会有符号问题，而且无符号加法回绕在 C++ 里是有定义的。

下标是否越界的判断：Java 里 `index < 0 || index >= length`；C++ 里把下标当 `uint32_t`，一次 `>= size()` 的比较同时挡住负数和过大。

**Java**

```java
public final class GenPool {
    private final IndexPool pool;
    private final int[] generation;

    public GenPool(int capacity) {
        pool = new IndexPool(capacity);
        generation = new int[capacity];
    }

    public long allocate() {
        int index = pool.allocate();
        if (index == -1) return -1L;
        return (long) generation[index] << 32 | (index & 0xFFFFFFFFL);
    }

    public void release(long handle) {
        int index = indexOf(handle);
        if (index < 0 || index >= generation.length) throw new IllegalArgumentException("no such block: " + index);
        if ((int) (handle >>> 32) != generation[index]) throw new IllegalStateException("stale handle");
        pool.release(index);
        generation[index]++;
    }

    public static int indexOf(long handle) { return (int) handle; }
}
```

**C++**

```cpp
class GenPool {
public:
    static constexpr std::uint64_t NONE = ~std::uint64_t{0};

    explicit GenPool(int capacity) : pool_(capacity), generation_(capacity, 0) {}

    std::uint64_t allocate() {
        const int index = pool_.allocate();
        if (index == -1) return NONE;
        return std::uint64_t{generation_[index]} << 32 | static_cast<std::uint32_t>(index);
    }

    void release(std::uint64_t handle) {
        const std::uint32_t index = index_of(handle);
        if (index >= generation_.size()) throw std::out_of_range("no such block");
        if (static_cast<std::uint32_t>(handle >> 32) != generation_[index]) throw std::logic_error("stale handle");
        pool_.release(static_cast<int>(index));
        ++generation_[index];
    }

    static std::uint32_t index_of(std::uint64_t handle) { return static_cast<std::uint32_t>(handle); }

private:
    IndexPool pool_;
    std::vector<std::uint32_t> generation_;
};
```

注意顺序：先 `pool.release`，成功之后才给版本号加 1。版本号相同但槽位不在用的情况（比如伪造的 `0L`，槽位 0 还没发出去）由 `pool.release` 抛出。

复杂度：都是 O(1)；额外空间是 capacity 个 32 位版本号。

## Part 3 · 口头追问和回答

**1. 怎样让这个池线程安全？**

最简单的做法是给 `allocate` 和 `release` 各加一把锁（Java 用 `synchronized`，C++ 用 `std::mutex`）。临界区只有几条指令，竞争不激烈时代价很小；竞争激烈时，线程会排队、被挂起、再被唤醒，延迟变得不稳定。无锁做法是把空闲链表做成 Treiber 栈：`head` 放在一个原子变量里，`allocate` 读出 `head`，用 CAS（compare-and-swap）把它换成 `next[head]`，失败就重读重试；`release` 同理把自己 CAS 成新的头。没有线程会被挂起，但代码更难写对，还要处理下一个问题。

**2. ABA 问题是什么？**

线程 T1 读到 `head = 3`、`next[3] = 5`，准备把 head CAS 成 5，这时被抢占。T2 取走 3、取走 5，又把 3 还回来，于是 head 又是 3，但 5 已经在用了。T1 恢复后 CAS 看到 head 仍是 3，成功，把 head 设成 5，结果一个正在使用的块被放回了空闲链。CAS 只比较值，看不出中间发生过变化。解法是让 head 带一个每次修改都加 1 的版本号（tag），把「编号」和「tag」打包在一个 64 位原子变量里一起 CAS；T1 回来时 tag 已经变了，CAS 失败。这和 Part 2 的 handle 是同一个思路。

**3. 对齐和伪共享**

池里放的是真实对象时，块的起始地址要满足对象的对齐要求。做法是从一块按对齐分配的内存（C++ 用 `std::aligned_alloc` 或 `operator new(size, std::align_val_t)`）里按固定步长切块，步长是对象大小向上取整到对齐的倍数。伪共享是指两个线程各自修改的变量落在同一条缓存行（cache line，常见 64 字节）里，一个线程写会让另一个线程的缓存行失效，两边互相拖慢。热点数据（比如无锁版本的 `head`）可以单独补齐到一条缓存行。

**4. 池为什么比 `new` / `malloc` 快？它带来什么新问题？**

通用分配器要在大小不一的块里找合适的，可能加锁，可能向操作系统要内存，耗时不稳定；池里块等大，借和还只是几条指令，耗时固定，没有碎片。在 Java 里还少了垃圾回收（GC）的压力。新问题：use-after-free 不再崩溃，而是变成逻辑错误，旧使用者悄悄改了新使用者的数据，这就是 Part 2 要检测的；归还时没清零会把上一个主人的数据漏给下一个；池的总量固定，满了就必须有应对办法。

**5. 32 位版本号回绕了怎么办？**

同一个槽位被借还 2^32 次之后版本号回到原值，一个存了这么久的旧 handle 会被当成有效的。实际上一个槽位要被借还 40 多亿次，而旧 handle 还一直没丢，概率极低。要更保险就用更宽的版本号（下标缩到 24 位给版本号 40 位），或者槽位的版本号用完就永久退役这个槽位。

**6. 池里要放的是对象，不只是编号怎么办？**

另开一个同样大小的数组（或一块原始内存），第 `i` 个块就是第 `i` 个元素；`allocate` 返回编号，调用方用编号读写元素。C++ 里原始内存要用 placement new 构造对象、显式调用析构函数，归还时先析构再放回链表。Java 里是对象数组，数组里的对象一直活着，借出时重置字段。

## 常见错误

1. 重复归还不检查：同一个块被插进链表两次 → 之后两次分配给出同一个块，两个调用方互相覆盖数据。
2. 为了判断「是否在用」另开 `boolean[]` 并用循环找空闲块 → `allocate` 变成 O(n)。
3. 先给版本号加 1 再检查槽位是否在用：被拒绝的归还也让版本号变化，合法 handle 莫名失效。
4. Java 里写 `(long) generation << 32 | index` 而没有 `& 0xFFFFFFFFL`：下标非负时没事，一旦下标是负数，符号扩展会把高 32 位的版本号全部改写。
5. 只比较下标不比较版本号 → 回到 Part 1，旧 handle 能归还新主人的块。
