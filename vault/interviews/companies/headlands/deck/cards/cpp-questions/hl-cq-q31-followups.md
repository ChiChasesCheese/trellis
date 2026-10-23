---
id: hl-cq-q31-followups
node: cpp-questions.g-concurrency
type: qa
step: 21
---
## Q
三个追问：缓存行多大？MESI 是什么？伪共享会影响读吗？

## A
- **缓存行大小**：x86 和多数 ARM 服务器是 64 字节；Apple 近年的核心 L2 行是 128 字节；用标准常量或实测值。
- **MESI**：缓存一致性协议的四个状态——Modified、Exclusive、Shared、Invalid。
- **对读的影响**：只有当有人在写这条线时才有影响；只读共享数据没问题。
