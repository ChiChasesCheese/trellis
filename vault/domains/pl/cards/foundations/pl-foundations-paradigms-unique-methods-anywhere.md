---
id: pl-foundations-paradigms-unique-methods-anywhere
node: foundations.paradigms
type: qa
step: 8
---
## Q
「方法属于类」这个面向对象的默认假设，在 Go 和 Rust 里是怎样被打破的？Java 和 Python 为什么做不到？

## A
Go 允许给任何自己定义的具名类型加方法，包括基于 `float64` 的类型：

```go
type Celsius float64

func (c Celsius) Fahrenheit() float64 { return float64(c)*9/5 + 32 }
// Celsius(100).Fahrenheit() 输出 212
```

Rust 更进一步：用 trait 可以给别人定义的类型加方法，包括 `i32`：

```rust
trait Double { fn double(&self) -> Self; }
impl Double for i32 { fn double(&self) -> i32 { self * 2 } }
// 21.double() 输出 42
```

Java 做不到，因为方法必须写在类的内部，而 `int` 不是类；Python 的内置 `int` 虽是对象，但是不可变类型，写 `int.double = lambda self: self * 2` 会报 `TypeError: cannot set 'double' attribute of immutable type 'int'`。

结论：Go 和 Rust 把「数据」和「行为」解耦了，方法只是语法糖，其本质是第一个参数叫 `self` 的函数。Java 和 Python 的对象模型把行为绑在类身上，所以想扩展内置类型只能包装或继承。
