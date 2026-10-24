---
id: pl-abstraction-classes-inheritance-foundation-go-rust-no-inheritance
node: abstraction.classes-inheritance
type: qa
step: 4
---
## Q
Go 和 Rust 没有实现继承。Go 的结构体嵌入（struct embedding）和 Rust 的 trait 默认方法分别是怎样复用代码的？

## A
**Go 结构体嵌入**：在结构体里写一个不带字段名的类型，它的字段和方法就「提升」到外层，可以直接用，外层仍是独立的类型。

```go
type Animal struct{ Name string }
func (a Animal) Speak() string { return a.Name + " makes a sound" }
type Dog struct {
    Animal           // 嵌入
    Tricks int
}
d := Dog{Animal{"rex"}, 3}
d.Speak()   // "rex makes a sound"；d.Name 也直接可用
```

这只是编译器帮你写了 `d.Animal.Speak()`。`Dog` 不是 `Animal` 的子类型，不能传给要 `Animal` 的参数；`Animal.Speak` 内部也看不到 `Dog`。

**Rust trait 默认方法**：trait 里可以给方法写默认实现，实现者只需提供必须的部分。

```rust
trait Animal {
    fn name(&self) -> String;
    fn speak(&self) -> String { format!("{} makes a sound", self.name()) }
}
struct Dog;
impl Animal for Dog { fn name(&self) -> String { "rex".into() } }
// Dog.speak() -> "rex makes a sound"
```

默认方法只能通过 trait 的其他方法工作，不能直接访问字段，所以没有「继承数据」。两门语言共同的立场是：**复用靠组合（持有别的值），可替换靠接口**，两件事不再用同一个机制。
