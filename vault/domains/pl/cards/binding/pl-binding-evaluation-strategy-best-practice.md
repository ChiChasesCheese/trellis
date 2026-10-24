---
id: pl-binding-evaluation-strategy-best-practice
node: binding.evaluation-strategy
type: qa
step: 9
---
## Q
在严格求值的语言里，什么时候该主动引入惰性？C++、Go、Java、Rust、Python 的最佳实践分别是什么？

## A
判断标准：**参数或数据的构造成本高，而且常常用不上，或者数据量大到不应该一次装进内存。**满足其一就引入惰性，否则保持严格，简单即正确。

**引入惰性的典型场景**
1. 备选值昂贵：缺省值、日志消息、错误详情的构造。
2. 数据流很大或无限：文件逐行、分页查询、事件流。
3. 提前结束：只要第一个符合条件的，不需要遍历全部。

**各语言的做法**
- **Java**：取缺省值用 `orElseGet(() -> load())` 而不是 `orElse(load())`；大集合用 `Stream`，并且用 `limit`、`findFirst`，但小集合上不要为了「现代」强用流，普通循环更快更清楚。日志用 `Supplier` 版本（如 `java.util.logging` 的 `logger.fine(() -> expensive())`）或参数化消息。
- **Rust**：默认用迭代器链，不要中途 `collect()` 成临时 `Vec`；缺省值昂贵时用 `unwrap_or_else`、`ok_or_else`，常量或廉价值才用 `unwrap_or`。clippy 的 `or_fun_call` 会提醒。
- **Python**：大数据用生成器和 `itertools`，不要为了迭代先 `list(...)`；日志用 `logging.debug("v=%s", obj)` 而不是 f-string，这样日志级别关闭时不会格式化。
- **C++**：`optional::value_or(load())` 同样会先执行 `load()`，昂贵缺省值用 C++23 的 `or_else`（只在为空时才调用传入的函数）传一个 lambda；管道用 `std::views`（C++20 的惰性视图），不要中途物化成临时 `std::vector`。视图不拥有数据，别把指向局部容器的视图返回出去。
- **Go**：用 `for` 与 `iter.Seq` 在循环里直接处理，别先构造大切片；昂贵缺省值直接写 `if` 分支，只在需要的分支里调用。

**什么时候违反**
- 小数据、热路径：惰性意味着闭包和对象分配，普通循环更快。
- 需要多次遍历：生成器和 `Stream` 只能消费一次，要多次使用就物化成列表。
- 有副作用的步骤：惰性序列里的副作用执行时机依赖消费者，需要确定时序时先物化。

一条通用规则：惰性对象不要跨越模块边界传递，除非 API 文档明确它是一次性的，否则调用者会在资源（文件、连接）已经关闭后才开始消费。
