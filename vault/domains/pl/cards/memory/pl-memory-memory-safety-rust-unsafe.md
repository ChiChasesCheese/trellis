---
id: pl-memory-memory-safety-rust-unsafe
node: memory.memory-safety
type: qa
step: 4
---
## Q
Rust 的 `unsafe` 块能做什么，不能做什么？它和别的语言的逃生口相比独特在哪里？

## A
没有 `unsafe` 时，解引用裸指针会被拒绝：

```rust
let x = 5;
let p = &x as *const i32;
println!("{}", *p);
```

```console
error[E0133]: dereference of raw pointer is unsafe and requires unsafe function or block
note: raw pointers may be null, dangling or unaligned; they can violate aliasing rules and cause data races
```

包进 `unsafe` 就能编译，运行输出 `5`：

```rust
let y = unsafe { *p };
```

`unsafe` 只开放五项能力：解引用裸指针、调用 `unsafe` 函数、访问可变静态变量、实现 `unsafe trait`、访问联合体（`union`）字段。**它不会关闭借用检查器**，`unsafe` 块里的普通引用仍然要遵守借用规则。你是在向编译器承诺：「这几行的安全性，我自己保证。」

独特之处：
1. **范围显式且可搜索**：全部不安全的代码都写着 `unsafe`，`grep unsafe` 就能审计。Go 的 `unsafe.Pointer` 和 Java 的 `Unsafe` 也有标记，但 Rust 把它做成了语法。
2. **对外封装成安全接口**：标准库的 `Vec`、`Rc`、`Mutex` 内部全是 `unsafe`，对外却是安全 API。用户只用安全部分，就继承标准库维护者的验证成果。
3. **安全代码不能触发未定义行为**：这是语言的承诺；如果出现了，bug 一定在某个 `unsafe` 块里，而不是任意位置。

对比 C：整个程序都是「`unsafe`」，没有边界，审计面是全部代码。

代价：`unsafe` 代码仍可能写错，且错误可以泄漏到安全代码里。社区工具 Miri（Rust 的解释器，检测未定义行为）常用于检查它。
