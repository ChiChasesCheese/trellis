# hc02 · 思路与追问（C++20 版）

Part 1 是 LeetCode 23 的变体，几分钟写完；面试官真正想看的是你能不能一路推到惰性迭代器、生产者加有界队列、永不无限阻塞、失败传播和取消。C++ 版每一步都有自己的坑：只能用 `<`、`std::priority_queue` 是大顶堆且不稳定、线程里漏出的异常是 `std::terminate`、取消是协作式的。下面按 Part 写清三件事：怎么写、面试官在探什么、该说出口的那句话。完整实现和推导在讲义 [[hc02_merge_k_streams_cpp]]。

## 30 秒版本

- **堆**：k 个队首放进最小堆，弹一个补一个，O(N log k)；比较键是 `(值, 序列编号)`，所以稳定。
- **堆里放下标不放元素**：`priority_queue<Head>`，`Head` 只有 `(stream, pos)`；元素留在原处，结果里恰好拷贝一次。
- **只用 `<`**：不写 `==`、`>`、`a - b`。`priority_queue` 弹出「最大」，比较器要表达「a 排在 b 后面」。
- **惰性**：构造时不读；输出一个元素后，它那条流的补位推迟到下一次调用，所以总读取数 ≤ k + n − 1。
- **并发**：一个 source 一个 `std::jthread` + 一个有界队列；每个生产者结束时一定留下 `End` 或 `Failed`；只有每条活着的流都有队首才能输出，否则 `Pending`。
- **取消与异常**：停止靠 `std::stop_token` 加 `condition_variable_any`；线程体里 `catch (...)` 把异常放进队列；线程组最后声明，最先销毁。

## Part 1 · 堆合并

**写法**

```cpp
auto later = [&](const Head& a, const Head& b) {
    const T& x = lists[a.stream][a.pos];
    const T& y = lists[b.stream][b.pos];
    if (less(y, x)) return true;      // a 的值更大：a 排后面
    if (less(x, y)) return false;
    return a.stream > b.stream;       // 值相等：序列编号大的排后面
};
```

弹出时先 `const Head h = heap.top(); heap.pop();`，再读 `h`。补位时，如果下一个元素比刚输出的小，就抛 `UnsortedInputException(h.stream, h.pos + 1)`。结果提前 `reserve(total)`。`merge_longs` 手写一个 `int` 下标堆，`sift_down` 里比较 `va < vb || (va == vb && a < b)`，建堆自底向上 O(k)。

**面试官在探什么**

1. **复杂度**。堆里永远只有 ≤ k 个队首，所以每次堆操作 O(log k)，共 N 次：O(N log k)。对比拼接再排序 O(N log N)，两两依次合并 O(N·k)。k = 2 时线性扫描更简单也更快。
2. **稳定性**。`priority_queue` 不保证相等元素的出堆顺序，所以序列编号必须写进比较器。能解释：编号大的才是「后面」的那个，所以是 `a.stream > b.stream`。
3. **`top()` 悬空**。`top()` 返回 `const&`，`pop()` 之后它指向已销毁的元素。16 字节的 `Head` 按值拷出来。
4. **只用 `<`**。`a - b` 在 `LLONG_MIN` / `LLONG_MAX` 上是有符号溢出，UB。判断相等写 `!less(a, b) && !less(b, a)`。
5. **堆里放什么**。放元素要拷贝，元素大时贵；放下标，元素留在原处，稳定性只需要把下标放进比较器。代价是比较时多一次间接寻址。
6. **内存里的 vector，堆合并未必比拼接再排序快**。堆合并的价值是流式、只要前 m 个、额外空间 O(k)、能边产生边合并，要如实说。
7. **无符号循环**。`for (size_t i = n / 2; i-- > 0;)` 才对，`i >= 0` 永远为真。

**该说出口的话**：「堆里只有每条序列的队首，所以 O(N log k)；比较键是值加序列编号，保证稳定；堆里放下标，元素只拷贝一次。」

