---
id: hi-c-sd-dealing-with-contention-n04-conditional-write-txn
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 4
---
## Q
**处理竞争 · 条件写 · 两个写要一起成功**｜摘要 · 必会

扣库存的同时还要插入一条订单记录，两条语句放进事务就够了吗？有什么暗坑？

## A
- **事务的作用：** `BEGIN ... COMMIT` 把多条写入变成"要么都发生，要么都回滚"，避免座位扣了但订单没建成。
- **暗坑：** `UPDATE` 匹配 0 行不是错误，语句照常成功，事务不会回滚。如果 `INSERT` 无条件执行，抢输的 Bob 也会得到一张根本没抢到座位的票。
- **修法一（纯 SQL）：** 用 `WITH reservation AS (UPDATE ... RETURNING ...) INSERT ... SELECT ... FROM reservation`。只有更新真的改了行才有返回行，插入才有数据可写。
- **修法二（应用层）：** 检查更新的受影响行数，为 0 就回滚并返回失败。
- **要点：** 凡是"更新后做后续动作"，都要用受影响行数当闸门。
