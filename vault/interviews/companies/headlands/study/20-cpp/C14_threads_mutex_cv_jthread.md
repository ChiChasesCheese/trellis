# C14 · 线程、`mutex`、`condition_variable`、`jthread`

> 目标：能用 C++ 标准库写出正确的多线程代码：启动/等待线程、保护共享数据、阻塞队列（生产者-消费者）、避免死锁、可取消线程。

## 1. Java 对照

| Java | C++ |
|---|---|
| `Thread` / `ExecutorService` | `std::thread` / `std::async`、`std::jthread` |
| `synchronized` / `ReentrantLock` | `std::mutex` + `lock_guard` / `unique_lock` / `scoped_lock` |
| `ReentrantReadWriteLock` | `std::shared_mutex` |
| `Condition` / `wait/notify` | `std::condition_variable` |
| `Future` | `std::future` |
| `ThreadLocal` | `thread_local` |
| `CountDownLatch` / `Semaphore` | `std::latch` / `std::counting_semaphore`（C++20） |
| `BlockingQueue` | 自己用 `mutex` + `condition_variable` 写 |
| `Thread.interrupt()` | `stop_token`（C++20，协作式） |

关键差别：C++ 的 `mutex` **不可重入**；线程对象析构时若仍可 join 会直接 `std::terminate`；没有「守护线程」；数据竞争是 UB（没有保底语义）。

## 2. 启动、传参、结果、异常

```cpp
void add_to(int& target, int amount) { target += amount; }

void passing_arguments() {
    int total = 0;
    std::thread t1(add_to, std::ref(total), 5);      // arguments are COPIED into the thread; std::ref asks for a reference
    t1.join();                                       // forgetting join()/detach() => std::terminate in ~thread
    std::cout << "  total after thread with std::ref: " << total << "\n";
    // std::thread t2(add_to, total, 5);             // does not compile: copies cannot bind to int&
}
```

```cpp
long parallel_sum(const std::vector<int>& v) {
    auto mid = v.begin() + static_cast<std::ptrdiff_t>(v.size() / 2);
    auto left = std::async(std::launch::async, [&] { return std::accumulate(v.begin(), mid, 0L); });   // runs on another thread
    long right = std::accumulate(mid, v.end(), 0L);                                                    // meanwhile, this thread
    return left.get() + right;                       // get() waits, and rethrows any exception the task threw
}
```

```cpp
void exceptions_cross_threads() {
    auto f = std::async(std::launch::async, []() -> int { throw std::runtime_error("worker failed"); });
    try { (void)f.get(); } catch (const std::exception& e) { std::cout << "  caught from worker: " << e.what() << "\n"; }
    // An exception that escapes a plain std::thread function calls std::terminate() instead.
}
```

```cpp
thread_local int per_thread_counter = 0;              // every thread has its own copy (Java: ThreadLocal<Integer>)

void thread_local_demo() {
    std::vector<std::thread> ts;
    std::vector<int> results(3);
    for (int i = 0; i < 3; ++i)
        ts.emplace_back([i, &results] { for (int k = 0; k <= i; ++k) ++per_thread_counter; results[i] = per_thread_counter; });
    for (auto& t : ts) t.join();
    std::cout << "  thread_local results: " << results[0] << " " << results[1] << " " << results[2] << ", main's copy: " << per_thread_counter << "\n";
}
```

```text
  total after thread with std::ref: 5
  parallel_sum(1..1000) = 500500
  caught from worker: worker failed
  thread_local results: 1 2 3, main's copy: 0
  hardware_concurrency >= 1: 1
```

* 参数默认被**拷贝**进线程；要引用必须 `std::ref`；lambda 的 `[&]` 要保证被引用对象比线程活得久。
* `std::thread` 析构时若没有 `join()`/`detach()` 直接终止程序。`detach` 后线程无人管理，极易访问已销毁的数据，**避免**。
* `std::async(launch::async, f)` 返回 `future`；`get()` 等待并**重新抛出**任务里的异常。直接从 `std::thread` 的函数里逃出的异常会 `terminate`。
* `thread_local`：每个线程独立一份。

## 3. 互斥与 RAII 锁

* `std::mutex`：`lock()`/`unlock()` 手动调用容易漏解锁（异常、提前 return）；**永远用 RAII 包装**：
  * `lock_guard`：构造加锁、析构解锁，最简单。
  * `unique_lock`：可手动解锁/重新加锁、可与 `condition_variable` 配合。
  * `scoped_lock`（C++17）：同时锁多个 mutex，内部用死锁避免算法。
  * `shared_lock` + `shared_mutex`：读写锁。