## Part 2 · 惰性合并器

**写法**：`Merger` 记住三样东西：每条流当前的队首 `head_`、上一个输出的元素 `prev_`（做乱序检查）、待补位的流编号 `refill_`。`prime()` 在每次 `has_next()` / `next()` 开头做两件事：第一次调用时给每条流取一个队首；之后把上一次输出的那条流补位。异常用 `std::exception_ptr failure_` 存下来，之后每次调用都 `rethrow_exception`。

**面试官在探什么**

1. **为什么补位要推迟**。一条慢的流刚输出完，立刻去取它的下一个元素会阻塞住，而当前已经能返回的结果还没给调用方。推迟到下一次调用，就是「用到才取」。总读取数因此 ≤ k + n − 1：开头 k 次，输出 n 个元素最多补位 n − 1 次。
2. **为什么 `Merger` 不能拷贝也不能移动**。堆的比较器里存着 `this`；拷贝出来的堆会去读旧对象的 `head_`，旧对象一销毁就悬空。
3. **乱序检查的时机与粘性**。读到那个元素时才发现，所以 `has_next()` 可以抛异常。抛出之后每次调用都重抛同一个异常，不能悄悄跳过坏元素，否则调用方看到的是一个看似正常、实则缺了东西的输出。
4. **为什么是 input range**。`iterator` 加 `sentinel`，所以 `m | std::views::take(8)` 能对无限流取前缀，而不用把无限序列物化。
5. **`from_range` 的所有权**。左值是借用，调用方保证它活着；右值被移入并拥有。状态放在 `shared_ptr` 里，拷贝或移动 `std::function` 也不会让迭代器失效。
6. **元素必须能拷贝**。`prev_` 要保留上一个元素做乱序检查。想支持只能移动的类型，就让 `prev_` 只存一个可拷贝的「键」。

**该说出口的话**：「构造时不读；输出一个元素后，它那条流的补位推迟到下一次调用，所以读取总数不超过 k 加已消费数减 1。」

## Part 3 · 生产者 + 有界队列

**写法**：三层。

| 层 | 做什么 |
|---|---|
| `BoundedQueue` | `mutex` + 两个 `condition_variable_any`（not_full / not_empty）+ `deque`；`push` 和 `pop` 的等待都带 `stop_token` |
| `produce` | 循环：取一个元素、检查顺序、`push`；source 结束时 `push(End{})`；乱序或 source 抛异常就往外抛 |
| `Combiner` | 消费者一侧：每条活着的流都有队首才选最小的，否则 `Pending`（`try_next`）或继续等（`next`） |

线程体里 `try { produce(...) } catch (...) { push(Failed{current_exception()}) }`。消息是 `variant<Item, End, Failed>`，`Combiner` 用 `std::visit` 处理，三种情况都要覆盖。

**面试官在探什么**

