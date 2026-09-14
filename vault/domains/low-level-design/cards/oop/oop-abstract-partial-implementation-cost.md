---
id: oop-abstract-partial-implementation-cost
node: oop.interfaces
type: qa
---
## Q
You put shared logic in an abstract base class with `protected` hooks (template method). What are you paying for that reuse, and what's the alternative shape?

## A
Costs:

- **You spend the single inheritance slot** — the subclass can never extend anything else.
- **`protected` members are public API to subclasses**: you can't rename or reorder them later without breaking every child, and the base's call order becomes a contract.
- The base is **hard to test alone** (needs a fake subclass), and subclasses can't be tested without dragging the base's behavior in.

Alternative: **interface + a composed helper** — the algorithm lives in a collaborator that takes the varying step as a strategy object. Java's compromise is the *skeletal implementation* pattern: publish the interface, offer `AbstractFoo` as an optional convenience so implementers who need their own hierarchy can forward to it instead.

## Q zh
你把共享逻辑放进一个带 `protected` 钩子的抽象基类（模板方法）。这份复用你要付出什么代价，替代方案是什么形状？

## A zh
代价：

- **你花掉了唯一的单继承名额** —— 子类以后再也不能继承别的东西了。
- **`protected` 成员对子类来说就是公开 API**：以后不能随意改名或调整调用顺序而不破坏每一个子类，基类的调用顺序也变成了一份契约。
- 基类**难以单独测试**（需要一个假的子类），子类也无法脱离基类的行为单独测试。

替代方案：**接口 + 一个组合的 helper** —— 算法住在一个协作对象里，把会变化的那一步作为 strategy 对象传入。Java 的折中方案是 *skeletal implementation*（骨架实现）模式：发布接口，把 `AbstractFoo` 作为一个可选的便利类提供出来，这样需要自建继承体系的实现者可以转而委托给它。
