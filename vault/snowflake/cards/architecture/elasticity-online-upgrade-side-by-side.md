---
id: elasticity-online-upgrade-side-by-side
node: architecture.elasticity-multitenancy
type: qa
tags: [grown]
---
## Q
Snowflake 作为共享服务频繁发布新版本，为什么升级不需要停机维护窗口？

## A
服务是无状态的，所有状态都在共享的元数据存储和对象存储中，因此新版本的服务可以与旧版本并排部署。用户请求被逐步切换到新版本，已在旧版本上运行的查询继续跑完，旧版本排空后再下线；如果新版本有问题，也可以把流量切回旧版本。由于新旧版本读写的是同一份元数据和数据，切换过程中无需迁移数据。
