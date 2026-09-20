---
id: problems-digital-wallet-idempotency-reuses-account-lock
node: problems.marketplaces.digital-wallet
type: qa
step: 6
tags: [grown]
---
## Q
数字钱包要支持幂等转账（同一个 client_key 重试不能把钱移动两次），为什么可以直接复用转账本身的两把账户锁，而不需要为每个 client_key 单独建一张锁表？

## A
同一个 client_key 的重试，转出账户和转入账户必然相同（重试定义上就是同一笔转账的第二次尝试），所以它们必然要竞争同一对账户的锁——这对锁提供的互斥性已经足够：第一个到达的请求持锁执行并把回执写入幂等缓存后再释放锁，第二个请求这时候才能拿到锁，一查缓存就命中，直接返回同一个回执而不重新执行。额外建一张“client_key → 锁”的表会引入一个没有天然出口的新容器：一个 key 用过一次之后再也用不到，但代码不知道“以后不会再来”，只能让锁表无限增长。
