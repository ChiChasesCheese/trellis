---
id: kafka-monitoring-sli-slo-sla-ola-terms
node: monitoring.metrics-and-slo
type: qa
step: 4
source: kafka-2e
---
## Q
工程师、经理、高管常常混用「服务级别」相关的术语。SLI（服务级别指标）、SLO（服务级别目标，也叫SLT）、SLA（服务级别协议）、OLA（运营级别协议）这四个术语分别描述的是什么，它们之间是什么关系？

## A
SLI（service level indicator）是描述服务可靠性的一个客观指标，通常表示为「正常事件数/总事件数」的比率，比如 Web 服务器返回 2xx/3xx/4xx 响应的请求占比。SLO（service level objective，也叫 SLT，service level threshold）是把一个 SLI 和一个目标值、以及一个时间窗口组合起来，例如「7天内99%的请求要返回2xx/3xx/4xx」。SLA（service level agreement）是服务提供方和客户之间的契约，通常包含若干条 SLO，加上如何度量报告、客户如何寻求支持、违约会有什么惩罚等条款——SLA 建立在 SLO 之上，而不是反过来。OLA（operational level agreement）则很少被提及，它描述的是为了整体交付 SLA，内部多个团队或供应商之间达成的协作协议，确保日常运营真的在做支撑 SLA 所需的事情。
