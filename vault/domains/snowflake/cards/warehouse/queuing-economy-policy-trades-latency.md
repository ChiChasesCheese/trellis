---
id: queuing-economy-policy-trades-latency
node: warehouse.query-queuing
type: qa
source: snowflake-docs
---
## Q
多集群仓库（multi-cluster warehouse）已开启 Auto-scale，却仍频繁观察到查询排队，而且集群数远没到上限。最可能是哪项配置导致的？

## A
伸缩策略（scaling policy）被设为 Economy。Economy 以省 credit（信用点）为先：只有估计新增负载足以让一个新集群至少忙 6 分钟时才启动它，倾向让现有集群保持满载，因此会接受查询排队、完成时间变长。若更看重响应时间，应改回默认的 Standard 策略——只要有查询排队或估计资源不足就加集群。
