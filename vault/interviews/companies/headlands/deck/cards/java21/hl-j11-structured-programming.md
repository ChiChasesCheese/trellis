---
id: hl-j11-structured-programming
node: java21.j11-structured-concurrency
type: qa
step: 1
---
## Q
什么是结构化编程（structured programming）？为什么一开线程这个保证就没了？

## A
早年用 `goto` 随意跳转，读代码的人不知道执行流从哪来、到哪去。1968 年 Dijkstra 发表《Go To Statement Considered Harmful》，共识成了结构化编程：只用 `if` / `for` / 方法调用，每个代码块**一个入口、一个出口**，块里开始的事在块结束前一定做完。

单线程里 `f()` 调 `g()`，`f` 返回时 `g` 一定做完。但 `new Thread(() -> g()).start()` 之后：
- `f()` 返回了 `g()` 可能还在跑；
- `g()` 抛异常，`f()` 的调用者永远不知道；
- 线程拿着的资源（连接、文件）可能没人关。
