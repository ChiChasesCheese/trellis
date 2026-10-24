---
id: pl-functional-immutability-foundation-rust-let-mut
node: functional.immutability
type: qa
step: 3
---
## Q
Rust 的默认不可变和 `mut` 是什么意思？它与借用规则（`&` 与 `&mut`）有什么关系？

## A
Rust 的变量**默认不可变**：`let v = vec![1, 2, 3];` 之后不能 `v.push(4)`，需要写 `let mut v`。

```rust
let v = vec![1, 2, 3];
v.push(4);
// error[E0596]: cannot borrow `v` as mutable, as it is not declared as mutable
```

不可变是**深的**：`v` 是 `Vec` 的所有者，要修改它就必须有可变访问权，而 `let` 不给这个权限（这与 Java 的 `final` 只管绑定不同）。

更深一层是借用规则：对一个值，任何时刻只能有**要么任意多个不可变引用 `&T`，要么一个可变引用 `&mut T`**，二者不能同时存在。

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];       // 不可变借用
v.push(4);               // 需要可变借用
println!("{first}");
// error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
```

这条规则在 Java 里没有对应物：Java 里 `first` 持有的是元素引用，`push` 导致内部数组重分配，会产生迭代器失效（`ConcurrentModificationException`）或悬空视图。Rust 在编译期就阻止这种别名加修改的组合。

所以 Rust 的 `mut` 不仅是「这个变量能改」，更是**排他访问权**的声明：看到 `&mut` 的人知道，调用期间没有别人能同时读写这个值。
