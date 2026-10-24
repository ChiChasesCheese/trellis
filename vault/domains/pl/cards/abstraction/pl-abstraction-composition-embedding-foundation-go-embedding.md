---
id: pl-abstraction-composition-embedding-foundation-go-embedding
node: abstraction.composition-embedding
type: qa
step: 3
---
## Q
Go 的结构体嵌入（struct embedding）有哪些规则？提升、遮蔽和冲突分别怎么处理？

## A
在结构体里写一个**不带字段名**的类型，就是嵌入。被嵌入类型的字段和方法被「提升」到外层：`d.Speak()` 是 `d.Animal.Speak()` 的简写，由编译器展开，没有运行期代价。

规则：

- **遮蔽**：外层自己定义同名方法或字段，就覆盖被提升的；被嵌入的版本仍可用 `d.Animal.Speak()` 访问。
- **冲突**：同一深度嵌入了两个类型都有 `Hi()`，外层 `C{}.Hi()` 编译失败：`ambiguous selector C{}.Hi`。必须显式写 `c.A.Hi()`。
- **嵌入接口**：可以嵌入接口类型，这样外层自动「实现」该接口，所有调用转给内部那个接口值。装饰器就是这样写的。但如果内部接口值是 `nil`，调用时会在运行期 panic。
- **内存布局**：被嵌入的值直接内联在外层里。实测 `Animal{Name string}` 是 16 字节，`Dog{Animal; Tricks int}` 是 24 字节（16 + 8，没有额外指针）；嵌入 `*Animal` 则外层只多一个指针。

```go
type Logger interface{ Log(string) }
type Svc struct{ Logger }   // 嵌入接口
Svc{}.Log("x")              // nil 内部值：panic, nil pointer dereference
```

嵌入因此是「自动写好转发方法」的语法糖，而不是继承：外层不是内层的子类型，不能传给要内层类型的参数（想要多态要靠接口）。
