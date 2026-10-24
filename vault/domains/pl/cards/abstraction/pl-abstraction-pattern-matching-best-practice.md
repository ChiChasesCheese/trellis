---
id: pl-abstraction-pattern-matching-best-practice
node: abstraction.pattern-matching
type: qa
step: 9
---
## Q
使用模式匹配时，资深工程师最重要的一条纪律是什么？各语言里怎么落实？

## A
最重要的一条：**对封闭的类型，不要写通配符分支（`_` / `default`）**。穷尽检查是用来在以后加新变体时让编译器指出所有需要更新的地方；一个 `_ => ...` 会把这个能力关掉，新变体悄悄落入兜底分支，行为错误却没有任何提示。

- **Rust**：对自己拥有的 `enum` 把每个变体写全；对第三方库里标了 `#[non_exhaustive]` 的 enum，必须有通配符，这是它的设计目的。想要「新增变体时编译失败」又需要简洁时，可以对不关心的变体写成显式列表，而不是 `_`。
- **Java**：对 `sealed` 层级的 `switch` 不写 `default`；有了 `default`，新增子类型不会触发编译错误。把「可能新增」的类型用 `sealed` 声明，是在把演进成本显式化。
- **Python**：`match` 的 `case _` 应该写成 `assert_never(x)`（`typing` 模块，3.11 起），让类型检查器对联合类型和 `Enum` 做穷尽性检查；单纯 `case _: pass` 是无声的洞。
- **Go**：type switch 必须有 `default`，在其中返回错误或 panic，而不是静默返回零值；考虑用接口加方法替代。

其他实践：守卫不要写太复杂，复杂条件提到函数里命名；顺序敏感的分支（特例在前，通用在后），Java 编译器会拒绝「被前面分支完全覆盖的」分支，Rust 会警告 `unreachable pattern`。
