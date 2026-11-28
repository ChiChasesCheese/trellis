---
id: hi-c-sd-online-auction-b01-conditional-update
node: sd.problem-breakdowns.online-auction.beyond
type: qa
step: 1
---
## Q
**在线拍卖 · 拓展：用一条带条件的 UPDATE 取代先读后写**｜拓展 · 加分

怎样把"比较并更新最高价"压成一条 SQL，它为什么是原子的？Python 里怎么写？

## A
- **做法：** `UPDATE auctions SET max_bid = :b, leader = :u WHERE id = :a AND status = 'OPEN' AND max_bid < :b`。检查和修改在同一条语句里，没有"读了再写"的空窗。
- **结果判断：** 看受影响行数：1 表示这条出价赢了，0 表示价格不够或拍卖已结束。不用先 SELECT，少一次往返。
- **为什么安全（Postgres）：** 更新要先拿到这行的行锁；如果另一个事务正持有锁，要等它提交，然后用最新的行值重新判断 WHERE 条件（READ COMMITTED 级别下这样做），所以后到的低价出价会发现条件不再成立，受影响行数为 0。
- **和 OCC 的关系：** 这就是把"版本号"换成"最高价本身"的 OCC，但冲突在数据库内部排队，不需要应用层重试循环。
- **记录出价放同一事务：** 无论赢输都插入一条 bids 记录，保留审计；更新与插入在一个事务里。
- **模式。** 条件写入：把前置条件写进写操作本身，让数据库来仲裁。
- **边界：** 其他隔离级别（可重复读、可串行化）下可能报序列化失败，需要重试。

```python
def place_bid(db, auction: int, user: int, amount: int) -> bool:
    with db:  # 一个事务：抬价和记录一起成功或一起不发生
        cur = db.execute(
            "UPDATE auctions SET max_bid=?, leader=? "
            "WHERE id=? AND status='OPEN' AND max_bid < ?",
            (amount, user, auction, amount))
        ok = cur.rowcount == 1   # 1 行被改 = 赢；0 行 = 价不够或已结束
        db.execute("INSERT INTO bids(auction_id,user_id,amount,accepted) VALUES (?,?,?,?)",
                   (auction, user, amount, int(ok)))
        return ok
```
