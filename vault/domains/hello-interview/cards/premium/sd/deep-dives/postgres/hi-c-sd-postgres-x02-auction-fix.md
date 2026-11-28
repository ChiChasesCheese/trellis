---
id: hi-c-sd-postgres-x02-auction-fix
node: sd.deep-dives.postgres.exam
type: qa
step: 2
---
## Q
**PostgreSQL · 补全竞价事务的并发保护**｜考点 · 必会

下面是竞价逻辑：`BEGIN; SELECT maxBid FROM Auction WHERE id=123; 应用判断 100 > maxBid; INSERT bids ...; UPDATE Auction SET maxBid=100 WHERE id=123; COMMIT;`。在 Read Committed 下并发会怎样？给出两种修法并比较，再说各自引入的新风险。

## A
- **出错方式：** 两个事务读到同一个旧最高价，都通过检查，都插入出价；较低的那条也留下，破坏"只接受更高价"。
- **修法一，行级锁：** 把第一条改成 `SELECT maxBid ... FOR UPDATE`。第二个事务在这一行上排队，等第一个提交后重新读到 100，检查就失败。新风险：多行加锁顺序不一致会死锁，需要固定加锁顺序。
- **修法二，SERIALIZABLE：** 代码不变，冲突时数据库回滚其中一个。新风险：应用必须捕获序列化失败并重试。
- **选择：** 竞价明确知道要锁哪一行，选行级锁；并发度更高，不需要重试逻辑。
- **补充：** 只改单一行的值时，`UPDATE ... WHERE maxBid < :bid` 一句话也能原子完成，再看影响行数即可。
