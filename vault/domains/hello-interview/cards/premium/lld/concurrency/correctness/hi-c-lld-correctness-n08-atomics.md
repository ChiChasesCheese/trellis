---
id: hi-c-lld-correctness-n08-atomics
node: lld.concurrency.correctness.notes
type: qa
step: 8
---
## Q
**并发正确性 · 原子变量与 CAS**｜摘要 · 必会

原子变量怎么工作？比较并交换（CAS）循环怎么用？Python 里怎么办？

## A
- **原理：** 用 CPU 指令一步完成读改写，不加锁；CAS 的意思是"仅当当前值等于期望值才设新值"，失败说明有人改过，返回 false
- **CAS 循环：** 读当前值、算新值、尝试 CAS，失败就重读重试；例：记录历史最大并发数
- **乐观并发：** 假设没人干扰，冲突了才重试，低竞争下比锁快
- **Python：** 没有原生原子变量也没有 CAS，GIL 不让操作原子；用锁模拟，或多进程的 `Value`
- **面试说法：** 单个计数器或标志，用原子整数
