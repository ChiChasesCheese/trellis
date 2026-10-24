---
id: pl-abstraction-polymorphism-kinds-foundation-rust-trait
node: abstraction.polymorphism-kinds
type: qa
step: 2
---
## Q
Rust 的 trait、`impl ... for`、trait 约束（trait bound）和 trait 对象（`dyn Trait`）分别是什么？一个小例子里它们怎样配合？

## A
心智模型：**trait 是一份能力清单**（「会 `describe`」），**`impl Trait for 某类型` 是该类型签署这份清单的实现**，两者可以写在不同的地方，甚至由不同的人来写。trait 本身不是类型，也没有字段。

```rust
trait Describe { fn describe(&self) -> String; }
impl Describe for i32  { fn describe(&self) -> String { format!("int {}", self) } }
impl Describe for &str { fn describe(&self) -> String { format!("str {}", self) } }
fn show<T: Describe>(x: T) -> String { x.describe() }      // 约束
fn show_dyn(x: &dyn Describe) -> String { x.describe() }   // trait 对象
// show(7) -> "int 7"；show_dyn(&"b") -> "str b"
// Vec<Box<dyn Describe>> 可以同时装 5 和 "a"
```

两种用法：

- **trait 约束** `T: Describe`：「T 可以是任何实现了 Describe 的类型」。编译器为每个实际用到的 `T` 各生成一份函数（静态分派，可内联）。
- **trait 对象** `&dyn Describe`：把具体类型抹掉，只留「实现了 Describe」这一事实；调用时运行期查表，所以一个 `Vec<Box<dyn Describe>>` 里可以混放不同类型。

同一个 trait 因此既可以做编译期的泛型约束，也可以做运行期的多态入口。选哪种是调用方的决定，实现者不用事先替你选好。
