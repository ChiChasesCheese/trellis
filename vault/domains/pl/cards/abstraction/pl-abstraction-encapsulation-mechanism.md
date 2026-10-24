---
id: pl-abstraction-encapsulation-mechanism
node: abstraction.encapsulation
type: qa
step: 6
---
## Q
各语言的封装边界是在编译期、运行期还是约定层面被强制的？谁有办法绕过它？

## A
| 语言 | 强制发生在 | 谁能绕过 |
|---|---|---|
| Go | 编译器；`reflect` 也拒绝写未导出字段 | 只有 `unsafe`，显眼 |
| Java | 编译器 + JVM 的访问检查 | 反射 `setAccessible`（JDK 内部和未开放的模块除外） |
| Rust | 编译器，运行期无痕迹 | 只有 `unsafe` 代码里的原始指针 |
| Python | 无，只有命名约定与名字改写 | 任何代码，随时 |

结论是：**越靠编译器强制的语言，越能把封装当成安全边界**。Rust 的私有字段在编译后不存在于任何运行期结构里，没有反射可以去撬；Go 同理，反射对未导出字段是只读的。Java 的 `private` 在字节码层面也被检查，但反射提供了合法的后门（`setAccessible`），所以从 Java 9 起要靠模块系统补上第二道门，让 JDK 内部真正不可达。Python 把边界留给人。

一个细节：编译期强制意味着**零运行期开销**。Rust 和 Go 的私有检查在编译完成后消失；Java 的访问检查在符号解析时做一次（Java 11 起的 nestmate 机制让内嵌类互访也不再需要编译器合成的访问方法）。

这一差异有直接的工程含义：想依赖「外部代码绝不会改这个字段」时，在 Rust 和 Go 里可以放心，在 Java 里要考虑反射和序列化框架，在 Python 里只能依赖团队纪律和测试。
