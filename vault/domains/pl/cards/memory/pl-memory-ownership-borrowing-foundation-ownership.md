---
id: pl-memory-ownership-borrowing-foundation-ownership
node: memory.ownership-borrowing
type: qa
step: 2
---
## Q
Rust 的所有权（ownership）规则具体是什么？一个值被传给函数后会发生什么？

## A
所有权有三条规则：
1. 每个值有且只有一个**所有者**（owner），通常就是持有它的变量。
2. 所有者离开作用域时，值被销毁（释放内存，调用 `Drop`）。
3. 把值赋给另一个变量，或按值传给函数，所有权就**移动**（move）过去，原变量作废。

```rust
fn consume(v: Vec<i32>) -> usize { v.len() }

fn main() {
    let v = vec![1, 2, 3];
    println!("{}", consume(v));   // 3; ownership of v moves into consume
    println!("{:?}", v);          // compile error
}
```

`consume` 返回时，它的参数 `v` 离开作用域，堆上的 `Vec` 被释放。如果调用者还能访问 `v`，就成了悬空引用，所以编译器拒绝最后一行：

```console
error[E0382]: borrow of moved value: `v`
```

这样，释放的责任始终清楚：谁是当前所有者，谁负责在作用域结束时释放，不会重复释放，也不会忘记。

要记住的一个事实：所有权把“谁负责释放”写进了每个值的当前持有者里，由编译器检查，运行时没有任何额外成本。
