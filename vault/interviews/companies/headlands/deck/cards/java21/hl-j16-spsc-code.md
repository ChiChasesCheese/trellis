---
id: hl-j16-spsc-code
node: java21.j16-concurrency-primitives
type: qa
step: 31
---
## Q
用 `VarHandle` 的 release/acquire 写一个无锁单生产者单消费者（SPSC）环形队列的 `offer` 和 `poll`。为什么不需要 CAS？

## A
```java
boolean offer(long v) {                       // 生产者
    long t = tail;                            // 自己写的，普通读
    long h = (long) HEAD.getAcquire(this);    // 读对方的进度
    if (t - h == buf.length) return false;    // 满
    buf[(int) (t & mask)] = v;                // 1. 先写数据
    TAIL.setRelease(this, t + 1);             // 2. release 发布
    return true;
}
long poll() {                                 // 消费者
    long h = head;
    long t = (long) TAIL.getAcquire(this);
    if (h == t) return Long.MIN_VALUE;        // 空
    long v = buf[(int) (h & mask)];
    HEAD.setRelease(this, h + 1);             // 归还槽位给生产者
    return v;
}
```
`head` 只有消费者写、`tail` 只有生产者写，各有**唯一写者**，所以不需要 CAS。5000 万个数校验和精确一致；这是 LMAX Disruptor 的核心思想。