1. **为什么不能先到先出**。有序合并要求：只有每条活着的流都有队首，才能决定下一个输出，否则那条流的下一个元素可能比别的队首都小。所以缺队首时 `try_next()` 返回 `Pending`；`Pending` 不是「没数据」，别的流的队列里可能已经攒了很多元素。
2. **背压**。队列满了生产者阻塞在 `push`。消费者不动时，每个 source 最多被取走 `capacity + 1` 次：队列里 `capacity` 个，加生产者手里那一个。
3. **永不无限阻塞**。每个生产者无论正常结束、抛异常还是被取消，都要留下 `End` 或 `Failed`，消费者才不会等一个已经死掉的生产者。
4. **线程体里的异常**。漏出线程体的异常是 `std::terminate`，整个进程退出，所以必须 `catch (...)`。用 `std::exception_ptr` 带出来，连 `throw 42` 这种不是 `std::exception` 的也不例外。
5. **失败要晚于它之前的元素**。`Failed` 排在队列里该流已产出的元素后面，所以消费者先拿到失败前的 10、20，才看到 `MergeException`。
6. **为什么用 `condition_variable_any`**。只有它的 `wait` 有 `stop_token` 重载；`close()` 才能叫醒阻塞在 `push` / `pop` 上的线程。普通 `condition_variable` 要自己配 `stop_callback` 并手动加锁通知，容易写错。
7. **取消是协作式的**。线程杀不掉：source 本身必须认 token。一个永远不返回、也不看 token 的 source，会让 `close()` 和析构一直 join 下去。真实系统里在 source 外面套超时，超时算 `Failed`。
8. **成员声明顺序**。`ConcurrentMerge` 的 `group_`（线程组）最后声明、最先销毁，析构时先 `request_stop` 再 join，之后线程用过的队列和 source 才被销毁。顺序写反就是线程还在用已销毁的队列。
9. **`std::vector<char>` 而不是 `vector<bool>`** 存 finished 标志：后者是按位压缩的代理对象。
10. **怎么测并发代码**。重复运行加随机 `yield` 打乱交错，和顺序实现对拍；ThreadSanitizer 找数据竞争；看门狗线程把死锁变成失败。
11. **一万个 source 怎么办**。一个 source 一个 OS 线程太贵：改成线程池加非阻塞 I/O（`epoll` / `kqueue`），或者限制同时在读的 source 数 m。`capacity` 是预读深度，不是并发数。

**该说出口的话**：「有序合并必须等每条活着的流的队首，所以缺队首就是 `Pending`；每个生产者一定留下 End 或 Failed；取消靠 stop token，线程组析构时 join。」

## Part 4 · `merge_all`

**写法**：生产者放在函数内的 `ThreadGroup`（析构 = `request_stop` + join）里。每个生产者 `catch (...)`，在互斥锁保护下记录第一个失败 `(stream, exception_ptr)`，再 `group.stop.request_stop()`。调用线程自己做消费者：每轮先看 `stop_requested()`，阻塞等待被 token 唤醒就返回 `nullopt`，然后抛 `MergeException`。

**面试官在探什么**

1. **C++ 里的结构化并发**。没有现成的作用域类型，用一个 RAII 对象代替：无论返回还是抛异常，离开函数时线程一定已经 join。
2. **第一个失败赢**。多个生产者可能同时失败，记录要加锁，只留第一个。
3. **其余生产者怎么停**。阻塞在 source 里的，靠 token 醒来（source 要认它）；阻塞在 `push` 上的，靠队列等待里的 token。
4. **声明顺序**。`queues`、`failure` 在 `group` 之前声明，`group` 最后声明，才能先 join 线程、再销毁它们用过的东西。
5. **不要用 `std::async` 加 `future.get()` 代替**：一个失败不会取消其他任务，永远阻塞的 source 会让函数挂住。

**该说出口的话**：「线程组放在函数里，析构就是取消加 join，所以不管怎么离开函数，线程都不会泄漏；第一个失败记下来并触发 stop。」

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 比较 | `compareTo`，要检查 `null` | 只用 `<`（`Less` 模板参数）；`a - b` 是 UB |
| 堆 | 每个元素一个对象 | `priority_queue<Head>` 存下标，元素留在原处 |
| 惰性迭代器 | `Iterator` | `Source` 函数 + input range（`iterator` + `sentinel`），可接 `views::take` |
| 线程 | 虚拟线程，开 k 个很便宜 | `std::jthread` 是 OS 线程，数量要自己控制 |
| 取消 | `interrupt`，阻塞调用抛 `InterruptedException` | `std::stop_token`，协作式，source 和每次等待都要认 |
| 队列 | `ArrayBlockingQueue` | 自己写：`mutex` + `condition_variable_any` + `deque` |
| 结构化并发 | `StructuredTaskScope` | `ThreadGroup`（析构 = 停止 + join）+ 记录第一个失败 |
| 线程里的异常 | 交给未捕获异常处理器 | 漏出线程体 = `std::terminate` |
| 内存 | GC | 成员声明顺序决定谁先销毁；`top()` 返回的引用 `pop()` 后悬空 |
