---
id: pl-errors-panics-mechanism
node: errors.panics
type: qa
step: 2
---
## Q
Go 的 `panic`/`recover` 和 Rust 的 panic 在运行时分别是怎么执行的？未处理时进程怎么退出？

## A
**Go**：`panic` 立刻停止当前函数的执行，开始逐层向调用栈上方返回，**途中运行每一层已注册的 `defer`**。如果某个 `defer` 里调用了 `recover()`，panic 被停止，`recover` 返回 panic 的值，程序从那个函数正常返回。如果直到 goroutine 的顶层都没人 `recover`，整个**进程**打印 panic 信息和 goroutine 的栈，以状态码 2 退出。

```go
defer func() {
	if r := recover(); r != nil { err = fmt.Errorf("recovered: %v", r) }
}()
return a / b, nil          // b == 0 -> panic: integer divide by zero
```

实测：`safeDiv(1, 0)` 返回 `0 recovered: runtime error: integer divide by zero`。`recover` 只在 `defer` 调用的函数里有效。

**Rust**：`panic!` 打印消息和位置，然后默认**展开栈**（unwind）：依次运行当前作用域里值的 `Drop`，释放资源，之后终止**这个线程**。主线程 panic 则进程以状态码 101 退出。可以在 `Cargo.toml` 里设置 `panic = "abort"`，此时不展开，直接中止进程（实测退出码 134，即 SIGABRT），二进制更小，但不运行 `Drop`。`std::panic::catch_unwind` 可以拦截展开，但不是为常规错误处理设计的。

**Java**：不存在独立的 panic。`Error` 是 `Throwable` 的子类，与 `Exception` 并列，表示不应被应用捕获的严重问题（`OutOfMemoryError`、`StackOverflowError`）；未捕获的异常终止所在线程，主线程终止后进程以状态码 1 退出（若无其他非守护线程）。

**Python**：异常层次的顶层是 `BaseException`；`Exception` 是常规错误的基类，`SystemExit`、`KeyboardInterrupt` 直接继承 `BaseException`，目的是让 `except Exception` 不会拦住退出和中断。

共同点：panic 的路径都经过「展开并运行清理」，区别是能否被拦截、拦截的粒度是线程还是进程。
