---
id: hi-c-sd-flash-sale-x02-check-then-decrement
node: sd.problem-breakdowns.flash-sale.exam
type: qa
step: 2
---
## Q
**限时抢购 · 排错：检查和扣减拆成两条语句**｜考点 · 必会

代码先 `SELECT inventoryCount`，大于 0 再 `UPDATE … SET inventoryCount = inventoryCount - 1`，两句在同一事务里（默认 READ COMMITTED）。只剩 1 件，A、B 同时请求，会发生什么？怎么改？

## A
- **时序：** A 和 B 都读到 1；A 更新为 0 并提交；B 的更新在 A 提交后执行，把 0 减成 −1（或在没有约束的情况下无声地继续）。两个人都拿到预留，超卖 1 件。事务本身不会替你保护"先读后写"之间的假设。
- **修法一：** 单语句条件更新 `UPDATE … SET n=n-1 WHERE productId=? AND n>0`，检查和修改在一条语句里原子完成，并检查影响行数：1 表示成功，0 表示售罄。
- **修法二：** 先 `SELECT … FOR UPDATE` 锁住行，读和写之间别人改不了。
- **兜底：** 在库存列上加 `CHECK (inventoryCount >= 0)`，即使代码出错，数据库也会拒绝把它减成负数。
- **常见遗漏：** 忘记检查影响行数，把"0 行被更新"当成功。
