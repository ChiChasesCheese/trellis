---
id: hl-javaq-g-q34-main
node: java-questions.g-os
type: qa
step: 1
---
## Q
进程、线程、虚拟线程有什么区别？上下文切换是什么、代价多大？怎么把线程绑到某个核上？
Process vs thread vs virtual thread: what is a context switch and what does it cost? How do you pin a thread to a core?

## A
一句话：**进程** = 独立地址空间 + 资源；**线程** = 同一进程内共享地址空间的调度单位；**虚拟线程** = JVM 里的用户态线程。

- 进程各有 `[代码|数据|堆|栈]` 和独立虚拟地址空间，互相隔离；线程共享代码、数据、堆，各有独立栈 + 寄存器。
- **上下文切换**：保存 A 的寄存器 → 调度器选 B → 恢复 B 的寄存器；进程间还要切换页表，TLB 部分失效。
- 代价：**直接成本是微秒级**（量级 1–几微秒，常见经验数字），**间接成本（缓存、分支预测变冷）通常更大**。
- Java 的 `Thread` 是 1:1 OS 线程（pthread）；虚拟线程由 JVM 在用户态切换栈。
- Java 标准库没有绑核 API，用 `taskset` / `numactl` 或第三方库。
