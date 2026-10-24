---
id: pl-trends-others-best-practice
node: trends.other-languages
type: qa
step: 10
---
## Q
资深工程师怎样从其他语言里学习，并把它用在日常的 Go、Java、Rust、Python 工作中？

## A
**通用规则**：
1. **学想法，不学语法**：问“这门语言在回答什么问题”，再看它在你的语言里是否有对应物。
2. **每隔一两年用一门风格不同的语言写一个小项目**：函数式（OCaml、Haskell）、系统（Zig、Rust）、渐进类型（TypeScript）。目的是改变你设计数据结构的方式，而不是换工作语言。
3. **把借来的想法翻译成当前语言的惯用法**，不要硬搬。
4. **阅读语言的设计文档**（Go 的设计草案、Rust 的 RFC、Java 的 JEP、Python 的 PEP）：里面写明了问题、备选方案与取舍，是最好的“为什么”来源。

按语言的具体迁移：
- **在 Go 里**：学 ML 的“让非法状态不可表示”：用自定义类型、小接口、构造函数校验；学 Zig 的“显式”：把分配与错误显式传递。
- **在 Java 里**：学 Kotlin/ML：用 `record` 加 `sealed` 建模，不写 `default`；学 Swift/Kotlin：用 `Optional` 和注解约定空值，不返回 `null`。
- **在 Rust 里**：学 C++ 的 RAII 和 Zig 的分配器意识：设计 API 时让分配与生命周期可见。
- **在 Python 里**：学 TypeScript：渐进加类型，从公共 API 与边界数据开始；学 ML：用 `dataclass(frozen=True)` 与 `match` 建模，用 `Literal` 和联合类型表达状态。

**何时不要学**：团队约定与生态已经选定风格时，不要在局部引入另一种范式；一个仓库里风格一致比局部最优更重要。

**判断一个“新想法”的价值**：它是否消除一类 bug、减少一类样板、或者让某个约束变得可见？三者都不是的，多半是语法糖。
