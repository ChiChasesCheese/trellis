---
id: pl-functional-first-class-functions-foundation-rust-closure-types
node: functional.first-class-functions
type: qa
step: 4
---
## Q
Rust 里 `fn` 指针、闭包和 `Fn` trait 的关系是什么？为什么每个闭包都有自己独一无二的类型？

## A
Rust 里有三层：

- **`fn` 指针**（`fn(i32) -> i32`）：指向普通函数的代码地址，不捕获环境，8 字节。
- **闭包**（`|x| x + k`）：可以捕获外层变量。编译器为**每一个闭包表达式**生成一个匿名结构体，字段就是被捕获的变量，再给这个结构体实现 `Fn` / `FnMut` / `FnOnce` trait。
- **`Fn` 系列 trait**：用来写「接受任意可调用对象」的泛型约束。

```rust
fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(x) }
fn apply_dyn(f: &dyn Fn(i32) -> i32, x: i32) -> i32 { f(x) }
let k = 3;
apply(|x| x + k, 1);       // 4：泛型，静态分派，可内联
apply_dyn(&|x| x * k, 2);  // 6：trait 对象，动态分派
```

由此带来的性质：没有捕获的闭包大小是 0；捕获一个 `i64` 的闭包是 8 字节（实测）。因为每个闭包是独特的类型，`apply` 会为每个闭包单态化，调用被内联成和手写一样的代码，**零开销**。

代价是：两个写法相同的闭包类型也不同，不能放进同一个 `Vec`，也不能在 `if/else` 的两个分支返回不同闭包（除非装箱成 `Box<dyn Fn>`）。这是 Rust 把「静态分派 + 零成本」摆在方便之前的体现。
