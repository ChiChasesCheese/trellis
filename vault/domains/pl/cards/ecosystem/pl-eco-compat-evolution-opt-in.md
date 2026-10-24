---
id: pl-eco-compat-evolution-opt-in
node: ecosystem.compatibility
type: qa
step: 11
---
## Q
语言兼容策略这些年的总体趋势是什么？为什么“按单位选择加入”正在取代“全局断裂”？

## A
**回顾**：2008 年的 Python 3 代表了“全局断裂”的时代：所有人在同一天面对新规则，生态必须同步迁移，实际上花了十二年。之后各语言的共同结论是：断裂的成本随生态规模超线性增长，必须把破坏的范围缩小。

**趋势一：版本信息下沉到最小单位**。从“整个语言的版本”下沉到“这个模块”（Go 的 `go` 行）、“这个 crate”（Rust 的 edition）、“这个文件”（Python 的 `__future__`）、“这个类文件”（Java 的类文件版本）、“这个编译单元”（C++ 的 `-std=c++XX`）。粒度越小，新旧代码越容易共存。

**趋势二：工具化迁移**。Rust 的 `cargo fix --edition`、Go 的 `go fix` 和 `gofmt -r`、Python 的 `pyupgrade` 与 `ruff` 的升级规则、Java 的 OpenRewrite 配方。变更不只是发布说明，还附带自动改写代码的工具，让“破坏”成本落到机器上。

**趋势三：发布节奏化**。Go 每半年、Java 每半年（加每两年一个 LTS）、Python 每年、Rust 每六周、C++ 标准每三年，固定节奏让弃用、预览、移除有可预期的时间线，用户可以规划，而不是被突然的大版本打断。

**趋势四：预览与孵化**。Java 的 preview features、Rust 的 nightly feature gates、Go 的 `GOEXPERIMENT`，让新特性在稳定之前被真实代码试用，错误决定在稳定之前就修正，减少事后需要的断裂。

**趋势五：把兼容性变成可度量的东西**。`cargo-semver-checks`、`gorelease`、Java 的 `japicmp` 比较两个版本的公共 API，直接告诉你有没有破坏。

**展望**：未来的语言设计，会把“怎样演进”当作语言设计的一部分在第一天就设计好，而不是等到出现包袱。edition 与 `go` 行是这类设计的早期样本。
