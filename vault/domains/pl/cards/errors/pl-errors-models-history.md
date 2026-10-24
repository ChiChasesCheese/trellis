---
id: pl-errors-models-history
node: errors.models
type: qa
step: 11
---
## Q
错误处理模型是怎么演变到今天的？现在的趋势是什么？

## A
1. **C（1970 年代）**：返回 -1 加全局变量 `errno`；`setjmp`/`longjmp` 做非局部跳转。简单但容易被忽略。
2. **异常的兴起（1980 到 1990 年代）**：Lisp、CLU 提出，C++ 引入，Java（1995）把「受检异常」推向主流，期望编译器强制处理错误。
3. **C++（2011 到 2023）**：先弃用、后删除运行时检查的异常规约（C++11 弃用，C++17 删除），保留 `noexcept`；`std::error_code`（C++11）把错误码加上类别；C++23 的 `std::expected` 补上值型结果，向 Rust 的 `Result` 靠拢。
4. **受检异常的退潮**：C#（2000）刻意不引入，Kotlin 放弃，Scala 放弃。原因是它与函数式风格（lambda、流）不兼容，并导致大量空 `catch` 和 `throws Exception`。
5. **错误值的回归（2009 年起）**：Go 回到「错误是普通返回值」，理由是显式比隐式好读。
6. **代数类型（2015 年起）**：Rust 把 Haskell 的 `Maybe`/`Either` 带入系统编程，并用 `?` 压缩样板；Swift 的 `throws` 虽然外观像异常，其实是编译成返回值，并要求调用处写 `try`，让可抛出点可见；Kotlin 提供 `Result`。

趋势：
- **显式比隐式**：新语言倾向让失败在签名和调用点都看得见（Rust `Result`、Swift `try`、Zig 的错误联合类型）。
- **类型承载错误**：用类型系统保证错误被处理，同时用语法糖降低样板。
- **异常并未消失**：Java、Python、C# 的海量代码仍然基于异常；Python 3.11 加入异常组（`ExceptionGroup`）支持并发场景，Java 也在改进。
- **不可恢复错误单独对待**：panic、abort，加进程级监督重启，已经成为共识。
