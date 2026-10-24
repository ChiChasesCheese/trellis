---
id: pl-types-inference-found-go-short-decl
node: types.inference
type: qa
step: 3
---
## Q
Go 的 `:=` 是什么？「无类型常量」怎样影响推导出的类型？

## A
`:=` 是 Go 的短变量声明：在函数内部同时声明并初始化变量，类型由右边的值决定。它是 Go 里最常用的声明形式。

Go 的字面量（`42`、`1.5`、`"s"`）起初是无类型常量（untyped constant），带着一个「种类」（整数、浮点、字符串），没有具体类型。到需要具体类型时才落定：`:=` 使用该种类的默认类型，整数字面量是 `int`，浮点字面量是 `float64`；若赋给已声明了类型的变量，则采用那个类型。

```go
a := 42              // int
b := 1.5             // float64
var c float64 = 1    // 无类型常量 1 在这里成为 float64
fmt.Printf("%T %T %T\n", a, b, c)
```

实际输出 `int float64 float64`。

推导是单向的，只看右边。所以右边没有类型信息时就推不出来：`y := nil` 编译失败，`use of untyped nil in assignment`。函数的参数和返回值永远必须写类型。

这个设计的理由是可读性：局部变量的类型几乎总能从右边一眼看出，而函数签名是别人要读的契约，所以只在前者省略。
