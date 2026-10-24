---
id: pl-types-algebraic-data-types-found-go-type-switch
node: types.algebraic-data-types
type: qa
step: 5
---
## Q
Go 的 type switch 是什么？它能当作和类型用到什么程度？

## A
Go 的接口变量内部保存「具体类型加值」。`switch v := x.(type)` 读取其中的具体类型并按类型分支，在每个 `case` 里 `v` 就是那个具体类型。空接口（写作 `any` 或 `interface{}`）没有任何方法要求，因此任何类型的值都可以放进去，type switch 把它们分流出来。

```go
type Cmd interface{}
type Quit struct{}
type Move struct{ DX, DY int }

func run(c Cmd) string {
    switch v := c.(type) {
    case Quit:
        return "quit"
    case Move:
        return fmt.Sprint("move ", v.DX, ",", v.DY)
    }
    return "?"
}
```

`run(Move{3, 4})` 得 `move 3,4`，`run(Quit{})` 得 `quit`（实际运行输出 `move 3,4 quit`）。

局限：`Cmd` 是空接口，它不限制能放进去什么，任何包里的任何类型都可以传入；编译器也不知道一共有多少种可能，所以不会检查你是否漏了某个 `case`。没有匹配的类型会落到 `switch` 后面的代码（这里的 `"?"`）。这是接口开放性的直接结果：Go 里的「几种之一」靠约定和测试保证，不靠编译器。
