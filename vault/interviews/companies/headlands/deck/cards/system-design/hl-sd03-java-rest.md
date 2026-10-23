---
id: hl-sd03-java-rest
node: system-design.sd03-low-latency-trading
type: qa
step: 28
---
## Q
Java 热路径的内存布局、并发、线程、字符串 / 装箱 / 流、网络这几项纪律分别怎么做？

## A
- **内存布局**：数据放 `long[]` / `int[]` / 堆外，整数下标代替引用，热字段紧凑，避免对象头与指针追逐；
- **并发**：单写者 + SPSC 环 + `VarHandle` acquire / release；热路径无 `synchronized`、无 `ReentrantLock`、无 `ConcurrentHashMap`；
- **线程**：平台线程，OS 绑核，忙等；**虚拟线程不进热路径**，用于外围（对账查询、重连管理、批处理）；
- **字符串 / 装箱 / 流**：热路径禁用：品种用 `int`，价格用 `long`，日志用预格式化的二进制，延迟日志异步写；
- **网络**：对 Java 而言内核旁路通常通过「对 socket 透明的用户态栈」（Onload 类产品，`LD_PRELOAD`）或 JNI / FFM 调本地库；NIO `Selector` 是普通内核栈下的折中。
