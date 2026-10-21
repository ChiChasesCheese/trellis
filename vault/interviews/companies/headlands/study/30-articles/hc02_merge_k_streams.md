# hc02 讲义 · 合并 K 个有序序列：从"全部排序"到"多线程、永不卡死"

> 读者：会写基本 Java（类、方法、循环、`ArrayList`/`HashMap`），没学过堆、迭代器协议、阻塞队列、线程中断、虚拟线程；每个概念从零讲。

---

## 1. 问题是什么

把 k 个各自已经排好序的序列合并成一个有序序列，再逐步加条件：序列变成可能无限、会阻塞的数据流，要用多个线程去读，内存必须有界，某条流出错还要有明确的处理方式。核心工具是一个**最小堆**（min-heap，永远能 O(log k) 取出当前最小元素的结构），堆里只放每条序列的队首。下面先看最基础的版本。

**Part 1**：给 `k` 个各自**升序**的序列，合并成一个升序序列。

```
输入:  A = [1, 4, 7]
       B = [2, 5, 8]
       C = [3, 6, 9]
输出:  [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

手算：每个序列只有"当前最前面没用的元素"（队首）有资格成为下一个输出。队首 1、2、3，输出 1；A 的队首变 4；队首 4、2、3，输出 2……"每次从 k 个候选里挑最小的"就是整题核心。

**后续追问**（多路数据流，带多线程、非阻塞、有界并发）：

* 序列是**数据流**（stream）：可能很大、无限、从网络慢慢来，不能一次读完。
* 多线程：每流一个线程读（可能阻塞），合并器怎么配合？
* 非阻塞：不能因某个慢流卡死整个程序。
* 有界：不能把无限数据缓存在内存里。
* 失败：一个流出错怎么办？

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性增长；`O(log n)` n 翻倍只多一步（二分、平衡树、堆）；`O(n²)` 每对元素都处理一次；`O(1)` 与 n 无关。

### 2.1 比较、`Comparable` 与"稳定"

**是什么**：合并"有序"序列，元素得能比大小。Java 里实现 `Comparable<T>`：`a.compareTo(b)` 返回负数（a 小）、0、正数（a 大）。

**注意**：不要用 `a - b < 0` 判断大小，`Long.MIN_VALUE - 1` 会溢出成大正数，判断反了。永远用 `compareTo` 或 `Long.compare`。

**稳定**（stable）：两个元素"相等"（`compareTo == 0`）但不是同一个东西（如同龄的两人），稳定的合并让它们**保持原来的相对顺序**。这里规定：相等时**序列编号小的在前**，同序列内保持原顺序。这样输出**确定**，才能写可验证的期望。

**泛型签名** `<T extends Comparable<? super T>>`：`T` 须能和"T 或其父类"比较。`Dog extends Animal`、`Animal implements Comparable<Animal>` 时，`Dog` 不是 `Comparable<Dog>` 却能和 `Animal` 比，`? super T` 让它也能用（`Collections.sort` 同写法）。

### 2.2 最小堆（min-heap）

**是什么**：支持两个快操作：**放进一个元素**和**取出最小元素**，都是 `O(log n)`。`java.util.PriorityQueue` 就是最小堆。

**为什么需要**：每步从 k 个候选挑最小的。扫描 `O(k)`，N 个输出共 `O(N·k)`；有序列表挑最小 `O(1)` 但插入 `O(k)`；堆两者都 `O(log k)`，总共 `O(N log k)`。

**怎么工作**：堆是"完全二叉树"，**每个节点都不大于它的两个孩子**（最小的在根）。完全二叉树可直接存数组：下标 `i` 的父亲是 `(i-1)/2`，孩子是 `2i+1`、`2i+2`。

* `add`：放数组最后，与父亲比，比父亲小就交换，一路往上（**上浮**，sift-up）。
* `poll`：取走根；最后一个元素搬到根；与较小的孩子比，比它大就交换，一路往下（**下沉**，sift-down）。

演示：依次放入 5, 3, 8, 1，再 `poll`：

```
add 5:  [5]
add 3:  [5,3]      3 的父亲是 5(下标0)，3<5 → 交换 → [3,5]
add 8:  [3,5,8]    8 的父亲是 3，不小于 → 不动
add 1:  [3,5,8,1]  1 在下标3，父亲下标1(值5)，1<5 → 交换 → [3,1,8,5]
                   现在 1 在下标1，父亲下标0(值3)，1<3 → 交换 → [1,3,8,5]
