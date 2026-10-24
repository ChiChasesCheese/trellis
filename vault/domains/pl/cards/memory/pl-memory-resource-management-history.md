---
id: pl-memory-resource-management-history
node: memory.resource-management
type: qa
step: 7
---
## Q
各语言的资源管理机制是怎样一步步出现的？这说明了什么趋势？

## A
1. **C++（1980 年代）**：RAII，用析构函数管理一切资源，成为后来所有方案的参照。
2. **Java 1.0（1996）**：选了 GC 和 `finalize`，很快发现终结器不能用来管文件，于是长期靠手写 `try/finally`。
3. **C#（2002）**：`using` 语句，开创了块级作用域语法。
4. **Python 2.5（2006，PEP 343）**：`with` 语句与上下文管理器协议。
5. **Go（2009）**：`defer`，函数级、轻量。
6. **Java 7（2011）**：try-with-resources，终于把块级语法补进语言。Java 9 起提供 `Cleaner`；`finalize` 在 JDK 18（JEP 421）被标记为待移除。
7. **Rust（2015）**：`Drop` 与所有权，把 RAII 与内存安全结合，类型系统保证只释放一次。
8. **近年**：Go 1.24 加入 `runtime.AddCleanup`，用来替代 `SetFinalizer`；Java 的 FFM API 把原生内存的生命周期交给 `Arena` 管理，也是块级作用域；Swift 也提供 `defer`。

趋势：每一代 GC 语言都在补回「确定性释放」。最终都收敛到同一个想法——**把资源的生命周期和一个词法作用域绑定**，区别仅在于绑定的方式是语法（`with`、`defer`）还是类型（`Drop`）。
