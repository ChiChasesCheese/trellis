---
id: bagu-link-metrics-monitoring-alerts-1-map
node: links.metrics-monitoring-alerts
type: qa
step: 1
---
## Q
**指标监控与告警平台 · 会被追问哪些八股**｜必会

设计指标监控与告警平台时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 写极多、读很少的时序问题。基础是：LSM 追加写、可观测性三件套与基数、各资源告警的口径、告警风暴与排查信息、队列与 Redis 的专项指标。

**下钻路线。**
- 指标写入存储为什么偏好 LSM → 追加写吞吐高，按时间范围顺序扫，[[b.search.lsm-vs-btree|LSM-Tree 与 B+ Tree 的本质区别]]
- 标签基数爆炸 → 不要把 user_id 当标签，按指标和租户限制序列数，[[b.scenario.timeseries-cardinality|时序基数与降采样]]
- 磁盘告警 → 使用率 80% 预警，同时配 inode 使用率，[[b.linux.disk-full|磁盘满了怎么处理]]
- 内存告警规则 → 看 available 和 swap 增长，不看 free，[[a.linux.mem-oom|内存占用高与 OOM 怎么查]]
- 告警风暴怎么避免 → 阈值看饱和度，分级抑制，[[a.protect.spike-10x|QPS 突增 10 倍怎么应对]]
- 值班拿到什么才能快速判断 → 范围（实例、接口）和最近变更，[[a.linux.general-method|线上排查通用思路与「服务突然变慢」完整清单]]
- 平台自己监控消息队列 → lag 绝对值与增速双告警，[[a.mq.backlog|消息积压怎么办]]
- Redis 延迟告警触发后 → 先慢日志，再看 fork、AOF、swap、碎片，[[b.redis.blocking-slow|Redis 变慢与阻塞的常见原因]]

**业务场景。** 监控支付渠道：某个渠道批准率下跌，UNKNOWN 状态的数量与存活时间超阈值就要告警，告警里要带渠道维度。
**系统设计。** [[links.metrics-aggregator|指标聚合系统（计数指标 + 直方图仪表盘）]]：写入侧同样先聚合，但这里多了告警状态机；[[links.github-cicd-workflow|CI/CD 平台（类 GitHub Actions）]]：同样看构建与发布的指标，范围更窄。
