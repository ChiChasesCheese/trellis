---
id: pl-functional-recursion-tco-foundation-java-stack-size
node: functional.recursion-tco
type: qa
step: 4
---
## Q
Java 的 `StackOverflowError` 是什么？默认能递归多深，怎样调整？

## A
JVM 的每个线程有固定大小的栈，默认约 1 MB（取决于平台，`-Xss` 可调整；主线程由操作系统决定）。超出时抛出 `StackOverflowError`，它是一个 `Error`（不是 `Exception`），**可以捕获**，但抛出时线程状态可能已经半途而废，不建议当作正常控制流。

一个最简单的无限递归，实测（Java 25，macOS，默认栈大小）：

```java
static int depth = 0;
static void down() { depth++; down(); }
// 捕获 StackOverflowError 后 depth 约 4.5 万（两次测量 45382、44654）
```

这是栈帧很小的极端情况；真实代码的栈帧里有更多局部变量，深度通常只有几千到一两万。同一份代码，被 JIT 编译前后的栈帧大小不同，所以溢出深度并不固定。

调整方式：

- 全局默认：`-Xss16m`，所有新线程的栈 16 MB；
- 单个线程：`new Thread(null, runnable, "name", 64 * 1024 * 1024)`，第四个参数是栈大小，常用来给"确实需要深递归"的任务开一个大栈线程。

虚拟线程（Java 21）的栈保存在堆上，可以按需增长，不占用固定的操作系统线程栈。HotSpot 不做尾调用优化，所以前面那个尾递归的 `loop` 在深度一百万时同样会溢出。
