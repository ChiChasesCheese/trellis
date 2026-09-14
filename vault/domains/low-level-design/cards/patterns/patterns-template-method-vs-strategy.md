---
id: patterns-template-method-vs-strategy
node: patterns.behavioral
type: qa
---
## Q
Template method and strategy both vary steps of an algorithm. When is each right, and why has the default shifted to strategy?

## A
- **Template method**: the *skeleton* is fixed in a base class; subclasses override selected hook steps (**inheritance**, variation chosen at class-definition time). Right when the invariant sequence is the point and variants are few and stable — e.g. a test framework's setup/run/teardown.
- **Strategy**: the varying step is an injected object (**composition**, swappable at runtime, independently testable, combinable — one class can hold several strategies).

Default is strategy because template method inherits inheritance's problems: one variation axis only, fragile base class, subclass locked to one variant forever. Rule of thumb: template method for framework skeletons you own; strategy everywhere the variation is a *domain* concept (pricing, parsing, matching).

## Q zh
Template Method vs Strategy——都定义可变步骤。何时选择哪一个？

## A zh
- **Template Method**：基类中的**骨架**（固定顺序的步骤），子类覆盖**钩子**。绑定在继承中。例：`PaymentProcessor` 有 `process()`，`validate()` / `charge()` / `confirm()` 是钩子。
- **Strategy**：**完整的算法**由外部对象持有，用 `setStrategy()` 或构造函数注入交换。解耦、灵活。例：`Sorter` 持有 `Comparator`。

选择：
- 步骤顺序**固定**，只有实现不同？→ Template Method。
- 想**在运行时交换**整个算法？→ Strategy。
- 步骤**独立/独立变化**？→ Strategy（更灵活）。

Modern 偏好：Strategy（组合）优于 Template Method（继承）。
