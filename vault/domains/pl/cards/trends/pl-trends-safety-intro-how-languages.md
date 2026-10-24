---
id: pl-trends-safety-intro-how-languages
node: trends.safety-push
type: qa
step: 3
---
## Q
Java、Go、Python 和 Rust 各自靠什么机制做到内存安全？各自留下了哪些“逃生舱”（escape hatch）？

## A
**机制**：
- **Java、Python、Go（垃圾回收加边界检查）**：对象由运行时管理，只要还有引用就不会被回收，所以没有悬空指针；每次数组访问检查下标，越界就抛异常。不能做任意的指针算术。
- **Rust（所有权与借用，编译期）**：每个值有唯一的所有者，借用有生命周期，编译器证明引用不会比数据活得久、不会同时存在可变别名。越界仍在运行时检查。没有垃圾回收的成本。

**逃生舱**：这些保证都有边界，进入边界之外的代码就回到 C 的风险：
- **Rust 的 `unsafe`** 块：开发者向编译器声明“这里我自己保证安全”。标准库内部大量使用，应用代码应极少使用。
- **Java 的 JNI 与 `sun.misc.Unsafe`**，以及较新的 Foreign Function & Memory API。
- **Go 的 `unsafe` 包与 `cgo`**：调用 C 代码。
- **Python 的 `ctypes` 与 C 扩展**：NumPy、PyTorch 的核心都是 C/C++。

一个 Python 的例子：

```python
import ctypes; ctypes.string_at(0)    # read address 0
# Fatal Python error: Segmentation fault
```

真实结果是进程直接崩溃。再看 Rust：

```rust
let p = v.as_ptr(); drop(v);
let x = unsafe { *p };   // compiles; reads freed memory
```

编译通过，运行得到一个垃圾值（本机一次得到 `4`），没有任何错误。

**关键设计点**：Rust 的做法是**把不安全局限在显式的块里**，可以用 `grep unsafe` 审计；GC 语言的逃生舱则是“调用另一门语言”，边界在 FFI（外部函数接口）。无论哪种，安全的范围就是不使用逃生舱的那部分代码。
