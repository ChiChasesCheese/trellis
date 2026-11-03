---
id: craft-observability-as-design-4-three-places-from-lld-to-slo
node: craft.architecture.observability-as-design
type: qa
step: 4
---
## Q
**可观测性即设计 · 一个进程内的丢弃计数，放到分布式系统里变成什么**｜架构

发布订阅的 `lagged_count`、熔断器的拒绝计数、重试用尽的失败计数，在一个进程里就是几个整数。同样的设计放到多机的消息系统里，对应的东西是什么，要多做什么？

## A
**要点。** 判断「该打什么指标」只需要问三个问题：哪里会**丢**、哪里会**拒**、哪里会**重试或降级**？进程内的每一处都是一个计数器；到了分布式系统，这些计数器变成按服务、按主题切分的指标，再被 SLO（服务等级目标）引用，比如丢弃率、重试率。

```python
@property
def lagged_count(self) -> int:
    """因为日志淘汰而**没看到**的消息条数。丢弃必须可观测，否则 DROP_OLDEST 就是静默丢数据。"""
    with self._state_lock:
        return self._lagged

@property
def failed_count(self) -> int:
    """重试用尽后仍然失败、交给失败策略处理的消息条数。"""
    with self._state_lock:
        return self._failed
```

发布订阅题解里这两个计数分别对应「丢」与「重试用尽」；熔断器的 `Metrics` 对应「拒」（`rejected`）；日志框架的 `dropped_count` 与 `error_count` 对应丢与内部出错。

| 进程内 | 分布式对应 |
|---|---|
| 消费者掉队丢失条数 | 消费者滞后（consumer lag）、保留期内被淘汰的偏移量 |
| 重试用尽的失败数 | 死信队列（dead letter queue）长度 |
| 熔断器拒绝数 | 下游错误预算（error budget）消耗、被限流比例 |
| 状态转移留痕 | 审计日志 |

**为什么。** 指标、日志、追踪各有分工：计数回答「多少」，留痕回答「谁、什么时候」，追踪回答「慢在哪」。这些都得在写代码时就留好位置，上线后再补，往往要改动控制流程。

**易错。** 计数器能数的只是你想到的地方。新增一条「丢弃」路径（例如一个新的超时分支）时，同时问「它的计数在哪」，把它写进评审清单；指标的个数多了，每条要有明确的所有者和阈值，否则只是噪声。
