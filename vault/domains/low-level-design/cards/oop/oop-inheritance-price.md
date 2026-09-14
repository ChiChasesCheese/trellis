---
id: oop-inheritance-price
node: oop.pillars
type: qa
---
## Q
Inheritance buys polymorphism plus code reuse with one keyword. What price does it charge that composition doesn't?

## A
- **Strongest coupling available**: the subclass depends on base internals — base edits break children (fragile base class).
- **Fixed at compile time** and single-slot (one superclass); a composed collaborator is swappable at runtime and stackable.
- **Public is-a commitment**: every base contract now binds you (LSP), forever part of your API.

Hence: inherit for substitutable is-a, compose for reuse.

## Q zh
继承用一个关键字就买到了多态加代码复用。它收取了哪些组合不收的代价？

## A zh
- **可选方案里最强的耦合**：子类依赖基类内部 —— 改基类就会打断子类（fragile base class）。
- **编译期固定**且只有一个槽位（单继承）；而被组合进来的协作者可以在运行时替换、还能叠加。
- **公开的 is-a 承诺**：基类的每一条契约从此都约束你（LSP），并且永久成为你 API 的一部分。

所以：为可替换的 is-a 而继承，为复用而组合。
