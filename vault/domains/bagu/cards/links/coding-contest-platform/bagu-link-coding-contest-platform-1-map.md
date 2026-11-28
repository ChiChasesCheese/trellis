---
id: bagu-link-coding-contest-platform-1-map
node: links.coding-contest-platform
type: qa
step: 1
---
## Q
**在线判题与编程竞赛平台（LeetCode） · 会被追问哪些八股**｜必会

设计在线判题与编程竞赛平台（LeetCode）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 难点是安全地跑不可信代码和比赛开始的提交洪峰。基础是：异步队列与消费者组削峰、限并发而不是限 QPS、cgroup 限制 CPU 和内存、ZSet 做榜单。

**下钻路线。**
- 比赛开始的提交洪峰 → 异步判题队列削峰，限并发而不是限 QPS，[[a.protect.rate-limit-algorithms|限流算法]]
- 一次判题几十秒，worker 扩容会卡全组吗 → 重平衡会暂停消费，调大 poll 间隔，[[b.mq.rebalance|消费者组重平衡为什么卡、怎么避免]]
- 判题队列满了 → 有界队列加拒绝策略，返回排队中让用户感知，[[a.runtime.java-threadpool|线程池的参数、执行流程与大小设置]]
- 用户死循环打满 CPU → cgroup CPU 配额加超时强杀，[[b.linux.cpu-load|CPU 使用率高与 load 高但 CPU 低]]
- 代码疯狂申请内存 → cgroup 内存上限，超限只杀该沙箱，[[b.net.memory-oom-swap|内存管理]]
- 用户代码防逃逸 → 最小权限、禁网络、只读文件系统，沙箱隔离，[[b.agent.safety-sandbox|Agent 安全]]
- 实时榜单与我的名次 → ZSet，分数编码罚时，[[a.redis.zset-skiplist|ZSet 与跳表]]
- 十亿行提交表显示总数、加列 → 汇总表计数，加列用 INSTANT 或 gh-ost，[[b.mysql.count-ddl|count 为什么慢，大表怎么加字段]]

**业务场景。** 类似直播开播的瞬间洪峰：开赛一刻几万人同时提交，和直播间开播涌入是同一类削峰问题。
**系统设计。** [[links.tt-flash-sale-ticketing|秒杀抢票（排队、限流、防超卖）]]：同样先削峰，但保护的是库存而不是 CPU；[[links.realtime-game-leaderboard|在线游戏排行榜（全球榜 + 我的名次 + 好友榜）]]：榜单同样用 ZSet，但分数来自游戏服务器。