poll:   取走 1；把最后一个 5 搬到根 → [5,3,8]
        5 的孩子是 3 和 8，较小的 3 < 5 → 交换 → [3,5,8]    返回 1
```

每步只沿一条路径走，树高 `log₂ n`，所以 `O(log n)`。

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();      // 自然顺序，最小的先出
PriorityQueue<Head> pq2 = new PriorityQueue<>(Comparator.comparing((Head h) -> h.value).thenComparingInt(h -> h.stream)); // 自定义比较器
pq.add(5);  int smallest = pq.poll();  // poll 在空时返回 null
```

### 2.3 迭代器（`Iterator`）与"惰性"

**是什么**：`Iterator<T>` 是"一次给一个元素"的协议：`hasNext()` 和 `next()`。`for (x : list)` 底层就是它。

**为什么需要**：`List` 要求元素都在内存，迭代器的元素可**用到时才生产**，即**惰性**（lazy）。可处理比内存大的数据（逐行读文件）、无限序列（`Stream.iterate(0, x -> x + 2).iterator()`）、慢来源（网络）。

**合并迭代器的惰性要求**：每个迭代器**必须**先取一个队首才能比较，但**不能多取**。更细：刚输出完 A 的队首 `x` 后，**不要立刻**取 A 的下一个，等调用者下一次 `hasNext/next` 再取。A 可能是慢流（网络），"取下一个"可能等一秒；调用者此刻只想要 `x`，不该为还没要的元素白等。

### 2.4 线程、阻塞与"生产者-消费者"

**线程**是一条执行路径。**阻塞**（block）是线程等某件事（数据、锁）时停住。单线程里一个流等网络，整个程序都停；每流一个线程，一个等，别的继续。

**生产者-消费者**：生产者产生数据，消费者使用，中间用**队列**交接，解耦两边速度。

**阻塞队列**（`BlockingQueue`）：
* `put(x)`：满了就阻塞到有空位。
* `take()`：空了就阻塞到有数据。
* `offer(x)` / `poll()`：不阻塞，满/空时立刻返回 `false`/`null`。

**有界**（bounded）：`new ArrayBlockingQueue<>(capacity)` 容量固定。生产者更快时，队列满后阻塞在 `put`，被"挡住"——**背压**（backpressure）。无界队列则消费者慢时内存无限涨。

```
生产者线程 ──put──▶ [ ][ ][x][x][x]   (容量5)  ──take──▶ 消费者
                       队列满 → put 阻塞 → 生产者暂停
```

### 2.5 线程中断（interrupt）与取消

Java 没有"强行杀线程"（`Thread.stop` 已废弃）。标准取消是**中断**：`thread.interrupt()` 设"中断标志"，线程若阻塞在 `take()`、`put()`、`sleep()`、`join()`，这些方法立刻抛 `InterruptedException` 并清标志。

**为什么重要**：取消卡在 `take()` 的线程只能靠中断。`catch (InterruptedException e) { }` 吞掉取消信号，线程继续跑——最常见的并发 bug 之一。正确：**退出**（`return`），或**重设标志** `Thread.currentThread().interrupt()`。

只有"可中断的阻塞方法"响应中断，读网络的老 API 不一定，所以 `close()` 里等线程退出要带**超时**。

### 2.6 虚拟线程（virtual thread，JDK 21）

平台线程一对一对应操作系统线程，很重（MB 级栈，几千个就吃力）。虚拟线程由 JVM 调度，极轻，可开几十万个，跑在少量"载体线程"上。这里"每流一个线程、写普通阻塞代码"，平台线程 k = 10000 就崩了；虚拟线程阻塞在 `take()`/`put()`/网络 I/O 时让出载体线程。

```java
Thread t = Thread.ofVirtual().name("merge-producer-0").start(() -> { ... });
```

