---
id: pl-out-go-defer
node: output.go
type: qa
step: 3
---
## Q
**defer 的求值时机**｜读代码说输出

```go
func f() (r int) {
	defer func() { r *= 2 }()
	return 3
}
func main() {
	for i := 0; i < 3; i++ {
		defer fmt.Println("defer", i)
	}
	x := 1
	defer fmt.Println("x =", x)
	x = 2
	fmt.Println(f())
}
```

输出什么？

## A
**输出。**
```
6
x = 1
defer 2
defer 1
defer 0
```

**为什么。**
- `defer fmt.Println("x =", x)` 在注册时就对参数求值，保存的是 1，之后 `x = 2` 不影响它。
- `defer` 在函数返回时按后进先出（LIFO）执行，所以 `defer 2`、`defer 1`、`defer 0` 倒序；它们都晚于 `fmt.Println(f())`，所以 6 先出现。
- `f()` 里 `return 3` 先把命名返回值 `r` 设成 3，再运行 `defer` 的闭包 `r *= 2`，返回 6：闭包不是参数，运行时才读 `r`。

**语言为什么这样设计。**
- 参数在注册时求值，是为了「把当时的现场固定下来」：`defer f.Close()` 关的就是当时那个文件；要读最新的值就用闭包。命名返回值加 `defer` 还能在返回前统一修改错误（例如 `recover` 之后设置 `err`）。
- C++ 靠析构（RAII），Java 靠 `finally` 和 try-with-resources，Python 靠 `with`，Rust 靠 `Drop`；Go 没有析构和异常，选择了 `defer` 让清理代码紧挨着申请资源的地方。

**怎么写才对。**
```go
defer func() { fmt.Println(x) }()   // 闭包读最新的 x
// 循环里的 defer 到函数结束才执行，大循环要拆成小函数
```

**面试里一句话。**
Deferred call arguments are evaluated when defer runs, not when the function returns, and deferred calls run last in, first out.
