---
id: craft-bounded-containers-every-dict-has-an-exit-5-across-problems-and-scales
node: craft.patterns.bounded-containers-every-dict-has-an-exit
type: qa
step: 5
---
## Q
**有界容器 · LRU 缓存、限流器、TTL 缓存、键值库、通知去重、消息主题里的同一个问题**｜模式

这六个问题里都有一个以外部输入为键的字典。它们各自用什么当出口？放大到生产系统，同一个问题有哪些名字？

## A
**要点。** 出口只有四种：容量上限（满了淘汰谁）、过期时间（多久没用或到期）、等价于初始状态（可以删）、所有者离开（退订、关闭）。每个字典必须能说出自己用的是哪一种。

```python
# LeetCode 146 LRU Cache：容量上限是出口
self.d[key] = value; self.d.move_to_end(key)
if len(self.d) > self.cap: self.d.popitem(last=False)
# rate-limiter：状态与新建的等价就删，摊还触发
for key in [k for k, s in shard.states.items() if s.is_idle(now)]: del shard.states[key]
# notification-service：超过 TTL 的去重记录，满容量时先清一遍
if len(self._entries) >= self._capacity: self._purge_locked(now)
```

**见于。** lru-cache、rate-limiter、ttl-cache、kv-store、notification-service、pub-sub。

**不变的。** 谁创建这一项，谁负责说明它什么时候消失；清理的触发条件不能依赖会无限增长的量；主表与旁路结构一起清；用计数属性把「有界」变成可测试的断言。**变化的。** 出口的种类，和清理的执行时机（访问时、摊还、定时）。

**信号。** 看到 `dict[外部输入, ...]`、`defaultdict`、`setdefault`、`self._xxx[key] = ...` 而在整个类里找不到对应的 `del` 或 `pop`。

**尺度对照。** 力扣：容量上限（LRU）。低层设计：TTL、摊还回收、计数断言。生产系统：Redis 的 `maxmemory` 加淘汰策略和 key 过期；监控里的**标签基数**（cardinality）爆炸，指标的标签值来自用户输入（用户 id、URL），每个值多一条时间序列，就是同一个无界字典的分布式版本；消息队列的保留策略（按时间或大小截断日志）。变化：单机里泄漏是 OOM 重启，分布式里泄漏是账单和查询变慢，而且出口往往要由系统外的人（运维、配额）来设，所以限制要写进配置（上限、TTL），不能靠约定。
