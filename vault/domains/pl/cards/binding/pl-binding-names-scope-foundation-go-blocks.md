---
id: pl-binding-names-scope-foundation-go-blocks
node: binding.names-scope
type: qa
step: 3
---
## Q
Go 的作用域有哪几层？短变量声明 `:=` 为什么会在 `if` 或 `for` 里悄悄创建新变量，吞掉外层的 `err`？

## A
Go 的名字解析是词法的，从内到外依次是：块（每对花括号，`if`、`for`、`switch` 的头部自成一层）、函数、文件（`import` 的名字只在本文件有效）、包（同一包所有文件共享）、全局的**宇宙块**（universe，放 `int`、`len`、`nil`、`true` 等预声明名字）。

`:=` 的规则是：在**当前块**里声明左边尚不存在的变量。关键在「当前块」：外层同名变量不算，所以内层会得到一个新变量，把外层那个**遮蔽**（shadow）：

```go
func run() error {
	var err error
	if true {
		n, err := load() // new n AND new err, scoped to this if-block
		_, _ = n, err
	}
	return err // still nil: the failure was assigned to the shadow
}
// run() returns <nil> even though load() failed
```

`load()` 失败了，但错误只赋给了 `if` 块里的影子 `err`，函数末尾返回的是外层那个仍为 `nil` 的变量。编译器不报错（影子被使用了），错误就这样被静默丢掉。

遮蔽也能作用于预声明名字：`len := 3` 合法，之后这一层里 `len(x)` 就不能再当函数用；`fmt := "oops"` 会盖住导入的包。

对策有两条：块里需要赋给外层变量时用 `=` 而不是 `:=`（先 `var n int`）；在 CI 里跑 `go vet` 的 shadow 检查（`golang.org/x/tools` 里的 `shadow` 分析器，默认不在 `go vet` 里）。

Go 选择让 `:=` 简短，代价是这个坑；这符合它「少写字」的取向，同时说明简短语法并不免费。
