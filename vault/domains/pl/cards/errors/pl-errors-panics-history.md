---
id: pl-errors-panics-history
node: errors.panics
type: qa
step: 9
---
## Q
「不可恢复错误」这个概念是怎么形成的，近年的趋势是什么？

## A
1. **断言与 `abort`（C，1970 年代）**：`assert` 条件不满足就终止进程，是最早的「快速失败」。
2. **Erlang（1980 年代，爱立信）**：为了做到电信系统的高可用，提出「让它崩溃」与监督树，把容错放在进程之外。
3. **Java（1995）**：用 `Error`/`RuntimeException` 层次区分严重和一般问题，但机制与普通异常相同。
4. **Go（2009）**：明确只给 `panic`/`recover` 一个狭窄的角色，主张错误用值；`recover` 主要给框架做边界保护。
5. **Rust（2015）**：把 panic 与 `Result` 分家，并允许选择展开或 abort，面向嵌入式与对体积敏感的场景。
6. **Swift**：`fatalError`、`precondition` 触发 trap，不可捕获，也不展开。
7. **近年**：云原生时代，「容器崩溃后由编排系统重启」成为通用的恢复策略，语言层的 panic 与基础设施层的重启形成了一条完整的链：快速失败，留下诊断信息，自动恢复。

趋势：
- **panic 越来越不可捕获**：Swift、Zig 的做法是直接终止，不提供 `recover`。Go 的 `recover` 被官方文档反复强调要谨慎使用。
- **崩溃时的诊断更重要**：栈追踪、core dump、结构化崩溃日志，以及 Rust 里 `RUST_BACKTRACE` 之类的开关，都是为了让「快速失败」能被分析。
- **隔离粒度变细**：线程级（Rust）、任务级（Rust 异步运行时 Tokio 的任务）、actor 级（Akka、Erlang）的隔离，让一个 bug 影响的范围尽量小。
