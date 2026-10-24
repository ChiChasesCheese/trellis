---
id: pl-abstraction-generics-implementation-foundation-rust-monomorphization
node: abstraction.generics-implementation
type: qa
step: 3
---
## Q
Rust 的单态化（monomorphization）是什么？编译产物里能看到什么，它换来了什么？

## A
心智模型：**编译器像一个自动复制粘贴的工具**。每遇到一个泛型函数被某个具体类型使用，就把函数体里的 `T` 全部替换成该类型，生成一份专用函数，再对这份函数单独优化。

```rust
#[inline(never)]
fn show<T: Display>(x: T) -> String { format!("<{x}>") }
show(1i32); show(2.5f64); show("s");
```

编译后用 `nm` 查看符号，能看到三个不同的 `show` 实例（一个对应 `i32`、一个 `f64`、一个 `&str`）。三份机器码各自知道自己的类型大小和 `Display` 的具体实现，调用 `Display::fmt` 是直接调用，常常内联。

换来的是：**没有任何运行期开销**。没有装箱、没有虚表、没有类型检查，泛型版本与你手写三份的性能相同，这就是「零成本抽象」的含义。

付出的是：

- **代码体积**：实例越多二进制越大。
- **编译时间**：同一个泛型函数在每个使用它的 crate 里都要重新生成和优化，是 Rust 编译慢的主要原因之一。
- **没有运行期多态**：想把不同类型放进同一个集合，必须转用 `dyn Trait`（动态分派）。

C++ 模板是同一套思路，只是在实例化时才检查，Rust 的在定义处检查。
