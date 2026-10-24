---
id: pl-conc-parallel-table
node: concurrency.parallelism
type: qa
step: 7
---
## Q
Java、Rust、Go、Python、C++ 对数据并行提供了怎样的支持？各自的取舍是什么？

## A
| 语言 | 方式 | 换来 | 代价 |
|---|---|---|---|
| Java | 标准库 `parallelStream()`、`ForkJoinPool` | 一个词 `.parallel()` 就能并行；标准库自带 | 公共池共享、阻塞操作会拖累全局；编译器不检查副作用 |
| Rust | 第三方 rayon：`iter()` 改成 `par_iter()` | 几乎同样简单，且编译器保证闭包无数据竞争 | 要引入依赖；闭包必须 `Send`/`Sync` |
| Go | 标准库没有并行 map；手工分片 + `WaitGroup`/`errgroup` | 完全可控，无魔法 | 样板代码多，分片和负载均衡要自己写 |
| Python | `multiprocessing`、`concurrent.futures`；NumPy/Polars 等释放 GIL 的库 | 把热点交给 C/Rust 内核，Python 只做编排 | 进程要序列化；纯 Python 循环无法并行 |
| C++ | C++17 并行算法：`std::for_each(std::execution::par, …)`（执行策略，execution policy）；OpenMP 等指令或 TBB 库是另一条路 | 改一个参数就并行，同一套算法；可选向量化的 `par_unseq` | 完全不检查副作用：闭包里写共享变量就是数据竞争；各标准库实现的支持不齐（本机 libc++ 需 `-fexperimental-library`） |

背后的逻辑：
- Java 的目标是**让并行像迭代一样容易**，所以把 `.parallel()` 放进标准库，选择了便利，代价是它能被滥用（共享可变累加器、阻塞调用）。
- Rust 同样追求易用，但把“安全”作为前提：并行迭代器是库，规则靠类型系统守住。
- Go 的哲学是显式、简单：不提供隐藏的并行，让你自己写 goroutine，换来可预测性。便利封装交给社区库。
- Python 的并行发生在语言**之外**：由底层的 C/Rust 库完成。Python 的角色是“把大块数据交给高效内核”，这也是它在科学计算领域成功的原因。
- C++ 与 Java 的 `.parallel()` 最像（一个参数换来并行），但没有 Java 的运行期兜底，也没有 Rust 的类型约束：并行体里的数据竞争是未定义行为。这符合 C++ 的两条原则：零开销（抽象不比手写慢）和手动控制（正确性由程序员负责）。
