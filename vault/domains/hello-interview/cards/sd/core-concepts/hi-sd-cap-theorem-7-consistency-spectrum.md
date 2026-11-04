---
id: hi-sd-cap-theorem-7-consistency-spectrum
node: qb.sd.distributed-rate-limiter.pre-sd-core-concepts-cap-theorem
type: qa
step: 7
---
## Q
**一致性强度的谱系**｜系统设计 · 核心概念

除了强一致与最终一致，还有哪些常被提到的一致性级别？各自适合什么场景？

## A
**由强到弱。**
- 强一致（strong）：所有读都反映最近一次写，性能代价最大，用于账户余额这类要绝对准确的数据
- 因果一致（causal）：有因果关系的事件对所有人顺序一致，如评论必须出现在帖子之后
- **读己之写**（read-your-own-writes）：用户总能立刻看到自己的更新，别人可以暂时看到旧版本；社交平台改资料常用
- 最终一致（eventual）：暂时不一致但会收敛，如 DNS；多数分布式数据库默认如此，选择可用性时就隐含选了它

**说法。** CAP 里谈的一致性通常指第一种。把需求精确到某个级别，比泛泛说「弱一致」更有说服力。
