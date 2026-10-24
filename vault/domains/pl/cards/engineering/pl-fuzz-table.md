---
id: pl-fuzz-table
node: engineering.fuzzing
type: qa
step: 6
---
## Q
Go、Java、Rust、Python 的模糊测试各有什么特点？它们分别最擅长找哪一类 bug？

## A
| 语言 | 工具 | 「崩溃」的含义 | 最擅长找什么 |
|---|---|---|---|
| Go | 标准库 `testing.F`，`go test -fuzz` | panic、`fatal error`、超时 | 解析与解码里的越界、空指针、死循环；无需额外安装 |
| Java | Jazzer（基于 libFuzzer，字节码插桩），可接入 JUnit 5 | 未捕获异常、内置检测器触发的漏洞 | 反序列化、注入、递归与资源耗尽等逻辑和安全问题 |
| Rust | `cargo-fuzz`（libFuzzer），也有 AFL | panic、abort；配合 ASan 看 `unsafe` 的内存错误 | `unsafe` 与 C 依赖里的内存破坏；安全代码里的 panic 和溢出 |
| Python | Atheris（基于 libFuzzer，字节码插桩） | 未处理异常、超时 | 纯 Python 解析逻辑里的异常；与 ASan 一起测 C 扩展 |

**规律**：语言的内存安全程度决定了 fuzz 能找到什么。在 C 和 C++ 里，fuzz 的主要战果是内存破坏（越界读写、释放后使用），所以和 ASan 是一套组合；在 Go、Java、Python 这些内存安全的语言里，战果主要是 panic、异常和拒绝服务，也就是「该拒绝却没拒绝」「该快却很慢」；Rust 介于其中：安全代码里是 panic，`unsafe` 里则仍可能是内存破坏。

哲学上，Go 把 fuzz 做进标准库，和测试、基准同一套工具，让「写 fuzz 目标」变成与写单元测试一样的日常动作；Rust 和 Java 依赖 LLVM 或 libFuzzer 生态，工具链复杂度更高，但能力更强（结构感知、检测器）。
