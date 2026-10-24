---
id: pl-memory-reference-counting-rc-vs-arc
node: memory.reference-counting
type: qa
step: 6
---
## Q
Rust 为什么要把引用计数分成 `Rc` 和 `Arc` 两个类型？把 `Rc` 发给另一个线程会怎样？

## A
区别只在计数的更新方式：
- `Rc<T>`：普通加减，不是原子操作，便宜，但两个线程同时增减同一个计数会丢失更新，导致提前释放或泄漏。
- `Arc<T>`（atomic reference counting）：用原子指令增减，线程安全，但每次克隆/销毁都有原子操作的成本，多核争用同一个计数时更明显。

别的语言把这个选择交给文档和纪律，Rust 交给类型系统。`Rc` 没有实现 `Send` 这个标记 trait（表示「可以安全地移动到另一个线程」），所以：

```rust
let a = Rc::new(1);
thread::spawn(move || println!("{}", a)).join().unwrap();
```

```console
error[E0277]: `Rc<i32>` cannot be sent between threads safely
  the trait `Send` is not implemented for `Rc<i32>`
```

编译器直接拒绝。换成 `Arc::new(1)` 就能通过。你不可能「不小心」在多线程里用了非原子计数，错误发生在编译期而不是线上。

对比：
- C++ 的 `shared_ptr` 只有一个版本，标准要求计数更新是线程安全的，所以每个用户都为线程安全付费（没有 `Rc` 这样的便宜选项）；它保护的只是计数，被指向的对象本身的并发读写仍是用户的责任；
- Python（默认构建）靠 GIL 保证计数更新不被打断；Python 3.13 起可选的 free-threaded 构建没有 GIL，改用偏向引用计数（biased reference counting）等技术：同一线程拥有的对象走快速路径，跨线程才用原子操作；
- Swift 的 ARC 为了线程安全也用原子操作，成为其性能开销的来源之一。
