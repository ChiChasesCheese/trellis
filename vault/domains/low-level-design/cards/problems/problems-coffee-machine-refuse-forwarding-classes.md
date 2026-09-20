---
id: problems-coffee-machine-refuse-forwarding-classes
node: problems.machines.coffee-machine
type: qa
step: 13
tags: [grown]
---
## Q
设计咖啡机时，`Menu`（菜单）类、`Outlet`（出口）类、以及机器上的 `refill()` 方法，这三样该不该有？判据是什么？

## A
三样都不要，判据是**它守着什么不变式**。`Menu` 除了『一个加了锁的字典』之外没有别的不变式，于是它就是机器里的一个字段；`Outlet` 需要的全部性质是『有编号、数量有限、用完归还』，而 `queue.Queue` 恰好就是这个；机器上的 `refill()` 只会把调用原样转发给库存的 `refill()`，不承担任何额外职责——库存是构造时注入的协作者（运维本来就直接对着料仓补货），把它作为只读属性交出去即可。『加一个类只是为了让另一个类少两个字段』是从 Java 带来的门面层习惯：一个类要么有自己的不变式，要么删掉，并在讲设计时说清是哪一种。
