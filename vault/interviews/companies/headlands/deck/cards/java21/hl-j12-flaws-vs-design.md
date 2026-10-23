---
id: hl-j12-flaws-vs-design
node: java21.j12-scoped-values
type: qa
step: 23
---
## Q
列出 `ThreadLocal` 的三个结构性毛病，并说明 `ScopedValue` 各用什么设计消除它。

## A
| 毛病 | `ScopedValue` 的对策 |
|---|---|
| 生命周期失控，泄漏/串号 | 绑定寿命等于一次 `run/call` 的执行期，**返回即消失** |
| 不跨线程，或 `InheritableThreadLocal` 继承成本高 | 结构化并发 `fork` 时继承**不可变快照的引用**，只复制一个引用 |
| 可变，随处可改 | **没有 `set`**，改值只能用内层 `where` 遮蔽，从缩进就能看出范围 |
