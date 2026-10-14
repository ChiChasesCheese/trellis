# hc02 讲义 · 合并 K 个有序序列：从"全部排序"到"多线程、永不卡死"

> 配套题集：[problem.md](../../loop/rounds/01_video/hc02_merge_k_streams/problem.md) · [REPORT.md](../../loop/rounds/01_video/hc02_merge_k_streams/REPORT.md) · 参考解 `loop/rounds/01_video/hc02_merge_k_streams/reference/`
> 读者设定：会写基本 Java（类、方法、循环、`ArrayList`/`HashMap`），没学过堆、迭代器协议、阻塞队列、线程中断、虚拟线程。每个概念从零讲。
> 标 **(reconstructed)** 的是我根据题目标题补出来的，不是原题（证据只有标题和第一句话）。

---

## 1. 这道题在问什么

**Part 1（证据：「Given sequences, an array of integer sequences, merge all their entries into one…」）**：

给你 `k` 个序列，每个序列自己是**升序**排好的。把所有元素合并成一个升序序列。

```
输入:  A = [1, 4, 7]
       B = [2, 5, 8]
       C = [3, 6, 9]
输出:  [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

手算：每个序列只有"当前最前面还没用的元素"（队首）有资格成为下一个输出。三个队首是 1、2、3，最小的 1 就是输出的第一个；A 的队首变成 4；
现在队首是 4、2、3，最小的 2；B 的队首变成 5……如此重复。这个"每次从 k 个候选里挑最小的"的动作，就是整题的核心。

**后续追问（证据：「merge multiple data streams，包括 multithreaded non-blocking follow-up」「bounded overlapping background reads」）**：

* 序列不是 `List`，而是**数据流**（stream）：可能很大、可能无限、可能从网络慢慢来，不能一次读完。
* 多线程：每个流由一个线程负责读取（因为读流可能阻塞），合并器怎么和它们配合？
* 非阻塞：合并器不能因为某一个慢流而卡死整个程序。
* 有界：不能为了追求速度，把无限多的数据缓存在内存里。
* 失败：一个流出错了怎么办？

本讲义按这个顺序，从最笨的办法出发，一步步推出最终的解。

---

## 2. 前置知识

### 2.1 比较、`Comparable` 与"稳定"

**是什么**：要合并"有序"序列，元素得能比大小。Java 里让类型可比较的方式是实现 `Comparable<T>` 接口：`a.compareTo(b)` 返回负数（a 小）、0（相等）、正数（a 大）。

**为什么要注意**：不要用 `a - b < 0` 判断大小。`Long.MIN_VALUE - 1` 会溢出变成很大的正数，判断反了。永远用 `compareTo` 或 `Long.compare`。

**稳定**（stable）：如果两个元素"相等"（`compareTo == 0`）但其实不是同一个东西（比如按年龄排序时两个人同龄），稳定的合并保证它们**保持原来的相对顺序**。
对合并 k 个序列，我们规定：相等时**序列编号小的在前**，同一序列内部保持原来的顺序。这样输出是**确定**的——不管你用什么算法实现都得到同一个答案，测试才写得出来。

**泛型签名** `<T extends Comparable<? super T>>`：`T` 必须能和"T 或 T 的父类"比较。为什么是 `? super T`：如果 `class Dog extends Animal`，而 `Animal implements Comparable<Animal>`，
那 `Dog` 不是 `Comparable<Dog>`，但它可以和 `Animal` 比较。`? super T` 让这种类型也能用。你背下这个写法即可（JDK 的 `Collections.sort` 也是这么写的）。

### 2.2 最小堆（min-heap）

**是什么**：堆是一种数据结构，支持两个快的操作：**放进去一个元素**，和**取出最小的元素**，都是 `O(log n)`（n = 堆里的元素数）。
`java.util.PriorityQueue` 就是最小堆。

**为什么需要**：我们每一步都要从 k 个候选里挑最小的。
* 每次扫描 k 个候选：`O(k)` 每步。N 个输出，总共 `O(N·k)`。
* 如果候选放在一个有序的列表里：挑最小的是 `O(1)`，但每次放进新候选要插入到正确位置，`O(k)`。
* 堆：挑最小 `O(log k)`，放进去 `O(log k)`。总共 `O(N log k)`。

**怎么工作**：堆是一棵"完全二叉树"，规则是**每个节点都不大于它的两个孩子**（所以最小的一定在根）。因为是完全二叉树，可以直接存在数组里：
下标 `i` 的节点，父亲是 `(i-1)/2`，孩子是 `2i+1` 和 `2i+2`。

放进去（`add`）：先放在数组最后，然后和父亲比，比父亲小就交换，一路往上（**上浮**，sift-up）。
取最小（`poll`）：取走根；把数组最后一个元素搬到根；然后和两个孩子里较小的比，比它大就交换，一路往下（**下沉**，sift-down）。

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

每一步只沿着树的一条路径走，树高是 `log₂ n`，所以 `O(log n)`。

**Java 里**：

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();      // 自然顺序，最小的先出
PriorityQueue<Head> pq2 = new PriorityQueue<>(Comparator.comparing((Head h) -> h.value).thenComparingInt(h -> h.stream)); // 自定义比较器
pq.add(5);  int smallest = pq.poll();  // poll 在空时返回 null
```

