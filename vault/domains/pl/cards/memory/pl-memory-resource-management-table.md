---
id: pl-memory-resource-management-table
node: memory.resource-management
type: qa
step: 6
---
## Q
Go、Java、Rust、Python 各用什么机制管理非内存资源？换来什么，代价是什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Go | `defer`，函数级、后进先出 | 获取与释放写在相邻两行，对错误处理友好 | 以函数而非块为作用域，循环里会堆积；可以忘记写 |
| Java | try-with-resources 加 `AutoCloseable` | 块级作用域，异常抑制（suppressed）保留原始异常 | 调用者必须使用该语法，忘了就泄漏；`finalize` 已弃用 |
| Rust | `Drop`，资源与类型绑定 | 无法忘记，内存和资源一套机制，panic 时也执行 | `Drop` 不能返回错误，也不保证一定运行 |
| Python | `with` 加上下文管理器 | 块级作用域，`__exit__` 能看到并处理异常 | 可以忘记；`__del__` 的时机因实现而异 |

逻辑：这四种选择排成一条「强制程度」的光谱。Rust 靠类型强制；Java、Python 靠语法提供便利，但不强制；Go 靠约定，`defer` 是一个轻量机制，符合它「少即是多」的哲学：不引入新的类和接口协议，只加一条语句。

Java、Python 与 Go 需要 linter 或代码评审来兜底「是否使用了作用域语法」；Rust 把这件事变成类型不变量，代价是 `Drop` 的限制（不能返回错误、不能异步）。
