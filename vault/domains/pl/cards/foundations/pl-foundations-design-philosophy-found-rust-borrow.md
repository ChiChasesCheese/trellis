---
id: pl-foundations-design-philosophy-found-rust-borrow
node: foundations.design-philosophy
type: qa
step: 3
---
## Q
Rust 的借用（borrowing）和借用检查器（borrow checker）是什么？它强制的核心规则是什么？

## A
所有权规定了值只有一个所有者。但函数经常只是想看一眼或改一下，不想接管所有权，于是有了借用：用 `&x` 创建一个不可变引用（可以有任意多个，只读），用 `&mut x` 创建可变引用（同一时刻只能有一个，可读可写）。引用是不拥有数据的指针，使用期间所有者不能走开。

借用检查器是编译器里的一个分析阶段，它强制一条规则：在任何时刻，对同一个值，要么有任意多个不可变引用，要么恰有一个可变引用，不能同时有。引用的存活范围只到它最后一次被使用为止。

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];        // 不可变借用
v.push(4);                // push 需要可变借用，而 first 还在使用
println!("{}", first);
```

编译失败，实际错误（缩短）：

```console
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
```

这条规则挡住的是一类真实的 bug：`push` 可能让向量重新分配内存，`first` 就会指向已释放的旧位置，在 C++ 里是悬空引用，在 Rust 里无法通过编译。规则的本质是「读者与写者互斥」，和读写锁同一个思想，只是在编译期检查，没有运行时开销。