* 临界区越短越好；**不要在持锁时调用未知代码**（回调、虚函数、IO）。

### 死锁与 `scoped_lock`

两个线程一个按 A→B、另一个按 B→A 加锁就可能死锁。解法：全局统一加锁顺序，或一次性 `scoped_lock(a, b)`：

```cpp
struct Account { std::mutex m; long balance = 0; };

void transfer(Account& from, Account& to, long amt) {
    std::scoped_lock lock(from.m, to.m);          // locks BOTH with a deadlock-avoidance algorithm, whatever the argument order
    from.balance -= amt; to.balance += amt;
}
```

读写锁适合读多写少：

```cpp
class Prices {
    mutable std::shared_mutex m_;                 // many readers OR one writer (Java: ReentrantReadWriteLock)
    long px_ = 100;
public:
    long read() const { std::shared_lock<std::shared_mutex> g(m_); return px_; }
    void write(long v) { std::unique_lock<std::shared_mutex> g(m_); px_ = v; }
};
```

## 4. `condition_variable`：等待条件

问题：消费者要等「队列非空」。忙等（自旋）浪费 CPU；`condition_variable` 让线程**睡眠**直到被唤醒。规则：

1. 条件本身是**被 mutex 保护的共享状态**（队列、标志）。
2. 等待用 `cv.wait(lock, predicate)`：线程先释放锁并睡眠，被唤醒时重新加锁并**重新检查谓词**——必须带谓词，因为存在**虚假唤醒（spurious wakeup）**和「通知后条件又被别人改回去」。
3. 修改状态后 `notify_one/notify_all`，通知可以在锁外发出（唤醒的线程不用再立即阻塞在锁上）。

一个有界阻塞队列（Java 的 `ArrayBlockingQueue`）：

```cpp
template <class T>
class BlockingQueue {
    std::mutex m_;
    std::condition_variable not_empty_, not_full_;
    std::deque<T> q_;
    const std::size_t cap_;
    bool closed_ = false;
public:
    explicit BlockingQueue(std::size_t cap) : cap_(cap) {}

    void push(T v) {
        std::unique_lock<std::mutex> lk(m_);                         // unique_lock: wait() must be able to unlock/relock it
        not_full_.wait(lk, [&] { return q_.size() < cap_; });        // predicate form: re-checked after every wakeup
        q_.push_back(std::move(v));
        lk.unlock();                                                 // notify without holding the lock: the woken thread can run at once
        not_empty_.notify_one();
    }
    std::optional<T> pop() {                                         // empty optional = queue closed and drained
        std::unique_lock<std::mutex> lk(m_);
        not_empty_.wait(lk, [&] { return !q_.empty() || closed_; });
        if (q_.empty()) return std::nullopt;
        T v = std::move(q_.front());
        q_.pop_front();
        lk.unlock();
        not_full_.notify_one();
        return v;
    }
    void close() { { std::lock_guard<std::mutex> g(m_); closed_ = true; } not_empty_.notify_all(); }
};
```

```text
consumed 1000 items, sum 500500
balances 1000 + 1000 = 2000
final price 199
```

`close()` 加 `notify_all` 让消费者在队列排空后退出，是干净的关闭协议。

## 5. C++20：`jthread` 与协作式取消

* `std::jthread`：析构时自动 `request_stop()` 再 `join()`，不会 `terminate`。
* `std::stop_token`：线程函数的第一个参数；循环里检查 `stop_requested()`。
* `std::condition_variable_any::wait(lock, stop_token, pred)`：被取消时也能从阻塞等待中醒来（返回 false）。
* `std::latch`（一次性倒计数）、`std::barrier`（可重复）、`std::counting_semaphore`。

```cpp
void worker(std::stop_token st, std::atomic<int>& ticks) {
    while (!st.stop_requested()) {                  // cooperative cancellation: the thread checks, nobody kills it
        ++ticks;
        std::this_thread::sleep_for(1ms);
    }
}
```

```cpp
struct Mailbox {
    std::mutex m;
    std::condition_variable_any cv;                 // _any: wait() can take a stop_token
    int pending = 0;
};
void waiter(std::stop_token st, Mailbox& mb, bool& woke_by_stop) {
    std::unique_lock lk(mb.m);
    bool got = mb.cv.wait(lk, st, [&] { return mb.pending > 0; });   // returns false if stop was requested first
    woke_by_stop = !got;
}
```

