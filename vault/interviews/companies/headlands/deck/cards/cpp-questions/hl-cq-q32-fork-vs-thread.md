---
id: hl-cq-q32-fork-vs-thread
node: cpp-questions.h-os
type: qa
step: 4
---
## Q
`fork()` 之后子进程把变量 `value` 改成 99，父进程的 `value` 会变吗？同一进程里一个线程把 `value` 改成 42 呢？

## A
- `fork` 后子进程的写**不影响**父进程：父进程的 `value` 仍是 1，因为地址空间是分开的。
- 线程写 `value = 42` 对同进程其他线程**可见**，因为共享同一个地址空间。
