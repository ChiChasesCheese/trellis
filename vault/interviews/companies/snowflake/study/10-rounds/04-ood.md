# 04 · OOD / 类设计（电面或 onsite，45 min）

> 本轮全部题目（含 GitHub 蒸馏补充的新题，按 28 法则排序）：[`../../CONTENTS.md`](../../CONTENTS.md) §04_ood。本文件里点名的题是示例，不是全集。

> 事实层在 `../../loop/LOOP_GUIDE.md` §4–§5；题目证据 `../../catalog/raw/ood.md`。本章：**怎么练**。

## 这轮到底考什么（一句话）

**先定 API 契约与不变量，再写状态，最后接住并发追问。** 一手挂经（Task Scheduler addTask/executeTask，同 task 可在不同 timestamp 重复 add）就是契约没问清：重复 ID 算覆盖、并存、还是执行后全部失效？

`raw/ood.md` 的横向结论：**10 道 OOD 里 5 道有明确的并发 / 分布式正确性追问**。默认它会来。

## 45 分钟怎么走

| 时间 | 做什么 | 出声说什么 |
|---|---|---|
| 0–5 | 问契约：方法签名、返回值、错误、重复/空/并发调用的语义 | "If the same id is added twice, do both live, does the second overwrite, or does executing one kill the other?" |
| 5–10 | 写类骨架 + 不变量注释 + 复杂度目标 | "Invariant: the heap never holds an executed id; execute is O(log n) amortized." |
| 10–25 | 实现 part 1 + 自测 | 3 个 assert：空、tie-break、重复 |
| 25–35 | part 2（语义扩展：重复 ID / 嵌套事务 / 多规则） | 改数据结构前先说为什么 |
| 35–43 | **并发追问**：锁在哪、什么必须原子、怎么测 | "The check-and-pop must be atomic; one lock around it, reads can stay lock-free because…" |
| 43–45 | 持久化 / 多实例一句话 | "Append-only op log + periodic snapshot; replay on restart." |

## 必做题

| 顺序 | 题 | 要点 | 命令 |
|---|---|---|---|
| 1 | od01 Priority Task Scheduler | 优先级 → 早时间戳 → 小 id；执行后同 id 全失效（懒删除）；threading 测 exactly-once | `mock.py start od01 -m 45` |
| 2 | od02 In-Memory File System | trie；rm/rmdir；分块；每路径锁 | `mock.py start od02` |
| 3 | od03 Transactional KV | 撤销日志栈；嵌套 commit 合并到父层；每线程栈 | `mock.py start od03` |
| 4 | od04 Rate Limiter | 单规则 deque → 多规则找"所有规则同时有余量的最早时刻" → try_acquire 原子 | `mock.py start od04` |
| 5 | od05 Cron Scheduler | `*/n` 子集；pause 与 claim 竞态；两实例 lease 不双触发 | `mock.py start od05` |
| 6 | od09 Queue → Service | ack + visibility timeout；崩溃后未 ack 重投、已 ack 永不重投 | `mock.py start od09` |
| 7 | od06 Query Audit Log | 时间窗查询；未访问集合别做 O(n²) 索引（参考解踩过） | `mock.py start od06` |
| 8 | od08 LRU / TTL | 哈希 + 双向链表 O(1)；过期优先淘汰；冷热两级 | `mock.py start od08` |

## 并发追问的标准答法（每题都套得上）

1. **找临界区**：哪两个操作交错会破坏不变量？（check-then-act：`if not executed: execute`）
2. **最小锁**：一把锁包住临界区；读路径能否无锁（不可变快照 / copy-on-write）。
3. **粒度升级**：热点时按 key/路径分段锁；说出死锁风险与加锁顺序。
4. **分布式版本**：单机锁换成存储层条件更新（CAS / 唯一约束）+ lease；时钟漂移靠宽租约 + 存储兜底。
5. **怎么测**：N 个线程同时 execute 同一任务，断言恰好一个成功；计数器无丢失更新。

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 不问契约直接写 | 前 5 分钟只问语义，列在注释里让面试官确认 |
| 堆里删除元素 O(n) | 懒删除：执行时跳过已失效 id |
| 嵌套事务 rollback 回滚了父层 | 每层一个 undo map，只记本层首次触碰的旧值 |
| 多规则限流逐个规则判断后分别占位 | 先求所有规则同时满足的时刻，再一次性占位 |
| 说"加锁"但说不出锁什么 | 用"check-then-act 哪两步必须原子"开头 |
| 持久化说"存数据库" | op log + snapshot + replay；说清幂等 |
