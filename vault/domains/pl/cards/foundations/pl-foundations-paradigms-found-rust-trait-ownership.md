---
id: pl-foundations-paradigms-found-rust-trait-ownership
node: foundations.paradigms
type: qa
step: 4
---
## Q
Rust 的 `trait` 和 `impl` 是什么？「每个值只有一个所有者（ownership）」在最小的例子里是什么意思？

## A
Rust 没有类和继承，行为通过两个构造组织：

- `trait`：一组方法签名，描述「能做什么」，类似 Java 的接口。
- `impl Trait for Type`：为某个具体类型实现这组方法，写在类型定义之外，因此也可以给别人定义的类型（包括内置的 `i32`）加方法。

```rust
trait Double { fn double(&self) -> Self; }
impl Double for i32 { fn double(&self) -> i32 { self * 2 } }
// 21.double() 得到 42
```

所有权是 Rust 管理内存的核心规则：每个值恰好有一个所有者变量；所有者离开作用域，值就被释放；把值赋给另一个变量是「移动」（move），所有权转走，旧变量不能再用。

```rust
let s = String::from("hi");
let t = s;                       // 所有权移到 t
println!("{} {}", t, 21.double());   // hi 42
// 此后再用 s 是编译错误
```

实际输出 `hi 42`。因为每块堆内存只有一个所有者，编译器就知道在什么时刻释放它，不需要垃圾回收器，也不会重复释放。你需要「借」而不是「移」时，用引用 `&s`，所有者保持不变。这一点是 Rust 一切设计（包括函数式风格写法的约束）的出发点。
