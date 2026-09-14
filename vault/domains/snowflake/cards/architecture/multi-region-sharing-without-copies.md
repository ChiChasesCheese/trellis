---
id: multi-region-sharing-without-copies
node: architecture.cloud-agnostic-multi-region
type: qa
source: snowflake-docs
---
## Q
数据提供方在 AWS 区域、使用方在 Azure 区域，Snowflake 用什么方式把数据交付过去？相比导出文件再搬运有什么好处？

## A
通过 listings（数据列表）等协作功能，由 Snowgrid（跨区域、跨云技术层）打通不同区域和云厂商。好处是提供方始终掌控访问权限，也不必自己在多个地方维护同步的数据副本；手工导出再导入则会产生多份各自漂移、难以撤销权限的拷贝。
