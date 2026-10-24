---
id: pl-memory-manual-raii-best-practice
node: memory.manual-raii
type: qa
step: 5
---
## Q
RAII 与手动管理的最佳实践是什么？Rust、C++ 与 Go、Java、Python 里各自怎么写才安全？

## A
核心原则：**让释放和获取绑在一起，别让它们之间隔着可能提前退出的代码**。

- **Rust / C++（RAII）**：把每个资源放进一个拥有它的类型里，由 `Drop`（析构）释放。不要在 `Drop` 里做必须成功的事（如提交事务、刷盘并检查错误）：`Drop` 不能返回错误，也可能因 `mem::forget`、abort 而不运行。这类动作写成显式的 `commit()`/`close()` 方法并返回 `Result`，`Drop` 只做兜底清理。C++ 的「零法则」（rule of zero）：尽量不自定义析构，组合已有的 RAII 类型（`unique_ptr`、`vector`）。
- **Go**：`defer` 紧跟在获取资源成功之后，这样提前 `return` 不会漏掉；对写入型资源（文件、网络连接）要检查 `Close` 的返回值，因为数据可能在 `Close` 时才真正写盘。不要在长循环里 `defer`，它要等整个函数结束才执行。
- **Java**：一律 try-with-resources，不要手写 `finally` 里 `close()`，后者在异常叠加时会丢失原始异常。
- **Python**：一律 `with`，不要依赖对象被销毁时自动关闭，那是 CPython 的实现细节。
- **C**：每个函数入口、出口只留一个清理标签（`goto cleanup`），并用 AddressSanitizer 和 Valgrind 跑测试。

为什么：释放遗漏几乎总是发生在错误路径，最不常被测试的地方。把释放绑定到作用域，就把「记得在每条路径上写」变成「语言保证」。

什么时候违反：资源的生命周期跨越作用域（连接池、缓存），这时需要一个明确的所有者对象，在自己的 `close()` 里统一释放。
