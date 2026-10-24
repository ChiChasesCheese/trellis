---
id: pl-eng-apidesign-table
node: engineering.api-design
type: qa
step: 7
---
## Q
同一个“带超时和重试的客户端”库，在 Go、Java、Rust、Python 里各自的地道设计是什么样？可选配置、错误、所有权、取消分别怎么表达？

## A
| 语言 | 可选配置 | 错误 | 所有权/可变性 | 取消/上下文 |
|---|---|---|---|---|
| Go | 配置结构体，或函数式选项 `NewClient(addr, WithTimeout(...))` | 最后一个返回值 `error`，用 `%w` 包装并保留原因，调用者用 `errors.Is/As` 判断 | 靠约定：返回切片可能共享底层数组；文档说明谁可以改 | 第一个参数 `ctx context.Context`，显式传递 |
| Java | 构建器 `Client.builder().timeout(...).build()`，对象不可变 | 受检异常表示可恢复的情形，非受检异常表示编程错误；自定义异常层次 | 返回不可变视图或副本；`final`、`record` | 线程中断、`Future.cancel`、`ScopedValue`；超时在客户端上设置 |
| Rust | 构建器（方法消耗并返回 `self`），或结构体更新语法 | `Result<T, MyError>`，错误枚举实现 `std::error::Error`，用 `From` 与 `?` 转换 | 签名写明 `&self`/`&mut self`/`self`，参数用借用或 `impl Into` | 丢弃 `Future` 即取消；`tokio::time::timeout` 包裹 |
| Python | 关键字参数与默认值，布尔标志用仅限关键字 | 自定义异常层次，继承一个库根异常 | 靠约定；不可变用 `tuple`、`frozenset`、`dataclass(frozen=True)` | `asyncio.timeout()`、`contextvars`；同步代码用 `timeout=` 参数 |

**这背后的逻辑**：
- **Go** 的设计把一切放到表面：错误是返回值，上下文是参数，配置是显式的选项函数。可见性胜过简洁。
- **Java** 靠类型和不可变对象建立信任：对象一旦构造就合法，错误通过异常层次分类，构建器弥补没有命名参数的缺失。
- **Rust** 把合同写进类型：所有权、错误、可变性都在签名里，编译器代为核对。代价是签名最复杂。
- **Python** 信任调用者并优先书写效率：默认值和关键字参数让 API 最短，约束靠文档与类型提示（可选）。

规律：**一门语言能在编译期表达的约束越多，API 越依赖签名；能表达的越少，API 越依赖约定和文档**。
