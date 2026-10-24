---
id: pl-memory-escape-analysis-foundation-go
node: memory.escape-analysis
type: qa
step: 2
---
## Q
Go 编译器的逃逸分析是什么样的？怎样看到它的决定？

## A
Go 的语法里没有“放栈”还是“放堆”的区别，`p := P{1, 2}` 与 `p := &P{1, 2}` 都只是创建一个值。编译器在编译期做**逃逸分析**：沿着每个变量的地址看它流向哪里，若地址在函数返回之后还可能被访问，就把变量放到堆上（并由 GC 管理）；否则留在栈帧里，函数返回时随栈帧自动消失，几乎免费。

用 `go build -gcflags=-m` 让编译器汇报：

```go
func onStack() int { p := P{1, 2}; return p.X + p.Y }
func onHeap() *P   { p := P{3, 4}; return &p }
```

```console
./main.go:13:2: moved to heap: p
```

被点名的是 `onHeap` 里的 `p`：它的地址被返回，调用者还要用，所以必须搬到堆。`onStack` 里的 `p` 没有出现，说明留在栈上。

常见导致逃逸的情形：地址被返回；存进全局变量或堆上的对象；传给接口参数（如 `fmt.Println(p)` 会把值装箱）；被逃逸的闭包捕获；大小在编译期未知或过大的切片。

要记住的一个事实：同样一行 `p := P{...}`，去向由后面怎么用它决定，写法上没有任何提示，只有编译器的 `-m` 输出和基准测试（`go test -bench . -benchmem`）里每次操作的堆分配次数 `allocs/op` 能告诉你。
