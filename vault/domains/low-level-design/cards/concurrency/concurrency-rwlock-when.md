---
id: concurrency-rwlock-when
node: concurrency.primitives
type: qa
---
## Q
When does replacing a mutex with a read-write lock make your code *slower*, and what failure mode does a naive reader-preferring RW lock add?

## A
- RW locks have **higher per-acquire overhead** (they track reader counts). With short critical sections or few concurrent readers, a plain mutex — or a concurrent data structure — wins.
- It only pays off when reads are **frequent and long** relative to writes.
- Reader-preference adds **writer starvation**: a continuous stream of readers keeps the write lock unavailable forever. Fair/writer-preferring modes fix this at the cost of read throughput.

Also: upgrading read → write while holding the read lock deadlocks in most implementations — release, reacquire, and re-validate instead.

## Q zh
读写锁什么时候有益，什么时候会伤害性能？

## A zh
**有益于**：
- 读远多于写（比例 10:1 或更高）
- 读操作计算密集且长期持有锁
- 例子：缓存读者多，偶尔写入器

**伤害性能**：
- 读和写大致相等
- 读操作很快（微秒）
- 线程计数低（竞争很少）
- 例子：计时器、计数器、单写数据结构

为什么伤害：
- 获取读锁的开销 > 独占 mutex
- 在低竞争下，mutex 通常赢
- 读写锁实现更复杂，缓存不友好

经验法则：测量。单独的 mutex 可能更简单且更快，除非你有证据证明大量读竞争。
