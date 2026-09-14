---
id: patterns-visitor-tradeoff
node: patterns.behavioral
type: qa
---
## Q
Visitor makes one thing easy and one thing hard. Which, and what property of the class hierarchy must hold before you use it?

## A
Visitor flips the extension axis:

- **Easy: adding operations.** A new operation over the hierarchy (type-check, pretty-print, evaluate over an AST) is one new visitor class — no touching the element classes.
- **Hard: adding element types.** A new element forces a new `visit` method on **every existing visitor** — it's the exact mirror of adding a method to every subclass.

Precondition: the element hierarchy is **stable** and the set of operations keeps growing (compilers, document models). If new element types arrive often, visitor is the wrong trade — use plain polymorphic methods. Mechanism worth naming: `element.accept(visitor)` → `visitor.visit(this)` is **double dispatch**, selecting behavior on both runtime types.

## Q zh
Visitor 让一件事变容易、另一件事变难。分别是哪两件，使用它之前类层次必须满足什么性质？

## A zh
Visitor 把扩展轴翻转了过来：

- **变容易：新增操作。** 在整个层次上加一个新操作（类型检查、格式化输出、在 AST 上求值）就是一个新的 visitor 类 —— 完全不用碰元素类。
- **变难：新增元素类型。** 加一个新元素会迫使**每一个已有的 visitor** 都增加一个 `visit` 方法 —— 这正是"给每个子类加一个方法"的镜像。

前提条件：元素层次是**稳定的**，而操作集合还在不断增长（编译器、文档模型）。如果新元素类型经常出现，visitor 就是错误的取舍 —— 用普通的多态方法。值得点名的机制：`element.accept(visitor)` → `visitor.visit(this)` 是 **double dispatch**，根据两个运行时类型共同选择行为。
