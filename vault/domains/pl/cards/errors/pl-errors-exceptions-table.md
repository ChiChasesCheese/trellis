---
id: pl-errors-exceptions-table
node: errors.exceptions
type: qa
step: 6
---
## Q
Java、Python 的异常设计有什么不同，Go 与 Rust 为什么不采用异常？各自换来什么、付出什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Java | 异常，受检与非受检并存，`finally`，try-with-resources | 编译器强制处理 I/O 等外部失败；类型层次清晰 | 受检异常在大型系统里噪声大，与 lambda 不兼容，催生大量空 `catch` |
| Python | 异常，全部非受检，EAFP 风格，`else`/`finally`/`with`（离开块时自动清理） | 最短的代码；用异常做常规控制流是惯用法（迭代结束就是 `StopIteration`） | 任何调用都可能抛，签名里看不出，漏处理要到运行时 |
| Go | 不采用，用错误值；`panic` 仅给 bug | 无隐藏控制流，调用点即处理点 | 样板多 |
| Rust | 不采用，用 `Result`；`panic!` 仅给 bug | 类型强制处理，失败路径零栈追踪成本 | 需要设计错误类型 |

逻辑：异常押注的是「失败应当罕见且难以就地处理」，因此值得为它建立一套独立于正常路径的机制；Go 与 Rust 押注的是「失败是业务的一部分，应该和别的值一样显式」。Java 与 Python 的分歧在于强制性：Java 想让编译器保证外部失败被处理，Python 相信程序员和测试。

另一个角度是并发：异常沿着调用栈传播，但异步任务和线程的调用栈是分开的，异常需要显式地跨线程搬运（`Future.get()` 抛 `ExecutionException`、Python 的 `asyncio` 任务异常），这是异常模型在并发时代遇到的麻烦；错误值天然是普通数据，能走 channel 或 `Future`。
