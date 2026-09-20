---
id: problems-airline-atomic-cross-segment
node: problems.booking.airline
type: qa
step: 4
tags: [grown]
---
## Q
航班管理设计里，一条跨两段航班的中转行程要“要么全订上、要么一段都不订”，`FlightInstance.reserve_across` 是怎么做到的，为什么不会死锁？

## A
把涉及的所有 `FlightInstance` 按各自的 `key`（航班号@日期）排序，用 `ExitStack` 依次进入每一把私有锁、全部持有之后，再做“先查完所有段的余量，都够才写入所有段”的两段式操作。固定的全局加锁顺序是不死锁的全部理由：任何两个线程无论构造哪条行程，最终都会按同一个顺序申请锁，不可能出现一个等另一个、另一个又等它的环形等待。
