---
id: pl-trends-convergence-intro-go
node: trends.convergence
type: qa
step: 3
---
## Q
Go 加入的泛型（generics）和迭代器（`range` over function）是什么？Go 为什么等了十几年才加，这些新特性在一个例子里怎样工作？

## A
**泛型（Go 1.18，2022）**：函数和类型可以带类型参数，同一份代码适用于多种类型，编译期检查。

```go
func Map[T, U any](s []T, f func(T) U) []U {
    out := make([]U, 0, len(s))
    for _, v := range s { out = append(out, f(v)) }
    return out
}
Map([]int{1, 2, 3}, func(i int) string { return fmt.Sprint(i * i) })  // [1 4 9]
```

在此之前，通用容器只能用 `interface{}`（丢失类型信息，要运行时断言）或为每种类型复制代码或代码生成。

**迭代器（Go 1.23，2024）**：`range` 现在可以遍历一个函数。这个函数接受一个 `yield` 回调，每产生一个值就调用它，返回 `false` 表示调用方想停止。标准库 `iter.Seq[T]` 就是这种函数的类型。

```go
func Evens(n int) iter.Seq[int] {
    return func(yield func(int) bool) {
        for i := 0; i < n; i += 2 { if !yield(i) { return } }
    }
}
for v := range Evens(7) { fmt.Print(v, " ") }   // 0 2 4 6
```

**配套**：Go 1.21 起有内建的 `min`、`max`，以及标准库 `slices`、`maps` 包（排序、查找、迭代器转换），把过去人人手写的辅助函数收进标准库。

**为什么等这么久**：Go 的设计者认为泛型会增加语言复杂度和编译、阅读成本，宁可等到找到“与 Go 风格相容”的设计（接口作为类型约束，类型参数用方括号）。几年里社区用大量案例论证需求，设计者借此理解到真正的痛点（容器、通用算法）。

**要记住的一点**：Go 的收敛是“后发、克制”的：只补最痛的缺口（泛型、迭代器），不引入重载、继承等，保持语言小。
