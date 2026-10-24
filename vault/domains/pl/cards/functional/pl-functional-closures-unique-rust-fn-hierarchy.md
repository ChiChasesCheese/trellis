---
id: pl-functional-closures-unique-rust-fn-hierarchy
node: functional.closures
type: qa
step: 8
---
## Q
为什么说 Rust 的 `Fn`/`FnMut`/`FnOnce` 把「闭包怎样使用环境」写进了类型？这和 Java 的 effectively final 有什么哲学差异？

## A
Rust 闭包的 trait 回答了三个其他语言留给程序员自己判断的问题：

- 这个闭包会不会改变状态？（`Fn` 不改，`FnMut` 改）
- 能不能被调用多次？（`FnOnce` 不能）
- 能不能被多个线程同时调用？（`Fn` 且捕获的东西 `Sync`）

调用方的函数签名因此携带了契约：`fn run<F: FnOnce()>(f: F)` 说「我只调用一次，所以你可以放心把所有权交给我」；`fn run_many<F: Fn()>(f: F)` 说「我会反复调用，你的闭包不能消耗状态」；`thread::spawn` 要求 `FnOnce + Send + 'static`，说「这个闭包会被移到别的线程，不能借用当前栈」。编译器据此在调用点检查，不匹配就报错。

**对比 Java**：Java 的 lambda 也要面对同样的问题——并发执行、状态修改、生命周期——但它用一条**一刀切的规则**回答：不许修改捕获的局部变量。简单、易懂，但表达力有限，要在对象里藏可变状态，规避这条规则。Rust 用类型系统给出**细粒度**的答案，让合法的用法（`FnMut` 累加计数）能直接写出来，非法的（把借用的变量送去别的线程）被拒绝。

哲学：Java 偏好「简单规则，保守安全」；Rust 偏好「精确表达，由编译器验证」。代价是 Rust 的学习曲线，收益是同样的闭包在高并发里也不需要加锁来补。
