---
id: kafka-monitoring-static-vs-dynamic-quota
node: monitoring.client-metrics
type: qa
source: kafka-2e
---
## Q
配置 Kafka 客户端配额既可以写在 broker 静态配置文件里（如 `quota.producer.default`），也可以用 `kafka-configs.sh` 或 AdminClient 动态设置。为什么说「特定客户端的配额通常采用动态配置」而不是写进静态配置文件？

## A
写在 broker 配置文件里的配额是静态的，任何修改都需要重启所有 broker 才能生效；但实际业务里客户端是不断有新的加入、旧的下线的，如果每次要给某个新客户端单独设定配额都必须重启整个集群，运维成本极高而且有风险。动态配置则可以通过命令行工具或 AdminClient 在线修改某个客户端 ID 或用户的配额，不需要重启任何 broker，能够灵活应对客户端数量和需求的变化，所以特定客户端/用户的配额几乎总是用动态配置而不是写进静态文件。
