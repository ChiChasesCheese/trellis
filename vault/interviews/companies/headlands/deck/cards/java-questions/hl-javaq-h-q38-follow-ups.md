---
id: hl-javaq-h-q38-follow-ups
node: java-questions.h-ipc
type: qa
step: 3
---
## Q
追问：两个进程在共享内存上怎么同步？忙等（busy-spin）有什么缺点、怎么缓解？
How do you synchronise two processes on shared memory? What are the downsides of busy-spinning?

## A
- **同步**：原子序号 + 单生产者单消费者环形缓冲，用 release / acquire 语义发布。
- **忙等的缺点**：占满一个核、耗电、超线程兄弟线程受影响。
- **缓解**：循环里调 `Thread.onSpinWait()`，或退避若干次后 `park`。
