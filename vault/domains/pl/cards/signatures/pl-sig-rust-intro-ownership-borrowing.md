---
id: pl-sig-rust-intro-ownership-borrowing
node: signatures.rust
type: qa
step: 2
---
## Q
Rust 的所有权（ownership）、移动（move）和借用（borrowing）是什么？两条规则分别在编译期拦住什么错误，真实报错是什么？

## A
**所有权**：每个值有且只有一个所有者（一个变量）。所有者离开作用域时，值被释放（运行 `Drop`）。所以不需要垃圾回收，也不会重复释放。

**移动**：把一个拥有堆数据的值赋给另一个变量，或传给函数，所有权就**转移**了，原变量不能再用。

```rust
let v = vec![1, 2, 3];
let n = consume(v);          // ownership of v moves into consume
println!("{} {}", n, v.len());
// error[E0382]: borrow of moved value: `v`
//   move occurs because `v` has type `Vec<i32>`, which does not implement `Copy`
```

这拦住的是“释放后使用”：`consume` 结束时 `v` 已被释放，再用就是悬空引用。

**借用**：不转移所有权，只借用引用。两条规则：
1. 任何时刻，要么有**多个只读引用**（`&T`），要么有**一个可变引用**（`&mut T`），不能同时存在。
2. 引用不能比它指向的数据活得更久（生命周期）。

```rust
let mut s = String::from("a");
let r1 = &mut s;
let r2 = &mut s;       // second mutable borrow
// error[E0499]: cannot borrow `s` as mutable more than once at a time
```

这拦住的是“别名加修改”：两个可变引用可能同时改一个数据，造成数据竞争、迭代器失效等。同一个规则也是并发安全的基础。

**心智模型**：把值想成图书馆里的一册藏书，所有者是它的登记人。你可以把它借给许多人只读（共享借用），或借给一个人修改（独占借用），但借出期间你自己不能改，别人也不能同时改。

**要记住的一点**：这些检查全在编译期，没有任何运行时代价；所以代价是编译器会拒绝一些“其实安全”的程序，你需要换一种写法让它能证明。
