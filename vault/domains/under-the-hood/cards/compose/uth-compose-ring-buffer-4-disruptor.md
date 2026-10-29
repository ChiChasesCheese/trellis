---
id: uth-compose-ring-buffer-4-disruptor
node: compose.ring-buffer
type: qa
step: 4
---
## Q
**真实实现多做了什么**｜Disruptor · 4.0.0

LMAX Disruptor 在这个骨架上加了什么？它和 `ArrayBlockingQueue` 的取舍有什么不同？

## A
**细节。**

- 预分配：构造时用 `EventFactory` 填满事件对象，之后只改字段、不再 `new`，减少垃圾回收停顿；发布分两步：`next()` 占序号，填字段，`publish(seq)`
- 不覆盖未读：`next()` 比较「序号减容量」与所有消费者序号的最小值，追上了就停下来等
- 多生产者：`getAndAdd(n)` 原子抢序号；抢到不等于写好，所以 `availableBuffer` 记每个槽发布到第几圈，消费者只读连续已发布的部分
- 批处理：消费者一次拿到最大可读序号，整批处理完才写一次自己的序号
- 防伪共享（false sharing）：`Sequence` 的 `long` 前后各垫 56 字节，事件数组两头各多 32 个槽

**为什么。** `ArrayBlockingQueue`（JDK 21）同样是环形数组，但用 `takeIndex`、`putIndex`、`count` 加一把锁，两端每次操作都争这把锁。

**坑。** `next()` 后忘了 `publish`（异常时没放进 `finally`），这个序号永远读不到，后面的事件全被卡住。槽里的对象反复复用，填字段要全部覆盖。

**对应 LeetCode：** 无直接对应的题
