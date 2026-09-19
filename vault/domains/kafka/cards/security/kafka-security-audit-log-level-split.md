---
id: kafka-security-audit-log-level-split
node: security.audit-hardening
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka broker 的授权器日志里，一次被拒绝的访问记录在 INFO 级别，一次被允许的访问却只记录在 DEBUG 级别。这样按结果区分日志级别，对安全审计有什么好处？

## A
生产环境通常默认持续采集 INFO 级别日志，而 DEBUG 级别默认关闭以避免日志量爆炸。把「拒绝访问」这类更值得关注的安全事件放在 INFO 级别，意味着不需要专门为了审计而打开高噪声的 DEBUG 日志，就能持续监控未授权访问尝试（比如某个身份反复访问自己无权限的主题）；而「允许访问」的正常流量数据量巨大，只在排查具体授权问题时才临时打开 DEBUG 收集。
