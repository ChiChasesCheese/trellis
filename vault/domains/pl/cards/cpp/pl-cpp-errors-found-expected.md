---
id: pl-cpp-errors-found-expected
node: cpp.errors
type: qa
step: 6
---
## Q
C++23 的 `std::expected<T, E>` 是什么？怎样用它把一串可能失败的步骤串起来，与 Rust 的 `Result` 有什么差别？

## A
`std::expected<T, E>` 是一个**要么持有值 `T`、要么持有错误 `E`** 的类型（和类型，sum type）。函数返回它，就是把"可能失败"写进了返回类型；调用者必须看一眼才能拿到值。没有堆分配，成本等同于一个带标记的联合体。

**基本用法**：成功时 `return v;`，失败时 `return std::unexpected(错误值);`。检查用 `if (r)`，取值 `*r`，取错误 `r.error()`。

**单子式链接**（monadic operations，C++23）：`and_then`（成功则调用下一个可能失败的函数）、`transform`（成功则变换值）、`or_else`（失败则尝试恢复）。本机实测：

```cpp
auto r = parse(in).and_then(positive).transform([](int v) { return v * 2; });
```

输入 `"21"` 得 `42`，`""` 得 `error Empty`，`"x1"` 得 `error NotNumber`，`"-5"` 得 `error Negative`。出错的第一步之后，后续步骤不会执行，错误原样传到最后。

**与 Rust 的差别**：
1. **Rust 有 `?` 运算符**：`let v = parse(s)?;` 一个符号完成"出错就返回"。C++ 没有对应的语法，只能 `if (!r) return std::unexpected(r.error());` 或用 `and_then` 链；写起来更啰嗦。
2. **Rust 强制**使用 `Result`：不处理就报警告（`#[must_use]`）；C++ 的 `expected` 默认不强制，需要自己加 `[[nodiscard]]`（给函数或类型）。
3. **错误类型**：Rust 习惯用统一的 `Box<dyn Error>`；C++ 常用 `std::error_code`、枚举或自定义类型，没有统一约定。

**什么时候用**：预期会发生的失败（解析、查找、网络、校验），性能敏感、禁用异常的代码，需要把错误显式写进接口的库。

**不用的情形**：构造函数（没有返回值）、真正罕见的资源耗尽（用异常更省事）、程序员错误（用断言）。

**要记住的一点**：`expected` 让 C++ 终于有了和 Go、Rust 同类的"错误即返回值"机制，但没有 `?` 的语法糖，链式写法要靠 `and_then`。
