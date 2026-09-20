---
id: principles-stack-extends-arraylist
node: principles.composition
type: qa
---
## Q
为什么 Stack 扩展 ArrayList 是一个设计错误？

## A
因为 Stack 是一个 LIFO（后进先出）数据结构，但 ArrayList 是一个 indexed、可随机访问的列表。

如果 Stack 扩展 ArrayList：
- 调用者可以调用 `get(0)`、`add(0, item)` 或 `remove(5)`
- 这违反了 Liskov 替换原则：Stack 的调用者期望 LIFO 行为，但可以进行不尊重 LIFO 的操作
- Stack 继承了所有不相关的方法：`indexOf`、`replaceAll` 等。

正确的设计：Stack 组合 ArrayList 或 LinkedList，只暴露 push、pop、peek 方法。这是组合而不是继承。
