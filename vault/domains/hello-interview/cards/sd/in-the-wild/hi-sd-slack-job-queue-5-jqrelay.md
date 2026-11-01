---
id: hi-sd-slack-job-queue-5-jqrelay
node: sd.in-the-wild.slack-job-queue
type: qa
step: 5
---
## Q
**JQRelay：受控排空与限速**｜系统设计 · 业界案例

Kafka 里的任务怎样可靠、可控地流入 Redis？同一个主题怎样避免多个中继重复处理？

## A
**要点。** JQRelay 每个实例把一个 Kafka 主题中继到对应的 Redis 集群。协调靠 Consul 的分布式锁：启动时尝试获取某个主题的锁，拿到的才中继该主题的全部分区；一旦丢锁就释放一切并重启，让别的实例接手。实例在自动伸缩组里，替换也走同一流程，因此每个主题始终只有一个中继。

```python
for job in consume(topic, partition):
    write_to_redis(job)        # Redis 不可用时无限重试，日志在背后继续吸收新任务
    commit_offset(partition)   # 只有 Redis 写入成功之后才提交偏移
```

**为什么。** 先写 Redis 再提交偏移，保证至少一次，不会丢；个别任务出错就重新入队到 Kafka，不阻塞整体。

**取舍。** 限速配置放在 Consul，通过 watch 接口动态生效：积压期间 Web 应用仍满速入队，运维把中继调慢到 worker 能消化的速度，积压落在磁盘上而不是内存里。
