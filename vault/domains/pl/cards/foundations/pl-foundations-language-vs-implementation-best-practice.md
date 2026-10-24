---
id: pl-foundations-language-vs-implementation-best-practice
node: foundations.language-vs-implementation
type: qa
step: 7
---
## Q
为了不被语言实现的细节绑架，资深工程师在工程上怎么做？每门语言怎样固定自己依赖的实现和版本？

## A
核心原则：只依赖规范承诺的行为，并把实现和版本当成需要显式管理的依赖。

1. 不依赖未承诺的行为。别靠 CPython 的引用计数来关文件，一律 `with open(...)`；别用 `is` 比较数值；别依赖 Go 的 map 遍历顺序；别假设 `HashMap` 的迭代顺序。这类代码在今天能跑，明天换实现或升级版本就会坏。
2. 在你实际运行的实现上测试。CI 里用和生产相同的实现与版本。语言一样、实现不同的行为差异（性能、GC 时机、线程语义）只会在真实环境里出现。
3. 钉住实现和版本。
   - Java：固定发行版和 LTS 版本（如 Temurin 21 或 25），不要写「任意 JDK」。
   - Go：`go.mod` 里的 `go` 指令和 `toolchain` 指令固定语言与工具链版本。
   - Rust：`rust-toolchain.toml` 固定工具链，库用 `rust-version` 声明最低支持版本。
   - Python：`.python-version` 或 `requires-python` 固定解释器，并写明是 CPython。
4. 为替代实现保持可移植，除非有收益。用 C 扩展就等于绑定 CPython；用 `Unsafe` 或 JVM 私有 API 就等于绑定特定 JDK。绑定要有理由，并且写进文档。

何时可以破例：性能需求很强、而且该实现的行为已经稳定多年（比如明确只跑在 CPython 并使用 NumPy），这时绑定实现是合理的交易，但要把它当作架构决策，而不是无意中的副作用。
