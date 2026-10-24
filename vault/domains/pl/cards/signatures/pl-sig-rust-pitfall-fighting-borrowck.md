---
id: pl-sig-rust-pitfall-fighting-borrowck
node: signatures.rust
type: qa
step: 9
---
## Q
新手与有经验的工程师在 Rust 里最常见的陷阱是什么？“与借用检查器的拉锯”和用逃生手段绕过它，各会带来什么问题？

## A
**陷阱一：持有引用的同时修改容器**。这是最常见的编译错误，真实输出：

```rust
let mut v = vec![1, 2, 3];
let first = &v[0];
v.push(4);
println!("{}", first);
// error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
```

编译器是对的：`push` 可能搬动内存，`first` 会悬空。修法是缩短借用的生命周期（先用完 `first`，再 `push`），或先复制出值。

**陷阱二：用 `clone()` 掩盖设计问题**。遇到所有权错误就 `.clone()`，编译通过了，但在热路径上大量复制数据，性能不再“零成本”。症状：基准测试里分配次数很多；代码里满是 `.clone()`。

**陷阱三：用 `Rc<RefCell<T>>` 模仿别的语言的共享可变对象**。这把借用检查推迟到运行时：违规时 `RefCell` 在运行时 panic（`already borrowed`），失去了 Rust 的主要优势，还要处理循环引用造成的泄漏（`Rc` 不检测环）。偶尔必要，但常常说明数据结构该重新设计。

**陷阱四：`unwrap()` 满天飞**。每个 `unwrap` 都是一个潜在的 panic。生产服务里，一个未处理的 `None` 会让线程（或整个进程）崩溃。

**陷阱五：持有锁跨越 `.await`**。在 async 代码里持有 `std::sync::Mutex` 的守卫跨过 `await`，可能死锁或使 future 不再是 `Send`。

**陷阱六：自引用结构**。想让一个结构体里的字段引用同结构体的另一个字段，借用检查器无法表达；需要 `Pin`、索引或专门的库。

**如何调试拉锯**：
1. 读完整条错误信息，它通常指出冲突的两个借用的位置，并给出建议。
2. 画出“谁拥有、谁借用、借多久”。
3. 缩小作用域，或引入索引/ID 代替引用。
4. 仍不行再考虑 `Rc`/`RefCell`，并记下理由。

**教训**：编译错误是 Rust 的反馈机制；最危险的不是报错，而是用逃生手段让报错消失，却把问题留到运行时。
