---
id: anchor-enables-rolling-upgrade
node: metadata.execution-anchor
type: qa
tags: [grown]
---
## Q
云服务（Cloud Services）实例需要升级或缩容时，如果不支持执行锚点（execution anchor）的主动转移，会带来什么运维代价？

## A
那就只能等实例上所有长时间运行的查询自然结束才能下线（可能要几小时），或者直接杀掉这些查询让用户重跑。支持主动转移后，实例可以把正在锚定的查询有序地交给其他实例，自己尽快排空下线，从而实现不打断用户查询的滚动升级和弹性缩容。
