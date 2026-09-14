---
id: oop-entity-vs-value-object
node: oop.values
type: qa
---
## Q
`Ticket` vs `Money` in a parking-lot design: which is an entity, which a value object, and how does equality differ between them?

## A
- `Ticket`: **entity** — has an id and a lifecycle; two tickets with identical fields are still different tickets. Equality = identity (compare ids).
- `Money(amount, currency)`: **value object** — immutable, no id; equality = structural (all fields), so `equals`/`hashCode` over fields.

Test: if you'd track it over time, it's an entity; if its attributes fully describe it, it's a value.

## Q zh
停车场设计里的 `Ticket` 和 `Money`：哪个是 entity，哪个是 value object，两者的相等性有什么不同？

## A zh
- `Ticket`：**entity** —— 有 id、有生命周期；两张字段完全相同的票仍然是两张不同的票。相等 = 同一性（比 id）。
- `Money(amount, currency)`：**value object** —— 不可变、没有 id；相等 = 结构性相等（比所有字段），所以 `equals`/`hashCode` 建立在字段上。

判据：如果你需要追踪它随时间的变化，它是 entity；如果它的属性就完整描述了它，它是 value。
