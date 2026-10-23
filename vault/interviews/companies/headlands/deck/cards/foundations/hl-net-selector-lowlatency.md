---
id: hl-net-selector-lowlatency
node: foundations.networking-basics
type: qa
step: 36
---
## Q
低延迟交易系统里 `Selector` 怎么用得更快？`select()` 和 `selectNow()` 有什么区别？

## A
- `select()` 让线程**睡眠**，被唤醒要经内核调度（往返约 1.5 µs / 次）。低延迟系统用 **`selectNow()` 忙轮询**（不睡眠，立即返回就绪集合），并把线程绑在隔离的核上，以 CPU 换延迟；
- `selectedKeys()` 默认分配迭代器和集合对象，产生垃圾；Netty 用反射换成数组实现；
- 用 `allocateDirect` 并复用，避免每个消息 `new byte[]`。
