---
id: pl-meta-codegen-evolution-absorbed
node: metaprogramming.code-generation
type: qa
step: 11
---
## Q
为什么代码生成的常见用例正在被语言本身吸收？Java 的 `record`、Python 的 `dataclass`、Go 的泛型各自替掉了哪些生成器？

## A
**规律**：一类样板只要足够常见，语言迟早把它做成内建特性。这样不再需要「生成器 + 产物 + 同步」这套机制，样板在语言里有一个标准名字。

- **Java**：getter、`equals`、`hashCode`、`toString` 曾经靠 IDE 生成、Lombok 或 AutoValue。`record`（Java 16 正式）把「只携带数据的类」做成语法，一行声明得到全部。`sealed` 与 switch 模式匹配也替掉了访问者模式的生成代码。
- **Python**：`dataclass`（Python 3.7，PEP 557）把 `__init__`、`__repr__`、`__eq__` 的手写样板变成装饰器，之前要靠 `attrs` 库或元类。
- **Go**：泛型（Go 1.18）取代了大量「为每种类型复制一份」的生成器，如各种类型特化的容器与排序。`go:embed` 取代了把静态文件生成成 Go 字节数组的工具。
- **Rust**：`derive` 本身就是被吸收的结果，使「生成」变成一行属性。

**仍然留在生成器手里的**：跨语言的 schema（protobuf、OpenAPI、GraphQL）、数据库查询（sqlc）、Mock、FFI 绑定（bindgen）。它们的共同点是事实来源在语言之外，语言无法内建。

**趋势**：语言内建吸收通用样板；生成器退守到「语言之外的 schema」。判断一个生成器是否长寿，就看它的输入是不是语言本身能表达的东西。
