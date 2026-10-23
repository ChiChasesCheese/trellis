---
id: hl-j03-typeswitch-perf
node: java21.j03-pattern-switch
type: qa
step: 18
---
## Q
JDK 21 的 `typeSwitch` 是怎么逐个匹配标签的？这对分支很多的热路径意味着什么？

## A
JDK 21 的 `typeSwitch` **按顺序依次做 `isInstance` 检查**标签，不是哈希表。

- 几个分支毫无问题；
- 热路径上有几十个分支要**实测**；
- 这是实现细节，随版本改进，不要当规范依赖。

变体很多且在热路径时，可考虑每个 `record` 实现一个 `apply()` 虚方法，可能更快，也更符合开闭原则。
