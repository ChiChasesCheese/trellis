---
id: principles-when-inherit
node: principles.composition
type: qa
---
## Q
什么时候继承是正确的选择？

## A
继承合适的场景：
- IS-A 关系是真实的且稳定：`Dog IS-A Animal`
- 子类需要重写行为（模板方法、策略模式风格）
- 框架要求它（如 JUnit 的 TestCase）

继承不适合：
- 代码重用；使用组合
- 不同的对象类型（如 ArrayList 和 Stack）
- 你只想从一个类中获取一些方法

经验法则：如果你不能用一句话解释"为什么 B 是 A"，那就使用组合。
