---
id: pl-errors-panics-foundation-go
node: errors.panics
type: qa
step: 2
---
## Q
Go 的 `panic` 和 `recover` 怎么配合 `defer` 工作？

## A
`panic(v)`（或运行时错误：越界、除零、对 nil map 写入）会立刻停止当前函数，开始逐层向上返回，**途中执行每一层已登记的 `defer`**（`defer` 即“登记一次调用，函数返回时执行”）。`recover()` 只在 `defer` 登记的函数里有效：调用它就停止 panic，并取回 panic 的值，程序从这个函数正常返回。如果一路到 goroutine 顶层都没人 `recover`，整个进程打印 panic 信息和栈，以状态码 2 退出。

```go
func safeDiv(a, b int) (res int, err error) {
	defer func() {
		if r := recover(); r != nil { err = fmt.Errorf("recovered: %v", r) }
	}()
	return a / b, nil
}
```

`safeDiv(1, 0)` 返回 `0 recovered: runtime error: integer divide by zero`（本机实测）。

注意：`recover` 只能拦住**同一个 goroutine** 里的 panic。goroutine 是 Go 的轻量并发执行单元，用 `go f()` 启动；别的 goroutine 里没处理的 panic 会让整个进程退出。

要记住的一个事实：Go 把 panic/recover 留给 bug 和框架边界，常规错误用返回值。
