---
id: pl-memory-resource-management-mechanism
node: memory.resource-management
type: qa
step: 2
---
## Q
try-with-resources、`with`、`defer` 在运行时的执行顺序是怎样的？异常发生时它们怎么保证清理？

## A
三者本质都是「在离开作用域的每条路径上执行清理」，细节不同。

**Java try-with-resources** 编译成 `try/finally`：按声明顺序获取资源，按相反顺序调用 `close()`。如果块内抛出异常，同时 `close()` 也抛出，`close()` 的异常被挂在原异常的 suppressed 列表里，原始异常不会丢。运行结果（两个资源，块内抛 `IllegalStateException`）：

```console
open A
open B
body
close B
close A
caught boom
```

**Python `with`** 调用对象的 `__enter__`，块结束时（正常或异常）调用 `__exit__(异常类型, 值, 栈)`。`__exit__` 能看到异常，返回真值表示「吞掉」，返回假值则继续传播。多个 `with` 项同样是后进先出。

**Go `defer`** 把调用压进当前函数的延迟列表，函数返回（包括 panic）时后进先出地执行；**参数在 `defer` 语句执行的那一刻求值**，不是在清理时。

```console
deferred 2
deferred 1
deferred 0
```

三个 `defer` 按相反顺序执行，各自捕获了当时的 `i`。

**Rust `Drop`** 在编译期插入：作用域的每个出口（包括 panic 展开）按声明相反顺序调用析构。

共同的设计：清理顺序与获取顺序相反，因为后获取的资源可能依赖先获取的资源。成本：`defer` 要维护一个延迟列表，现代 Go 编译器对不在循环里的 `defer` 做了开放编码（open-coded），开销接近零；`with` 与 try-with-resources 的开销是几次方法调用。
