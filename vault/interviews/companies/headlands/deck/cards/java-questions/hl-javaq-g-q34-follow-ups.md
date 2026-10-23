---
id: hl-javaq-g-q34-follow-ups
node: java-questions.g-os
type: qa
step: 3
---
## Q
追问：在 Java 里对 socket 调阻塞 `read()` 时，内核里发生了什么？一个 JVM 最多能建多少线程？
How many threads can one JVM create?

## A
- **阻塞 `read()`**：线程陷入内核（系统调用）→ 数据没到 → 线程睡眠、让出 CPU → 数据到达触发中断 → 内核把数据拷贝到用户 buffer → 线程被唤醒。
- **线程数上限**：受 OS 限制——`ulimit -u`、内存、`max_map_count`；虚拟线程解决规模问题。