**坑**：纯自旋（`while (!flag) {}`）不让出载体线程；JDK 21 里 `synchronized` 块内阻塞会"钉住"载体线程。所以阻塞处用 `ReentrantLock` 或 `java.util.concurrent` 的类（`ArrayBlockingQueue` 内部用 `ReentrantLock`）。

### 2.7 happens-before

阻塞队列保证：线程在 `put(x)` **之前**的所有写入，另一线程 `take()` 到 `x` **之后**都看得见，传递对象不必额外加锁。背景：CPU 缓存和编译器重排使写入不一定立刻被别的线程看见；Java 内存模型用 **happens-before** 规定保证可见的情形：释放锁 → 之后获取同一把锁；`volatile` 写 → 之后的读；`Thread.start()`、`join()`、并发队列的 `put`/`take`。

### 2.8 `sealed` 消息类型

生产者要告诉合并器三件事之一：（1）一个元素；（2）正常结束；（3）出错。用 `sealed interface Msg permits Item, End, Failed` 表示"只有这三种"。

用 `null` / 特殊值表示会混乱（元素本身可能是 `null`），用类型区分则 `switch` 时编译器检查处理全。`End` 和 `Failed` 是**终止标记**：合并器看到才知道该流不会再有数据，否则永远在等。

### 2.9 结构化并发（`StructuredTaskScope`，JDK 21 预览）

**是什么**：管理一组相关子任务——生命周期限制在一个 `try` 块里，离开块时保证所有子任务已结束。

