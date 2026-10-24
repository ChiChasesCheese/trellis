---
id: pl-conc-os-threads-found-rust
node: concurrency.os-threads
type: qa
step: 3
---
## Q
Rust 的 `thread::spawn`、`JoinHandle` 和 `move` 闭包是什么？为什么直接借用局部变量会被编译器拒绝？

## A
- **`thread::spawn(闭包)`**：新建一个 OS 线程执行闭包（匿名函数）。它返回 **`JoinHandle<T>`**，`T` 是闭包的返回类型。
- **`handle.join()`**：等线程结束，返回 `Result<T, _>`：线程正常结束是 `Ok(返回值)`，线程里发生 panic 则是 `Err`。错误是普通的值，调用者必须决定怎么处理。
- **`move` 闭包**：闭包默认只“借用”它用到的外部变量；`move` 让闭包把用到的变量的**所有权**搬进去。

例子：
```rust
let hs: Vec<_> = (1..=3).map(|i| thread::spawn(move || i * i)).collect();
let r: Vec<i32> = hs.into_iter().map(|h| h.join().unwrap()).collect();
println!("{:?}", r);
let h = thread::spawn(|| { if true { panic!("boom"); } 1 });
println!("{}", h.join().is_err());
```
输出：`[1, 4, 9]`；panic 时 stderr 打印 `thread '<unnamed>' panicked ... boom`，然后输出 `true`。

**为什么借用局部变量不行**：新线程的生命周期不受创建者控制，它可能比创建它的函数活得更久。如果闭包只借用了函数里的局部变量 `v`，函数返回后 `v` 被销毁，线程里就是悬空引用。所以 `spawn` 要求闭包不借用任何栈上的数据（类型约束写作 `'static`）：
```rust
let v = vec![1, 2, 3];
let h = std::thread::spawn(|| println!("{:?}", v));
```
真实报错（节选）：`error[E0373]: closure may outlive the current function, but it borrows v`，并提示用 `move` 关键字。改成 `move || ...` 把 `v` 的所有权交给线程即可。

这是 Rust 的基本思路：悬空引用在**编译期**就被排除，而不是在运行时偶发崩溃。
