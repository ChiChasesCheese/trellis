---
id: pl-abstraction-generics-foundation-go-generics
node: abstraction.generics
type: qa
step: 3
---
## Q
Go 的泛型（1.18 起）长什么样？类型约束是怎样用接口表达的，`~int` 和 `comparable` 是什么？

## A
函数名后面的方括号声明类型参数，每个参数配一个**约束**（constraint）。约束就是一个接口，但这类接口除了方法，还可以列出「允许哪些类型」，叫类型集合（type set）：

```go
type Number interface{ ~int | ~float64 }
func Sum[T Number](xs []T) (s T) { for _, x := range xs { s += x }; return }
type Celsius float64
Sum([]int{1, 2})        // 3
Sum([]Celsius{1.5, 2})  // 3.5，Celsius 的底层类型是 float64，满足 ~float64
Sum([]string{"a"})
// error: string does not satisfy Number (string missing in ~int | ~float64)
```

要点：

- `A | B` 表示并集；`~int` 表示「底层类型是 `int` 的所有类型」，包括用户定义的 `type MyInt int`，不带 `~` 则只接受 `int` 本身。
- `any` 是空接口，等于不加约束；`comparable` 是内置约束，表示「可以用 `==` 比较」，用来写 map 的键、去重等。
- **类型推断**：调用 `Sum(xs)` 时不必写 `Sum[int](xs)`，编译器从实参推出 `T`。

Go 把约束写成接口，是为了不引入新概念：已有的接口机制扩展一下就能表达约束，符合它「少特性」的作风。代价是约束的写法比较间接，例如要求 `T` 支持 `<` 只能列出所有有序类型的联合，没有 trait 那样的「能比较」这一语义名字（标准库提供 `cmp.Ordered` 来代替）。
