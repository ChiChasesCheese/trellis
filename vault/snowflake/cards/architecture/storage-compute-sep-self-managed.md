---
id: storage-compute-sep-self-managed
node: architecture.storage-compute-separation
type: qa
source: snowflake-docs
---
## Q
作为一个自管理服务（self-managed service），Snowflake 在存储和计算两侧分别替用户省去了哪些工作？

## A
在计算侧，用户不需要选型、安装、配置或管理任何虚拟或物理硬件来运行虚拟仓库；在存储侧，用户也几乎不需要安装或配置任何软件来管理持久化数据的组织、压缩与文件布局。Snowflake 负责这两侧运行在公有云基础设施上的软件更新、日常维护与调优，用户无法在本地或私有云上自行部署 Snowflake。
