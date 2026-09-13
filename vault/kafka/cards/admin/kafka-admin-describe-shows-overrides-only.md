---
id: kafka-admin-describe-shows-overrides-only
node: admin.dynamic-config
type: qa
source: kafka-2e
---
## Q
用 `kafka-configs.sh --describe` 查看一个主题的配置时，输出里只列出了 `retention.ms=3600000` 这一行，这是不是说明这个主题只有 retention.ms 这一个配置项，其余配置都是空的？如果要做自动化脚本读取主题的完整有效配置，这一点意味着什么？

## A
不是。`--describe` 命令只显示被**动态覆盖**过的配置，主题上其它所有沿用集群默认值的配置项根本不会出现在这份输出里，而且这个命令本身也无法动态查到 broker 级别的默认值是什么。这意味着如果自动化流程只依赖这个命令的输出去判断某个主题「实际生效」的完整配置，会遗漏所有走默认值的参数；要拿到完整有效配置，必须结合对集群默认配置（broker 级别的静态配置）的了解，而不能只看 --describe 的覆盖列表。
