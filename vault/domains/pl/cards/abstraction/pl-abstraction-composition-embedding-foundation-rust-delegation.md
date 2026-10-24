---
id: pl-abstraction-composition-embedding-foundation-rust-delegation
node: abstraction.composition-embedding
type: qa
step: 4
---
## Q
Rust 里怎样通过组合复用行为？为什么不要用 `Deref` 假装继承？

## A
Rust 的结构体只能持有别的结构体作为字段，**没有自动转发**。要让外层也具备内层的 trait 能力，需要手写转发 trait 方法：

```rust
trait Logger { fn log(&self, m: &str); }
struct Stdout;
impl Logger for Stdout { fn log(&self, m: &str) { println!("{m}"); } }
struct Service<L: Logger> { log: L }
impl<L: Logger> Logger for Service<L> {
    fn log(&self, m: &str) { self.log.log(m) }   // 手写委托
}
```

泛型参数 `L` 让这个组合是静态分派：`Service<Stdout>` 的转发会被内联，没有运行期开销。

`Deref` 是智能指针 trait（`Box<T>`、`Rc<T>` 用它让 `*p` 和 `p.method()` 指向内部值）。有人用它给外层实现 `Deref<Target = Inner>`，这样 `dog.eat()` 就能直接调到内部 `Animal` 的方法，`&Dog` 还会自动转成 `&Animal`，看起来像继承。这被社区列为**反模式**：`Deref` 是为「指针和它指向的东西」设计的，滥用它会让方法解析难以预测、与同名方法冲突，且表达的关系（is-a）和 Rust 的类型系统并不一致。

正统的做法是显式字段加手写转发，或者用 `delegate` / `ambassador` 这类宏生成转发代码。
