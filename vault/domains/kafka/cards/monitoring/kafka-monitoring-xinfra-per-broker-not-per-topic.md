---
id: kafka-monitoring-xinfra-per-broker-not-per-topic
node: monitoring.lag-e2e
type: qa
step: 6
source: kafka-2e
---
## Q
理想情况下，端到端监控应该对集群里每一个主题都验证一遍读写是否正常，但 Xinfra Monitor（原名 Kafka Monitor）这类工具实际上把验证粒度下沉到了 broker 级别而不是主题级别，为什么？

## A
如果要对集群里的每一个真实业务主题都专门注入一份人工合成流量来验证读写，主题数量一多（可能成百上千个），这种做法的开销和复杂度会变得不现实。折中的办法是构造一个横跨集群所有 broker 的专用主题，持续向这个主题的每个 broker 生成并读取消息，以此监控每个 broker 上生产请求和读取请求的可用性以及读写之间的延迟，只要每个 broker 本身工作正常，跑在它上面的所有真实业务主题大概率也是正常的，这样用远小得多的成本获得了对整个集群健康状况有代表性的观测。
