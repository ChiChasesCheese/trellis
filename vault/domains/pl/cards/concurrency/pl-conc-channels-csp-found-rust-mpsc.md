---
id: pl-conc-channels-csp-found-rust-mpsc
node: concurrency.channels-csp
type: qa
step: 4
---
## Q
Rust 标准库的 `mpsc` 通道是什么？“多个发送端、一个接收端”怎么用，发送时所有权会发生什么？

## A
`std::sync::mpsc`（multiple producer, single consumer，多生产者单消费者）提供一个通道，由两端组成：`Sender<T>`（可以 `clone`，每个生产者持有一个）和 `Receiver<T>`（只有一个，不能克隆）。

```rust
let (tx, rx) = mpsc::channel();
for id in 0..3 {
    let tx = tx.clone();                  // one Sender per producer
    thread::spawn(move || { for j in 0..2 { tx.send(id * 10 + j).unwrap(); } });
}
drop(tx);                                 // drop the original Sender
let mut got: Vec<i32> = rx.iter().collect();
got.sort();
println!("{:?}", got);
```
输出：`[0, 1, 10, 11, 20, 21]`。三个线程各发 2 个值。

要点：
1. **结束信号来自所有发送端被丢弃**：`rx.iter()` 在所有 `Sender`（包括主线程手里的原始 `tx`）都销毁后才结束，所以示例里必须 `drop(tx)`，否则 `iter()` 永远等下去。
2. `channel()` 创建的是**无界**队列，永不阻塞发送；`sync_channel(n)` 创建容量为 n 的有界通道（n=0 就是同步碰头）。
3. **发送会转移所有权**：`tx.send(s)` 把值 `s` 移进通道，之后发送方不能再使用 `s`：
```rust
let s = String::from("hello");
tx.send(s).unwrap();
println!("{}", s);
```
真实报错（节选）：`error[E0382]: borrow of moved value: s`，说明 `s` 已经被移动。这保证了“通过通信来共享内存”：交出去之后只有接收方拥有它。
4. 接收端被丢弃后，`send` 返回 `Err`，发送方可以据此知道没人再听了。
