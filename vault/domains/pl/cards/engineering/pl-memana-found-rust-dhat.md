---
id: pl-memana-found-rust-dhat
node: engineering.memory-analysis
type: qa
step: 5
---
## Q
Rust 没有 GC，为什么还会泄漏？怎样用 dhat 观察堆上还剩什么？

## A
Rust 的内存安全保证不包括「一定释放」：泄漏是**安全**行为，编译器不会拦。常见成因：
- `Rc` / `Arc`（引用计数指针，计数降到 0 才释放）形成**引用环**：A 持有 B、B 持有 A，两个计数永远不为 0；
- `Box::leak`、`std::mem::forget` 主动放弃释放；
- 无界增长的 `Vec`、`HashMap`、通道、缓存。

**dhat**（`dhat` crate，思路来自 Valgrind 的 DHAT 工具）是堆剖析器：把全局分配器换成 `dhat::Alloc`，每次分配都记录调用栈。退出时输出 JSON，用查看器看三个视角：总分配、峰值时刻仍存活的（`t-gmax`）、结束时刻仍存活的（`t-end`）。测试模式下可以直接读统计。构造 1000 对互相引用的节点（`RefCell` 是允许在运行时检查借用的前提下修改内部值的容器，这里用来在建好节点之后再回头设置 `next`）：

```rust
struct Node { _payload: Vec<u8>, next: RefCell<Option<Rc<Node>>> }
fn leak_pair() {
    let a = Rc::new(Node { _payload: vec![0; 10_000], next: RefCell::new(None) });
    let b = Rc::new(Node { _payload: vec![0; 10_000], next: RefCell::new(Some(a.clone())) });
    *a.next.borrow_mut() = Some(b.clone());   // a -> b -> a
}
```

调用 1000 次后读 `dhat::HeapStats::get()`：

```text
live at end: 4000 blocks, 20112000 bytes
```

每对节点留下 4 个块（2 个 `Rc` 节点加 2 个 `Vec`），共约 20 MB，程序结束时仍然存活，这就是泄漏的直接证据。修复：环中的一条边改用 `Weak`（不增加强计数的引用）。
