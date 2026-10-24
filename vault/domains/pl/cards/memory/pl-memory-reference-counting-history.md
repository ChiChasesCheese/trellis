---
id: pl-memory-reference-counting-history
node: memory.reference-counting
type: qa
step: 9
---
## Q
引用计数从最早的提出到今天的 Swift ARC、Python 的新变化，经历了怎样的路线？

## A
1. **1960 年**：Collins 提出引用计数，几乎与追踪式 GC 同时诞生；循环问题当时就已被指出。
2. **1990 年代**：Python 选择引用计数作为主要机制，原因是实现简单、对 C 扩展友好、销毁时机可预测；再加循环检测器（Python 2.0，2000 年）补洞。
3. **2000 年代**：COM、Objective-C 的手动 `retain`/`release` 让程序员自己写加减，漏写即泄漏或崩溃。
4. **2011 年**：Apple 的 ARC 让编译器自动插入 `retain`/`release`，2014 年 Swift 沿用，并加上 `weak`、`unowned` 打破循环。
5. **Rust（2015 年）**：把引用计数降为库功能，只有需要共享所有权时才使用，单线程和多线程分别用 `Rc` 和 `Arc`。
6. **Python 近年**：3.12 引入永生对象（PEP 683），让 `None` 等对象的计数不再变化，减少多进程下的写时复制和缓存争用；3.13 起提供可选的 free-threaded 构建（PEP 703，去掉 GIL），为此重新设计了引用计数。

趋势：引用计数没有消失，而是被放到更小的范围里使用。现代做法是「默认单一所有权或追踪式 GC，只在必要时局部使用引用计数」，同时通过编译器优化消除多余的加减（Swift 和 Rust 都有）。
