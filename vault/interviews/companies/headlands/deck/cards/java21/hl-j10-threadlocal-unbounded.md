---
id: hl-j10-threadlocal-unbounded
node: java21.j10-virtual-threads
type: qa
step: 24
---
## Q
虚拟线程下 `ThreadLocal` 有什么隐患？无界并发又有什么隐患？各自的对策？

## A
**ThreadLocal**：每个虚拟线程有自己的副本，一百万个虚拟线程就是一百万份。原来靠「50 个池线程 → 50 份 `SimpleDateFormat`/缓冲区」省内存的假设崩了，所以别把它当缓存。传请求上下文的新方案是 `ScopedValue`（Java 21 预览，一块只读、随调用作用域生灭的值）。

**无界并发**：以前线程池是天然闸门。去掉它，10 万个虚拟线程同时打数据库会直接打满连接池。**永远要有显式并发上限**：`Semaphore`、连接池大小、令牌桶。
