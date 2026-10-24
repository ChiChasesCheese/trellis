---
id: pl-binding-names-scope-pitfall-closure-loop
node: binding.names-scope
type: qa
step: 10
---
## Q
在循环里创建闭包（closure）为什么在 Python 里全都看到最后一个值？Go 1.22 为什么要改循环变量的作用域？

## A
闭包捕获的是**变量**，不是创建那一刻的**值**。如果整个循环只有一个循环变量，所有闭包共享它，等它们被调用时，变量早已走到最后一个值。

Python 的循环变量属于函数作用域，只有一个 `i`：

```python
fs = [lambda: i for i in range(3)]
print([g() for g in fs])                  # [2, 2, 2]
fs = [lambda i=i: i for i in range(3)]    # default arg freezes the value now
print([g() for g in fs])                  # [0, 1, 2]
```

这叫**晚绑定**（late binding）：`i` 在闭包被调用时才查。默认参数在函数定义那一刻求值，所以能把当前值固定下来。

Go 1.21 及以前也是单个循环变量，`go func() { use(i) }()` 或把闭包存进切片，结果与 Python 一致，是 Go 最常见的并发 bug 之一。Go 1.22 起，`for` 循环**每次迭代新建一份变量**（语言版本由 `go.mod` 里的 `go` 行决定，旧模块保持旧语义）：

```go
for i := 0; i < 3; i++ {
	fs = append(fs, func() int { return i })
}
// Go 1.22+: prints 0 1 2   (before 1.22: 3 3 3)
```

Java 出不了这个问题：经典 `for (int i…; i++)` 的 `i` 会被修改，不是 effectively final，lambda 一引用编译器就报错，逼你先复制到一个新变量。Rust 的闭包默认借用循环变量，把闭包存到循环之外时变量已经销毁，编译失败，必须 `move` 把值复制进闭包。

对比可见：语言要么让规则更不容易出错（Go 改语义、Java 禁止、Rust 借用检查），要么靠约定（Python）。Python 的对策是推导式里用默认参数，或用 `functools.partial` 提前绑定。