### 2.3 迭代器（`Iterator`）与"惰性"

**是什么**：`Iterator<T>` 是一个"一次给你一个元素"的协议，两个方法：`hasNext()`（还有吗？）和 `next()`（给我下一个）。`for (x : list)` 底层就是迭代器。

**为什么需要**：`List` 要求所有元素已经在内存里。迭代器不要求——元素可以**用到时才生产**。这叫**惰性**（lazy）。
惰性让你可以处理：比内存大的数据（一行一行读文件）、无限序列（所有偶数）、慢的来源（网络）。

**例子**：无限序列"所有偶数"：`Stream.iterate(0, x -> x + 2).iterator()`。它永远 `hasNext() == true`，你取多少它生成多少。

**合并迭代器的"惰性"要求**：合并 `k` 个迭代器时，我们每个迭代器**必须**先取一个队首才能比较，但除此之外**不能多取**。
并且更细的一点：刚输出完 A 的队首 `x` 以后，**不要立刻**去取 A 的下一个元素，要等到调用者下一次调用 `hasNext/next` 才取。
为什么：A 可能是个慢流（网络），"取下一个"可能要等一秒；调用者此刻只想要 `x`，不应该为了一个他还没要的元素白等一秒。

### 2.4 线程、阻塞与"生产者-消费者"

**是什么**：线程是程序里同时进行的一条执行路径。**阻塞**（block）是指线程在等某件事（等数据、等锁）时停在那里什么都不做。

**为什么需要**：如果一个流读数据要等网络，单线程里等它的时候整个程序（包括其他流）都停了。让每个流有自己的线程，一个等，别的还能继续。

**生产者-消费者**：一些线程（生产者）产生数据，另一些线程（消费者）使用数据，中间用一个**队列**交接。队列把两边的速度解耦。

**阻塞队列**（`BlockingQueue`）：
* `put(x)`：队列满了就阻塞，直到有空位。
* `take()`：队列空了就阻塞，直到有数据。
* `offer(x)` / `poll()`：不阻塞，满了/空了立刻返回 `false`/`null`。

**有界**（bounded）：`new ArrayBlockingQueue<>(capacity)` 的容量固定。如果生产者比消费者快，队列满后生产者在 `put` 上阻塞——生产者被"挡住"了。这叫**背压**（backpressure）。
没有它（无界队列），消费者慢时内存会无限涨直到爆掉。

```
生产者线程 ──put──▶ [ ][ ][x][x][x]   (容量5)  ──take──▶ 消费者
                       队列满 → put 阻塞 → 生产者暂停
```

### 2.5 线程中断（interrupt）与取消

**是什么**：Java 里没有"强行杀死线程"（`Thread.stop` 早就废弃，因为危险）。取消的标准方法是**中断**：`thread.interrupt()` 给目标线程设一个"中断标志"，
并且如果它正阻塞在 `take()`、`put()`、`sleep()`、`join()` 这类方法里，这些方法会立刻抛出 `InterruptedException` 并清掉标志。

**为什么重要**：取消一个卡在 `take()` 里的线程，只能靠中断。如果你写 `catch (InterruptedException e) { /* 什么也不做 */ }` 就吞掉了取消信号，线程会继续跑——这是最常见的并发 bug 之一。
正确做法：要么**退出**（`return`），要么**重新设置标志** `Thread.currentThread().interrupt()`。

**注意**：只有"可中断的阻塞方法"响应中断。一个读网络的老 API 不一定响应。所以 `close()` 里等线程退出要带**超时**，不能无限 `join`。

### 2.6 虚拟线程（virtual thread，JDK 21）

**是什么**：传统线程（平台线程）一个对应一个操作系统线程，很重（每个占 MB 级栈，几千个就吃力）。虚拟线程由 JVM 调度，非常轻，可以开几十万个，跑在少量"载体线程"上。

