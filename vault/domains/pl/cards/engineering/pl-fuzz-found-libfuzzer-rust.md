---
id: pl-fuzz-found-libfuzzer-rust
node: engineering.fuzzing
type: qa
step: 4
---
## Q
Rust 的 `cargo-fuzz` 和 libFuzzer 是什么关系？fuzz 目标怎么写，它擅长发现什么？

## A
**libFuzzer** 是 LLVM 自带的**进程内**覆盖率引导模糊器：被测函数与模糊器链接在同一个进程里，被反复调用，没有每次启动进程的开销，所以很快。Rust 的后端是 LLVM，可以直接使用同样的覆盖率插桩。`cargo-fuzz` 是封装它的 Cargo 子命令：`cargo fuzz init` 创建目录，`cargo fuzz run <目标>` 运行。它需要 nightly 工具链，因为用到了不稳定的编译器选项。

**fuzz 目标**写成 `fuzz_target!` 宏：

```rust
fuzz_target!(|data: &[u8]| {
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = fr::parse(s);   // splits "<len>:<payload>"
    }
});
```

被测的 `parse` 按 `"<长度>:<内容>"` 切分字符串，直接用 `&s[i + 1..i + 1 + n]` 取内容，没检查冒号是否存在、长度是否越界。不到一秒，输出：

```text
panicked at src/lib.rs:5:7:
start byte index 1 is out of bounds for string of length 0
SUMMARY: libFuzzer: deadly signal
```

触发的是空输入，崩溃文件保存在 `fuzz/artifacts/` 下，`cargo fuzz tmin` 可以进一步缩小。

**Rust 的特点**：
- 安全代码里的 bug 表现为 **panic**（越界下标、`unwrap` 失败、除零；调试构建里整数溢出也会 panic），这些都是崩溃信号，可以直接被发现；
- `unsafe` 代码和 C 依赖里的内存错误本身不会崩溃，需要配合 AddressSanitizer 才变得可见，`cargo-fuzz` 默认开启它；
- 用 `arbitrary` crate 可以把字节流解码成自定义的结构体或枚举，fuzz 目标就能直接接收结构化输入，越过格式层去测逻辑。
