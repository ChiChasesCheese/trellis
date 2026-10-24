---
id: pl-abstraction-typeclasses-foundation-java-go-limits
node: abstraction.typeclasses
type: qa
step: 4
---
## Q
为什么 Java 接口和 Go 接口不能「为已有类型追加能力」？它们各自用什么办法绕过，代价是什么？

## A
**Java：能力是类型声明的一部分。**一个类要实现接口，必须在自己的定义里写 `implements`。`Integer`、`String` 的定义在 JDK 里，你无法让它们实现你的 `Describable`。绕过办法：

- **适配器 / 包装类**：`record DescribableInt(int v) implements Describable`，每次使用时包一层，有分配成本，且包装后与原值不等价。
- **把实现作为参数传入**：`Comparator<T>`、`Function<T, String>`。调用者负责传，容易传错、容易忘；而且泛型约束无法表达，`<T>` 看不出需要什么能力。
- **静态工具方法**：`Describers.describe(Object)` 里一长串 `instanceof`，新类型要改这个方法。

**Go：接口是结构化的，但方法必须定义在类型所在的包里。**Go 的接口只要求类型拥有对应方法即可满足，不用声明。这意味着你自己定义的接口，可以被别人的类型满足，只要它碰巧有这些方法。但如果它没有，你**不能自己给它加方法**：

```go
func (x int) Describe() string { return "int" }
// ./t2.go:3:9: cannot define new methods on non-local type int
```

能给 `int` 补方法的只有 `int` 所在的包（语言本身）。绕过办法与 Java 类似：自定义类型包装（`type MyInt int`，转换后才有方法）、函数参数、`switch x.(type)`。

对比 Rust：`impl Describe for i32` 直接合法，没有包装，没有额外分配，泛型函数也能表达 `T: Describe`。

背后的原因不同：

1. Java/Go 的方法表依附于类型：Java 的虚方法表在对象头里，Go 的方法集是类型定义的一部分。能力 = 类型的属性。
2. Rust/Haskell 的 trait 实例是**独立的实体**，由编译器在编译期查找。能力 = 类型与 trait 之间的一条关系。

由此得到的设计后果：Java、Go 的库作者必须**预先**想到所有想用的接口；类型类允许之后再补，代价是需要一致性规则（孤儿规则）来防冲突。
