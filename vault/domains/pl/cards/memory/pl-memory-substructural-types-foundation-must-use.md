---
id: pl-memory-substructural-types-foundation-must-use
node: memory.substructural-types
type: qa
step: 5
---
## Q
`#[must_use]` 在做什么？为什么说它是对线性类型（必须使用一次）的一个务实的近似，其他语言在这方面有什么？

## A
线性类型要求每个值**恰好用一次**，包括「不能被丢弃」。把这条规则用在整个语言上代价很大，Rust 选择了折中：仿射类型加上一个**可选的提醒**。给类型或函数标上 `#[must_use]`，如果调用者把返回值直接丢掉，编译器给出警告：

```rust
#[must_use = "a Guard must be released"]
struct Guard;
fn make() -> Guard { Guard }
fn parse() -> Result<i32, String> { Ok(1) }
fn main() {
    make();          // warning: unused `Guard` that must be used
    parse();         // warning: unused `Result` that must be used
    let _ = parse(); // explicitly ignored: silent
}
```

`Result` 本身就带 `#[must_use]`：被忽略时会提示 `this Result may be an Err variant, which should be handled`。这是 Rust 里「错误不能被悄悄吞掉」的一半保障（另一半是 `Result` 必须被显式解包）。迭代器适配器、`Future` 也带这个标记，因为只创建不消费等于什么都没做。

它**不是**线性类型：只是警告，可以用 `let _ =` 显式放过；对值的使用也只检查「返回值有没有被丢掉」，不检查资源最终有没有被关闭。

对比其他语言：

- **Go**：函数可以直接忽略返回的 `error`，编译器不管；靠 `errcheck`、`golangci-lint` 之类外部工具补。
- **Java**：有 `@CheckReturnValue`（Error Prone 等工具识别），不是语言规则；资源靠 `try-with-resources` 约定，编译器不强制你写。
- **Python**：忘记关闭文件，最多在开发模式下得到 `ResourceWarning`（`python -X dev`），而且是运行时、垃圾回收时才发现。

线性类型在这条谱系的最严格一端；`#[must_use]` 位于中间；其余语言的做法位于「靠约定」一端。

选择仿射加提醒而不是线性的原因：线性要求每个值显式消耗，错误路径和提前返回时都必须手工清理，没有 `Drop` 的自动清理就非常繁琐；Rust 优先让常见代码简短，用 `Drop` 处理清理，用 `must_use` 提醒容易遗漏的地方。
