---
nodes: [problems.marketplaces.digital-wallet]
url: https://algomaster.io/learn/lld
tags: [no-archive]
---
# AlgoMaster — Low Level Design (LLD)

值得读：AlgoMaster 的 LLD 系列课程目录，钱包/支付相关的章节把"防止同一笔请求被重复
扣款"列为并发小节要考虑的问题，但没有展开成一份可运行的幂等实现。本文把幂等实现为
"复用账户锁本身的互斥性、不另建一张按 key 的锁表"，并且专门测试了"同一个 key 用在了
不同参数的转账上必须报错"这个更容易被面试现场忽略的分支。
