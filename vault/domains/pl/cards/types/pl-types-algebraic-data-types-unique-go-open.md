---
id: pl-types-algebraic-data-types-unique-go-open
node: types.algebraic-data-types
type: qa
step: 4
---
## Q
Go 为什么至今没有和类型？用 type switch 模拟时，漏掉一种类型会发生什么？

## A
Go 的设计取向是语言小、规则少。和类型需要新的类型构造、模式匹配语法和穷尽检查，会显著扩大语言规模，Go 的设计者认为接口加 type switch 已经够用。Go 的接口本来就是开放的：任何包里的任何类型只要有对应方法都能满足它。这与和类型要求的封闭集合是相反的哲学。

类型约束里可以写联合（`interface{ int | string }`），但只能作为泛型约束，不能当作普通变量的类型：

```console
cannot use type U outside a type constraint: interface contains type constraints
```

用 type switch 模拟时，编译器不知道有哪些类型：

```go
switch v := s.(type) {
case Circle:
    return 3.14 * v.R * v.R
case Rect:
    return v.W * v.H
}
return -1
```

当传入一个没处理的 `Tri{1, 1, 1}` 时，代码编译通过，实际输出 `-1`，一个看起来像合法答案的哨兵值悄悄出现。

这就是开放与封闭的权衡在 Go 中的体现：开放换来了扩展性和语言的小，代价是「是否处理完所有情况」由程序员和测试负责，不由编译器负责。补救办法是：给接口加一个未导出的标记方法让实现者局限在本包，并用 `exhaustive`、`go-sumtype` 之类的 linter 做近似的穷尽检查。
