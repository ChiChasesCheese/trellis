---
id: pl-memory-memory-safety-foundation-escape-hatches
node: memory.memory-safety
type: qa
step: 3
---
## Q
“内存安全”语言的逃生口是什么？Rust 的 `unsafe`、Go 的 `unsafe`/cgo、Java 的 JNI 和 Python 的 `ctypes` 各是什么，意味着什么？

## A
安全语言禁止直接操作原始地址，但总要有人做底层的事：实现 `Vec`、调用操作系统、和 C 库打交道。所以每门语言都留有逃生口，在其中编译器的保证失效，责任回到程序员身上：

- **Rust**：`unsafe { ... }` 块。里面可以解引用裸指针（raw pointer，不受借用检查的地址）、调用 `unsafe` 函数。它**不会关闭借用检查器**，只是开放这几项能力。没有 `unsafe` 就解引用裸指针，编译器报 `E0133`。
- **Go**：标准库的 `unsafe` 包（`unsafe.Pointer` 可以绕过类型系统）和 **cgo**（在 Go 里调用 C 代码）。
- **Java**：JNI（Java Native Interface，调用本地 C 代码）、`sun.misc.Unsafe`，以及较新的 FFM API（外部函数与内存访问）。
- **Python**：`ctypes`（把任意地址当指针用）和 C 扩展。例如 `ctypes.string_at(0)` 读地址 0，进程直接被 SIGSEGV 终止（本机退出码 139），没有 `IndexError`，也来不及 `try/except`。

设计原则是**缩小信任的范围**：只有这些带标记的区域需要审查，并且要把它们封装成对外安全的接口（例如 `Vec::push` 内部有 `unsafe`，对外是安全函数）。

要记住的一个事实：“内存安全语言”的准确含义是只用语言的安全部分写出的代码不会出现内存错误；`unsafe`、FFI、C 扩展里的 bug 仍然能打穿整个程序。
