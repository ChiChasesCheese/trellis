---
nodes: [problems.marketplaces.digital-wallet]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/digital-wallet-service.md
tags: [no-archive]
---
# Design a Digital Wallet Service | LLD | Low Level Design

值得读：ashishps1/awesome-low-level-design 仓库里的钱包设计题，给出了账户、交易记录、
钱包服务的类图和多语言实现骨架。它的余额是账户对象上的一个可变字段，充值/提现/转账各自
独立更新余额，没有"每笔移动都是两条分录"的统一表示，并发控制用给整个服务加一把大锁；
本文把余额收成账本的缓存投影，按账户拆分锁并给出稳定的加锁顺序。
