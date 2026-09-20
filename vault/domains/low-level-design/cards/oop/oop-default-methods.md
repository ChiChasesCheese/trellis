---
id: oop-default-methods
node: oop.interfaces
type: qa
---
## Q
接口的 default method 解决了什么问题，又是哪两个限制让它无法取代抽象类？

## A
它让一个已经发布的接口能够**在不破坏现有实现的前提下增长** —— 加方法时给一个合理的默认实现，实现方可以从容地按自己的节奏去覆盖。

限制：
- **没有实例状态** —— default 方法只能基于接口自己的方法去计算。
- **菱形冲突**：从两个接口继承到同名 default，类就必须显式覆盖（用 `InterfaceName.super.method()` 挑一个）。
