---
id: pl-conc-os-threads-unique-rust-static
node: concurrency.os-threads
type: qa
step: 7
---
## Q
Rust 的 `thread::spawn(|| println!("{:?}", v))` 为什么编译不过？这和 Java、Python 里线程直接使用局部变量有什么本质区别？

## A
Rust 编译器在编译期拒绝了这段代码：
```rust
let v = vec![1, 2, 3];
let h = std::thread::spawn(|| println!("{:?}", v));
h.join().unwrap();
```
真实报错（节选）：
```
error[E0373]: closure may outlive the current function,
but it borrows `v`, which is owned by the current function
note: function requires argument type to outlive `'static`
help: use the `move` keyword
```
原因：新线程的生命周期不受创建它的函数控制，它可能比 `v` 活得更久。`thread::spawn` 要求闭包是 `'static`（不借用任何栈上的数据），所以编译器不允许闭包只借用 `v`。改成 `move || ...`，把 `v` 的所有权整个交给新线程即可。同时闭包还必须满足 `Send`（可以安全地搬到别的线程），编译器会逐字段检查。

对比：
- Java 的 lambda 只能捕获不再被修改的局部变量，或对象引用；两个线程同时改同一个对象是否安全，编译器不管。
- Python 的闭包直接引用外层变量，线程之间随便共享。

Rust 把「线程会不会访问已经失效的数据」和「数据能不能跨线程」变成了编译期规则，这是它的并发安全的起点。
