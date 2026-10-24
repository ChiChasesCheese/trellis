---
id: pl-meta-annotations-mechanism
node: metaprogramming.annotations-decorators
type: qa
step: 6
---
## Q
Java 注解、Python 装饰器、Go struct tag、Rust 属性在底层各是什么？它们在什么时候起作用？

## A
- **Java 注解**：本质是一种特殊接口，随 `@Retention` 决定存活到哪一阶段：`SOURCE`（只在源码，如 `@Override`）、`CLASS`（写进 `.class` 但运行时不可见，**这是默认值**）、`RUNTIME`（运行时可由反射读到）。处理有两条路：编译期的注解处理器（Dagger、MapStruct 生成新源码），或运行期的反射加动态代理（Spring 的 `@Transactional` 在运行时给 bean 包一层代理对象）。
- **Python 装饰器**：`@d` 加 `def f` 等价于 `f = d(f)`，在模块导入、函数定义的那一刻执行一次，之后调用的是返回的对象。
- **Go struct tag**：就是紧跟字段后的一个字符串字面量，约定格式为 `key:"value"`；`reflect.StructTag.Get("json")` 在运行时按这个约定解析。编译器不检查内容。
- **Rust 属性**：`#[...]`。有些由编译器直接理解（`cfg`、`inline`、`test`），有些是过程宏（`derive`、`#[tokio::main]`），在编译期改写代码。

**时机总结**：Rust 全在编译期，Python 在定义（导入）时，Java 可选编译期或运行期，Go 的 tag 在运行期靠反射读取。时机决定了错误何时暴露、以及运行时要付多少反射成本。
