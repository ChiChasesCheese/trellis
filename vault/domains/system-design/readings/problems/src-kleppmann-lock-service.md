---
nodes: [problems.foundations.lock-service]
url: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
tags: [reference]
---
# Kleppmann — How to do distributed locking

值得读：一手分析文章，本题解对 Redlock 的批评直接引自这篇文章的论证——Redlock 的安全性
依赖一系列时序假设（进程不会长时间暂停、网络延迟有界、时钟漂移有界），且协议本身产生不出
可验证的单调递增令牌。本题解认同它的核心结论（锁的正确性依赖必须用 fencing token，效率
优化场景可以不用），但把落地方式放在了一个真正的共识系统里，而不是停留在"该不该用 Redlock"
这个问题本身。
