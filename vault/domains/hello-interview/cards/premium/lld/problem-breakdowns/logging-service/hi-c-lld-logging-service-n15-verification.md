---
id: hi-c-lld-logging-service-n15-verification
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 14
---
## Q
**日志库 · 验证：三个场景**｜摘要 · 必会

实现完用哪三个场景验证设计？每个场景应该看到什么？

## A
- **场景一，阈值：** 控制台目的地阈值 DEBUG，文件目的地阈值 WARN，调用 `info("user logged in")`。控制台写一行，文件目的地判断 INFO < WARN 后静默丢弃。两个目的地各自独立用自己的阈值决定。
- **场景二，并发：** 两个线程同时 `error(..)` 同一个文件目的地。两边都可以并行格式化（纯函数），然后抢锁：A 拿到先写，B 等待，A 释放后 B 写。结果是两条记录各自完整，没有交错字节；先后顺序是拿锁顺序，不是调用顺序，这符合需求。需要严格的每目的地顺序就要上异步队列。
- **场景三，失败：** 磁盘满，文件 sink 每次都抛。同一次 `warn("disk space low")`：控制台正常输出，文件目的地捕获异常并在 stderr 写一行诊断，`Logger.log` 正常返回，应用不知道发生过什么。一个目的地的失败不扩散。
- **要点：** 主动走一遍，比等面试官发现 bug 更好。
