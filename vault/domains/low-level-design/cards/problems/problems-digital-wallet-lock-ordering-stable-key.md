---
id: problems-digital-wallet-lock-ordering-stable-key
node: problems.marketplaces.digital-wallet
type: qa
step: 5
tags: [grown]
---
## Q
数字钱包里一次转账要同时锁住转出和转入两个账户，为什么加锁的顺序必须按账户 id 这样的稳定键排序，而不能按参数 `(from, to)` 的顺序？

## A
按参数顺序加锁会造成经典的 AB-BA 死锁：线程 1 执行 `transfer(A, B, ...)` 先锁 A 再锁 B，线程 2 同时执行 `transfer(B, A, ...)` 先锁 B 再锁 A；如果线程 1 拿到 A、线程 2 拿到 B，两者都在等对方已持有的锁，构成环形等待，程序永远卡死且没有任何异常提示。按账户 id 的字典序等稳定键排序后，不管调用方传的是 `(A, B)` 还是 `(B, A)`，代码内部永远先锁同一个账户——两个方向的并发转账因此只会互相排队，不会互相等待，打破了环形等待这个死锁必要条件。
