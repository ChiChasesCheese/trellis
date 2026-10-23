---
id: hl-j10-pinning-jdk24
node: java21.j10-virtual-threads
type: qa
step: 21
---
## Q
JDK 24 对虚拟线程 pinning 做了什么改变？面试里被问到「`synchronized` 会不会 pin」该怎么答？

## A
JDK 24 让虚拟线程在 `synchronized` 里阻塞也能卸载，`Object.wait()` 同样。仍会 pin 的：栈上有 native 帧；类初始化器（`static {}`）里阻塞或等别的线程初始化类。同时 `jdk.tracePinnedThreads` 被移除，只剩 JFR 事件 `jdk.VirtualThreadPinned`。

**话术**：「在 21 里持锁阻塞要用 `ReentrantLock`；24 起 `synchronized` 不再 pin，但目标版本是 21，所以按 21 的规则写。」
