# 评分 rubric（五维，1–4 分/维，满分 20）

## 1. Problem framing

- **1 分**：直接说"查一张 permissions 表，有记录就放行"，不提继承、拒绝优先、吊销延迟、agent
  主体。
- **4 分**：复述后说出不变量：**deny 永远覆盖 allow**（无论 deny 来自哪一层继承）；**吊销必须
  在有界的时间窗内对所有读路径生效**（不能"永久缓存"出一个已吊销却仍放行的决策）；**每次决策
  可审计**（主体、资源、动作、结果、依据的策略版本）；**agent 的权限是委托它的用户当前权限的
  受限子集，随用户权限变化而变化**，不是创建时的快照。明确"不做"：不保证跨区域瞬时强一致；不
  是通用图查询引擎；批量"我能访问哪些资源"不保证与单次点查同样的延迟 SLA。

## 2. API & data model

- **1 分**：只有 `permissions(principal, resource, action)` 一张宽表，没有角色继承、没有资源
  层级、没有版本号。
- **4 分**：API：`POST /authorize {principal, action, resource} → {allow|deny, reason,
  policy_version}`、批量 `POST /authorize/batch`、管理面 `PUT/DELETE grant`、`GET /audit`；
  数据模型分层——**身份层** `principals(id, type: human|agent|service, delegated_by)`、**资源
  层** `resources(id, parent_id, type)` 形成有向无环的层级、**策略层**
  `role_assignments(principal, role, scope, expiry)` + `grants(subject, permission,
  resource_pattern, effect: allow|deny, policy_version)`；agent 主体额外带 `delegated_by` 与
  `expiry`，校验时对 agent 的决策 = **agent 自身授权 ∩ delegated_by 当前授权**（不是快照）。

## 3. Failure modes & scale

- **1 分**：权限缓存加 TTL 就算完事；吊销和读路径的竞态没讨论；centralized 服务挂了怎么办没
  提；没想到角色继承图可能出现环。
- **4 分**：讲清**吊销与缓存的竞态**——用**策略版本号 + 推送式失效**（吊销时给受影响的
  `(principal, resource)` 缓存条目发失效事件）加**兜底短 TTL**（推送丢失时最坏情况的 staleness
  上界，比如 5 秒）；**角色继承图必须在写入时拒绝环**（增量环检测，不是每次读时遍历判环）；
  **中心服务不可用时按资源敏感度分级降级**——高敏感资源 fail-closed（宁可拒绝也不误放行），低
  敏感只读场景可以用"上一次已知良好决策 + 短宽限期"的断路器兜底，两种都要明确讲，不能只说
  "fail open 保可用性"；**热点资源**（被几千个查询同时校验的共享表）用旁路缓存 + 推送失效而不
  是每次打中心服务；**审计写放大**：审计写不能阻塞授权决策返回，但也不能丢——本地持久化缓冲 +
  异步落盘 + 失败重试对账。

## 4. Separation of concerns

- **1 分**：一个服务同时管身份、策略存储、图遍历、审计写入、缓存失效全部耦合在一起。
- **4 分**：**客户端 SDK / sidecar 缓存**（本地判定 + 推送/拉取失效）→ **授权 API**（无状态，
  评估层级 + deny-wins）→ **策略存储**（强一致、有版本号的 source of truth）→ **继承图 / 可达
  性索引**（角色图的环检测与预计算 reachability，独立于热路径可以异步刷新）→ **失效推送总线**
  （吊销事件广播给所有缓存）→ **审计服务**（独立、异步、可重放）。

## 5. Delivery beyond the diagram

- **1 分**：画完就停。
- **4 分**：影子模式——新服务与旧权限判断并行跑，逐条 diff 决策结果，先找出"新服务多放行了什么"
  再上线；吊销延迟（p99 失效生效时间）、误放行次数（目标 0，出现即 page）、审计完整率作为核心
  指标；灰度按资源敏感度分级/按租户逐步启用；故障演练：失效推送丢失、策略存储只读降级、agent
  委托链断裂（delegated_by 被删）时的行为；能类比 Snowflake：Horizon 的 AI Agent Identity 正是
  "agent 权限 = 用户权限的受限子集，且随之变化"这条不变量的产品级实现，RBAC/grant 的元数据集中
  在 FoundationDB。
