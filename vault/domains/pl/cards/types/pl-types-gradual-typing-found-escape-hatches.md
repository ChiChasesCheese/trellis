---
id: pl-types-gradual-typing-found-escape-hatches
node: types.gradual-typing
type: qa
step: 4
---
## Q
静态类型语言怎样「退出」类型检查？Go 的 `any`、Java 的原始类型（raw type）和 Rust 的 `dyn Any` 各是什么？

## A
即使是整体静态的语言，也提供让某个值暂时脱离静态检查的逃生口，换取灵活性：

- Go 的 `any`（空接口 `interface{}`）：可以装任何值，取出时用类型断言还原类型。

```go
var x any = 1
x = "now a string"
fmt.Println(x)     // now a string
```

- Java 的原始类型：不带类型参数的泛型类，如 `List` 而不是 `List<String>`，为兼容 Java 5 之前的代码而保留。编译器不检查元素类型，错误推迟到使用处，以 `ClassCastException` 的形式出现：

```java
List raw = new ArrayList();
raw.add("s"); raw.add(1);
List<String> typed = raw;       // 未经检查的赋值，编译器只警告
String s = typed.get(1);        // 运行时才抛 ClassCastException
```

实际输出：Go 打印 `now a string`；Java 在 `typed.get(1)` 处抛出 `ClassCastException`（编译时有 unchecked 警告）。

- Rust 的 `Box<dyn Any>`：装任何类型的值，用 `downcast_ref::<T>()` 询问它是不是 `T`，返回 `Option`：`Some(5)` 或 `None`。比 Go 和 Java 更谨慎，询问失败得到 `None`，不会崩溃。

共同点：逃生口是例外，用在序列化、插件、与旧代码互通的边界；把它们和 Python 的 `Any` 比较，区别在于静态语言里逃生口是少数地方，整个程序默认受检查。
