---
id: hl-javaq-f-q31-follow-ups
node: java-questions.f-concurrency
type: qa
step: 23
---
## Q
虚拟线程阻塞时怎么不阻塞 OS 线程？它在低延迟交易热路径里合适吗？`ThreadLocal` 的替代品是什么？
How does a virtual thread block without blocking the OS thread? What replaces `ThreadLocal`?

## A
- **机制**：栈帧拷到堆上，continuation 挂起；I/O 走非阻塞加 poller。
- **热路径**：**不是它的场景**——热路径通常是固定线程 + 绑核 + 忙等；虚拟线程适合研究平台 / 基础设施里的 I/O 并发。
- **`ThreadLocal` 替代**：`ScopedValue`，21 里仍是预览；结构化并发在 21 也是预览。
- 在 21 里 `synchronized` 内阻塞会 pin 载体。
