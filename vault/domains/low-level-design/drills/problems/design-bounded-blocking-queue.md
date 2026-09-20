---
nodes: [problems.components.bounded-blocking-queue, concurrency.primitives]
tags: [problem]
---
# Drill：有界阻塞队列（Bounded Blocking Queue）

从零实现一个容量固定的线程安全队列：满则 `put` 阻塞，空则 `take` 阻塞，多个生产者和
多个消费者可以同时用它。这是并发主题里最经典的条件变量练习——没有业务建模，所有分数
都在"锁 + 等待谓词"这套机制是不是准确到每一行。照真实机考的节奏分关来做，做完一关再
看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`put`／`take`，满则阻塞、空则阻塞，先不考虑超时和关闭。硬要求
  是等待必须写成 `while 谓词: cond.wait()`，绝不能是 `if`；想清楚为什么。
- 第 2 关（约 15 分钟）：设计问题——如果两个方向的等待共用同一个 `Condition`，只用
  `notify()` 会发生什么？把它实现成两个 `Condition`（`_not_full`、`_not_empty`）共享同一
  把锁，并说清楚这样做既不丢信号也不惊群。
- 第 3 关（约 15 分钟）：加 `timeout` 参数（超时统一抛异常，说清楚为什么不是返回哨兵值
  或布尔值）；加 `close()`——唤醒所有等待者，之后 `put` 立即失败，`take` 把关闭前已有的
  元素放完才失败。
- 第 4 关（选做）：加 `drain(max_items=)` 给批量消费者用，且不能碰前面已经调对的等待
  逻辑——叫醒之后有多少拿多少，不为凑够 `max_items` 再等一轮。

**怎么练**：把
`vault/domains/low-level-design/problems/bounded-blocking-queue/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/bounded-blocking-queue -q`。

**评分点**
- 等待循环写成 `while` 而不是 `if`，并说得出虚假唤醒和"被唤醒后条件又被别人抢先改回去"
  这两条理由（[[problems-bounded-blocking-queue-while-not-if]]、[[concurrency-condvar-wait-loop]]）。
- 用两个 `Condition` 共享同一把锁，而不是一个共享 `Condition`，并说得出这样既不丢信号
  也不惊群（[[problems-bounded-blocking-queue-two-conditions-vs-one]]、[[concurrency-bounded-queue-invariants]]）。
- 能推演出"单条件变量 + `notify()`"为什么会丢信号、最终让所有线程永久阻塞
  （[[problems-bounded-blocking-queue-single-notify-lost-signal]]、[[concurrency-single-condvar-lost-signal]]）。
- 超时统一抛异常而不是返回哨兵值或布尔值，说得出哨兵值在什么场景下会和合法数据混淆
  （[[problems-bounded-blocking-queue-timeout-raises]]）。
- `close()` 之后 `put` 立即失败、`take` 排空已有元素才失败，两者故意不对称
  （[[problems-bounded-blocking-queue-close-semantics]]）。
- 不为 `close()` 引入 `threading.Event`，说得出为什么受锁保护的 `bool` 加已有的
  `notify_all()` 就是完整答案（[[problems-bounded-blocking-queue-close-no-event]]）。
- `drain` 复用 `take` 已经验证过的等待谓词，不新增一套"等到凑够数量"的逻辑
  （[[problems-bounded-blocking-queue-drain-reuses-wait]]）。
- 用 `waiting_putters`／`waiting_takers` 之类的可断言状态确认线程真的阻塞了，而不是靠
  `sleep` 赌时长（[[problems-bounded-blocking-queue-waiting-counts-for-tests]]）。
- 并发测试断言不变式（不超员、不丢不重、恰好一个线程抢到刚腾出的位置），一句依赖具体
  耗时的断言都没有（[[problems-bounded-blocking-queue-two-conditions-vs-one]]）。
- 知道生产代码里遇到"要一个有界阻塞队列"的需求，默认答案是直接用 `queue.Queue`
  （[[concurrency-producer-consumer-queue]]），自己写一遍的价值仅限于像这样的面试场景。

**题解**：[[solution-bounded-blocking-queue]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
