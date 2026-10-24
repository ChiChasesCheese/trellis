---
id: pl-functional-iterators-laziness-best-practice
node: functional.iterators-laziness
type: qa
step: 9
---
## Q
资深工程师在各语言里怎样使用迭代器和流水线？

## A
通用原则：**流水线适合表达「数据怎样变换」，但不要让副作用藏在惰性步骤里**。副作用的发生时机由终端操作决定，调试时会觉得顺序混乱。

- **Java**：Stream 用于变换，别在 `map`/`filter` 里改外部状态；不要为了「现代」把简单循环改成 Stream（可读性不一定更好，调试更难）；数值计算用 `IntStream`；`parallelStream()` 只在数据量大、每个元素的计算重、且流水线无副作用时才用，并且先测量。
- **Rust**：优先迭代器链，它不比手写循环慢；用 `collect::<Result<Vec<_>, _>>()` 把「中途失败就停止」的逻辑自然表达出来；避免不必要的 `collect()` 中间集合；返回迭代器时用 `impl Iterator<Item = T>`，避免暴露具体适配器类型。
- **Python**：大数据用生成器表达式和 `itertools`，不要先构造 `list`；只遍历一次的用生成器，需要多次遍历就用 `list` 或 `tuple`；写 API 时参数类型用 `Iterable[T]`，调用方传什么都行。
- **Go**：新代码里需要暴露集合遍历时，提供返回 `iter.Seq` 的方法；使用 `iter.Pull` 后一定调用 `stop`；标准库的 `slices`、`maps` 包已经提供 `Collect`、`Sorted` 等工具。

何时打破：对性能极度敏感的内层循环，在非 Rust 语言里手写循环通常比流水线快（少了抽象开销），但要先用剖析数据确认。