**为什么需要**：我们的设计是"每个流一个线程，线程里写普通的阻塞代码"。如果是平台线程，k = 10000 就崩了。虚拟线程让这种直白的写法可以扩展。
虚拟线程阻塞在 `take()`/`put()`/网络 I/O 时会让出载体线程，别的虚拟线程接着用。

**怎么用**：

```java
Thread t = Thread.ofVirtual().name("merge-producer-0").start(() -> { ... });
```

**坑**：纯自旋（`while (!flag) {}`）不会让出载体线程；`synchronized` 块里阻塞在 JDK 21 会"钉住"载体线程——所以要阻塞的地方用 `ReentrantLock` 或 `java.util.concurrent` 里的类（`ArrayBlockingQueue` 内部用 `ReentrantLock`）。

### 2.7 happens-before（一句话 + 链接）

阻塞队列保证：一个线程在 `put(x)` **之前**做的所有写入，另一个线程 `take()` 到 `x` **之后**都看得见。你不必额外加锁来传递对象。
内存可见性的完整讲解见 [hc04 讲义 §2.8](hc04_queue_mean_snapshot.md)。

### 2.8 `sealed` 消息类型

**是什么**：生产者要告诉合并器三件事之一：（1）这是一个元素；（2）我正常结束了；（3）我出错了。用一个 `sealed interface Msg permits Item, End, Failed` 表示"只有这三种"。

**为什么需要**：这三件事如果都用 `null` / 特殊值表示就混乱了（元素本身可能就是 `null`？）。用类型区分，`switch` 时编译器检查你有没有处理全部三种。
关键的两种是 `End` 和 `Failed`：**终止标记**。合并器看到它们才知道这条流不会再有数据了，否则会永远在等。

### 2.9 结构化并发（`StructuredTaskScope`，JDK 21 预览）

**是什么**：一种管理一组相关子任务的方式——子任务的生命周期被限制在一个 `try` 块里，离开块时保证所有子任务已结束。

**为什么需要**：传统写法：`ExecutorService.submit(...)` 得到一堆 `Future`，你逐个 `get()`。如果第二个任务失败了，第一个、第三个任务还在跑（甚至永远阻塞）；
如果你忘了关线程池，线程泄漏。结构化并发的原则："**谁启动的子任务，谁等它们结束**"，像普通代码里的 `{ }` 作用域。

