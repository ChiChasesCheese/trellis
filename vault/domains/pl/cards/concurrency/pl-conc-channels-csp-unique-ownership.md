---
id: pl-conc-channels-csp-unique-ownership
node: concurrency.channels-csp
type: qa
step: 9
---
## Q
Rust 的 `tx.send(s)` 之后再使用 `s` 为什么编译不过？这和 Go、Java 里「发出去之后还能改」有什么本质区别？

## A
Rust 的 `send` 按值接收参数，会**移动**（move）所有权：
```rust
let (tx, rx) = mpsc::channel::<String>();
let s = String::from("hello");
tx.send(s).unwrap();
println!("{}", s);
```
真实报错（节选）：
```
error[E0382]: borrow of moved value: `s`
note: move occurs because `s` has type `String`,
which does not implement the `Copy` trait
note: value moved here: tx.send(s).unwrap();
```
`s` 已经交给通道，发送方不能再碰它。编译器保证了「通过通信来共享内存」这句话的前半截：同一时刻只有一个所有者，数据竞争不可能发生，而且不需要拷贝（`String` 只是搬动指针）。

对比：
- Go 的通道发送的是值的拷贝。如果值是指针、切片或 map，发送方和接收方就共享同一块底层内存，之后双方都能改，数据竞争只能靠自觉避免（或用 `-race` 检测）。
- Java 的 `BlockingQueue` 传的是对象引用，放进队列后生产者仍持有该引用，可变对象同样是共享的。
- Python 同理，队列里是对象引用。
- C++ 用 `std::move`（把对象标记为“可被搬走”）把值放进队列，被搬走的变量仍然合法、仍能编译。实测 `q.push(std::move(s))` 之后读 `s`：`-Wall -Wextra` 没有任何警告，输出 `[] size=0`，一个“空字符串”，不是错误。所有权转移只是约定，没有编译期保证。

规律：通道本身只提供同步，不负责所有权。只有 Rust 的所有权规则让「发出去就是交出去」成为编译期保证。
