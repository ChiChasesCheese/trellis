---
id: hl-os-qa-context-switch
node: foundations.os-processes-threads-ipc
type: qa
step: 36
---
## Q
面试题：上下文切换为什么贵？

## A
推荐答法：「直接成本是进内核、存取寄存器、调度，约一到几微秒；更大的是间接成本：缓存、TLB、分支预测器被新线程污染要重新预热，跨核醒来缓存全冷。我测过阻塞式交接 `park/unpark` 往返约 2.5–3 µs，忙等往返约 90 ns，所以低延迟系统把热线程绑核自旋。」
