---
id: concurrency-lock-free-trap
node: concurrency.hazards
type: qa
---
## Q
A candidate says "I'll make it lock-free, so no deadlock." Why is this usually the wrong move in an LLD round?

## A
Lock-free removes deadlock but not the hazards that actually bite:

- **CAS covers one word.** Any invariant spanning two fields (`balance` *and* `ledger`) can't be maintained by a CAS loop — you get torn, individually-atomic updates.
- **Livelock/starvation remain**: under contention, CAS retry loops burn CPU and a slow thread can retry forever (lock-*free* guarantees system progress, not per-thread progress; that's wait-free).
- Plus ABA and memory reclamation, and code no reviewer can verify in an hour.

Right answer: use lock-free **components** others wrote — `AtomicLong` counters, `ConcurrentHashMap`, `LongAdder` — and a plain lock for your own multi-field invariants. If contention is the concern, shrink the critical section or shard the lock before going lock-free.

## Q zh
有候选人说"我做成 lock-free，这样就不会死锁了"。为什么在 LLD 轮里这通常是错的一步？

## A zh
Lock-free 消除了死锁，但没有消除真正会咬人的那些危险：

- **CAS 只覆盖一个字**。任何跨两个字段的不变量（`balance` *和* `ledger`）都无法靠 CAS 循环维持 —— 你得到的是撕裂的、各自原子的更新。
- **Livelock/starvation 依然存在**：竞争之下，CAS 重试循环空烧 CPU，慢线程可能永远重试下去（lock-*free* 保证的是系统级进展，不是每个线程的进展；那是 wait-free）。
- 再加上 ABA 和内存回收问题，以及没有哪个评审能在一小时内验证的代码。

正确答案：使用别人写好的 lock-free **组件** —— `AtomicLong` 计数器、`ConcurrentHashMap`、`LongAdder` —— 而你自己的多字段不变量就用一把普通的锁。如果担心的是竞争，先缩小临界区或者对锁分片，再谈 lock-free。
