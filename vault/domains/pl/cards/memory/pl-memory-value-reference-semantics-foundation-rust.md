---
id: pl-memory-value-reference-semantics-foundation-rust
node: memory.value-reference-semantics
type: qa
step: 4
---
## Q
Rust 的“移动”（move）、`Copy` 和 `clone` 分别是什么？`let b = a;` 之后 `a` 还能用吗？

## A
Rust 对“把一个值交给另一个变量”有三种明确的说法：

- **复制**（`Copy`）：小而简单的类型（`i32`、`bool`、`f64`、只含这些的结构体，且声明了 `Copy`）赋值时按位复制，两个变量都可以继续用。
- **移动**（move）：其他类型（`String`、`Vec`、拥有堆内存的类型）赋值时，值的所有权转交给新变量，**旧变量立即失效**，之后再用就是编译错误。机器层面只复制了几个字节（指针、长度），堆上的数据没动。
- **克隆**（`clone`）：显式地做一次真正的深拷贝，得到两份独立的数据，写出来就表示你愿意付这个成本。

```rust
let a = 5;  let b = a;               // Copy: a and b both usable
let s = String::from("hi");
let t = s.clone();                   // explicit deep copy: s and t both usable
let u = s;                           // move: s is dead from here on
println!("{} {} {}", a, b, t);       // 5 5 hi
```

如果在 `let u = s;` 之后再用 `s`，编译器报 `E0382: borrow of moved value: s`。

另外，`&s` 是借用：拿到一个指向 `s` 的只读引用，不转让所有权，`s` 之后仍可使用；`&mut s` 是可修改的借用。

要记住的一个事实：Rust 里“一个值只有一个所有者”，赋值默认转让所有权而不是共享；想要两份数据，必须写 `clone`。
