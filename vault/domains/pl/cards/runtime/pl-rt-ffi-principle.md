---
id: pl-rt-ffi-principle
node: runtime.ffi
type: qa
step: 1
---
## Q
跨语言调用（FFI，Foreign Function Interface，外部函数接口）要解决什么问题？为什么语言之间的调用不能像同一语言内的函数调用那样直接？

## A
**为什么需要 FFI**：没有哪门语言包办一切。操作系统接口、加密库（OpenSSL）、数据库客户端、图形/GPU、数值内核（BLAS、LAPACK）、音视频编解码，都是用 C/C++（现在也有 Rust）写好的、几十年积累的代码。新语言要使用它们，就必须能调用 C。反过来，C 或 Python 程序也想使用 Rust/Go 写的组件。

**为什么不能直接调用**：两边对“一次函数调用长什么样”有不同约定：
1. **调用约定与 ABI**（Application Binary Interface，应用二进制接口）：参数放在哪些寄存器/栈上、返回值放哪、谁清理栈、结构体怎么布局。C 的 ABI 是事实上的“通用语”，几乎所有语言都能说 C ABI，所以 FFI 几乎都经过 C。
2. **数据表示不同**：C 字符串是以 `\0` 结尾的字节指针；Java 的 `String` 是 UTF-16 对象，Go 的字符串是“指针 + 长度”，Rust 的 `&str` 也是“指针 + 长度”，Python 的 `str` 是带头部的对象。跨边界必须**转换**（marshalling）。
3. **内存管理不同**：垃圾回收器可能移动对象（Java、Go），交给 C 的指针会失效；谁负责释放？C 的 `malloc` 内存不能交给 GC 管理。
4. **运行时状态**：Go 的 goroutine 栈是可增长的小栈，C 需要大的普通线程栈；Java 的线程要与 GC 同步安全点；Python 的 C API 需要持有 GIL。

**设计空间**（怎么跨）：
- 编译期绑定的“胶水代码”（Java JNI、Python C API、Go cgo）：每次调用经过一层生成的转接；
- 运行期动态绑定（Python `ctypes`、Java FFM API）：描述函数签名后直接调用，不用写 C 胶水；
- 同一 ABI 零胶水（Rust `extern "C"`）：Rust 本身可以按 C ABI 布局，调用几乎等于普通调用；
- 避开 FFI：用进程间通信（gRPC、管道）或 WebAssembly 模块。

核心权衡：**易用性、安全性、性能**三者不可兼得，下面各语言选的位置不同。
