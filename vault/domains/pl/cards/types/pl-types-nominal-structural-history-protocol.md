---
id: pl-types-nominal-structural-history-protocol
node: types.nominal-structural
type: qa
step: 7
---
## Q
名义类型和结构类型的取舍在语言史上是怎样演变的？Python 为什么在 3.8 加了 `Protocol`？

## A
名义类型是 Simula、C++、Java 一路传下来的主流：类的关系写在声明里，工具容易分析，继承层级清晰。

结构类型在不同时代以不同形态出现：Smalltalk 和 Python 的鸭子类型是运行期的结构类型；ML 家族的模块系统用签名匹配做结构检查；Go（2009）把它带进了主流的静态类型语言，TypeScript（2012）也采用结构类型，并因此能给已有的 JavaScript 库补类型。

趋势是静态语言向结构靠拢，动态语言向静态检查靠拢：

- Python 3.8（2019）通过 PEP 544 加入 `typing.Protocol`。以前想让类型检查器接受「任何有 `read()` 的对象」，只能要求大家继承某个抽象基类（名义），而这对第三方类型不可能。`Protocol` 让你声明一个结构接口，`mypy` 按形状检查，运行时依旧是鸭子类型。
- C++20 的 concepts 用「满足这些表达式」来约束模板参数，是编译期的结构约束。
- Java 和 Rust 保持名义，但分别提供了补救：Java 的函数式接口让任何形状匹配的 lambda 自动成为实例，Rust 的 `impl` 可以独立于类型定义。

选哪种没有标准答案：名义换来清晰和显式意图，结构换来解耦和事后适配。
