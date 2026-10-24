---
id: pl-conc-structured-table
node: concurrency.structured-concurrency
type: qa
step: 7
---
## Q
Python、Java、Go、Rust、C++ 各自怎样提供结构化并发？强制程度、取消传播和错误处理有什么差别？

## A
| 语言 | 机制 | 强制程度 | 取消与错误 |
|---|---|---|---|
| Python | 标准库 `asyncio.TaskGroup`（3.11） | 靠约定，裸 `create_task` 仍可用 | 自动取消兄弟，`ExceptionGroup` 聚合全部错误 |
| Java | `StructuredTaskScope`，JDK 25 仍是预览特性 | 结构由 API 保证（线程归属于作用域） | 策略可选（全成功 / 任一成功），失败自动取消 |
| Go | `errgroup`（`golang.org/x/sync`，非标准库） | 纯约定，`go` 语句不受限 | `context` 取消，只返回第一个错误 |
| Rust | `std::thread::scope`；async 用 tokio `JoinSet` | 编译器保证线程在作用域内结束 | 无内置取消；panic 会在作用域结束时传播 |
| C++ | `std::jthread`（C++20）：析构时自动 `join`；`std::stop_token` 协作取消；没有任务组类型 | 用对象生命周期（RAII，析构函数在离开作用域时运行）表达结构 | 不检查借用，线程可持有已销毁变量的引用；异常逃出线程直接终止进程，无聚合 |

背后的逻辑：
- 各语言**默认的原始工具都是无结构的**，结构化并发是后加的库。因此强制程度取决于语言能否在类型上表达“归属”：Rust 能（生命周期），Java 靠 API 设计，Python 和 Go 只能靠约定。
- 取消的实现取决于运行时模型：async 语言有现成的取消点（`await`），所以最自然；线程与 goroutine 只能靠中断标志或 `context` 协作。
- Go 把 `context` 做成显式参数，层层传递，代价是啰嗦，好处是取消路径肉眼可见；Python/Java 把取消藏进作用域，代码更短，但要理解它的隐式行为。
- C++ 用「作用域即生命周期」这个它最擅长的工具：`jthread` 把 `join` 写进析构函数，与 Rust 的 `scope` 殊途同归，但少了编译期的借用检查。零开销原则让标准只给最小的积木，任务组之类的高层结构留给库（C++26 的 `std::execution`，即发送者/接收者异步框架，在补这一层）。
- 错误的聚合策略反映哲学：Python 保留所有错误（`ExceptionGroup`），Go 只要第一个，因为“失败了就整体失败”足够。
