---
id: bagu-db-consistency-5-binlog
node: a.cache.db-consistency
type: qa
step: 5
---
## Q
**缓存一致性 · 订阅 binlog 删缓存怎么落地**｜追问

面试官：「业务代码里删缓存总有遗漏，手工改库、运维脚本也会改数据，怎么统一处理？」

## A
**基本回答。** 用 Canal 或 Debezium 这类组件订阅数据库的 binlog，解析出变更行的主键，发消息给专门的消费者去删缓存。业务代码不用管缓存，所有写入路径都会触发。
**一句话记住。** 不再靠每个业务员自己记得去擦黑板，而是请一位「监控员」盯着账本的修改记录（binlog）：账本只要被改过，不管是谁改的，监控员都立刻去擦对应的黑板。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="8" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务服务写库</text>
<rect x="182" y="8" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">运维脚本、手工改库</text>
<rect x="90" y="56" width="160" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MySQL</text>
<text x="170" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入 binlog</text>
<line x1="83" y1="34" x2="134.402" y2="53.8395" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,56.0 132.3,56.5 134.6,50.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="257" y1="34" x2="205.598" y2="53.8395" stroke-width="1.2" stroke="currentColor"/>
<polygon points="200.0,56.0 205.4,50.5 207.7,56.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="86" x2="170" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,104.0 166.8,97.0 173.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="104" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Canal 或 Debezium</text>
<line x1="170" y1="132" x2="170" y2="144" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,150.0 166.8,143.0 173.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="150" width="160" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ 里带主键的消息</text>
<line x1="170" y1="176" x2="170" y2="186" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,192.0 166.8,185.0 173.2,185.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="192" width="160" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者删 Redis</text>
</svg>
无论是业务服务写库，还是运维脚本、手工改库，变更都会落进 binlog；后面的链路统一负责删缓存，业务代码完全不参与。
**讲明白。**
- **解决什么问题：** 业务代码里「更新库然后删缓存」总可能有遗漏，比如某个新写的接口忘了删，运维用脚本批量改库、DBA 手工改数据，这些都不会去删缓存。
- **做法：** Canal 模拟成数据库的从库，拉取 binlog（Debezium 同样是读 binlog），解析出变更的表和主键，投到消息队列，由专门的消费者按主键删除缓存。
- **为什么可靠：** binlog 是数据库已经提交的事实，不会漏；业务里「更新库和删缓存」两步可能在中间崩溃，binlog 不会。
- **重复消息无妨：** 删除是幂等的，同一条消息处理两遍，结果一样。
- **顺序错乱也无妨：** 消费者只做删除，删除与顺序无关：不论先处理哪条，最终缓存都是空的，下一次读会回源拿到最新值。
- **一定要保证的：** 消费失败要重试，否则缓存会一直留着旧值。
- **代价是延迟：** 多了一条异步链路，增加几十到几百毫秒的延迟，这段时间缓存仍是旧值，所以要监控消费延迟，设告警。
- **要写后立刻读到新值的场景：** 写后的读走主库，或这次请求绕过缓存。
**举个例子。** 客服用脚本批量改了一批订单状态，没有经过业务服务：
1. **脚本执行：** 直接 `UPDATE` 数据库里 1000 个订单的状态。
2. **binlog 记录：** 数据库提交后，把这 1000 行的变更写进 binlog。
3. **Canal 解析：** 拉到 binlog，取出表名和每行的主键，发到 MQ。
4. **消费者：** 按主键逐个删除 Redis 里对应的订单缓存。
5. **用户再读：** 缓存未命中，回源读库，得到最新状态。
6. **如果消息乱序或重复：** 删除无所谓顺序，重复删也只是多一次未命中。
**容易错。**
- **以为 binlog 删缓存没有延迟：** 多一条异步链路，有几十到几百毫秒的延迟，要监控。
- **担心消息乱序要加排序：** 只做删除，顺序无关，不需要排序。
- **只有这一条路径：** 它是兜底和统一入口，写路径里的同步删和 TTL 仍然保留。
- **消费失败不重试：** 缓存会一直留旧值，必须重试。
**业务场景。** 客服用脚本批量改了一批订单状态，没走业务服务；binlog 消费者照样删掉对应缓存，不会留旧状态。
**系统设计。** [[links.tt-cache-consistency-hot-keys|缓存一致性与热点 Key]]：收尾：问「你的方案对运维直接改库也成立吗」，答 binlog 订阅，并说明它的延迟代价。
**可能问法。**
- Canal 删缓存的链路怎么设计？ → Canal 模拟从库协议拉取数据库的 binlog（Debezium 也是读 binlog），解析出变更行的表和主键，投到消息队列，由专门的消费者按主键删除缓存。业务代码不用管缓存，手工改库、运维脚本这些写入路径也都会触发。
- binlog 消息乱序会怎样？ → 无妨。消费者只做删除，删除是幂等的，也与顺序无关：不论先处理哪条，最终缓存都是空的，下一次读会回源拿到最新值，重复消息同理。要保证的是消费失败会重试，否则缓存会一直留着旧值。
- 这个方案的延迟多大？ → 多一条异步链路，增加几十到几百毫秒延迟，这段时间缓存仍是旧值，所以要监控消费延迟并设告警。需要写后立刻读到新值的场景，写后的读走主库或这次请求绕过缓存。
