---
id: pl-conc-structured-unique-rust-scope
node: concurrency.structured-concurrency
type: qa
step: 8
---
## Q
Rust 的 `thread::scope` 为什么能让子线程直接借用局部变量，而普通的 `thread::spawn` 做不到？这说明结构化并发带来的什么能力？

## A
普通 `thread::spawn` 的线程可能比创建它的函数活得更久，所以要求闭包 `'static`（不借用栈上数据），只能把数据 `move` 进去或放进 `Arc`。`thread::scope` 保证**作用域结束前所有子线程已 join**，因此编译器知道子线程活不过父函数，借用局部变量就是安全的：
```rust
let mut data = vec![1, 2, 3, 4, 5, 6];
let (left, right) = data.split_at_mut(3);
thread::scope(|s| {
    s.spawn(|| { for x in left.iter_mut() { *x *= 10; } });
    s.spawn(|| { for x in right.iter_mut() { *x += 1; } });
});                          // every thread is joined here
println!("{:?}", data);
```
输出：`[10, 20, 30, 5, 6, 7]`。两个线程分别借用了数据的不相交两半，没有 `Arc`、没有 `Mutex`、没有拷贝。借用检查器验证了两段可变借用不重叠（`split_at_mut`）。

这揭示结构化并发的**真正价值不只是少几个 bug，而是让“生命周期”这一事实成为程序结构的一部分**：
- 作用域嵌套 ⇒ 任务生命周期嵌套 ⇒ 借用安全 ⇒ 不需要引用计数和锁来延长生命周期。
- 在 GC 语言里没有悬空问题，但同样得益于“确定的收尾点”：资源（连接、文件）在作用域结束时一定已经没人用了。
- Java 的 `StructuredTaskScope` 和 Python 的 `TaskGroup` 没有借用检查器，所以只能拿到“不泄漏、能传播错误和取消”这几项，拿不到“借用局部变量的安全性”。

并行的数据处理库（rayon）依赖同样的结构保证，才能让并行迭代器直接借用输入切片。
