---
id: pl-rt-ffi-found-rust
node: runtime.ffi
type: qa
step: 4
---
## Q
Rust 怎样调用 C，又怎样把 Rust 暴露给别的语言？`extern "C"`、`unsafe` 和 bindgen 分别起什么作用？

## A
**Rust 调用 C**：用 `extern "C"` 块声明 C 函数的签名，调用时必须放在 `unsafe` 里：
```rust
use std::ffi::{c_char, CString};
unsafe extern "C" { fn strlen(s: *const c_char) -> usize; }
let s = CString::new("hello, ffi").unwrap();
let n = unsafe { strlen(s.as_ptr()) };   // prints 10
```
输出：`10`。

- `extern "C"` 告诉编译器“按 C 的 ABI 调用”，这是 Rust 与 C 共同的约定，所以没有额外转接层，**调用本身和普通函数调用一样便宜**。
- `unsafe` 的含义：编译器无法检查 C 函数的契约（指针是否有效、是否越界、是否线程安全），所以由程序员承担责任。典型做法是在 `unsafe` 外面包一层**安全封装**，把不变量写清楚，调用者永远看到安全接口。
- `CString` 保证字符串以 `\0` 结尾且中间没有 `\0`；`&str`、`String` 不保证，所以要转换。

**bindgen**：读 C 头文件，自动生成 Rust 的 `extern "C"` 声明和结构体定义，避免手写签名出错。

**反方向（把 Rust 暴露给 C 及其他语言）**：在函数前写 `#[unsafe(no_mangle)] pub extern "C" fn ...`，以 C ABI 导出符号，编译成动态库（`crate-type = ["cdylib"]`），任何能调用 C 的语言都能调用它；`cbindgen` 可以生成 C 头文件。Python 的 PyO3、Node 的 napi-rs 等是更高层的绑定库，帮你自动完成类型转换。

Rust 做 FFI 的两个优势：没有运行时和 GC，不存在“GC 移动对象”或“进入 C 要切栈”的问题；所有权规则能表达“这块内存归谁”。代价是仍需 `unsafe`。
