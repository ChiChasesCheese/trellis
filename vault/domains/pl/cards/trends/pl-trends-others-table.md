---
id: pl-trends-others-table
node: trends.other-languages
type: qa
step: 8
---
## Q
这些“其他语言”的核心想法分别流向了 Go、Java、Rust、Python、C++ 的哪里？一张表怎样总结“谁借了谁”？

## A
| 想法（来源） | Go | Java | Rust | Python | C++ |
|---|---|---|---|---|---|
| RAII 与零开销（C++） | `defer` 近似手动版 | try-with-resources | `Drop` 与所有权，原样继承并强化 | `with` 语句与上下文管理器 | 出处；析构函数加模板 |
| async/await（C#） | 未采用，选 goroutine | 未采用，选虚拟线程 | 采用，无运行时 | 3.5 引入 | C++20 协程（`co_await`），只给机制，无调度器 |
| 空安全（Kotlin、Swift、C#） | 无，nil 仍存在 | `Optional` 加注解式检查 | 无 null，`Option` | `Optional` 类型注解，检查器负责 | 无；引用不可为空，`std::optional` 是值，裸指针仍可空 |
| ADT 与模式匹配（ML 家族） | 未采用，接口加 type switch | `record`、`sealed`、模式 `switch` | `enum`、`match`，第一天就有 | `dataclass`、`match` | `std::variant` 加 `std::visit`（库），无语言级匹配 |
| 类型类（Haskell） | 接口（结构化）近似 | 接口（名义）近似 | trait，几乎等价 | `Protocol` 近似 | C++20 概念（concept），约束模板参数 |

**规律**：
1. **Rust 是借得最多的**：它同时吸收了 C++（RAII、零开销）、ML 家族（ADT、trait）、C#（async），并加了自己的创新（借用检查）。这解释了为什么 Rust 的学习曲线陡：每个借来的想法都带着自己的概念。
2. **Go 是借得最少的**：刻意从 C 家族和 CSP（通信顺序进程）出发，拒绝大部分新想法，以保持语言小。
3. **C++ 既是出借者也是借入者**：它是 RAII 和零开销的出处，却在 C++11 之后持续借入别人的想法（lambda、协程、`optional`/`variant`/`expected`、概念）。借入的方式很有特点：只补库和机制，不改旧语义，所以借来的特性往往比原产地弱（没有模式匹配，没有空安全）。
4. **Java 与 Python 是“晚期吸收者”**：Java 吸收 Kotlin/C#/ML 的想法，Python 吸收 TypeScript/C#/ML 的想法，都受向后兼容和动态特性的约束，形式有所变形。

**表中未列的两条**：TypeScript 的渐进类型对应 Python 的类型注解（注解、`mypy`、`pyright`），Go、Java、Rust 本来就是静态类型；Zig 与 C++ 的编译期执行对应 Rust 的 `const fn` 与过程宏，Go、Java、Python 没有对应物（C++ 自己有模板与 `constexpr`）。

**提醒**：表格中“采用”不等于“同等保证”。Python 的类型注解不做运行时检查，Java 的 `Optional` 不能阻止 `null`，Go 的接口不是类型类。借来的想法在新环境里常被弱化。
