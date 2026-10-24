---
id: pl-memory-ownership-borrowing-foundation-borrows
node: memory.ownership-borrowing
type: qa
step: 3
---
## Q
Rust 的借用（`&T` 与 `&mut T`）是什么？“可以多个读，或者一个写”的规则在代码里长什么样？

## A
每次传参都交出所有权太不方便，所以 Rust 允许**借用**：临时拿到一个引用，不转移所有权，借用结束后原所有者继续用。

- `&v`：**共享引用**（shared reference），只能读。同一时间可以有任意多个。
- `&mut v`：**可变引用**（mutable reference），可以读写。同一时间只能有一个，并且此时不能有任何其他引用（包括只读的）。

```rust
fn peek(v: &Vec<i32>) -> usize { v.len() }       // read only
fn add(v: &mut Vec<i32>) { v.push(4); }          // may modify

let mut v = vec![1, 2, 3];
println!("{}", peek(&v));     // 3
add(&mut v);
println!("{:?}", v);          // [1, 2, 3, 4]; v is still ours
```

违反规则时编译器报错，例如拿着指向第 0 个元素的只读引用又去 `push`：

```console
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
```

为什么要有这条规则：`push` 可能让 `Vec` 重新分配缓冲区，旧的只读引用就指向了已释放的内存。

借用检查器（borrow checker）还有一个宽松之处：引用只在**最后一次使用**之前有效。`let r = &s; println!("{}", r); s.push('!');` 是合法的，因为 `r` 在 `push` 之前就不再用了。

要记住的一个事实：Rust 规定“读者可以很多，写者只能一个且独占”，这条规则同时消灭了迭代器失效、悬空引用和数据竞争。
