---
id: problems-lock-service-fencing-token-is-free
node: problems.foundations.lock-service
type: qa
step: 3
tags: [grown]
---
## Q
In a distributed lock service built on a consensus-replicated log, why doesn't the design need a separate mechanism to generate fencing tokens, and what is the interface-level contract that still has to be designed deliberately?

## A
Because every successful write to the replicated log already produces a monotonically increasing position/version number as a structural side effect of consensus — reusing that value as the fencing token means a lock service built this way gets a verifiable, monotonically increasing token for free, unlike an ad hoc multi-instance voting scheme (e.g. Redlock), whose protocol has no equivalent value to hand out. What still requires deliberate design is the contract with the downstream resource: the lock service can only hand out the token, it cannot enforce anything — the protected resource itself must persist the highest token it has seen and reject writes carrying a lower one, since the lock service has no way to intercept or validate writes made directly to that resource.

## Q zh
在一个建立在共识复制日志之上的分布式锁服务中，为什么设计不需要另外发明一套机制来生成 fencing token？接口层面仍然需要刻意设计的契约是什么？

## A zh
因为复制日志的每一次成功写入本身，作为共识机制的结构性副产品，就已经产生了一个单调递增的位置/版本号——把这个值复用为 fencing token，意味着这样建出来的锁服务天生就能拿到一个可验证的单调递增令牌，不像 Redlock 这类临时的多实例投票方案，其协议本身根本产生不出一个等价的值可以发放。仍然需要刻意设计的是和下游资源之间的契约：锁服务只能发放令牌，它无法强制任何事情——真正被保护的资源必须自己持久化它见过的最大令牌，并拒绝携带更小令牌的写入，因为锁服务没有办法拦截或校验直接写向那个资源的请求。
