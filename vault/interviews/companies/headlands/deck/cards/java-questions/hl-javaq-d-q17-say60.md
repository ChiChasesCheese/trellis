---
id: hl-javaq-d-q17-say60
node: java-questions.d-memory
type: qa
step: 34
---
## Q
用英文 60 秒回答：How do CPU caches affect Java performance? Why is `long[]` faster than `List<Long>`? What is false sharing?

## A
结构：64 字节缓存行与预取 → long[] 连续、List<Long> 追指针 → 实测数字（约 10 倍）→ 伪共享是多线程版本 → 填充或分条（LongAdder）。

> "The CPU fetches memory in 64-byte cache lines, so contiguous arrays get both locality and hardware prefetching, while pointer chasing misses cache - roughly 100 nanoseconds per miss compared to a nanosecond for L1. In Java a `long[]` is contiguous but a `List<Long>` is an array of references to separate objects. In my test summing 12 million elements took a couple of milliseconds for the primitive array, about the same for boxed longs walked in allocation order, but around ten times longer once the reference order was shuffled. False sharing is the multi-threaded version: two threads writing different variables on the same cache line keep invalidating each other's copy; the fix is padding or striping, which is what `LongAdder` does internally."
