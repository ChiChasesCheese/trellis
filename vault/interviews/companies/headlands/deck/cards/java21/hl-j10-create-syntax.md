---
id: hl-j10-create-syntax
node: java21.j10-virtual-threads
type: qa
step: 7
---
## Q
写出 Java 21 创建并启动虚拟线程的三种写法（`ofVirtual().name(..).start`、`startVirtualThread`、`unstarted`），并对照写出平台线程的 builder。

## A
```java
Thread t  = Thread.ofVirtual().name("v-1").start(() -> work());
Thread t2 = Thread.startVirtualThread(() -> work());   // 最短，无名字
Thread t3 = Thread.ofVirtual().name("v-", 0).unstarted(() -> work());
t3.start();                                            // 名字自动编号 v-0, v-1...
Thread p  = Thread.ofPlatform().name("p-1").start(() -> work());
```
`Thread.ofVirtual()` 返回 `Thread.Builder.OfVirtual`；`Thread.ofPlatform()` 返回 `Thread.Builder.OfPlatform`（可设优先级、栈大小、守护）。两种 builder 都有 `.factory()`，得到的 `ThreadFactory` 可交给任何接受 `ThreadFactory` 的 API。
