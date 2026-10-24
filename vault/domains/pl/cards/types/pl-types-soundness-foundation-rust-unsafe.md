---
id: pl-types-soundness-foundation-rust-unsafe
node: types.soundness
type: qa
step: 6
---
## Q
Rust 的「安全 Rust 是可靠的」是什么意思？`unsafe` 怎样划出信任边界，什么样的封装算 sound，什么样算 unsound？

## A
Rust 承诺：**只写安全代码（不用 `unsafe`），不会出现未定义行为**，包括悬空引用、数据竞争、越界访问、类型混淆。编译器强制执行这一点。例如悬空引用在编译期就被拒绝：

```rust
let r;
{ let x = 5; r = &x; }
println!("{r}");
// error[E0597]: `x` does not live long enough
```

但有些事编译器无法证明安全，如裸指针解引用、调用 C 函数、手写数据结构的内部。这时用 `unsafe` 块：它**不是关闭检查**，而是程序员说「这里的安全性由我来证明」。`unsafe` 把验证责任从编译器转给人，并把需要审计的代码集中到有标记的小范围。

关键概念是**健全的封装**（sound abstraction）：一个对外安全的函数，不管调用者传什么合法参数，都不会触发未定义行为。内部可以用 `unsafe`，但必须自己建立前提条件：

```rust
fn nth_ok(v: &[i32], i: usize) -> Option<i32> {
    if i < v.len() { Some(unsafe { *v.get_unchecked(i) }) } else { None }
}
fn nth(v: &[i32], i: usize) -> i32 {      // safe signature, no check: unsound
    unsafe { *v.get_unchecked(i) }
}
```

`nth_ok` 自己检查了下标，是 sound 的。`nth` 签名是安全的，却把前提条件推给了调用者，传入越界下标就是未定义行为，所以它是 **unsound**（不健全）。调试构建里能看到：

```text
panicked at u.rs:3:17:
unsafe precondition(s) violated: slice::get_unchecked requires that the index is within the slice
```

这条检查是可选的、尽力而为的，发布构建里不会有。

规则：**安全函数的健全性是库作者的责任，不是调用者的。**如果一个函数可能触发未定义行为，就必须标成 `unsafe fn`，把义务写进签名。标准库的 `Vec`、`Rc`、`Mutex` 内部都是 `unsafe`，但对外健全。编译器本身偶尔也有健全性缺陷，Rust 项目用 `I-unsound` 标签单独追踪这类问题。
