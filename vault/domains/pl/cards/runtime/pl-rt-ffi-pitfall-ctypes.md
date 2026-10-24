---
id: pl-rt-ffi-pitfall-ctypes
node: runtime.ffi
type: qa
step: 10
---
## Q
Python `ctypes` 调用 C 函数时，不声明参数类型会发生什么？
请用 `strlen` 说明，并列出 FFI 里其他典型的“静默出错”陷阱。

## A
`ctypes` 在运行时按你传入的 Python 对象猜测怎么转成 C 参数，没有声明 `argtypes` 时，它不知道函数想要什么。
```python
libc = ctypes.CDLL(None)
libc.strlen.argtypes = [ctypes.c_char_p]
libc.strlen.restype = ctypes.c_size_t
print(libc.strlen(b"hello, ffi"))   # 10: declared, bytes passed

libc.strlen.argtypes = None
print(libc.strlen("hello"))          # no declaration, a str is passed
```
输出：`10` 与 `1`。第二次传的是 Python 的 `str`，被转成宽字符串（`wchar_t*`，每个字符 4 字节），`strlen` 按字节数，第一个字符 `h` 后面紧跟 `\0` 字节，所以得到 1，没有任何异常。返回类型默认是 `int`，如果函数返回 64 位指针或 `size_t`，会被截断。

这类问题的共同特征：**边界处丢失了类型信息，错误不报警，结果似是而非。** 其他典型陷阱：
1. **字符串编码与终止符**：C 字符串以 `\0` 结尾；Go 的 `CString` 要手动 `free`；Rust 的 `CString::new` 遇到内部 `\0` 会返回错误；UTF-8 与 UTF-16/本地编码混淆导致乱码。
2. **结构体布局**：C 编译器可能插入填充字节，字段顺序/对齐必须与 `#[repr(C)]`、`ctypes.Structure`、Java `MemoryLayout` 完全一致，否则读出垃圾值。
3. **悬空指针**：把指向 GC 管理内存的指针交给 C 保存，GC 移动或回收后指针失效。Go 有明确的“cgo 指针传递规则”，运行时检查违规并 panic；Java 要用 `Arena` 或 pinned 内存；Python 的临时对象在调用返回后可能被释放，而 C 还持有指针。
4. **长度与整数类型**：`int`、`long`、`size_t` 在不同平台宽度不同（Windows 的 `long` 是 32 位），声明错会截断。
5. **释放不匹配**：用 `free` 释放 Rust 分配的内存，或用 Rust 的 `Box::from_raw` 重建 C 分配的指针，都是未定义行为。

对策：声明完整的类型；使用生成工具（bindgen、cbindgen、`jextract`）而不是手写；用 ASan 跑测试。
