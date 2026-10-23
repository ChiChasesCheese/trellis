---
id: hl-j06-flow-scoping
node: java21.j06-instanceof-pattern
type: qa
step: 4
---
## Q
`instanceof` 模式的绑定变量作用域规则叫什么？有什么一句话判断法？

## A
叫**流敏感作用域**（flow scoping）：绑定变量**只在编译器能证明"模式一定匹配了"的地方**可用。

不用死记，问一句：
> "走到这一行时，`o instanceof String s` 是不是**一定**为 `true`？"

一定 → `s` 可用；不一定 → 不可用（`cannot find symbol`）。这是 `instanceof` 模式最重要的概念，也是后面 `switch` 模式的基础。
