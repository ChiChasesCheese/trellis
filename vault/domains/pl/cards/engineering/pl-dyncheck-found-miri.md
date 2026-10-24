---
id: pl-dyncheck-found-miri
node: engineering.dynamic-checkers
type: qa
step: 4
---
## Q
Rust 的 Miri 是什么？它能发现什么，为什么说它比 sanitizer 更严格？

## A
**Miri** 是 Rust 的**解释器**：它不生成机器码，而是直接解释 Rust 的中层中间表示 MIR（Mid-level IR），每执行一步都检查「这一步是不是未定义行为」。需要 nightly 工具链，用 `cargo +nightly miri run` 或 `miri test` 运行。

**它检查的**，主要是 `unsafe` 代码是否守住了 Rust 的规则：
- 越界访问、释放后使用、重复释放；
- 未初始化内存的读取、未对齐的指针访问；
- 违反借用别名规则（Stacked Borrows 或 Tree Borrows 模型）；
- 有限的数据竞争检测。

**例**：释放一个 `Vec` 后，用保留的裸指针读取：

```rust
let v = vec![1u8, 2, 3, 4];
let p = v.as_ptr();
drop(v);
let x = unsafe { *p.add(1) };   // use after free
```

stable 工具链的 `cargo run` 直接运行，结果是 `0`：读到已释放内存里的垃圾，没有任何提示。Miri 的输出：

```console
error: Undefined Behavior: in-bounds pointer arithmetic failed: alloc291 has been freed, so this pointer is dangling
 --> src/main.rs:5:23
help: alloc291 was allocated here:
 --> src/main.rs:2:13
help: alloc291 was deallocated here:
 --> src/main.rs:4:5
```

它同时给出了出错位置、分配点（第 2 行）和释放点（第 4 行）。

**为什么比 sanitizer 严格**：ASan 只能发现「访问了不该访问的地址」，Miri 知道每个指针的来源和权限，可以发现「地址上合法、但违反语言规则」的访问，比如用一个已经失效的别名去读写。

**代价**：比原生慢一到两个数量级，所以只对 `unsafe` 密集的模块、小测试集运行；对外部 C 函数调用（FFI）的支持很有限；和所有动态工具一样，只检查实际执行的路径。
