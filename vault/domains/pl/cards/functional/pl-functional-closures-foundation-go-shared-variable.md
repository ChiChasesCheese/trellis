---
id: pl-functional-closures-foundation-go-shared-variable
node: functional.closures
type: qa
step: 3
---
## Q
Go 的闭包捕获的是什么？计数器闭包里的变量存在哪里，生命周期怎么保证？

## A
Go 的闭包捕获**变量本身**，不是它的值。多个闭包捕获同一个变量就共享状态，一方修改，另一方立刻看到。

```go
func counter() func() int {
    n := 0
    return func() int { n++; return n }
}
a, b := counter(), counter()
fmt.Println(a(), a(), b())   // 1 2 1
x := 1
inc := func() { x++ }
inc(); inc()
fmt.Println(x)               // 3：闭包直接改了外层的 x
```

`a` 和 `b` 各自调用 `counter()`，各有一个独立的 `n`，所以 `b()` 从 1 开始。

变量的生命周期靠**逃逸分析**保证：编译器发现 `n` 被一个会逃出函数的闭包引用，就把 `n` 从栈上挪到堆上（`go build -gcflags=-m` 会输出 `moved to heap: n`），由 GC 回收。程序员不需要关心，但要知道：闭包逃出函数时，被捕获的变量多了一次堆分配。

与 Java 的对比：Java 复制值，所以不能修改；Go 共享变量，所以可以修改，也因此要面对**并发下的数据竞争**（多个 goroutine 的闭包共享同一个变量）和**循环变量共享**的陷阱（见后文）。Go 的取舍是：保持直观的语义（闭包就是引用外层变量），把安全交给 `go vet`、race detector 和惯例。
