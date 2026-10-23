---
id: hl-j10-promise
node: java21.j10-virtual-threads
type: qa
step: 6
---
## Q
虚拟线程（virtual thread）的承诺是什么？它是哪个版本转正的、是语言特性还是运行时特性？

## A
承诺：**保留同步、阻塞、栈清楚的写法，去掉线程的昂贵**。线程极便宜，于是「一任务一线程」，不用池；限流改用别的手段（如 `Semaphore`）。

版本：Java 19、20 为预览，**Java 21 正式**。

它是**纯运行时（JVM + JDK 库）特性**，没有新语法，编译器几乎什么都没做。阻塞 API（`Thread.sleep`、`Object.wait`、`BlockingQueue.take`、`Lock.lock`、`socket.read`）照常可用，这就是卖点：**阻塞 API 不用改**。