**为什么需要**：传统 `submit(...)` 得一堆 `Future` 逐个 `get()`；第二个失败时其余仍在跑（甚至永远阻塞），忘关线程池则线程泄漏。原则："**谁启动子任务，谁等它们结束**"，像 `{ }` 作用域。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<A> a = scope.fork(() -> fetchA());
    Subtask<B> b = scope.fork(() -> fetchB());
    scope.join();                 // 等所有子任务结束，或有一个失败
    scope.throwIfFailed();        // 有失败就抛出
    return combine(a.get(), b.get());
}                                 // 离开块：所有子线程一定已结束
```

`ShutdownOnFailure`：只要一个子任务失败，scope 立刻"关闭"，**中断**所有还在跑的兄弟。这是 JDK 21 **预览** API，需 `--enable-preview` 编译运行，未来版本可能改。

---

## 3. 从最笨的解法开始

### 笨解法 A：全部拼起来再排序

```java
List<Integer> all = new ArrayList<>();
for (List<Integer> l : lists) all.addAll(l);
Collections.sort(all);
return all;
```

对，`O(N log N)`（N = 元素总数）。**没用上"各序列已有序"。**

**不行的输入**：数据是**流**（放不下或无限）；只要合并后的**前 10 个**却要排完全部。（`Collections.sort` 稳定，稳定性这里满足。）

**诚实地说**：k = 1000 条、每条 1000 个 `int`（N = 10⁶）时这个笨办法只要约 **50 ms**，比堆合并还快一倍——TimSort 会识别已有序的 run 再归并，实际就是 k 路归并。所以**内存里的 `List`，别为炫技放弃它**；堆的价值在惰性/流式/只取前 m 个/常数额外空间/能并发。这样说显得有判断力。

### 笨解法 B：依次两两合并

```java
List<Integer> acc = new ArrayList<>();
for (List<Integer> l : lists) acc = mergeTwo(acc, l);   // mergeTwo 是标准的双指针合并
return acc;
```

`mergeTwo(a, b)` 两个下标各指当前位置，谁小取谁，`O(|a| + |b|)`。对，但第 i 次合并要拷贝已合并的 `acc`（约 `i · (N/k)`），总共 `Σ i·N/k ≈ N·k/2`，即 `O(N·k)`。k = 1000，N = 10⁶ 时 **约 1230 ms**，是堆版本的 11 倍；k = 10⁴ 时每个元素平均被拷贝 5000 次。根源：`acc` 越来越大却每次整个拷贝。

---

## 4. 一步一步改进

### 步骤 1：用堆挑最小的（Part 1）

**问题**：B 反复拷贝大 `acc`；A 忽略有序性。**想法**：全局最小一定在 k 个队首里。k 个队首放进最小堆，弹出堆顶，再把它所在序列的下一个元素放进堆。
**为什么行**：每个元素进堆、出堆各一次，`O(log k)`；总共 `O(N log k)`，额外空间 `O(k)`。**稳定性**：堆项是 `(值, 序列编号)`，先比值再比编号。

手跑 `[[1,4,7],[2,5,8],[3,6,9]]`：

```
堆: (1,A) (2,B) (3,C)
弹出 (1,A) → 输出 1，补 (4,A)      堆: (2,B) (3,C) (4,A)
弹出 (2,B) → 输出 2，补 (5,B)      堆: (3,C) (4,A) (5,B)
弹出 (3,C) → 输出 3，补 (6,C)
……
```

代码见 5.1 `mergeIterators`。

### 步骤 2：检查输入真的有序

**问题**：某序列其实不升序时，堆合并会默默给出"看似有序实则错"的结果。**想法**：每次取下一个元素与**上一个**比较，更小就抛 `UnsortedInputException(序列编号, 位置)`，每元素 `O(1)`。升序 = 非降序，必须允许相等；用 `compareTo < 0`，不是 `a - b`。

### 步骤 3：去掉装箱（性能版 `mergeLongs`）

**问题**：`PriorityQueue<Head<Long>>` 每元素一个 `Long` 对象，堆里是指针，比较时到处跳读（缓存未命中）。
**想法**：数据已在 `long[][]`，堆里只放 `int` 序列号，比较直接读 `arrays[s][pos[s]]`；自己写堆。无分配、顺序读：**约 65 ms**（装箱版约 110 ms）。代价：代码长、下沉易写错；面试先写简单版，被追问性能再写。

### 步骤 4：惰性（Part 2）

**问题**：`merge(List)` 要求序列全在内存；流式下是迭代器，可能无限。**想法**：自己的 `Iterator<T>`，内部持堆：
1. **构造时不取任何元素**（构造函数不应有副作用/阻塞）。
2. 第一次 `hasNext()/next()` 时，每个 source 取一个队首入堆。
3. `next()` 弹出堆顶返回，**记下**它来自哪个序列（`lastEmitted`），**不立刻**取下一个。
4. 下一次 `hasNext()/next()` 开始时先给 `lastEmitted` 补位，再看堆。

**为什么**：慢 source 的下一个元素不该拖慢当前能返回的结果。**可验证性质**：消费 n 个元素后，所有 source 的 `next()` 总调用 ≤ k + n − 1（两个无限序列取前 10 个只读约 11 个）。

**`Stream` 版**：`StreamSupport.stream(Spliterators.spliteratorUnknownSize(iterator, ORDERED), false)` 包成 `Stream`，再 `onClose` 关闭所有输入；`.limit(5)` 只读够用的。

### 步骤 5：多线程 —— 为什么要有 `Pending`（Part 3）

**问题**：source 会阻塞。单线程取 B 的队首被卡住，A、C 有数据也没法处理。**想法 1**：每个 source 一个线程，循环 `while (src.hasNext()) 放进队列`，合并器从队列取。**想法 2：能不能"谁先到先输出"？** 不能！例子：

```
A 已经有数据: 5, 9
B 还什么都没到。
如果现在输出 A 的 5，然后 B 才送来一个 2 —— 我们已经输出的 5 在 2 前面，顺序错了。
```

合并器**必须等每条还活着的流都给出队首**才能决定谁最小；某流暂时没队首时**无法安全输出任何东西**。这就是 **`Pending`**：不是"没有数据"，而是"现在还决定不了"。流"死了"（正常结束或失败）就不用再等。

**接口**：
* `tryNext()`：**非阻塞**，有活流没队首就返回 `Pending`（调用者可先做别的，如不许阻塞的事件循环，或"最多等 100 ms"）。
* `next()`：阻塞，对没队首的流 `take()`。
* 返回值是 sealed 的 `Poll<T> = Ready(value, stream) | Pending | Done`，`switch` 必须三种都处理。

### 步骤 6：有界队列与背压

**问题**：生产者读得快，合并器慢，队列越堆越多。**想法**：每条流一个 `ArrayBlockingQueue(capacity)`，满了生产者阻塞在 `put`。**性质**：消费者完全不动时，一个 source 最多被读 `capacity + 1` 次（队列里 `capacity` 个，生产者手里再拿 1 个等着放）。
**为什么每流一个队列**：共用时 A 的元素可能塞满队列，B 的放不进去，而合并器恰在等 B 的队首——死锁。独立队列让合并器想要哪条就读哪条，互不挡。

### 步骤 7：永不无限阻塞 —— 终止标记

**问题**：生产者线程因异常死了，合并器 `take()` 永远等。**想法**：生产者循环写成：

```java
try {
    while (src.hasNext()) { ...; q.put(new Item<>(v)); }
    q.put(new End<>());
} catch (InterruptedException _) {
    // close() 叫我们走，没人在听了
} catch (Throwable t) {
    q.put(new Failed<>(t));    // 留遗言
}
```

**为什么行**：无论怎么结束，队列最后一定有 `End` 或 `Failed`（除非整体被取消）。合并器读到 `Failed` 抛 `MergeException(流编号, cause)` 并自动 `close()` 其它生产者。
**`close()`**：对所有生产者 `interrupt()`，再 `join(1 秒)`。阻塞在 `put`/`take` 的被中断唤醒；不响应中断的 source 等 1 秒后放弃——设上限正是为了 `close()` 本身不永远卡住。

### 步骤 8：失败自动取消兄弟 —— `StructuredTaskScope`（Part 4）

**问题**：步骤 7 里失败靠标记传到合并器再由它 `close()`；合并器自己恰好在别处阻塞呢？手动管理线程易错。**想法**：k 个生产者和 1 个合并任务都 `fork` 到同一个 `ShutdownOnFailure` scope：
* 生产者失败 → 抛 `MergeException(流编号, cause)` → scope 自动关闭 → 所有兄弟被中断（含卡在 `take()` 的合并任务）。
* `scope.join()` 后 `throwIfFailed(...)` 抛出第一个失败；离开 `try` 块时所有线程已结束，**不可能泄漏**。

不需要 `Failed` 标记，代码更短。代价：只能"一次性合并全部"，不能边合并边消费。

---

## 5. 逐段讲解法

### 5.1 `MergeK.mergeIterators`

```java
private static final class Head<T> {
    final int stream; final Iterator<? extends T> source;
    T value; long position;
}
```
堆项 = 某 source 的"当前队首"；`stream` 打破相等，`position` 在乱序时报告位置。

```java
return new Iterator<>() {
    private final PriorityQueue<Head<T>> heap = new PriorityQueue<>(
            Math.max(1, snapshot.size()),
            Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream));
    private boolean started;
    private Head<T> lastEmitted;
