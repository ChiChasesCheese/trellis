---
id: cc-verification-invariant-two-indexes
node: verification.invariants
type: qa
---
## Q
You keep a `dict` from id to record and a second index from target to its member set. What is the failure mode, and what discipline prevents it?

## A
**The two structures drift**: an entity is removed from one and left in the other, so a later query returns a phantom — or a capacity check counts a member who left.

- Discipline: **one function per transition** (`place`, `remove`, `move`) that updates *every* structure. No caller touches a structure directly, so there is exactly one place to be wrong.
- Invariant to assert in tests: the indexes contain the same set of ids, and each id maps back consistently.
- The coupling *is* the cost of a second index. Pay it only when it makes a hot query sub-linear ([[cc-performance-budget-bounds-multiply]]), and delete the index when the query it served moves.

## Q zh
你维护了一个 id 到记录的 `dict`，还有一个从目标到其成员集合的第二索引。故障模式是什么？什么纪律能防住它？

## A zh
**两个结构会漂移**：某个实体从一个里被移除、却留在另一个里，于是后续查询返回幽灵条目 —— 或者容量检查把已离开的成员算了进去。

- 纪律：**每个状态转移一个函数**（`place`、`remove`、`move`），由它更新*所有*结构。调用方不直接碰任何结构，于是只有一个地方可能出错。
- 要在测试里断言的不变量：两个索引包含同一组 id，且每个 id 反向映射一致。
- 这种耦合*就是*第二索引的代价。只有当它让热点查询变成次线性时才付（[[cc-performance-budget-bounds-multiply]]），一旦它服务的那个查询变了就删掉它。
