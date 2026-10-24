---
id: pl-memory-manual-raii-foundation-gc-languages
node: memory.manual-raii
type: qa
step: 4
---
## Q
Go、Java、Python 没有析构函数，它们怎么释放内存和文件这类资源？

## A
这三门语言走的是另一条路：**内存由运行时自动回收**，程序员不写释放代码。

- **垃圾回收**（GC，garbage collection）：Go、Java 的做法。运行时定期找出“已经没有任何引用能到达”的堆对象并回收它们。对象何时被回收由 GC 决定，程序员不能预知。
- **引用计数**（reference counting）：CPython 的做法。每个对象记着“有多少个名字指向我”，计数降到 0 立刻回收。

内存之外的资源（文件、锁、网络连接）不能等 GC 的不确定时机，所以这三门语言各加了一种“块结束时自动执行清理”的语法：
- Java：`try (var f = open()) { ... }`，称 try-with-resources，块结束时自动调用 `f.close()`。
- Python：`with open(p) as f: ...`，块结束时自动调用清理方法。
- Go：`defer f.Close()`，把一次调用登记下来，在当前函数返回时执行。

要记住的一个事实：这三种语法都是“提醒语言替你调用清理”，但调用者仍然必须记得写；而 Rust/C++ 的 RAII 把清理做进类型里，调用者不需要记得。这是两类语言在资源管理上的根本区别。
