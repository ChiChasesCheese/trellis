---
id: pl-abstraction-bounds-variance-table
node: abstraction.bounds-variance
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 在约束的表达与型变的支持上有什么区别？

## A
| 语言 | 约束的写法 | 型变 | 代价 |
|---|---|---|---|
| Go | 接口 / 类型集合 | 无，全部不变 | 需要显式转换，如逐个复制到 `[]Animal` |
| Java | `T extends X & Y`，通配符 | 使用处，`? extends` / `? super` | 语法重，每个使用方都要重复写 |
| Rust | trait 约束 + `where` | 仅生命周期 | 类型间无子类型，一般不需要型变 |
| Python | `Bound`，`TypeVar` | 检查器自动推导（3.12） | 只在静态检查期生效 |

规律：语言越强调「类型之间有子类型关系」（Java、Python），越需要型变来协调泛型；越没有子类型（Go 的结构化接口 + 值类型、Rust 的 trait），越不需要。

Java 的使用处型变是为了在引入泛型时不改动已有类库；代价是通配符语法被公认难懂，API 签名里满是 `? super T`。C#、Kotlin、Scala 事后吸取教训，改成声明处，更好读。Rust 和 Go 因为从设计起就不依赖子类型，直接绕过了问题。Python 的类型系统晚到，借鉴了较新的设计，所以直接让检查器推导。

一个观察：「型变」是继承式子类型体系的产物，系统里没有继承时它几乎是多余的，这也是 Go 与 Rust 的泛型规则可以简单很多的原因。
