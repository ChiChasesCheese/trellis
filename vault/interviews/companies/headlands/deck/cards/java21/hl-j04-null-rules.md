---
id: hl-j04-null-rules
node: java21.j04-record-patterns
type: qa
step: 9
---
## Q
record 模式遇到 `null` 有哪三条规则？

## A
1. **外层 record 本身为 `null`**：不匹配任何 record 模式；没有 `case null` 就抛 NPE。
2. **某组件值为 `null`，且对应子模式是无条件的**（类型模式的类型正是组件声明类型或其父类型，或 `var`）：**匹配成功，绑定变量为 `null`**。
3. **子模式不是无条件的**（组件是 `Object`，子模式写 `String s`）：`null` 不是 `String`，**匹配失败**，继续试下一分支。
