---
id: pl-errors-models-pitfall-ignored
node: errors.models
type: qa
step: 10
---
## Q
「忽略一个会失败的调用」在 C++、Go、Rust、Java、Python 里分别会发生什么？为什么这是各模型的核心差别？

## A
同一个失败的操作：把字符串 `"12x"` 转成整数。

```go
n, _ := strconv.Atoi("12x")   // error discarded
fmt.Println(n * 2)
```

Go 输出 `0`，既不报错也不警告，`go vet` 也没有意见。程序带着一个假值 `0` 继续运行，错误在远处以别的形式出现。

```rust
"12x".parse::<i32>();         // Result dropped
```

```console
warning: unused `Result` that must be used
  = note: this `Result` may be an `Err` variant, which should be handled
```

Rust 给出警告（`#[must_use]`），要想真正忽略，必须写 `let _ = ...` 或 `.ok()`，这是有意为之的痕迹，评审里可见。

C++ 取决于你用的机制：异常无法被忽略（未捕获会终止进程）；错误码和 `expected` 是否被忽略则要看函数有没有标 `[[nodiscard]]`，标了才有警告，没标就像 Go 一样静默：
```console
warning: ignoring return value of function declared with 'nodiscard' attribute [-Wunused-result]
```
这条是本机对一个返回 `std::expected`（C++23 的值型结果）的 `[[nodiscard]]` 函数的丢弃调用得到的警告；标准库的大多数错误码函数（如 C 的 `fclose`、`printf`）并没有标，丢弃返回值不会有任何提示。
Java 的受检异常是编译错误：

```console
error: unreported exception IOException; must be caught or declared to be thrown
```

Python 的异常无法被忽略，它会一路传播直到程序终止并打印栈追踪，所以「忘了处理」的后果是崩溃，而不是静默的错误数据。

这就是各模型的核心差别：**忘了处理错误时，系统以什么方式失败。** Go 是静默地继续（最危险，C++ 的未标 `[[nodiscard]]` 的错误码同理），Rust 是警告（有痕迹，C++ 的 `[[nodiscard]]` 同理），Java 受检异常是编译失败，Python 是大声崩溃。

对策：Go 里启用 `errcheck` 或 `golangci-lint` 的 `errcheck` 检查，把「未检查的错误」变成 CI 失败；不要用 `_` 吞错误，除非有明确理由并写注释；Rust 里生产代码避免 `unwrap`，用 `?` 或 `expect` 并写清不变量。
