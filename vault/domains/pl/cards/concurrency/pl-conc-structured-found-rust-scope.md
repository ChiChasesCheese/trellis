---
id: pl-conc-structured-found-rust-scope
node: concurrency.structured-concurrency
type: qa
step: 5
---
## Q
Rust 的 `thread::scope` 是什么？它和普通 `thread::spawn` 的使用区别在哪里？

## A
`std::thread::scope(|s| { ... })` 创建一个线程作用域。在闭包里用 `s.spawn(...)` 启动的线程，**保证在 `scope` 调用返回之前全部结束**（自动 join）。
- 普通 `thread::spawn`：线程可以比创建者活得更久，所以闭包不能借用局部变量，必须 `move` 或用 `Arc`；
- `thread::scope`：线程的生命周期被限制在作用域内，所以闭包**可以直接借用**外面的局部变量。

例子：把一个 `Vec` 分成两半，两个线程各改一半：
```rust
let mut data = vec![1, 2, 3, 4, 5, 6];
let (left, right) = data.split_at_mut(3);
thread::scope(|s| {
    s.spawn(|| { for x in left.iter_mut() { *x *= 10; } });
    s.spawn(|| { for x in right.iter_mut() { *x += 1; } });
});                          // every thread is joined here
println!("{:?}", data);
```
输出：`[10, 20, 30, 5, 6, 7]`。`split_at_mut` 返回两段不重叠的可变借用，编译器据此知道两个线程不会互相踩；没有 `Arc`、没有 `Mutex`、没有拷贝。

如果某个子线程 panic，`scope` 在所有线程结束后会 panic 把错误传上去。

注意：`thread::scope` 保证“不泄漏、不悬空”，但**不提供取消**——线程要自己检查一个共享的标志位（如 `AtomicBool`）决定何时退出。tokio 的 `JoinSet` 是 async 版本：任务属于集合，`JoinSet` 被丢弃时其中的任务被取消。
