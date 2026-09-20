---
nodes: [problems.components.ttl-cache, structure.api, concurrency.primitives]
tags: [problem]
---
# Drill：带过期时间的缓存（TTL Cache）

一个进程内缓存：固定容量，每条数据可以单独设定存活时间（TTL），到点必须失效。
规模是一百万条数据、几十个线程。**这道题真正加进来的东西不是一个时间字段**，
而是"数据会在没有任何人调用的情况下变得不合法"——本题几乎所有分歧都从这一句长出来。
照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`get`／`put(key, value, ttl)`／`delete`，时钟从构造函数注入，
  整套测试里不许出现 `sleep`。核心设计题是**过期由谁发现**：读时惰性判断、后台线程定期
  全表扫描、按截止时刻排序的索引——三个都要能说出代价，判据是"一条写进来之后再也没人读的
  数据会怎样"。选定之后写出来，并回答一条数据该存"还能活多久"还是"什么时刻死"。
- 第 2 关（约 15 分钟）：加容量上限和淘汰策略。先定死一个语义问题：已经过期、但还没被物理
  删除的条目，`len()`、遍历、"容量满了吗"分别该怎么看它——想清楚算进去会让哪件事出错。
  然后回答"满了先赶走谁"：按策略，还是按最近的截止时刻？把这个分歧做成同一条接缝的两种实现。
- 第 3 关（约 15 分钟）：线程安全；"读一次续一次命"作为构造参数而不是第二个类；
  然后是一百个线程同时未命中同一个 key 的场景——回源只许发生一次。
  想清楚为什么不能把整段"取不到就回源"锁起来，以及领跑者写缓存和唤醒后来者的先后顺序。
- 第 4 关（选做）：命中／未命中／过期／淘汰四个计数，以及数据离开缓存时的回调。
  判分点只有一个：存储、策略、到期索引三个类一行都不许改。
  顺便想想为什么这两样都**不该**用装饰器或订阅框架来做。

**怎么练**：把 `vault/domains/low-level-design/problems/ttl-cache/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/ttl-cache -q`。

**评分点**
- 三种过期方案当场比较，并说得出"没人再读的数据"在每种方案下的下场（[[problems-ttl-cache-three-ways-to-expire]]）。
- 到期堆里的墓碑会被压实掉，并把堆长度暴露成可断言的只读属性（[[problems-ttl-cache-tombstones-must-be-compacted]]）。
- 堆元组里有自增序号，说得出没有它为什么会偶发 `TypeError`（[[problems-ttl-cache-heap-tuple-needs-a-counter]]）。
- 过期条目对 `len()`、遍历和容量判断一律不可见，并说得出算进去会提前淘汰活数据（[[problems-ttl-cache-expired-is-invisible]]、[[structure-api-leaking-internals]]）。
- 存绝对截止时刻而不是剩余时间；时钟注入且用 `time.monotonic`（[[problems-ttl-cache-absolute-deadline-not-remaining]]）。
- "满了淘汰谁"做成可替换策略，并说得出按最近截止时刻淘汰的理由（[[problems-ttl-cache-evict-by-policy-or-deadline]]）。
- 未命中回源有单飞闸门，先写缓存再唤醒，摘牌写在 `finally` 里（[[problems-ttl-cache-single-flight]]、[[concurrency-lock-while-calling-out]]）。
- 统计返回不可变快照、淘汰事件带着值且在锁外广播，并拒绝把统计做成装饰器（[[problems-ttl-cache-stats-and-callback-refuse-patterns]]、[[patterns-observer-notify-lock]]）。
- 一百万条数据全部过期之后，存活条数和索引长度都真的回落到零。

**题解**：[[solution-ttl-cache]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
