---
id: hl-cq-q35-spin-vs-block
node: cpp-questions.h-os
type: qa
step: 17
---
## Q
面试题：上下文切换代价多大？什么时候用自旋（spin）而不是阻塞？用哪些 Linux 工具排查性能？
What does a context switch cost? When do you spin instead of block? Which Linux tools do you use to investigate performance?

## A
- **阻塞等待**：内核把线程挂起再唤醒（系统调用 + 调度器 + 缓存变冷），往返在**微秒级**。
- **忙等（自旋）**：在原子变量上空转，往返**几十到一百纳秒**，但独占一个核。
- 做法：关键线程**绑核**并忙等，其余用阻塞；折中是先自旋一小会儿再阻塞。
- 排查工具：`perf`、`strace`、`top` / `vmstat` / `pidstat`、`ss` 等。
