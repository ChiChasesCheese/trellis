---
id: hl-javaq-e-q23-follow-ups
node: java-questions.e-jit-gc
type: qa
step: 22
---
## Q
ZGC 里的分配停顿（allocation stall）是什么？怎么解决？
What is an allocation stall in ZGC?

## A
- **是什么**：应用分配对象的速度超过 ZGC 并发回收的速度，线程被迫等待回收腾出空间，造成暂停。
- **解决**：加堆（留余量）、降低分配率、加 GC 线程。
- 所以 ZGC 的亚毫秒暂停是以"堆余量充足"为前提的。
