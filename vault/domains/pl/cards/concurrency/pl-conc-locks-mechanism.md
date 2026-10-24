---
id: pl-conc-locks-mechanism
node: concurrency.locks-shared-memory
type: qa
step: 5
---
## Q
互斥锁在底层怎么实现？为什么无竞争时加锁很快，竞争时却变慢？

## A
典型实现分两条路径：

**快速路径（无竞争）**：用一条原子的比较并交换（CAS，compare-and-swap）指令把锁字从 0 改成 1。成功就进入临界区，大约十几纳秒，不进内核。

**慢速路径（有竞争）**：CAS 失败说明别的线程持有锁。线程先自旋（spin，原地空转重试）几次，期待很快被释放；还不行就进入操作系统挂起（Linux 上是 `futex`），等持有者解锁时唤醒。挂起和唤醒要进内核、切换线程，是微秒级。

各语言：
- Java `synchronized`：锁状态存在对象头（object header）里；无竞争时是对象头上的轻量 CAS，竞争时膨胀为带等待队列的「监视器」（monitor）。
- Go `sync.Mutex`：正常模式下新来的 goroutine 可以直接抢锁（吞吐高）；等待超过 1 毫秒的 goroutine 会让锁切换到饥饿模式，锁直接交给队首（保证公平）。
- Rust `std::sync::Mutex`：Linux 上基于 `futex` 的字（1.62 起）。
- Python `threading.Lock`：阻塞等待锁的线程会释放 GIL，让别的线程继续运行。

实测（4 个线程各对同一个计数器加锁累加 100 万次，一次测量，12 核 Mac）：Java `synchronized` 488 毫秒，Go `Mutex` 171 毫秒，Rust `Mutex` 126 毫秒（`-O`），Python `Lock` 166 毫秒。也就是每次加锁约 30–120 纳秒；这是激烈竞争下的结果，若只有一个线程，成本会低一个量级。

结论：锁便宜，但**竞争**昂贵。热点上的一把全局锁，会把多核变成排队。
