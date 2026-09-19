---
id: kafka-monitoring-throttle-silent-must-monitor
node: monitoring.client-metrics
type: qa
step: 6
source: kafka-2e
---
## Q
当一个生产者或消费者客户端的流量超出了配额被 broker 节流（throttle）时，broker 返回给客户端的响应里会不会带一个「你被限流了」的错误码？这对监控策略意味着什么？

## A
不会。broker 节流的方式是延迟响应客户端的请求，而不是在响应里携带专门的节流错误码，所以从应用程序的角度看，被节流只表现为请求变慢，程序本身根本不知道这是配额限制造成的还是别的原因造成的。这意味着如果不主动监控 `produce-throttle-time-avg`、`fetch-throttle-time-avg` 这类节流时间指标，就完全无法察觉客户端正在被限流；即使当前集群还没有开启配额限制，也建议提前把这些指标接入监控，因为配额随时可能在未来被启用，比出问题后再补监控要容易得多。
