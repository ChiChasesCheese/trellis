---
id: kafka-practice-azure-disk-tier-sla
node: practice.cloud-deployment
type: qa
step: 4
source: kafka-2e
---
## Q
在 Azure 上为 Kafka broker 选托管磁盘时，托管机械磁盘、高级固态硬盘（Premium SSD）、超级固态硬盘（Ultra SSD）这几档存储在价格、性能和可用性保证（SLA）上有什么区别？

## A
托管机械磁盘价格相对便宜，但微软没有为它提供明确的可用性 SLA（服务级别协议）承诺；高级固态硬盘或超级固态硬盘价格更贵，但读写速度快得多，而且微软为它们提供了99.99%的可用性 SLA。因此，如果业务要求非常低的延迟或需要明确的可用性保证，应该选择高级/超级固态硬盘；如果对延迟不敏感、更看重成本，托管机械磁盘或者甚至 Blob 存储就足够了。
