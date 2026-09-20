---
id: patterns-visitor-tradeoff
node: patterns.behavioral
type: qa
step: 6
---
## Q
Visitor 让一件事变容易、另一件事变难，分别是哪两件？使用它之前类层次必须满足什么性质？

## A
Visitor 把扩展轴翻转了过来：

- **变容易：新增操作。** 在整个层次上加一个新操作（类型检查、格式化输出、在 AST 上求值）就是新加一个 visitor 类，完全不用碰元素类。
- **变难：新增元素类型。** 加一个新元素会迫使**每一个已有的 visitor** 都增加一个对应的 `visit` 方法——正好是"给每个子类加一个方法"的镜像问题。

前提条件：元素层次是**稳定的**，而操作集合还在不断增长（编译器、文档模型是典型场景）。如果新元素类型经常出现，Visitor 就是错误的取舍，应该用普通的多态方法。机制上值得点名：`element.accept(visitor)` 转发到 `visitor.visit(self)`，这叫双重分发（double dispatch）——根据两个对象各自的运行时类型共同决定调用哪个实现。
