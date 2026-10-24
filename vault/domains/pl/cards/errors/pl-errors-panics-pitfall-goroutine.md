---
id: pl-errors-panics-pitfall-goroutine
node: errors.panics
type: qa
step: 6
---
## Q
Go 里在 `main` 中写了 `defer recover()`，为什么另一个 goroutine 的 panic 还是让整个程序退出？

## A
`recover` 只能拦住**同一个 goroutine** 里的 panic：panic 沿着该 goroutine 自己的调用栈向上，只经过该 goroutine 里的 `defer`。别的 goroutine 里的 `defer` 对它无能为力。

```go
func main() {
	defer func() { fmt.Println("recovered:", recover()) }()
	go func() { panic("boom in goroutine") }()
	time.Sleep(100 * time.Millisecond)
	fmt.Println("not reached")
}
```

实测输出：

```console
panic: boom in goroutine

goroutine 19 [running]:
main.main.func2()
```

`recovered:` 一行从未出现，`not reached` 也没有，进程直接以状态码 2 退出。

后果：一个后台 goroutine 里的空指针或越界，就能让整个服务宕机，即使 `main` 里写了保护。

修复：**每个自己启动的 goroutine 都在入口处自带 `recover`**，统一封装：

```go
func safeGo(f func()) {
	go func() {
		defer func() {
			if r := recover(); r != nil { log.Printf("panic: %v\n%s", r, debug.Stack()) }
		}()
		f()
	}()
}
```

其他容易踩的 panic 坑：
- 对 `nil` 的 map 写入会 panic（`assignment to entry in nil map`），读取则不会；
- `recover` 之后程序继续运行，但共享数据可能处在中间状态，不应假设一切正常；
- 对已关闭的 channel 再发送，或关闭两次，都会 panic。

Rust 对应：线程里的 panic 只终止该线程，`join()` 返回 `Err`，主线程可以决定如何处理，隔离性更好。
