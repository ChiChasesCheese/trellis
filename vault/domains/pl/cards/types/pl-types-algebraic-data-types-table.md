---
id: pl-types-algebraic-data-types-table
node: types.algebraic-data-types
type: qa
step: 3
---
## Q
Go、Java、Rust、Python 怎样表达和类型？各自换来什么，付出什么？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Go | 没有和类型；用接口加 type switch 模拟，类型集合是开放的 | 语言保持极简，任何包都能给接口加实现 | 编译器无法检查是否处理了所有类型，漏掉的类型静默落入 `default` |
| Java | `sealed interface` 加 `record`，`switch` 模式匹配（Java 21） | 封闭集合加穷尽检查，与现有类系统融合 | 语法比 Rust 啰嗦；变体是堆对象；老代码要迁移 |
| Rust | `enum` 是一等公民，`Option`、`Result` 都是普通的 `enum` | 非法状态不可表示，`match` 强制穷尽，变体内联存储无堆分配 | 学习成本；递归类型要 `Box` |
| Python | `dataclass` 加 `Union[A, B]`，`match` 语句 | 运行时灵活，检查器可以做穷尽检查 | 检查只在类型检查器里，运行时不强制 |

背后的逻辑：和类型要求语言把「集合封闭」当成核心特性。Rust 从 ML 家族继承了这条哲学，把它放在语言中心；Java 是在 JDK 17 到 21 之间用 `sealed`、`record`、模式匹配三步补齐；Go 的哲学是让语言小，不加这个特性，宁可接受漏处理的风险；Python 则把穷尽检查交给外部工具。越是关心「状态转换必须全覆盖」的领域（协议、状态机、编译器），越能感受到和类型的价值。
