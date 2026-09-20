---
nodes: [problems.components.thread-pool, concurrency.patterns]
tags: [problem]
---
# Drill：线程池（Thread Pool）

从零实现一个固定数量工作线程的线程池：`submit(fn, *args)` 返回一个 `Future`，任务在
后台跑，结果或异常通过 `Future` 拿回来；池子能优雅关闭。这道题直接站在
[[design-bounded-blocking-queue|有界阻塞队列]]的基础上——工作线程从队列取任务，就是
那道题里"消费者取元素"的翻版。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：固定数量的 worker 线程从共享队列取任务执行，`submit` 返回一个
  `Future`（能 `result()`、`exception()`、`add_done_callback()`）。硬要求：一个任务抛出
  异常绝不能让它所在的 worker 退出，之后提交的任务照样要能被同一个 worker 处理。
- 第 2 关（约 15 分钟）：`shutdown(wait=True)` 等全部已提交任务（排队的和正在跑的）跑完；
  `shutdown(wait=False)` 立即返回，放弃队列里还没被取走的任务（它们的 `Future` 要收到
  一个明确的异常），但正在执行的任务不受影响。想清楚：`shutdown()` 之后再 `submit()`
  应该发生什么？
- 第 3 关（约 15 分钟）：设计问题——如果提交速度长期超过处理速度，队列会不会无限膨胀？
  实现一种背压策略（推荐：让 `submit()` 在队满时阻塞调用方），并说清楚另外两种策略
  （直接拒绝、在调用方线程上直接跑）的代价，以及 `concurrent.futures.ThreadPoolExecutor`
  自己在这件事上的真实选择。
- 第 4 关（选做）：给任务加优先级，且不能碰 worker 循环的代码。

**怎么练**：把 `vault/domains/low-level-design/problems/thread-pool/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/thread-pool -q`。

**评分点**
- worker 循环里用 `except BaseException` 兜住任务体的一切异常，说得出为什么不是更常见的
  `except Exception`（[[problems-thread-pool-base-exception-in-worker]]）。
- 背压包在 `submit()` 前面的信号量上，而不是给内部队列本身设 `maxsize`，说得出这样能
  避免 `shutdown()` 投递哨兵时被队满卡住（[[problems-thread-pool-backpressure-semaphore-not-queue-maxsize]]、[[concurrency-thread-pool-backpressure]]）。
- 信号量许可在 worker『取到任务』时释放，而不是『任务跑完』时释放，说得出这控制的是
  排队容量而不是并发度（[[problems-thread-pool-admission-release-on-dequeue]]）。
- `shutdown(wait=False)` 只放弃排队中的任务，说得出为什么正在执行的任务没法被安全打断
  （[[problems-thread-pool-shutdown-wait-false-only-abandons-queued]]）。
- `Future` 完成时"设置标志"与"取出并清空回调列表"是同一次加锁下的原子操作，说得出不这样
  做会漏掉哪个回调（[[problems-thread-pool-finish-atomic-check-then-act]]、[[concurrency-check-then-act]]）。
- 队列条目参与比较时只留优先级和序号，`fn`／`Future` 显式 `field(compare=False)`，说得出
  不这样做会在什么情况下抛 `TypeError`（[[problems-thread-pool-priority-queue-tie-break]]）。
- 拒绝给 `Future` 做一个四态状态机，说得出为什么两态（完成/未完成 + 结果或异常）已经
  覆盖全部需求（[[problems-thread-pool-future-two-state]]）。
- 说得出 Python 线程池只对 I/O 密集型任务有意义，CPU 密集型该换
  `multiprocessing`（[[problems-thread-pool-cpu-vs-io]]、[[concurrency-cpu-vs-io-bound-choice]]、[[concurrency-gil-definition]]）。
- 能对照 `concurrent.futures.ThreadPoolExecutor` 说出它的队列无界、永不拒绝，以及
  `submit()` 返回的 `Future` 具体给了调用方什么（[[concurrency-threadpool-future]]）。
- 并发测试用 `Barrier` 断言峰值并发度恰好等于 worker 数、用可断言的计数（而不是
  `sleep`）确认背压真的挡住了调用方。

**题解**：[[solution-thread-pool]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