```
比较器先比值再比序列编号——这一行就是"稳定"。`PriorityQueue` 初始容量不能为 0，故 `Math.max(1, …)`；`snapshot = List.copyOf(sources)` 防调用者之后修改 `List`。

```java
private void prime() {
    if (!started) {
        started = true;
        for (int i = 0; i < snapshot.size(); i++) {
            var h = new Head<T>(i, snapshot.get(i));
            if (advance(h, null)) heap.add(h);
        }
    }
    if (lastEmitted != null) {
        var h = lastEmitted; lastEmitted = null;
        if (advance(h, h.value)) heap.add(h);
    }
}
```
`prime()` 在每次 `hasNext/next` 开头调用：第一次初始化所有队首，之后给上一个输出的序列补位。**构造函数什么也没做**。

```java
private boolean advance(Head<T> h, T prev) {
    if (!h.source.hasNext()) return false;
    T next = Objects.requireNonNull(h.source.next(), "null element in stream " + h.stream);
    if (prev != null) {
        if (next.compareTo(prev) < 0) throw new UnsortedInputException(h.stream, h.position + 1);
        h.position++;
    }
    h.value = next;
    return true;
}
```
取下一个元素，检查非 null、检查升序。`prev == null` 表示是第一个元素，无可比较。

```java
@Override public T next() {
    prime();
    Head<T> h = heap.poll();
    if (h == null) throw new NoSuchElementException();
    lastEmitted = h;
    return h.value;
}
```
弹出堆顶，记为 `lastEmitted`，返回其值。`Iterator` 协议要求耗尽后 `next()` 抛 `NoSuchElementException`。

### 5.2 `MergeK.mergeLongs`

```java
int[] pos = new int[k];    // pos[s] = 序列 s 下一个要读的下标
int[] heap = new int[k];   // 堆里放序列号
for (int i = n / 2 - 1; i >= 0; i--) siftDown(arrays, pos, heap, n, i); // 自底向上建堆 O(k)
```
**自底向上建堆**：从最后一个有孩子的节点（下标 `n/2 - 1`）往前依次下沉，共 `O(k)`（比 k 次上浮的 `O(k log k)` 快）。

```java
while (n > 0) {
    int s = heap[0];
    long v = arrays[s][pos[s]];
    out[o++] = v;
    if (++pos[s] < arrays[s].length) {
        if (arrays[s][pos[s]] < v) throw new UnsortedInputException(s, pos[s]);
    } else {
        heap[0] = heap[--n];     // 这个序列用完：把堆尾搬到堆顶
    }
    siftDown(arrays, pos, heap, n, 0);
}
```
序列用完时用堆尾顶替根再下沉；没用完时根的键变了（`pos[s]` 前进）同样下沉。都是 `siftDown(…, 0)`，不需上浮（新键只会变大）。`less(a, b)`：`va < vb || (va == vb && a < b)`——稳定。

### 5.3 `ConcurrentMerge.Combiner.poll`

```java
Poll<T> poll(boolean block) throws InterruptedException {
    boolean pending = false;
    for (int i = 0; i < queues.size(); i++) {
        if (finished[i] || heads.get(i) != null) continue;
        Msg<T> m = block ? queues.get(i).take() : queues.get(i).poll();
        if (m == null) { pending = true; continue; }
        switch (m) {
            case Item<T> item -> heads.set(i, item);
            case End<T> _ -> finished[i] = true;
            case Failed<T>(var cause) -> throw new MergeException(i, cause);
        }
    }
    if (pending) return new Pending<>();
    ...选最小的...
}
```
对每条"活着但没队首"的流取一条消息：阻塞版 `take()`，非阻塞版 `poll()`（空则 `null`）。`m == null` 记为 pending 但**继续循环**——别的流的 `Failed` 才不会被漏掉。`switch` 对 sealed 的 `Msg` 穷尽。

选最小：

```java
for (int i = 0; i < heads.size(); i++) {
    var h = heads.get(i);
    if (h != null && (best < 0 || h.value().compareTo(heads.get(best).value()) < 0)) best = i;
}
```
**严格小于**才替换，相等保留编号小的——稳定。k 个候选线性扫描 `O(k)`；换堆也省不了，因每次 `poll` 都要检查是否所有流都有队首（面试提一下这个取舍）。

### 5.4 `produce` 与构造器

```java
producers.add(Thread.ofVirtual().name("merge-producer-" + i).start(() -> {
    try { produce(idx, src, q); }
    catch (InterruptedException _) { /* closed */ }
    catch (Throwable t) { try { q.put(new Failed<>(t)); } catch (InterruptedException _) {} }
}));
```
就是步骤 7。构造器里直接启动线程，所以不要让 `this` 逃逸（线程只用局部变量 `q`/`src`）。

### 5.5 `close()`

```java
@Override public void close() {
    if (!closed.compareAndSet(false, true)) return;       // 幂等
    producers.forEach(Thread::interrupt);
    for (Thread t : producers) {
        try { t.join(Duration.ofSeconds(1)); }
        catch (InterruptedException _) { Thread.currentThread().interrupt(); return; }
    }
}
```
`AtomicBoolean.compareAndSet(false, true)` 原子地"若 false 就设 true"，保证只有第一次调用执行。`join(Duration)` 是 JDK 19+ 的带超时版本。

### 5.6 `mergeAll`

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure("merge-all", Thread.ofVirtual().factory())) {
    for (int i = 0; i < srcs.size(); i++) {
        final int idx = i;
        scope.fork(() -> {
            try { produce(idx, srcs.get(idx), queues.get(idx)); }
            catch (InterruptedException e) { throw e; }
            catch (Exception e) { throw new MergeException(idx, e); }
            return null;
        });
    }
    var merged = scope.fork(() -> { ...Combiner 阻塞循环，收集到 List... });
    scope.join();
    scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
    return merged.get();
}
```
* `fork` 返回 `Subtask`；`Thread.ofVirtual().factory()` 让子任务跑在虚拟线程上。
* `InterruptedException` 原样抛出（被取消），其他异常包成带流编号的 `MergeException`。
* `throwIfFailed(Function)` 把失败原因转成想要的异常类型；`e instanceof MergeException me` 是 `instanceof` 模式匹配。
* 失败时 `ShutdownOnFailure` 记录**第一个**失败并中断其余；兄弟因被中断而抛的异常**不会**覆盖它。

