---
id: pl-errors-models-foundation-panic
node: errors.models
type: qa
step: 5
---
## Q
panic 是什么？它和普通错误的区别是什么？

## A
**panic**（Go、Rust 的叫法）是“不可恢复错误”：程序发现自己处在不应该出现的状态（下标越界、对 nil map 写入、违反了断言），于是停止正常执行，打印错误信息和栈，然后终止（线程或整个进程）。

和普通错误的区别在于**谁来负责**：
- 普通错误（文件不存在、输入非法）：程序没问题，调用者有办法应对，用返回值或异常。
- panic：程序本身有 bug，调用者也不知道状态坏在哪里，最安全的做法是尽快失败，让进程重启或让人去修。

```go
v := []int{1, 2, 3}
fmt.Println(v[5])   // panic: runtime error: index out of range [5] with length 3
```

Go 进程因此以状态码 2 退出，Rust 以 101 退出（本机实测）。Java 和 Python 没有独立的 panic：未捕获的异常终止线程，严重的问题放在 `Error` 子类（Java）或 `BaseException` 子类（Python）里。

要记住的一个事实：panic 表示“这是 bug，不是错误”；常规的失败不应该用它。
