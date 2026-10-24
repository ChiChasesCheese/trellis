---
id: pl-abstraction-operator-overloading-table
node: abstraction.operator-overloading
type: qa
step: 6
---
## Q
Go、Java、Rust、Python 对运算符重载的立场各是什么？

## A
| 语言 | 立场 | 买到 | 付出 |
|---|---|---|---|
| Go | 不支持 | `+` 的成本永远可预测 | 数值 / 向量代码冗长 |
| Java | 不支持（仅字符串 `+` 内置） | 同上，防止 C++ 式滥用 | `BigDecimal` 链式调用难读 |
| Rust | 通过 `std::ops` trait | 编译期解析，零成本，可用于泛型约束 | 需为引用重复实现，所有权易让人意外 |
| Python | dunder 方法 | 科学计算生态（NumPy、pandas）的基础 | 运行期查找，类型含糊时出现 `TypeError` |

规律：面向「通用服务端、大团队」的语言（Go、Java）选择可预测；面向「数值与领域建模」的语言（Python、Rust）选择表达力。

Go 的立场来自「读代码时不需要查定义就知道发生了什么」，Java 来自对 C++ 的反思。Rust 把运算符放在 trait 里，既有表达力，又保持一致：每个运算符都对应一个固定的 trait，行为被 trait 的契约限制，不能发明新的符号。Python 认为类型是协议的集合，运算符只是协议的一部分，鸭子类型的逻辑自然延伸到数学记号上。

一个共同点：没有哪种主流语言允许「发明新的运算符符号」（Haskell、Swift、Scala 是例外），因为那会让同一份代码在不同项目里读起来像不同的语言。
