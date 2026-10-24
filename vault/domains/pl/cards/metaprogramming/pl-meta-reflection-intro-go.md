---
id: pl-meta-reflection-intro-go
node: metaprogramming.reflection
type: qa
step: 3
---
## Q
Go 的 `reflect` 包是什么？`reflect.Type` 与 `reflect.Value` 怎样对应一个接口值，一个具体场景里它怎样工作？

## A
**是什么**：Go 编译时没有保留 Java 那样完整的类及方法的元数据，但每个类型都有一份只读的类型描述（type descriptor）链接进二进制。`reflect` 包把一个接口值（空接口 `any` 里存着「类型指针 + 数据指针」）拆开，让你读到这两部分。

**心智模型**：两个对象分工明确。
- `reflect.Type`：这个值的「形状」，字段名、字段类型、struct tag、方法集。
- `reflect.Value`：这个值的「内容」，可以读，也可以在特定条件下写。

入口是 `reflect.ValueOf(x)` 和 `reflect.TypeOf(x)`。**关键约束**：只有可寻址（addressable，即通过指针拿到）且导出的字段才能写。

**场景**：写一个通用的打印函数，对任何结构体都能输出字段名、类型和 JSON tag：

```go
func dump(x any) {
    v := reflect.ValueOf(x); t := v.Type()
    for i := 0; i < t.NumField(); i++ {
        f := t.Field(i)
        fmt.Printf("%s (%s) = %v tag=%q\n", f.Name, f.Type, v.Field(i), f.Tag.Get("json"))
    }
}
```

传入 `User{"ann", 30}` 的真实输出：`Name (string) = ann tag="name"` 与 `Age (int) = 30 tag="age"`；传入匿名结构体 `struct{X, Y float64}{1,2}` 同样可以，tag 为空。

**要记住的一点**：`encoding/json`、`fmt` 的 `%v`、`database/sql` 的扫描全是靠它实现的。Go 里「接口值带着类型」是反射的前提：这也是为什么 `reflect` 的入口参数都是 `any`。