---

## 6. Java 21 特性小课

### `record` / `sealed` / 模式匹配 `switch` / record 模式
`Poll`、`Msg` 都是 sealed + record，`case Failed<T>(var cause) ->` 一次拆开；旧写法是类 + `instanceof` + 强转，漏一种情况无提示。`case Ready<T>(var v, _)` 的 `_` 表示不关心该字段（预览）。

### `instanceof` 模式
旧：`if (e instanceof MergeException) { MergeException me = (MergeException) e; … }`。新：`e instanceof MergeException me ? me : …`，判断与绑定合一，`me` 只在为真的分支可见。

### 虚拟线程、`StructuredTaskScope`、`_`
虚拟线程（2.6）**不该用**于 CPU 密集任务（不阻塞，没好处）或需要线程局部大对象的场景。`StructuredTaskScope`（2.9）是预览 API，需 `--enable-preview`，JDK 21 到 25 间还在变，生产代码等正式版。`_`（预览）表示故意不用的绑定：`catch (InterruptedException _)`、`case End<T> _`。

### Stream
`StreamSupport.stream(spliterator, false)` 把迭代器变 `Stream`；`.onClose(Runnable)` 注册关闭回调（`try-with-resources` 触发）；`Stream.iterate(seed, f)` 做无限序列；`toList()`（Java 16）返回不可修改列表。

