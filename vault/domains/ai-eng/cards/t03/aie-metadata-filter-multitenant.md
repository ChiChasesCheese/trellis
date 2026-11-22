---
id: aie-metadata-filter-multitenant
node: t03.metadata-filtering-multi-tenant
type: qa
step: 1
tags: [实践]
---
## Q
**Multi-tenant RAG · 在检索阶段做权限隔离**｜实践 · 必会

一个 SaaS 的知识库问答要服务 500 个客户，每个客户只能看到自己的文档。你把所有文档放进一个索引，生成后再把别家内容遮掉，行不行？

## A
**不行：** 别人的文档已经进入了 prompt，模型可能泄露，或者被注入利用。权限必须在**检索阶段**就生效，别家的 chunk 根本进不到 context。

**两种实现（以 Pinecone 文档为例）：**

| 方式 | 做法 | 特点 |
|---|---|---|
| **namespace** | 每个租户一个 namespace，查询只指向该 namespace | 物理隔离；下线租户直接删 namespace；搜索成本按 namespace 大小计 |
| **metadata filter** | 全部放一个 namespace，每个 chunk 带 `tenant_id`，查询时加过滤条件 | 要跨租户搜索时才方便；搜索会扫整个 namespace，大 namespace 延迟高 |

- 官方示例：100 个各 1 GB 的租户，搜一个租户花 1 RU（按 1 GB 1 RU 计）；在一个 100 GB 的 namespace 里过滤要花 100 RU。
- 过滤条件的 `$in` / `$nin` 每个最多 10,000 个值；按一长串用户 ID 过滤是反模式，改用访问控制组、namespace 或客户端后过滤。

**先过滤还是后过滤：**
- **pre-filter**（过滤在检索时）：只在有权限的文档里取 top-k；
- **post-filter**（取完 top-k 再过滤）：可能 top-k 全是无权限的，过滤后什么都不剩，召回率塌掉。

**检查：** 写一个测试：用租户 A 的身份问只有租户 B 的文档里才有的问题，应当「查无此事」。

**出处：** Pinecone 文档 docs.pinecone.io/guides/index-data/implement-multitenancy（2026-11-21 读）；pre/post-filter 对比为通用向量检索实践
