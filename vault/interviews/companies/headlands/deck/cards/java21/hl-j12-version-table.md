---
id: hl-j12-version-table
node: java21.j12-scoped-values
type: qa
step: 17
---
## Q
`ScopedValue` 在 JDK 20 到 25 各版本发生了什么？面试要能说清哪些变化？

## A
| 版本 | 状态 / 变化 |
|---|---|
| JDK 20 | 孵化（incubator） |
| **JDK 21** | 第一次预览；有 `runWhere/callWhere/getWhere` 和 `Carrier.run/call/get(Supplier)` |
| JDK 22、23 | 继续预览，小改 |
| JDK 24 | 第四次预览：`callWhere` 与 `runWhere` 被移除，使用已绑定值的唯一方式是 `Carrier.call` / `run` |
| **JDK 25** | **转正（final）**：`orElse` 不再接受 `null` 参数 |

`Carrier.get(Supplier)` 在后续版本的去向未核对，新代码别依赖它。