### `Comparator` 组合子
`Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream)`：先值后编号（旧写法手写 `if (c != 0) return c;`）。显式 `<Head<T>, T>` 因 lambda 参数类型推不出。

---

## 7. 追问预演

**Q1：复杂度？为什么是 log k？**
* 每元素进出堆一次，堆里最多 k 个：`O(N log k)` 时间、`O(k)` 额外空间；对比拼接排序 `O(N log N)`、顺序两两合并 `O(N·k)`。

**Q2：能不能不用堆？**
* 分治两两合并（`log k` 轮，每轮 N 个元素，也是 `O(N log k)`），缓存友好、易并行，但出第一个结果前要完成第一轮，不能流式。也可提败者树（loser tree），比堆少约一半比较，外排序常用。

**Q3：为什么不能先到先输出？**
* 构造反例（A 有 5，B 之后到 2）。有序合并必须知道每条活流的下一个元素，所以有 `Pending`；除非放宽语义（允许乱序 + 水位线）。

**Q4：怎么避免消费者永远阻塞？**
* 终止标记（End/Failed）；生产者 `catch Throwable`；`close()` 中断 + 带超时 join；`next` 加超时 `poll(timeout)`。
* 说法："阻塞在**不保证会结束**的事件上，就要设计'谁来保证它结束'——这里是生产者的 finally 和关闭时的中断。"

**Q5：队列容量怎么选？**
* 太小，生产者常阻塞、吞吐低；太大，内存多、背压反应慢。经验几十到几千，按"每流最多预读多少"想；提 `capacity + 1` 的上界表明你懂精确边界。

**Q6：为什么每条流一个队列？**
* 共享队列会被快流占满，合并器要等的慢流元素放不进去，死锁/饥饿（步骤 6）。

**Q7：失败的流怎么处理？**
* fail-fast（这里：抛 `MergeException` 并取消其他）；或 skip-and-continue（视为结束并记录错误）。这是产品决策，要问清楚。

**Q8：用线程池不行吗？为什么 `StructuredTaskScope`？**
* 线程池 + `Future` 不自动取消兄弟，离开作用域线程可能仍在跑；虚拟线程 + 结构化并发代码是直线的。

