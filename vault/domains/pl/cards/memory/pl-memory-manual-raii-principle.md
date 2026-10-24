---
id: pl-memory-manual-raii-principle
node: memory.manual-raii
type: qa
step: 1
---
## Q
手动内存管理（manual memory management）是什么，会出哪几类错？RAII（Resource Acquisition Is Initialization）为什么被发明，它改变了什么？

## A
手动管理指程序员自己决定何时分配、何时释放堆内存：C 里用 `malloc` 申请、`free` 归还。运行时不替你追踪，所以出错的方式很固定：
1. **泄漏**（leak）：忘了 `free`，内存只增不减。
2. **重复释放**（double free）：同一块内存释放两次，破坏分配器的数据结构。
3. **释放后使用**（use-after-free）：`free` 之后还通过旧指针读写，读到的是别人的数据，写则破坏别人的数据。
4. **悬空指针**（dangling pointer）：指向已经消失的内存，比如返回局部变量的地址。

难点在于：释放的时机分散在每一条控制流路径上，函数中途 `return`、报错退出，都要记得补一次 `free`。

RAII 是 C++ 在 1980 年代提出的惯用法：把资源的生命周期绑定到一个对象的生命周期上。构造对象时获取资源，对象离开作用域时编译器自动调用析构函数（destructor）释放资源。「不会忘」从纪律问题变成了编译器保证：无论函数是正常结束、提前 `return` 还是抛异常，析构都会运行。

于是「释放内存」的设计空间被分成两路：交给程序员手动写，或交给语言机制自动触发（RAII、GC、引用计数）。RAII 的特点是触发时机确定：就在作用域结束那一刻，不需要运行时追踪。
