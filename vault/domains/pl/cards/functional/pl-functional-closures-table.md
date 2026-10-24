---
id: pl-functional-closures-table
node: functional.closures
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 的闭包捕获语义有什么区别？各自的代价是什么？

## A
| 语言 | 捕获什么 | 能修改吗 | 生命周期保证 | 代价 |
|---|---|---|---|---|
| Go | 变量（引用） | 能，共享 | 逃逸到堆，GC | 堆分配，并发时有数据竞争 |
| Java | 值的拷贝 | 不能（effectively final） | 值已复制 | 状态要包进对象 |
| Rust | 引用或所有权（由使用方式推导，可 `move`） | 视 `Fn`/`FnMut`/`FnOnce` | 借用检查器 | 编译期约束，类型复杂 |
| Python | 变量（cell） | 需要 `nonlocal` | 引用计数 | 晚绑定陷阱 |

规律：**共享变量的语言**（Go、Python）灵活直观，却会在循环和并发里产生意外；**复制或独占的语言**（Java、Rust）不会产生联动，但限制修改。

Java 做出限制，是因为设计者担心 lambda 在多线程里共享可变局部变量会产生难以排查的并发错误，宁可在编译期禁止。Go 的取向是简单直观，由工具补充（`go vet` 的 loopclosure 检查、race detector）。Rust 要保证内存与并发安全而无需 GC，所以把捕获模式写进类型。Python 的 cell 是为了让嵌套函数这个特性实现起来简单，晚绑定是自然的结果，而不是刻意设计。

结论：同样叫闭包，可变性、共享性、生命周期这三个维度上各语言取值不同，写跨语言的代码时需要逐个确认。
