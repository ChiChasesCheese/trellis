---
id: pl-binding-parameter-passing-foundation-rust-move-borrow
node: binding.parameter-passing
type: qa
step: 5
---
## Q
Rust 的函数参数有哪几种传法？`T`、`&T`、`&mut T` 在签名里分别向调用者承诺了什么？

## A
Rust 把「函数会怎样对待你的数据」写进参数类型，调用者读签名就知道：

- `v: T`（按值，**移动**）：所有权转给函数，调用者的变量失效。函数负责销毁或返回它。
- `v: &T`（共享借用）：函数只能读，调用者保留所有权，期间可以有多个读者。
- `v: &mut T`（独占借用）：函数可以改，期间没有任何其他读者或写者；调用点必须写 `&mut x`，一眼可见。
- 实现了 `Copy` 的小类型（整数、浮点）按值传就是复制，原变量仍可用。

```rust
fn take(v: Vec<i32>) -> usize { v.len() }
fn peek(v: &Vec<i32>) -> usize { v.len() }
fn push(v: &mut Vec<i32>) { v.push(99); }
fn swap(a: &mut i32, b: &mut i32) { std::mem::swap(a, b); }

let mut v = vec![1];
push(&mut v);
println!("{} {:?}", peek(&v), v);   // 2 [1, 99]
let (mut a, mut b) = (1, 2);
swap(&mut a, &mut b);               // a=2 b=1: a working swap
take(v);                            // v is moved; using v afterwards is a compile error
```

注意 `swap(&mut a, &mut b)` 真的交换了调用者的两个变量：在四门语言里，只有 Rust 的 `&mut`（和 Go 的指针）能让函数改变调用者的**局部变量**，而且 Rust 的版本由编译器保证没有别名、没有悬空。

和 Java、Python 的差别：它们把「共享可变的对象」当默认，Rust 把它变成需要显式申请的特例；代价是调用者要多写 `&`、`&mut`，签名要想清楚所有权。

要记住的事实：传参在 Rust 里不是实现细节，而是 API 契约。选 `T`、`&T` 还是 `&mut T`，就是在回答「谁拥有、谁能改」。
