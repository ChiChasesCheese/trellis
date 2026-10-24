---
id: pl-abstraction-pattern-matching-table
node: abstraction.pattern-matching
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 的模式匹配能力有什么区别？

## A
| 语言 | 机制 | 解构 | 穷尽检查 | 作为表达式 |
|---|---|---|---|---|
| Rust | `match`，语言核心 | 嵌套、守卫、绑定 | 强制 | 是 |
| Java（21） | `switch` + `sealed` + `record` | 嵌套的 record 模式 | 对 `sealed` 强制 | `switch` 表达式是 |
| Python（3.10） | `match` / `case` | 序列、映射、类 | 无（检查器可选） | 否（语句） |
| Go | type switch | 无 | 无 | 否 |

规律：模式匹配的力度与语言是否有**封闭的和类型**成正比。Rust 把和类型作为核心，匹配就成了语言的中心；Java 用 `sealed` 事后补上封闭性，匹配也随之获得穷尽检查；Python 动态、没有封闭类型，匹配只能是运行期解构；Go 刻意没有和类型，所以也不需要完整的模式匹配。

背后的哲学：Rust 来自 ML 家族，信奉「用类型表达所有可能的状态，让编译器检查」；Java 是向这个方向缓慢靠拢，以兼容为前提一步步加（2014 的 `Optional`，2021 的 `record`，2021 的 `sealed`，2023 的模式 `switch`）；Python 追求让常见的解析场景（命令、JSON、AST）写得简洁；Go 追求最少的语言特性，宁愿让开发者用接口和方法解决。
