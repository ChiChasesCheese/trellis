---
id: distributed-process-pause-causes
node: distributed.time.failure
type: qa
---
## Q
Distributed algorithms must assume any node can freeze for seconds to minutes at any line of code, then resume as if nothing happened. List the real causes of such pauses, and explain why the paused process cannot defend itself.

## A
Causes, all routine:
- **Stop-the-world GC** — worst-case collections run seconds to minutes on large heaps.
- **VM suspension / live migration** — the whole guest freezes, then resumes.
- **Swapping/page faults and disk stalls** — one memory access or "simple" read blocks on slow I/O.
- **OS-level preemption**: CPU steal on oversubscribed hosts, `SIGSTOP` from an operator or debugger, laptop lid closing (for client software).

Why self-defense fails: the pause is **invisible from inside** — no code runs during it, so there is no hook, and afterwards the thread continues mid-operation with stale beliefs (a lease it thinks is valid, a leadership it thinks it holds). Even `if (lease.stillValid()) write()` is unsound: the freeze can strike **between the check and the write**. Safety therefore must live *outside* the process — fencing tokens at the resource, epoch checks, quorum confirmation.

Mitigations reduce frequency, not possibility: low-pause collectors, heap discipline, disabling swap, and treating a full GC like a planned outage (drain traffic, collect, rejoin).

## Q zh
分布式算法必须假设任何节点都可能在任意一行代码处冻结数秒到数分钟，然后若无其事地继续运行。列举这类暂停的真实原因，并解释为什么被暂停的进程无法自我防御。

## A zh
原因，全都稀松平常：
- **Stop-the-world GC**——大堆上的最坏情况回收可达数秒到数分钟。
- **VM 挂起 / 热迁移**——整个客户机冻结，然后恢复。
- **换页/缺页与磁盘卡顿**——一次内存访问或一个"简单的"读会阻塞在慢速 I/O 上。
- **操作系统层面的抢占**：超卖宿主机上的 CPU steal、运维或调试器发的 `SIGSTOP`、笔记本合盖（对客户端软件而言）。

自我防御为何失败：暂停**从内部不可见**——期间没有任何代码在跑，所以没有钩子；恢复后线程带着过期的信念从操作中间继续（它以为还有效的 lease、它以为还在手上的 leader 身份）。连 `if (lease.stillValid()) write()` 都不可靠：冻结可以恰好打在**检查和写入之间**。因此安全性必须放在进程*外部*——资源侧的 fencing token、epoch 校验、quorum 确认。

缓解手段只能降低频率，不能消除可能性：低停顿收集器、控制堆规模、关闭 swap，以及把一次 full GC 当作计划内停机来处理（先摘流量、回收、再归队）。
