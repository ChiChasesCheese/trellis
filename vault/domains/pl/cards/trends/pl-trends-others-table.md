---
id: pl-trends-others-table
node: trends.other-languages
type: qa
step: 8
---
## Q
这些“其他语言”的核心想法分别流向了 Go、Java、Rust、Python 的哪里？一张表怎样总结“谁借了谁”？

## A
| 想法（来源） | Go | Java | Rust | Python |
|---|---|---|---|---|
| RAII 与零开销（C++） | `defer` 近似手动版 | try-with-resources | `Drop` 与所有权，原样继承并强化 | `with` 语句与上下文管理器 |
| async/await（C#） | 未采用，选 goroutine | 未采用，选虚拟线程 | 采用，无运行时 | 3.5 引入 |
| 空安全（Kotlin、Swift、C#） | 无，nil 仍存在 | `Optional` 加注解式检查 | 无 null，`Option` | `Optional` 类型注解，检查器负责 |
| ADT 与模式匹配（ML 家族） | 未采用，接口加 type switch | `record`、`sealed`、模式 `switch` | `enum`、`match`，第一天就有 | `dataclass`、`match` |
| 类型类（Haskell） | 接口（结构化）近似 | 接口（名义）近似 | trait，几乎等价 | `Protocol` 近似 |

**规律**：
1. **Rust 是借得最多的**：它同时吸收了 C++（RAII、零开销）、ML 家族（ADT、trait）、C#（async），并加了自己的创新（借用检查）。这解释了为什么 Rust 的学习曲线陡：每个借来的想法都带着自己的概念。
2. **Go 是借得最少的**：刻意从 C 家族和 CSP（通信顺序进程）出发，拒绝大部分新想法，以保持语言小。
3. **Java 与 Python 是“晚期吸收者”**：Java 吸收 Kotlin/C#/ML 的想法，Python 吸收 TypeScript/C#/ML 的想法，都受向后兼容和动态特性的约束，形式有所变形。

**表中未列的两条**：TypeScript 的渐进类型对应 Python 的类型注解（注解、`mypy`、`pyright`），Go、Java、Rust 本来就是静态类型；Zig 与 C++ 的编译期执行对应 Rust 的 `const fn` 与过程宏，Go、Java、Python 没有对应物。

**提醒**：表格中“采用”不等于“同等保证”。Python 的类型注解不做运行时检查，Java 的 `Optional` 不能阻止 `null`，Go 的接口不是类型类。借来的想法在新环境里常被弱化。
