---
id: problems-stock-exchange-buying-power-conditional-update
node: problems.commerce.stock-exchange
type: qa
step: 6
tags: [grown]
---
## Q
A brokerage needs to reserve buying power for a new order without letting two concurrent order submissions both pass a balance check and together overdraw the account. Why does a single conditional SQL update like `UPDATE accounts SET buying_power = buying_power - :notional, reserved = reserved + :notional WHERE id = :accountId AND buying_power >= :notional` close this race, where a read-then-write pattern (SELECT buying_power, check in application code, then UPDATE) does not?

## A
In a read-then-write pattern, two concurrent requests can both execute the SELECT and see the same pre-deduction balance, both pass the application-level check, and both then issue an UPDATE — over-committing the account. The single conditional UPDATE instead evaluates the balance check and performs the deduction in one atomic database statement: the database's row-level write serializes concurrent attempts, so only the first to execute actually has its WHERE clause matched (rows affected = 1); any later concurrent attempt re-evaluates the condition against the now-reduced balance and fails (rows affected = 0), which the caller treats as insufficient buying power. There is no window between checking and writing because they are the same operation.

## Q zh
经纪商需要为一笔新订单预占用买力（buying power），同时不能让两个并发的下单请求都通过余额校验、合计超支账户。为什么单条 SQL 条件更新语句 `UPDATE accounts SET buying_power = buying_power - :notional, reserved = reserved + :notional WHERE id = :accountId AND buying_power >= :notional` 能关闭这个竞态窗口，而“先查询余额、应用层判断、再更新”的模式不能？

## A zh
在“先查后写”的模式下，两个并发请求可能都执行了 SELECT、看到同一份扣减前的余额、都在应用层判断通过、然后都发起 UPDATE——导致账户被超额占用。单条条件更新语句则把余额校验和扣减压缩进同一条原子的数据库语句：数据库的行级写会把并发尝试串行化，只有先执行的那个请求的 WHERE 条件真正匹配（受影响行数为 1）；之后的并发尝试会针对已经被扣减过的新余额重新判断条件，因而失败（受影响行数为 0），调用方把这个结果当作买力不足处理。因为校验和写入是同一个操作，两者之间不存在窗口期。
