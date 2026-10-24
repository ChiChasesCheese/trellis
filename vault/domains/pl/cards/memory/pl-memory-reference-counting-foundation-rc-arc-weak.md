---
id: pl-memory-reference-counting-foundation-rc-arc-weak
node: memory.reference-counting
type: qa
step: 3
---
## Q
Rust 的 `Rc`、`Arc` 和 `Weak` 是什么？它们解决什么问题，各自怎么用？

## A
Rust 默认每个值只有一个所有者。但有些数据确实需要多个所有者（图里的一个节点被多条边指向），这时用库类型 `Rc<T>`（Reference Counted）：把值放在堆上，附带一个计数；`Rc::clone(&a)` 不复制数据，只让计数加 1；每个 `Rc` 被丢弃时计数减 1，到 0 时值才被销毁。

```rust
let a = Rc::new(5);
let b = Rc::clone(&a);
println!("{}", Rc::strong_count(&a));   // 2
drop(b);
println!("{}", Rc::strong_count(&a));   // 1
```

三个相关类型：
- `Rc<T>`：计数用普通加减，只能在单个线程里用，便宜。
- `Arc<T>`（Atomic Rc）：计数用原子指令，可以跨线程共享，每次克隆/销毁略贵。
- `Weak<T>`：弱引用，指向同一个值，但**不增加强计数**，所以不会阻止值被销毁；要用时调用 `upgrade()`，得到 `Option<Rc<T>>`，值已销毁则为 `None`。

`Weak` 的用途是打破循环：父节点用 `Rc` 持有子节点，子节点用 `Weak` 指回父节点。如果两个方向都是 `Rc`，计数永远降不到 0，值泄漏，而且没有任何警告。

要记住的一个事实：在 Rust 里引用计数是一个需要主动选择的库类型，不是语言默认；循环必须自己用 `Weak` 避免。
