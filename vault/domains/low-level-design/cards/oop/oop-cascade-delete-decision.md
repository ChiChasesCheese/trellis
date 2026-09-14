---
id: oop-cascade-delete-decision
node: oop.relationships
type: qa
---
## Q
`removeFloor(floor)` is called. How does the relationship type decide what happens to the objects the floor referenced, and what must you clean up regardless?

## A
- **Composition (owned parts)** — `Spot`s exist only inside that floor → **cascade**: delete them with the floor; nothing else may hold a reference.
- **Aggregation (shared parts)** — a `Vehicle` parked there outlives the floor → **never cascade**: either detach (`spot.release()`) or **refuse the delete** while a live reference exists, which is usually the right answer for occupied floors.

Regardless of type, delete must also remove the object from every **secondary index / back-pointer** you built (`spotById`, `ticketsByPlate`). In-memory designs don't have foreign keys, so a missed index entry becomes a stale object that stays reachable and reads as "deleted but still bookable."

## Q zh
调用了 `removeFloor(floor)`。关系类型如何决定这层楼所引用的对象会怎么样，以及无论哪种类型你都必须清理什么？

## A zh
- **Composition（被拥有的部件）** —— `Spot` 只存在于这层楼里 → **级联删除**：跟着楼一起删，不允许别处还持有引用。
- **Aggregation（共享的部件）** —— 停在那里的 `Vehicle` 比这层楼活得久 → **绝不级联**：要么解除关联（`spot.release()`），要么在还有活引用时**拒绝这次删除** —— 对有车占用的楼层，后者通常才是对的答案。

无论哪种类型，删除还必须把对象从你建的每一个**二级索引 / 反向指针**里移除（`spotById`、`ticketsByPlate`）。内存态设计没有外键，所以漏掉一条索引项就会留下一个可达的陈旧对象，表现为"已删除但仍然能被预订"。
