---
id: hl-javaq-g-q34-say60
node: java-questions.g-os
type: qa
step: 14
---
## Q
用英文 60 秒回答：Process vs thread vs virtual thread: what is a context switch and what does it cost? How do you pin a thread to a core?

## A
结构：进程与线程的区别 → 上下文切换的直接成本（微秒）与间接成本（缓存变冷）→ 因此一线程一核 → Java 线程 1:1，虚拟线程在用户态 → 绑核用 taskset、numactl、isolcpus 或库。

> "A process has its own address space; threads within a process share it and are what the OS schedules. A context switch saves one thread's registers and loads another's - and for a different process also switches page tables. The direct cost is on the order of microseconds, but the bigger cost is indirect: the cache and branch predictor are cold when you come back. That's why latency-critical systems use a thread per core and avoid blocking. Java platform threads map one-to-one to OS threads; virtual threads are scheduled in user space by the JVM. For pinning, Java has no standard API, so I'd use `taskset` or `numactl` for the process, plus isolated cores via `isolcpus`, or a library such as OpenHFT Affinity for per-thread pinning."
