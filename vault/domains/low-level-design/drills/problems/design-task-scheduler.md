---
nodes: [problems.components.task-scheduler, concurrency.patterns]
tags: [problem]
---
# Drill：任务调度器（Task Scheduler）

一个进程内的调度器（不是分布式任务队列）：调用方交给你一个函数和一个延时/时刻/周期，
调度器负责在合适的时候把它跑起来，支持取消。时间只从注入的时钟来，核心调度逻辑要能在
不涉及任何真实线程、不涉及真实 `sleep` 的情况下被测试。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：调度一个回调在某个延时之后或某个时刻运行一次，支持取消。核心引擎
  暴露一个 `run_pending(now)`：给它一个时间点，同步执行所有到期任务。真正跑线程的调度器只是
  这个引擎外面薄薄的一层。先想清楚"进程忙的时候能保证什么"——只能保证不早于，不能保证恰好。
- 第 2 关（约 20 分钟）：周期任务，**固定速率**和**固定延迟**两种语义，说清一次执行超时
  之后两者分别怎么办。数据结构是一个按到期时间排序的堆。取消要处理"还没轮到就被取消"的
  情况，而且**堆本身不能因为大量取消而无限增长**——想清楚 `heapq` 不支持删除任意元素这件事
  怎么解决。
- 第 3 关（约 15 分钟）：一个工作线程池并发执行到期任务，调度线程只管掐点。一个任务抛出的
  异常不能杀死调度循环，也不能取消它自己未来的调度。`shutdown` 明确选一种行为（等已经派发
  的任务跑完，还是不等直接丢弃排队中的），并且能被测出来。
- 第 4 关（选做）：同一时刻到期的多个任务之间的优先级，或者 cron 式的日历规则——评分点是
  "加它有没有改动堆本身的取出/压缩逻辑"。

**怎么练**：把 `vault/domains/low-level-design/problems/task-scheduler/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/task-scheduler -q`。

**评分点**
- 固定速率的下一次到期在**取出时**按"这次到期时间 + 周期"算，落后了会连续追赶；固定延迟只在**完成之后**按"完成时刻 + 周期"算，永远不追赶（[[problems-task-scheduler-fixed-rate-vs-fixed-delay]]）。
- 取消是一枚墓碑：任务表里的条目立刻删除，堆里的位置留到被取出或被批量压缩时才清理，堆的物理大小不会因为大量取消而无限增长（[[problems-task-scheduler-cancel-is-a-tombstone]]）。
- 调度逻辑的核心锁和调度线程的 `Condition` 是两把不同的锁，所有代码路径只按同一个方向嵌套拿它们，因此不会锁顺序死锁（[[problems-task-scheduler-two-locks-one-direction]]）。
- 固定速率与固定延迟只是一个 `Enum` 加两行 `if`，不需要策略模式的一族类（[[problems-task-scheduler-no-strategy-class-for-two-modes]]）。
- 系统只保证任务"不早于"到期时间执行，从不保证"恰好在"那一刻，落后的固定速率任务会连续追赶而不是被跳过或无限期推迟（[[problems-task-scheduler-not-earlier-never-exactly]]）。
- 优先级加入时只是堆比较键的元组里多一栏，取出、判断到期、压缩这些逻辑一行都不用改（[[problems-task-scheduler-priority-without-touching-heap]]）。
- 执行回调的代码用 `try`/`except BaseException`/`finally` 包住：异常不会传到调度线程，`finally` 保证收尾逻辑（比如固定延迟的重新调度）总会执行（[[problems-task-scheduler-worker-pool-decoupled-from-timing]]）。
- `shutdown` 明确区分 drain（等已派发任务跑完）和 abandon（排队中的直接丢弃），并各自有对应的测试证明（[[problems-task-scheduler-shutdown-drain-vs-abandon]]）。

**题解**：[[solution-task-scheduler]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
