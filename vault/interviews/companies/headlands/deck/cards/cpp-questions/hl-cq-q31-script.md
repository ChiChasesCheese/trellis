---
id: hl-cq-q31-script
node: cpp-questions.g-concurrency
type: qa
step: 22
---
## Q
用英文 60 秒回答：What is false sharing? How would you detect and avoid it?

## A
结构：定义（不同变量同一缓存行，一致性协议来回搬运）→ 实测 404 ms 对 30 ms（13 倍）→ 检测症状与修法（`alignas(64)`、每线程局部状态、队列两个索引分行）→ 代价是内存。

- **False sharing** is when threads write *different* variables that live on the **same cache line**. The coherence protocol must move that line between cores on every write, so the threads serialize even though they share no data.
- I measured four threads incrementing their own atomic counters: adjacent counters took about 400 ms, and the same code with each counter on its own 64-byte line took about 30 ms - a **13x** difference.
- I look for it when scaling is poor with more threads or when I see per-thread slots in an array. The fix is `alignas(64)` padding or per-thread local state merged at the end; in a queue, the producer's and consumer's indices go on **separate lines**.
- The cost is memory, so I only pad hot, contended variables.
