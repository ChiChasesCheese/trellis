---
nodes: [problems.components.lru-cache, python.data-model, structure.api]
tags: [problem]
---
# Drill：LRU / LFU 缓存

一个固定容量的进程内缓存，支持 `get`/`put`，两者都要 O(1)；容量满了要按某种规则淘汰。
先亲手写出哈希表配双向链表的核心结构，再让淘汰规则、线程安全、过期时间逐关加上去，
每一关都不应该逼你回头重写已经写好、已经测过的类。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`get(key)`/`put(key, value)` 均为 O(1)，容量满时按最近最少使用
  （LRU）淘汰最久未用的 key；覆盖写入已有 key 不算淘汰、也不触发淘汰判断；容量必须是正整数，
  否则要在构造时就报错；键值支持任意可哈希类型（不要假设 key 是 `int`/`str`）。
- 第 2 关（约 15 分钟）：加一种新的淘汰规则——LFU（最不经常使用），频率相同时淘汰同频率里
  最久未用的那个。要求：不能新写一个平行的 `LFUCache` 类，必须让同一个缓存类通过换一个
  参数就能在 LRU/LFU 之间切换，且淘汰选择和插入/更新一样都是 O(1)（不能遍历找最小频率）。
- 第 3 关（约 15 分钟）：让缓存在多线程下安全——多个线程并发调用 `get`/`put` 不应该出现
  条目数超过容量、或者某次写入凭空丢失。先说清楚"粗粒度锁"怎么加、为什么 `get` 在这里也要
  加锁，再讨论有没有更细粒度的方案。
- 第 4 关（选做）：给每个 key 加一个可选的存活时间（TTL），时钟从外部注入（不要在核心逻辑
  里直接调用 `time.time()`），过期的 key 应该表现得像不存在一样。要求这一关的代码新增，
  而不是回头修改第 1/2 关已经写好的类。

**怎么练**：把 `vault/domains/low-level-design/problems/lru-cache/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lru-cache -q`。

**评分点**
- 一开始就把"存储"（key→value）和"淘汰顺序"拆成两个职责，而不是把链表操作直接写进
  `get`/`put`（[[problems-lru-cache-store-vs-order-split]]、[[problems-lru-cache-strategy-pattern-python-form]]）
- 双向链表用头尾哨兵节点，插入/删除/挪到尾部不需要对"链表为空""操作的是头/尾节点"做任何特判
  （[[problems-lru-cache-sentinel-dll-on1]]）
- key 必须可哈希才能放进哈希表当键，说得出相等与哈希契约在这里起的作用
  （[[python-data-model-hash-eq-contract]]）
- LFU 用 `min_freq` 指针维护当前最小频率桶，而不是每次淘汰都扫描找最小值；说得出 `min_freq`
  只在插入新 key、或某个桶被搬空时才移动（[[problems-lru-cache-lfu-min-freq-pointer]]）
- 覆盖写入一个已有 key 和插入一个新 key 走不同的代码路径，不会因为更新触发不必要的淘汰
  （[[problems-lru-cache-overwrite-not-insert]]）
- 说得出为什么这里 `get` 也是一次"写"、为什么读写锁在这里帮不上忙，以及一把粗粒度锁背后
  隐藏着和"`dict` 加锁做复合操作"一样的丢更新风险（[[problems-lru-cache-get-is-write]]、
  [[structure-storage-chm-compound-ops]]）
- TTL（或者命中率统计）作为独立的包装类加上去，不修改缓存和策略类原有的代码
  （[[problems-lru-cache-ttl-wrapper-extension]]）

**题解**：[[solution-lru-cache]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
