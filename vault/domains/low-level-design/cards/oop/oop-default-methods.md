---
id: oop-default-methods
node: oop.interfaces
type: qa
---
## Q
What problem do interface default methods solve, and which two limits keep them from replacing abstract classes?

## A
They let a published interface **grow without breaking existing implementations** — add the method with a sensible default, implementers override at leisure.

Limits:
- **No instance state** — a default can only compute over the interface's own methods.
- **Diamond conflicts**: inherit the same default from two interfaces and the class must override explicitly (`InterfaceName.super.method()` to pick one).

## Q zh
接口的 default method 解决了什么问题，又是哪两个限制让它无法取代抽象类？

## A zh
它让一个已经发布的接口能够**在不破坏现有实现的前提下增长** —— 加方法时给一个合理的默认实现，实现方可以从容地按自己的节奏去覆盖。

限制：
- **没有实例状态** —— default 方法只能基于接口自己的方法去计算。
- **菱形冲突**：从两个接口继承到同名 default，类就必须显式覆盖（用 `InterfaceName.super.method()` 挑一个）。
