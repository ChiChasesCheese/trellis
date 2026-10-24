---
id: pl-errors-panics-table
node: errors.panics
type: qa
step: 5
---
## Q
Go、Java、Rust、Python 各自如何表示和处理「不可恢复」的错误？取舍是什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Go | `panic` 加 `defer`/`recover`，未捕获则终止整个进程 | 机制简单；框架可在边界 `recover` 保护服务 | 一个 goroutine 的 panic 会拖垮整个进程；`recover` 容易被滥用成异常 |
| Java | 异常体系里的 `Error` 与 `RuntimeException`，没有独立的 panic | 统一机制，可在任意层捕获 | 区分靠约定（不要捕获 `Error`），容易 `catch (Throwable)` 吞掉严重问题 |
| Rust | `panic!` 默认展开，可配置为 abort，按线程终止 | 清理有保证；`abort` 模式更小更快 | 展开增加二进制体积；跨 FFI 边界展开是未定义行为 |
| Python | `BaseException` 与 `Exception` 两层 | `SystemExit` 等不被 `except Exception` 拦截 | 裸 `except` 会拦住一切，包括 `Ctrl+C` |

逻辑：这四种选择体现了对「crash 的粒度」的态度。Go 与 Rust 都认为 panic 是 bug，不是错误处理的一部分，区别在于终止的范围：Rust 默认终止线程，Go 终止进程（任何 goroutine 里没处理的 panic 都会让整个程序退出）；Java 与 Python 更宽松，把严重问题放进同一套异常机制，用类层次区分，靠约定遵守。

选型含义：对长期运行的服务，Go 的「一个 panic 拖垮整个进程」要求你在每个 goroutine 的入口处加 `recover` 保护；Rust 的线程隔离让你可以用线程池隔离风险。
