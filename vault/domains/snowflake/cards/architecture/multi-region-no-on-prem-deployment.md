---
id: multi-region-no-on-prem-deployment
node: architecture.cloud-agnostic-multi-region
type: qa
source: snowflake-docs
---
## Q
一家公司出于合规考虑想把 Snowflake 部署在自己机房或私有云里，为什么做不到？这对“跨云”意味着什么？

## A
Snowflake 是自托管服务（self-managed service）：它只运行在公有云基础设施上，用云厂商的虚拟计算实例和持久化存储承载计算与数据，软件升级与基础设施都由 Snowflake 管理，因此不能在本地（on-premises）或私有云上安装运行。所谓“跨云”指的是在不同公有云（AWS、Azure、Google Cloud）之间运行同一套服务，而不是覆盖用户自有的基础设施。
