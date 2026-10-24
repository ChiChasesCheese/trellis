---
id: pl-types-type-conversions-found-go-assertion
node: types.type-conversions
type: qa
step: 2
---
## Q
Go 的类型断言（type assertion）`x.(T)` 是什么？带 `ok` 和不带 `ok` 的写法有什么区别？

## A
类型断言用于接口类型的值：它声称「这个接口变量里装的具体类型是 `T`」，运行时检查并取出。接口值内部保存（具体类型，值）一对，断言就是比较那个具体类型。

两种形式：

- `v, ok := x.(T)`：逗号 ok 形式。类型不符时 `ok` 为 `false`，`v` 是 `T` 的零值，不会崩溃。
- `v := x.(T)`：不带 `ok`。类型不符时直接 panic（运行时错误，程序崩溃并打印栈）。

```go
var x any = 42
n, ok := x.(int)
s, ok2 := x.(string)
fmt.Println(n, ok, s == "", ok2)   // 42 true true false
fmt.Println(x.(string))
```

实际输出：`42 true true false`，然后最后一行 panic：`panic: interface conversion: interface {} is int, not string`。

选择原则：只要类型不是百分之百确定，就用逗号 ok 形式，并处理 `false` 的分支；panic 形式只留给「这里类型错了就是程序 bug」的场合。注意类型断言只能用于接口类型的值；普通数值之间的转换用 `T(x)` 的转换形式，两者语法不同、语义不同。