**怎么用**：

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<A> a = scope.fork(() -> fetchA());
    Subtask<B> b = scope.fork(() -> fetchB());
    scope.join();                 // 等所有子任务结束，或有一个失败
    scope.throwIfFailed();        // 有失败就抛出
    return combine(a.get(), b.get());
}                                 // 离开块：所有子线程一定已结束
```

`ShutdownOnFailure`：只要有一个子任务失败，scope 立刻"关闭"，**中断**所有还在跑的兄弟任务。
这是 JDK 21 的**预览**API：要用 `--enable-preview` 编译和运行，未来版本可能改。

---

## 3. 从最笨的解法开始

### 笨解法 A：全部拼起来再排序

```java
List<Integer> all = new ArrayList<>();
for (List<Integer> l : lists) all.addAll(l);
Collections.sort(all);
return all;
```

**对吗**：对。**复杂度**：`O(N log N)`（N = 所有元素总数）。**它没用上"各序列已经有序"这个条件。**

**在哪个输入上不行**：
* 数据是**流**，不能先全部读进来再排序（放不下内存，或者是无限的）；
* 只想要合并后的**前 10 个**，却要排完全部；
* 稳定性要自己保证——`Collections.sort` 是稳定的，所以这里其实是满足的，别白扔掉这个优点。

**但是，诚实地说**：本机实测（k = 1000 条，每条 1000 个 `int`，N = 10⁶）这个笨办法只要约 **50 ms**，比下面的堆合并还快一倍——
因为 `Collections.sort` 用的 TimSort 会识别"已经有序的一段"（run）然后归并它们，实际上做的就是 k 路归并。
所以：**在内存里的 `List`，别为了炫技放弃它**。堆的价值在于惰性/流式/只取前 m 个/常数额外空间/能并发。面试里这样说会让面试官觉得你有判断力。

### 笨解法 B：依次两两合并

```java
List<Integer> acc = new ArrayList<>();
for (List<Integer> l : lists) acc = mergeTwo(acc, l);   // mergeTwo 是标准的双指针合并
return acc;
```

`mergeTwo(a, b)` 用两个下标各指向 a、b 的当前位置，谁小取谁，`O(|a| + |b|)`。

**对吗**：对。**复杂度**：第 i 次合并要拷贝前面已经合并好的 `acc`，长度大约 `i · (N/k)`。总共 `Σ i·N/k ≈ N·k/2`，即 `O(N·k)`。
**在哪个输入上慢**：k = 1000，N = 10⁶ 实测 **约 1230 ms**，是堆版本的 11 倍；k 再大就更糟（k = 10⁴ 时每个元素平均被拷贝 5000 次）。
问题的根源：`acc` 越来越大，却每次都要整个拷贝一遍。

---

## 4. 一步一步改进

### 步骤 1：用堆挑最小的（Part 1）

**发现问题**：笨解法 B 反复拷贝大的 `acc`；笨解法 A 忽略了有序性。
**想法**：每个序列只有"队首"能成为下一个输出，全局最小一定在 k 个队首里。把 k 个队首放进最小堆，每次弹出堆顶（全局最小），再把它所在序列的下一个元素放进堆。
**为什么能解决**：每个元素只进堆一次、出堆一次，每次 `O(log k)`（堆里最多 k 个）。总共 `O(N log k)`，额外空间 `O(k)`（加输出）。
**稳定性**：堆里每项是 `(值, 序列编号)`，比较时先比值，值相等再比序列编号。

手跑样例 `[[1,4,7],[2,5,8],[3,6,9]]`：

```
堆: (1,A) (2,B) (3,C)
弹出 (1,A) → 输出 1，补 (4,A)      堆: (2,B) (3,C) (4,A)
弹出 (2,B) → 输出 2，补 (5,B)      堆: (3,C) (4,A) (5,B)
弹出 (3,C) → 输出 3，补 (6,C)
……
```

**代码**：见第 5 节的 `mergeIterators`（`merge(List)` 就是调用它并收集结果）。

### 步骤 2：检查输入真的有序（健壮性）

**发现问题**：如果某个序列其实不是升序，堆合并会默默给出一个"看起来有序但其实错了"的结果。
**想法**：每次从一个序列取下一个元素时，和它**上一个**元素比较；比上一个小就抛 `UnsortedInputException(序列编号, 位置)`。
**为什么能解决**：每个序列只被顺序读一遍，检查是 `O(1)` 每元素。
**注意**：比较必须允许相等（升序 = 非降序）；比较用 `compareTo < 0`，不是 `a - b`。

### 步骤 3：去掉装箱（性能版 `mergeLongs`）

**发现问题**：`PriorityQueue<Head<Long>>` 每个元素一个 `Long` 对象，堆里是指针，比较时要跳到各处读数据（缓存未命中）。
**想法**：数据已经在 `long[][]` 里了。堆里只放 `int` 序列号，比较时直接读 `arrays[s][pos[s]]`。自己写堆（数组 + 上浮/下沉）。
**为什么能解决**：没有分配对象，数据按顺序读（CPU 预取友好）。本机 **约 65 ms**（对比装箱版约 110 ms）。
**代价**：代码长、容易写错下沉逻辑；面试里要先写简单版，被追问性能再写这个。

### 步骤 4：惰性（Part 2）

**发现问题**：`merge(List)` 要求所有序列已经在内存里。流式场景里序列是迭代器，可能无限。
**想法**：写一个自己的 `Iterator<T>`，它内部持有堆。
1. **构造时不取任何元素**——构造函数不应该有副作用/阻塞。
2. 第一次 `hasNext()/next()` 时，每个 source 取一个队首放进堆。
3. `next()` 弹出堆顶返回，但**记下**它来自哪个序列（`lastEmitted`），**不立刻**去取下一个。
4. 下一次 `hasNext()/next()` 开始时先给 `lastEmitted` 补位，再看堆。

**为什么这样设计**：2.3 节讲过：慢 source 的下一个元素不该拖慢当前能返回的结果。
**可验证的性质**（测试里就是这样断言的）：消费 n 个元素后，所有 source 的 `next()` 总调用次数 ≤ k + n − 1。
**无限序列**：两个无限序列取前 10 个，只需要读约 11 个元素（k + 10 − 1）。

**`Stream` 版**：`StreamSupport.stream(Spliterators.spliteratorUnknownSize(iterator, ORDERED), false)` 把迭代器包成 `Stream`，再 `onClose` 关闭所有输入。
`Stream` 本身也是惰性的，所以 `.limit(5)` 只会读够用的元素。

### 步骤 5：多线程 —— 为什么要有 `Pending`（Part 3）

**发现问题**：source 现在是会阻塞的（读网络）。单线程里，合并器在取 B 的队首时被卡住，A、C 就算有数据也没法处理。
**想法 1**：每个 source 一个线程，线程里循环 `while (src.hasNext()) 把 src.next() 放进队列`。合并器从队列取。
**想法 2：合并器能不能"谁先到就先输出谁"？** 不能！看这个例子：

```
A 已经有数据: 5, 9
B 还什么都没到。
如果现在输出 A 的 5，然后 B 才送来一个 2 —— 我们已经输出的 5 在 2 前面，顺序错了。
```

所以合并器**必须等每一条还活着的流都给出队首**，才能决定谁最小。如果有一条流暂时没有队首，我们**无法安全输出任何东西**。这就是 **`Pending`** 的含义：不是"没有数据"，而是"现在还决定不了"。
一条流"死了"（正常结束或失败）就不用再等它了。

**接口设计**：
* `tryNext()`：**非阻塞**。每条活着的流没队首就立刻返回 `Pending`（调用者可以去做别的事再来试）。
* `next()`：阻塞。对没有队首的流用 `take()` 等。
* 返回值是 sealed 的 `Poll<T> = Ready(value, stream) | Pending | Done`，调用者的 `switch` 必须三种都处理。

**为什么非阻塞版有意义**：调用者可能是一个事件循环，不允许任何地方阻塞；或者想要"最多等 100 ms 再放弃"。

### 步骤 6：有界队列与背压

**发现问题**：生产者线程飞快读 source，合并器慢——数据在队列里越堆越多。
**想法**：每条流一个 `ArrayBlockingQueue(capacity)`。满了生产者阻塞在 `put` 上。
**可验证的性质**：消费者完全不动时，一个 source 最多被读 `capacity + 1` 次（队列里 `capacity` 个，生产者手里再拿着 1 个正等着放）。
**为什么每条流一个队列，而不是共用一个**：共用一个队列时，A 的元素可能把队列塞满，B 的元素放不进去，而合并器恰恰在等 B 的队首——死锁。每条流独立的队列，合并器想要哪条流的队首就读哪条队列，不会互相挡。

### 步骤 7：永不无限阻塞 —— 终止标记

**发现问题**：生产者线程如果因为异常死了，没人往队列放东西，合并器 `take()` 会永远等下去。
**想法**：生产者的循环写成：

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

**为什么能解决**：无论生产者怎么结束，队列里最后一定有 `End` 或 `Failed`（除非整体被取消），合并器读到就知道这条流完了。
合并器读到 `Failed` 抛 `MergeException(流编号, cause)`，自动 `close()` 其它生产者。
**`close()`**：对所有生产者线程 `interrupt()`，再 `join(1 秒)` 等它们。阻塞在 `put`/`take` 的生产者会被中断唤醒。不响应中断的 source 我们只能等 1 秒后放弃——设上限正是为了 `close()` 本身也不会永远卡住。

### 步骤 8：让失败自动取消兄弟 —— `StructuredTaskScope`（Part 4）

**发现问题**：步骤 7 的手写版本里，失败要通过标记传到合并器，合并器再去 `close()`。如果合并器自己正好在别处阻塞呢？线程的生命周期靠我们手动管理，容易出错。
**想法**：把 k 个生产者和 1 个合并任务都 `fork` 到同一个 `ShutdownOnFailure` scope 里。
* 生产者失败 → 抛 `MergeException(流编号, cause)` → scope 自动关闭 → 所有兄弟被中断（包括卡在 `take()` 的合并任务）。
* `scope.join()` 之后 `throwIfFailed(...)` 把第一个失败抛出来。
* 离开 `try` 块时保证所有线程已结束，**不可能泄漏**。

这个版本里生产者不需要 `Failed` 标记（scope 负责传播失败），所以代码更短。代价：只能"一次性合并全部"，不能边合并边消费。

---

## 5. 逐段讲参考解

文件在 `loop/rounds/01_video/hc02_merge_k_streams/reference/`。

### 5.1 `MergeK.mergeIterators`

```java
private static final class Head<T> {
    final int stream; final Iterator<? extends T> source;
    T value; long position;
}
```
堆里的一项 = 某个 source 的"当前队首"。`stream` 用来打破相等，`position` 用来在乱序时报告位置。

```java
return new Iterator<>() {
    private final PriorityQueue<Head<T>> heap = new PriorityQueue<>(
            Math.max(1, snapshot.size()),
            Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream));
    private boolean started;
    private Head<T> lastEmitted;
