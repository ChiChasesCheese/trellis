---
id: concurrency-deadlock-detect-vs-prevent
node: concurrency.hazards
type: qa
---
## Q
Asked to "make sure this can't deadlock" in a coding round: what do you build, and what belongs to detection instead?

## A
**Prevent by construction** — that's what's gradable in an hour:

- One global lock order, or better, **one lock** for a small design (say out loud that you chose coarse-grained for correctness first).
- `tryLock(timeout)` + release-all + jittered retry where ordering is impossible — breaks hold-and-wait, but you must handle the failure path.
- **Never call an alien/callback method while holding a lock** (listeners, comparators, user strategies) — you can't know what it locks, so ordering is unprovable.

**Detection** is a production/runtime tool, not a design: a wait-for-graph cycle check, `jstack`/`ThreadMXBean.findDeadlockedThreads`, watchdog timeouts. Mention it as diagnosis and recovery (kill/restart a victim), then go back to prevention.

## Q zh
Deadlock 检测和预防之间有什么权衡？

## A zh
**Deadlock 预防**（在死锁发生前阻止）：
- 打破四个必要条件之一（锁定顺序、超时等）
- 成本：开销（超时检查）、性能（严格的锁定规则）
- 优势：避免死锁开销

**Deadlock 检测**（等待并响应）：
- 让死锁发生，然后检测
- 成本：等待时间，然后恢复（通常重启或回滚）
- 优势：允许更灵活的锁定模式

实践中：
- 大多数应用使用预防（超时、一致的锁定顺序）
- 数据库系统常使用检测和事务回滚
