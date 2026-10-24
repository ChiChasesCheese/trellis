# TikTok 后端基础（八股）：九个主题，一小时怎么走

后端基础（八股）是技术面里的一段：要么占一场技术面的前 20–30 分钟（简历拷问之后），要么单独一场约 45 分钟。面试官从你简历上用过的技术切入，沿着一条线往下挖，直到你答不上来为止；所以每个主题要准备到「机制 → 为什么 → 数字或取舍 → 追问」四层。下面九页每页 8–15 个问题，每个问题都有可以直接口述的答案和常见追问。

## 一小时怎么走

1. **0–5 分钟**：自我介绍后，面试官挑一个你简历上的组件（Redis、Kafka、MySQL）问「你们怎么用的」，先答用法和规模，再准备被追问原理。
2. **5–25 分钟**：沿着一个主题深挖 4–6 层。典型链条：Redis 分布式锁 → 锁过期怎么办 → 看门狗 → 主从切换丢锁 → RedLock 与它的批评；或 Kafka 分区 → 顺序 → 不丢消息 → 重平衡 → 积压。
3. **25–40 分钟**：换一个主题或进入场景题：「QPS 涨 10 倍」「磁盘满了」「订单重复扣款」「输入 URL 发生了什么」。这时重点是有条理：先说判断顺序，再说命令和手段。
4. **40–50 分钟**：按岗位补语言运行时（Java 的 HashMap / 线程池 / GC，Go 的 GMP，Python 的 GIL）。只准备自己主语言，其余了解到能比较。
5. **最后 5 分钟**：你的提问。答不出来的题要说「我的理解是……，不确定的是……」，不要编；能给出排查思路也算分。

## 九个主题

| 主题 | 页面 | 会被问到的核心 |
|---|---|---|
| Redis | [[tiktok-redis]] | 分布式锁（SET NX + Lua、看门狗、RedLock 及批评）、数据结构、持久化、主从与 Cluster |
| MySQL | [[tiktok-mysql]] | B+ 树索引、隔离级别与 MVCC、间隙锁、慢查询、深分页、分库分表 |
| 缓存问题 | [[tiktok-cache-problems]] | 穿透、击穿、雪崩、缓存一致性、热 key、大 key |
| 消息队列 | [[tiktok-message-queues]] | Kafka 分区、重平衡、顺序、不丢消息、积压、死信 |
| 幂等与分布式事务 | [[tiktok-idempotency-transactions]] | 幂等键、2PC、TCC、SAGA、outbox、对账 |
| 运行时与并发 | [[tiktok-runtime-concurrency]] | ConcurrentHashMap、线程池、GC；Go GMP；Python GIL |
| 服务保护 | [[tiktok-service-protection]] | 限流、熔断、降级、重试退避、10 倍流量突增、秒杀 |
| 网络与操作系统（low priority） | [[tiktok-networking-os]] | TCP 握手与 TIME_WAIT、TLS、DNS、输入 URL 发生了什么、虚拟内存 |
| Linux 线上排查（low priority） | [[tiktok-linux-troubleshooting]] | 磁盘满、CPU 高、内存与 OOM、网络慢、容器 |

## 复习顺序

- **先练前四页**（Redis、MySQL、缓存、消息队列）：它们占一场八股的大部分时间，而且题与题之间互相接着问。
- **再练幂等与事务、服务保护**：支付、订单类的系统设计和场景题几乎都会落到这里；与简历项目结合时最能拉开差距。
- **然后按主语言读运行时**，最后读网络与 Linux 排查。
- 每页末尾的速记表用来自测：盖住右列，用一句话说出答案，说不出来就回到对应的问题。

## 相关页面

- 系统设计中的支付、限流、排行榜：[[tiktok-sd-index]]
- 整个 TikTok 面试流程：[[interviews/companies/tiktok/README]]
