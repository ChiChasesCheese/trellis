---
id: problems-lock-service-watch-herd-effect-context
node: problems.foundations.lock-service
type: qa
step: 5
tags: [grown]
---
## Q
In a coordination service design, why is it correct for a mutex-lock recipe to have each waiter watch only its immediate predecessor node (waking exactly one client per release), while it is correct for a 200-instance group's shared 'current leader pointer' to wake all 200 watchers on a single change — even though both look like the same 'many watchers on one key' pattern?

## A
The two cases differ in what the watchers actually need once notified. For a mutex lock, only one waiter can ever legally acquire the lock next, so waking all waiters means every one of them but one performs wasted work re-checking and re-competing — an O(n) thundering herd that gets worse as n grows; watching only the predecessor node wakes exactly the one client whose turn it now is. For a leader pointer watched by a whole group, every member genuinely needs to learn the new value to route correctly, so waking all of them is the desired behavior, not a bug to avoid. The watch mechanism itself stays a simple one-shot, payload-free signal in both cases — which behavior you get is entirely determined by which node the recipe chooses to register the watch against, not by anything the server does differently.

## Q zh
在一个协调服务设计中，为什么一个互斥锁配方让每个等待者只 watch 自己紧邻的前驱节点（每次释放恰好唤醒一个客户端）是对的，而一个 200 实例服务组共享的「当前 leader 指针」在一次变化时唤醒全部 200 个 watcher 也是对的——尽管两者表面上都是「很多 watcher 盯着同一个键」这种模式？

## A zh
这两种情况的区别在于被唤醒之后各个 watcher 真正需要什么。对互斥锁而言，下一个能合法拿到锁的永远只有一个，所以唤醒所有等待者意味着除了一个之外全都在做无谓的重新检查和重新竞争——这是一次会随 n 增大而恶化的 O(n) 惊群；只 watch 前驱节点则恰好唤醒轮到的那一个客户端。而对一整个组共享的 leader 指针而言，每个成员都真的需要知道新值才能正确路由，所以唤醒所有人正是期望行为，不是需要避免的 bug。watch 机制本身在两种情况下都保持简单、一次性、不携带数据——具体会得到哪种行为，完全由配方选择把 watch 注册在哪个节点上决定，而不是由服务端做了什么不同的事情。