```
比较器：先比值，再比序列编号——这一行就是"稳定"。`PriorityQueue` 的初始容量不能是 0，所以 `Math.max(1, …)`。
`snapshot = List.copyOf(sources)` 防止调用者之后修改传入的 `List`。

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
`prime()` 在每次 `hasNext/next` 开头调用：第一次先初始化所有队首；之后给上一个输出的序列补位。**构造函数里什么也没做**，所以"构造时不取数"。

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
取下一个元素，检查非 null，检查升序。`prev == null` 表示这是第一个元素，没有可比较的。

```java
@Override public T next() {
    prime();
    Head<T> h = heap.poll();
    if (h == null) throw new NoSuchElementException();
    lastEmitted = h;
    return h.value;
}
```
弹出堆顶，记为 `lastEmitted`，返回它的值。`Iterator` 协议要求耗尽后 `next()` 抛 `NoSuchElementException`。

### 5.2 `MergeK.mergeLongs`

```java
int[] pos = new int[k];    // pos[s] = 序列 s 下一个要读的下标
int[] heap = new int[k];   // 堆里放序列号
for (int i = n / 2 - 1; i >= 0; i--) siftDown(arrays, pos, heap, n, i); // 自底向上建堆 O(k)
```
**自底向上建堆**：从最后一个有孩子的节点（下标 `n/2 - 1`）开始往前依次下沉，总共 `O(k)`（比 k 次上浮的 `O(k log k)` 更快）。

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
注意：序列用完时用堆尾顶替根，再下沉；没用完时根的"键"变了（因为 `pos[s]` 前进了），同样下沉。两种情况都是 `siftDown(…, 0)`，不需要上浮（因为新的键只会变大——序列是升序的）。

`less(a, b)`：`va < vb || (va == vb && a < b)`——稳定。

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
对每条"还活着但还没有队首"的流取一条消息：阻塞版用 `take()`，非阻塞版用 `poll()`（空则返回 `null`）。
`m == null` 记为 pending 但**继续循环**——这样别的流的 `Failed` 也能被发现，不会因为第一条流 Pending 就漏掉后面流的失败。
`switch` 对 sealed 的 `Msg` 穷尽。

选最小：

```java
for (int i = 0; i < heads.size(); i++) {
    var h = heads.get(i);
    if (h != null && (best < 0 || h.value().compareTo(heads.get(best).value()) < 0)) best = i;
}
```
**严格小于**才替换，所以相等时保留编号小的——稳定。这里只有 k 个候选，线性扫描 `O(k)`；若 k 很大可以换成堆，但每次 `poll` 都要检查是否所有流都有队首，反正是 `O(k)`。（面试里提一下这个取舍。）

### 5.4 `produce` 与构造器

```java
producers.add(Thread.ofVirtual().name("merge-producer-" + i).start(() -> {
    try { produce(idx, src, q); }
    catch (InterruptedException _) { /* closed */ }
    catch (Throwable t) { try { q.put(new Failed<>(t)); } catch (InterruptedException _) {} }
}));
```
这就是 4 节步骤 7。构造器里直接启动线程，所以 `start(…)` 返回时生产者已经在跑了——这也意味着构造过程里不要 `this` 逃逸（这里线程只用局部变量 `q`/`src`，没用 `this`）。

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
`AtomicBoolean.compareAndSet(false, true)`：原子地"若是 false 就设成 true"，保证只有第一次调用真正执行。`join(Duration)` 是 JDK 19+ 的带超时版本。

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
* `InterruptedException` 原样抛出（被取消），其他异常包成 `MergeException` 带上流编号。
* `throwIfFailed(Function)`：把失败的原因转成我们想要的异常类型。`e instanceof MergeException me` 是 `instanceof` 模式匹配。
* 失败时：`ShutdownOnFailure` 记录**第一个**失败，中断其余；兄弟任务因为被中断而抛出的异常**不会**覆盖第一个。

---

## 6. Java 21 特性小课

### J01 `record` / J02 `sealed` / J03 模式匹配 `switch` / J04 record 模式
`Poll`、`Msg` 都是 sealed + record。`case Failed<T>(var cause) ->` 一次拆开。旧写法是类 + `instanceof` + 强转 + `getCause()`，漏掉一种情况时没有任何提示。
`case Ready<T>(var v, _)` 里的 `_` 表示"这个字段我不关心"（J13，预览）。

### J06 `instanceof` 模式
旧：`if (e instanceof MergeException) { MergeException me = (MergeException) e; … }`。新：`e instanceof MergeException me ? me : …`，判断和绑定在一起，且 `me` 只在为真的分支里可见。

### J10 虚拟线程
见 2.6。**什么时候不该用**：CPU 密集型任务（它们不会阻塞，虚拟线程没有好处）；需要线程局部大对象的场景。

### J11 `StructuredTaskScope`（预览）
见 2.9。编译运行需要 `--enable-preview`；API 在 JDK 21 到 25 之间还在变，生产代码要等正式版。

### J13 `_` 未命名模式/变量（预览）
`catch (InterruptedException _)`、`case End<T> _`。表明这个绑定故意不用。

### J14 Stream
`StreamSupport.stream(spliterator, false)` 把迭代器变成 `Stream`；`.onClose(Runnable)` 注册关闭回调，`try-with-resources` 会触发；`Stream.iterate(seed, f)` 做无限序列；`stream.toList()`（Java 16）返回不可修改列表。

### J18 `Comparator` 组合子
`Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream)`：先比值再比编号。旧写法要手写 `compare` 方法里的 `if (c != 0) return c;`。
（`<Head<T>, T>` 是显式给泛型参数，因为 lambda 的参数类型推不出来。）

---

## 7. 追问预演

**Q1：复杂度？为什么是 log k？**
* 思考：每个元素进堆一次出堆一次；堆里最多多少个元素？k 个。
* 要点：`O(N log k)` 时间、`O(k)` 额外空间。对比拼接排序 `O(N log N)`、两两顺序合并 `O(N·k)`。
* 说法："堆里只有 k 个队首，所以每次操作 log k；k = 1 或 2 时几乎是线性的。"

**Q2：能不能不用堆？**
* 要点：分治两两合并（`log k` 轮，每轮 N 个元素，也是 `O(N log k)`），缓存友好、易并行，但不能流式输出第一个结果前要完成第一轮。
* 还可以提：败者树（tournament tree/loser tree），比堆少约一半比较次数，数据库外排序常用。

**Q3：为什么不能先到先输出？**
* 思考：构造一个反例（A 有 5，B 之后到 2）。
* 要点：有序合并必须知道每条活流的下一个元素；所以有 `Pending`；除非放宽语义（允许乱序 + 水位线）。

**Q4：怎么避免消费者永远阻塞？**
* 要点：终止标记（End/Failed）；生产者 `catch Throwable`；`close()` 中断 + 带超时 join；`take` 要响应中断；给 `next` 加超时 `poll(timeout)`。
* 说法："阻塞在一个**不保证会结束**的事件上，就一定要设计'谁来保证它结束'——这里是生产者的 finally 和关闭时的中断。"

**Q5：队列容量怎么选？**
* 要点：太小，生产者经常阻塞，吞吐低；太大，内存多、延迟大（背压反应慢）。经验：几十到几千；按"每条流最多预读多少"来想。用 `capacity + 1` 的上界告诉面试官你知道精确的边界。

**Q6：为什么每条流一个队列？**
* 要点：共享队列会被一条快流占满，合并器要等的慢流元素放不进去，死锁/饥饿（见 4 节步骤 6）。

**Q7：失败的流怎么处理？**
* 要点：fail-fast（本题：抛 `MergeException` 并取消其他）；或 skip-and-continue（把失败流视为结束，记录错误）。这是产品决策，要问清楚。

**Q8：用线程池不行吗？为什么用 `StructuredTaskScope`？**
* 要点：见 2.9；线程池 + `Future` 不会自动取消兄弟；离开作用域线程可能仍在跑；虚拟线程 + 结构化并发代码是直线的。

**Q9：C++ 怎么写？**
* 要点：`std::priority_queue` + 比较器；每条流一个线程 + 有界队列（`mutex` + `condition_variable`）；取消用 `std::jthread` 的 `stop_token`；也可以每条流一个 SPSC 无锁环形队列。

---

## 8. 常见误区

1. **用 `a - b` 比较。**
   * 错在哪：`Long.MAX_VALUE - (-1)` 溢出成负数，比较方向反了。
   * 对应测试：`extremesDoNotOverflowComparisons`。
   * 正确：`Long.compare` / `compareTo`。

2. **堆里只按值比较，不带序列号。**
   * 错在哪：相等值的出堆顺序由堆内部状态决定，不稳定、不确定。
   * 对应测试：`equalElementsComeOutInStreamOrder`、并发测试里的 tie 检查。

3. **构造时或刚输出完就去取下一个元素。**
   * 错在哪：多读了不需要的元素；遇到慢/无限 source 可能卡死。
   * 对应测试：`constructionPullsNothingAndPullsAreMinimal`、`totalPullsNeverExceedKPlusConsumed`。

4. **有流没数据时输出别的流的元素。**
   * 错在哪：见 4 节步骤 5，顺序错。
   * 对应测试：`tryNextIsPendingUntilEveryLiveStreamHasAHead`。

5. **无界队列。**
   * 错在哪：消费者慢时内存无限增长。
   * 对应测试：`backpressureBoundsReadAhead`（精确断言 `capacity + 1`）。

6. **所有流共用一个队列。**
   * 错在哪：快流占满队列，慢流的元素放不进去，合并器永远等它的队首。

7. **生产者异常后没有终止标记。**
   * 错在哪：消费者永远 `take()`。
   * 对应测试：`failingSourceSurfacesAsMergeExceptionAfterItsEarlierItems`。

8. **`catch (InterruptedException e) {}` 吞掉中断。**
   * 错在哪：取消信号丢失，线程继续跑，`close()` 等不到它。
   * 对应测试：`closeInterruptsBlockedProducersAndIsIdempotent`、`oneFailingProducerCancelsTheOthers`。

9. **写测试时依赖 `Thread.sleep` 判断"现在应该是 Pending"。**
   * 错在哪：睡多久都不保证生产者线程已经跑过。
   * 正确：让慢 source 由测试控制（`Gated`）——只要它没给数据，`Pending` 就是确定的结果；要等到某个事件时用 `CountDownLatch`、或在 `assertTimeoutPreemptively` 里 `yield` 轮询。

---

## 9. 自测题

**1.（概念）** 堆里存的是什么？为什么大小是 k 而不是 N？
<details><summary>答案</summary>
存的是每个序列"当前队首"。一个序列同一时刻只有一个元素在堆里，所以最多 k 个。其余元素还没轮到，不需要进堆。
</details>

**2.（手算）** 对 `A=[1,3]`, `B=[1,2]`，稳定合并的输出顺序里，两个 `1` 分别来自谁？写出每一步的堆。
<details><summary>答案</summary>
初始堆 `(1,A) (1,B)`；比较键 `(值, 编号)`，`(1,A) < (1,B)`。弹出 `(1,A)`，补 `(3,A)` → 堆 `(1,B) (3,A)`；弹出 `(1,B)` → 输出的前两个 1 依次来自 A、B。然后补 `(2,B)`，弹出 `(2,B)`，最后 `(3,A)`。输出 `[1(A),1(B),2,3]`。
</details>

**3.（设计）** 为什么 `mergeIterators` 要延迟补位，而不是 `next()` 里弹出后立刻补？
<details><summary>答案</summary>
立刻补位会在 `next()` 返回前就去取那个 source 的下一个元素；source 如果慢（网络）或这是最后一次调用，就白白阻塞/多读。延迟到下一次调用，能保证"调用者要的元素已经能返回时，不会为他还没要的元素等待"。
</details>

**4.（并发）** 如果把每条流一个队列改成"所有生产者共用一个容量为 `capacity` 的队列"，给出一个会死锁的场景。
<details><summary>答案</summary>
流 A 很快，把共享队列塞满 A 的元素；合并器要决定下一个输出，必须拿到 B 的队首，于是等 B 的元素；B 的生产者想 `put`，但队列已满，阻塞。合并器等 B，B 等队列空位，而空位只有合并器消费才有。互相等待。
</details>

**5.（Java）** `catch (InterruptedException e) { }` 为什么危险？写出两种正确的处理。
<details><summary>答案</summary>
中断是取消信号，吞掉后线程不知道被要求停止，继续运行/阻塞。正确：（1）`return`/退出循环；（2）`Thread.currentThread().interrupt()` 重新设置中断标志，让上层继续感知，然后退出或抛出。
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

## 10. 延伸阅读

* Cormen 等，*Introduction to Algorithms*（CLRS）第 6 章 Heapsort / 优先队列，以及习题 6.5-9（合并 k 个有序列表）——堆与 k 路归并的标准出处。
* Knuth, *The Art of Computer Programming* Vol. 3 §5.4.1——败者树（tournament tree）与外排序的多路归并。
* `java.util.PriorityQueue`、`java.util.concurrent.ArrayBlockingQueue`、`java.util.concurrent.StructuredTaskScope` 的 Javadoc。
* JEP 444（Virtual Threads）、JEP 453（Structured Concurrency，JDK 21 预览）——设计动机与使用约束（尤其是 pinning 一节）。
* Goetz 等，*Java Concurrency in Practice* 第 5 章（阻塞队列与生产者-消费者）和第 7 章（取消与关闭、中断策略）。
* Tim Peters 的 `listsort.txt`（CPython 源码里的 TimSort 说明，Java 的 TimSort 同源）——解释为什么"拼接再排序"对分段有序的输入这么快。