```cpp
std::latch ready(3);                            // one-shot countdown
std::counting_semaphore<2> slots(2);            // at most 2 workers inside the section at once
std::atomic<int> inside{0}, max_inside{0};
std::vector<std::jthread> ts;
for (int i = 0; i < 3; ++i)
    ts.emplace_back([&] {
        slots.acquire();
        int n = ++inside;
        int m = max_inside.load();
        while (m < n && !max_inside.compare_exchange_weak(m, n)) { }
        std::this_thread::sleep_for(5ms);
        --inside;
        slots.release();
        ready.count_down();
    });
ready.wait();
```

```text
worker stopped cleanly, ticked at least once: 1
blocked waiter released by stop request: 1
latch released; max concurrent inside semaphore section: 2 (limit 2)
```

## 6. 线程池、任务划分的几条经验

* 线程数 ≈ 核数（CPU 密集型），I/O 密集可更多；不要为每个小任务建线程。
* 优先「分块 + 各自累加 + 最后合并」而不是所有线程争一个共享变量。
* 共享可变状态越少越好；能用「每线程私有 + 合并」就不要锁。

## 7. 坑

1. **忘记 join/detach** → `terminate`。
2. **`wait` 不带谓词** → 虚假唤醒导致错误。
3. **先判断后加锁**：`if (!q.empty()) { lock; q.pop(); }`——判断和操作之间被别人改了；判断必须在锁内。
4. **返回持锁保护的数据的引用**，出了锁就是数据竞争。
5. **按不同顺序加多个锁**。
6. **在持锁时 `notify` 并立刻等待同一把锁**——只是性能问题；正确性问题是在改状态**之前**通知。
7. **`detach` 的线程访问已销毁的局部变量**。
8. 对同一 `mutex` 重复加锁（不可重入）→ 死锁/UB。
9. `std::thread` 的构造抛 `system_error`（资源不足）；线程数不能无限。

## 8. 面试官接着会问

**Q：`mutex`、`lock_guard`、`unique_lock`、`scoped_lock` 的区别？**
要点：第 3 节；`unique_lock` 更灵活但稍重；`condition_variable` 需要 `unique_lock`。

**Q：为什么 `condition_variable::wait` 要用 while/谓词？**
要点：虚假唤醒；通知与检查之间条件可能变化；谓词版本等价于 `while (!pred()) wait(lock)`。

**Q：怎么避免死锁？**
要点：固定加锁顺序；`scoped_lock`；少持锁、不持锁调用外部代码；超时 `try_lock_for`；死锁四条件。

**Q：实现一个线程安全队列 / 生产者消费者。**
要点：第 4 节代码；`close` 语义；有界 vs 无界；多生产者多消费者用 `notify_all` 或每个条件一个 cv。

**Q：`std::async` 和 `std::thread` 的区别？**
要点：`async` 返回 future、能传回结果和异常；默认策略可能延迟执行（用 `launch::async` 强制）；`future` 析构会阻塞等待（如果来自 async）。

**Q：C++ 线程和 Java 线程在语义上的主要差别？**
要点：数据竞争 UB；`mutex` 不可重入；没有 `interrupt`（用 `stop_token`）；没有 monitor；线程析构 `terminate`；没有虚拟线程。

**Q：什么时候用 `shared_mutex`？**
要点：读远多于写且读临界区较长；否则 `mutex` 更快（`shared_mutex` 本身更重）。

## 9. 自测

1. `std::thread t(f); ` 之后函数直接返回会怎样？
2. `cv.wait(lk)` 不带谓词的两个风险？
3. `transfer(a, b)` 与 `transfer(b, a)` 同时执行，为什么用 `lock_guard` 两把会死锁？怎么修？
4. `jthread` 比 `thread` 好在哪？

<details><summary>答案</summary>

1. 析构时线程仍 joinable，调用 `std::terminate`。
2. 虚假唤醒；通知丢失时（通知先于等待）永远睡眠；应在锁内检查谓词。
3. 两个线程各持一把等另一把；用 `std::scoped_lock(a.m, b.m)`（或统一顺序）。
4. 析构自动 join（并先请求停止），内置 `stop_token` 协作取消。

</details>
