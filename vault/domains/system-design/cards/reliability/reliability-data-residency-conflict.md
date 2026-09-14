---
id: reliability-data-residency-conflict
node: reliability.multi-region
type: qa
---
## Q
Data residency law says EU user data stays in the EU, but your DR plan fails everything over to us-east. How do these conflict, and what architecture resolves it?

## A
Residency caps where data may be **replicated** — you cannot fail EU data over to a US region, so a global active-passive design is illegal for that data, and residency shrinks your failure-domain choices.

Standard resolution: **partition by user home region** —

- Each user's data lives and replicates **only within its jurisdiction** (e.g. two EU regions for EU users) — failover stays in-boundary.
- A thin **global layer** (routing/directory metadata, nothing personal) sends each request to the user's home partition.
- Accept the trade: an EU user traveling in the US eats cross-ocean latency; that's the compliance cost, not a bug.

## Q zh
数据驻留法说欧盟用户数据停留在欧盟，但你的 DR 计划对所有东西故障转移到 us-east。这些如何冲突，什么架构解决它？

## A zh
驻留上限数据可能**复制**的地点——你不能将欧盟数据故障转移到美国区域，所以全球 active-passive 设计对该数据是非法的，驻留缩小你的故障域选择。

标准解决方案：**按用户主区域分割**——

- 每个用户的数据只在其司法管辖区内生存和复制**（例如欧盟用户的两个欧盟区域）——故障转移停留在边界内。
- 一个薄**全球层**（routing/directory 元数据，没有个人信息）将每个请求发送到用户的主分割。
- 接受权衡：在美国旅行的欧盟用户吃跨洋延迟；那是合规成本，不是错误。
