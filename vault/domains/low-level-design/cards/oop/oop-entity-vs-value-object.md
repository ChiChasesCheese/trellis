---
id: oop-entity-vs-value-object
node: oop.values
type: qa
step: 1
---
## Q
停车场设计里的 `Ticket` 和 `Money`：哪个是 entity，哪个是 value object，两者的相等性有什么不同？

## A
- `Ticket`：**entity**——有业务意义上的 id、有生命周期；两张字段完全相同的票仍然是两张不同的票。相等应该比较那个业务 id，而不是 Python 对象本身的身份（`is`）。
- `Money(amount, currency)`：**value object**——不可变、没有 id；相等 = 结构性相等（比所有字段），`__eq__` 建立在字段上，通常用 `@dataclass(frozen=True)` 直接生成。

判据：如果你需要追踪它随时间的变化，它是 entity；如果它的属性就完整描述了它，它是 value。
