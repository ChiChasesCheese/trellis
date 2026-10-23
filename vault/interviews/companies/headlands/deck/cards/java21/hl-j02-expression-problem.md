---
id: hl-j02-expression-problem
node: java21.j02-sealed
type: qa
step: 17
---
## Q
什么是表达式问题（expression problem）？`sealed` + `switch` 在其中偏向哪一边，适合什么场景、不适合什么场景？

## A
- **开放继承**：加子类容易，但加一个对所有子类的操作要改全部子类。
- **`sealed` + `switch`**：加操作容易（再写一个 `switch`），加变体要改所有 `switch`——但编译器会**列出**所有要改处。

所以 `sealed` 适合"**变体少变、操作常加**"：协议消息、命令、事件、AST。变体常由别人扩展（插件、驱动）就该用开放接口。
