---
nodes: [amazon.amz-configurable-cache, patterns.strategy, patterns.structural]
tags: [problem]
---
# Drill：可配置缓存（Configurable Cache）

Amazon 面试官的原话是：设计一个缓存，淘汰策略（LRU、LFU）可插拔，存储后端（内存、文件）可互换。规模是一个进程内的缓存，容量几十到几千条，几个线程同时读写。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`Cache(capacity, policy, store)` 的 `get`／`put`／`delete`，先只做内存后端和 LRU。核心设计题是**缓存、策略、后端三者各管什么**：谁知道「淘汰谁」，谁知道「数据放哪」。写出来之后回答：覆盖一个已有的 key 要不要淘汰、算不算一次使用。
- 第 2 关（约 15 分钟）：加 LFU，并加一个 `create_cache(config)`，用名字（"lru"、"lfu"）选策略。要求 O(1) 选受害者；想清楚同频时淘汰谁，以及为什么新插入的 key 不能被自己淘汰。
- 第 3 关（约 15 分钟）：加文件后端，key 一个文件。先回答：key 里带 `../` 怎么办，值不能序列化怎么办，写到一半失败怎么办。然后回答最关键的一问：**后端写入失败时，策略和后端会不会不一致**，操作顺序怎么排。
- 第 4 关（选做）：TTL（注入时钟）、命中／未命中／淘汰／过期统计，以及线程安全。判分点：新增一种淘汰策略只加一个类并在注册表登记一行，`Cache` 与其他类一行不改。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-configurable-cache/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-configurable-cache -q`。

**评分点**
- 开场问清楚创建时选还是运行时切换、值的类型、要不要 TTL 与线程安全（[[amz-configurable-cache-prompt-and-three-questions]]）。
- 缓存、策略、后端各管一件事，说得出划分依据（[[amz-configurable-cache-objects-and-one-job-each]]）。
- 写入新 key 的顺序：先写后端，再淘汰，最后让策略登记（[[amz-configurable-cache-stage1-put-flow-code]]）。
- LFU 用频率桶加最小频率指针做到 O(1)，空桶即时删除（[[amz-configurable-cache-lfu-frequency-buckets]]）。
- 两条轴用组合而不是子类：说得出 4 个组合类的代价（[[amz-configurable-cache-bridge-vs-subclass-explosion]]）。
- 加一种新策略只加一个类并登记一行（[[amz-configurable-cache-followup-add-fifo-policy]]）。
- 后端写入失败时策略与后端保持一致（[[amz-configurable-cache-failed-write-policy-store-disagree]]）。
- 连 `get` 也加锁，并说得出 GIL 为什么不够（[[amz-configurable-cache-concurrency-lock-covers-reads]]、[[amz-configurable-cache-lfu-new-key-evicted-immediately]]）。

**题解**：[[solution-amz-configurable-cache]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
