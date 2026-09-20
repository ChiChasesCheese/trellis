---
id: concurrency-free-threading-pep703
node: concurrency.model
type: qa
step: 6
---
## Q
"free-threaded"（无 GIL）CPython 构建是什么，它对本文讨论的加锁规则有什么影响？

## A
PEP 703 从 Python 3.13 起提供了一个可选的"free-threaded"（自由线程）构建，移除了 GIL，让多个线程可以真正同时执行 Python 字节码——这个构建仍在演进中，尚未成为默认构建。它不改变本文的任何结论，反而让"靠 GIL 保证正确性"这件事更站不住脚：一旦 GIL 消失，连"单条字节码原子"这个最后的隐性保护也不再能默认依赖，复合操作和跨对象不变量必须显式加锁才安全。

结论：无论跑在哪种构建上，`x += 1`、check-then-act、跨对象不变量都应该一直用锁保护——free-threaded 构建只是让不这样做的代价从"某些平台上偶发"变成"更容易暴露"。
