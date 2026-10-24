---
id: pl-conc-datarace-found-send-sync
node: concurrency.data-race-freedom
type: qa
step: 2
---
## Q
Rust 的 `Send` 和 `Sync` 是什么？为什么 `Rc` 不能放进线程，`RefCell` 不能被多个线程共享，而 `Arc<Mutex<T>>` 可以？

## A
**`Send` 和 `Sync`** 是两个没有方法的标记 trait（marker trait，只表达“这个类型有某种性质”），编译器根据类型的字段自动推导：
- `T: Send`：`T` 的值可以**移动**到另一个线程；
- `T: Sync`：`&T` 可以在多个线程间共享，即 `T` 能被多个线程同时只读借用。

`thread::spawn` 的签名要求闭包是 `Send`；闭包是否 `Send` 取决于它捕获的所有变量。于是编译器能在**编译期**检查“这个值能不能跨线程”。

三个典型例子（真实报错节选）：

**`Rc` 不是 `Send`**：`Rc` 的引用计数是普通整数加减，两个线程同时改会算错。
```rust
let r = Rc::new(5);
thread::spawn(move || println!("{}", r)).join().unwrap();
```
`error[E0277]: Rc<i32> cannot be sent between threads safely`，`the trait Send is not implemented for Rc<i32>`。换成原子计数的 `Arc` 才行。

**`RefCell` 不是 `Sync`**：它在运行时检查借用规则，但检查本身没有同步。
```rust
let c = Arc::new(RefCell::new(0));
let c2 = Arc::clone(&c);
thread::spawn(move || { *c2.borrow_mut() += 1; }).join().unwrap();
```
`error[E0277]: RefCell<i32> cannot be shared between threads safely`，并提示 “use `std::sync::RwLock` instead”。

**`Arc<Mutex<T>>` 合法**：`Arc` 是 `Send + Sync`（计数是原子的），`Mutex<T>` 是 `Sync`（所有访问都经过锁）。把 `RefCell` 换成 `Mutex`、`Rc` 换成 `Arc`，就是多线程版本：
```rust
let c = Arc::new(Mutex::new(0));
let c2 = Arc::clone(&c);
thread::spawn(move || { *c2.lock().unwrap() += 1; }).join().unwrap();
```
要点：单线程版共享可变状态是 `Rc<RefCell<T>>`，多线程版是 `Arc<Mutex<T>>`。它们是不同的类型，编译器强制你选对，规则写在类型里而不是文档里。
