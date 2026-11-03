%% trellis:begin %%
# 竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`
*并发模型：GIL、线程与进程*

理解 `x += 1` 不是原子操作、内建容器的单个方法在 GIL 下原子但复合操作不是、死锁的四个条件与锁顺序，以及线程安全的单例/计数器实现。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]]

**Unlocks:** [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]], [[domains/python/map/craft.patterns.atomic-claim-check-then-act|原子占位：检查与占用在同一个临界区（claim, not check-then-act）]], [[domains/python/map/craft.patterns.idempotency-key-stores-result|幂等键存结果：占位 → 执行 → 保存，重复请求拿到第一次的结果]], [[domains/python/map/craft.patterns.notify-outside-the-lock|锁内记事件、锁外派发（collect under lock, dispatch outside）]], [[domains/python/map/craft.patterns.external-call-outside-the-lock|外部调用不持锁：占位 → 调用 → 提交（claim, call, commit）]], [[domains/python/map/craft.patterns.generation-token-stale-detection|代号/版本令牌：识别并拒绝迟到的旧结果（generation token / fencing）]], [[domains/python/map/craft.patterns.condition-wait-predicate-loop|条件变量：谓词 while 循环 + 精确通知（Condition wait loop）]], [[domains/python/map/craft.patterns.ordered-multi-lock-acquisition|按全局固定顺序拿多把锁（lock ordering）]], [[domains/python/map/craft.patterns.per-key-and-sharded-locks|每个对象一把锁与分片锁：把竞争限制在真正冲突的范围]], [[domains/python/map/craft.patterns.single-flight-coalescing|单飞/请求合并：同一件事只做一次，后到者等结果]], [[domains/python/map/craft.patterns.backpressure-overflow-policy|背压与溢出策略：丢最旧 / 阻塞 / 拒绝，必须当场选并可观测]], [[domains/python/map/craft.idioms.context-managers-for-invariants|上下文管理器守不变量：@contextmanager 与 ExitStack]], [[domains/python/map/craft.idioms.event-wait-and-handoff|Event / Condition 的惯用法：中断式睡眠、结果交接、截止时间]], [[domains/python/map/craft.idioms.decorators-for-cross-cutting-locks|装饰器做横切关注点：@_synchronized / @_op 与 functools.wraps]], [[domains/python/map/craft.idioms.id-generation|ID 生成：itertools.count、next 与生成器表达式的陷阱]], [[domains/python/map/craft.architecture.lock-lives-with-the-invariant|锁跟着不变量走：谁拥有不变量，谁拥有锁（aggregate owns its lock）]], [[domains/python/map/craft.architecture.lock-as-transaction-boundary|一把锁就是一个事务：临界区边界 = 原子性边界]], [[domains/python/map/craft.architecture.lock-hierarchy-and-reentrancy|调用方向与可重入：谁能调谁，回调时手里不能有锁]]

## Readings
- [[effective-09-concurrency-parallelism|Effective Python 3e · 第 9 章 并发与并行]]
- [[fowler-11-synchronization|Python Concurrency with asyncio · 第 11 章 同步原语]]
- [[pydocs-threading-module|threading 模块：线程、锁与同步原语]]

## Drills
- [[concurrency-pick-the-executor|Drill：三个任务，各选线程/进程/asyncio 并说代价]]

## Cards (6)
1. [[condition-while-not-if]]
2. [[deadlock-lock-order]]
3. [[event-vs-lock-purpose]]
4. [[lock-acquire-timeout]]
5. [[lock-vs-rlock]]
6. [[semaphore-vs-bounded]]
%% trellis:end %%

## Notes
