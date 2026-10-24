---
id: pl-meta-reflection-best-practice
node: metaprogramming.reflection
type: qa
step: 9
---
## Q
资深工程师在 Java、Go、Python、Rust 里怎样使用反射？通用规则是什么，何时可以破例？

## A
**通用规则**：反射只放在框架边界，在启动时做一次，把结果缓存成普通数据结构，热路径上只走缓存。理由是反射的代价（查表、丢失内联、运行时才暴露的错误）和它的收益（通用性）都集中在「发现类型」这一步，应该只付一次。

- **Java**：启动时反射扫描，把结果存成 `MethodHandle`（存进 `static final` 字段时 JIT 能把它当常量内联）或直接生成字节码；能用编译期注解处理器解决的（Dagger、MapStruct）优先用，它们没有运行时反射，对 GraalVM 原生镜像也友好。
- **Go**：先问能不能用接口或泛型。必须用时，按 `reflect.Type` 缓存字段偏移量，不要每次 `FieldByName`；写测试覆盖每条 panic 路径。
- **Python**：`getattr` 要给默认值或捕获 `AttributeError`，不要拿 `eval` 当反射用；公共库里优先用 `typing`/`dataclasses.fields()` 这类有结构的 API，而不是翻 `__dict__`。
- **Rust**：不要为模仿反射而滥用 `Any`；用 trait 加 `derive`，需要运行时多态用 `dyn Trait`。
- **C++**：不要为了“反射”打开 RTTI 到处 `dynamic_cast`，用虚函数或 `std::variant`；需要序列化时，现有项目用成熟的库（如 nlohmann/json 的宏、Boost.Describe）或外部生成器，新项目等 C++26 静态反射在目标编译器上可用后再迁移。

**何时破例**：写一次性脚本、测试工具、调试器、通用序列化库，反射本来就是正确的工具。规则针对的是业务逻辑里「图方便」的反射：它把本该在编译期发现的错误推迟到了凌晨三点的线上。
