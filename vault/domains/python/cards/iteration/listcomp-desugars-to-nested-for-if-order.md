---
id: listcomp-desugars-to-nested-for-if-order
node: iteration.comprehensions
type: qa
source: python-docs
---
## Q
列表推导式 `[(x, y) for x in A for y in B if x != y]` 等价于哪种嵌套 for/if 结构？多个 `for`/`if` 子句的先后顺序重要吗？

## A
等价于按书写顺序嵌套的 for 循环，每个 `if` 紧跟在它所在那层 `for` 之后过滤：`for x in A: for y in B: if x != y: 收集 (x, y)`。顺序完全重要——子句在推导式里出现的先后顺序，就是嵌套循环里 for/if 语句的先后顺序，调换顺序会改变语义或作用域可见性（内层子句用到的名字必须由外层的 for 先绑定）。
