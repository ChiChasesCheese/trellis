---
id: pl-errors-error-values-pitfall-typed-nil
node: errors.error-values
type: qa
step: 6
---
## Q
Go 里一个返回 `error` 的函数明明返回了 nil 指针，为什么 `err != nil` 却是真？

## A
这是 Go 错误处理里最经典的陷阱：**带类型的 nil 接口值不等于 nil**。

```go
type MyErr struct{}
func (*MyErr) Error() string { return "my" }

func f() error {
	var e *MyErr = nil
	return e                 // the interface now holds (type *MyErr, value nil)
}

func main() {
	err := f()
	fmt.Println(err == nil, err != nil)
}
```

实测输出：

```console
false true
```

原因：接口值由「动态类型」和「动态值」两部分组成，只有两者都为空，接口才等于 `nil`。`f` 把一个类型为 `*MyErr`、值为 nil 的指针装进了 `error` 接口，类型部分非空，所以 `err != nil` 为真。调用者看到「有错误」，进入错误分支，却发现错误值是个 nil 指针，调用 `err.Error()` 时可能 panic。

触发场景：函数内部有一个具体错误类型的变量，最后无条件地 `return thatVar`。

修复：函数的返回类型声明为 `error` 时，成功路径必须**显式返回字面量 `nil`**，而不是返回一个可能为 nil 的具体类型变量：

```go
func f(bad bool) error {
	var e *MyErr
	if bad { e = &MyErr{} }
	if e != nil { return e }
	return nil               // a literal nil, not e
}
```

这样 `f(false) == nil` 为 `true`，`f(true)` 返回 `my`。

经验：不要在会被作为 `error` 返回的函数里，声明具体类型的错误变量；先用 `error` 类型的变量，或者直接 `return &MyErr{}`、`return nil`。
