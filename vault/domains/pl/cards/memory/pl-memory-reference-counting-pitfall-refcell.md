---
id: pl-memory-reference-counting-pitfall-refcell
node: memory.reference-counting
type: qa
step: 8
---
## Q
Rust 里 `Rc<RefCell<T>>` 的组合有什么陷阱？它把哪部分检查从编译期推迟到了运行期？

## A
`Rc` 让多个所有者共享同一个值，但共享的 `Rc` 只给不可变访问。要想修改，需要内部可变性（interior mutability）：`RefCell<T>`。它在运行期维护一个借用状态，规则与编译期相同：任意时刻要么有多个不可变借用，要么只有一个可变借用。违反规则不是编译错误，而是 panic。

```rust
let shared = Rc::new(RefCell::new(vec![1]));
let a = Rc::clone(&shared);
let b = Rc::clone(&shared);
let r1 = a.borrow_mut();
let r2 = b.borrow_mut();      // second mutable borrow, same cell
println!("{} {}", r1.len(), r2.len());
```

这段代码能通过编译，运行时：

```console
thread 'main' panicked at bm.rs:8:16:
RefCell already borrowed
```

也就是说，用了 `Rc<RefCell<T>>` 后，Rust 最有价值的「借用冲突在编译期报错」被降级成「运行期才发现」，行为和 Java、Python 里的对象共享相近，但多了崩溃的可能。

使用建议：
1. 优先用单一所有权加 `&mut` 重构数据流，把 `Rc<RefCell<T>>` 留给图、GUI 树这类确实需要共享可变状态的场景。
2. 持有 `borrow_mut()` 的时间越短越好，避免在持有期间调用可能再次借用同一单元的代码。
3. 多线程下对应的是 `Arc<Mutex<T>>`，冲突表现为阻塞而不是 panic。
