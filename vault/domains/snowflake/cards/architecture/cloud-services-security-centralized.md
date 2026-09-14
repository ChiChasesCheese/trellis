---
id: cloud-services-security-centralized
node: architecture.cloud-services-layer
type: qa
source: snowflake-docs
---
## Q
Snowflake 中有很多相互独立的虚拟仓库（virtual warehouse），为什么认证与访问控制（access control）不会因为仓库不同而出现不一致的规则？

## A
因为安全、认证与访问控制由云服务（Cloud Services）层统一管理，而不是由各个虚拟仓库各自实现。所有请求在进入任何仓库之前都要经过同一层做身份认证和权限检查，同一层还负责 Horizon Catalog（治理目录）和合规（regulatory compliance）等服务，所以规则只有一份，对所有仓库一致生效。
