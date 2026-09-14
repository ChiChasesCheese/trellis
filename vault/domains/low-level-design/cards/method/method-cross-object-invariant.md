---
id: method-cross-object-invariant
node: method.modeling
type: qa
---
## Q
"A vehicle may hold at most one active ticket." Neither `Vehicle` nor `Ticket` can enforce this alone. Where does the invariant go?

## A
An invariant spanning several objects belongs to the **smallest object that can see all of them** — here `ParkingLot` (the aggregate root), which owns ticket issuance and can check the existing-active-ticket index atomically.

Consequences worth saying out loud:
- `new Ticket(...)` must not be callable from outside; construction goes through `lot.issueTicket(vehicle)`.
- The root becomes the **transaction/lock boundary** if concurrency is added later.

Rule: if enforcement needs two objects' state, neither of them is the owner — find or introduce the one that contains both.


## Q zh
"一辆车最多持有一个活跃的停车票。"既不是 `Vehicle` 也不是 `Ticket` 能单独执行这个。这个不变式放在哪里?

## A zh
一个跨越多个对象的不变式属于**能看到它们所有对象的最小对象** — 这里是 `ParkingLot`（聚合根），它拥有票的签发并能原子地检查现有活跃票的索引。

值得明确说的后果:
- `new Ticket(...)` 不能从外部调用；构造通过 `lot.issueTicket(vehicle)` 进行。
- 如果以后添加并发，根变成**事务/锁边界**。

规则：如果执行需要两个对象的状态，两者都不是所有者 — 找到或引入包含两者的那个。
