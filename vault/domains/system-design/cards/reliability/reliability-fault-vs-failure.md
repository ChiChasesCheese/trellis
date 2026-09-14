---
id: reliability-fault-vs-failure
node: reliability.availability
type: qa
---
## Q
Fault vs failure (DDIA framing): what is the difference, and what does that make "fault tolerance" mean in practice?

## A
- **Fault**: one component deviates from spec (a disk dies, a node returns garbage, a network link drops packets).
- **Failure**: the *system as a whole* stops providing its service to the user.

Fault tolerance = designing so faults do **not** escalate into failures — you cannot reduce fault probability to zero, so you contain faults instead. Corollary: deliberately *inducing* faults (killing processes, injecting latency) is how you prove the containment machinery works — see [[reliability-chaos-hypothesis]].

## Q zh
Fault vs failure（DDIA 框架）：区别是什么，那使"fault tolerance"在实践中意味着什么？

## A zh
- **Fault**：一个组件偏离规范（磁盘死、节点返回垃圾、网络链接丢包）。
- **Failure**：*整个系统*停止向用户提供其服务。

Fault tolerance = 设计使 fault**不会**升级为 failure——你不能将 fault 概率减少到零，所以你改为遏制 fault。推论：故意*诱发* fault（杀进程、注入延迟）是你证明遏制机器工作的方式——见 [[reliability-chaos-hypothesis]]。
