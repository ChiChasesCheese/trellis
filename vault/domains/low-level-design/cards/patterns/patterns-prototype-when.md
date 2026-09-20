---
id: patterns-prototype-when
node: patterns.creational
type: qa
---
## Q
Prototype 是什么，它何时比 Factory 更好？

## A
**Prototype**：调用 `clone()` 而不是 `new`，避免重新初始化。对象充当自己的工厂。

何时比 Factory 更好：
- 你有一个**配置好的对象**，想创建许多类似的副本（数据库连接池中的样本连接）。
- 初始化**昂贵**（建立连接、加载大配置）。
- **类型未知** —— 运行时传递的对象可能是任何类的实例；`clone()` 起作用；Factory 需要知道所有子类。

陷阱：浅拷贝 vs 深拷贝。Prototype 通常需要深拷贝；容易被遗忘。