**Q9：C++ 怎么写？**
* `std::priority_queue` + 比较器；每流一线程 + 有界队列（`mutex` + `condition_variable`）；取消用 `std::jthread` 的 `stop_token`；也可每流一个 SPSC 无锁环形队列。

---

## 8. 常见误区

1. **用 `a - b` 比较。** `Long.MAX_VALUE - (-1)` 溢出成负数。用 `Long.compare` / `compareTo`。
2. **堆里只按值比，不带序列号。** 相等值的出堆顺序由堆内部状态决定，不稳定。
3. **构造时或刚输出完就取下一个元素。** 多读不需要的；遇慢/无限 source 可能卡死。
4. **有流没数据时输出别的流的元素。** 顺序错（步骤 5）。
5. **无界队列。** 消费者慢时内存无限增长。
6. **所有流共用一个队列。** 快流占满，慢流元素放不进，合并器永远等它的队首。
7. **生产者异常后没有终止标记。** 消费者永远 `take()`。
8. **`catch (InterruptedException e) {}` 吞掉中断。** 取消信号丢失，`close()` 等不到线程。
9. **用 `Thread.sleep` 判断"现在应该是 Pending"。** 睡多久都不保证生产者已跑过。正确：让慢 source 由你控制（如需手动放行）——没给数据，`Pending` 就是确定结果；等事件用 `CountDownLatch`。

---

## 9. 自测题

**1.（概念）** 堆里存的是什么？为什么大小是 k 而不是 N？
<details><summary>答案</summary>
每个序列"当前队首"。一个序列同一时刻只有一个元素在堆里，所以最多 k 个；其余还没轮到。
</details>

**2.（手算）** `A=[1,3]`, `B=[1,2]`，稳定合并输出里两个 `1` 分别来自谁？写出每步的堆。
<details><summary>答案</summary>
初始堆 `(1,A) (1,B)`，键 `(值, 编号)`，`(1,A) < (1,B)`。弹出 `(1,A)`，补 `(3,A)` → 堆 `(1,B) (3,A)`；弹出 `(1,B)`，前两个 1 依次来自 A、B。再补 `(2,B)`，弹出 `(2,B)`，最后 `(3,A)`。输出 `[1(A),1(B),2,3]`。
</details>

**3.（设计）** 为什么 `mergeIterators` 延迟补位，而不是 `next()` 里弹出后立刻补？
<details><summary>答案</summary>
立刻补位会在 `next()` 返回前取该 source 的下一个元素；source 慢（网络）或这是最后一次调用，就白白阻塞/多读。延迟到下一次调用，保证"调用者要的元素已能返回时，不为他还没要的元素等待"。
</details>

**4.（并发）** 把每条流一个队列改成"所有生产者共用一个容量为 `capacity` 的队列"，给出会死锁的场景。
<details><summary>答案</summary>
流 A 很快，塞满共享队列；合并器要决定下一个输出，必须拿到 B 的队首，于是等 B；B 的生产者想 `put` 但队列已满，阻塞。合并器等 B，B 等空位，空位只有合并器消费才有。互相等待。
</details>

**5.（Java）** `catch (InterruptedException e) { }` 为什么危险？写出两种正确处理。
<details><summary>答案</summary>
中断是取消信号，吞掉后线程不知被要求停止，继续运行/阻塞。正确：（1）`return`/退出循环；（2）`Thread.currentThread().interrupt()` 重设标志让上层感知，然后退出或抛出。
</details>

**6.（小编程）** 写一个 `Iterator<Integer>`，把一个迭代器的每个元素 ×2，要求惰性。
<details><summary>答案</summary>

```java
Iterator<Integer> doubled(Iterator<Integer> it) {
    return new Iterator<>() {
        public boolean hasNext() { return it.hasNext(); }
        public Integer next()    { return it.next() * 2; }
    };
}
```
不预读，调用者每次 `next()` 才从 `it` 取一个。
</details>

---

## 延伸阅读

* Goetz 等《Java Concurrency in Practice》第 5 章（阻塞队列与生产者-消费者）、第 7 章（取消与关闭）。
