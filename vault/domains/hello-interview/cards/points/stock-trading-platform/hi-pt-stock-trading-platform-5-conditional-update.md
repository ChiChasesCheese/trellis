---
id: hi-pt-stock-trading-platform-5-conditional-update
node: qb.sd.stock-trading-platform.points
type: qa
step: 5
---
## Q
**股票交易平台（券商端） · 条件更新防超额占用**｜出自：股票交易平台（券商端） › 深入 1

并发下单时怎样保证买入不超过购买力、卖出不超过持有？先读后扣、悲观锁、条件更新哪个是首选？

## A
**问题。** 先读余额再判断再扣：两个并发请求都读到够用，都通过，超卖。
**首选。** 条件更新 `UPDATE account SET reserved = reserved + :x WHERE id=:id AND cash - reserved >= :x`，行数为 0 就拒单，一条语句原子完成检查和占用。卖单同样更新持仓 `frozen`，要求 `qty - frozen >= :n`。
**备选。** `SELECT ... FOR UPDATE` 也正确，同账户串行。单账户下单频率低，没有瓶颈。
