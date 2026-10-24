---
id: pl-abstraction-typeclasses-best-practice
node: abstraction.typeclasses
type: qa
step: 10
---
## Q
在有类型类（Rust）和没有类型类（Go、Java、Python）的语言里，资深工程师怎样设计「按能力抽象」的接口？

## A
共同原则：**让抽象描述调用方需要的最小能力，而不是实现者是谁。**

**Rust**
- 先问：这个行为是类型本身的性质（用 trait），还是调用时才确定的策略（传闭包或 enum）？排序规则、哈希方式这类每个类型天然只有一种合理答案的，用 trait；每个调用点可能不同的（比较函数、过滤条件），传闭包。
- trait 保持小而专注（`Read`、`Display` 的粒度），大 trait 难以实现，也难以加 blanket impl。
- 泛型参数用于性能关键路径，`dyn Trait` 用于异构集合和边界；公共 API 里谨慎暴露 `impl Trait` 以外的复杂约束。
- 给外部类型加行为，用 newtype 或扩展 trait（`trait OptionExt`），并为它起不会与标准库冲突的方法名。

**C++**
- 给外部类型加行为，用自由函数重载（放在该类型所在的命名空间，让 ADL 找到），或特化标准库的定制点（`std::hash<T>`、`std::formatter<T>`）；不要往 `std` 命名空间里加别的东西（未定义行为，除非标准明确允许特化）。同一个类型的特化只在一个头文件里写一份，避免违反单一定义规则。
**Go**
- 接口由使用方定义，越小越好（1 到 3 个方法）；返回具体类型，接收接口。
- 需要对标准类型加方法时，定义自己的类型（`type Celsius float64`）；需要策略时传函数值或 `cmp` 函数，如 `slices.SortFunc`。

**Java**
- 为外部类型提供行为，用函数式接口加策略对象；`Comparator`、`Function` 比引入包装类轻。
- 想让泛型方法有能力约束，用有界类型参数 `<T extends Comparable<? super T>>`；记得 `Comparable` 与 `equals` 的一致性。

**Python**
- 用 `Protocol` 描述需要的能力，类不需要继承；跨库的事后扩展用 `singledispatch`，不要猴子补丁别人的类。
- 登记要集中在一个明确的模块，避免导入顺序影响行为。

通用判断：如果你发现自己在写 `instanceof` / `switch x.(type)` / `isinstance` 的长链，说明缺的是一个能力抽象，把它提成接口、trait 或分派表。

什么时候违反：只有两三个固定类型、且不会增加时，直接 `match` 或 `switch` 比抽象更清楚。
