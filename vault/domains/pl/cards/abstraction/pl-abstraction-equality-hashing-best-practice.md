---
id: pl-abstraction-equality-hashing-best-practice
node: abstraction.equality-hashing
type: qa
step: 9
---
## Q
资深工程师在各语言里怎样安全地定义相等与哈希？

## A
核心原则：**相等与哈希只依赖不可变的字段，并且两者用同一组字段**。

- **Java**：能用 `record` 就用 `record`（自动生成且一致）；手写时 `equals` 与 `hashCode` 一起改，用 `Objects.equals` / `Objects.hash`；作为 `HashMap` 键的类必须不可变。比较对象永远用 `equals`，不要用 `==`，装箱类型更要小心。`equals` 里用 `getClass()` 还是 `instanceof` 要想清楚继承场景（`record` 和 `final` 类没有这个问题）。
- **Rust**：优先 `#[derive(PartialEq, Eq, Hash)]`，让编译器保证三者一致；手写 `Hash` 时只哈希参与 `PartialEq` 的字段。浮点要排序或做键，明确选 `total_cmp` 或包装类型。
- **C++**：C++20 起用 `bool operator==(const T&) const = default;`（需要排序再加 `auto operator<=>(const T&) const = default;`），让编译器逐成员生成；放进 `unordered_map` 的类型自己特化 `std::hash`（标准库的哈希定制点），只哈希参与 `==` 的字段；不用 `double` 当键。
- **Go**：想当 map 键的类型，保证由可比较字段组成；需要自定义相等时，写成独立方法（`func (a T) Equal(b T) bool`），标准库的 `time.Time` 就这样（它推荐用 `Equal` 而不是 `==`，因为 `==` 还会比较时区信息和单调时钟）。
- **Python**：值对象用 `@dataclass(frozen=True)`，同时获得 `__eq__` 和 `__hash__`；不要给可变对象定义 `__hash__`；`__eq__` 里对不认识的类型返回 `NotImplemented` 而不是 `False`。

通用检查清单：这个对象会不会被放进集合 / 字典？放了之后字段还会变吗？相等是否对称、传递？浮点和 `NaN` 是否可能进入？

何时打破：身份语义的对象（连接、线程、有生命周期的实体）应该保持默认的同一性相等，不要重载成值相等；要按 ID 比较时，用显式的 `sameId()` 之类的名字，让读者知道比较的是什么。
