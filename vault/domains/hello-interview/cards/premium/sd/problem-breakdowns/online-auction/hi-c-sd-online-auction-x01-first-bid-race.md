---
id: hi-c-sd-online-auction-x01-first-bid-race
node: sd.problem-breakdowns.online-auction.exam
type: qa
step: 1
---
## Q
**在线拍卖 · 预测失败：第一条出价与 FOR UPDATE**｜考点 · 必会

一场刚开始的拍卖还没有任何出价。两个用户同时出价，都执行"SELECT … FOR UPDATE 锁该拍卖所有出价行，查最大值，插入"。在 Postgres 默认的隔离级别下会发生什么？怎么修？

## A
- **结果：** 此时锁定的行集合是空的，两个事务都没有锁到任何东西，都读到"没有最大值"，都通过比较，都插入。两条出价都被接受，竞态没有被挡住。
- **和有出价时同一个根因：** FOR UPDATE 只锁已存在的行，挡不住并发的插入。有出价时还有人被锁住的假象；没出价时是彻底没锁。
- **修法一：** 锁拍卖那一行（`SELECT … FROM auctions WHERE id = :id FOR UPDATE`），所有出价的比较都先拿这把锁，行永远存在；
- **修法二：** 咨询锁（advisory lock），按拍卖 ID 加锁；
- **修法三：** 把最高价放在拍卖行，用带条件的更新，一条语句同时完成比较和写入。
- **注意：** 个别数据库的更高隔离级别或间隙锁（如 MySQL InnoDB 的可重复读）能挡住范围内的插入，但行为因数据库而异，不要依赖，要在设计里显式锁一个存在的行。
