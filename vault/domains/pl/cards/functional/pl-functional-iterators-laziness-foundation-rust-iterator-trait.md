---
id: pl-functional-iterators-laziness-foundation-rust-iterator-trait
node: functional.iterators-laziness
type: qa
step: 4
---
## Q
Rust 的 `Iterator` trait 是什么？适配器和消费者怎样分工，编译器怎么提醒你「没有消费」？

## A
`Iterator` trait 只有一个必须实现的方法：`fn next(&mut self) -> Option<Item>`，每次返回 `Some(下一个)`，耗尽时返回 `None`。其余几十个方法（`map`、`filter`、`take`、`sum`、`collect`……）都是基于它的**默认方法**。

分两类：

- **适配器**（adapter）：`map`、`filter`、`take` 等，返回一个包装了原迭代器的**新迭代器类型**，本身不做任何计算，是惰性的。
- **消费者**（consumer）：`sum`、`collect`、`find`、`for` 循环，反复调用 `next` 把迭代器耗尽，才触发计算。

```rust
let v = vec![1, 2, 3, 4, 5];
v.iter().map(|x| { println!("map {x}"); x * 2 });      // 没有消费者
// warning: unused `Map` that must be used
//   = note: iterators are lazy and do nothing unless consumed
let first = v.iter().map(|x| { println!("map {x}"); x * 2 }).find(|&x| x > 2);
// 输出 map 1 / map 2，first 为 Some(4)
```

第一句什么都不会执行，Rust 还在类型上标了 `#[must_use]`，编译器警告你「迭代器是惰性的，不消费就不做事」。第二句 `find` 在第二个元素就找到了答案，后面不再计算。

`for x in v` 其实就是对 `v.into_iter()` 反复调用 `next` 的语法糖。所有权也体现在这里：`iter()` 借用元素，`iter_mut()` 可变借用，`into_iter()` 取走所有权。
