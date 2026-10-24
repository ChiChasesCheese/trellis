---
id: pl-functional-immutability-best-practice
node: functional.immutability
type: qa
step: 9
---
## Q
资深工程师在各语言里怎样在实践中落实不可变性？

## A
通用做法：**值对象、配置、消息、缓存键都做成不可变；可变状态收拢到少数明确的地方**。

- **Java**：值对象用 `record`；集合字段在构造时 `List.copyOf` 防御性复制，对外暴露的也是不可变集合；字段一律 `final`；多线程共享的数据优先设计成不可变，再考虑锁。注意 `record` 里的集合字段要自己复制成不可变副本（见陷阱）。
- **Go**：小结构体按值传递；对外暴露的数据，返回副本或只读视图；并发的共享数据遵循「创建后不再修改」，通过通道传递所有权；配置在启动时一次构造，之后只读。
- **Rust**：不用想，默认就是不可变；函数参数能用 `&T` 就不用 `&mut T`；返回新值而非修改参数，除非性能证明有必要；共享不可变数据用 `Arc<T>`，需要内部可变再用 `Mutex`。
- **Python**：值对象用 `@dataclass(frozen=True)` 加不可变字段类型（`tuple` 取代 `list`）；函数不要修改参数（尤其是默认参数）；模块级常量用 `tuple`、`frozenset`；类型注解里用 `Sequence`、`Mapping` 这样的只读抽象类型。

何时打破：热点路径上反复复制成本高时，使用局部的可变状态（构建时可变，构建完成后冻结，如 `StringBuilder` 到 `String`，Rust 的 `Vec` 到 `Box<[T]>`）。关键是可变性不要「泄漏」到边界之外。
